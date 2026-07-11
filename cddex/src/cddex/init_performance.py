"""Endless fictional telemetry for the simulated ``/init`` flow."""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Callable
from cddex.banner import footer_line, paint, panel_frame, rewrite_line

@dataclass(frozen=True)
class InitEvent:
    role: str
    text: str

class InitPerformance:
    CATALOG = tuple(InitEvent(role, text) for role, text in (
        ("scan", "fictional scan: simulated workspace map"), ("skills", "fictional skill: simulated capability check"),
        ("skills", "fictional reasoning: simulated plan alignment"), ("work", "fictional draft/patch: simulated change set"),
        ("success", "fictional verification: simulated checks passed"), ("warning", "fictional retry: prior fictional hypothesis discarded and rewritten"),
        ("warning", "[SIMULATED RETRY] prior fictional hypothesis discarded and rebuilt"), ("scan", "[FICTIONAL TRACE] echo route widened"),
        ("blue", "[SIMULATED INDEX] lantern cache harmonized"), ("skills", "[FICTIONAL REASONING] prism lattice warming"),
        ("work", "[SIMULATED PATCH] cobalt thread rewritten"), ("success", "[FICTIONAL CHECK] narrative boundary stable"),
        ("orange", "[SIMULATED RECOVERY] idle sparks recollected"), ("warning", "[FICTIONAL WARNING] hypothesis folded for revision"),
        ("scan", "[SIMULATED DISCOVERY] imaginary node illuminated"), ("skills", "[FICTIONAL SKILL] retry-chorus singing"),
    ))
    def __init__(self, event_interval: float = .35, footer_interval: float = .15, max_cycles: int | None = None, duration: float | None = None, interval: float | None = None) -> None:
        if interval is not None: event_interval = interval
        if event_interval <= 0 or footer_interval <= 0: raise ValueError("intervals must be greater than zero")
        if duration is not None and max_cycles is None: max_cycles = max(1, math.ceil(duration / event_interval))
        self.event_interval, self.footer_interval, self.max_cycles, self.duration = event_interval, footer_interval, max_cycles, duration
    def run(self, write: Callable[[str], None], use_color: bool, now: Callable[[], float], sleep: Callable[[float], None]) -> int:
        started, events = now(), 0
        rows: list[str] = []
        while self.max_cycles is None or events < self.max_cycles:
            event = self.CATALOG[events % len(self.CATALOG)]
            events += 1
            chunk = events % 12 + 1
            amount = 1024 + (events * 413) % 6144
            bar = "#" * (events % 8 + 1) + "." * (8 - (events % 8 + 1))
            row = f"[SIMULATED READ] {event.text} · chunk {chunk:02d}/12 · bytes {amount / 1024:.1f} KiB · buffer [{bar}] · cursor {events * 137:04d}"
            rows.append(row)
            rows = rows[-4:]
            footer = footer_line(now() - started, events, events, "fictional data lattice", use_color)
            if use_color:
                write(panel_frame(rows, footer, True))
            else:
                write(row + "\n")
                write(footer + "\n")
            if events % 7 == 0 or (events == 6 and self.max_cycles is not None):
                if use_color:
                    rows[-1] = "[SIMULATED REBUILD] prior fictional hypothesis discarded and rebuilt · buffer refreshed"
                    write(panel_frame(rows, footer, True))
                else:
                    write(rewrite_line("[SIMULATED REBUILD] prior fictional hypothesis discarded and rebuilt", False))
            remaining = self.duration - (now() - started) if self.duration is not None else self.event_interval
            sleep(min(self.event_interval, max(0.0, remaining)))
        if self.max_cycles is not None and events:
            write(f"{paint('fictional init summary: simulated initialization complete', 'success', use_color)}\n")
        return events

