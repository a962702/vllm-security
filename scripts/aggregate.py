"""Aggregate per-image Trivy scan results into the published dashboard data."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

SEVERITY_KEYS = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]


def severity_counts(trivy_report: dict) -> dict:
    counts = {key: 0 for key in SEVERITY_KEYS}
    for result in trivy_report.get("Results") or []:
        for vuln in result.get("Vulnerabilities") or []:
            severity = (vuln.get("Severity") or "UNKNOWN").upper()
            if severity not in counts:
                severity = "UNKNOWN"
            counts[severity] += 1
    counts["total"] = sum(counts.values())
    return counts


def _cli_count_severity(path: str) -> None:
    with open(path, encoding="utf-8") as fh:
        report = json.load(fh)
    print(json.dumps(severity_counts(report)))


def merge_with_expected(expected: list[dict], found_summaries: dict[tuple[str, str], dict]) -> list[dict]:
    merged = []
    for combo in expected:
        key = (combo["version"], combo["variant"])
        if key in found_summaries:
            merged.append(found_summaries[key])
        else:
            merged.append(
                {
                    "version": combo["version"],
                    "variant": combo["variant"],
                    "image": combo["image"],
                    "scanned_at": None,
                    "before": None,
                    "after": None,
                    "system_upgrade_ok": None,
                    "python_upgrade_ok": None,
                    "patched_image": None,
                    "status": "job_failed",
                }
            )
    return merged


def build_history_lines(entries: list[dict], date: str) -> list[str]:
    lines = []
    for entry in entries:
        row = {
            "date": date,
            "version": entry["version"],
            "variant": entry["variant"],
            "before": entry.get("before"),
            "after": entry.get("after"),
            "patched_image": entry.get("patched_image"),
            "status": entry.get("status"),
        }
        lines.append(json.dumps(row, sort_keys=True))
    return lines


def is_within_retention(date_str: str, current_date: str, retention_days: int = 7) -> bool:
    current = datetime.strptime(current_date, "%Y-%m-%d").date()
    target = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (current - target).days < retention_days


def prune_old_reports(reports_dir: Path, current_date: str, retention_days: int = 7) -> None:
    if not reports_dir.exists():
        return
    for entry in reports_dir.iterdir():
        if not entry.is_dir():
            continue
        if not is_within_retention(entry.name, current_date, retention_days):
            shutil.rmtree(entry)


def write_reports_index(reports_dir: Path) -> None:
    dates = sorted((p.name for p in reports_dir.iterdir() if p.is_dir()), reverse=True)
    (reports_dir / "index.json").write_text(json.dumps(dates, indent=2))


KEPT_VULN_FIELDS = ["VulnerabilityID", "PkgName", "InstalledVersion", "FixedVersion", "Severity", "Title"]


def trim_report_for_storage(trivy_report: dict) -> dict:
    trimmed_results = []
    for result in trivy_report.get("Results") or []:
        vulns = [
            {field: vuln.get(field) for field in KEPT_VULN_FIELDS}
            for vuln in (result.get("Vulnerabilities") or [])
        ]
        trimmed_results.append({"Vulnerabilities": vulns})
    return {"Results": trimmed_results}


def run(scan_dir: Path, expected_path: Path, results_dir: Path, date: str) -> None:
    scan_dir = Path(scan_dir)
    results_dir = Path(results_dir)
    expected = json.loads(Path(expected_path).read_text())

    found_summaries: dict[tuple[str, str], dict] = {}
    for path in scan_dir.glob("scan-*.json"):
        if path.name.endswith("-before.json") or path.name.endswith("-after.json"):
            continue
        data = json.loads(path.read_text())
        found_summaries[(data["version"], data["variant"])] = data

    merged = merge_with_expected(expected, found_summaries)

    latest_dir = results_dir / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)
    (latest_dir / "summary.json").write_text(json.dumps(merged, indent=2))

    reports_dir = results_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    date_dir = reports_dir / date
    for combo in expected:
        for suffix in ("before", "after"):
            src = scan_dir / f"scan-{combo['version']}-{combo['variant']}-{suffix}.json"
            if src.exists():
                date_dir.mkdir(parents=True, exist_ok=True)
                trimmed = trim_report_for_storage(json.loads(src.read_text()))
                dst = date_dir / f"{combo['version']}-{combo['variant']}-{suffix}.json"
                dst.write_text(json.dumps(trimmed))

    if date_dir.exists() and not any(date_dir.iterdir()):
        date_dir.rmdir()

    prune_old_reports(reports_dir, current_date=date, retention_days=7)
    write_reports_index(reports_dir)

    # Read-modify-write rather than a blind append: re-running the workflow on a
    # day it already ran would otherwise leave duplicate rows for the same
    # (date, version, variant), and the dashboard sums per-date values -- so a
    # re-run day would show a permanent spurious spike.
    history_path = results_dir / "history.jsonl"
    new_lines = build_history_lines(merged, date)
    incoming_keys = {(entry["version"], entry["variant"]) for entry in merged}

    existing_lines: list[str] = []
    if history_path.exists():
        for line in history_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("date") == date and (row.get("version"), row.get("variant")) in incoming_keys:
                continue  # superseded by this run's fresh line for the same key
            existing_lines.append(line)

    history_path.write_text("\n".join(existing_lines + new_lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate scan-job outputs into dashboard data")
    subparsers = parser.add_subparsers(dest="command", required=True)

    count_parser = subparsers.add_parser("count-severity")
    count_parser.add_argument("path")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--scan-dir", type=Path, required=True)
    run_parser.add_argument("--expected-path", type=Path, required=True)
    run_parser.add_argument("--results-dir", type=Path, required=True)
    run_parser.add_argument("--date", required=True)

    args = parser.parse_args()
    if args.command == "count-severity":
        _cli_count_severity(args.path)
    elif args.command == "run":
        run(scan_dir=args.scan_dir, expected_path=args.expected_path, results_dir=args.results_dir, date=args.date)


if __name__ == "__main__":
    main()
