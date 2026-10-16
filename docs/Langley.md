# Langley

[Comparative research](LangleyComps.md) surveys alternative products and UX patterns.

## Agent Conversation List

- [Status](../.wibey/docs/StatusVocabulary.md#status-definitions): ▶️ 🛑 ❓ ⏰ 👀 ⏸️ ⚠️ ☠️ ❌ ✅
- Title
- Started
- Idle
- Cost
- uncommitted files
- Model power/expense: \$–\$\$\$
- expanded
  - latest prompt with time
  - latest output with time
- obvious
  - repo, branch
  - harness
  - IDE
- out of scope
  - Conversation relationships — parent/fork, related parallel sessions, peer chats, delegated agents, and whether workspaces are shared or isolated.
  - Attached context — linked repositories, issues or pull requests, files or selected code, and the originating request.
- Organization and actions — search, filters, grouping and sorting, pinned/favorite/archive state, and direct resume/open/fork/archive/delete actions.

### Conversation table mockups

- One summary row per conversation; expansion inline; no cards or repeated badges.
- Screenshot-derived titles; completed endings and metrics are illustrative, not telemetry or Air capabilities.

#### Dense list

Conversations　⌕ Search…　All ▾　◴ ↑　＋


|      |                               |       |      |           |     |
| :--: | :---------------------------- | ----: | ---: | --------: | --: |
| ▶️ | ▾ phantom-agent              | ✦22m | ◴0m | \$\$\$.18 | Δ2 |
|      | 👤 Add a minimal off-VPN in… |       | ◴3m |           |     |
|      | 🤖 Restore trap added. Chec… |       | ◴0m |           |     |
|  ❓  | enable copilot in IDEA        |  ✦1d | ◴8m |   \$\$.42 | Δ1 |
|  ✅  | Wysiwyg editor: what doe…    |  ✦2d | ◴1d |    \$1.26 | Δ0 |
| ☠️ | code-puppy extension not…    |  ✦2d | ◴2d | \$\$\$.63 | Δ3 |

- Headers hidden; accessible column names and hover/focus labels retained.
- Titles: ≤25 grapheme clusters; truncate to 24 + `…`. Full title on hover/focus and in accessible names.
- → or disclosure: expand latest exchange; no intermediate state.
- Message previews: ≤25 grapheme clusters including `…`, excluding role/time; full text on hover/focus.
- Click changes: diff. Expansion never resumes execution.
- ✦: age since creation. ◴: age since last agent/user activity, not execution state.
- Ages: round down to one unit; minimum `0m`, never seconds. Exact timestamps on hover/focus.
- Spend: `$.18`, `$1.26`, `$0`; unknown `$?`. Prefix count: \$ low, \$\$ medium, \$\$\$ high model power/expense.
- Files: `Δ3` total; `Δ0` none; `Δ2+3-1` = modified/added/deleted, disjoint counts—not lines.
- Shared repo/branch/harness/IDE/permissions: scope line; mixed values: optional columns.

## Recommendation

Build the first usable version **inside the Wibey JetBrains plugin**, as an optional dense renderer for the existing history surface. Keep the existing renderer and navigation available. Separate **history appearance** from **conversation placement**: choosing a table should not also commit the user to editor tabs or a split pane.

Recommended progression: minimal dense prototype with existing navigation → collapsible list above the current conversation → optional conversation editor tabs. Change shared runtime/core only for demonstrated missing data or ownership contracts, not to render a JetBrains table. Defer a CLI UI until it has an independent user need.

The cheap part is drawing rows. The expensive parts are knowing what an agent is actually waiting for, attributing shared working-tree changes, and safely displaying the same live conversation in several places.

## Contents

- [Agent Conversation List](#agent-conversation-list)
- [Investigation checkpoint](#investigation-checkpoint)
- [Implementation baseline](#implementation-baseline)
- [History appearance and compatibility](#history-appearance-and-compatibility)
- [Conversation placement options](#conversation-placement-options)
- [Architecture and core boundary](#architecture-and-core-boundary)
- [Feature feasibility](#feature-feasibility)
- [Delivery phases](#delivery-phases)
- [Validation and acceptance](#validation-and-acceptance)
- [Choices for proceeding](#choices-for-proceeding)

*[doc-audit](https://github.com/BrianHoltz/tools/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.10.16.Fri*


## Investigation checkpoint

2026.10.16.Fri — documentation/design work only; no plugin implementation.

- **Completed:** comparative material separated into [Langley Comps](LangleyComps.md); conversation-list specification preserved here. JetBrains upstream and CLI session/history entry points inspected.
- **Working recommendation:** JetBrains-first optional dense history renderer, reusing existing actions and whatever status signals are already available. Fixed columns and existing ordering are sufficient for the first prototype.
- **Prototype exclusions:** custom sorting, resizable columns, excerpt expansion, richer status classification, dollar accounting, and attributed file counts are not prerequisites.
- **Next investigation:** confirm the target release/UI toolkit; compare minimal history replacement with integrated splitter and editor-tab lifecycle costs.
- **Parallel-agent scope:** independently evaluate placement and integration choices. Private source citations and verified data gaps are in the internal companion, `docs/LangleyImplementation.md`, in the team repository. Do not assume the developer checkout, installed plugin, and upstream main match.
- **Open choices:** preferred prototype placement; whether conversations outside the IDE need live attachment at launch; whether editor tabs are essential or a later option. No decision is required to finish this proposal.

## Implementation baseline

**Assessment date: 2026.10.16.Fri.** This is a design proposal, not an implemented feature or a runtime-tested compatibility claim. Source-level implementation evidence belongs in the internal companion, `LangleyImplementation.md`, under the team repository's docs directory; private code excerpts and internal repository links are deliberately excluded here.

Treat the installed plugin, a developer's local branch, upstream main, and in-flight UI replacements as different baselines. Before implementation, select the target release and UI toolkit with the maintainers. A speculative toolkit migration is not a reason to build two production renderers from scratch: keep the list model toolkit-neutral and implement against the accepted release path.

Distinguish these concepts throughout the design:

- **Conversation:** durable transcript identity, potentially reopened across processes.
- **Runtime session:** the process-local owner of execution, stream, pending requests, and cancellation.
- **View:** a sidebar, split-pane region, or editor tab showing a conversation.
- **Workspace:** repository/worktree context; multiple conversations can share it.

Historical discovery is not attachment to a running process. Opening a transcript is not sending a prompt. An idle session is not proof that its task succeeded.

## History appearance and compatibility

**Preserve the existing history UI initially.** Add a persisted `History view: Existing / Dense` preference and an immediately reachable switch in the history toolbar. Keep the existing History action, settings, shortcuts, storage, resume checks, rename/export/delete behavior, and any current compact picker. Scope the first rollout to opt-in users.

Use one conversation read model and one action layer for both views; do not copy the old history implementation into a competing storage/navigation subsystem. Existing-only presentation features may stay in the existing renderer, but destructive actions, identity resolution, permission handling, and resume gates must remain shared.

The dense view combines open, running, idle, closed, and historical conversations into one deduplicated list. Do not implement it as only a replacement for the historical half of a running/past split. Otherwise a conversation can disappear when it stops streaming but remains open. Preserve a row through that transition and through provisional-to-durable ID assignment.

An alternative is replacing the old renderer outright. That reduces long-term maintenance but broadens regression and adoption risk. Prefer retirement only after action parity, accessibility, large-history performance, and navigation behavior are demonstrated. Do not promise permanent support for every renderer/layout combination.

## Conversation placement options

These are independent of the Existing/Dense renderer switch. All placements use the same rows, selection identity, previews, and commands.

### History replaces chat — smallest change

The sidebar alternates between history and the selected conversation. Explicitly opening a row switches to chat; Back returns to the same query, scroll position, expansion, and selection. This preserves the familiar model and needs little layout work.

**Strengths:** lowest integration risk; narrow sidebar remains usable; fastest delivery. **Costs:** no persistent overview while reading or steering a conversation; repeated history/chat navigation.

**Interaction:** arrows change selection; Right/disclosure expands; Enter or clicking the title opens. Clicking status reveals the reason, and clicking Δ opens a diff. None of those actions sends a prompt or approves anything. Opening an already running conversation attaches its existing view rather than creating another execution owner.

**Difficulty:** small layout change, medium total delivery once the shared list model and accessibility are included. Recommended first release and permanent compact fallback.

### Sidebar list with conversation editor tabs — strongest overview

Keep history in the sidebar and open conversations in the central editor area. A preview tab follows selection; an explicit Open or pin action makes it durable. Support several conversation tabs and editor splits only after single-tab ownership works correctly.

**Strengths:** history stays visible; wide conversation area; native tab/split workflow; several conversations can be compared. **Costs:** editor lifecycle, focus, restoration, toolbar/action routing, memory, and close semantics become product features rather than cosmetic details.

Use a JetBrains file-editor integration with a stable virtual conversation identity and an explicit editor provider; verify APIs against the supported IDE build. Do not model a live conversation as a generated Markdown file. Opening two editors must not start two sessions. A Swing component cannot occupy two parents: either move its sole live view or construct separate views over the same session state. A read-only second view is a reasonable intermediate scope, but must be visibly read-only.

Closing an editor detaches the view, not silently stops work or deletes history. Stopping execution remains a separate action. Project close, runtime disconnect, deleted worktree, and reopened editor require explicit unavailable/reconnect states. Never auto-send after restoration.

**Difficulty:** large; a single read-only editor preview is medium. Best destination if simultaneous overview and multiple conversations outweigh editor space consumed by chat.

### Collapsible history above chat — recommended second phase

Place the dense list above the current conversation in the existing tool window, separated by a draggable horizontal divider. Collapse leaves a compact header with the current scope and attention count. Expansion restores the user's previous proportion; support a keyboard-operated resize/collapse action and persist proportions per project/layout.

**Strengths:** matches the requested integrated-pane vision; list and current chat stay visible without occupying code-editor tabs; reuses the existing conversation host. **Costs:** vertical competition in a short sidebar; nested scrolling, focus, composer visibility, and minimum heights need deliberate handling.

Keep the list outside the transcript's scroll container. Give it independent scrolling and bounded expanded-preview heights. Preserve the composer and enough transcript height to remain useful; when space is insufficient, offer collapsed or history-only mode rather than tiny unreadable regions. Selecting a row changes only list selection; explicitly opening it changes the lower conversation. Keep the active conversation highlighted separately from keyboard selection.

**Difficulty:** medium if the session/view boundary is respected; medium-large if the existing outer panel assumes exclusive history/chat cards everywhere. Recommended practical default after the dense renderer proves useful.

### Dedicated history tool window — modular alternative

Register a separate Conversations tool window while retaining the existing Wibey chat tool window. JetBrains docking can place them side-by-side, stacked, or on different edges. Row Open targets the existing chat host; it can target editor tabs later.

**Strengths:** both surfaces stay visible without custom splitter code; native docking; small impact on the existing chat container. **Costs:** another tool-window entry, discoverability, focus across windows, limited space when both dock on the same edge, and synchronization between two lifecycles.

**Difficulty:** medium. Useful if changing the current chat container is too invasive. Less coherent than the integrated split and less powerful than editor tabs; prototype it only if it resolves a concrete integration constraint.

### Shared interaction contract

- Expansion previews content only; it does not open, activate, resume execution, acquire a runtime, or trigger model usage.
- Open activates or restores a conversation; Send starts another turn. Keep any existing resume-cost warning until its semantics are explicitly reviewed.
- Maintain one execution owner per conversation; multiple views subscribe to it. A title click must not cancel a different running session.
- Permission decisions stay in the target session's existing approval UI. Status navigation is not a global approve button.
- Persist renderer, placement, sort/filter, and divider state separately. Avoid a settings matrix that exposes unfinished combinations.

## Architecture and core boundary

### JetBrains-first implementation

Introduce small, proposed components rather than adding table logic to a large chat coordinator:

- **ConversationListRepository:** reads existing summaries, lazily loads preview data, and merges local live sessions with persisted rows. Existing transcript/storage readers remain authoritative.
- **ConversationRow:** immutable identity, title, timestamps with provenance, status/reason, preview references, workspace context, optional spend, and optional file summary. Missing is distinct from zero.
- **ConversationListController:** selection, filtering, sort, paging, expansions, and action dispatch. Existing session-opening and destructive-action services remain responsible for their operations.
- **ConversationStatusReducer:** consumes session events to derive a display state without inspecting rendered widget text.
- **DenseHistoryView:** native list/table presentation; no transcript parsing, Git scans, or runtime calls inside cell renderers.
- **ConversationHost:** placement adapter for existing chat, integrated split, or editor. This is a narrow navigation boundary, not a new orchestration framework.

Use a native JetBrains table/list compatible with the chosen UI toolkit. For Swing, prototype a `JBTable` summary model plus nonselectable preview rows keyed to their parent conversation. That preserves column alignment and avoids a full nested chat renderer per row. Verify variable-height rows, sorting, screen-reader navigation, and selection before committing to this technique; a custom painted virtual list buys compactness at a substantial accessibility cost.

Update snapshots on the UI thread; perform storage/Git work on background dispatchers with cancellation. Refresh by events and a lightweight visible-age timer, coalescing streamed output rather than rebuilding every row per token. Lazy-load previews, memoize against transcript versions, and keep list scroll/selection stable as timestamps change. Do not silently reorder a row out from under a click; apply live sorting at a stable interaction boundary.

### What belongs in shared runtime/core

“Core” can mean a shared client library, the executable runtime/transport, or a central service. Confirm the actual owner before proposing a change; those are not interchangeable repositories.

**No core change needed for:** dense rendering, grapheme truncation, relative ages from known timestamps, search over supplied summaries, UI preferences, divider placement, or editor hosting. All are frontend responsibilities.

**Possible narrow shared contract:** versioned conversation summaries and lifecycle events carrying durable ID, source namespace, runtime owner, workspace, last user/agent activity, current wait reason, terminal outcome, and optional usage provenance. Add only fields a tested feature actually needs; old producers must remain readable with unsupported values shown as unknown.

**Core becomes justified when:** independently running CLI/IDE processes need trustworthy live discovery, attachment, request routing, heartbeats/owner leases, crash detection, or concurrent metadata writes. File watching can detect transcript changes, but cannot prove a permission request is pending or that another process owns a resumable live stream.

A shared file sidecar without cross-process concurrency control is not a session registry. If several clients write metadata, define ownership or compare-and-swap, schema negotiation, redaction, and rebuild behavior. Keep the index derived/rebuildable; do not introduce a second transcript source of truth.

### CLI-first and shared-service alternatives

**CLI-only table:** appropriate for terminal users, not a shortcut to a JetBrains history mode. It still needs conversation discovery, real status, previews, terminal width handling, and explicit resume semantics; editor tabs and IDE diffs do not transfer. A terminal embedded in the plugin would be a different UX with weaker native integration.

**Shared data contract, native UIs:** the best later expansion. Reuse semantics/schema and conformance fixtures, not Kotlin/Swing widgets in a TypeScript terminal application. Port a minimal read-only CLI list after the JetBrains model settles; add watch/attach only if supported by a real owner protocol.

**Daemon/control plane first:** strongest route to cross-IDE live sessions, but largest cost and security/lifecycle scope. It introduces installation, updates, process survival, IPC authorization, recovery, and multi-client writer arbitration. Not required to prove the desired history UX; defer unless live cross-process steering is a launch requirement.

## Feature feasibility

Effort labels describe incremental implementation risk, not commitments. Several simple cells can conceal difficult data ownership requirements.

### Title and dense rows — small

Reuse persisted/derived titles; never rename stored conversations just to fit a cell. Truncate display to 25 grapheme clusters, including ellipsis, using a Unicode implementation tested for combining marks, flags, and joined emoji. Ordinary string length is insufficient. Provide full title on hover, keyboard focus, and accessible name. Fit columns responsively; drop optional context columns before forcing horizontal scrolling.

### Started and idle ages — small presentation, medium semantics

Use recorded creation time; if only a fallback timestamp exists, show unknown rather than a fabricated start. Idle is elapsed time since actual user/agent activity, including meaningful streaming output, not merely the last save, file modification, or last completed turn. Record activity in the live session and persist suitable summary timestamps. A rename, pin, export, or index rebuild must not reset idle.

Round down to the largest defined unit, minimum `0m`; specify minutes/hours/days and exact hover timestamps. Clamp future timestamps to `0m` with diagnostic provenance. Creation and idle values are not lifecycle statuses.

### Status vocabulary — medium locally, large cross-process

Implement evidence-backed states, with an explanation available on focus/click:

- ▶️: executing a turn or tool; not merely an open tab.
- 🛑: explicit permission/action requirement; ❓: explicit user question.
- ⏰: a known timed wait or expected external event; not any slow tool call.
- 👀: explicitly awaiting review; not inferred from a final answer.
- ⏸️: explicitly paused work; an ordinary idle conversation is not automatically paused.
- ⚠️: recoverable fault; ☠️: recorded fatal failure; ❌: explicit cancellation.
- ✅: explicit completed task outcome or user mark; a completed model turn alone does not prove task completion.

Keep execution, attention, outcome, and open/closed state separate internally, even if one dominant glyph is rendered. Prefer actionable blocked states over a still-open stream indicator; distinguish recoverable/fatal errors only when the producer supplies that classification. Show a neutral unknown/idle indicator when evidence is insufficient. After restart, persisted “running” without a verified owner must become stale/unknown, not live. Add less-observable states progressively instead of inventing heuristics to fill every glyph.

### Latest prompt/output expansion — medium

Read the latest user text and latest assistant text with their own timestamps, excluding tool results, host notices, hidden reasoning, and command wrappers. For live work use current in-memory text; for history load lazily. A prompt waiting for its answer may legitimately sit above an older assistant message: preserve timestamps rather than implying they form a matched turn.

Render the requested 25-grapheme preview and accessible full text. Loading/error/empty states are necessary feedback, not an intermediate navigation page. Handle cancelled partial output, restored checkpoints, multiline text, attachments-only messages, and missing old timestamps. Never parse all full transcripts on each paint.

### Spend and model power — medium, with a dollar-data gate

The dollar mockup is a target, not authorization to relabel another usage unit as dollars. Use authoritative USD totals when available; otherwise show `$?` and offer separately labeled credits/tokens. Any estimate needs pricing basis, model mix, timestamp/rate version, and completeness. Do not silently sum known turns into an apparently complete total when others are unpriced, double-count cumulative usage, or reconstruct historical prices using today's rate card.

For multi-model sessions, define whether the power prefix denotes the currently selected model or the cost-dominant model. Recommend current/last effective model, with mixed history explained in the tooltip. Treat power and price as a user-facing tier classification, not an empirical claim that a costly model is smarter. Resolve aliases through model metadata; unknown tier remains unknown. An accessibility label must disambiguate tier dollars from actual spend.

### Uncommitted files and diff — medium workspace-wide, large attributable

Define Δ as **current dirty files in the row's repository/worktree**, including staged, unstaged, and untracked files, deduplicated by path. Count each path once; treat a rename as one modified path and deleted paths as deleted. Clarify handling of submodules, ignored files, and unavailable worktrees. Unknown is `Δ?`, never `Δ0`.

In a shared worktree this is a workspace total, not “files changed by this conversation.” Several rows can legitimately share it. Per-conversation attribution requires isolated worktrees, a recorded baseline plus change tracking, or an explicit attribution mechanism; a baseline alone still includes other writers. Do not promise attribution in the first release.

Reuse IDE VCS state where available, refresh once per distinct worktree on a bounded cadence/event stream, and avoid per-row Git processes. Δ opens the corresponding current workspace diff. A historical row must not display today's checkout as the conversation's old diff; label it current-worktree state or omit it when its worktree is gone.

### Repo, branch, harness, IDE, permissions — small locally, medium across origins

Show common context once in the scope line; reveal differing/unknown values per row or optional columns. Keep original conversation origin distinct from the host currently viewing it. Branch is session/worktree context, not the viewer's current branch projected onto every row. Do not infer an originating IDE from a transcript merely being visible in that IDE. Permission mode is informational; changing it must use the existing session-scoped controls.

### Search, filtering, sorting, and grouping — small to medium

Start with title/summary search and filters for attention, running, project, and pinned state; label search scope. Full transcript search needs background indexing, privacy controls, cancellation, and bounded result loading. Sort by created/activity/spend only when their data is known; put unknowns consistently last. Preserve pinned ordering and expanded children with their parent. Grouping must not turn previews into independently sorted rows.

### Pin, favorite, archive, open, fork, delete — mixed

Reuse pin/open/rename/export/delete contracts. Prefer pin as the first favorite mechanism rather than two indistinguishable preferences. Archive is a reversible visibility flag, not deletion or execution cancellation; introduce storage only if missing and define its interaction with running sessions. Fork is a deliberate history action, distinct from merely displaying a parent/child relationship; verify runtime checkpoint support before offering it, and defer generic cross-harness forks. Confirm deletion with the exact title, preserve existing protections against autosave resurrecting deleted history, and do not invent bulk deletion for the first release.

The specification excludes relationship visualization and attached-context browsing. Keep those exclusions even where the underlying runtime supports related features.

## Delivery phases

Estimates are rough engineering ranges for one contributor familiar with the plugin, excluding review queues and unrelated runtime migrations. They are incremental, not a project schedule; source-level design cannot establish measured delivery time.

### Baseline and interaction spike — 2–4 engineering days

Select target release/toolkit; map actual history, live-session, storage, and action paths. Build synthetic-data prototypes for the three requested placements; assess the dedicated tool-window alternative only if useful. Validate column fit, keyboard interactions, preview row accessibility, and stable identity. Decide timestamp/status/Δ/spend semantics before introducing persistence.

**Exit:** a chosen UI integration point, fixture-backed row contract, and a working narrow-width table prototype. No core dependency required.

### Minimal dense prototype — 1–3 engineering days

Reuse current summaries, status indicators, default ordering, and existing open callbacks. Use fixed nonresizable columns, title, available age/context fields, and unknown placeholders or omitted unsupported cells. Keep the existing history renderer selectable. No new status taxonomy, sorting controls, column-width settings, previews, core changes, or storage migrations. Prefer a small renderer spike over extracting a comprehensive repository/controller architecture before first use.

**Exit:** an actual dense history mode that opens existing conversations safely and can be compared with the current UI. Synthetic rows are acceptable for layout exploration but must be clearly labeled; connect real summaries before calling it a usable prototype.

### Dense history hardening — 4–8 engineering days

Harden the opt-in Existing/Dense switch; unified live/persisted rows; title, known start/activity age, truthful basic status, scope context, title search, sort, pin, open, and existing safe actions. Add disclosure previews with lazy loading only after the basic table is useful; custom sorting and column resizing are optional follow-ups, not release blockers. Display honest unknowns for spend and Δ when not yet backed by data. Preserve legacy history and picker behavior.

**Exit:** every conversation remains discoverable across running→idle→closed transitions; opening/expanding never sends a message; old data works without migration. This is a useful independently shippable product.

### Live attention and integrated split — 5–10 engineering days

Add structured permission/question/error state and last-activity events; establish precedence, stale-owner behavior, and keyboard navigation to attention. Integrate upper-list/lower-chat splitter, collapse, independent scrolling, minimum heights, and persisted layout. Keep history-only available. Implement trustworthy workspace Δ and diff where VCS integration allows it; keep attribution deferred.

**Exit:** overview stays visible while another session streams or waits, and selecting/opening never interrupts unrelated work. No cross-process live claim without an owner protocol.

### Optional conversation editor hosting — 8–15 engineering days

Spike one editor-hosted conversation, first read-only if necessary; establish session ownership and close/restore semantics. Then enable interactive preview/pinned tabs and several conversation tabs. Add multi-view subscription only after lifecycle tests pass. Reuse the same history and command model.

**Exit:** closing/moving/splitting views cannot duplicate sends, lose drafts, approve the wrong request, cancel unrelated streams, or resurrect deleted conversations.

### Shared runtime and richer accounting — separate discovery scope

Only after measured gaps: reliable cross-process owner events, optional CLI list, cross-client attach, complete USD accounting, attributable changes, archive/fork parity, full-text index, or additional harness adapters. Size each separately; these are not a single cheap “polish” phase. Share contract fixtures before extracting a library or introducing a daemon.

## Validation and acceptance

Use failing tests before implementation, then targeted tests and the supported full suite. A documentation proposal is not evidence that these checks already pass.

- **Identity:** provisional IDs, SDK/durable IDs, two simultaneous opens, live/persisted dedup, restored/forked histories, deleted rows, and stable selection during refresh.
- **Semantics:** missing versus zero, no fabricated success, pending permission/question precedence, recoverable/fatal errors, cancellation, stale running after restart, and historical records lacking timestamps/usage.
- **Formatting:** grapheme fixtures, exact age thresholds and future clocks, unknown spend/tier, partial pricing, mixed models, 25-grapheme previews, and independent preview timestamps.
- **Navigation:** expansion causes no runtime calls; Open reuses an owner; Send only targets its conversation; legacy shortcuts and resume gates remain intact.
- **VCS:** staged+unstaged same path, untracked/deleted/renamed files, shared worktrees, missing worktrees, multi-root projects, and exact diff target.
- **Layouts:** narrow sidebar, small window height, divider keyboard control, independent scrolling, editor close/restoration, simultaneous sessions, draft preservation, and focus return.
- **Accessibility:** keyboard-only completion of every action; named columns despite hidden headers; accessible expanded state; full-text focus disclosure; visible focus; no color/emoji-only meaning; screen-reader checks at scaled fonts. Apply WCAG 2.2 AA equivalents suitable for native desktop UI.
- **Performance:** benchmark synthetic histories with thousands of summaries and very large transcripts. Proposed budgets: warm visible page within 200ms and simple selection/expansion feedback within 100ms on a named reference machine; cold reads asynchronous with progress. Measure before accepting these budgets. No transcript or Git I/O on the UI thread, no unbounded component-per-history construction, and no listener/timer leaks after toggling layouts.
- **Privacy and rollback:** no transcript/preview payloads in telemetry; no new network dependency for history; UI flag off returns to the existing renderer without losing data. Use redacted fixtures, never real private conversations in snapshots.

## Choices for proceeding

**Low-risk experiment:** implement dense history using existing navigation only. Best if the question is whether the table itself is valuable; smallest maintained surface.

**Recommended JetBrains product path:** dense history, then the collapsible upper-list/lower-chat layout. Keep existing history as a compatibility fallback and preserve an optional history-only placement. This directly addresses the requested sidebar experience without forcing shared-runtime work.

**Editor-centric path:** dense sidebar plus conversation editor tabs. Choose this when several visible conversations are a primary requirement; accept the larger session/view lifecycle refactor and treat editor hosting as its own deliverable.

**Cross-client platform path:** shared summary/event/owner contract before CLI and JetBrains watch/attach. Choose only if conversations started outside the IDE must be live and steerable at launch. It is substantially more than an alternate history renderer.

**Recommended decision:** authorize the baseline spike and dense-history release, with integrated split as the intended next placement. Reserve editor tabs as an opt-in follow-up. Require an explicit demonstrated gap before changing core; do not make complete dollars, change attribution, all status glyphs, or cross-process steering prerequisites for the useful first version.
