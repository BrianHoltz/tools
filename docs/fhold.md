# FHold Concurrent Write Permit Protocol

## Context

`fhold` coordinates whether a tracked Markdown file is in exclusive human-review mode or user-authorized parallel-write mode. Review mode is an exception for an imminent, intentional human review—not the default for every agent edit—because its exclusive hold blocks all other agents from writing that file.

An agent may register a review hold only when it is highly confident the user intends to inspect and resolve this specific diff promptly, and is likely to do so within 10 minutes. Otherwise use the normal concurrent-write workflow. Register immediately before the first reviewed write; release immediately when the user accepts/rejects the diff. Do not renew or wait beyond 10 minutes. If the diff is still unresolved then, stop and ask the user to resolve it before any further writes to that file. Do not silently release the unresolved hold and continue: a later IDE rejection can revert subsequent edits. This is a behavioral limit; the current CLI's default hold TTL remains 30 minutes and does not enforce the 10-minute review window.

When another agent discovers an existing review hold, it must show the owner and hold details and wait for the user's decision. A hold older than 10 minutes has exceeded the review window; ask the user to resolve it. Never release or take over an unresolved review hold automatically, because a later IDE rejection may revert subsequent writes. A review hold is not permission to make later writes while the user reviews.

## Menu (as presented to user)

`[filename]` has a review hold from another agent. Resolve or ignore the pending changes, then indicate your decision:

- **Diff resolved, stay in review mode** — This agent will register its own review hold and write its changes for review. Future agents finding a review hold will be offered the same options.
- **Diff resolved, switch to unreviewed mode** — This agent will register a permit hold and write without user review. All subsequent agent changes use permit holds until all permits have expired or been released, at which point review mode resumes automatically.
- **Diff ignored, switch to unreviewed mode** — Current on-disk state is treated as accepted; the review hold is released. All subsequent agent changes use permit holds and write safely in parallel (via safewrite) until all permits have expired or been released, at which point review mode resumes automatically. ⚠️ The pending diff can be safely accepted at any time, but rejecting any part of it will immediately overwrite any disk changes (including this agent's) that happened after that pending diff was authored.

## Hold Tags

Holds are implemented as sidecar tag files under `/tmp/fhold.tags/`. Each file is keyed by `sha256(resolved_path)[:24]`, the same scheme as safewrite locks. Not in any repo; ephemeral; cleared on reboot.

Applies only to git-tracked markdown files.

### Review Hold (review_hold)

**Meaning:** An exclusive, short-lived checkpoint for an imminent human review. If the user rejects the diff, the IDE may revert all changes made after those writes; the IDE may not detect that conflict reliably. Use only when the user is expected to resolve this exact diff within 10 minutes. Otherwise do not take this hold.

**Tag:** `<path-hash>.review_hold`

**When created:** Only for a user-requested or clearly expected imminent diff review; register immediately before the first write, via `fhold review register <file>`. It is created atomically (O_EXCL). The hold remains active through the reviewable writes and the user's prompt review, for no more than 10 minutes. Release immediately when the user accepts/rejects. If unresolved at 10 minutes, stop and ask the user to resolve it; do not renew it or silently release and continue. On success: exit 0, prints the tag path. On contention (review hold already exists): exit 2, prints the owning agent's session-id and task to stderr.

**Contents:**

```
agent: <session-id>
file: <repo-relative-path>
task: <one-line description>
acquired: <ISO timestamp>
pre-write-sha256: <hash of file before any writes>
post-write-sha256: <hash of file after all writes complete>  ← written after release
```

**Released by:** Immediately after the user resolves the diff, using `fhold review release`. Ten minutes is the maximum intended review window, not a reason to auto-release an unresolved diff; after ten minutes stop and ask the user to resolve it. The CLI's configured stale-hold TTL is currently 30 minutes.

**Auto-stale detection:** If `post-write-sha256` is set and current file hash differs → user rejected/modified the diff → hold is stale, auto-release on next check. The `post-write-sha256` is captured after `fhold review release` to mark what the user reviewed.

### Permit Hold (concurrent_write_permit)

**Meaning:** The user authorized unreviewed parallel writes when the agent registered this permit. Multiple agents may hold permits simultaneously. No agent should make IDE-reviewed writes while any permit exists for the file.

**Tag:** `<path-hash>.concurrent_write_permit.<session-id>`

**When created:** When an agent begins working on a file in unreviewed mode (i.e. after contention is resolved with a "switch to unreviewed mode" choice). Agents in review mode register review holds, not permit holds. Writes use safewrite for CAS-coordinated parallel access.

**Contents:** Minimal — agent-id and file path. The tag file's **mtime is the heartbeat**; refreshed on each write to the target file.

**Released by:** Explicit `fhold permit release`; TTL 30 min of mtime inactivity.

**Dual purpose:**

- Signals that this file is in unreviewed mode. Any permit hold present = unreviewed mode. No permit holds + no review holds = review mode (default).
- Tracks active agents so the last to release can restore review mode. When all permit holds are gone, review mode resumes automatically — no user action needed.

---

## Known Hazards

**IDEA Accept All hazard:** If the user makes any local edits to the file while reviewing an agent diff — including undos — clicking "Accept All" in IDEA will revert all such edits or undos and just accept the original proposed changeset. While a review hold is active, accept or reject individual diff chunks only; never use Accept All if local edits have been made.

---

## Prior Art

**Emacs `.#filename` symlink** — closest analogue to the review hold. Emacs creates a symlink (not a regular file) whose target encodes `USER@HOST.PID:BOOT`. Lives adjacent to the target file, not in /tmp. Exclusive only; no pending-review semantic; no multi-writer concept. Validates the "tag lives near the file" pattern, though we deliberately chose /tmp to avoid repo pollution.

**Git `index.lock` / `packed-refs.lock`** — validates O_EXCL atomic creation. Pure exclusive mutex with no metadata stored; recovery from crashes requires human intervention. Confirms file-based tags over POSIX are the right approach.

**POSIX fcntl/flock advisory locks** — three documented failure modes explain why we use file-based tags instead: (a) any fd close from any thread releases all locks on that inode; (b) unreliable or silent-no-op over NFS; (c) advisory-only means non-cooperating processes are not blocked. None of these affect our file-based approach.

**Non-exclusive permit holds** — no prior art found. The counting-semaphore pattern exists in-process but has no widely-used filesystem incarnation for coordinating independent writers. The inversion here — multiple simultaneous permit holds collectively signaling a shared mode — is uncommon in filesystem coordination.

**AI agent frameworks (AutoGen, CrewAI, LangGraph)** — all coordinate at the message or state-graph layer, not the filesystem. None treat concurrent file writes as a first-class concern or have a pending-review primitive.

**"Pending review" as a write-coordination primitive** — novel at the machine level. GitHub PR review status and Wikipedia Pending Changes are semantic analogues but are human editorial workflows operating at coarser granularity.

**Remote writer limitation** — tags in `/tmp` are invisible to agents on other hosts, the same failure mode that made POSIX flock unreliable on NFS. Deliberately out of scope: this protocol targets single-machine human-in-the-loop workflows only.

## Reviewed Improvement Suggestions (2026.05.09)

This section replaces an earlier conversational note with a decisioned review.
Each item was checked against the current `fhold` implementation.

### Accepted (high priority)

- **Atomic tag writes for updates**: accepted.
  Current `_write_tag` uses direct `write_text`, which can expose partially written JSON to concurrent readers.
  Revision: write to a temp file in the same directory, then `os.replace()`.

- **Proactive TTL enforcement in operational commands**: accepted.
  Current stale cleanup depends on explicit `fhold gc`.
  Revision: `review register`, `permit check`, and `status` should ignore or clear expired tags based on `--ttl` before deciding mode or contention.

- **Narrow broad exception handling in tag reads**: accepted.
  Current `_read_tag` catches all exceptions.
  Revision: catch only expected file/parse errors (for example `OSError` and `json.JSONDecodeError`) so interrupts and fatal signals are not swallowed.

### Accepted (medium priority)

- **Deduplicate repeated tag-age logic**: accepted.
  Revision: add a shared helper for mtime age computation and fallback behavior.

- **Harden review-hold creation write path**: accepted.
  Current atomic create path is correct (`O_CREAT|O_EXCL`), but error-safe file descriptor handling should be improved.
  Revision: use `os.fdopen` context handling after `os.open` so failures do not leak descriptors.

### Deferred (needs compatibility decision)

- **Change default tag root from shared `/tmp/fhold.tags/` to user-scoped path**: deferred.
  Benefit: better isolation on multi-user machines.
  Risk: behavior drift for users/scripts expecting the existing global default.
  Next step: decide whether to change default, add an opt-in mode, or support a migration window.

- **Migrate manual CLI parsing to `argparse`**: deferred.
  Benefit: less fragile flag handling.
  Risk: command UX/help formatting and argument-position behavior may change.
  Next step: keep current parser unless parser bugs become frequent.

### Not Recommended Right Now

- **Convert tag metadata to dataclasses**: not recommended currently.
  The tag schema is small, and dict-based metadata keeps file I/O and backward compatibility straightforward.

### Implementation Order

1. Atomic `_write_tag` and safer fd handling.
2. Proactive TTL checks in status/register/check paths.
3. Exception narrowing and age-helper refactor.
4. Optional tag-root and parser redesign decisions.
