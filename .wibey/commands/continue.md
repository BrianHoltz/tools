---
name: continue
description: Checkpoint state into the active doc, then continue working. Commit, update work log, overwrite active work, append pending investigations, optionally compact.
---

> [!NOTE]
> **Mirror-safe command.** This file contains no Walmart-proprietary content and is
> designed to be manually mirrored to personal laptops. The canonical copy lives in
> [`relationship-shared/.wibey/commands/`](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared).
> **If you are reading this outside of Walmart GHE, do not edit it here** — make
> changes in relationship-shared and re-sync.

# Continue — Checkpoint and Resume

Distill current state into the active doc, commit it, call `/convo`, then keep working. Default behavior: **write → commit → /convo → continue**. Pass `--compact` to run `/compact` after committing. Pass `--no-commit` to update the doc without committing (e.g. mid-task snapshot).

An optional steering prompt can be appended: `/continue [optional prompt]`. If a prompt is provided, incorporate it into the doc before committing — append new subtasks to Active Work, reprioritize if the prompt implies urgency, note any ambiguity in Pending Investigations — then continue with the merged plan.

## Steps (execute in order — do not skip any step)

**1. Find the anchor doc.**

Run the Find Existing Anchor Doc protocol from `AnchorDoc.md §Find` (steps F1–F4).
(Path: `shared/docs/AnchorDoc.md` → `~/bin/.wibey/docs/AnchorDoc.md` →
[GitHub](https://github.com/BrianHoltz/tools/blob/main/.wibey/docs/AnchorDoc.md).)
If no doc is found: create `aidocs/yyyy-mm-dd/hhmm_CamelCase.md` (use `shared/aidocs/…`
if a `shared/` symlink exists), seed it with `## Summary`, `## Work Log`,
`## Active Work`, and `## Pending Investigations` sections, populate with current state,
then proceed.

**2. Write the doc.** Update (or create) the following sections:

- **`## Work Log`** — *append* a new timestamped entry (ISO datetime, local timezone). 1–3 sentences: what was done, what was found, what changed. Do not edit previous entries.
- **`## Active Work`** — *overwrite entirely*. Current state plus what comes next: one sentence on what was just being done, then an ordered list of immediate next subtasks specific enough that a fresh agent with no prior context can resume without asking the user. If a steering prompt was provided, integrate it here — append new tasks or reprioritize as appropriate. If stopping, note "Handoff" and list pickup steps.
- **`## Pending Investigations`** — *append* any new unresolved questions or blockers, including ambiguity from a steering prompt. Mark resolved items with ~~strikethrough~~ and a resolution note.

**Quality gate:** Could a fresh agent reading only this doc resume without asking the user anything? If no, add what's missing before proceeding.

**3. Commit (unless `--no-commit` was passed).**

Per AGENTS.md commit rules, commit from within `shared/`. Message: `docs: /continue checkpoint — <one-line summary of Active Work>`.

**4. Call `/convo` with the task title.**

Derive a short title (≤6 words) from the Active Work summary and call `/convo <title>`. This updates the conversation name in Mission Control so the user can see that state is committed and safe — and marks the natural window to steer before the agent resumes.

**5. Compact (only if `--compact` was passed, or context is >80% full and you judge it necessary).**

Run `/compact` now. The doc is committed — state is safe. After compacting, re-read `## Active Work` from the doc to restore orientation before continuing.

**6. Continue working.**

Resume from `## Active Work`, top subtask first. Do not ask for confirmation — just proceed.
