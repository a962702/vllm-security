"""Render the vulnerability summary table and splice it into README.md."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

START_MARKER = "<!-- scan-summary:start -->"
END_MARKER = "<!-- scan-summary:end -->"


def _format_counts(counts: dict | None) -> str:
    if not counts:
        return "-"
    return f"{counts['CRITICAL']}/{counts['HIGH']}/{counts['MEDIUM']}/{counts['LOW']}/{counts['UNKNOWN']}"


def render_summary_table(entries: list[dict]) -> str:
    header = (
        "| Version | Variant | Before (C/H/M/L/U) | After (C/H/M/L/U) | Status | Patched Image |\n"
        "|---|---|---|---|---|---|"
    )
    rows = []
    for entry in entries:
        patched = entry.get("patched_image") or "-"
        rows.append(
            f"| {entry['version']} | {entry['variant']} | "
            f"{_format_counts(entry.get('before'))} | {_format_counts(entry.get('after'))} | "
            f"{entry.get('status')} | {patched} |"
        )
    return "\n".join([header, *rows])


def update_readme(readme_text: str, table_md: str, timestamp: str, dashboard_url: str) -> str:
    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        raise ValueError("README is missing scan-summary markers")

    start_idx = readme_text.index(START_MARKER) + len(START_MARKER)
    end_idx = readme_text.index(END_MARKER)

    block = f"\n\n_Last scanned: {timestamp}_ · [Full dashboard]({dashboard_url})\n\n{table_md}\n\n"
    return readme_text[:start_idx] + block + readme_text[end_idx:]


def main() -> None:
    parser = argparse.ArgumentParser(description="Update README.md scan-summary block")
    parser.add_argument("--summary-path", type=Path, required=True)
    parser.add_argument("--readme-path", type=Path, required=True)
    parser.add_argument("--dashboard-url", required=True)
    parser.add_argument("--timestamp", required=True)
    args = parser.parse_args()

    entries = json.loads(args.summary_path.read_text())
    table = render_summary_table(entries)
    readme_text = args.readme_path.read_text()
    updated = update_readme(readme_text, table, args.timestamp, args.dashboard_url)
    args.readme_path.write_text(updated)


if __name__ == "__main__":
    main()
