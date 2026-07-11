from __future__ import annotations

import unittest

from cddex.activity import compose_plan


class ActivityTests(unittest.TestCase):
    def test_plan_has_four_simulated_stages_and_summary(self) -> None:
        plan = compose_plan("코드 에러를 고쳐줘")

        self.assertEqual(len(plan.stages), 4)
        self.assertTrue(all("SIMULATED" in stage for stage in plan.stages))
        self.assertIn("가상", plan.summary)
        self.assertTrue(plan.closing)


if __name__ == "__main__":
    unittest.main()

