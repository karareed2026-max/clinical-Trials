#!/usr/bin/env python3
"""Create the homepage status graphic from the existing AACT candidate data."""

from __future__ import annotations

import csv
import gzip
import html
from collections import Counter
from pathlib import Path


SOURCE = Path("data/processed/aact_trial_termination_candidate_2026-09-12.tsv.gz")
OUTPUT = Path("assets/aact_status_distribution.svg")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def main() -> None:
    counts: Counter[str] = Counter()
    with gzip.open(SOURCE, "rt", encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            counts[row["overall_status"] or "Not reported"] += 1

    statuses = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    total = sum(counts.values())
    width, left, right = 1120, 300, 96
    row_height, top = 42, 202
    chart_width = width - left - right
    height = top + row_height * len(statuses) + 86
    max_count = max(counts.values())

    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Clinical trial status distribution</title>',
        '<desc id="desc">Counts and percentages of 602,514 AACT studies by overall status. Terminated studies are highlighted in coral.</desc>',
        '<rect width="100%" height="100%" fill="#f7f4ed"/>',
        '<style>text{font-family:DM Sans,Arial,sans-serif;fill:#183642}.title{font-family:Space Grotesk,Arial,sans-serif;font-size:30px;font-weight:700}.subtitle{font-size:15px;fill:#42616a}.label{font-size:15px;font-weight:700}.value{font-size:14px;font-weight:500}.tick{font-size:12px;fill:#42616a}.grid{stroke:#d9e2df;stroke-width:1}.bar{fill:#b8d8d8}.terminated{fill:#e76f51}.rule{stroke:#e76f51;stroke-width:2}</style>',
        '<text x="56" y="56" class="title">Where studies stand</text>',
        f'<text x="56" y="84" class="subtitle">{total:,} AACT-registered studies, grouped by their original overall status</text>',
        '<line x1="56" y1="112" x2="1064" y2="112" class="rule"/>',
        '<text x="56" y="146" class="subtitle">TERMINATED is highlighted. Other categories remain distinct; they are not treated as one comparison group.</text>',
        '<text x="300" y="178" class="tick">Number of studies</text>',
    ]

    for index, (status, count) in enumerate(statuses):
        y = top + index * row_height
        bar_width = max(2, chart_width * count / max_count)
        percentage = count / total * 100
        bar_class = "terminated" if status == "TERMINATED" else "bar"
        svg.extend([
            f'<line x1="{left}" y1="{y + 25}" x2="{left + chart_width}" y2="{y + 25}" class="grid"/>',
            f'<text x="{left - 18}" y="{y + 22}" class="label" text-anchor="end">{esc(status)}</text>',
            f'<rect x="{left}" y="{y + 5}" width="{bar_width:.1f}" height="22" rx="3" class="{bar_class}"/>',
            f'<text x="{left + bar_width + 12:.1f}" y="{y + 22}" class="value">{count:,}  ({percentage:.1f}%)</text>',
        ])

    svg.append(f'<text x="56" y="{height - 26}" class="tick">Source: AACT candidate dataset snapshot 2026-09-12 • descriptive counts, not causal evidence</text>')
    svg.append('</svg>')
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(svg), encoding="utf-8")


if __name__ == "__main__":
    main()