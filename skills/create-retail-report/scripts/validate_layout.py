#!/usr/bin/env python3
"""Validate Power BI-style visual rectangles in a simple JSON layout spec."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED = ("name", "x", "y", "width", "height")


def overlaps(a: dict, b: dict) -> bool:
    return not (
        a["x"] + a["width"] <= b["x"]
        or b["x"] + b["width"] <= a["x"]
        or a["y"] + a["height"] <= b["y"]
        or b["y"] + b["height"] <= a["y"]
    )


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    page = data.get("page", {})
    width, height = page.get("width"), page.get("height")
    if not isinstance(width, (int, float)) or width <= 0:
        errors.append("page.width must be a positive number")
    if not isinstance(height, (int, float)) or height <= 0:
        errors.append("page.height must be a positive number")
    if errors:
        return errors

    visuals = data.get("visuals")
    if not isinstance(visuals, list):
        return ["visuals must be an array"]

    names: set[str] = set()
    valid: list[dict] = []
    for index, visual in enumerate(visuals):
        label = visual.get("name", f"visual[{index}]") if isinstance(visual, dict) else f"visual[{index}]"
        if not isinstance(visual, dict):
            errors.append(f"{label} must be an object")
            continue
        missing = [key for key in REQUIRED if key not in visual]
        if missing:
            errors.append(f"{label} missing: {', '.join(missing)}")
            continue
        if visual["name"] in names:
            errors.append(f"duplicate visual name: {visual['name']}")
        names.add(visual["name"])
        numeric = all(isinstance(visual[key], (int, float)) for key in REQUIRED[1:])
        if not numeric:
            errors.append(f"{label} coordinates and dimensions must be numbers")
            continue
        if visual["width"] <= 0 or visual["height"] <= 0:
            errors.append(f"{label} width and height must be positive")
            continue
        if visual["x"] < 0 or visual["y"] < 0 or visual["x"] + visual["width"] > width or visual["y"] + visual["height"] > height:
            errors.append(f"{label} is outside the {width}x{height} page")
        valid.append(visual)

    for index, left in enumerate(valid):
        for right in valid[index + 1 :]:
            if overlaps(left, right):
                errors.append(f"overlap: {left['name']} and {right['name']}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_layout.py <layout.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: {len(data.get('visuals', []))} visuals fit without overlap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
