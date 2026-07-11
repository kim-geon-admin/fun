from __future__ import annotations

import os
from typing import TextIO

RESET = "\033[0m"
PALETTES = (
    {
        "scan": "\033[96m",
        "skills": "\033[95m",
        "work": "\033[93m",
        "success": "\033[92m",
        "warning": "\033[91m",
    },
    {
        "scan": "\033[36m",
        "skills": "\033[35m",
        "work": "\033[33m",
        "success": "\033[32m",
        "warning": "\033[31m",
    },
    {
        "scan": "\033[94m",
        "skills": "\033[95m",
        "work": "\033[93m",
        "success": "\033[92m",
        "warning": "\033[91m",
    },
)
ROLE_ALIASES = {
    "navigation": "scan",
    "reasoning": "skills",
    "progress": "work",
    "validation": "success",
    "discarded": "warning",
}

WORDMARK = (
    "  CCCCC  DDDDD   DDDDD   EEEEE  X   X\n"
    " C       D    D  D    D  E       X X \n"
    " C       D    D  D    D  EEEE     X  \n"
    " C       D    D  D    D  E       X X \n"
    "  CCCCC  DDDDD   DDDDD   EEEEE  X   X"
)


def should_use_color(disabled: bool) -> bool:
    """Color is on by default; callers explicitly opt out with ``disabled``."""
    return not disabled


def use_ansi(stream: TextIO) -> bool:
    """Keep the legacy stream-based color decision API, without a TTY gate."""
    del stream
    return should_use_color(disabled=bool(os.environ.get("NO_COLOR")))


def paint(text: str, role: str, enabled: bool, theme_index: int = 0) -> str:
    """Paint text using a semantic role from the selected terminal palette."""
    if not enabled:
        return text
    role = ROLE_ALIASES.get(role, role)
    color = role if role.startswith("\033[") else PALETTES[theme_index % len(PALETTES)].get(role, PALETTES[0]["scan"])
    return f"{color}{text}{RESET}"


def banner(use_color: bool, theme_index: int = 0) -> str:
    """Return the original CP949-safe CDDEX wordmark and fictional subtitle."""
    roles = ("scan", "skills", "work", "success", "warning")
    logo = "CDDEX\n" + WORDMARK if not use_color else "\n".join(
        paint(line, roles[index % len(roles)], True, theme_index)
        for index, line in enumerate(WORDMARK.splitlines())
    )
    subtitle = "CDDEX / fictional simulated console"
    return f"{logo}\n{paint(subtitle, 'scan', use_color, theme_index)}"


def simulation_notice(use_color: bool, theme_index: int = 0) -> str:
    notice = "[SIMULATED] All activity is fictional; no real files, commands, networks, or persistence are used."
    return paint(notice, "warning", use_color, theme_index)


def dashboard(use_color: bool, theme_index: int) -> str:
    """Render a fictional dashboard that explicitly discloses the simulation."""
    lines = (
        ("[SIMULATED] CDDEX fictional tools dashboard", "warning"),
        ("profile: fictional-coral", "scan"),
        ("workspace: /simulated/aurora", "scan"),
        ("skill: violet-reasoning", "skills"),
        ("work: amber queue is simulated", "work"),
        ("validation: lime checks are fictional", "success"),
        ("navigation: /init", "scan"),
    )
    return "\n".join(paint(text, role, use_color, theme_index) for text, role in lines)


def rewrite_line(text: str, use_color: bool) -> str:
    """Return a fictional terminal rewrite, with a plain-text disclosure fallback."""
    if use_color:
        return f"\033[1A\033[2K{text}\n"
    return f"{text}\n[SIMULATED REWRITE]\n"


def startup_stage(use_color: bool, theme_index: int = 0) -> str:
    """Render the dense, entirely fictional stage shown before the prompt."""
    left = ("CDDEX", *WORDMARK.splitlines(), "", "  .-.-.  ", " / o o ", " |  ^  |", "  `-+-' ")
    right = (
        "[SIMULATED] CDDEX stage manifest",
        "fictional tools: prism_scan · echo_route · patch_bloom",
        "fictional server: aurora-channel / 7 imaginary signals",
        "fictional skills: signal-weave · memo-mosaic · retry-chorus",
        "profile: prism-operator · catalog: 38 simulated tools",
        "commands: /init /help /status /theme /clear /exit",
    )
    rows = max(len(left), len(right))
    lines = []
    for index in range(rows):
        l = left[index] if index < len(left) else ""
        r = right[index] if index < len(right) else ""
        lines.append(f"{paint(l, 'scan', use_color, theme_index):<42} {paint(r, 'skills' if index in {2, 3} else 'work', use_color, theme_index)}")
    return "\n".join(lines)


def footer_line(elapsed: float, cycle: int, frame: int, active: str, use_color: bool) -> str:
    minutes, seconds = divmod(int(elapsed), 60)
    spinner = ("⌛", "⏳", "◜", "◝") if use_color else ("|", "/", "-", "\\")
    text = f"[SIMULATED TELEMETRY] {spinner[frame % len(spinner)]} {minutes:02d}:{seconds:02d} · cycle {cycle:02d} · {active} · Ctrl+C to return"
    return paint(text, "work", use_color)


def panel_frame(rows: list[str], footer: str, use_color: bool) -> str:
    """Render a compact fixed-height live work panel."""
    visible_rows = rows[-4:]
    visible_rows += ["[SIMULATED READ] waiting for fictional data..."] * (4 - len(visible_rows))
    if not use_color:
        return "\n".join(("[SIMULATED] live data reader", *visible_rows, footer))
    rendered = ["\033[2J\033[H", paint("[SIMULATED] CDDEX live data reader", "skills", True)]
    rendered.extend(paint(row, "scan", True) for row in visible_rows)
    rendered.append(paint(footer, "work", True))
    return "\n".join(rendered)

