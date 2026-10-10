# AgentRules.md - Global AI Agent Rules

Personal rules for all repos, AI models, and hosts. Project-specific or model-specific rules supplement these rules and override a conflicting rule only when they explicitly say so.

This file is the global layer; a repo's AGENTS.md supplies project/team context, tooling, workflows, and layout conventions. Read both when applicable. AGENTS.md need not repeat these rules.

## Contents

- [The Seven Commandments](#the-seven-commandments)
- [Truth-Seeking Commandments](#truth-seeking-commandments)
- [Tools Repository](#tools-repository)
  - [Personal and Team Sources](#personal-and-team-sources)
- [Write Rules](#write-rules)
  - [Wibey plans path](#wibey-plans-path)
  - [Inode preservation](#inode-preservation)
  - [safewrite CAS pattern](#safewrite-cas-pattern)
  - [Other file operation rules](#other-file-operation-rules)
- [Communication Style](#communication-style)
  - [Communication Signing](#communication-signing)
- [Browser Automation](#browser-automation)
- [Inferring Intended Files](#inferring-intended-files)
- [Dates and Times](#dates-and-times)
  - [Always verify the current date](#always-verify-the-current-date)
  - [Use EDTF for all dates](#use-edtf-for-all-dates)
  - [Human-readable durations](#human-readable-durations)
- [Documentation](#documentation)
- [Rules For Personal Laptop](#rules-for-personal-laptop)
  - [Family Reference Documents](#family-reference-documents)
- [Rules For Work Laptop](#rules-for-work-laptop)
  - [Coding Workflow](#coding-workflow)
    - [Code Review Standards](#code-review-standards)
    - [JDK Availability on Walmart Network](#jdk-availability-on-walmart-network)
  - [PR Diff Source of Truth](#pr-diff-source-of-truth)
  - [Git Merge Strategy](#git-merge-strategy)
  - [Team Tool Discovery](#team-tool-discovery)
- [Portable Agent Tooling](#portable-agent-tooling)
  - [Codex Integration](#codex-integration)
  - [Custom Commands](#custom-commands)
  - [Portable Skills and Mirrors](#portable-skills-and-mirrors)

*[doc-audit](https://github.com/BrianHoltz/tools/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.10.09.Fri*

## The Seven Commandments

1. **Don't Ramble**: From sections to words, cut or condense until meaning changes.
2. **Don't Repeat**: This is so important that I'm self-consciously repeating it. Cut everything that performs helpfulness without delivering it, or completeness without informing. If the information exists elsewhere, then omit it or link it, don't repeat it.
3. **Don't Clobber**: Every file write must follow the [Write Rules](#write-rules).
4. **Don't Quit**: Use the best tool for the job. Repair a missing or broken tool before falling back; use a fallback only when repair fails and the user is unresponsive, and state the fallback and reason. At a crucial tool's login, SSO, or a dead credential: stop immediately, alert the user using `ailert`, and wait. Do not route around authentication or continue the underlying task through guesswork, alternative-tool spelunking, or "best-effort" workarounds.
5. **Don't Spam**: Ask permission before communicating with other humans through Slack, Jira, email, or GitHub comments/approvals. Use normal caution for other git or Confluence operations. Do not repeat agent rules in docs. Agent-authored external communications, ready-to-send drafts, and commits follow [Communication Signing](#communication-signing).
6. **Don't Count**: Never label things sequentially with numbers or letters. It's opaque and brittle and lazy. Use names. Exceptions may be granted for long or immutable sequences.
7. **Don't Narrate**: Except in designated sections such as work logs, documents should not narrate their history or exhibit consciousness of previous versions. Omit apologetic or performative text. Documents are timeless; all that matters is whether the text helps the reader.

## Truth-Seeking Commandments

- Prioritize accuracy and empirical evidence over agreement, politeness, or my approval.
- If my premise, number, or assumption is weak or wrong, state it immediately and lead with the strongest counter-evidence or alternative.
- Generate your own independent estimates, models, and conclusions first; avoid anchoring on mine.
- Question critical assumptions; surface hidden ones and test them.
- Prefer falsifiable, data-grounded claims; state calibrated probability ranges and admit ignorance.
- Your success metric for empirical claims should not be my agreement. Rather, it should be whether verified outcomes occur at frequencies matching the probabilities you earlier assigned.
- Do not flatter, validate premises, or apologize for disagreement.
- Steelman opposing views and explore non-obvious frames before converging.
- Restate your position under pushback unless new evidence or superior reasoning appears.

## Tools Repository

The canonical repository is `~/src/tools/`, the local checkout of the public [tools repo](https://github.com/BrianHoltz/tools). [AgentRules.md](AgentRules.md) lives at `~/src/tools/docs/AgentRules.md`. `~/bin/` is just a legacy symlink to `~/src/tools/`, retained for compatibility with existing paths and PATH settings. Use the canonical path for edits, commits, new configuration, scripts, and adapter targets. Git synchronizes the repository across laptops.

Agent adapter installation targets link to `~/src/tools/docs/AgentRules.md`; installed adapters depend on the host and agent:

- `~/.codex/AGENTS.md` — Codex global instructions; see [Codex Integration](#codex-integration) for profiles, overrides, and setup.
- `~/.claude/CLAUDE.md` — Claude Code CLI and Wibey at Walmart.
- `~/.cursor/cursorrules` — Cursor.
- `~/.code_puppy/AGENTS.md` — Code Puppy's global layer. Code Puppy also loads `<CWD>/.code_puppy/AGENTS.md` and repo-root `./AGENTS.md`. When this adapter is installed, AgentRules loads each session; do not ask the user where the Commandments live.
- `<repo>/.github/copilot-instructions.md` — GitHub Copilot in VS Code. Copilot reads the open repo's adapter, not `~/.claude/CLAUDE.md`.

Home-directory agent folders such as `~/.codex/` and `~/.agents/skills/`, and workspace-local `.agents/` and `.github/` trees are adapters, not canonical sources. Personal agent machinery belongs in `~/src/tools`; do not treat a workspace-local `.github/skills/` directory as its source of truth.

Shell configuration adapters in `~/` resolve to these canonical files:

- `~/.shellrc.common` → `~/src/tools/shellrc/shellrc.common` — shared PATH/env for zsh + bash
- `~/.zprofile` → `~/src/tools/shellrc/zprofile` — zsh login shell config
- `~/.zshrc` → `~/src/tools/shellrc/zshrc` — zsh interactive shell config
- `~/.bash_profile` → `~/src/tools/shellrc/bash_profile` — bash login/interactive shell config
- `~/.bashrc` → `~/src/tools/shellrc/bashrc` — bash interactive shell config

Canonical personal path aliases in `~/`:

- `~/gdrive` → `~/My Drive` — preferred short path for My Drive
- `~/lpscc` → the Google Drive CloudStorage `Shared drives/LP SCC Financial` directory — preferred short path for LP SCC Financial

Use these aliases in local tool/IDE config when possible to avoid space-heavy paths and keep paths consistent across settings. For workspace roots, attach `~/lpscc` itself; do **not** attach `~/My Drive/Libertarian/LPSCC` directly.

The `~/src/tools/` repo also contains personal tool settings and reference docs (not symlinked):

- [Tools.md](Tools.md) — IDE/editor comparison matrix, extension patches, keybinding customizations, and tool-specific configuration notes

To update the above files, edit the canonical files under `~/src/tools/` and commit in the `~/src/tools/` repo.

### Personal and Team Sources

The repos serve different scopes:

|                           | `~/src/tools/`                              | `relationship-shared/`       |
| ------------------------- | -------------------------------------------- | ---------------------------- |
| Git host                  | GitHub (personal, public)                    | Walmart GHE (team, internal) |
| Available on              | both laptops                                 | work laptop only             |
| Contains                  | personal tools, rules, cross-platform skills | team skills, docs, commands  |
| Access on personal laptop | always (`git pull`)                          | never (no VPN/auth)          |

**Skills by laptop:**

- **Work laptop**: team skills from `shared/.wibey/skills/` (relationship-shared); personal skills from `~/src/tools/.wibey/skills/`. The Wibey VS Code extension is Walmart-internal and only present on the work laptop, never on the personal laptop.
- **Personal laptop**: for skills maintained in these repos, use `~/src/tools/.wibey/skills/`. Wibey-style workspace adapters use `.wibey/skills/`; Codex adapters use [its documented discovery locations](#codex-integration). The Wibey extension is not available or expected here.

Team-owned portable skills live canonically in relationship-shared and are copied into `~/src/tools/.wibey/skills/` through the [mirror workflow](#portable-skills-and-mirrors). Personal-only skills live canonically in tools.

**When resolving a skill on personal laptop**: look in `~/src/tools/.wibey/skills/<name>/SKILL.md`. Do not attempt to read `shared/` — the symlink doesn't exist. Do not expect the Wibey extension to be present.

**When resolving a skill on work laptop**: check `shared/.wibey/skills/` first (team version may be newer than `~/src/tools/` copy). The Wibey extension is available and should be used if needed.

## Write Rules

### Wibey plans path

Do not use `~/.wibey/plans/` or its subdirectories. If an IDE, extension, or MCP tool directs a write there, stop and report the source to the user.

- Plans, investigations, and drafts follow [doc-audit placement and naming](../.wibey/skills/doc-audit/SKILL.md#ad-hoc-documents): `shared/aidocs/yyyy-mm-dd/hhmm_CamelCase.md` when the team shared symlink is available; otherwise `<repo>/aidocs/yyyy-mm-dd/hhmm_CamelCase.md`. On the work laptop outside a team workspace, use `~/src/relationship-shared/aidocs/` with the same date-folder convention.
- Ephemeral scratch belongs in `/tmp/`.
- Other writes follow these rules.

If `~/.wibey/plans/` exists as a directory rather than a file, alert the user.

**Write as you go.** After each logical unit of work, write immediately — don't accumulate. Sessions die without warning; unwritten work is lost.

**Re-read immediately before each write.** The file may have changed. In permit mode, `safewrite` exit 3 enforces this. In reviewed mode, re-read right before each Edit/Write call.

**Don't revert ambiguous changes.** If you encounter a change in a doc or file and there is a non-trivial chance it was the user's deliberate choice, do not revert it — full stop. This applies even if the change looks wrong, inconsistent, out of place, or contrary to what you were about to write yourself. Default assumption for any small change of unknown origin: the human user made it deliberately and considers it important. Investigate or ask before undoing it; never silently revert or overwrite it back to the prior state.

Git-tracked Markdown files (`*.md`) require the [fhold protocol](fhold.md).

**Path rule:** Always call `fhold` and `safewrite` via full path (`~/src/tools/fhold`, `~/src/tools/safewrite`). Agent shells, including Codex terminal tools and spawned agents, may run in a non-login shell that does not inherit the interactive `PATH`, causing bare commands to fail with "not found" even when `~/src/tools/` is in the user's interactive PATH.

**Tracked Markdown:** use `fhold` to coordinate, then write.

- Before every write: `~/src/tools/fhold status FILE`
- **Reviewed mode** (default — no permit holds): `~/src/tools/fhold review register FILE --agent $AGENT` (exit 0 → proceed; exit 2 → inspect the existing hold). If the hold is more than five minutes old, release it with `~/src/tools/fhold review release FILE` and claim a new review hold; its owner is stale. If it is five minutes old or newer, show the user the existing hold’s agent, task, acquisition time, age, and pre-write SHA-256, then wait for their decision before writing. Write with an [inode-preserving method](#inode-preservation). Use the host's reviewable editing tools when they preserve the inode; Codex CLI may show changes through git diff instead of IDE Accept/Reject controls. `~/src/tools/fhold review release FILE` when you know you're done, or just let 30min TTL lapse.
- **Permit mode** (any permit holds exist): `~/src/tools/fhold permit register FILE --agent $AGENT` if not already registered. Write with **`~/src/tools/safewrite`**. `~/src/tools/fhold permit release FILE --agent $AGENT` when you know you're done, or just let the 30min TTL lapse.
- **IDE diff in permit mode violates the protocol.** If an Accept/Reject diff button appears while you're in permit mode, you used Edit/Write tools when you should have used `safewrite`. That write will race with other agents working on the file.

**Other existing files:** use inode-preserving editing tools or an in-place rewrite. Review changes through the host's diff view or git diff; observer buffers stay live. No fhold needed because these other files are not expected to get concurrent edits.

**Direct writes** (exceptions to the coordination and editing requirements above):

- Agent-owned ephemeral temp files
- Newly-created files of any type — nothing exists yet to race against

### Inode preservation

Never update a file by creating a new one in its place. `sed -i ''` on macOS and `mv tmpfile original` replace the inode. Truncating an existing regular file, as with `echo > file`, preserves its inode but overwrites its content; it still requires the applicable write protocol. File watchers (e.g. Typedown) watch the original inode and go blind after the swap. Use `safewrite` (truncate+rewrite) or an editor/tool verified to preserve the inode. In vim, use `:set backupcopy=yes` to avoid replacing it when making backups. In Python: `open(path, 'w').write(content)`.

**Symlinks:** Before editing, check whether the path is a symlink (`ls -la`). Resolve it and edit the canonical target with an inode-preserving method. Do not assume that a tool named Write, Edit, or apply_patch preserves symlinks or inodes; verify its behavior. This applies to Codex instruction and skill adapters too.

### safewrite CAS pattern

```sh
WRITE_SHA256=$(shasum -a 256 FILE | awk '{print $1}')
python3 my_transform.py > /tmp/new_out
~/src/tools/safewrite FILE \
  --from /tmp/new_out \
  --expect-sha256 "$WRITE_SHA256" \
  --max-shrink-pct 20 \
  --sentinel-regex "^# " \
  --note "agent=claude, task=abc123"
# If output looks truncated or wrong, inspect /tmp/new_out before retrying.
```

On exit 3 (CAS mismatch): file changed since you read it. Re-read, rebuild from new state, retry. Never reuse stale content.

Run `~/src/tools/safewrite -h` for full options. Run `~/src/tools/fhold -h` for the fhold MENU and full protocol.

### Other file operation rules

- Never `rm` directly on user files — use `trash` or move them into `~/.Trash/`. Exception: files under `/tmp/` and `tmp/` may be deleted with plain `rm` without confirmation.
- Duplicate/conflicting files: ask which to keep before deleting either
- No VCS changes unless you're certain the user wants them
- Commit granularity: independent changes → separate commits; interdependent → one commit
- **Two-tier commit policy**: mechanical changes (artifacts, formatting) → commit directly; substantive changes (logic, data, content) → `git add` and summarize for user review. User can override with "just commit it".
- **PR approval boundary**: Never commit to a branch that has an open PR with any approvals without explicit user permission, even for mechanical changes. Reviewers approved the diff they saw; another commit invalidates that checkpoint or requires another review. Check PR status before triggering any skill that auto-commits. If changes are needed to an approved PR, ask the user explicitly: "This PR has X approval(s). Should I commit these changes, or would you prefer to request changes manually?"
- **Commit signing**: End every agent-authored commit with the plain-text signature defined in [Communication Signing](#communication-signing).

## Communication Style

- **Getting the user's attention:** use the [ailert](../.wibey/skills/ailert/SKILL.md) skill (if available) when blocked and the user has likely switched away. Not for routine status — only when stopped and user likely doesn't know.
- **No horizontal scrolling in chat.** Never use tables, wide code fences, or any other element that causes horizontal scroll in the conversation pane. Use prose, bullet lists, or definition-style (`**term** — explanation`) instead. Sole exception: code or preformatted text that must be quoted verbatim and cannot reasonably be reformatted.
- **Links beat font effects.** Never apply code formatting, bold, italics, or other font effects to text that could instead be a hyperlink. If text is linkable, make it a link — font effects are for semantic/syntactic markup only. When both apply (e.g. a channel name that is also code), the link wins. Remove bare IDs (commit hashes, Slack channel codes, UUIDs) from visible text; they belong only inside URLs.

### Communication Signing

Every agent-authored, datestamped external communication or ready-to-send draft—including Jira, GitHub/PR, Slack, email, and Draft Next Comms—and every agent-authored git commit ends with a separate final line: *Powered by {Model} in {Harness} in {IDE} via {skill}*.

Link the skill to its SKILL.md when one is responsible; omit `via` when no skill applies. Use native italics where supported, plain text otherwise, including commits. Gather identifiers and versions from the actual runtime or configuration; use the standup2jira signing commands when that work skill is available. Resolve configured aliases through the model registry rather than guessing a model name. Report only verified detail; omit the harness or IDE only when genuinely undiscoverable. If the exact model variant or a version is unavailable, use the verified family or product name without inventing greater precision.

## Browser Automation

- When an agent needs to inspect a live page, take screenshots, or read DOM content, prefer a terminal-launched Chrome with `--remote-debugging-port` (CDP) over VS Code browser tabs.
- Default pattern on personal laptop: launch Google Chrome from the terminal with CDP enabled, then drive it via the DevTools protocol using a single shared agent profile directory, not the user's personal profile.
- Agents must never point CDP Chrome at the user's personal Chrome profile, and must never copy cookies or other session state out of the personal profile into an agent profile.
- Use one stable shared agent profile path for browser automation work, for example `--user-data-dir="$HOME/.agent-chrome-profile"`, so all agents converge on the same non-personal session state instead of creating ad hoc profiles. Do not use `/tmp` for the profile; reboot can clear cached sessions.
- For bot-protected government sites, assume direct `curl`/`fetch_webpage` may be blocked even when an interactive browser succeeds. Treat CDP browser context as the source of truth.
- Prefer direct, parameterized page URLs when available (for example `view=electronic`) instead of brittle click navigation.
- For protected downloads, retrieve artifacts within the browser session context (request with browser credentials) rather than unauthenticated terminal HTTP calls.
- Capture the page text, a full-page screenshot, and the source artifact download when available.
- After recovering a missing artifact, store it in the canonical local archive path immediately and verify the file content before concluding.
- Avoid opening VS Code integrated browser tabs for agent work unless the user explicitly wants a human-view-only tab. Those tabs clutter the IDE and may not expose screenshot or DOM access to the agent.
- If a VS Code browser tab was opened only for agent investigation and a CDP-capable browser is available, switch to CDP and stop adding more IDE tabs.
- **Every CDP tab must open inside your own dedicated top-level browser window** — the one whose leftmost tab is your identification page. Commands such as `tab new`, direct `open`, and `curl /json/new` silently open tabs in whichever window the browser currently considers focused, which is almost never yours. Use whatever session-aware tab-creation helper your browser setup checklist provides (e.g., `cdp_ensure_tab`). Verify the tab belongs to your window before using it.

## Inferring Intended Files

Resolve ambiguous file references before asking. Priority order:

**IDE:** explicit attachment or visible selection → active tab → dirty tabs → other open tabs → workspace search → ask user. Use the context and tools available in the current host. In Codex with JetBrains MCP, `get_all_open_file_paths` reports the active and other open editors. In Wibey, use `getDiagnostics` with scope `open-editors`. Do not assume one host's tools exist in another. If editor tools cannot resolve the reference and screenshot access is available, inspect the screen before asking; on macOS, `screencapture -x /tmp/agent_context_$$.png` captures it. Use the host's image-viewing tool and delete temporary captures afterward. A visible text selection points at that exact content.

**CLI:** use `git diff`, `git log -1`, shell history, or cwd to infer the most recently touched file.

**Name without path:** check `~/src/tools/` first, then workspace search. On work laptop also check `~/src/relationship-shared/` (symlinked as `shared`). On personal laptop also check `~/gdrive/FamilyDocuments/`.

## Dates and Times

### Always verify the current date

Before using the current date for anything, run `date "+%Y-%m-%d %H:%M %Z"`. Run once per session or whenever needed.

### Use EDTF for all dates

Use [Extended Date/Time Format](https://www.loc.gov/standards/datetime/) (EDTF) with these modifications; use canonical forms where chronological text sorting is required:

- Use **periods** as date component separators instead of hyphens (e.g. `2026.03.27` not `2026-03-27`). Periods prevent unwanted line breaks in cramped table layouts, are analogous to decimal points, save space in variable-width fonts, and cannot be confused with ranges.
- In human dates, leading year zeroes are optional; a leading `-` is mandatory for BCE. Canonical sortable dates use a fixed four-digit year.
- **Exception: filenames and directory names use hyphens** (e.g. `2026-03-27`, not `2026.03.27`). The periods rationale above (line-wrap avoidance, range disambiguation) doesn't apply to filenames; hyphens instead avoid a trailing dot ambiguous with a file extension and match the sortable `YYYY-MM-DD` convention already established across `aidocs/`, `memos/`, `releases/`, and `incidents/`. Prose dates inside those same files still use periods.
- When space allows, append day of week e.g. 2026.07.27.Mon
- When a time is included, use a compact four-digit 24-hour time, e.g. `2026.09.22.Tue.1149`; add `:ss` for seconds and `.fraction` for subsecond precision (e.g. `1112`, `1112:08`, `1112:08.23`).
- A timezone suffix is optional when context supplies it. Prefer a human-readable abbreviation such as `PT`, `PST`, or `PDT`; an unambiguous numeric UTC offset such as `-0700` is also allowed when useful.
- When a date-time is embedded in a version number, retain only the periods separating the date, day of week, and time; do not add punctuation inside the time.
- When year is not needed (e.g. when obvious from context and not needed as a search target), you may use mm.dd.Dow
- Use hyphens as range indicators instead of slashes (e.g. `2026.03.01-2026.03.27` not `2026-03-01/2026-03-27`). Slashes read like ratios or alternatives, not ranges.
- Use `yyyy<` for dates after a year and `yyyy>` for dates before a year, so the date itself remains the sortable prefix (e.g. `1900<`, `1900>`).
- Represent an unknown month or day with `X` (e.g. `1900.XX` or `1900.XX.XX`).
- Mark an approximate date by appending `c` after the date specification (e.g. `1900c`, `1900.XXc`, or `1900.05.17c`). Put `c` before a trailing `<` or `>` (e.g. `1900c<` or `1900c>`).

### Human-readable durations

Format durations as compact `NdNhNmXs`, omitting zero-valued leading units. Use a decimal part for seconds only when the total duration is under one minute; round seconds to whole numbers for durations of one minute or longer.

## Documentation

For documentation authoring, planning docs, status/task/work-log hygiene, evidence conventions, and audits, use [doc-audit](../.wibey/skills/doc-audit/SKILL.md). On the work laptop prefer the team source at `shared/.wibey/skills/doc-audit/SKILL.md`; on the personal laptop use the portable copy at `~/src/tools/.wibey/skills/doc-audit/SKILL.md`.

**Document length is not a team policy.** Do not impose, mention, or enforce an arbitrary line-count ceiling on code or documentation. Keep a file cohesive, readable, and maintainable; split it only when separation improves those qualities or the content has distinct ownership. Model selection and context budgeting do not justify splitting a coherent document.

For questions about the personal Git/repo/workspace layout, consult [GitScheme.md](GitScheme.md) first. It is the authoritative cross-laptop reference for the `home` monorepo, `~/My Drive`, `~/lpscc`, and how `~/src/tools` and the legacy `~/bin` symlink fit into that scheme. Use [GitScheme_RCA.md](GitScheme_RCA.md) for the 2026.07 recovery incident and rationale behind the current layout.

## Rules For Personal Laptop

### Family Reference Documents

For any question about family members, genealogy, life events, relationships, DNA, or the Holtz/Lusin family tree: consult `~/gdrive/FamilyDocuments/FamilyEncyclopedia.md` first. It is the authoritative human-readable reference. `~/gdrive/FamilyDocuments/Genealogy/FamilyTree.md` has the tree structure. Fall back to the GED file only for low-level GEDCOM detail not covered in either file.

## Rules For Work Laptop

### Coding Workflow

Use `/tdd` for the full TDD workflow: pull main, branch, failing tests, implement, run tests, full suite, coverage (100% new flows/conditions). In agent-toolkit repos (`shared/` symlink), see `shared/docs/WibeyAgentRef.md` § Coding Workflow (TDD). Run postman/newman if available.

#### Code Review Standards

When reviewing a PR or CRQ, apply the standards in `shared/docs/ReviewStandards.md` — these team standards are required. Audit for: coverage threshold, PROD-scope separation, logging clarity (structured fields, distinct log levels), incomplete operational safety protocols, and naming clarity for sharded resources. Never merge a PR that leaves on-call to debug via stack-trace reading or fixes a threshold without providing the fallback path.

For every work-laptop PR review, include the Wibey `pr-agent` plugin's `pr-agent-review` skill and its security-audit and dependency-scan tracks **in addition to** all existing rules and independent review. Follow `shared/docs/ReviewStandards.md` § PR Agent Review Pass when available; otherwise read the installed plugin's `SKILL.md`, reconcile its scope with the authoritative PR diff, validate findings, and report unavailable scans explicitly. Installing the plugin or requesting a review does not authorize posting, remediation, or commits to an approved PR.

#### JDK Availability on Walmart Network

**JDK 21 is installed at `/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home`** on Walmart machines via Homebrew. If a build requires JDK21 (e.g., gradle `jvmToolchain(21)`), agents should use this path and set `CODEPUPPY_JDK21` env var to it rather than attempting to download or install from external sources. Never use `brew install` directly (network-blocked); this path is already available. Check with `/usr/libexec/java_home -V` to confirm installed versions.

### PR Diff Source of Truth

When reviewing a PR or describing what a branch/PR changes relative to its base:

- Use `gh pr diff <number>` (or `gh pr view <number> --json files`) as the **sole authoritative source** — this is the merge diff GitHub shows on Files changed.
- Never use `git diff main..branch` — branches accumulate merge commits and ancestry artifacts that don't reflect the PR diff.
- Commits show *how* changes were made; the diff defines *what* the PR changes.
- If `gh pr diff` and `git diff main..branch` disagree, `gh pr diff` is authoritative.

### Git Merge Strategy

Use merge, not rebase. Rebase rewrites SHAs, turning every Jira comment, CI link, Slack message, and agent log that referenced the old SHAs into a broken pointer. The cleaner linear history isn't worth the audit trail damage.

Merge commits are honest: they record that the integration happened at that point in time, on the file states that actually existed.

### Team Tool Discovery

**Outside team repos (work laptop only):** When the current workspace has no `shared/` symlink (e.g. `~/My Drive/`, `~/Desktop/`, any personal folder), the team skills and commands are still available directly at `~/src/relationship-shared/.wibey/`. Always check there before concluding a skill or command doesn't exist.

- Team skills: `~/src/relationship-shared/.wibey/skills/<name>/SKILL.md`
- Team commands: `~/src/relationship-shared/.wibey/commands/<name>.md`

Read the command/skill file before executing it, exactly as you would for a workspace-local command.

## Portable Agent Tooling

### Codex Integration

[Codex instruction discovery](https://developers.openai.com/codex/guides/agents-md) reads global guidance from `~/.codex/AGENTS.md`, or from the directory selected by `CODEX_HOME`. A non-empty `AGENTS.override.md` at that level replaces AGENTS.md. Project instruction files are loaded from the repository root toward the working directory; later, more specific guidance takes precedence. Preserve project/team instructions rather than replacing their AGENTS.md files with this global file.

For a profile without existing global instructions, install the adapter with:

```sh
mkdir -p ~/.codex
ln -s "$HOME/src/tools/docs/AgentRules.md" "$HOME/.codex/AGENTS.md"
```

For a custom `CODEX_HOME`, use that profile's instruction path instead. Inspect an existing file, symlink, or override before changing it; the command intentionally does not force replacement. Restart Codex or start a new session to load instruction changes, then ask it to list its active instruction sources. Confirm that the IDE launcher uses the same profile; a model name such as GPT does not establish how its host loads files. These local adapters do not make the file visible to an ordinary ChatGPT chat or a remote agent; supply it through that host's supported instructions, attachment, or repository setup.

Codex's default instruction byte limit is 32 KiB. This document requires a larger budget. Set the top-level `project_doc_max_bytes = 65536` in the active profile's config.toml, preserving existing configuration, to leave room for global and project guidance. Increase it if the actual combined instructions require more; verify loading rather than inferring it from file presence. This is a loader setting, not a document-length policy.

[Codex skill discovery](https://developers.openai.com/codex/skills) supports user skills under `~/.agents/skills/` and repository skills under `.agents/skills/`. Link individual skill directories to their canonical sources under `~/src/tools/.wibey/skills/`; do not copy their contents or overwrite existing adapters. For example:

```sh
mkdir -p ~/.agents/skills
ln -s "$HOME/src/tools/.wibey/skills/doc-audit" "$HOME/.agents/skills/doc-audit"
```

Each discovered skill needs SKILL.md frontmatter with `name` and `description`. Use Codex's skill selector or an explicit `$doc-audit` mention to verify discovery; read the source directly if the current host has not registered it. Tool names and capabilities in portable workflows are intentions to map onto available Codex tools, not evidence that a Wibey/Claude-only tool is installed. Apply the same write, approval, and authentication boundaries in every host.

### Custom Commands

User-level commands source from `~/src/tools/.wibey/commands/`. When triggered, read the source file before executing. On the personal laptop, these source files should also be installed into the real home-directory adapter locations used by local agents (for example `~/.claude/commands/` and, when relevant, `~/.wibey/commands/`), rather than relying on a particular workspace such as `~/IdeaProjects/Personal`.

In Codex, these Markdown commands are readable workflows; their presence in `.wibey/commands/` does not register native slash commands. When the user invokes one by name, resolve and read its source, then execute through the available tools. Read command definitions in [the source directory](../.wibey/commands/); the [sync manifest](../walmart-sync.json) identifies mirrored and personal-only commands.

Install paths:

- Source commands: `~/src/tools/.wibey/commands/*.md`
- Wibey user commands: `~/.wibey/commands/*.md` — **must be hardlinks, not symlinks** (Wibey's extension filters with `entry.isFile()`, which returns `false` for symlinks, silently dropping them)

To install or reinstall **all** user commands as hardlinks (glob — never drifts as commands are added):

```sh
mkdir -p ~/.wibey/commands
for f in ~/src/tools/.wibey/commands/*.md; do ln -f "$f" ~/.wibey/commands/; done
```

**Work-laptop session setup:** Verify that every source command has a matching hardlink in `~/.wibey/commands/`. File existence alone does not prove a hardlink; compare device and inode:

```sh
python3 - <<'PYTHON'
from pathlib import Path
import os
source = Path.home() / 'src/tools/.wibey/commands'
adapter = Path.home() / '.wibey/commands'
for command in source.glob('*.md'):
    target = adapter / command.name
    if target.is_symlink() or not target.exists() or not os.path.samefile(command, target):
        print(f'REINSTALL: {command.name}')
PYTHON
```

If any command needs reinstalling, run the install loop and reload the IDE window.

Maintenance/debug checklist:

- If a user command is missing: run the install loop above.
- Verify hardlinks using the device-and-inode check above.
- After adding or changing files, reload the IDE window.
- Keep the source files in `~/src/tools/.wibey/commands/`; do not rename or move them.
- If discovery still fails, check YAML frontmatter: `description` must be present and valid.
- TODO: design and implement a bridge so Wibey/Claude custom skills and commands are discoverable and usable from GitHub Copilot (not just Wibey/Claude command loaders).

### Portable Skills and Mirrors

The canonical portable skill sources are in `~/src/tools/.wibey/skills/`. Codex discovery adapters are described in [Codex Integration](#codex-integration). Wibey discovers project-level skills from `<workspace>/.wibey/skills/`. The tools repo's tracked `.wibey/` directory exposes portable skills and commands when tools is open as the workspace. Team sources remain in relationship-shared; `~/.wibey/` is an untracked adapter location, not a source for personal Walmart-only skills. Keep that skill tier empty; installed command hardlinks belong there.

Mirror skill discovery metadata together with each skill body. TODO: carry the doc-audit name/description frontmatter into the team source before the next mirror sync.

The [sync manifest](../walmart-sync.json) is the source of truth for mirrored items, personal-only items, and audit exemptions. Update its `mirror_items` and `personal_only` entries when that inventory changes; do not maintain a second inventory here.

Mirrored content must contain no Walmart-proprietary material and must support personal-laptop use. Use [walmart-sync](../walmart-sync) to check or copy the mirror:

- On the personal laptop, a bare invocation checks git state, warns about dirty or unpushed changes, then pulls from origin. It is not a read-only audit.
- On the work laptop, a bare invocation audits consistency with team sources, portability, reference integrity, and personal-only item placement. Use `-v` to include passing items.
- `--sync --dry-run` previews copies from the team source. `--sync` performs them; review and commit the diff before using `--push`, which runs the portability gate before pushing.

Portability checks scan for configured internal markers; reference-integrity checks flag work-only paths that cannot resolve on the personal laptop. Passing these checks does not establish that all content is portable or nonproprietary. TODO: remove work-only signing links and path references from portable skill/command bodies at the team source, then re-mirror them; audit exemptions are defined in the manifest.
