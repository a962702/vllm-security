"""Apply a gen_patch.py plan inside the image being patched (stdlib only).

Usage: python3 -I apply_python.py <plan.json> <result.json>

Each package is upgraded on its own:
  * protected packages (vllm, torch & co., anything not installed from an
    index) are pinned to their installed versions and never rebuilt;
  * the packages that depend on the target are requested along with it (at
    their installed version or newer), so the resolver can move a family pinned
    together (opentelemetry-api/-sdk/-proto) instead of leaving their
    requirements broken; anything not needed stays put;
  * nothing is built from source (--no-build / --only-binary);
  * if the result downgrades or removes anything, or has dependency conflicts
    that weren't there before, every changed package is put back.
Outcomes are recorded in the result file instead of failing the build; only a
rollback that doesn't restore the environment exits non-zero.
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

# Core of the image: changing these needs a rebuild, not a patch.
PROTECTED = {
    "vllm", "torch", "torchvision", "torchaudio", "triton", "pytorch-triton-rocm",
    "numpy", "transformers", "xformers", "flashinfer-python", "flash-attn",
}


class RollbackFailed(Exception):
    pass


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
    """install / uninstall / check commands for this interpreter: uv if present, else pip."""
    extra = [] if venv else ["--break-system-packages"]
    if shutil.which("uv"):
        return {"install": ["uv", "pip", "install", "--python", python, "--no-cache", "--no-build", *extra],
                "uninstall": ["uv", "pip", "uninstall", "--python", python, *extra],
                "check": ["uv", "pip", "check", "--python", python]}
    if subprocess.run([python, "-m", "pip", "--version"], capture_output=True).returncode == 0:
        return {"install": [python, "-m", "pip", "install", "--no-cache-dir", "--only-binary", ":all:", *extra],
                "uninstall": [python, "-m", "pip", "uninstall", "-y", *extra],
                "check": [python, "-m", "pip", "check"]}
    return None


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(proc.stdout[-4000:])
    sys.stdout.write(proc.stderr[-4000:])
    return proc


# Runs in the target interpreter: name -> version, runtime requirements, and
# whether it was installed from somewhere other than an index (PEP 610).
INSPECT = r"""
import json, re, importlib.metadata as md
out = {}
for d in md.distributions():
    name = d.metadata["Name"]
    if not name or name in out:
        continue
    reqs = []
    for r in d.requires or []:
        if re.search(r"extra\s*==", r):
            continue
        m = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9._-]*)", r)
        if m:
            reqs.append(m.group(1))
    out[name] = {"version": d.version, "requires": reqs,
                 "direct_url": d.read_text("direct_url.json") is not None}
print(json.dumps(out))
"""


def inspect_env(python: str) -> dict[str, dict]:
    proc = subprocess.run([python, "-I", "-c", INSPECT], capture_output=True, text=True, check=True)
    return {normalize(name): {**info, "requires": [normalize(r) for r in info["requires"]]}
            for name, info in json.loads(proc.stdout).items()}


def is_protected(name: str, info: dict) -> bool:
    return name in PROTECTED or "+" in info["version"] or info["direct_url"]


def dependents(target: str, meta: dict[str, dict]) -> set[str]:
    """Unprotected packages that depend on target, directly or transitively."""
    found: set[str] = set()
    queue = [target]
    while queue:
        current = queue.pop()
        for name, info in meta.items():
            if current in info["requires"] and name not in found and name != target \
                    and not is_protected(name, info):
                found.add(name)
                queue.append(name)
    return found


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


def new_conflicts(baseline: dict[str, str], current: dict[str, str], target: str,
                  allowed: set[str]) -> list[str]:
    """Conflicts not present before, minus accepted ones (allowed requirer on target)."""
    def accepted(line: str, requirer: str) -> bool:
        return requirer in allowed and re.search(rf"[`\s]{re.escape(target)}\b", line.lower()) is not None
    return sorted(line for line, requirer in current.items()
                  if line not in baseline and not accepted(line, requirer))


def version_changes(before: dict[str, dict], after: dict[str, dict]) -> dict[str, list]:
    names = set(before) | set(after)
    return {n: [before.get(n, {}).get("version"), after.get(n, {}).get("version")]
            for n in sorted(names)
            if before.get(n, {}).get("version") != after.get(n, {}).get("version")}


def downgrades(changes: dict[str, list]) -> dict[str, list]:
    return {n: v for n, v in changes.items()
            if v[0] and (v[1] is None or version_key(v[1]) < version_key(v[0]))}


def with_pins(cmd: list[str], meta: dict[str, dict], requirements: list[str]) -> subprocess.CompletedProcess:
    """Run an install with every protected package pinned to its installed version."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as pins:
        for name, info in sorted(meta.items()):
            if is_protected(name, info):
                pins.write(f"{name}=={info['version']}\n")
    try:
        return run([*cmd, "-c", pins.name, *requirements])
    finally:
        os.unlink(pins.name)


def rollback(tools: dict[str, list[str]], python: str, before: dict[str, dict],
             changes: dict[str, list]) -> None:
    restore = [f"{n}=={old}" for n, (old, _) in changes.items() if old]
    added = [n for n, (old, _) in changes.items() if not old]
    if restore:
        with_pins(tools["install"], before, restore)
    if added:
        run([*tools["uninstall"], *added])
    left = version_changes(before, inspect_env(python))
    if left:
        raise RollbackFailed(f"could not restore {left}")


# The fix exists but can't coexist with what the image already has (uv / pip).
UNRESOLVABLE = re.compile(r"No solution found|ResolutionImpossible|Could not find a version that satisfies")


def upgrade(pkg: dict, tools: dict[str, list[str]], python: str) -> dict:
    """Upgrade one package; status is upgraded, already, skipped (protected),
    blocked (no version set fits without breaking the image; rolled back) or
    failed (anything else)."""
    target = normalize(pkg["name"])
    before = inspect_env(python)
    if target in before and is_protected(target, before[target]):
        return {"name": pkg["name"], "status": "skipped", "reason": "protected package; needs a rebuild"}
    have = before.get(target, {}).get("version")
    if have and version_key(have) >= version_key(pkg["min_version"]):
        return {"name": pkg["name"], "status": "already", "version": have}

    baseline = dependency_issues(tools["check"])
    # Dependents may move forward with the target, never back.
    requests = [pkg["spec"], *(f"{n}>={before[n]['version']}" for n in sorted(dependents(target, before)))]
    proc = with_pins(tools["install"], before, requests)
    changes = version_changes(before, inspect_env(python))
    down = downgrades(changes)
    status = "blocked"
    if proc.returncode != 0:
        output = proc.stderr + proc.stdout
        reason = " / ".join((proc.stderr or proc.stdout).strip().splitlines()[-3:])
        if not UNRESOLVABLE.search(output):
            status = "failed"
    elif down:
        reason = "would downgrade " + ", ".join(f"{n} {old}->{new}" for n, (old, new) in down.items())
    else:
        conflicts = new_conflicts(baseline, dependency_issues(tools["check"]), target,
                                  {normalize(n) for n in pkg.get("allow_conflicts_with", [])})
        if not conflicts:
            return {"name": pkg["name"], "status": "upgraded", "from": have, "spec": pkg["spec"],
                    "changes": changes}
        reason = "new dependency conflicts: " + " / ".join(conflicts)
    if changes:
        rollback(tools, python, before, changes)
    return {"name": pkg["name"], "status": status, "reason": reason}


def apply_env(env: dict) -> list[dict]:
    python = find_python(env["site_dir"])
    tools = installer(python, env["venv"]) if python else None
    if tools is None:
        reason = "no interpreter found" if python is None else "no uv or pip available"
        return [{"name": p["name"], "status": "failed", "reason": reason} for p in env["packages"]]
    results = [upgrade(pkg, tools, python) for pkg in env["packages"]]

    # A fix that failed on its own may have landed later as another target's
    # dependent (datasets moved by the fsspec upgrade); report what's installed.
    final = inspect_env(python)
    for pkg, result in zip(env["packages"], results):
        now = final.get(normalize(pkg["name"]), {}).get("version")
        if result["status"] in ("blocked", "failed") and now \
                and version_key(now) >= version_key(pkg["min_version"]):
            result["reason"] = f"{result['status']} on its own ({result['reason']}); " \
                               f"reached {now} with a later upgrade"
            result["status"] = "upgraded"
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
            proc = run(["bash", os.path.join(HERE, "remove-pip.sh")])
            kept = [line[len("KEPT: "):] for line in proc.stdout.splitlines() if line.startswith("KEPT: ")]
            result["pip_removed"] = proc.returncode == 0 and not kept
            if kept:
                result["pip_kept"] = kept
        else:
            result["pip_removed_skipped"] = "uv not available; pip kept as the package manager"

    for cache in ("/root/.cache/uv", "/root/.cache/pip"):
        shutil.rmtree(cache, ignore_errors=True)
    result["failed"] = sum(1 for p in result["packages"] if p["status"] == "failed")
    result["blocked"] = sum(1 for p in result["packages"] if p["status"] == "blocked")
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    with open(result_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:3])
