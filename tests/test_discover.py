import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from discover import filter_releases


def test_filter_releases_excludes_prerelease_and_sorts_newest_first():
    releases = [
        {"tag_name": "v0.27.0", "prerelease": False, "published_at": "2026-08-10T21:18:11Z"},
        {"tag_name": "v0.28.0-rc1", "prerelease": True, "published_at": "2026-08-20T00:00:00Z"},
        {"tag_name": "v0.28.0", "prerelease": False, "published_at": "2026-08-26T09:46:30Z"},
        {"tag_name": "v0.26.0", "prerelease": False, "published_at": "2026-07-27T01:06:58Z"},
    ]

    result = filter_releases(releases, max_versions=10)

    assert result == ["v0.28.0", "v0.27.0", "v0.26.0"]


def test_filter_releases_truncates_to_max_versions():
    releases = [
        {"tag_name": f"v0.{i}.0", "prerelease": False, "published_at": f"2026-01-{i:02d}T00:00:00Z"}
        for i in range(1, 21)
    ]

    result = filter_releases(releases, max_versions=10)

    assert len(result) == 10
    assert result[0] == "v0.20.0"
    assert result[-1] == "v0.11.0"


def test_filter_releases_empty_input_returns_empty():
    assert filter_releases([], max_versions=10) == []


import pytest

import discover
from discover import VARIANT_REPOS, build_matrix, variant_tag_exists


@pytest.fixture
def sleep_calls(monkeypatch):
    """Replace discover's backoff sleep with a no-op recorder.

    Keeps the retry tests instant while still letting them assert that the
    exponential backoff actually fired (and with the right delays).
    """
    recorded: list[float] = []
    monkeypatch.setattr(discover.time, "sleep", recorded.append)
    return recorded


def test_variant_repos_mapping():
    assert VARIANT_REPOS == {
        "gpu": "vllm/vllm-openai",
        "cpu": "vllm/vllm-openai-cpu",
        "rocm": "vllm/vllm-openai-rocm",
    }


def test_build_matrix_includes_only_existing_variants():
    versions = ["v0.28.0", "v0.20.2"]
    tag_exists_map = {
        "v0.28.0": {"gpu": True, "cpu": False, "rocm": False},
        "v0.20.2": {"gpu": True, "cpu": True, "rocm": True},
    }

    result = build_matrix(versions, tag_exists_map)

    assert {
        "version": "v0.28.0", "variant": "gpu",
        "image": "vllm/vllm-openai:v0.28.0", "image_repo": "vllm/vllm-openai",
    } in result
    assert not any(e["version"] == "v0.28.0" and e["variant"] == "cpu" for e in result)
    assert len(result) == 4


def test_build_matrix_drops_version_missing_from_map():
    result = build_matrix(["v0.99.0"], tag_exists_map={})
    assert result == []


def test_variant_tag_exists_true_on_200():
    result = variant_tag_exists("vllm/vllm-openai", "v0.28.0", get_status_fn=lambda url: 200)
    assert result is True


def test_variant_tag_exists_false_on_404():
    result = variant_tag_exists("vllm/vllm-openai-cpu", "v0.28.0", get_status_fn=lambda url: 404)
    assert result is False


def test_variant_tag_exists_retries_then_succeeds(sleep_calls):
    calls = {"n": 0}

    def flaky(url):
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("boom")
        return 200

    result = variant_tag_exists("vllm/vllm-openai", "v0.28.0", get_status_fn=flaky, attempts=3)

    assert result is True
    assert calls["n"] == 3


def test_variant_tag_exists_raises_after_exhausting_attempts(sleep_calls):
    def always_fails(url):
        raise ConnectionError("boom")

    try:
        variant_tag_exists("vllm/vllm-openai", "v0.28.0", get_status_fn=always_fails, attempts=3)
        assert False, "expected RuntimeError"
    except RuntimeError:
        pass


def test_variant_tag_exists_404_returns_false_without_retrying(sleep_calls):
    """A genuine 'not published' answer is final -- no retry, no backoff."""
    calls = {"n": 0}

    def not_found(url):
        calls["n"] += 1
        return 404

    result = variant_tag_exists("vllm/vllm-openai-rocm", "v0.28.0", get_status_fn=not_found, attempts=3)

    assert result is False
    assert calls["n"] == 1
    assert sleep_calls == []


def test_variant_tag_exists_rate_limited_raises_instead_of_dropping_variant(sleep_calls):
    """429 must never be mistaken for 404 -- it retries, then fails loudly."""
    calls = {"n": 0}

    def rate_limited(url):
        calls["n"] += 1
        return 429

    with pytest.raises(RuntimeError) as excinfo:
        variant_tag_exists("vllm/vllm-openai", "v0.28.0", get_status_fn=rate_limited, attempts=3)

    assert "after 3 attempts" in str(excinfo.value)
    assert "429" in str(excinfo.value.__cause__)
    assert calls["n"] == 3
    # Exponential backoff between attempts, and none after the final one.
    assert sleep_calls == [1, 2]


def test_variant_tag_exists_server_error_then_200_succeeds(sleep_calls):
    """A transient 5xx is retried, and a later 200 still yields True."""
    statuses = [500, 200]
    calls = {"n": 0}

    def flaky_status(url):
        calls["n"] += 1
        return statuses.pop(0)

    result = variant_tag_exists("vllm/vllm-openai", "v0.28.0", get_status_fn=flaky_status, attempts=3)

    assert result is True
    assert calls["n"] == 2
    assert sleep_calls == [1]


def test_variant_tag_exists_rate_limited_then_404_returns_false(sleep_calls):
    """After a transient 429, an authoritative 404 is honoured as 'not published'."""
    statuses = [429, 404]

    def flaky_status(url):
        return statuses.pop(0)

    result = variant_tag_exists("vllm/vllm-openai-cpu", "v0.28.0", get_status_fn=flaky_status, attempts=3)

    assert result is False
    assert sleep_calls == [1]


import json
import os

from discover import run


def test_run_writes_matrix_and_expected_and_github_output(tmp_path, monkeypatch):
    releases = [
        {"tag_name": "v0.28.0", "prerelease": False, "published_at": "2026-08-26T09:46:30Z"},
        {"tag_name": "v0.20.2", "prerelease": False, "published_at": "2026-05-09T10:28:13Z"},
    ]

    def fake_fetch_releases(token):
        return releases

    def fake_http_get_status(url):
        if "v0.28.0" in url and "vllm-openai-cpu" not in url and "vllm-openai-rocm" not in url:
            return 200
        if "v0.20.2" in url:
            return 200
        return 404

    out_dir = tmp_path / "out"
    github_output_path = tmp_path / "github_output.txt"
    monkeypatch.setenv("GITHUB_OUTPUT", str(github_output_path))

    matrix = run(
        max_versions=10,
        out_dir=out_dir,
        fetch_releases_fn=fake_fetch_releases,
        http_get_status_fn=fake_http_get_status,
    )

    assert {
        "version": "v0.28.0", "variant": "gpu",
        "image": "vllm/vllm-openai:v0.28.0", "image_repo": "vllm/vllm-openai",
    } in matrix
    assert any(e["version"] == "v0.20.2" and e["variant"] == "cpu" for e in matrix)

    written_matrix = json.loads((out_dir / "matrix.json").read_text())
    written_expected = json.loads((out_dir / "expected.json").read_text())
    assert written_matrix == matrix
    assert written_expected == matrix

    output_line = github_output_path.read_text().strip()
    assert output_line.startswith("matrix=")
    payload = json.loads(output_line[len("matrix="):])
    assert payload == {"include": matrix}


def test_run_without_github_output_env_does_not_raise(tmp_path, monkeypatch):
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)

    run(
        max_versions=1,
        out_dir=tmp_path / "out2",
        fetch_releases_fn=lambda token: [
            {"tag_name": "v0.28.0", "prerelease": False, "published_at": "2026-08-26T09:46:30Z"}
        ],
        http_get_status_fn=lambda url: 200,
    )


def test_run_includes_nightly_by_default(tmp_path):
    releases = [
        {"tag_name": "v0.28.0", "prerelease": False, "published_at": "2026-08-26T09:46:30Z"},
    ]

    def fake_http_get_status(url):
        if "nightly" in url and "vllm-openai-cpu" not in url and "vllm-openai-rocm" not in url:
            return 200
        if "v0.28.0" in url and "vllm-openai-cpu" not in url and "vllm-openai-rocm" not in url:
            return 200
        return 404

    matrix = run(
        max_versions=10,
        out_dir=tmp_path / "out",
        fetch_releases_fn=lambda token: releases,
        http_get_status_fn=fake_http_get_status,
    )

    assert {
        "version": "nightly", "variant": "gpu",
        "image": "vllm/vllm-openai:nightly", "image_repo": "vllm/vllm-openai",
    } in matrix
    assert not any(e["version"] == "nightly" and e["variant"] == "cpu" for e in matrix)


def test_run_excludes_nightly_when_disabled(tmp_path):
    releases = [
        {"tag_name": "v0.28.0", "prerelease": False, "published_at": "2026-08-26T09:46:30Z"},
    ]

    matrix = run(
        max_versions=10,
        out_dir=tmp_path / "out",
        fetch_releases_fn=lambda token: releases,
        http_get_status_fn=lambda url: 200,
        include_nightly=False,
    )

    assert not any(e["version"] == "nightly" for e in matrix)
