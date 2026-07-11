from __future__ import annotations

from dataclasses import dataclass

THEME_COUNT = 3


@dataclass(frozen=True)
class CommandResult:
    handled: bool
    output: str = ""
    should_exit: bool = False
    run_init: bool = False
    clear_screen: bool = False
    theme_index: int = 0


def handle_command(text: str, theme_index: int) -> CommandResult:
    """Handle a local presentation command without invoking system resources."""
    command = text.casefold()
    if command in {"/exit", "/quit"}:
        return CommandResult(
            handled=True,
            output="CDDEX: 무대 조명을 끕니다. 안녕!",
            should_exit=True,
            theme_index=theme_index,
        )
    if command == "/help":
        return CommandResult(
            handled=True,
            output="[SIMULATED] /help /status /init /theme /clear /exit",
            theme_index=theme_index,
        )
    if command == "/status":
        return CommandResult(
            handled=True,
            output="[SIMULATED] runtime: lively | tools: fictional | workspace: imaginary",
            theme_index=theme_index,
        )
    if command == "/theme":
        return CommandResult(
            handled=True,
            output="[SIMULATED] 팔레트가 다음 장면으로 전환되었습니다.",
            theme_index=(theme_index + 1) % THEME_COUNT,
        )
    if command == "/clear":
        return CommandResult(handled=True, clear_screen=True, theme_index=theme_index)
    if command == "/init":
        return CommandResult(handled=True, run_init=True, theme_index=theme_index)
    if command.startswith("/"):
        return CommandResult(
            handled=True,
            output="알 수 없는 연출 지시입니다. /help를 입력해 보세요.",
            theme_index=theme_index,
        )
    return CommandResult(handled=False, theme_index=theme_index)

