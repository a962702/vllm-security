import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from update_readme import render_summary_table, update_readme


def test_render_summary_table_formats_counts_and_dash_for_missing():
    entries = [
        {
            "version": "v0.28.0", "variant": "gpu",
            "before": {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4, "UNKNOWN": 5, "total": 15},
            "after": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 0},
            "status": "ok",
            "patched_image": "ghcr.io/owner/vllm-security/gpu:v0.28.0-patched",
        },
        {
            "version": "v0.28.0", "variant": "cpu",
            "before": None, "after": None,
            "status": "job_failed", "patched_image": None,
        },
    ]

    table = render_summary_table(entries)

    assert "v0.28.0" in table
    assert "1/2/3/4/5" in table
    assert "0/0/0/0/0" in table
    assert "ghcr.io/owner/vllm-security/gpu:v0.28.0-patched" in table
    assert table.count("| -") >= 2  # cpu row's missing before/after render as "-"


def test_update_readme_replaces_between_markers_and_preserves_rest():
    readme = (
        "# My Project\n\n"
        "Intro text.\n\n"
        "<!-- scan-summary:start -->\nold content\n<!-- scan-summary:end -->\n\n"
        "Footer text.\n"
    )

    updated = update_readme(readme, table_md="| a | b |", timestamp="2026-08-30T00:00:00Z", dashboard_url="https://example.github.io/repo/")

    assert "Intro text." in updated
    assert "Footer text." in updated
    assert "old content" not in updated
    assert "| a | b |" in updated
    assert "2026-08-30T00:00:00Z" in updated
    assert "https://example.github.io/repo/" in updated


def test_update_readme_raises_when_markers_missing():
    readme = "# My Project\n\nNo markers here.\n"
    try:
        update_readme(readme, table_md="x", timestamp="t", dashboard_url="u")
        assert False, "expected ValueError"
    except ValueError:
        pass
