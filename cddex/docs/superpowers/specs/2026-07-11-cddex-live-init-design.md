# CDDEX live init performance design

## Purpose

Improve CDDEX from a short, plain response stream into a colorful fictional agent-console performance. The new `/init` command creates a 30-second live session that appears to inspect, reason, revise, and retry, while remaining entirely local, deterministic, and explicitly simulated.

## Visual presentation

- ANSI color is enabled by default, even if stdout does not identify as a TTY. `--no-color` remains the explicit opt-out.
- Palette meaning is stable: cyan for scans and navigation, violet for skills and reasoning, amber for work in progress, lime for successful validation, and coral for abandoned hypotheses or warnings.
- Startup expands into a compact pseudo-status dashboard containing fictional tool, skill, workspace, and profile entries. Every overview contains a `SIMULATED` or `FICTIONAL` marker.
- The original ASCII `CDDEX` wordmark remains CP949-encodable. It is colored line by line rather than replaced with copied product branding.

## `/init` behavior

`/init` invokes `InitPerformance.run`, which uses a monotonic clock to render a maximum 30-second session. It repeatedly cycles through stage recipes:

1. Scan an imaginary workspace or signal map.
2. Announce a fictional skill invocation.
3. Show a short artificial reasoning checkpoint.
4. Draft a pretend patch, memo, or hypothesis.
5. Validate it, then either continue or discard the hypothesis and retry.

At least once per cycle, the active status line is replaced using ANSI cursor-up and erase-line sequences. The replacement explicitly says that the previous fictional hypothesis was discarded or rewritten. Without color/ANSI support, the session appends a visible replacement line instead.

After the duration ends, `/init` prints a fictional session summary and returns to the prompt. It never reads files, invokes tools, starts subprocesses, connects to a service, or persists data.

## Interruption and commands

- Ctrl+C during `/init` cancels only the live session and returns to the prompt with a simulation notice.
- Ctrl+C at the normal prompt retains the existing clean application exit.
- `/exit` and `/quit` retain existing clean exit behavior.
- `/help` includes `/init`; `/status` names the current display mode as fictional.

## Architecture

- `cddex.banner`: palette, ANSI renderer, startup dashboard, and safe cursor rewrite helpers.
- `cddex.init_performance`: immutable event recipes and `InitPerformance` timing/rendering logic.
- `cddex.commands`: recognises `/init` without treating it as a regular completed command.
- `cddex.cli`: invokes the live performance, catches an in-session interrupt, and returns to the REPL.

`InitPerformance` accepts injected clock and sleep functions. Tests use a fake clock and zero-delay sleep function, so a 30-second simulated session completes immediately.

## Tests

- Default color policy and explicit no-color override.
- Dashboard includes fictional/simulated disclosures and the new command.
- `/init` produces multiple colored stage kinds, at least one replacement/retry, and a final session summary.
- Fake clock confirms the session ends at its configured duration without waiting in real time.
- Keyboard interrupt cancels `/init` and preserves the REPL; prompt-level Ctrl+C still exits.

## Out of scope

- Real inference, file inspection, shell commands, APIs, network traffic, or historical storage.
- Copying Codex, Hermes, OpenAI, or another product's exact logo, UI layout, copy, tool list, or identity.

