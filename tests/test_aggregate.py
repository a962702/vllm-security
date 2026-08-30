import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from aggregate import severity_counts


def test_severity_counts_empty_report():
    assert severity_counts({}) == {
        "CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 0,
    }


def test_severity_counts_results_without_vulnerabilities_key():
    report = {"Results": [{"Target": "os-pkgs", "Class": "os-pkgs"}]}
    assert severity_counts(report)["total"] == 0


def test_severity_counts_mixed_severities_across_results():
    report = {
        "Results": [
            {
                "Class": "os-pkgs",
                "Vulnerabilities": [
                    {"VulnerabilityID": "CVE-1", "Severity": "CRITICAL"},
                    {"VulnerabilityID": "CVE-2", "Severity": "HIGH"},
                ],
            },
            {
                "Class": "lang-pkgs",
                "Vulnerabilities": [
                    {"VulnerabilityID": "CVE-3", "Severity": "HIGH"},
                    {"VulnerabilityID": "CVE-4", "Severity": "LOW"},
                ],
            },
        ]
    }

    result = severity_counts(report)

    assert result == {
        "CRITICAL": 1, "HIGH": 2, "MEDIUM": 0, "LOW": 1, "UNKNOWN": 0, "total": 4,
    }


def test_severity_counts_unknown_severity_string_bucketed_as_unknown():
    report = {"Results": [{"Vulnerabilities": [{"VulnerabilityID": "CVE-5", "Severity": "WEIRD"}]}]}
    result = severity_counts(report)
    assert result["UNKNOWN"] == 1
    assert result["total"] == 1


from aggregate import build_history_lines, merge_with_expected


def test_merge_with_expected_fills_missing_as_job_failed():
    expected = [
        {"version": "v0.28.0", "variant": "gpu", "image": "vllm/vllm-openai:v0.28.0"},
        {"version": "v0.28.0", "variant": "cpu", "image": "vllm/vllm-openai-cpu:v0.28.0"},
    ]
    found = {
        ("v0.28.0", "gpu"): {
            "version": "v0.28.0", "variant": "gpu", "image": "vllm/vllm-openai:v0.28.0",
            "scanned_at": "2026-08-30T00:00:00Z",
            "before": {"CRITICAL": 1, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 1},
            "after": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 0},
            "system_upgrade_ok": True, "python_upgrade_ok": True,
            "patched_image": "ghcr.io/owner/vllm-security/gpu:v0.28.0-patched",
            "status": "ok",
        }
    }

    merged = merge_with_expected(expected, found)

    assert len(merged) == 2
    assert merged[0]["status"] == "ok"
    assert merged[1] == {
        "version": "v0.28.0", "variant": "cpu", "image": "vllm/vllm-openai-cpu:v0.28.0",
        "scanned_at": None, "before": None, "after": None,
        "system_upgrade_ok": None, "python_upgrade_ok": None,
        "patched_image": None, "status": "job_failed",
    }


def test_merge_with_expected_ignores_unexpected_found_entries():
    expected = [{"version": "v0.28.0", "variant": "gpu", "image": "vllm/vllm-openai:v0.28.0"}]
    found = {
        ("v0.28.0", "gpu"): {"version": "v0.28.0", "variant": "gpu", "status": "ok"},
        ("v0.99.0", "gpu"): {"version": "v0.99.0", "variant": "gpu", "status": "ok"},
    }

    merged = merge_with_expected(expected, found)

    assert len(merged) == 1
    assert merged[0]["version"] == "v0.28.0"


def test_build_history_lines_roundtrips_expected_fields():
    entries = [
        {
            "version": "v0.28.0", "variant": "gpu",
            "before": {"CRITICAL": 1, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 1},
            "after": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 0},
            "patched_image": "ghcr.io/owner/vllm-security/vllm-openai:v0.28.0-20260830",
            "status": "ok",
        },
    ]

    lines = build_history_lines(entries, date="2026-08-30")

    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["date"] == "2026-08-30"
    assert row["version"] == "v0.28.0"
    assert row["variant"] == "gpu"
    assert row["before"]["total"] == 1
    assert row["after"]["total"] == 0
    assert row["patched_image"] == "ghcr.io/owner/vllm-security/vllm-openai:v0.28.0-20260830"
    assert row["status"] == "ok"


from aggregate import is_within_retention


def test_is_within_retention_same_day_is_kept():
    assert is_within_retention("2026-08-30", current_date="2026-08-30", retention_days=7) is True


def test_is_within_retention_six_days_back_is_kept():
    assert is_within_retention("2026-08-24", current_date="2026-08-30", retention_days=7) is True


def test_is_within_retention_seven_days_back_is_pruned():
    assert is_within_retention("2026-08-23", current_date="2026-08-30", retention_days=7) is False


def test_is_within_retention_future_date_is_kept():
    """Clock skew / a stray manual dispatch shouldn't crash or wrongly prune."""
    assert is_within_retention("2026-09-01", current_date="2026-08-30", retention_days=7) is True


from aggregate import prune_old_reports, write_reports_index


def test_prune_old_reports_removes_dirs_outside_retention_window(tmp_path):
    reports_dir = tmp_path / "reports"
    for d in ["2026-08-30", "2026-08-24", "2026-08-23", "2026-08-01"]:
        (reports_dir / d).mkdir(parents=True)
        (reports_dir / d / "v0.28.0-gpu-before.json").write_text("{}")

    prune_old_reports(reports_dir, current_date="2026-08-30", retention_days=7)

    remaining = {p.name for p in reports_dir.iterdir()}
    assert remaining == {"2026-08-30", "2026-08-24"}


def test_prune_old_reports_missing_dir_is_a_noop(tmp_path):
    prune_old_reports(tmp_path / "does-not-exist", current_date="2026-08-30", retention_days=7)


def test_write_reports_index_lists_dirs_sorted_descending(tmp_path):
    reports_dir = tmp_path / "reports"
    for d in ["2026-08-24", "2026-08-30", "2026-08-29"]:
        (reports_dir / d).mkdir(parents=True)

    write_reports_index(reports_dir)

    index = json.loads((reports_dir / "index.json").read_text())
    assert index == ["2026-08-30", "2026-08-29", "2026-08-24"]


from aggregate import trim_report_for_storage


def test_trim_report_for_storage_keeps_only_dashboard_fields():
    report = {
        "Results": [
            {
                "Target": "os-pkgs",
                "Vulnerabilities": [
                    {
                        "VulnerabilityID": "CVE-2026-00001", "PkgName": "libfoo",
                        "InstalledVersion": "1.0", "FixedVersion": "1.1", "Severity": "HIGH",
                        "Title": "some issue", "Description": "a very long description...",
                        "References": ["https://example.com/1", "https://example.com/2"],
                        "Layer": {"Digest": "sha256:...", "DiffID": "sha256:..."},
                    },
                ],
            }
        ]
    }

    trimmed = trim_report_for_storage(report)

    assert trimmed == {
        "Results": [
            {
                "Vulnerabilities": [
                    {
                        "VulnerabilityID": "CVE-2026-00001", "PkgName": "libfoo",
                        "InstalledVersion": "1.0", "FixedVersion": "1.1", "Severity": "HIGH",
                        "Title": "some issue",
                    }
                ]
            }
        ]
    }


def test_trim_report_for_storage_handles_missing_results():
    assert trim_report_for_storage({}) == {"Results": []}


from aggregate import run as aggregate_run


def test_run_merges_copies_and_appends_history(tmp_path):
    scan_dir = tmp_path / "scan"
    scan_dir.mkdir()
    results_dir = tmp_path / "results"

    before = {"Results": [{"Vulnerabilities": [
        {"VulnerabilityID": "CVE-1", "PkgName": "libfoo", "InstalledVersion": "1.0",
         "FixedVersion": "1.1", "Severity": "HIGH", "Title": "some issue"}
    ]}]}
    after = {"Results": [{"Vulnerabilities": []}]}
    summary = {
        "version": "v0.28.0", "variant": "gpu", "image": "vllm/vllm-openai:v0.28.0",
        "scanned_at": "2026-08-30T00:00:00Z",
        "before": {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 1},
        "after": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 0},
        "system_upgrade_ok": True, "python_upgrade_ok": True,
        "patched_image": "ghcr.io/owner/vllm-security/gpu:v0.28.0-patched",
        "status": "ok",
    }
    (scan_dir / "scan-v0.28.0-gpu-before.json").write_text(json.dumps(before))
    (scan_dir / "scan-v0.28.0-gpu-after.json").write_text(json.dumps(after))
    (scan_dir / "scan-v0.28.0-gpu.json").write_text(json.dumps(summary))

    expected_path = tmp_path / "expected.json"
    expected_path.write_text(json.dumps([
        {"version": "v0.28.0", "variant": "gpu", "image": "vllm/vllm-openai:v0.28.0"},
        {"version": "v0.28.0", "variant": "cpu", "image": "vllm/vllm-openai-cpu:v0.28.0"},
    ]))

    # Pre-existing history line from a prior run must survive the append.
    results_dir.mkdir()
    (results_dir / "history.jsonl").write_text(
        json.dumps({"date": "2026-08-29", "version": "v0.27.0", "variant": "gpu",
                     "before": None, "after": None, "patched_image": None, "status": "ok"}) + "\n"
    )

    aggregate_run(scan_dir=scan_dir, expected_path=expected_path, results_dir=results_dir, date="2026-08-30")

    merged = json.loads((results_dir / "latest" / "summary.json").read_text())
    assert len(merged) == 2
    assert any(e["status"] == "job_failed" and e["variant"] == "cpu" for e in merged)

    assert json.loads((results_dir / "reports" / "2026-08-30" / "v0.28.0-gpu-before.json").read_text()) == {
        "Results": [{"Vulnerabilities": [
            {"VulnerabilityID": "CVE-1", "PkgName": "libfoo", "InstalledVersion": "1.0",
             "FixedVersion": "1.1", "Severity": "HIGH", "Title": "some issue"}
        ]}]
    }
    assert json.loads((results_dir / "reports" / "2026-08-30" / "v0.28.0-gpu-after.json").read_text()) == {
        "Results": [{"Vulnerabilities": []}]
    }
    assert not (results_dir / "reports" / "2026-08-30" / "v0.28.0-cpu-before.json").exists()

    index = json.loads((results_dir / "reports" / "index.json").read_text())
    assert index == ["2026-08-30"]

    history_lines = (results_dir / "history.jsonl").read_text().strip().splitlines()
    assert len(history_lines) == 3  # 1 pre-existing + 2 from this run
    dates_versions = {(json.loads(l)["date"], json.loads(l)["version"]) for l in history_lines}
    assert ("2026-08-29", "v0.27.0") in dates_versions
    assert ("2026-08-30", "v0.28.0") in dates_versions


def test_run_replaces_same_date_history_rows_instead_of_duplicating(tmp_path):
    """A same-day re-run (e.g. a manual workflow_dispatch) must not double-count.

    The dashboard sums per-date values, so a duplicate (date, version, variant)
    row would show a spurious spike forever.
    """
    scan_dir = tmp_path / "scan"
    scan_dir.mkdir()
    results_dir = tmp_path / "results"
    results_dir.mkdir()

    summary = {
        "version": "v0.28.0", "variant": "gpu", "image": "vllm/vllm-openai:v0.28.0",
        "scanned_at": "2026-08-30T12:00:00Z",
        "before": {"CRITICAL": 0, "HIGH": 7, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 7},
        "after": {"CRITICAL": 0, "HIGH": 2, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 2},
        "system_upgrade_ok": True, "python_upgrade_ok": True,
        "patched_image": "ghcr.io/owner/vllm-security/gpu:v0.28.0-patched",
        "status": "ok",
    }
    (scan_dir / "scan-v0.28.0-gpu.json").write_text(json.dumps(summary))

    expected_path = tmp_path / "expected.json"
    expected_path.write_text(json.dumps([
        {"version": "v0.28.0", "variant": "gpu", "image": "vllm/vllm-openai:v0.28.0"},
    ]))

    # Seed history as if today's run already happened once (stale counts), plus
    # two rows that must survive untouched: a different date, and a different
    # (version, variant) on the same date.
    stale_today = {"date": "2026-08-30", "version": "v0.28.0", "variant": "gpu",
                   "before": {"total": 999}, "after": {"total": 999},
                   "patched_image": None, "status": "job_failed"}
    other_date = {"date": "2026-08-29", "version": "v0.28.0", "variant": "gpu",
                  "before": {"total": 5}, "after": {"total": 1},
                  "patched_image": None, "status": "ok"}
    other_combo_same_date = {"date": "2026-08-30", "version": "v0.27.0", "variant": "cpu",
                             "before": {"total": 3}, "after": {"total": 3},
                             "patched_image": None, "status": "ok"}
    (results_dir / "history.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in
                  [other_date, stale_today, other_combo_same_date]) + "\n"
    )

    aggregate_run(scan_dir=scan_dir, expected_path=expected_path, results_dir=results_dir, date="2026-08-30")

    rows = [json.loads(l) for l in
            (results_dir / "history.jsonl").read_text().strip().splitlines()]

    today_gpu = [r for r in rows if (r["date"], r["version"], r["variant"]) == ("2026-08-30", "v0.28.0", "gpu")]
    assert len(today_gpu) == 1, "same-date re-run must supersede, not duplicate"
    assert today_gpu[0]["before"]["total"] == 7  # the fresh row, not the stale 999
    assert today_gpu[0]["status"] == "ok"

    # Non-colliding rows are preserved verbatim.
    assert other_date in rows
    assert other_combo_same_date in rows
    assert len(rows) == 3


def test_run_prunes_reports_older_than_seven_days(tmp_path):
    scan_dir = tmp_path / "scan"
    scan_dir.mkdir()
    results_dir = tmp_path / "results"
    results_dir.mkdir()

    stale_dir = results_dir / "reports" / "2026-08-01"
    stale_dir.mkdir(parents=True)
    (stale_dir / "v0.27.0-gpu-before.json").write_text("{}")

    summary = {
        "version": "v0.28.0", "variant": "gpu", "image": "vllm/vllm-openai:v0.28.0",
        "scanned_at": "2026-08-30T00:00:00Z",
        "before": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 0},
        "after": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0, "total": 0},
        "system_upgrade_ok": True, "python_upgrade_ok": True,
        "patched_image": "ghcr.io/owner/vllm-security/vllm-openai:v0.28.0-20260830",
        "status": "ok",
    }
    (scan_dir / "scan-v0.28.0-gpu.json").write_text(json.dumps(summary))
    (scan_dir / "scan-v0.28.0-gpu-before.json").write_text("{}")
    (scan_dir / "scan-v0.28.0-gpu-after.json").write_text("{}")

    expected_path = tmp_path / "expected.json"
    expected_path.write_text(json.dumps([
        {"version": "v0.28.0", "variant": "gpu", "image": "vllm/vllm-openai:v0.28.0"},
    ]))

    aggregate_run(scan_dir=scan_dir, expected_path=expected_path, results_dir=results_dir, date="2026-08-30")

    assert not stale_dir.exists()
    index = json.loads((results_dir / "reports" / "index.json").read_text())
    assert index == ["2026-08-30"]
