from __future__ import annotations

import unittest

from cddex.commands import handle_command


class CommandTests(unittest.TestCase):
    def test_help_is_handled_and_discloses_simulation(self) -> None:
        result = handle_command("/help", 0)

        self.assertTrue(result.handled)
        self.assertIn("SIMULATED", result.output)
        self.assertIn("/init", result.output)

    def test_init_requests_a_performance_session_without_exiting(self) -> None:
        result = handle_command("/init", 1)

        self.assertTrue(result.handled)
        self.assertTrue(result.run_init)
        self.assertFalse(result.should_exit)
        self.assertEqual(result.theme_index, 1)

    def test_theme_cycles_index(self) -> None:
        self.assertEqual(handle_command("/theme", 2).theme_index, 0)

    def test_exit_requests_clean_exit(self) -> None:
        self.assertTrue(handle_command("/quit", 0).should_exit)

    def test_unknown_slash_command_is_handled(self) -> None:
        result = handle_command("/warp", 0)

        self.assertTrue(result.handled)
        self.assertIn("/help", result.output)


if __name__ == "__main__":
    unittest.main()

