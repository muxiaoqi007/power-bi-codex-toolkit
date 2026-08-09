#!/usr/bin/env python3
"""Generate exact visual rectangles from a 12-column Power BI page grid."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def generate(spec: dict) -> dict:
    page = spec.get("page", {})
    width = page.get("width")
    height = page.get("height")
    margin = page.get("margin", 24)
    gap = page.get("gap", 16)
    header = page.get("header_height", 64)
    values = (width, height, margin, gap, header)
    if not all(isinstance(value, (int, float)) for value in values):
        raise ValueError("page width, height, margin, gap, and header_height must be numbers")
    if width <= 0 or height <= 0 or margin < 0 or gap < 0 or header < 0:
        raise ValueError("page dimensions must be positive; spacing values cannot be negative")

    usable_width = width - 2 * margin
    unit = (usable_width - 11 * gap) / 12
    if unit <= 0:
        raise ValueError("page is too narrow for the requested margin and gap")

    visuals = []
    if header:
        visuals.append({"name": spec.get("title_name", "page-title"), "x": margin, "y": margin, "width": usable_width, "height": header})
    y = margin + header + (gap if header else 0)
    for row_index, row in enumerate(spec.get("rows", [])):
        row_height = row.get("height")
        columns = row.get("columns", [])
        if not isinstance(row_height, (int, float)) or row_height <= 0:
            raise ValueError(f"row {row_index} height must be positive")
        spans = [column.get("span") for column in columns]
        if not columns or not all(isinstance(span, int) and 1 <= span <= 12 for span in spans):
            raise ValueError(f"row {row_index} columns require integer spans from 1 to 12")
        if sum(spans) > 12:
            raise ValueError(f"row {row_index} spans exceed 12 columns")
        cursor = 0
        for column_index, column in enumerate(columns):
            span = column["span"]
            name = column.get("name")
            if not isinstance(name, str) or not name.strip():
                raise ValueError(f"row {row_index} column {column_index} requires a name")
            x = margin + cursor * (unit + gap)
            visual_width = span * unit + (span - 1) * gap
            visuals.append({
                "name": name,
                "x": round(x, 2),
                "y": round(y, 2),
                "width": round(visual_width, 2),
                "height": row_height,
            })
            cursor += span
        y += row_height + gap
    if visuals and max(item["y"] + item["height"] for item in visuals) > height - margin:
        raise ValueError("generated rows exceed the page height")
    return {"page": {"width": width, "height": height}, "visuals": visuals}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args()
    try:
        result = generate(json.loads(args.spec.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
