# CDDEX fixed live panel design

## Purpose

Replace scrolling `/init` output with a contained ANSI live panel. It shows one CDDEX logo, four rotating fictional work rows, and a fixed footer that continuously displays elapsed time and a spinner.

## Layout

- Startup renders only `startup_stage`; the separate `banner` and sparse `dashboard` calls are removed to prevent duplicate logos.
- `/init` saves cursor state, clears the screen, and renders a panel with exactly four work rows plus one footer row.
- Each cycle redraws those fixed positions rather than appending history, so terminal scrollback does not grow during the session.
- Ctrl+C restores the saved cursor state, clears the panel, prints a simulated cancellation note, and returns to the prompt.

## Work rows

Each row is explicitly `SIMULATED` or `FICTIONAL` and includes a changing fictional activity, chunk number, byte count, buffer bar, and cursor offset. Examples: simulated shard read, fictional trace decode, imaginary buffer merge, and simulated index replay.

The row store is a four-item ring buffer: an incoming event removes the oldest row and appears as the newest. Data values are deterministic by cycle for tests.

## Footer

The bottom panel row remains fixed and updates every 0.15 seconds with a spinner/hourglass, `MM:SS` elapsed time, cycle count, active fictional operation, and Ctrl+C hint. ANSI uses absolute cursor movement; no-color/non-ANSI output retains the existing visible telemetry fallback.

## Safety and tests

All actions are fictional and no real resources are read. Tests cover a single startup logo, four-row buffer replacement, data-read markers, fixed ANSI cursor controls/footer, no-color fallback, and Ctrl+C restoration.

