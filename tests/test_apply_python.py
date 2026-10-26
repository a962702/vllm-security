import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "patch"))

from apply_python import (dependents, downgrades, is_protected, new_conflicts, normalize, parse_dependency_issues,
                          version_changes, version_key)


def test_normalize_follows_pep503():
    assert normalize("Jaraco.Context") == "jaraco-context"
    assert normalize("opentelemetry_api") == "opentelemetry-api"


def test_version_key_compares_numerically():
    assert version_key("80.10.2") > version_key("80.9.0")


def test_parse_uv_check_output():
    output = (
        "Using Python 3.12.3 environment at: /usr\n"
        "Found 2 incompatibilities\n"
        "The package `opentelemetry-sdk` requires `opentelemetry-api==1.40.0`, but `1.45.1` is installed\n"
        "The package `torch` requires `nvidia-nccl-cu13==2.29.7 ; sys_platform == 'linux'`, but `2.30.7` is installed\n"
    )
    assert parse_dependency_issues(output) == {
        "The package `opentelemetry-sdk` requires `opentelemetry-api==1.40.0`": "opentelemetry-sdk",
        "The package `torch` requires `nvidia-nccl-cu13==2.29.7 ; sys_platform == 'linux'`": "torch",
    }


def test_parse_pip_check_output():
    output = "opentelemetry-sdk 1.40.0 has requirement opentelemetry-api==1.40.0, but you have opentelemetry-api 1.45.1.\n"
    assert parse_dependency_issues(output) == {
        "opentelemetry-sdk 1.40.0 has requirement opentelemetry-api==1.40.0": "opentelemetry-sdk",
    }


def test_preexisting_conflict_matches_baseline_after_installed_version_moves():
    before = parse_dependency_issues(
        "The package `opentelemetry-exporter-otlp-common` requires `opentelemetry-sdk~=1.45.1`, but `1.40.0` is installed")
    after = parse_dependency_issues(
        "The package `opentelemetry-exporter-otlp-common` requires `opentelemetry-sdk~=1.45.1`, but `1.41.0` is installed")
    assert before.keys() == after.keys()


def pkg(version, requires=(), direct_url=False):
    return {"version": version, "requires": list(requires), "direct_url": direct_url}


def test_is_protected():
    assert is_protected("vllm", pkg("0.32.0"))
    assert is_protected("lmcache", pkg("0.5.3", direct_url=True))  # built from source
    assert is_protected("some-ext", pkg("1.0+rocm7"))
    assert not is_protected("certifi", pkg("2026.7.22"))


def test_dependents_walks_the_family_but_not_through_protected_packages():
    meta = {
        "opentelemetry-api": pkg("1.40.0"),
        "opentelemetry-sdk": pkg("1.40.0", ["opentelemetry-api"]),
        "opentelemetry-exporter-otlp-proto-grpc": pkg("1.40.0", ["opentelemetry-sdk"]),
        "vllm": pkg("0.32.0", ["opentelemetry-sdk"]),
        "vllm-plugin": pkg("1.0", ["vllm"]),
        "requests": pkg("2.32.0"),
    }
    assert dependents("opentelemetry-api", meta) == {
        "opentelemetry-sdk", "opentelemetry-exporter-otlp-proto-grpc"}


def test_new_conflicts_ignores_baseline_and_accepted_ones():
    baseline = {"The package `torch` requires `nvidia-nccl-cu13==2.29.7`": "torch"}
    current = {
        "The package `torch` requires `nvidia-nccl-cu13==2.29.7`": "torch",
        "The package `vllm` requires `setuptools>=77.0.3,<80`": "vllm",
        "The package `opentelemetry-sdk` requires `opentelemetry-api==1.40.0`": "opentelemetry-sdk",
    }
    assert new_conflicts(baseline, current, "setuptools", {"vllm"}) == [
        "The package `opentelemetry-sdk` requires `opentelemetry-api==1.40.0`"]
    assert len(new_conflicts(baseline, current, "setuptools", set())) == 2


def test_new_conflicts_accepts_pip_check_format():
    current = {"vllm 0.32.0 has requirement setuptools<80,>=77.0.3": "vllm"}
    assert new_conflicts({}, current, "setuptools", {"vllm"}) == []


def test_version_changes_reports_upgrades_additions_and_removals():
    before = {"a": pkg("1.0"), "b": pkg("2.0"), "c": pkg("3.0")}
    after = {"a": pkg("1.1"), "b": pkg("2.0"), "d": pkg("4.0")}
    assert version_changes(before, after) == {"a": ["1.0", "1.1"], "c": ["3.0", None], "d": [None, "4.0"]}


def test_downgrades_flags_lower_versions_and_removals_only():
    changes = {"lmcache": ["0.5.6", "0.4.3"], "otel": ["1.40.0", "1.45.1"], "gone": ["1.0", None],
               "cupy-cuda12x": [None, "14.2.0"]}
    assert downgrades(changes) == {"lmcache": ["0.5.6", "0.4.3"], "gone": ["1.0", None]}
