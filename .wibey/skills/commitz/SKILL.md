---
name: commitz
description: Review pending Git changes across the current IDE's repository roots, group them into commit buckets, and commit or push only after an explicit C or P token.
user-invocable: true
disable-model-invocation: true
---

# Commitz

Use this workflow when the user invokes `/commitz`. This file is the canonical
cross-harness workflow; IDE and agent entry points should delegate here.

## Inventory and review

1. Identify the Git roots attached to the current IDE/workspace. Prefer the
   IDE's registered VCS roots. If unavailable, use only the current workspace
   folders and their directly configured Git roots; do not recursively scan
   arbitrary nested repositories.
2. In each dirty root, run `commitz_ui` (or `~/src/tools/commitz_ui`) to obtain
   the canonical file list, counts, additions/deletions, untracked line,
   unpushed count, and CTA. Do not invent files or statistics.
3. Read `git diff HEAD` and `git log --oneline -10` in each dirty root.
4. Group related files, keeping every bucket inside exactly one repository.
   Give every bucket a global number across the response. Keep code, tests, and
   directly related documentation together.
5. Present one block: repository heading and path, that root's `commitz_ui`
   count/untracked/unpushed/CTA text, then the bucketed file list. Use
   basenames and a display summary of at most 30 characters for each file.

Single-file bucket:

    N. filename +A/-D: short summary

Multi-file bucket:

    N. short bucket title [repo: path]
      - filename +A/-D: short summary
      - filename +A/-D: short summary

Every file from `commitz_ui` must appear in exactly one bucket. Prefer fewer
coherent buckets. Omit clean roots.

**Stop after presenting the buckets. Do not commit until the user sends a C or
P token.**

## Explicit token handling

- `C` or `C.`: commit all buckets.
- `C1,3-5` or `C1,3-5.`: commit selected buckets only.
- `P` or `P.`: commit all buckets and push; if there is nothing to commit,
  push only.
- `P1,3-5` or `P1,3-5.`: commit selected buckets, then push.
- A period separates the token from any additional request, e.g.
  `C1,3. and also fix the tests`.

For selected buckets, stage only their listed files and commit each bucket
separately in its owning repository. Never stage or commit across repositories.
Use the repository's commit-message style and include the configured
Co-authored-by trailer. Push only for an explicit P token. After committing,
show the new `git log --oneline` entries and `git status` for every affected
root.

## `yours` mode

When invoked as `/commitz yours`, identify only files changed by the current
agent in this conversation, filter each root's `commitz_ui` inventory to those
files, bucket them with the same repository boundaries, then commit and push
those buckets without waiting for C/P. Keep the buckets visible in the
response. Do not include a file absent from `commitz_ui`; note it briefly.
