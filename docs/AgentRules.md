# AgentRules.md - Global AI Agent Rules

Personal global rules for the user. The rules in this file apply to all repos, all AI models, all hosts. Any project-specific or model-specific AI rules override them only where they explicitly conflict.

**AgentRules.md vs AGENTS.md:** These are two different layers of agent instruction:

- **AgentRules.md** (this file) — global, cross-laptop, cross-repo, cross-model. Personal rules that always apply. Lives in `~/bin/`, synced to both laptops via git. Not team-visible; not project-specific.
- **AGENTS.md** — project/team-level supplement. Lives at the repo root (or symlinked from the team's shared repo). Adds team context: domain terminology, shared tooling, team workflows, file layout conventions. Supplements this file; does not override it.

When both apply, read both. If they conflict, AgentRules.md loses to AGENTS.md only where AGENTS.md explicitly says so. AGENTS.md can safely skip any rule already in AgentRules.md — agents will have both in context.

## Table of Contents

- [The Seven Commandments](#the-seven-commandments)
- [~/bin/ structure](#bin-structure)
  - [~/bin/ vs relationship-shared/](#bin-vs-relationship-shared)
- [Write Rules](#write-rules)
  - [Inode preservation](#inode-preservation)
  - [safewrite CAS pattern](#safewrite-cas-pattern)
  - [Other file operation rules](#other-file-operation-rules)
- [Communication Style](#communication-style)
- [Browser Automation](#browser-automation)
- [Inferring Intended Files](#inferring-intended-files)
- [Dates and Times](#dates-and-times)
  - [Always verify the current date](#always-verify-the-current-date)
  - [Use EDTF for all dates](#use-edtf-for-all-dates)
- [Documentation](#documentation)
- [Rules For Personal Laptop](#rules-for-personal-laptop)
  - [Family Reference Documents](#family-reference-documents)
- [Rules For Work Laptop](#rules-for-work-laptop)
  - [Coding Workflow](#coding-workflow)
  - [PR Diff Source of Truth](#pr-diff-source-of-truth)
  - [Git Merge Strategy](#git-merge-strategy)
  - [Custom Commands](#custom-commands)
  - [Wibey Skills — ~/bin/.wibey/ Directory](#wibey-skills----binwibey-directory)
    - [Project-Level Commands](#project-level-commands)

## The Seven Commandments

1. **Don't Ramble**: From sections to words, cut or condense until meaning changes.
2. **Don't Repeat**: This is so important that I'm self-consciously repeating it. Cut everything that performs helpfulness without delivering it, or completeness without informing. If what you're writing already exists elsewhere, then omit it or link it, don't repeat it.
3. **Don't Clobber**: Every file write must follow the [Write Rules](#write-rules).
4. **Don't Quit**: Do not give up on the best tool for the job: if it is missing or broken or needs auth, invest in getting it to work, and fallback only when repair fails and user is unresponsive, and state the fallback + reason.
5. **Don't Spam**: Ask permission before communicating with other humans, e.g. via Slack, Jira, email, or Github comments/approvals. But just use normal caution when doing other git or Confluence operations. And don't spam in docs reminding agents what the rules are.
6. **Don't Count**: Never label things sequentially, e.g. with numbers or letters. It's opaque and brittle and lazy. Use names. Exceptions may be granted for sequences that are long or immutable.
7. **Don't Narrate**: Except in designated sections (e.g. work logs), documents should not narrate their history or be self-conscious of previous versions. Omit apologetic or performative text. Documents are timeless; all that matters is whether the text helps the reader.

## ~/bin structure

The canonical source of this file is `~/bin/docs/AgentRules.md`, version-controlled in the public tools repo (`github.com/BrianHoltz/tools`) checked out at `~/src/tools` and exposed locally at `~/bin`. **The `tools` repo is the cross-laptop sync mechanism, and `~/bin` is the stable local entrypoint** — push on work laptop, pull on personal laptop. The following paths are symlinks to this file:

- `~/.claude/CLAUDE.md` — read by Claude Code CLI (and Wibey at Walmart)
- `~/.cursor/cursorrules` — read by Cursor
- `~/.code_puppy/AGENTS.md` — read by Code Puppy. Code Puppy has no single CLAUDE.md-style entrypoint; it concatenates three AGENTS.md layers into every session's system prompt — global (`~/.code_puppy/AGENTS.md`, this file), project (`<CWD>/.code_puppy/AGENTS.md`), and repo-root fallback (`./AGENTS.md`) — so this symlink is what makes AgentRules.md load automatically, every session, every repo, with no action needed from the user or the agent. If the user references "the Commandments", "AgentRules", or anything from this file, it is already in context via this path — never say you can't find it or ask where it lives.
- `.github/copilot-instructions.md` symlink in each repo root — read by GitHub Copilot (VS Code). GitHub Copilot does NOT read `~/.claude/CLAUDE.md`; it only reads this file from the open repo root.

**Canonical-vs-adapter rule:** personal agent machinery lives canonically in the `tools` repo at `~/src/tools/`, exposed locally at `~/bin/`. Home-directory special folders such as `~/.claude/commands/`, `~/.claude/CLAUDE.md`, `~/.cursor/cursorrules`, and `~/.wibey/commands/` are adapter/install locations. Workspace-local `.github/` trees are also adapters for GitHub Copilot. Do **not** treat `~/IdeaProjects/Personal/.github/skills/` or any other workspace-local `.github/skills/` directory as a primary source of truth.

Other `~/bin/` files symlinked into `~/`:

- `~/.shellrc.common` → `~/bin/shellrc/shellrc.common` — shared PATH/env for zsh + bash
- `~/.zprofile` → `~/bin/shellrc/zprofile` — zsh login shell config
- `~/.zshrc` → `~/bin/shellrc/zshrc` — zsh interactive shell config
- `~/.bash_profile` → `~/bin/shellrc/bash_profile` — bash login/interactive shell config
- `~/.bashrc` → `~/bin/shellrc/bashrc` — bash interactive shell config

Canonical personal path aliases in `~/`:

- `~/gdrive` → `~/Google Drive` — preferred short path for the Google Drive mount
- `~/lpscc` → `~/Google Drive/Shared drives/LP SCC Financial` — preferred short path for LP SCC Financial

Use these aliases in local tool/IDE config when possible to avoid space-heavy paths and keep paths consistent across settings.
For workspace roots, attach `~/lpscc` itself; do **not** attach `~/My Drive/Libertarian/LPSCC` directly.

The `~/bin/` repo also contains personal tool settings and reference docs (not symlinked):

- `~/bin/docs/Tools.md` — IDE/editor comparison matrix, extension patches, keybinding customizations, and tool-specific configuration notes

To update the above files, edit the `~/bin/` copies and commit in the `~/bin/` repo.

### ~/bin/ vs relationship-shared/

Two completely separate repos serve different scopes:


|                           | `~/bin/`                                     | `relationship-shared/`       |
| ------------------------- | -------------------------------------------- | ---------------------------- |
| Git host                  | GitHub (personal, public)                    | Walmart GHE (team, internal) |
| Available on              | both laptops                                 | work laptop only             |
| Contains                  | personal tools, rules, cross-platform skills | team skills, docs, commands  |
| Access on personal laptop | always (`git pull`)                          | never (no VPN/auth)          |

**Skills by laptop:**

- **Work laptop**: team skills from `shared/.wibey/skills/` (relationship-shared); personal skills from `~/bin/.wibey/skills/`. The Wibey VS Code extension is Walmart-internal and only present on the work laptop, never on the personal laptop.
- **Personal laptop**: only `~/bin/.wibey/skills/`, exposed per-workspace via `.wibey/skills/` symlinks. The Wibey extension is not available or expected here.

Skills useful on both laptops live canonically in relationship-shared (team owns them) and are manually copied to `~/bin/.wibey/skills/` + committed when updated.

**When resolving a skill on personal laptop**: look in `~/bin/.wibey/skills/<name>/SKILL.md`. Do not attempt to read `shared/` — the symlink doesn't exist. Do not expect the Wibey extension to be present.

**When resolving a skill on work laptop**: check `shared/.wibey/skills/` first (team version may be newer than `~/bin/` copy). The Wibey extension is available and should be used if needed.

## Write Rules

**Write as you go.** After each logical unit of work, write immediately — don't accumulate. Sessions die without warning; unwritten work is lost.

**Re-read immediately before each write.** The file may have changed. In permit mode, `safewrite` exit 3 enforces this. In reviewed mode, re-read right before each Edit/Write call.

**Don't revert ambiguous changes.** If you encounter a change in a doc or file and there is a non-trivial chance it was the user's deliberate choice, do not revert it — full stop. This applies even if the change looks wrong, inconsistent, out of place, or contrary to what you were about to write yourself. Default assumption for any small change of unknown origin: the human user made it deliberately and considers it important. Investigate or ask before undoing it; never silently revert or overwrite it back to the prior state.

Three rules for how to write:

Files requiring the fhold protocol (expand this list as the protocol matures):

- Git-tracked markdown files (`*.md`)

**Path rule:** Always call `fhold` and `safewrite` via full path (`~/bin/fhold`, `~/bin/safewrite`). Agent subshells (Bash tool, spawned agents) may run in a non-login shell that does not inherit the interactive `PATH`, causing bare commands to fail with "not found" even when `~/bin/` is in the user's interactive PATH.

**Rule 1 — Files in the list above:** use `fhold` to coordinate, then write.

- Before every write: `~/bin/fhold status FILE`
- **Reviewed mode** (default — no permit holds): `~/bin/fhold review register FILE --agent $AGENT` (exit 0 → proceed; exit 2 → show user the MENU from `~/bin/fhold -H` and wait for their choice). Write with an **inode-preserving method** (IDE Edit/Write tools, vim). The IDE shows your changes as a diff for user review. `~/bin/fhold review release FILE` when you know you're done, or just let 30min TTL lapse.
- **Permit mode** (any permit holds exist): `~/bin/fhold permit register FILE --agent $AGENT` if not already registered. Write with **`~/bin/safewrite`**. `~/bin/fhold permit release FILE --agent $AGENT` when you know you're done, or just let the 30min TTL lapse.
- **IDE diff in permit mode = violation.** If an Accept/Reject diff button appears while you're in permit mode, you used Edit/Write tools when you should have used `safewrite`. That write will race with other agents working on the file.

**Rule 2 — All other files:** use inode-preserving Edit/Write tools. IDE diff shows your changes; observer buffers stay live. No fhold needed because these other files are not expected to get concurrent edits.

**Rule 3 — Write directly** (exceptions to Rules 1–2):

- Agent-owned ephemeral temp files
- Newly-created files of any type — nothing exists yet to race against

### Inode preservation

Never update a file by creating a new one in its place. `sed -i ''` on macOS, `mv tmpfile original`, and `echo > file` all change the inode. File watchers (e.g. Typedown) watch the original inode and go blind after the swap. Safe methods: `safewrite` (truncate+rewrite), IDE Edit/Write tools, vim. In Python: `open(path, 'w').write(content)`.

**Symlinks:** Before using Write on any file, check whether it is a symlink (`ls -la`). The Write tool may sever the symlink by creating a new regular file at the path rather than writing through to the target. Use Edit instead — Edit patches the existing bytes and preserves the symlink. If you must use Write (e.g. full-file rewrite), do it from the directory where the file is real, not from the symlinked path.

### safewrite CAS pattern

```sh
HASH=$(shasum -a 256 FILE | awk '{print $1}')
python3 my_transform.py > /tmp/new_out
~/bin/safewrite FILE \
  --from /tmp/new_out \
  --expect-sha256 "$HASH" \
  --max-shrink-pct 20 \
  --sentinel-regex "^# " \
  --note "agent=claude, task=abc123"
# If output looks truncated or wrong, inspect /tmp/new_out before retrying.
```

On exit 3 (CAS mismatch): file changed since you read it. Re-read, rebuild from new state, retry. Never reuse stale content.

Run `~/bin/safewrite -h` for full options. Run `~/bin/fhold -h` for the fhold MENU and full protocol.

### Other file operation rules

- Never `rm` directly on user files — use `trash` or `mv ~/.Trash/`. **Exception: `/tmp/` and `tmp/` may be deleted with plain `rm` — no `trash`, no confirmation, no hesitation (see [Seven Commandments](#the-seven-commandments)).**
- Duplicate/conflicting files: ASK which to keep before deleting either
- No VCS changes unless you're certain the user wants them
- Commit granularity: independent changes → separate commits; interdependent → one commit
- **Two-tier commit policy**: mechanical changes (artifacts, formatting) → commit directly; substantive changes (logic, data, content) → `git add` and summarize for user review. User can override with "just commit it".
- **Commit message provenance**: Every commit made by an agent must include a provenance trailer block at the end, one line per fact that is actually available in the current session — omit any line whose fact can't be determined, don't guess or invent a value:
  - `Model: <name>-<version>` (e.g. `Model: claude-sonnet-5`) — always required. Use the resolved model identifier (check the agent's model registry/config, e.g. `~/.code_puppy/models.json`, for what a configured alias like `claude-5-sonnet` actually resolves to) — don't guess a plausible-sounding name.
  - `Harness: <name> <version>` (e.g. `Harness: code-puppy 0.1.57`, `Harness: wibey <version>`) — the agent runtime/CLI, if its version is discoverable (installed package version, `--version` flag, or config file).
  - `IDE: <name> <version>` (e.g. `IDE: IntelliJ IDEA 2026.2`, `IDE: VS Code`, `IDE: Code Puppy Desktop`) — the editor/IDE the session is running inside, if detectable (e.g. via environment variables, running process inspection, or app bundle metadata). Version is a bonus, not required, if the IDE doesn't expose one easily.
  - This makes agent provenance auditable in `git log`: which model, which harness, which IDE produced a given change.

## Communication Style

- **Getting the user's attention:** use the `ailerts` skill (if available) when blocked and the user has likely switched away. Not for routine status — only when stopped and user likely doesn't know.
- **No horizontal scrolling in chat.** Never use tables, wide code fences, or any other element that causes horizontal scroll in the conversation pane. Use prose, bullet lists, or definition-style (`**term** — explanation`) instead. Sole exception: code or preformatted text that must be quoted verbatim and cannot reasonably be reformatted.
- **Links beat font effects.** Never apply code formatting, bold, italics, or other font effects to text that could instead be a hyperlink. If text is linkable, make it a link — font effects are for semantic/syntactic markup only. When both apply (e.g. a channel name that is also code), the link wins. Remove bare IDs (commit hashes, Slack channel codes, UUIDs) from visible text; they belong only inside URLs.

## Browser Automation

- When an agent needs to inspect a live page, take screenshots, or read DOM content, prefer a terminal-launched Chrome with `--remote-debugging-port` (CDP) over VS Code browser tabs.
- Default pattern on personal laptop: launch Google Chrome from the terminal with CDP enabled, then drive it via the DevTools protocol using a single shared agent profile directory, not the user's personal profile.
- Agents must NEVER point CDP Chrome at the user's personal Chrome profile, and must NEVER copy cookies or other session state out of the personal profile into an agent profile.
- Use one stable shared agent profile path for browser automation work, for example `--user-data-dir=/tmp/agent-chrome-profile`, so all agents converge on the same non-personal session state instead of creating ad hoc profiles.
- For bot-protected government sites, assume direct `curl`/`fetch_webpage` may be blocked even when an interactive browser succeeds. Treat CDP browser context as the source of truth.
- Prefer direct, parameterized page URLs when available (for example `view=electronic`) instead of brittle click navigation.
- For protected downloads, retrieve artifacts within the browser session context (request with browser credentials) rather than unauthenticated terminal HTTP calls.
- Capture evidence in a reusable triad: 1) page text extract, 2) full-page screenshot, 3) source artifact download when available.
- After recovering a missing artifact, store it in the canonical local archive path immediately and verify the file content before concluding.
- Avoid opening VS Code integrated browser tabs for agent work unless the user explicitly wants a human-view-only tab. Those tabs clutter the IDE and may not expose screenshot or DOM access to the agent.
- If a VS Code browser tab was opened only for agent investigation and a CDP-capable browser is available, switch to CDP and stop adding more IDE tabs.

## Inferring Intended Files

Resolve ambiguous file references before asking. Priority order:

**IDE (Wibey):** active tab → dirty tabs → other open tabs → workspace search → ask user. Use `getDiagnostics` scope `open-editors`. Active tab = strongest signal; dirty tab = recently edited. If `getDiagnostics` fails to identify the active file, take a macOS screenshot: `screencapture -x /tmp/wibey_ctx_$$.png && sips -Z 1800 /tmp/wibey_ctx_$$.png --out /tmp/wibey_ctx_small_$$.png`, read it with the Read tool to see what's on screen, then delete both files. Never ask the user which file before trying this. When reading the screenshot, also note any visible text selection (highlighted text in the editor) — a selection is the strongest possible signal about what the user is focused on and should be treated as the user pointing at that exact content.

**CLI:** use `git diff`, `git log -1`, shell history, or cwd to infer the most recently touched file.

**Name without path:** check `~/bin/` first, then workspace search. On work laptop also check `~/src/relationship-shared/` (symlinked as `shared`). On personal laptop also check `~/Documents/Google Drive/FamilyDocuments/`.

## Dates and Times

### Always verify the current date

Before using the current date for anything, run `date "+%Y-%m-%d %H:%M %Z"`. Run once per session or whenever needed.

### Use EDTF for all dates

With these modifications:

- Use **periods** as date component separators instead of hyphens (e.g. `2026.03.27` not `2026-03-27`). Periods prevent unwanted line breaks in cramped table layouts, are analogous to decimal points, save space in variable-width fonts, and cannot be confused with ranges.
- When space allows, append day of week e.g. 2026.07.27.Mon
- When year serves no purpose (e.g. grep'ing), you may use 07.27.Mon
- Use hyphens as range indicators instead of slashes (e.g. `2026.03.01-2026.03.27` not `2026-03-01/2026-03-27`). Slashes read like ratios or alternatives, not ranges.
- Use &gt;yyyy or &lt;yyyy instead of aft/bef if space is tight or you want to prevent line wraps in Markdown prose. Use >yyyy and <yyyy in data values.

## Documentation

For documentation authoring, planning docs, status/task/work-log hygiene, evidence conventions, and doc audits, use the doc-audit skill as the shared reference. On the work laptop, it is at `shared/.wibey/skills/doc-audit/SKILL.md` (team repo). It is **not** in `~/bin/.wibey/` because it contains Walmart-internal URLs (gecgithub01, Jira keys, service names) that would be exposed in a public GitHub push.

For questions about the personal Git/repo/workspace layout, consult `~/bin/docs/GitScheme.md` first. It is the authoritative cross-laptop reference for the `home` monorepo, `~/My Drive`, `~/lpscc`, and how `~/src/tools` plus the `~/bin` symlink fit into that scheme. Use `~/bin/docs/GitScheme_RCA.md` for the 2026.07 recovery incident and rationale behind the current layout.

## Rules For Personal Laptop

### Family Reference Documents

For any question about family members, genealogy, life events, relationships, DNA, or the Holtz/Lusin family tree: consult `~/Documents/Google Drive/FamilyDocuments/FamilyEncyclopedia.md` first. It is the authoritative human-readable reference. `FamilyDocuments/Genealogy/FamilyTree.md` has the tree structure. Fall back to the GED file only for low-level GEDCOM detail not covered in either file.

## Rules For Work Laptop

### Coding Workflow

Use `/tdd` for the full TDD workflow: pull main, branch, failing tests, implement, run tests, full suite, coverage (100% new flows/conditions). In agent-toolkit repos (`shared/` symlink), see `shared/docs/WibeyAgentRef.md` § Coding Workflow (TDD). Run postman/newman if available.

### PR Diff Source of Truth

When reviewing a PR or describing what a branch/PR changes relative to its base:

- Use `gh pr diff <number>` (or `gh pr view <number> --json files`) as the **sole authoritative source** — this is the merge diff GitHub shows on "Files changed".
- **Never** use `git diff main..branch` — branches accumulate merge commits and ancestry artifacts that don't reflect the PR diff.
- Commits show *how* changes were made; the diff defines *what* the PR changes.
- If `gh pr diff` and `git diff main..branch` disagree, `gh pr diff` is correct. Period.

### Git Merge Strategy

Use merge, not rebase. Rebase rewrites SHAs, turning every Jira comment, CI link, Slack message, and agent log that referenced the old SHAs into a broken pointer. The cleaner linear history isn't worth the audit trail damage.

Merge commits are honest: they record that the integration happened at that point in time, on the file states that actually existed.

### Custom Commands

User-level commands source from `~/bin/.wibey/commands/`. When triggered, read the source file before executing. On the personal laptop, these source files should also be installed into the real home-directory adapter locations used by local agents (for example `~/.claude/commands/` and, when relevant, `~/.wibey/commands/`), rather than relying on a particular workspace such as `~/IdeaProjects/Personal`.

User-level commands (available in all workspaces via hardlinks to `~/.wibey/commands/`):

- **commitz** — cluster diffs into commit buckets
- **continue** — checkpoint and resume: write work log, commit, keep working *(mirrored from relationship-shared)*
- **convo** — park conversation with visible title for Mission Control
- **plando** — structured plan-and-execute workflow *(mirrored from relationship-shared)*
- **say** — text-to-speech output
- **tdd** — TDD workflow enforcer: branch, baseline, red, green, verify, coverage *(mirrored from relationship-shared)*

Install paths:

- Source commands: `~/bin/.wibey/commands/*.md`
- Wibey user commands: `~/.wibey/commands/*.md` — **must be hardlinks, not symlinks** (Wibey's extension filters with `entry.isFile()`, which returns `false` for symlinks, silently dropping them)

To install or reinstall **all** user commands as hardlinks (glob — never drifts as commands are added):

```sh
mkdir -p ~/.wibey/commands
for f in ~/bin/.wibey/commands/*.md; do ln -f "$f" ~/.wibey/commands/; done
```

**Agent workspace setup check (work laptop, run at session start):** Verify every command in `~/bin/.wibey/commands/` has a corresponding hardlink in `~/.wibey/commands/`. If any are missing, run the loop above and reload the IDE window.

```sh
# Quick check: list missing
for f in ~/bin/.wibey/commands/*.md; do
  name=$(basename "$f")
  [ -f ~/.wibey/commands/"$name" ] || echo "MISSING: $name"
done
```

Maintenance/debug checklist:

- If a user command is missing: run the install loop above.
- Verify hardlinks (not symlinks): `node -e "const fs=require('fs'); fs.readdirSync(process.env.HOME+'/.wibey/commands',{withFileTypes:true}).forEach(e=>console.log(e.name,'isFile:',e.isFile(),'isSymlink:',e.isSymbolicLink()))"`
- After adding or changing files, reload the IDE window.
- Keep the source files in `~/bin/.wibey/commands/`; do not rename or move them.
- If discovery still fails, check YAML frontmatter: `description` must be present and valid.
- TODO: design and implement a bridge so Wibey/Claude custom skills and commands are discoverable and usable from GitHub Copilot (not just Wibey/Claude command loaders).

**Outside team repos (work laptop only):** When the current workspace has no `shared/` symlink (e.g. `~/My Drive/`, `~/Desktop/`, any personal folder), the team skills and commands are still available directly at `~/src/relationship-shared/.wibey/`. Always check there before concluding a skill or command doesn't exist.

- Team skills: `~/src/relationship-shared/.wibey/skills/<name>/SKILL.md`
- Team commands: `~/src/relationship-shared/.wibey/commands/<name>.md`

Read the command/skill file before executing it, exactly as you would for a workspace-local command.

### Wibey Skills — ~/bin/.wibey/ Directory

Wibey discovers project-level skills from `<workspace>/.wibey/skills/`. The `~/bin/` repo ships its own `.wibey/` directory (git-tracked real directory, not a symlink) so that opening `~/bin/` in a Wibey IDE exposes a curated set of portable skills and commands.

**Three-tier taxonomy:**


| Tier                       | Location                                              | Tracked       | Available on                  |
| -------------------------- | ----------------------------------------------------- | ------------- | ----------------------------- |
| 1 — Team                  | `relationship-shared/.wibey/` (via `shared/` symlink) | Walmart GHE   | Work laptop, team repos       |
| 2 — Portable              | `~/bin/.wibey/`                                       | Public GitHub | Both laptops                  |
| 3 — Personal Walmart-only | `~/.wibey/`                                           | Untracked     | Work laptop only (keep empty) |

**`~/bin/.wibey/` directory layout:**

```
.wibey/
  skills/
    ailert/          SKILL.md + assets/  — mirrored from relationship-shared
    clipboard-read/  SKILL.md            — mirrored
    converge/        SKILL.md            — mirrored
    doc-audit/       SKILL.md            — mirrored
    ftm/             SKILL.md            — personal-only (Family Tree Maker integration)
  commands/
    avoid-numbering.md — personal-only (admonish agent to scrub sequential labels)
    commitz.md       — personal-only (cluster diffs into commit buckets)
    convo.md         — personal-only (park conversation for Mission Control)
    say.md           — personal-only (text-to-speech output)
    continue.md      — mirrored from relationship-shared
    plando.md        — mirrored
    tdd.md           — mirrored
  docs/
    AnchorDoc.md                         — mirrored from relationship-shared
    StatusVocabulary.md                  — mirrored from relationship-shared
    IncidentRCA.md                       — mirrored
    templates/
      Project.md                         — mirrored
      Incident.md                        — mirrored
  hooks/             (empty)
```

**Mirror-safe convention:** Skills, commands, and docs in relationship-shared that are mirror-safe contain no Walmart-proprietary content and are designed for personal-laptop use. Use `~/bin/walmart-sync` to audit and sync the mirror.

**Checking mirror state** — behaviour depends on laptop:

- **Personal laptop** (shared absent): `~/bin/walmart-sync` checks git state (warns on dirty tree or unpushed commits) then pulls from origin.
- **Work laptop** (shared present): `~/bin/walmart-sync` runs the full three-check audit.

**Sync workflow (work laptop only) — three steps:**

```sh
~/bin/walmart-sync --sync          # copy drifted items from shared to bin
cd ~/bin && git add -p && git commit  # review and commit manually
~/bin/walmart-sync --push          # portability gate, then push to origin
```

Other useful invocations:

```sh
~/bin/walmart-sync          # full audit (work) or pull (personal)
~/bin/walmart-sync -v       # full audit, also show passing items
~/bin/walmart-sync --sync --dry-run  # preview what would be synced
```

Three checks that `walmart-sync --` audit runs:

- **Consistency** — byte-diff bin copies vs relationship-shared originals. Work laptop only.
- **Portability** — grep for Walmart-internal markers (`gecgithub01`, internal hostnames, Jira keys) that must not appear in the public `~/bin/` GitHub repo.
- **Ref-integrity** — flag references to paths/skills that dangle on personal laptop (`~/src/relationship-shared`, `shared/` symlink).

**Known pre-existing portability issues:** The SKILL.md files for `ailert`, `clipboard-read`, and `converge`, and the commands `continue`, `plando`, `tdd` all contain GHE provenance links (`gecgithub01.walmart.com`) and `relationship-shared` text references — these shipped with the initial mirror and are already committed to the public repo. To clean them up, strip the provenance block from each file in relationship-shared before re-mirroring, or patch them locally after sync.

**When AgentRules.md mirror lists change**, update the `mirror_items` and `personal_only` arrays in `~/bin/walmart-sync.json` to match — the policy manifest; `~/bin/walmart-sync` itself is a thin orchestrator with no embedded lists.

Currently mirror-safe skills: `ailert` (with `assets/`), `clipboard-read`, `converge`, `doc-audit`.
Currently mirror-safe commands: `continue`, `plando`, `tdd`.
Currently mirror-safe docs: `AnchorDoc.md`, `StatusVocabulary.md`, `IncidentRCA.md`, `templates/Project.md`, `templates/Incident.md`.

### Project-Level Commands

In teams using the agent-toolkit shared repo pattern, commands live at `<workspace>/shared/.wibey/commands/` and are consistent across all repos via the `shared/` symlink:

- **plando** — Structured plan-and-execute workflow with aidocs task record.
- **tdd** — TDD workflow enforcer: branch, baseline, red, green, verify, full suite, newman, coverage.
- **continue** — Checkpoint and resume: write work log, commit, then keep working.
