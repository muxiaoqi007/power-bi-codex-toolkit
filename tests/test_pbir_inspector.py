import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSPECTOR = ROOT / "skills" / "inspect-pbir-report" / "scripts" / "inspect_pbir.py"
module_spec = importlib.util.spec_from_file_location("inspect_pbir", INSPECTOR)
module = importlib.util.module_from_spec(module_spec)
assert module_spec.loader is not None
sys.modules[module_spec.name] = module
module_spec.loader.exec_module(module)


SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def create_report(root: Path, overlap: bool = False) -> Path:
    report = root / "Demo.Report"
    write_json(report / "definition.pbir", {
        "$schema": SCHEMA + "definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byConnection": {"connectionString": "placeholder"}},
    })
    write_json(report / "definition" / "version.json", {"$schema": SCHEMA + "version/1.0.0/schema.json", "version": "1.0.0"})
    write_json(report / "definition" / "report.json", {"$schema": SCHEMA + "report/3.2.0/schema.json", "themeCollection": {}})
    write_json(report / "definition" / "pages" / "pages.json", {"$schema": SCHEMA + "pagesMetadata/1.0.0/schema.json", "pageOrder": ["overview"], "activePageName": "overview"})
    page = report / "definition" / "pages" / "overview"
    write_json(page / "page.json", {"$schema": SCHEMA + "page/2.1.0/schema.json", "name": "overview", "displayName": "Overview", "displayOption": "FitToPage", "width": 1280, "height": 720})
    write_json(page / "visuals" / "sales" / "visual.json", {"$schema": SCHEMA + "visualContainer/2.7.0/schema.json", "name": "sales", "position": {"x": 24, "y": 100, "width": 400, "height": 200}, "visual": {}})
    write_json(page / "visuals" / "margin" / "visual.json", {"$schema": SCHEMA + "visualContainer/2.7.0/schema.json", "name": "margin", "position": {"x": 300 if overlap else 440, "y": 100, "width": 400, "height": 200}, "visual": {}})
    return report


class PBIRInspectorTests(unittest.TestCase):
    def test_clean_report_has_no_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            inspector = module.Inspector()
            inspector.inspect_report(create_report(Path(temp)))
            self.assertEqual(inspector.findings, [])
            self.assertEqual((inspector.reports, inspector.pages, inspector.visuals), (1, 1, 2))

    def test_overlap_is_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            inspector = module.Inspector()
            inspector.inspect_report(create_report(Path(temp), overlap=True))
            self.assertTrue(any(item.code == "visual_overlap" and item.level == "warning" for item in inspector.findings))

    def test_readable_page_folder_maps_by_page_json_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = create_report(Path(temp))
            pages = report / "definition" / "pages"
            (pages / "overview").rename(pages / "Executive Overview.Page")
            inspector = module.Inspector()
            inspector.inspect_report(report)
            self.assertFalse(any(item.code == "missing_page_folder" for item in inspector.findings))

    def test_missing_page_folder_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = create_report(Path(temp))
            pages = report / "definition" / "pages" / "pages.json"
            write_json(pages, {"$schema": SCHEMA + "pagesMetadata/1.0.0/schema.json", "pageOrder": ["missing"]})
            inspector = module.Inspector()
            inspector.inspect_report(report)
            self.assertTrue(any(item.code == "missing_page_folder" and item.level == "error" for item in inspector.findings))

    def test_out_of_bounds_visual_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            report = create_report(Path(temp))
            visual = report / "definition" / "pages" / "overview" / "visuals" / "sales" / "visual.json"
            write_json(visual, {"$schema": SCHEMA + "visualContainer/2.7.0/schema.json", "name": "sales", "position": {"x": 1000, "y": 100, "width": 400, "height": 200}, "visual": {}})
            inspector = module.Inspector()
            inspector.inspect_report(report)
            self.assertTrue(any(item.code == "visual_out_of_bounds" for item in inspector.findings))


if __name__ == "__main__":
    unittest.main()
