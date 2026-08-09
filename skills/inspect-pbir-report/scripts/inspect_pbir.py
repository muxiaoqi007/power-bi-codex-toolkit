#!/usr/bin/env python3
"""Static, read-only inspection of Power BI Enhanced Report (PBIR) projects."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


NAME_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_-]*$")
SCHEMA_PREFIX = "https://developer.microsoft.com/json-schemas/fabric/item/report/"


@dataclass
class Finding:
    level: str
    code: str
    message: str
    path: str


class Inspector:
    def __init__(self) -> None:
        self.findings: list[Finding] = []
        self.reports = 0
        self.pages = 0
        self.visuals = 0

    def add(self, level: str, code: str, message: str, path: Path) -> None:
        self.findings.append(Finding(level, code, message, str(path)))

    def load_json(self, path: Path, required: bool = True) -> dict | None:
        if not path.is_file():
            if required:
                self.add("error", "missing_file", f"Required file is missing: {path.name}", path)
            return None
        try:
            raw = path.read_text(encoding="utf-8-sig")
            data = json.loads(raw)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            self.add("error", "invalid_json", str(exc), path)
            return None
        if isinstance(data, dict):
            schema = data.get("$schema")
            if schema and not str(schema).startswith(SCHEMA_PREFIX):
                self.add("warning", "unexpected_schema", "Schema URL is outside the expected Microsoft PBIR prefix", path)
        return data if isinstance(data, dict) else None

    def require(self, data: dict, keys: tuple[str, ...], path: Path) -> None:
        for key in keys:
            if key not in data:
                self.add("error", "missing_field", f"Missing required field: {key}", path)

    def inspect_report(self, report_dir: Path) -> None:
        self.reports += 1
        entry_path = report_dir / "definition.pbir"
        entry = self.load_json(entry_path)
        if entry:
            self.require(entry, ("version", "datasetReference"), entry_path)
            reference = entry.get("datasetReference") or {}
            if "byPath" in reference:
                local_path = (reference.get("byPath") or {}).get("path")
                if not local_path:
                    self.add("error", "empty_by_path", "datasetReference.byPath.path is missing", entry_path)
                elif not (report_dir / local_path).resolve().is_dir():
                    self.add("error", "missing_dataset_path", "Local datasetReference path does not resolve", entry_path)
            elif "byConnection" in reference:
                if not (reference.get("byConnection") or {}).get("connectionString"):
                    self.add("error", "missing_connection", "byConnection.connectionString is missing", entry_path)
            else:
                self.add("error", "invalid_dataset_reference", "datasetReference requires byPath or byConnection", entry_path)

        definition = report_dir / "definition"
        if not definition.is_dir():
            self.add("error", "missing_definition", "PBIR definition directory is missing", definition)
            return
        version_path = definition / "version.json"
        version = self.load_json(version_path)
        if version:
            self.require(version, ("$schema", "version"), version_path)
        report_path = definition / "report.json"
        report = self.load_json(report_path)
        if report:
            self.require(report, ("$schema", "themeCollection"), report_path)
        self.inspect_pages(definition / "pages")

    def inspect_pages(self, pages_dir: Path) -> None:
        list_path = pages_dir / "pages.json"
        listing = self.load_json(list_path)
        if not listing:
            return
        self.require(listing, ("$schema", "pageOrder"), list_path)
        order = listing.get("pageOrder")
        if not isinstance(order, list):
            self.add("error", "invalid_page_order", "pageOrder must be an array", list_path)
            return
        active = listing.get("activePageName")
        if active and active not in order:
            self.add("warning", "stale_active_page", "activePageName is not present in pageOrder", list_path)

        folders: dict[str, Path] = {}
        if pages_dir.is_dir():
            for child in pages_dir.iterdir():
                if child.is_dir():
                    slug = child.name[:-5] if child.name.endswith(".Page") else child.name
                    identifier = slug
                    try:
                        page_data = json.loads((child / "page.json").read_text(encoding="utf-8-sig"))
                        if isinstance(page_data.get("name"), str):
                            identifier = page_data["name"]
                    except (OSError, UnicodeError, json.JSONDecodeError):
                        pass
                    if identifier in folders:
                        self.add("error", "duplicate_page_name", f"Multiple page folders declare identifier: {identifier}", child)
                    folders[identifier] = child
                    if " " in child.name:
                        self.add("warning", "folder_space", "Page folder contains spaces; verify tool compatibility", child)
        for page_name in order:
            if not isinstance(page_name, str) or not NAME_RE.fullmatch(page_name):
                self.add("error", "invalid_page_name", f"Invalid page identifier: {page_name!r}", list_path)
                continue
            folder = folders.get(page_name)
            if not folder:
                self.add("error", "missing_page_folder", f"pageOrder references missing page folder: {page_name}", pages_dir)
                continue
            self.inspect_page(folder, page_name)
        for identifier, folder in folders.items():
            if identifier not in order:
                self.add("warning", "orphan_page", f"Page identifier is absent from pageOrder: {identifier}", folder)

    def inspect_page(self, page_dir: Path, expected_name: str) -> None:
        self.pages += 1
        page_path = page_dir / "page.json"
        page = self.load_json(page_path)
        if not page:
            return
        self.require(page, ("$schema", "name", "displayName", "displayOption", "width", "height"), page_path)
        if page.get("name") != expected_name:
            self.add("error", "page_name_mismatch", "page.json name does not match the folder/pageOrder identifier", page_path)
        width, height = page.get("width"), page.get("height")
        if not self.positive(width) or not self.positive(height):
            self.add("error", "invalid_page_size", "Page width and height must be positive numbers", page_path)
            return
        visuals_dir = page_dir / "visuals"
        rectangles: list[tuple[str, dict, Path]] = []
        if visuals_dir.is_dir():
            for folder in sorted(path for path in visuals_dir.iterdir() if path.is_dir()):
                if " " in folder.name:
                    self.add("warning", "folder_space", "Visual folder contains spaces; verify tool compatibility", folder)
                rectangle = self.inspect_visual(folder, width, height)
                if rectangle:
                    rectangles.append((rectangle[0], rectangle[1], folder / "visual.json"))
        for index, (left_name, left, left_path) in enumerate(rectangles):
            for right_name, right, _ in rectangles[index + 1 :]:
                if self.overlaps(left, right):
                    self.add("warning", "visual_overlap", f"Visuals overlap: {left_name} and {right_name}", left_path)

    def inspect_visual(self, visual_dir: Path, page_width: float, page_height: float) -> tuple[str, dict] | None:
        self.visuals += 1
        path = visual_dir / "visual.json"
        data = self.load_json(path)
        if not data:
            return None
        self.require(data, ("$schema", "name", "position"), path)
        if not ("visual" in data or "visualGroup" in data):
            self.add("error", "missing_visual_payload", "visual.json requires visual or visualGroup", path)
        name = data.get("name")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            self.add("error", "invalid_visual_name", f"Invalid visual identifier: {name!r}", path)
        position = data.get("position")
        if not isinstance(position, dict):
            self.add("error", "invalid_position", "position must be an object", path)
            return None
        required = ("x", "y", "width", "height")
        if not all(isinstance(position.get(key), (int, float)) for key in required):
            self.add("error", "invalid_position", "position requires numeric x, y, width, and height", path)
            return None
        if position["x"] < 0 or position["y"] < 0 or not self.positive(position["width"]) or not self.positive(position["height"]):
            self.add("error", "invalid_position", "Visual coordinates cannot be negative and dimensions must be positive", path)
        elif position["x"] + position["width"] > page_width or position["y"] + position["height"] > page_height:
            self.add("error", "visual_out_of_bounds", "Visual extends beyond the page canvas", path)
        return (name if isinstance(name, str) else visual_dir.name, position)

    @staticmethod
    def positive(value: object) -> bool:
        return isinstance(value, (int, float)) and value > 0

    @staticmethod
    def overlaps(a: dict, b: dict) -> bool:
        return not (a["x"] + a["width"] <= b["x"] or b["x"] + b["width"] <= a["x"] or a["y"] + a["height"] <= b["y"] or b["y"] + b["height"] <= a["y"])


def discover_reports(target: Path) -> list[Path]:
    resolved = target.resolve()
    if resolved.is_dir() and resolved.name.endswith(".Report"):
        return [resolved]
    root = resolved.parent if resolved.is_file() and resolved.suffix == ".pbip" else resolved
    return sorted(path for path in root.iterdir() if path.is_dir() and path.name.endswith(".Report")) if root.is_dir() else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    inspector = Inspector()
    reports = discover_reports(args.path)
    if not reports:
        inspector.add("error", "no_report", "No .Report directory was discovered", args.path)
    for report in reports:
        inspector.inspect_report(report)
    errors = sum(item.level == "error" for item in inspector.findings)
    warnings = sum(item.level == "warning" for item in inspector.findings)
    result = {"reports": inspector.reports, "pages": inspector.pages, "visuals": inspector.visuals, "errors": errors, "warnings": warnings, "findings": [asdict(item) for item in inspector.findings]}
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"PBIR static inspection: {inspector.reports} report(s), {inspector.pages} page(s), {inspector.visuals} visual(s)")
        for item in inspector.findings:
            print(f"{item.level.upper()} [{item.code}] {item.path}: {item.message}")
        if not inspector.findings:
            print("PASS: no static structural or layout findings")
    return 2 if errors else 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
