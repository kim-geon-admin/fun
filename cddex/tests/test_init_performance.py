from __future__ import annotations

import unittest

from cddex.init_performance import InitPerformance


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0
        self.sleeps: list[float] = []

    def now(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.value += seconds


class InitPerformanceTests(unittest.TestCase):
    def test_catalog_is_varied_and_finite_run_emits_telemetry(self) -> None:
        clock = FakeClock()
        lines: list[str] = []
        performance = InitPerformance(max_cycles=8, event_interval=0.1, footer_interval=0.05)
        count = performance.run(lines.append, False, clock.now, clock.sleep)
        self.assertEqual(count, 8)
        self.assertGreaterEqual(len(InitPerformance.CATALOG), 16)
        self.assertTrue(any("SIMULATED TELEMETRY" in line for line in lines))
        self.assertTrue(any("discarded" in line and "rebuilt" in line for line in lines))
    def test_rejects_a_nonpositive_interval(self) -> None:
        for interval in (0.0, -0.7):
            with self.subTest(interval=interval):
                with self.assertRaises(ValueError):
                    InitPerformance(interval=interval)

    def test_run_emits_a_complete_fictional_cycle_with_plain_rewrite(self) -> None:
        clock = FakeClock()
        output: list[str] = []

        event_count = InitPerformance(duration=4.2, interval=0.7).run(
            output.append,
            use_color=False,
            now=clock.now,
            sleep=clock.sleep,
        )

        rendered = "".join(output)
        self.assertGreater(event_count, 1)
        self.assertIn("fictional scan", rendered)
        self.assertIn("fictional skill", rendered)
        self.assertIn("fictional reasoning", rendered)
        self.assertIn("fictional draft/patch", rendered)
        self.assertIn("fictional verification", rendered)
        self.assertIn("fictional retry", rendered)
        self.assertIn("prior fictional hypothesis discarded and rewritten", rendered)
        self.assertIn("[SIMULATED REWRITE]", rendered)
        self.assertEqual(rendered.count("fictional init summary"), 1)
        self.assertGreaterEqual(clock.value, 4.2)
        self.assertTrue(all(seconds >= 0.0 for seconds in clock.sleeps))
        self.assertLessEqual(max(clock.sleeps), 0.7)

    def test_run_sleeps_only_for_the_remaining_final_duration(self) -> None:
        clock = FakeClock()

        InitPerformance(duration=1.0, interval=0.7).run(
            lambda text: None,
            use_color=False,
            now=clock.now,
            sleep=clock.sleep,
        )

        self.assertEqual(clock.value, 1.0)
        self.assertEqual(len(clock.sleeps), 2)
        self.assertEqual(clock.sleeps[0], 0.7)
        self.assertAlmostEqual(clock.sleeps[-1], 0.3)


if __name__ == "__main__":
    unittest.main()

