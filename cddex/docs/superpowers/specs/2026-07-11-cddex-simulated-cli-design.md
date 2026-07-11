# CDDEX simulated CLI design

## Purpose

Build a Python command-line app named `cddex`. It is an intentionally fictional agent-console experience: it accepts real keyboard input, but never reads local files, executes commands, connects to services, or claims that simulated work is real.

The visual identity uses an original colorful ASCII `CDDEX` wordmark and a dark terminal theme. It does not reuse Codex, OpenAI, Hermes, or other product logos, names, or visual assets.

## Packaging and launch

- Use a `src/` package layout and `pyproject.toml`, following the supplied reference repository's packaging pattern.
- Register `cddex = "cddex.cli:main"` as the installed console command.
- Include `cddex.bat` for running the app from a source checkout on Windows.
- Require Python 3.11 or later and use only the standard library.

## Console experience

At startup, the app clears no terminal state and prints:

- An original, multicolor ASCII `CDDEX` banner.
- A visible disclaimer that all activities are simulated.
- Fictional runtime information, tool names, and workspace statistics clearly labelled as simulated or fictional.
- A prompt that accepts free-form user input.

For ordinary input, the app prints four short lines one at a time with a small configurable delay, then prints a Korean summary and a playful closing line. The stream must always visibly react to a user message before it returns to the prompt.

## Request behavior

`RequestClassifier` derives one or more intent labels by matching Korean and English keywords. `ActivityComposer` turns the result into a deterministic `ActivityPlan` containing a stage list, summary, and closing phrase.

| Intent | Example signals | Fictional activity |
| --- | --- | --- |
| file | 파일, 폴더, README, file, directory | imaginary index and preview scan |
| search | 검색, 찾아, search, find | signal trace and result ordering |
| code | 코드, 함수, patch, code | structure review and patch theory |
| error | 오류, 에러, bug, error | diagnostic isolation and recovery hypothesis |
| general | any unmatched input | intent mapping and idea synthesis |

Multiple matching intents are combined into one coherent stage sequence. Summaries are intentionally framed as fictional interpretations, not facts about a user system.

## Local commands

- `/help`: show available commands and the simulation notice.
- `/status`: show fictional runtime status, explicitly marked simulated.
- `/theme`: cycle safe ANSI color modes when the terminal supports color.
- `/clear`: emit ANSI clear-screen only when supported; otherwise print separator lines.
- `/exit` and `/quit`: leave cleanly.

EOF and Ctrl+C display a short farewell and exit with code zero. Unknown slash commands show a concise help hint.

## Modules

- `cddex.cli`: argument parsing, startup, REPL, stream output, and graceful exit.
- `cddex.banner`: ASCII banner and terminal color helpers.
- `cddex.classifier`: pure keyword-to-intent classification.
- `cddex.activity`: pure activity-plan construction.
- `cddex.commands`: pure local command routing.

The REPL is the only input/output boundary; classification and composition remain deterministic and independently testable.

## Error handling and accessibility

- ANSI color is disabled when output is not a TTY or `NO_COLOR` is set.
- No external configuration or system paths are required.
- Empty input returns a short friendly prompt and does not start a fake workflow.
- Startup and every plan include a visible simulation disclosure.

## Tests

Use `unittest` and validate:

- intent classification for Korean and English terms, including multi-intent input;
- each plan has four streaming stages, a simulation marker, a summary, and a closing phrase;
- local command routing and unknown-command handling;
- `--no-delay` operation for fast tests;
- CLI startup banner, disclaimer, normal request, and exit behavior.

## Out of scope

- Real filesystem inspection, web search, model/API calls, subprocesses, or persistent chat history.
- Reproducing a third-party product's brand, logo, layout, or messages.

