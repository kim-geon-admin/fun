from __future__ import annotations

import argparse
import os
import sys
import time
from collections.abc import Callable
from typing import Protocol, TextIO

from .activity import ActivityPlan, compose_plan
from .banner import banner, dashboard, should_use_color, simulation_notice, startup_stage
from .commands import handle_command
from .init_performance import InitPerformance

PROMPT = "CDDEX > "


class PerformanceRunner(Protocol):
    """Structural interface for the fictional `/init` event renderer."""

    def run(
        self,
        write: Callable[[str], None],
        use_color: bool,
        now: Callable[[], float],
        sleep: Callable[[float], None],
    ) -> int: ...


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cddex",
        description="A colorful terminal performance that simulates agent activity.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.22,
        help="seconds between simulated activity lines (default: 0.22)",
    )
    parser.add_argument("--no-delay", action="store_true", help="print activity lines immediately")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI color")
    return parser


def write_line(stream: TextIO, text: str) -> None:
    print(text, file=stream, flush=True)


def write_and_flush(stream: TextIO, text: str) -> None:
    """Write one live performance event and make it visible immediately."""
    stream.write(text)
    stream.flush()


def render_plan(stream: TextIO, plan: ActivityPlan, delay: float) -> None:
    for stage in plan.stages:
        write_line(stream, stage)
        if delay:
            time.sleep(delay)
    write_line(stream, "")
    write_line(stream, f"CDDEX 요약 · {plan.summary}")
    write_line(stream, plan.closing)
    write_line(stream, "")


def main(
    argv: list[str] | None = None,
    input_fn: Callable[[str], str] = input,
    output: TextIO | None = None,
    performance: PerformanceRunner | None = None,
) -> int:
    """Run the interactive simulated console and return a process exit code."""
    args = build_parser().parse_args(argv)
    stream = output or sys.stdout
    color_enabled = should_use_color(args.no_color or bool(os.environ.get("NO_COLOR")))
    delay = 0.0 if args.no_delay else max(args.delay, 0.0)
    theme_index = 0
    performance = performance if performance is not None else InitPerformance()

    write_line(stream, startup_stage(color_enabled, theme_index))
    write_line(stream, simulation_notice(color_enabled, theme_index))
    write_line(stream, "fictional tools: scan_workspace · trace_signal · patch_theory · error_oracle")
    write_line(stream, "무엇을 꾸며 볼까요?  /help  /status  /theme  /exit")

    while True:
        try:
            text = input_fn(PROMPT).strip()
        except (EOFError, KeyboardInterrupt):
            write_line(stream, "CDDEX: 무대 조명을 끕니다. 안녕!")
            return 0

        if not text:
            write_line(stream, "CDDEX: 한 줄만 던져 주세요. 상상 엔진은 예열 중입니다.")
            continue

        command = handle_command(text, theme_index)
        if command.handled:
            theme_index = command.theme_index
            if command.clear_screen:
                write_line(stream, "\033[2J\033[H" if color_enabled else "─" * 56)
            if command.output:
                write_line(stream, command.output)
            if command.run_init:
                try:
                    performance.run(
                        lambda text: write_and_flush(stream, text),
                        use_color=color_enabled,
                        now=time.monotonic,
                        sleep=time.sleep,
                    )
                except KeyboardInterrupt:
                    write_line(stream, "[SIMULATED] /init cancelled; fictional session returned to CDDEX >")
            if command.should_exit:
                return 0
            continue

        render_plan(stream, compose_plan(text), delay)


if __name__ == "__main__":
    raise SystemExit(main())

