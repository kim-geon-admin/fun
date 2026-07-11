# CDDEX endless init telemetry design

## Purpose

Replace the bounded `/init` scene with a continuous, colorful fictional telemetry session. It should make the terminal feel actively occupied through varied fake messages, a live elapsed-time footer, and occasional visible retries, while retaining explicit simulation disclosures and avoiding all real operations.

## `/init` lifecycle

- `/init` runs until Ctrl+C is pressed; it does not automatically end after 30 seconds.
- Ctrl+C interrupts only the session, clears the live footer, prints a simulated cancellation notice, and returns to `CDDEX >`.
- The ordinary prompt-level Ctrl+C and `/exit` behavior stay unchanged.
- Tests use a `max_cycles` parameter and injected monotonic clock/sleep functions, never an unbounded real loop.

## Live presentation

- A new fictional event is emitted every 0.35 seconds by default.
- Events accumulate as readable colored history.
- A footer refreshes every 0.15 seconds in place using cursor save/restore/erase sequences. It contains elapsed time, cycle number, a rotating hourglass/spinner, a fictional active operation, and `Ctrl+C to return`.
- Every 6–8 emitted events, a visible rewrite replaces the latest fictional conclusion with an explicit discard/rebuild message.
- On a non-ANSI/no-color output stream, footer state is appended as labelled simulated telemetry instead of relying on cursor movement.

## Rich startup stage

Before the prompt appears, CDDEX renders a dense two-column fictional stage: its original CP949-safe ASCII wordmark and a custom abstract signal glyph occupy the left column; a compact stage manifest occupies the right column. The manifest includes all of the following, each labelled `SIMULATED` or `FICTIONAL`:

- runtime/version/upstream cue;
- fictional tool groups and short tool names;
- a fictional server/channel section;
- a fictional skill catalog arranged in wrapped categories;
- profile, session token, and catalog counts;
- a prompt command hint including `/init`.

The layout uses a colored divider and border when ANSI is active, but falls back to clean aligned ASCII when color is disabled. Its information density is inspired by the supplied terminal reference, but it does not reuse another product's logo, names, tool list, exact text, or identity.

## Message catalog and colors

The deterministic catalog has at least 16 message templates across these fictional categories:

- cyan: workspace and signal scans;
- blue: cache, routing, and index operations;
- violet: skill invocation and reasoning;
- amber: drafts and in-progress synthesis;
- lime: pretend verification and alignment;
- orange: queue reshuffling and recovery;
- pink/coral: discarded hypotheses and retries.

Each entry contains a `SIMULATED` or `FICTIONAL` marker. Template selection rotates predictably for tests but feels varied during a live run.

## Architecture

- `cddex.banner`: extended semantic palette, ANSI-capability helper, footer renderer, and rich startup stage with original logo, abstract glyph, and fictional manifest.
- `cddex.init_performance`: event catalog, infinite-by-default session loop, cycle counter, and live footer cadence.
- `cddex.cli`: writer callback that flushes every history event and footer update; no new real integrations.

The performance accepts `max_cycles: int | None`, `event_interval`, `footer_interval`, `now`, and `sleep` injection. `None` is the production infinite mode; tests pass a finite value.

## Tests

- Infinite default is represented by `max_cycles is None`; a finite fake-clock run emits the requested number of cycles.
- Catalog covers at least 16 templates and all specified palette roles.
- Footer contains elapsed time, cycle number, spinner/hoursglass frame, active fictional task, and Ctrl+C hint.
- Startup stage includes the original logo, abstract glyph, fictional tool/server/skill/profile sections, and a visible `/init` hint without copying the reference identity.
- ANSI footer update uses cursor controls; the plain fallback remains visible.
- Footer updates occur between events, history is flushed immediately, and a discard/rebuild rewrite appears in each finite test cycle.
- Existing no-color, cancellation, and no-real-operations guarantees remain covered.

## Out of scope

- Real agent inference, filesystem inspection, shell execution, service calls, network traffic, or persistence.
- Copying third-party product branding, assets, exact UI layouts, tool names, or copy.

