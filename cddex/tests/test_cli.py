from __future__ import annotations

import io
import os
import time
import unittest
from unittest.mock import patch

from cddex.cli import PROMPT, main


class FakePerformance:
    def __init__(self) -> None:
        self.calls: list[tuple[bool, object, object]] = []

    def run(self, write, use_color: bool, now, sleep) -> int:  # type: ignore[no-untyped-def]
        self.calls.append((use_color, now, sleep))
        write("[SIMULATED] fake init completed")
        return 1


class InterruptingPerformance:
    def __init__(self) -> None:
        self.calls = 0

    def run(self, write, use_color: bool, now, sleep) -> int:  # type: ignore[no-untyped-def]
        self.calls += 1
        raise KeyboardInterrupt


class FlushTrackingStringIO(io.StringIO):
    def __init__(self) -> None:
        super().__init__()
        self.flush_count = 0

    def flush(self) -> None:
        self.flush_count += 1
        super().flush()


class FlushAwarePerformance:
    def __init__(self, stream: FlushTrackingStringIO) -> None:
        self.stream = stream
        self.flush_counts: list[int] = []

    def run(self, write, use_color: bool, now, sleep) -> int:  # type: ignore[no-untyped-def]
        write("[SIMULATED] first fictional init event\n")
        self.flush_counts.append(self.stream.flush_count)
        write("[SIMULATED] second fictional init event\n")
        self.flush_counts.append(self.stream.flush_count)
        return 2


class CliTests(unittest.TestCase):
    def test_startup_displays_rich_stage(self) -> None:
        replies = iter(["/exit"])
        output = io.StringIO()
        main(["--no-delay", "--no-color"], input_fn=lambda _: next(replies), output=output)
        self.assertIn("stage manifest", output.getvalue())
        self.assertIn("fictional server", output.getvalue())
    def test_prompt_is_encodable_by_windows_cp949_console(self) -> None:
        PROMPT.encode("cp949")

    def test_request_streams_simulated_stages_then_exits(self) -> None:
        replies = iter(["README 파일 오류를 찾아줘", "/exit"])
        output = io.StringIO()

        code = main(["--no-delay", "--no-color"], input_fn=lambda _: next(replies), output=output)

        self.assertEqual(code, 0)
        self.assertIn("CDDEX", output.getvalue())
        self.assertIn("[SIMULATED 04/04]", output.getvalue())
        self.assertIn("가상 분석 결과", output.getvalue())

    def test_empty_input_does_not_start_plan(self) -> None:
        replies = iter(["", "/exit"])
        output = io.StringIO()

        main(["--no-delay", "--no-color"], input_fn=lambda _: next(replies), output=output)

        self.assertNotIn("[SIMULATED 01/04]", output.getvalue())
        self.assertIn("한 줄만 던져", output.getvalue())

    def test_clear_renders_the_existing_plain_text_clear_marker(self) -> None:
        replies = iter(["/clear", "/exit"])
        output = io.StringIO()

        self.assertEqual(
            main(["--no-delay", "--no-color"], input_fn=lambda _: next(replies), output=output),
            0,
        )

        self.assertIn("─" * 56, output.getvalue())

    def test_startup_uses_ansi_and_displays_dashboard_without_no_color(self) -> None:
        output = io.StringIO()

        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                main(["--no-delay"], input_fn=lambda _: "/exit", output=output),
                0,
            )

        self.assertIn("\033[", output.getvalue())
        self.assertIn("[SIMULATED] CDDEX stage manifest", output.getvalue())

    def test_no_color_environment_disables_ansi_sequences(self) -> None:
        output = io.StringIO()

        with patch.dict(os.environ, {"NO_COLOR": "1"}):
            self.assertEqual(
                main(["--no-delay"], input_fn=lambda _: "/exit", output=output),
                0,
            )

        self.assertNotIn("\033[", output.getvalue())

    def test_init_runs_injected_performance_with_stream_writer_and_runtime_hooks(self) -> None:
        replies = iter(["/init", "/exit"])
        output = io.StringIO()
        performance = FakePerformance()

        code = main(
            ["--no-delay", "--no-color"],
            input_fn=lambda _: next(replies),
            output=output,
            performance=performance,
        )

        self.assertEqual(code, 0)
        self.assertEqual(len(performance.calls), 1)
        self.assertFalse(performance.calls[0][0])
        self.assertIs(performance.calls[0][1], time.monotonic)
        self.assertIs(performance.calls[0][2], time.sleep)
        self.assertIn("[SIMULATED] fake init completed", output.getvalue())

    def test_init_without_no_color_passes_color_enabled_to_performance(self) -> None:
        replies = iter(["/init", "/exit"])
        output = io.StringIO()
        performance = FakePerformance()

        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                main(
                    ["--no-delay"],
                    input_fn=lambda _: next(replies),
                    output=output,
                    performance=performance,
                ),
                0,
            )

        self.assertTrue(performance.calls[0][0])

    def test_init_flushes_each_event_written_by_performance(self) -> None:
        replies = iter(["/init", "/exit"])
        output = FlushTrackingStringIO()
        performance = FlushAwarePerformance(output)

        self.assertEqual(
            main(
                ["--no-delay", "--no-color"],
                input_fn=lambda _: next(replies),
                output=output,
                performance=performance,
            ),
            0,
        )

        self.assertEqual(len(performance.flush_counts), 2)
        self.assertEqual(performance.flush_counts[1], performance.flush_counts[0] + 1)

    def test_init_keyboard_interrupt_cancels_session_and_returns_to_prompt(self) -> None:
        replies = iter(["/init", "/exit"])
        prompts: list[str] = []
        output = io.StringIO()
        performance = InterruptingPerformance()

        code = main(
            ["--no-delay", "--no-color"],
            input_fn=lambda prompt: (prompts.append(prompt), next(replies))[1],
            output=output,
            performance=performance,
        )

        self.assertEqual(code, 0)
        self.assertEqual(performance.calls, 1)
        self.assertEqual(prompts, [PROMPT, PROMPT])
        self.assertIn("[SIMULATED] /init cancelled", output.getvalue())

    def test_keyboard_interrupt_exits_zero(self) -> None:
        output = io.StringIO()

        def raise_interrupt(_: str) -> str:
            raise KeyboardInterrupt

        self.assertEqual(
            main(["--no-delay", "--no-color"], input_fn=raise_interrupt, output=output),
            0,
        )
        self.assertIn("무대 조명을 끕니다", output.getvalue())


if __name__ == "__main__":
    unittest.main()

