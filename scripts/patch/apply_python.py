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


def installer(python: str, venv: bool) -> tuple[list[str], list[str]] | None:
    """(list command, install command) for this interpreter: uv if present, else pip."""
    if shutil.which("uv"):
        extra = [] if venv else ["--break-system-packages"]
        return (["uv", "pip", "list", "--python", python, "--format", "json"],
                ["uv", "pip", "install", "--python", python, "--no-cache", *extra])
    if subprocess.run([python, "-m", "pip", "--version"], capture_output=True).returncode == 0:
        extra = [] if venv else ["--break-system-packages"]
        return ([python, "-m", "pip", "list", "--format", "json"],
                [python, "-m", "pip", "install", "--no-cache-dir", *extra])
    return None


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(proc.stdout[-4000:])
    sys.stdout.write(proc.stderr[-4000:])
    return proc


def apply_env(env: dict) -> list[dict]:
    results = []
    python = find_python(env["site_dir"])
    tools = installer(python, env["venv"]) if python else None
    if tools is None:
        reason = "no interpreter found" if python is None else "no uv or pip available"
        return [{"name": p["name"], "status": "failed", "reason": reason} for p in env["packages"]]
    list_cmd, install_cmd = tools

    for pkg in env["packages"]:
        listed = run(list_cmd)
        if listed.returncode != 0:
            results.append({"name": pkg["name"], "status": "failed", "reason": "package list failed"})
            continue
        installed = {normalize(p["name"]): p["version"] for p in json.loads(listed.stdout)}
        have = installed.get(normalize(pkg["name"]))
        if have and version_key(have) >= version_key(pkg["min_version"]):
            results.append({"name": pkg["name"], "status": "already", "version": have})
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as pins:
            for name, version in sorted(installed.items()):
                if name != normalize(pkg["name"]):
                    pins.write(f"{name}=={version}\n")
        proc = run([*install_cmd, "-c", pins.name, pkg["spec"]])
        os.unlink(pins.name)
        if proc.returncode == 0:
            results.append({"name": pkg["name"], "status": "upgraded", "from": have, "spec": pkg["spec"]})
        else:
            tail = (proc.stderr or proc.stdout).strip().splitlines()[-3:]
            results.append({"name": pkg["name"], "status": "failed", "reason": " / ".join(tail)})
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
