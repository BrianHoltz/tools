---
description: Cluster pending changes across all IDEA git roots into repository-local commit buckets.
allowed-tools: Bash(git *), Read, Grep, Glob
---

## Context

- Canonical file inventory in each root: !`commitz_ui`
- Current git diff in each root (for understanding changes): !`git diff HEAD`
- Recent commit style reference in each root: !`git log --oneline -10`

Process all dirty Git roots shown in the IDEA VCS window in one interaction.
Keep each root's commits, pushes, histories, and buckets separate under the
hood. Do not include arbitrary nested repositories that are not IDEA VCS roots.

The file list from `commitz_ui`, run from each root, is the source of truth for
which files changed and their +/-stats. Do not invent files or stats not
present in `commitz_ui` output.

## Your task

1. Identify every dirty IDEA Git root for the current run.
2. In each dirty root, run `commitz_ui` to get its canonical file inventory, counts, and CTA chrome.
3. In each dirty root, read `git diff HEAD` and `git log --oneline -10` to understand the changes and commit style.
4. Cluster files into logical commit buckets, never putting files from different repositories in one bucket.
5. Assign one global bucket number to every bucket, grouped under its repository path.
6. Present one combined block containing each repository's `commitz_ui` counts, its bucketed files, and its unpushed count and CTA. Omit clean roots.

### Output format

Emit a horizontal line, then present each dirty repository as a subsection.
Use that root's heading, untracked line, unpushed line, and CTA from
`commitz_ui` verbatim, replacing its numbered file list with the globally
numbered bucketed version. Include the repository path in each subsection
heading so identical basenames remain unambiguous.

Single-file bucket — the bucket line IS the file line:

    N. filename +A/-D: <=30-char summary

Multi-file bucket — a short title line, then indented file sub-items:

    N. short bucket title [repo: ~/path]
      - filename +A/-D: <=30-char summary
      - filename +A/-D: <=30-char summary

### Example output

```
home (~/path/to/repo)
3 files to commit. Select buckets with e.g. 1,3-7 or omit for all.
1. commitz_ui output improvements [repo: ~/path/to/repo]
  - commitz_ui +40/-11: count heading, untracked line
  - commitz_ui_test.py +28/-5: update count assertions
2. commitz.md +16/-4: restore bucketing rules

6 commits already in next push.
C: commit. P: commit+push. Or ignore & keep prompting.
```

### Key rules

- The <=30-char label per file is a **display summary only**, not the commit message.
- Every file from every dirty root's `commitz_ui` appears in exactly one bucket.
- Never invent files absent from `commitz_ui`.
- Prefer fewer coherent buckets. One bucket is fine if all changes are related.
- Keep code + its tests/docs together in the same bucket.
- Use basenames only — no directory paths.
- Every bucket belongs to exactly one repository; include the repository label on
  every multi-file bucket and in each repository subsection.
- `C` stages and commits selected buckets separately within their owning
  repositories. `P` does the same, then pushes each affected repository
  separately. Never stage or commit across repository boundaries.
**STOP after presenting buckets. Do not commit until the user sends a C or P token.**

## `yours` mode

Invoked as `/commitz yours`.

1. **Identify agent-touched files**: review this conversation's history to determine which files you (the agent) created or modified via Edit, Write, or equivalent file-writing tools. These are "your files."
2. **Run `commitz_ui` in every dirty IDEA Git root** to get canonical inventories.
3. **Filter**: keep only entries matching your files, retaining each file's repository. If a file you touched is absent from `commitz_ui` (already committed or untracked), note it but don't block.
4. **Bucket** the filtered files using the normal cross-repository bucketing rules above.
5. **Show the buckets** briefly for visibility, then immediately — without waiting for a C/P token:
   - Commit each bucket (autonomous commit messages, repo style, one per bucket).
   - Push each affected repository.
   - For any `.md` files in the committed buckets: if the `md2confluence` skill is available and the file has a Confluence front-matter marker, invoke `md2confluence` to mirror it. Skip silently otherwise.
6. Show final `git log --oneline` for new commits and `git status`.

## Token handling

- `C` or `C.`: commit all buckets.
- `C1,3-5` or `C1,3-5.`: commit only selected bucket numbers.
- `P` or `P.`: commit all, then push. If nothing to commit, push only.
- `P1,3-5` or `P1,3-5.`: commit selected buckets, then push.

Period separates token from rest of prompt: `C1,3. and also fix the tests`

**Nothing to commit:** if `commitz_ui` shows no uncommitted files but there are unpushed commits, skip bucket presentation. Show only the unpushed count line and the P CTA.

## Commit behavior

- Bucket numbers from the most recent combined bucketed block are the reference.
- Stage only files in selected buckets, and stage them only in their owning
  repository.
- Write good commit messages autonomously (repo style). Do not draft or ask.
- One commit per bucket unless user says otherwise, with no cross-repository
  commits.
- After commits, show each affected repository's `git log --oneline` for new
  commits and `git status`.
- Push only on explicit `P` token, pushing each affected repository separately.
