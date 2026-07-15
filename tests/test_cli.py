from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from lfsweaver.cli import main


class CliTests(unittest.TestCase):
    def test_init_validate_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "lfsweaver.toml"
            plan = Path(directory) / "plan.json"
            self.assertEqual(main(["init", str(manifest)]), 0)
            self.assertEqual(main(["validate", str(manifest), "--json"]), 0)
            self.assertEqual(main(["plan", str(manifest), "--output", str(plan)]), 0)
            self.assertTrue(plan.is_file())


if __name__ == "__main__":
    unittest.main()
