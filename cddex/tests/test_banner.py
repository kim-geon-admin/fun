from __future__ import annotations

import io
import os
import unittest
from unittest.mock import patch

from cddex.banner import (
    WORDMARK,
    banner,
    dashboard,
    rewrite_line,
    should_use_color,
    simulation_notice,
    startup_stage,
    footer_line,
    panel_frame,
    use_ansi,
)


class BannerTests(unittest.TestCase):
    def test_startup_stage_contains_fictional_manifest(self) -> None:
        text = startup_stage(False)
        for item in ("CDDEX", "SIMULATED", "fictional tools", "fictional skills", "profile:", "/init"):
            self.assertIn(item, text)

    def test_footer_shows_time_cycle_spinner_and_hint(self) -> None:
        text = footer_line(125.4, 8, 1, "fictional signal weave", False)
        self.assertIn("02:05", text)
        self.assertIn("cycle 08", text)
        self.assertIn("Ctrl+C to return", text)

    def test_panel_frame_contains_fixed_rows_and_data_read_markers(self) -> None:
        frame = panel_frame(
            ["[SIMULATED READ] chunk 01/12 · bytes 3.4 KiB · buffer [####....] · cursor 0182"] * 4,
            "[SIMULATED TELEMETRY] 00:01",
            use_color=False,
        )
        self.assertEqual(frame.count("[SIMULATED READ]"), 4)
        self.assertIn("chunk 01/12", frame)
        self.assertIn("buffer", frame)
    def test_banner_contains_original_cddex_wordmark(self) -> None:
        self.assertIn("CDDEX", banner(use_color=False))

    def test_notice_discloses_simulation(self) -> None:
        self.assertIn("SIMULATED", simulation_notice(use_color=False))

    def test_color_is_enabled_by_default_even_for_non_tty_output(self) -> None:
        stream = io.StringIO()
        self.assertTrue(should_use_color(disabled=False))
        self.assertFalse(should_use_color(True))
        with patch.dict(os.environ, {}, clear=True):
            self.assertTrue(use_ansi(stream))
        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            self.assertFalse(use_ansi(stream))

    def test_dashboard_discloses_its_fictional_simulation(self) -> None:
        output = dashboard(use_color=False, theme_index=0)

        self.assertIn("SIMULATED", output)
        self.assertIn("fictional tools", output)
        self.assertIn("/init", output)
        self.assertIn("profile", output)
        self.assertIn("workspace", output)
        self.assertIn("skill", output)

    def test_rewrite_line_uses_ansi_or_a_visible_simulation_marker(self) -> None:
        self.assertEqual(rewrite_line("replacement", True), "\033[1A\033[2Kreplacement\n")
        self.assertEqual(
            rewrite_line("replacement", False),
            "replacement\n[SIMULATED REWRITE]\n",
        )

    def test_wordmark_is_encodable_by_windows_cp949_console(self) -> None:
        WORDMARK.encode("cp949")


if __name__ == "__main__":
    unittest.main()

