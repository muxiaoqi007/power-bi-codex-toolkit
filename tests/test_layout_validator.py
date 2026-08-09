import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "create-retail-report" / "scripts"))

from validate_layout import validate  # noqa: E402


class LayoutValidatorTests(unittest.TestCase):
    def fixture(self, name: str) -> dict:
        path = ROOT / "tests" / "fixtures" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def test_valid_layout_passes(self) -> None:
        self.assertEqual(validate(self.fixture("layout-valid.json")), [])

    def test_invalid_layout_reports_bounds_and_overlap(self) -> None:
        errors = validate(self.fixture("layout-invalid.json"))
        self.assertTrue(any("outside" in error for error in errors))
        self.assertTrue(any("overlap" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
