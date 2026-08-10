# bin — agentic utility belt

## NAME

A bin of agent skills, utility scripts, and shell configs

## SYNOPSIS

- [Agent Coordination](#agent-coordination) — `fhold`, `safewrite`
- [Shell Environment](#shell-environment) — `shellrc/`, login/interactive configs
- [File & Media Tools](#file--media-tools) — `mdar`, `fixexif`, `dupes`, `langlines`, `fakepath`, Fitbit
- [Network Tools](#network-tools) — `webmon`, `webstat`
- [Git Tools](#git-tools) — `commitz_ui`, `repo-emoji`
- [Shell Utilities](#shell-utilities) — `recd.sh`
- [AI Customizations](#ai-customizations) — commands, skills
- [Documentation](#documentation) — `docs/`
- [Patches](#patches) — `patches/`
- [Tests](#tests) — `test/`
- [Files](#files) — symlinks installed into `~/`

## DESCRIPTION

### Agent Coordination

- **`fhold`** — advisory hold protocol; coordinates IDE-reviewed vs. unreviewed parallel writes across agents. Two modes: *review* (single agent, diff visible in IDE) and *permit* (multiple agents, CAS writes via `safewrite`). See `docs/fhold.md`.
- **`safewrite`** — CAS-gated file writer. Writes to TARGET only if the file's sha256 matches `--expect-sha256`; uses a tmp-dir mutex with heartbeat to serialize concurrent agents and recover from crashes.

### Shell Environment

All files in `shellrc/` are symlinked into `~/`:

- **`shellrc.common`** — shared PATH, env vars, aliases; sourced by both zsh and bash
- **`zprofile`** / **`zshrc`** — zsh login / interactive config
- **`bash_profile`** / **`bashrc`** — bash login / interactive config
- **`setup.sh`** — initial Mac provisioning script
- **`python`** / **`pip`** — lightweight shims in repo root that forward to `python3` / `pip3`

### File & Media Tools

- **`mdar`** — archive and normalize AI-generated markdown docs into `aidocs/YYYY-MM-DD/hhmm_CamelName.md`; can also normalize a directory in-place. Skips patterns in `mdar_ignore`.
- **`fixexif`** / **`retouch`** — set image modtime and EXIF date from filename datetime prefix (`yyyy[-mm[-dd]] [hhmm]`). `retouch` is the shell wrapper; `fixexif` does the EXIF write.
- **`dupes`** — read a key+name stream from stdin; emit sets of duplicate files (key = inode or hash).
- **`langlines FILE`** — count lines by embedded language (Python / JS / CSS / HTML) in a Python source file containing multi-language string literals.
- **`fakepath PATH`** — generate a human-readable, unique filesystem-path identifier; used to create stable lock-file names.
- **`fitbit_to_csv.py`** — convert Fitbit JSON weight-export files to CSV (date, weight, BMI, fat%).
- **`fitbit_weights.sh`** — batch helper for Fitbit export processing.

### Network Tools

- **`webmon`** — poll internet connectivity against Google, Zoom, and Walmart in parallel; loop-friendly (`while true; do webmon; sleep 5; done`).
- **`webstat`** — one-shot probe: fires three parallel `curl --head` requests and exits 0 only if at least one succeeds.

### Git Tools

- **`commitz_ui`** — render a deterministic pending-commit menu from `git status` and upstream delta; output is computed from git state only (no freehand inventory). Used by the `/commitz` command.
- **`repo-emoji`** — print the emoji associated with a repo by reading `customColor` from `.idea/workspace.xml`.

### Shell Utilities

- **`recd.sh`** — smart `cd` with directory history and bookmarks; resolves bare patterns against DIRSTACK, history, and bookmarks. Install: `source recd.sh; alias cd=recd`.

### AI Customizations

#### Commands (`wibey/commands/`)

Canonical source lives in this repo. Install/adapt outward from here; do **not** treat any workspace-local `.github/` folder as the source of truth.

Custom slash commands in Claude markdown format. Install paths:

- Claude Code CLI: `~/.claude/commands/` (symlinks OK)
- Wibey VSCode: `~/.wibey/commands/` (must be hardlinks — Wibey's `isFile()` rejects symlinks)

Commands:

- **`commitz`** — cluster the next dirty IDEA git root into themed buckets; uses `commitz_ui` for deterministic file inventory.
- **`convo`** — render a timestamped markdown banner summarizing the current conversation (date, repo, branch, last-3-turns summary).
- **`say`** — render a timestamped markdown banner with custom user-provided message text.

#### Skills (`wibey/skills/`)

Markdown context documents invoked as skills in Wibey; usable as `@file` references in Claude Code.

For GitHub Copilot, any `.github/copilot-instructions.md` or `.github/skills/...` under a workspace is only an adapter layer. Keep the canonical content in this repo and project it into workspace-local Copilot hooks only where needed.

- **`doc-audit`** — consolidated reference for documentation authoring, task record format, audit checklist, and DRY principles.
- **`ftm`** — Family Tree Maker 2019 automation for Claude Desktop (screenshot + mouse/keyboard); navigates, edits, and sources facts in the Holtz Lusin tree.

### Documentation

All in `docs/`:

- **`AgentRules.md`** — global cross-laptop AI agent rules; symlinked to `~/.claude/CLAUDE.md` and `~/.cursor/cursorrules`. Canonical source of truth for agent behavior on all machines.
- **`fhold.md`** — fhold protocol reference: hold types, tag formats, contention resolution.
- **`ManPageRules.md`** — man-page typography style guide (colors, underline/italic/bold conventions).
- **`NewMacSetup.md`** — Mac provisioning checklist.
- **`ToDoMgt.md`** — todo/task management conventions.
- **`Tools.md`** — IDE/editor comparison matrix, extension patches, keybinding customizations.

### Patches

- **`patches/patch-zaaack.py`** — patches for the [zaaack](https://github.com/zaaack/vscode-markdown-editor) VSCode markdown preview extension (find/outline/anchor-nav fixes, IR-mode parity).

### Tests

`test/` contains unit and integration tests for core tools:

- `commitz_ui_test.py`, `fakepath_test.py`, `fhold_test.py`, `safewrite_test.py`
- `mdar_test/` — directory fixture for mdar integration tests

## FILES

Symlinks installed from this repo into `~/`:


| Symlink                 | Source                   |
| ------------------------- | -------------------------- |
| `~/.claude/CLAUDE.md`   | `docs/AgentRules.md`     |
| `~/.cursor/cursorrules` | `docs/AgentRules.md`     |
| `~/.shellrc.common`     | `shellrc/shellrc.common` |
| `~/.zprofile`           | `shellrc/zprofile`       |
| `~/.zshrc`              | `shellrc/zshrc`          |
| `~/.bash_profile`       | `shellrc/bash_profile`   |
| `~/.bashrc`             | `shellrc/bashrc`         |

Hardlinks (not symlinks — required by Wibey):


| Hardlink                       | Source                      |
| -------------------------------- | ----------------------------- |
| `~/.wibey/commands/commitz.md` | `wibey/commands/commitz.md` |
| `~/.wibey/commands/convo.md`   | `wibey/commands/convo.md`   |

For IDE workspace roots, use `~/lpscc` (the symlink) instead of `~/My Drive/Libertarian/LPSCC`; that keeps the LPSCC root attached to the shared-drive root rather than the local folder tree.

## SEE ALSO

- `docs/AgentRules.md` — full agent behavior spec including write rules, fhold protocol, and communication style

## AUTHOR

Brian Holtz `<brian@holtz.org>` — `github.com/BrianHoltz/tools`
