# GitScheme.md - Repo Organization Reference

## Overview

- **Authoritative location:** `~/bin/docs/GitScheme.md` in the public `tools` repo is the cross-laptop reference for personal repo and workspace layout.
- **Current structure:** Private monorepo at `~` tracking Documents and My Drive; lpscc as standalone GitHub repo; public tools repo at `~/src/tools`
- **Workspace file**: `~/Personal.code-workspace` (local, not tracked)
- **Status**: ✅ Northstar achieved — migration complete as of 2026-07-16

**Quick links:**

- [Requirements](#requirements) — why we're doing this
- [Workspace Architecture](#workspace-architecture--north-star) — the end state (current)
- [Repo Census](#repo-census) — current state of each repo
- [Operating Rules](#operating-rules) — how to maintain it

## Requirements

- Private monorepo at `~` so GitHub-hosted Copilot sees Documents + My Drive from one repo.
- Keep LPSCC rooted at `~/lpscc` (symlink to shared-drive folder), tracked in its own standalone GitHub repo, visible as a content root and VCS root in the IDEA workspace.
- Keep the personal toolchain publicly shareable via `BrianHoltz/tools`; local checkout at `~/src/tools` with stable `~/bin` entrypoint.
- **Personal laptop only:** Mirror `~/My Drive` for redundancy — family members access these files and they warrant extra backup across devices.
- **Work laptop:** Do not mirror Google Drive. Read-only access acceptable; all real edits on personal laptop.

## Workspace Architecture (North Star)

### North Star: 1 monorepo at `$HOME`, 3 content roots, lpscc standalone

The end state (now achieved) is a single private monorepo rooted at `~`, with an aggressive allowlist `.gitignore` tracking only intended personal content. `lpscc` lives alongside as its own GitHub repo, visible in the same IDEA workspace.

Content roots and git tracking:

- `~/Documents` ← tracked in `home` monorepo
- `~/My Drive` ← tracked in `home` monorepo
- `~/lpscc` ← standalone GitHub repo (`BrianHoltz/lpscc`); NOT part of `home` monorepo

**What is `~/My Drive`:**
The most important personal files — curated documents worth extra backup and family sharing. Google Drive provides cross-device availability; the monorepo provides durable git history visible to GitHub-hosted Copilot.

The public tools repo lives at `~/src/tools/` with a stable Unix-y entrypoint via `~/bin → ~/src/tools`:

```text
~/src/tools/          public repo (BrianHoltz/tools)
  fhold               executable scripts live at repo top level
  safewrite
  walmart-sync
  docs/
  .wibey/
  shellrc/
  ...

~/bin -> ~/src/tools
```

Layout:

```
~/Personal.code-workspace   (local to laptop, not in any git repo)

Git root:
  ~                   → private monorepo git root (allowlist only)

IDEA content roots:
  ~/Documents         → content root 1 (VCS: home monorepo)
  ~/My Drive          → content root 2 (VCS: home monorepo)
  ~/lpscc             → content root 3 (VCS: standalone lpscc repo)

Nested/sibling repos:
  ~/src/tools         → public tooling repo (also an IDEA content root)
Excluded by design:
  ~/src/*             → separate public repos, outside `home` tracked scope/history

Git detection: git.autoRepositoryDetection = "subFolders"
```

This gives one GitHub-visible monorepo while local IDEs work with natural `Documents`, `My Drive`, and `lpscc` content roots — each showing their own git changes in the commit pane.

### Why Git root at `~` but IDEA roots at Documents/My Drive/lpscc

**Constraint:** IDEA prohibits using `$HOME` as a content root. It requires bounded, specific folder paths. This is by design — the home directory is too broad and contains system files, caches, and app data that should not be indexed.

**Solution:**

- **Git root: `~`** — establishes a single monorepo that GitHub-hosted Copilot sees as one unified private repo.
- **IDEA content roots: Documents, My Drive, lpscc** — three bounded folders IDEA can index efficiently.
- **IDEA VCS roots: `~`, Documents, My Drive, wiki, lpscc** — all five mapped so all changes surface in the commit pane.

### Why LPSCC is separate

**Design decision:** `~/lpscc` is intentionally **NOT** part of the `home` monorepo.

- `~/lpscc` is a symlink to `~/Library/CloudStorage/GoogleDrive-<account>/Shared drives/LP SCC Financial`
- If tracked in monorepo, git would store paths using the long target, not the symlink alias
- Shared-drive content belongs on Google Drive; GitHub tracks it via a standalone `BrianHoltz/lpscc` repo
- Shared-drive permissions and collaborative model differ from private-laptop files

**Result:**
- IDEA content root: `~/lpscc` ✅
- IDEA VCS root: `~/lpscc` ✅ (mapped in `.idea/vcs.xml`)
- Git remote: standalone `BrianHoltz/lpscc` repo
- Home monorepo: NOT included

### Public tooling repo structure

The public tools repo lives in `~/src/tools/`. Its stable entrypoint is `~/bin -> ~/src/tools`.

Other public repos in `~/src/*` are standalone project repos outside the `home` repo's tracked scope.

**Default rule for new public repos:** put them in `~/src/<name>`.

## Repo Census

Current state (2026-07-16, post-recovery, Northstar achieved):

| Repo              | Working tree                            | Git dir              | Remote                      | Status                                           |
| ----------------- | --------------------------------------- | -------------------- | --------------------------- | ------------------------------------------------ |
| `home` (monorepo) | `~`                                     | in-tree              | `BrianHoltz/home` private   | ✅ active; Documents + My Drive + wiki history   |
| `lpscc`           | `~/lpscc` (symlink)                     | in-tree              | `BrianHoltz/lpscc` private  | ✅ standalone repo; VCS root in IDEA workspace   |
| `tools` (public)  | `~/src/tools`                           | in-tree              | `BrianHoltz/tools` public   | ✅ active at `~/src/tools`; `~/bin` symlink      |
| `wiki` (nested)   | `~/Documents/HoltzDotOrg/Thoughts/wiki` | `~/gitdirs/wiki.git` | `BrianHoltz/wiki` public    | ✅ history imported into monorepo; still active  |
| `gdrive` (legacy) | —                                       | `~/gitdirs/gdrive`   | `BrianHoltz/gdrive` private | ⏳ archive after 2026-07-30 grace period         |

### IDE Setup

IDE project at `~/IdeaProjects/Personal/`:

**Content roots:**
- Documents, My Drive, `~/src/tools`, lpscc (four bounded modules for IDE visibility)

**Version control roots (`.idea/vcs.xml`):**
- `~` (home monorepo root)
- `~/Documents`
- `~/My Drive`
- `~/Documents/HoltzDotOrg/Thoughts/wiki`
- `~/src/tools` ← standalone public repo; surfaces tools changes in commit pane
- `~/lpscc` ← standalone repo; surfaces lpscc changes in commit pane

**First-class indexing requirement:**
Every content root listed above must be loaded as an IDEA module and indexed as a first-class citizen. Files outside loaded content roots will not appear in IDEA's **Find Files**, navigation, or Copilot context. If a file (e.g. `GitScheme.md`) is missing from Find Files, verify its real directory is a loaded content root and is not excluded.

**No overlapping exclusions:**
A module that owns a parent directory must not exclude a path that is another module's content root. For example, if `src.iml` claims `~/src` and excludes `~/src/tools`, while `tools.iml` claims `~/src/tools` as its own content root, IDEA will not index `~/src/tools`. Exclusions must be scoped so they do not hide sibling module roots.

**`~/bin` is not a content root or git repo:**
`~/bin` is a legacy symlink to `~/src/tools` retained only for `$PATH` and scripts that expect executables at `~/bin/`. It must never be used as an IDEA content root, VCS root, or git working tree. All IDE indexing and git operations must use the real path `~/src/tools`.

**Workspace-local files:**
- `.github/` at `~/IdeaProjects/Personal/` are adapters only
- Canonical agent machinery belongs in `BrianHoltz/tools` repo
- Attach the real repo path `~/src/tools` as the IDEA content root and VCS root; do not rely on the `~/bin` symlink for IDE root configuration.

## Operating Rules

- Always push every repo to GitHub (no local-only history).
- `~/My Drive` is the primary source of truth for those files (managed by Google Drive); GitHub tracks them as selective backup for Copilot visibility.
- `~/Documents` is the primary source; GitHub is the durable backup and publication mechanism.
- `~/lpscc` changes commit and push to `BrianHoltz/lpscc`, not to `home`.
- **CRITICAL:** Google Drive sync is NOT a backup mechanism. Files deleted from disk are deleted from Google Drive automatically. Keep important files in git.

## Google Docs access plan

For agent access to Google Docs content, prefer a real OAuth flow first and use browser-auth/CDP as the fallback.

1. **Primary path:** create a Google Cloud Desktop OAuth client, enable Google Drive API and Google Docs API, and keep the downloaded client JSON in a user-local location that is not committed.
2. **Token handling:** let local tooling exchange that client JSON for refreshable user tokens stored outside git, then export/read docs by id.
3. **Fallback path:** when OAuth is not yet wired up, launch Google Chrome with `--remote-debugging-port` and a dedicated shared agent profile (for example `/tmp/agent-chrome-profile`), then have the human user sign in there.
4. **Security posture:** never point agent automation at the user's personal Chrome profile and never copy cookies out of that profile into agent tooling.
5. **Operational rule:** if a `.gdoc` stub is present but the content is needed, agents should first try OAuth export, then fall back to the dedicated CDP browser session.

## Recovery: July 2026 Data Loss Incident

**Summary:** On July 11, 2026, Copilot deleted 102 files from `My Drive/` (family documents). Google Drive sync propagated deletions to cloud. All 102 files were recovered from git history on 2026-07-16.

**Details:** See `GitScheme_RCA.md` for full technical analysis, timeline, and lessons learned.

**Backup:** Tarball at `~/tmp/gdrive.20260715.tar` (6.7G, 5,257 files) — retain until 2026-07-30.
