"""Discover vLLM release versions and which image variants exist for each."""
from __future__ import annotations

import time


def filter_releases(releases: list[dict], max_versions: int) -> list[str]:
    stable = [r for r in releases if not r.get("prerelease", False)]
    stable_sorted = sorted(stable, key=lambda r: r["published_at"], reverse=True)
    return [r["tag_name"] for r in stable_sorted[:max_versions]]


VARIANT_REPOS: dict[str, str] = {
    "gpu": "vllm/vllm-openai",
    "cpu": "vllm/vllm-openai-cpu",
    "rocm": "vllm/vllm-openai-rocm",
}

NIGHTLY_VERSION = "nightly"


def variant_tag_exists(repo: str, tag: str, get_status_fn, attempts: int = 3) -> bool:
    """Return whether `repo:tag` is published on Docker Hub.

    Only a 404 counts as "this variant isn't published for this version" (the
    expected, silently-dropped case). Any other status -- notably 429 rate
    limits and 5xx errors -- is transient and retried with exponential backoff,
    then raised, so a rate limit can never masquerade as a missing tag and
    silently shrink the scan matrix.
    """
    last_exc: Exception | None = None
    for attempt in range(attempts):
        try:
            status = get_status_fn(f"https://hub.docker.com/v2/repositories/{repo}/tags/{tag}/")
            if status == 200:
                return True
            if status == 404:
                return False
            last_exc = RuntimeError(f"unexpected status {status} checking tag {repo}:{tag}")
        except Exception as exc:  # noqa: BLE001 - deliberately broad, retried below
            last_exc = exc
        if attempt < attempts - 1:
            time.sleep(2 ** attempt)
    raise RuntimeError(f"failed checking tag {repo}:{tag} after {attempts} attempts") from last_exc


def build_matrix(versions: list[str], tag_exists_map: dict[str, dict[str, bool]]) -> list[dict]:
    matrix = []
    for version in versions:
        variants_for_version = tag_exists_map.get(version, {})
        for variant, repo in VARIANT_REPOS.items():
            if variants_for_version.get(variant):
                matrix.append(
                    {"version": version, "variant": variant, "image": f"{repo}:{version}", "image_repo": repo}
                )
    return matrix


import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path


def fetch_releases(token: str) -> list[dict]:
    request = urllib.request.Request(
        "https://api.github.com/repos/vllm-project/vllm/releases?per_page=30",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def http_get_status(url: str) -> int:
    try:
        with urllib.request.urlopen(url) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code


def run(
    max_versions: int,
    out_dir: Path,
    fetch_releases_fn=fetch_releases,
    http_get_status_fn=http_get_status,
    token: str = "",
    include_nightly: bool = True,
) -> list[dict]:
    releases = fetch_releases_fn(token)
    versions = filter_releases(releases, max_versions)
    if include_nightly:
        versions = [NIGHTLY_VERSION] + versions

    tag_exists_map = {
        version: {
            variant: variant_tag_exists(repo, version, http_get_status_fn)
            for variant, repo in VARIANT_REPOS.items()
        }
        for version in versions
    }
    matrix = build_matrix(versions, tag_exists_map)

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "matrix.json").write_text(json.dumps(matrix, indent=2))
    (out_dir / "expected.json").write_text(json.dumps(matrix, indent=2))

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"matrix={json.dumps({'include': matrix})}\n")

    return matrix


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover vLLM versions and image variants")
    parser.add_argument("--max-versions", type=int, default=10)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN", ""))
    parser.add_argument("--include-nightly", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()

    matrix = run(
        max_versions=args.max_versions,
        out_dir=args.out_dir,
        token=args.token,
        include_nightly=args.include_nightly,
    )
    print(f"discovered {len(matrix)} (version, variant) combos")


if __name__ == "__main__":
    main()
