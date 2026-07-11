from __future__ import annotations

import unittest
from pathlib import Path


class LauncherTests(unittest.TestCase):
    def test_source_launcher_exposes_src_package_directory(self) -> None:
        launcher = Path("cddex.bat").read_text(encoding="utf-8")

        self.assertIn('set "PYTHONPATH=%~dp0src"', launcher)


if __name__ == "__main__":
    unittest.main()

