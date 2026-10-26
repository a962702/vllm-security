"""Build a Python fix plan for a vLLM image from its Trivy report.

The plan is consumed inside the image by scripts/patch/apply_python.py. OS
packages are handled separately by scripts/patch/fix-os.sh (apt-get upgrade).

Fix strategy for Python findings:
  * a package with a fixed version -> install the smallest fixed version above
    the installed one, into the interpreter that owns the package's site dir;
  * a CVE in a package's vendored copy (e.g. setuptools/_vendor/wheel) -> fixed
    through the parent package, per VENDOR_POLICY;
  * packages listed in SKIP for the image repo are left alone.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Parent package -> how to fix CVEs found in its vendored copies.
# setuptools 80.10.2 is the first release vendoring jaraco.context>=6.1.0 and
# wheel>=0.46.2 that still ships pkg_resources (removed in 82), and it
# satisfies vllm's CUDA build constraint setuptools<81. Newer installs are kept.
# pip (<=26.2.2) still vendors vulnerable msgpack/urllib3/setuptools and the
# images manage packages with uv, so pip is removed (only when uv is present).
VENDOR_POLICY: dict[str, dict] = {
    "setuptools": {"name": "setuptools", "spec": "setuptools==80.10.2", "min_version": "80.10.2"},
    "pip": {"remove": True},
}

# Packages whose PyPI wheels don't match how the image built them; upgrading
# from PyPI would break the image, so they need a source rebuild instead.
SKIP: dict[str, dict[str, str]] = {
    "vllm/vllm-openai-rocm": {
        "lmcache": "built from source with hipcc for ROCm; the PyPI wheel is CUDA-only",
    },
}


# Upper bounds for direct upgrades: a fix that needs a version at or above the
# cap is skipped instead (and reported). setuptools 82 drops pkg_resources,
# which sentry_sdk, supervisor & co. still import, and vllm pins setuptools<81;
# the setuptools CVEs fixed only past that (sdist/legacy-wheel handling) don't
# apply at inference time.
CAPS: dict[str, dict[str, str]] = {
    "setuptools": {
        "below": "81",
        "reason": "fix needs setuptools>=81, which breaks vllm's pin and drops pkg_resources",
    },
}


def version_key(version: str) -> list:
    parts = re.split(r"[.\-+]", version)
    return [(0, int(p), "") if p.isdigit() else (1, 0, p) for p in parts]


def pick_fixed_version(installed: str, fixed: str) -> str:
    """Smallest listed fixed version above the installed one."""
    candidates = [f.strip() for f in fixed.split(",") if f.strip()]
    above = [c for c in candidates if version_key(c) > version_key(installed)] or candidates
    return min(above, key=version_key)


def site_dir(pkg_path: str) -> str | None:
    match = re.match(r"/?(.*/(?:site|dist)-packages)/", pkg_path or "")
    return "/" + match.group(1) if match else None


def vendored_parent(pkg_path: str) -> str | None:
    if not pkg_path:
        # Findings without a path come from an embedded SBOM
        # (pip/_vendor/*.cdx.json), i.e. pip's vendored copies.
        return "pip"
    if "/_vendor/" in pkg_path:
        return pkg_path.split("/_vendor/")[0].rsplit("/", 1)[-1]
    return None


def build_plan(report: dict, image_repo: str, image_env: dict[str, str]) -> dict:
    venv = image_env.get("VIRTUAL_ENV")
    skip = SKIP.get(image_repo, {})
    packages: dict[str, dict[str, str]] = {}  # site dir -> name -> min version
    vendored: dict[str, set[str | None]] = {}  # parent -> site dirs holding it
    skipped: dict[str, str] = {}

    for result in report.get("Results") or []:
        if result.get("Type") != "python-pkg":
            continue
        for vuln in result.get("Vulnerabilities") or []:
            if not vuln.get("FixedVersion"):
                continue
            path = vuln.get("PkgPath") or ""
            name = vuln["PkgName"]
            parent = vendored_parent(path)
            if parent:
                vendored.setdefault(parent, set()).add(site_dir(path))
                continue
            if name in skip:
                skipped[name] = skip[name]
                continue
            sd = site_dir(path)
            if not sd:
                continue
            want = pick_fixed_version(vuln["InstalledVersion"], vuln["FixedVersion"])
            cap = CAPS.get(name)
            if cap and version_key(want) >= version_key(cap["below"]):
                skipped[name] = cap["reason"]
                continue
            current = packages.setdefault(sd, {}).get(name)
            if current is None or version_key(want) > version_key(current):
                packages[sd][name] = want

    envs = [
        {
            "site_dir": sd,
            "venv": bool(venv and sd.startswith(venv)),
            "packages": [
                {"name": name, "spec": f"{name}>={version}", "min_version": version}
                for name, version in sorted(pkgs.items())
            ],
        }
        for sd, pkgs in sorted(packages.items())
    ]

    remove_pip = False
    unhandled: list[str] = []
    for parent, dirs in sorted(vendored.items()):
        policy = VENDOR_POLICY.get(parent)
        if policy is None:
            unhandled.append(parent)
        elif policy.get("remove"):
            remove_pip = True
        else:
            pkg = {k: policy[k] for k in ("name", "spec", "min_version")}
            for sd in sorted(d for d in dirs if d):
                env = next((e for e in envs if e["site_dir"] == sd), None)
                if env is None:
                    env = {"site_dir": sd, "venv": bool(venv and sd.startswith(venv)), "packages": []}
                    envs.append(env)
                if all(p["name"] != pkg["name"] for p in env["packages"]):
                    env["packages"].append(pkg)

    return {
        "image_repo": image_repo,
        "virtual_env": venv,
        "envs": envs,
        "remove_pip": remove_pip,
        "skipped": [{"name": n, "reason": r} for n, r in sorted(skipped.items())],
        "unhandled_vendored": unhandled,
    }


def image_env(image: str) -> dict[str, str]:
    out = subprocess.run(
        ["docker", "image", "inspect", "--format", "{{json .Config.Env}}", image],
        capture_output=True, text=True, check=True).stdout
    return dict(e.split("=", 1) for e in json.loads(out) or [])


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Python fix plan from a Trivy report")
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--image", required=True, help="local image the report was taken from")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    report = json.loads(args.report.read_text())
    plan = build_plan(report, args.image.rsplit(":", 1)[0], image_env(args.image))
    args.out.write_text(json.dumps(plan, indent=2))
    print(json.dumps(plan, indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
