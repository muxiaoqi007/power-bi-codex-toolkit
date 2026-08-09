import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "skills" / "design-power-bi-report" / "scripts" / "generate_grid.py"
spec = importlib.util.spec_from_file_location("generate_grid", GENERATOR)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class GridGeneratorTests(unittest.TestCase):
    def fixture(self) -> dict:
        path = ROOT / "tests" / "fixtures" / "grid-spec.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_generates_expected_visual_count_and_bounds(self) -> None:
        result = module.generate(self.fixture())
        self.assertEqual(len(result["visuals"]), 7)
        self.assertEqual(result["visuals"][0]["name"], "overview-title")
        self.assertLessEqual(max(v["x"] + v["width"] for v in result["visuals"]), 1256)
        self.assertLessEqual(max(v["y"] + v["height"] for v in result["visuals"]), 696)

    def test_rejects_row_spans_over_twelve(self) -> None:
        data = self.fixture()
        data["rows"][0]["columns"][0]["span"] = 6
        with self.assertRaisesRegex(ValueError, "exceed 12"):
            module.generate(data)

    def test_rejects_rows_beyond_page_height(self) -> None:
        data = self.fixture()
        data["rows"][1]["height"] = 600
        with self.assertRaisesRegex(ValueError, "page height"):
            module.generate(data)


if __name__ == "__main__":
    unittest.main()
