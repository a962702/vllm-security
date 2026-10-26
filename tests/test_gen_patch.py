import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from gen_patch import build_plan, pick_fixed_version, site_dir, vendored_parent, version_key

VENV_SITE = "/opt/venv/lib/python3.12/site-packages"
SYS_SITE = "/usr/local/lib/python3.12/dist-packages"


def python_result(*vulns):
    return {"Results": [{"Type": "python-pkg", "Vulnerabilities": list(vulns)}]}


def vuln(name, installed, fixed, path):
    return {"PkgName": name, "InstalledVersion": installed, "FixedVersion": fixed, "PkgPath": path}


def test_version_key_orders_numerically_not_lexically():
    assert version_key("2026.10.19") > version_key("2026.7.22")
    assert version_key("0.13.10") > version_key("0.13.4")


def test_pick_fixed_version_takes_smallest_fix_above_installed():
    assert pick_fixed_version("2.7.0", "2.6.3, 2.8.0, 2.9.1") == "2.8.0"


def test_pick_fixed_version_falls_back_when_no_fix_above_installed():
    assert pick_fixed_version("3.0", "2.1, 2.5") == "2.1"


def test_site_dir_accepts_relative_trivy_paths():
    assert site_dir("usr/local/lib/python3.12/dist-packages/certifi-2026.7.22.dist-info/METADATA") == SYS_SITE
    assert site_dir("") is None


def test_vendored_parent():
    assert vendored_parent(f"{VENV_SITE}/setuptools/_vendor/wheel-0.45.1.dist-info/METADATA") == "setuptools"
    assert vendored_parent("") == "pip"  # embedded SBOM findings carry no path
    assert vendored_parent(f"{VENV_SITE}/certifi-1.dist-info/METADATA") is None


def test_build_plan_keeps_highest_fix_per_package_and_routes_to_its_env():
    report = python_result(
        vuln("certifi", "2026.7.22", "2026.10.19", f"{VENV_SITE}/certifi-2026.7.22.dist-info/METADATA"),
        vuln("pillow", "12.3.0", "12.4.0", f"{SYS_SITE}/pillow-12.3.0.dist-info/METADATA"),
        vuln("pillow", "12.3.0", "13.0.0", f"{SYS_SITE}/pillow-12.3.0.dist-info/METADATA"),
    )
    plan = build_plan(report, "vllm/vllm-openai-cpu", {"VIRTUAL_ENV": "/opt/venv"})

    envs = {e["site_dir"]: e for e in plan["envs"]}
    assert envs[VENV_SITE]["venv"] is True
    assert envs[VENV_SITE]["packages"] == [
        {"name": "certifi", "spec": "certifi>=2026.10.19", "min_version": "2026.10.19"}]
    assert envs[SYS_SITE]["venv"] is False
    assert envs[SYS_SITE]["packages"][0]["spec"] == "pillow>=13.0.0"


def test_build_plan_ignores_findings_without_fix_and_os_packages():
    report = {"Results": [
        {"Type": "ubuntu", "Vulnerabilities": [vuln("openssl", "3.0.2", "3.0.2-1", "")]},
        {"Type": "python-pkg", "Vulnerabilities": [
            vuln("flash_attn", "2.8.3", "", f"{SYS_SITE}/flash_attn-2.8.3.dist-info/METADATA")]},
    ]}
    plan = build_plan(report, "vllm/vllm-openai", {})
    assert plan["envs"] == []
    assert plan["remove_pip"] is False


def test_build_plan_fixes_vendored_copies_through_their_parent():
    report = python_result(
        vuln("wheel", "0.45.1", "0.46.2", f"{VENV_SITE}/setuptools/_vendor/wheel-0.45.1.dist-info/METADATA"),
        vuln("jaraco.context", "5.3.0", "6.1.0",
             f"{VENV_SITE}/setuptools/_vendor/jaraco.context-5.3.0.dist-info/METADATA"),
        vuln("urllib3", "2.7.0", "2.8.0", ""),
        vuln("msgpack", "1.1.2", "1.2.1", f"{VENV_SITE}/pip/_vendor/msgpack/METADATA"),
    )
    plan = build_plan(report, "vllm/vllm-openai-cpu", {"VIRTUAL_ENV": "/opt/venv"})

    assert plan["remove_pip"] is True
    assert plan["envs"] == [{"site_dir": VENV_SITE, "venv": True, "packages": [
        {"name": "setuptools", "spec": "setuptools==80.10.2", "min_version": "80.10.2"}]}]


def test_build_plan_reports_vendored_parents_without_policy():
    report = python_result(vuln("six", "1.0", "1.1", f"{SYS_SITE}/somepkg/_vendor/six-1.0.dist-info/METADATA"))
    assert build_plan(report, "vllm/vllm-openai", {})["unhandled_vendored"] == ["somepkg"]


def test_build_plan_skips_source_built_packages_for_their_repo_only():
    report = python_result(vuln("lmcache", "0.5.3", "0.5.6", f"{SYS_SITE}/lmcache-0.5.3.dist-info/METADATA"))

    rocm = build_plan(report, "vllm/vllm-openai-rocm", {})
    assert rocm["envs"] == []
    assert rocm["skipped"][0]["name"] == "lmcache"

    gpu = build_plan(report, "vllm/vllm-openai", {})
    assert gpu["envs"][0]["packages"][0]["spec"] == "lmcache>=0.5.6"
    assert gpu["skipped"] == []


def test_build_plan_caps_setuptools_and_keeps_vendored_fix():
    report = python_result(
        vuln("setuptools", "78.1.1", "83.0.0", f"{VENV_SITE}/setuptools-78.1.1.dist-info/METADATA"),
        vuln("wheel", "0.45.1", "0.46.2", f"{VENV_SITE}/setuptools/_vendor/wheel-0.45.1.dist-info/METADATA"),
    )
    plan = build_plan(report, "vllm/vllm-openai-cpu", {"VIRTUAL_ENV": "/opt/venv"})

    assert [s["name"] for s in plan["skipped"]] == ["setuptools"]
    assert plan["envs"][0]["packages"] == [
        {"name": "setuptools", "spec": "setuptools==80.10.2", "min_version": "80.10.2"}]


def test_build_plan_allows_setuptools_fix_below_cap():
    report = python_result(
        vuln("setuptools", "70.3.0", "78.1.1", f"{SYS_SITE}/setuptools-70.3.0.dist-info/METADATA"))
    plan = build_plan(report, "vllm/vllm-openai", {})
    assert plan["envs"][0]["packages"][0]["spec"] == "setuptools>=78.1.1"
