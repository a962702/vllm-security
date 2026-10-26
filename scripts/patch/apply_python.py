"""Apply a gen_patch.py plan inside the image being patched (stdlib only).

Usage: python3 -I apply_python.py <plan.json> <result.json>

Each package is installed on its own, with every other installed package pinned
to its current version, so one unresolvable upgrade neither blocks the others
nor drags torch & co. to new versions. Failures are recorded in the result file
instead of failing the build; scan.sh decides what to do with them.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def version_key(version: str) -> list:
    parts = re.split(r"[.\-+]", version)
    return [(0, int(p), "") if p.isdigit() else (1, 0, p) for p in parts]


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def find_python(site_dir: str) -> str | None:
    """Interpreter whose sys.path contains site_dir."""
    match = re.match(r"(.*)/lib/(python\d+\.\d+)/(?:site|dist)-packages$", site_dir)
    if not match:
        return None
    prefix, pyver = match.groups()
    candidates = [f"{prefix}/bin/{pyver}", f"{prefix}/bin/python3", f"/usr/bin/{pyver}"]
    for exe in candidates:
        if not os.access(exe, os.X_OK):
            continue
        out = subprocess.run([exe, "-I", "-c", "import sys, json; print(json.dumps(sys.path))"],
                             capture_output=True, text=True)
        if out.returncode == 0 and site_dir in json.loads(out.stdout):
            return exe
    return None


def installer(python: str, venv: bool) -> dict[str, list[str]] | None:
    """list / install / check commands for this interpreter: uv if present, else pip."""
    extra = [] if venv else ["--break-system-packages"]
    if shutil.which("uv"):
        return {"list": ["uv", "pip", "list", "--python", python, "--format", "json"],
                "install": ["uv", "pip", "install", "--python", python, "--no-cache", *extra],
                "check": ["uv", "pip", "check", "--python", python]}
    if subprocess.run([python, "-m", "pip", "--version"], capture_output=True).returncode == 0:
        return {"list": [python, "-m", "pip", "list", "--format", "json"],
                "install": [python, "-m", "pip", "install", "--no-cache-dir", *extra],
                "check": [python, "-m", "pip", "check"]}
    return None


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(proc.stdout[-4000:])
    sys.stdout.write(proc.stderr[-4000:])
    return proc


# `uv pip check`: "The package `opentelemetry-sdk` requires `opentelemetry-api==1.40.0`, but ..."
# `pip check`:    "opentelemetry-sdk 1.40.0 has requirement opentelemetry-api==1.40.0, but ..."
UV_ISSUE = re.compile(r"The package `([^`]+)` requires")
PIP_ISSUE = re.compile(r"^(\S+) \S+ (?:has requirement|requires) ")


def parse_dependency_issues(output: str) -> dict[str, str]:
    """Broken requirements -> the package whose requirement is broken.

    Keys drop the ", but X is installed" tail, so a conflict that existed before
    patching still matches its baseline entry after the installed side moves.
    """
    issues = {}
    for line in output.splitlines():
        line = line.strip()
        match = UV_ISSUE.search(line) or PIP_ISSUE.match(line)
        if match:
            issues[line.split(", but ")[0]] = normalize(match.group(1))
    return issues


def dependency_issues(check_cmd: list[str]) -> dict[str, str]:
    proc = subprocess.run(check_cmd, capture_output=True, text=True)
    return parse_dependency_issues(proc.stdout + proc.stderr)


def installed_versions(list_cmd: list[str]) -> dict[str, str] | None:
    listed = run(list_cmd)
    if listed.returncode != 0:
        return None
    return {normalize(p["name"]): p["version"] for p in json.loads(listed.stdout)}


def install(install_cmd: list[str], installed: dict[str, str], floating: set[str],
            requirements: list[str]) -> subprocess.CompletedProcess:
    """Install requirements with every installed package outside `floating` pinned."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as pins:
        for name, version in sorted(installed.items()):
            if name not in floating:
                pins.write(f"{name}=={version}\n")
    try:
        return run([*install_cmd, "-c", pins.name, *requirements])
    finally:
        os.unlink(pins.name)


MAX_ROUNDS = 3


def upgrade(pkg: dict, tools: dict[str, list[str]], installed: dict[str, str]) -> dict:
    """Upgrade one package without introducing new dependency conflicts.

    When the upgrade breaks a requirement of another installed package (e.g.
    opentelemetry-sdk pinning opentelemetry-api exactly), those dependents are
    upgraded along with it; everything else stays pinned. If that still leaves
    new conflicts, every package touched is put back to its original version.
    """
    target = normalize(pkg["name"])
    baseline = dependency_issues(tools["check"])
    floating = {target}
    reason = ""
    for _ in range(MAX_ROUNDS):
        proc = install(tools["install"], installed, floating, [pkg["spec"], *sorted(floating - {target})])
        if proc.returncode != 0:
            reason = " / ".join((proc.stderr or proc.stdout).strip().splitlines()[-3:])
            break
        new = {line: req for line, req in dependency_issues(tools["check"]).items() if line not in baseline}
        if not new:
            result = {"name": pkg["name"], "status": "upgraded", "from": installed.get(target), "spec": pkg["spec"]}
            if floating - {target}:
                result["with_dependents"] = sorted(floating - {target})
            return result
        reason = "new dependency conflicts: " + " / ".join(sorted(new))
        if set(new.values()) <= floating:
            break
        floating |= set(new.values())

    originals = [f"{name}=={installed[name]}" for name in sorted(floating) if name in installed]
    if originals:
        install(tools["install"], installed, floating, originals)
    return {"name": pkg["name"], "status": "failed", "reason": reason}


def apply_env(env: dict) -> list[dict]:
    results = []
    python = find_python(env["site_dir"])
    tools = installer(python, env["venv"]) if python else None
    if tools is None:
        reason = "no interpreter found" if python is None else "no uv or pip available"
        return [{"name": p["name"], "status": "failed", "reason": reason} for p in env["packages"]]

    for pkg in env["packages"]:
        installed = installed_versions(tools["list"])
        if installed is None:
            results.append({"name": pkg["name"], "status": "failed", "reason": "package list failed"})
            continue
        have = installed.get(normalize(pkg["name"]))
        if have and version_key(have) >= version_key(pkg["min_version"]):
            results.append({"name": pkg["name"], "status": "already", "version": have})
            continue
        results.append(upgrade(pkg, tools, installed))
    return results


def main(plan_path: str, result_path: str) -> None:
    with open(plan_path, encoding="utf-8") as fh:
        plan = json.load(fh)
    result = {"packages": [], "pip_removed": False, "skipped": plan.get("skipped", []),
              "unhandled_vendored": plan.get("unhandled_vendored", [])}
    for env in plan["envs"]:
        for item in apply_env(env):
            item["site_dir"] = env["site_dir"]
            result["packages"].append(item)

    # pip goes last: until here it may still be the fallback installer.
    if plan.get("remove_pip"):
        if shutil.which("uv"):
            result["pip_removed"] = run(["bash", os.path.join(HERE, "remove-pip.sh")]).returncode == 0
        else:
            result["pip_removed_skipped"] = "uv not available; pip kept as the package manager"

    for cache in ("/root/.cache/uv", "/root/.cache/pip"):
        shutil.rmtree(cache, ignore_errors=True)
    result["failed"] = sum(1 for p in result["packages"] if p["status"] == "failed")
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:3])
