import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts" / "patch"))

from apply_python import normalize, parse_dependency_issues, version_key


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
