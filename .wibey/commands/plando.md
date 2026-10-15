---
name: plando
description: Structured plan-and-execute workflow with aidocs task record and audit trail.
---

> [!NOTE]
> **Mirror-safe command.** This file contains no Walmart-proprietary content and is
> designed to be manually mirrored to personal laptops. The canonical copy lives in
> [`relationship-shared/.wibey/commands/`](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared).
> **If you are reading this outside of Walmart GHE, do not edit it here** — make
> changes in relationship-shared and re-sync.

# Plan and Do

This command does NOT use plan mode. You stay in your current permission mode and both plan and execute in a single session. The goal is to get the benefits of structured planning without the mode-switch overhead.

Make and execute a detailed systematic plan for the following request.

- **Orient.** If `AGENTS.md` exists, read it and consult its "What to Read for a Given Task" table for any docs relevant to this request. Read the repo-specific doc in `shared/docs/repos/` if one exists.
- **Clarify.** Ask any clarifying questions before you start.
- **Anchor Doc.** Find or create the anchor doc using `AnchorDoc.md §Find`.
  (Path: `shared/docs/AnchorDoc.md` → `~/bin/.wibey/docs/AnchorDoc.md` →
  [GitHub](https://github.com/BrianHoltz/tools/blob/main/.wibey/docs/AnchorDoc.md).)
  1. **Find existing:** Run steps F1–F4. If a matching doc exists: update Active Work with
     this task's plan, add a Work Log entry, and proceed.
  2. **Decide on new doc:** If none found, decide:
     - **Attach** to an already-open aidocs file if this work is clearly within a larger
       tracked task.
     - **Create** `aidocs/yyyy-mm-dd/hhmm_CamelCase.md` (use `shared/aidocs/…` if a
       `shared/` symlink exists) if this is a self-contained new task.
  3. **Seed** new docs: populate `## Summary` with the task description, add a
     timestamped `## Work Log` entry, add blank `## Active Work` and
     `## Open Questions` sections.
  4. **Open in the default editor:** `open <filepath>` (respects the current macOS
     default app for Markdown, not a hardcoded editor). Update as you execute —
     plan phases in Active Work, blockers in Open Questions.
- **Plan.** Break the work into numbered phases with clear deliverables.
- **Execute.** Use the deep knowledge and skills in this repo and any linked shared/ repo. If you are Wibey, leverage your DX/MCP powers and run the /safe-browse command if you might need a browser. For work with independent or parallel workstreams, you may spawn subagents — all state flows back to the anchor doc; subagents do not maintain their own docs. Think critically and question your assumptions.
