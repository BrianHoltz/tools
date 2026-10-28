---
name: doc-audit
description: Audit and improve maintained documentation for accuracy, structure, links, duplication, and durable wording. Use doc-audit interview for user-guided cleanup proposals and decisions. Exclude ephemeral scratch notes.
---
# Doc Audit Skill

Consolidated reference for documentation authoring, project document formatting, and audit standards. Describes patterns for any repo: immortal (timeless) vs mortal (time-bound) docs, mortal doc structure, evidence, temporal writing, and consistency audits.

## Governing rule

Laser-focus documents on empowering humans and agents to understand the current state and future paths. Ruthlessly remove stale material and historical narrative unless critical to that understanding; tombstone only when the deletion itself needs a durable pointer. Only closed task-table entries and Work Logs are exempt. Apply this test to every section, including evidence and resolved investigations. Lean toward compression/deletion: Git preserves the discussion. Commit messages must clearly tombstone removed topics and why they were retired, so readers can recover them without keeping a recap in the document.

## Contents

- [Immortal vs Mortal Docs](#immortal-vs-mortal-docs) — timeless reference vs time-bound work docs
- [Mortal Doc Structure](#mortal-doc-structure) — sections, consistency, task tracking
  - [Summary](#summary)
  - [Contents](#contents-1)
  - [Tasks](#tasks)
    - [Status Glyphs](#status-glyphs)
    - [Format Rules](#format-rules)
    - [Task Table Columns](#task-table-columns)
    - [Task Discipline Rules](#task-discipline-rules)
  - [Active Work](#active-work)
  - [Next Daily Jira Update](#next-daily-jira-update)
  - [Draft Next Comms](#draft-next-comms)
  - [Pending Decisions](#pending-decisions)
  - [Decisions](#decisions)
  - [Pending Investigations](#pending-investigations)
  - [Resolved Investigations](#resolved-investigations)
  - [Diagnosis](#diagnosis)
  - [Evidence](#evidence)
  - [Work Log](#work-log)
- [Drafting Comms](#drafting-comms) — evidence-linking bar for outbound messages
  - [Compose](#compose)
  - [Substantiate](#substantiate)
  - [Verify](#verify)
  - [Maintain](#maintain)
- [Rules About Pending Work](#rules-about-pending-work)
  - [Tasks Pipeline](#tasks-pipeline)
  - [Where Pending Work Lives](#where-pending-work-lives)
  - [Where Pending Questions Live](#where-pending-questions-live)
  - [Cross-References for Pending Work/Questions](#cross-references-for-pending-workquestions)
- [Doc-audit interview](#doc-audit-interview) — user-guided cleanup
- [Doc Audit Checklist](#doc-audit-checklist) — run on every non-trivial edit
  - [Task Creep Audit](#task-creep-audit)
  - [Active Work Hygiene Audit](#active-work-hygiene-audit)
  - [When to Audit](#when-to-audit)
  - [What to Audit](#what-to-audit)
- [See Also](#see-also)
- [Temporal Writing Rules](#temporal-writing-rules) — timeless perspective, absolute dates, no future prose
  - [Timeless Perspective](#timeless-perspective)
- [Content Brittleness](#content-brittleness) — sync with code, avoid line numbers, maintain TOC
- [Ad Hoc Documents](#ad-hoc-documents) — placement, naming, when to create
  - [Placement](#placement)
  - [Naming](#naming)
  - [When to Create](#when-to-create)
- [Styling Discipline](#styling-discipline) — footnotes, table cells, links, escaping
  - [Table Cell Vocabulary](#table-cell-vocabulary)
  - [Escaping](#escaping)
  - [Hyperlinks](#hyperlinks)
  - [Mandatory Links](#mandatory-links)
  - [Define Terms on First Use](#define-terms-on-first-use)
  - [Stylistic Restraint](#stylistic-restraint)
- [DRY Principles](#dry-principles) — no revision history, banned phrases
  - [Rule Change Management](#rule-change-management)
  - [Banned Words and Phrases](#banned-words-and-phrases)

## Immortal vs Mortal Docs

Every repo organizes docs into two types:

- **Immortal docs** — timeless, non-narrative, reference (e.g., specs, designs, playbooks, guides). Maintained for accuracy and durability.
- **Mortal docs** — content is anchored to a defined time span and not maintained afterward (e.g., projects, incidents, releases, memos).

### Testing.md Evidence Records

A `*Testing.md` file is a leaf-node CRQ evidence payload, not a mortal work document. It is frozen to PDF and attached to the ServiceNow CRQ at submission so the collected evidence cannot be edited after submission. Agents must enforce these rules even where the general mortal-document template conflicts:

- no YAML frontmatter;
- no Work Log, editorial history, task tracking, status narrative, project summary, or navigation section;
- no links to other documents, including project docs, CRQ docs, SQL files, or testing records; the required final crq-write provenance link and local image references needed to render evidence in the PDF are allowed;
- body content is only text destined for the final PDF, actual Red/Green evidence, and visible `(TODO: …)` or `(TBD: …)` markers whose surrounding text says exactly what evidence remains to be captured; the marker’s closing `)` ends the macro;
- preserve evidence already collected; do not replace it with procedures, operational instructions, or cross-references;
- use named Red/Green sections near the top when the test record covers pre-change and post-change evidence;
- end with the universal plain-text provenance signature `Powered by {Model} in {Harness} in {IDE} via [crq-write](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared/blob/main/.wibey/skills/crq-write/SKILL.md)`, separated from the evidence by a blank line. Keep it unitalicized so the prescribed PDF renderer prints it literally. Resolve model, harness and IDE values using [runtime provenance](https://github.com/BrianHoltz/tools/blob/main/docs/AgentRules.md#communication-signing); Code Puppy and Wibey always include core and active extension/plugin versions, with explicit unknown or CLI n/a when applicable. Never guess.

The Testing.md file is immutable after CRQ submission. Any planning, execution procedure, rationale, cross-reference, or work history belongs in the project or CRQ document instead.

## Mortal Doc Structure

Organize mortal docs with the following sections:

**● required, ○ optional, — not applicable:**


| Section                 | Projects | Incidents, Releases | Memos |
| ----------------------- | -------- | -------------------- | ----- |
| Summary                 | ●       | ●                   | ●    |
| Contents                | ●       | ○                   | ○    |
| References              | ●       | ○                   | ●    |
| Tasks                   | ●       | ○                   | —    |
| Active Work             | ●       | ○                   | —    |
| Next Daily Jira Update  | ○       | ○                   | —    |
| Draft Next Comms        | ○       | ●                   | ○    |
| Pending Decisions       | ○       | ○                   | ○    |
| Decisions               | ○       | ○                   | ○    |
| Pending Investigations  | ○       | ●                   | ○    |
| Resolved Investigations | ○       | ○                   | ○    |
| Diagnosis               | —       | ●                   | —    |
| Evidence                | ●       | ●                   | ●    |
| Work Log                | ●       | ●                   | ○    |

### Summary

Sits at the very top. Always structured bullets — never prose paragraphs. See [Project.md](../../../docs/templates/Project.md) and [Incident.md](../../../docs/templates/Incident.md) for canonical markup.


| Field     | Projects                    | Incidents                                            | Memos                          |
| --------- | --------------------------- | ---------------------------------------------------- | ------------------------------ |
| **Where** | ● trackers esp. Jira       | ● trackers esp. Slack                               | ○ often no trackers           |
| **What**  | ● capability               | ● business impact                                   | ● findings, conclusions      |
| **Why**   | ● significance, motivation | ● leading hypothesis                                | ● significance, motivation    |
| **How**   | ● approach                 | ● symptoms, not root cause                          | ○ methodology                 |
| **Which** | ● systems                  | ● systems                                           | ○ systems                     |
| **Who**   | ● ICs, teams              | ● ICs, teams                                        | ○ ICs, teams                  |
| **When**  | ● Started, Stg, Prod     | ● Started, Detected, Invoked,<br />Engaged/Routed | ○ Started, 1st/last published |

### Status

No doc type gets a dedicated `## Status` heading — none of [Project.md](../../../docs/templates/Project.md), [Incident.md](../../../docs/templates/Incident.md), or the memo pattern define one (consistent with the [Mortal Doc Structure](#mortal-doc-structure) table above, which has no Status row). Status is conveyed inline instead, using the mechanism suited to each doc type:

- **Projects**: the [Tasks](#tasks) table **IS** the status display — keep it well-sorted and up-to-date so readers can scan it directly for current work. With the sorting discipline (done → in-progress → not-started, preserving order within each group), the Tasks table itself provides clear status visibility without needing a separate section.
- **Incidents**: fold outcome/status into Summary's **What** (Business Impact) bullet — e.g. "Outcome: ✅ test completed successfully..." or a status token from [StatusVocabulary.md](../../../docs/StatusVocabulary.md) (optionally qualified with an em-dash, e.g. `INVESTIGATING — root cause undiagnosed`), inline in that bullet. Updated each session. **Never create a standalone `## Status` heading for an incident** — it is not part of the template.
- **Memos**: fold a status token inline where relevant (same StatusVocabulary.md tokens: `INVESTIGATING`, `PAUSED`, `DONE`, `UNDER_REVIEW`, `AWAITING`, `BLOCKED`, `CANCELED`) only when the memo is not yet complete. Omit entirely for memos written and completed in one session.

### Contents

`## Contents` section for docs longer than \~5 pages. Aids navigation and serves as a structural integrity check. Always titled **Contents**, never "Table of Contents".

- **Projects**: Required (usually auto-generated by markdown processor)
- **Incidents & Releases**: Optional (postmortems are often short; include only if substantial)
- **Memos**: Optional (point-in-time analyses are typically short)

### Tasks

A planning device — captures scoped work before it begins. Not a retroactive record of what happened.

- Rows describe **planned** work, not completed work
- Completed rows stay (scope record); remove only on cancellation (🚫)
- Status updated as work progresses

All task lists follow a consistent format:

#### Status Glyphs

**Only use glyphs from [StatusVocabulary.md](../../../docs/StatusVocabulary.md).** That is the canonical, single source of truth for all task statuses. Custom or similar-looking emoji (e.g. ⏳ hourglass, 🔍 magnifying glass) are not permitted — they cause ambiguity and agent confusion. If a glyph from StatusVocab doesn't fit your intended meaning, the meaning itself may need clarification (consult the Meaning column), or the task status needs rethinking.

**Blank Status cell = unstarted.** Never fill with a placeholder glyph. Absence of glyph IS the signal.

#### Format Rules

- **No space between glyph and date**: `✅03.14` not `✅ 03.14` so they don't line-break in tables
- **Dates in MM.DD format** (never DD.MM): `03.14` not `14.03` or `Mar 14` so they alphabetize
- **Glyph + date appear in Status column**, with detailed explanation in Notes column

#### Task Table Columns

Acceptable columns (not all required):

- **Task** — terse, permanent title/description designed not to change
- **LOE** — prior estimated person-days. Only for planning; remove after Jira tickets created. Never log effort after completion.
- **Jira** — **omit unless two or more tickets exist for this project.** When present: terse anchor text linked to ticket. Single-ticket projects have no Jira column — the project tracker belongs in Summary/Where Tracked, not duplicated in every task row.
- **Status** — glyph + MM.DD date
- **Notes** — detailed explanation, blockers, rationale

#### Task Discipline Rules

- **Never add a task and mark it complete in the same work session.** Work already finished when the task would be written belongs in the Work Log, not the task table.
- **Never backfill completed work into Tasks.** Completed rows stay in the table (useful record), but Tasks is forward-looking only. If work was completed before the task was planned, it belongs in Work Log.
- **Future work appears only in Tasks, Draft Next Comms, Pending Decisions, Pending Investigations, and TODOs.** No "Critical/Important/Urgent/Deprioritized" labels — use order. No capitalized exclamations (Bug, Gap, Pending, Next). No ⚠️ in task tables — see [Cross-References for Pending Work/Questions](#cross-references-for-pending-workquestions) for the ⚠️ antipattern rule.
- **On audit, sort the Tasks table itself using a three-tier group rule:** (1) completed rows sorted by date (oldest first), (2) ▶️ in-progress rows, (3) not-yet-started rows — **with no interleaving between groups.** Within in-progress and not-yet-started groups, **preserve insertion order.** Never invent a secondary sort key (alphabetical, date, priority labels) within these groups. Position reflects priority and readability, not a signal of dependency.

#### Task Dependencies

**Row order is the primary signal for dependencies.** In a well-ordered Tasks table, each task depends on the immediately preceding one by default. This is the normal case: no marker needed.

**⬆️ DEPENDS_ON marks exceptions only: non-adjacent dependencies.** If a task depends on a task that is NOT immediately before it in the table, use the `⬆️ DEPENDS_ON` marker. This keeps non-obvious dependencies explicit while reducing noise on linear chains.

**Row order must respect all dependencies** (adjacent or non-adjacent): A task may never appear before its prerequisites in the table.

**⚠️ Agent rule:** Scan a task table top-to-bottom. By default, assume each task depends on the one directly above it. If a `⬆️` marker appears, it signals a non-adjacent dependency to an earlier row — follow the marker to find the actual prerequisite. Do not infer dependencies from row order when a marker is present; the marker overrides row order for that task.

**Task title durability & bolding:** Task titles serve as stable reference targets for dependencies. Choose titles that are:

- Self-contained (omit project/repo prefixes that would be redundant when referenced)
- Durable (unlikely to be rephrased; title changes break references)
- Meaningful (first ≤5 words should make the reference unambiguous)

For example, "Create new AD group" is better than "variant-group-shell: create new AD group" — omit the repo prefix since it's not needed in a reference within the same doc, and use the first few words as the stable target.

**Bold task titles only if they are dependencies for later tasks.** If a task title appears as a `⬆️ DEPENDS_ON` reference in any later task's Notes cell, bold the title in the Task column. If a task has no downstream dependencies, leave it unbolded (normal text). This visual convention signals at a glance which tasks are reference targets and which are leaf nodes.

**Marker rules:**

- If a task has one or more direct dependencies on prior tasks in the same table, the Notes cell **must start with** the marker followed by a **bold reference** to the first ≤5 words of the target task's title:
  ```
  ⬆️ **Create new AD group**. Do not submit until...
  ⬆️ **Create new AD group**, **Complete SailPoint integration**. Blocked on both...
  ```
- The referenced task title in the dependency marker should also be **bold** in the Tasks table, so readers can visually link the reference to the source row.
- List only direct dependencies; indirect dependencies remain implicit (i.e., if A→B→C and both B and C explicitly mark their immediate prerequisites, the chain is clear).
- The marker is not a status — it is a relationship signal (see [StatusVocabulary.md § Task Relationship Markers](../../../docs/StatusVocabulary.md#task-relationship-markers)).
- **Row order must respect dependencies:** If A→B (B depends on A), then A must appear before B in the table. But if C appears before B, C may or may not be a prerequisite of B — that relationship is declared only by the marker, never inferred from position.

**Example — linear chain (no markers needed):**

```markdown
| Task | Status | Notes |
| --- | --- | --- |
| **Create new AD group** | 🛑08.14 | Blocked on ServiceNow ticket...
| **Register GitHub App** | | Must use group name in GARS request... (implicitly depends on Create new AD group) |
| **Complete SailPoint integration** | | Do not submit until GitHub registration complete... (implicitly depends on Register GitHub App) |
```

(No `⬆️` markers needed; each task depends on the one directly above it.)

**Example — non-adjacent dependency (marker required):**

```markdown
| Task | Status | Notes |
| --- | --- | --- |
| **Create new AD group** | 🛑08.14 | Blocked on ServiceNow ticket...
| **Check org webhooks** | 👀08.11 | Org-level check (no dependency on AD group)... |
| **Register GitHub App** | | ⬆️ **Create new AD group**. Must use group name in GARS request... |
| **Complete SailPoint integration** | | Follows Register GitHub App (implicitly) |
```

(Register GitHub App depends on Create new AD group, which is 2 rows back — marker required. Check org webhooks is independent and can appear anywhere. Complete SailPoint integration depends on the immediately preceding Register GitHub App — no marker needed.)

In this example, "Check org webhooks" comes after the AD group task but does not depend on it — the bold `⬆️` references on the other two tasks make their prerequisites explicit and linkable. The table is ordered for readability and to respect declared dependencies, but position alone never implies a prerequisite relationship.

**Glyph: `⬆️` (up arrow).** Literal and intuitive in top-to-bottom reading order: "the task above" → must complete first. The priority is that the reference is **bold** and matches the source task title exactly so readers can click/search to find the prerequisite.

**English form (timeline/review tables):** When a table explicitly opts out of ⬆️ markers (declared via an agent note above the table), express dependencies at the start of the Notes cell as:

```
**Depends on:** **Task Title A**, **Task Title B**.
```

"Depends on:" label and all task titles are bold; titles are comma-separated; period closes the dependency declaration before the rest of the note. "Blocked by" is reserved for tasks whose Status cell carries a 🛑 or ❓ glyph — do not use it as a synonym for a task dependency.

### Active Work

Mutable working state for in-progress items. Answers: "What are we doing right now?"

**Scope & Organization:**

- **ALL and only ▶️ (in-progress) tasks get a subsection here** — one `###` heading per task. No more, no fewer. If a task is in-progress, it has a section; if a task is not in-progress, it has no section.
- **Active Work heading must match (be verbatim or a prefix of) the task title** — the `###` heading slug must resolve to the task title when linked. Examples:
  - Task: `**Check repo settings**` → Active Work: `### Check repo settings` ✅
  - Task: `**Check repo settings** for webhooks` → Active Work: `### Check repo settings` (prefix) ✅
  - Task: `**Check repo settings** for webhooks` → Active Work: `### Webhook audit` (mismatch) ❌
  - This makes task-title anchors stable and enables direct linking from Tasks table to Active Work subsections.
- **Order matches Tasks table order** — subsections appear in the same sequence as their corresponding ▶️ rows in the Tasks table, so readers can navigate between them.
- **Task titles in Tasks table should link to Active Work** — when a task title is in progress, make the entire title a link to its Active Work subsection: `[**Task Title**](#task-title)`. This enables one-click navigation from planning to execution state.

**Why task titles must be TERSE and DURABLE:**

- Task titles serve as **anchor identifiers** — they are the only stable reference point between Tasks table and Active Work. Changing a task title after work begins breaks all existing links and makes it impossible to find the corresponding Active Work subsection.
- **TERSE** — keep titles to ≤5 words if possible; use bold for clarity. No narrative context or qualifiers (dates, statuses, decision rationale) belong in the title.
- **DURABLE** — once a task title is published, treat it as immutable for the lifetime of the doc session. If you need to add detail, context, or status updates, put them in Notes (Tasks table) or in the Active Work subsection body — never in the title.
- **When in doubt, Notes not title** — if you're tempted to qualify or expand the title (e.g., "Review [X] before doing [Y]"), that content belongs in the Notes column, not in the title. The title is the label; Notes carry the conditions/context.

**Content Rules:**

- Contains subtasks, blockers, partial results, dependencies for the in-progress work
- Next agent or human picks up here after an interruption
- Strictly organized by `###` heading per ▶️ task — one section per task, no free-form prose at the top level
- **DRY with Tasks** — no information here that is not grounded in a ▶️ task row. If you find yourself writing subtasks for work that has no corresponding ▶️ task, add the task first

**Completion & Archival:**

- **Concluded work moves to Work Log, never to Active Work.** When a ▶️ task completes, clear its subtasks from here and add one terse Work Log entry summarizing what was decided/discovered
- **Completed work in Active Work is a violation.** Do not mark tasks as "DONE" in Active Work or leave past-tense status updates here. The moment a task is no longer in-progress, remove its section entirely
- **Once cleared, a completed task has no Active Work subsection** — all its detail lives in the Work Log entry for that session

### Next Daily Jira Update

**Include only when the doc has a Jira ticket** in Summary → Where Tracked — required for projects (nearly always ticketed), optional/rare for incidents (most are Slack-only), N/A for memos (no recurring cadence or ticket). Delete the heading entirely when there's no ticket to post to.

A standing, terse, bullet-heavy draft sized to paste directly as a Jira comment — never prose. Three fixed sub-bullets:

- **Done today** — one bullet per logical change/finding this session
- **Status** — current state in one line (on-track / at-risk / blocked / investigating / resolved, and why)
- **Next** — the next 1–3 concrete steps

End the draft with a blank line and the universal italicized provenance line: `*Powered by {Model} in {Harness} in {IDE} via {skill-or-command}*`. Use compact model names such as `GPT5.6`, not `GPT-5.6`, in all Powered-by signatures; apply prospectively without backfilling existing signatures. Select and link the skill or command using [Drafting Comms](#drafting-comms)' provenance rule. Use native italics in the destination, or the same plain-text line where italics are unavailable.

**Key distinction from Draft Next Comms: this section is overwritten, never deleted.** Draft Next Comms holds one-off outbound messages that vanish once sent. Next Daily Jira Update is a recurring cadence artifact — today's bullets replace yesterday's the moment they're posted (prefix per team convention, e.g. `MM.DD.Dow:`), and the section stays in the doc ready for tomorrow's update. Only delete it once the ticket itself closes or the daily-update cadence stops. The Work Log remains the permanent, cumulative history — this section is a disposable cache of "what would I post right now," derived from Tasks/Active Work/Work Log, never a source of new facts. See [git2jira](../git2jira/SKILL.md) for auto-generating these bullets from git history.

### Draft Next Comms

Holds only unsent outbound communication drafts. For formatting, provenance, evidence, approval, and send lifecycle rules, use [Drafting Comms](#drafting-comms). A sent draft is removed from this section and recorded once in Work Log with destination and message URL. Workflow-specific additions belong in the owning workflow, not here.

### Diagnosis

**Incident docs only.** Structured record of the investigation's epistemic state regarding causation. Two subsections:

- **Differential Diagnosis** — ranked table of candidate causes (Theory | P% | Status). P% is a betting odd on the theory being a significant contributor; need not sum to 100%. Ordered highest probability first; reordering is a claim that must be justifiable from the Work Log. Status glyphs: ▶️ Active · ⏭️ Queued · ✅ Ruled out. Ruled-out rows stay in the table as a record of losing bets — do not delete; log the reasoning in Work Log. P% on ruled-out rows stays at its last active value: the historical weight is informative. *(Exception to the prose falsified-hypothesis deletion rule in [Temporal Writing Rules](#temporal-writing-rules): that rule applies to narrative prose, not to Differential Diagnosis table rows, which are a structured record.)*
- **Cause** — withheld from the template; add only when a theory is Leading: tested against named alternatives with none falsifying it. Never create speculatively. Distinguish the proximate trigger (immediate cause) from the systemic root cause (underlying condition). Use "supported by" followed by a linked neutral [evidence glyph](#evidence) for each supporting claim and "leading" to characterize the overall theory. When written, update Status to `🎯 DIAGNOSED`. See [IncidentRCA.md](../../../docs/IncidentRCA.md#counterfactual-analysis) for the counterfactual methodology.

*Note: Pending investigative threads belong in the top-level [Pending Investigations](#pending-investigations) section, not here. Diagnosis is for the epistemic state of causation (what could cause this?), while Pending Investigations captures what we don't yet know (what can we answer ourselves?).*

Ruled-out theories never reach Decisions — their closure path is the Work Log (how they were eliminated) and the Differential Diagnosis table (their P% and ✅ status preserved as record). Decisions is for team choices only.

### Evidence

**Required in all project, incident, release, and memo docs.** Every verifiable empirical claim must cite its source.

**Placement:** Dedicated `## Evidence` section near the bottom, above Work Log.

**Inline evidence citations:** Choose a neutral decorative Unicode glyph (for example ❀, ✿, ❁ or ✧) for each unique evidence target in the document. The glyph identifies a source only; it must not imply a problem, question, warning, uncertainty, priority, approval, or task status. Do not use symbols such as ⚠️, ❗, ❓, 🔍, 🔔, ✅ or ❌ as citation markers. Append its linked glyph to the end of the supported claim, with no intervening space: `claim text[❀](#e-descriptive-slug)`. Never put the glyph at the start of a bullet or claim. Evidence-first prose states the evidence before the proposed action; its citation still follows the evidence claim.

Append the same plain glyph to the end of the target evidence heading: `### Brief evidence description ❀`. Keep the explicit descriptive anchor stable. Repeated citations to that target reuse its glyph; different targets in the same document must have different glyphs, even across sections or tables. Do not use daggers, numbered markers, or task-status glyphs for evidence citations.

Example: "Latency dropped 40%[❀](#e-latency-drop)." targets `### Latency measurement ❀` with anchor `e-latency-drop`.

**Entry structure** — each entry is a `###` heading:

```
### Brief description of what is being evidenced ❀

<a id="e-descriptive-slug"></a>

- **Claim**: the specific assertion being backed
- **Source**: URL, file path, git commit SHA, dashboard name, or person name + role
- **Dates**: source vintage (when authored/published) and collection date (YYYY.MM.DD.Dow, when retrieved)
- **Quote / data**: exact text excerpt, metric value, or command output
```

Omit any field that genuinely doesn't apply; include as many as possible.

**Additional rules:**

- **Audit citations:** verify one-to-one glyph/target mapping, claim-suffix placement, matching heading-suffix glyphs, and valid stable anchors throughout the document.
- **Unsourced claims:** label "Inference:" or "Unverified:" until evidenced
- **Perishable data** (stats, counts, latency, costs, queue depths): add vintage parenthetical:

  ```
  claim text[(2025)](#e-slug)         — annual figures
  claim text[(2025.03)](#e-slug)      — monthly figures
  claim text[(2025.03.14)](#e-slug)   — daily figures
  ```

  Granularity matches shelf life: annual for slow data, daily for fast-moving data.
- **Citing dated sources** (incident, analysis, ADR): put the date *after* the verb:

  `Rohith cataloged ([2025.09](#e-bv-sync-issue)) 5 manifestations` — not `Rohith (Sep 2025) cataloged...`
- **Log search queries must be copy-pasteable and clickable.** When an evidence entry cites an OLS query, Grafana query, Splunk search, or any log-search platform:

  1. The **Source** field must link to the platform: `[OLS prod](https://scf.logs.prod.walmart.com)` or `[OLS nonprod](https://openlogsearch.logs.nonprod.walmart.com)`, not bare text like `OLS prod (scf.logs.prod.walmart.com)`.
  2. SQL/query strings must be **complete and copy-pasteable** — no ellipsis (`…`, `...`), no `WHERE ...`, no truncated clauses. The reader should be able to copy the query verbatim into the platform and get results. Include the full `WHERE` clause with all filter predicates (namespace, labels, message patterns).
  3. If a query repeats a common WHERE prefix from an earlier entry, **repeat it in full** — do not abbreviate as "same stream" or "same filters." Each query stands alone.
  4. Prose quotes of log output or exception messages may use `…` to abbreviate — the rule applies only to queries the reader would execute.

### Work Log

**Required in all project, incident, release, and memo docs except `*Testing.md` evidence records.** Audit trail of effort — what we spent time on, what the problems were, how we moved closer to the goal. Git commits describe *what* changed; the Work Log describes *how* we got there. `*Testing.md` is a frozen PDF payload and must never contain a Work Log.

- Records decisions, discoveries, costs incurred, obstacles overcome
- Provides context for why code looks the way it does
- Built incrementally — one entry every \~30 minutes during active work
- Concluded items from Active Work are recorded here, then cleared from Active Work

**Format:**

```
### 03.16 Sun Refactored cache layer

- **14:32:** Pulled PR #582, found race condition in auth middleware lock ordering
- **15:02:** Added mutex lock to fix race; unit tests updated and passing
- **15:32:** Ran full test suite; 2 flaky timeouts (unrelated), otherwise green
- **16:01:** Created PR #589 for review; ready for STG tomorrow
```

Heading: `### MM.DD Dow Title of The Day's Work` (prefix YYYY at year boundaries: `### 2026.03.16 Sun ...`)

Entry: `- **HH:MM:** Entry text`

#### Timestamp Collection Rules — DO NOT ESTIMATE TIMES

**Critical:** Agents are catastrophically bad at estimating elapsed time. Never guess or estimate. Always collect actual system time. Record timestamps as they occur, or if recording retroactively, consult `date` or git history for bounds.

- **As work happens:** Run `date "+%H:%M"` when completing a unit of work and immediately record the timestamp. The actual system time is the source of truth.
- **Recording past work retroactively:** If you're writing an entry for work that completed some time ago, use the "bef." prefix to indicate the timestamp is earlier than the current system time, e.g. `- **bef.14:32:** Refactored cache layer (completed earlier today; timestamp estimated from commit time)`.
- **Use git history to bound timestamps:** If you have a unit of work that spans multiple commits, the commit times in `git log --oneline --date=short --format="%h %ad %s"` provide the tightest bounds. Use the latest commit time for that work unit.
- **Example of retroactive entry with git evidence:**
  ```
  - **bef.15:47:** Added mutex lock to fix race condition (commit 8f2a3c9 at 15:47)
  ```
- **Never estimate duration or time deltas.** "~15 minutes" or "about 20 mins" is an anti-pattern. Use `date` to get the actual time, or use `bef.HH:MM` if retroactive.

**For incidents specifically:** Write entries in real time, not retroactively — before switching contexts, after each significant finding. Use `date "+%H:%M"` immediately after each finding to capture the actual clock time. Minimum required entries: when the incident opens (symptom, scope, first data inspected); when each major hypothesis is formed or ruled out; when root cause is confirmed or unresolved; when the doc is committed. **If auditing an incident with no Work Log:** flag as a critical gap; reconstruct what you can from git history and commit messages — note `(reconstructed from git; original timestamps unavailable)` if you do.

## Drafting Comms

Apply to outbound messages and ready-to-send drafts, including Draft Next Comms. Minimize the recipient's effort to understand, verify, and act. Follow Compose → Substantiate → Verify → Maintain; approval to draft is not approval to send.

### Compose

- **Ask the fewest, easiest questions.** Lead with the root question whose answer decides the rest. Drop questions another answer settles, or that we can answer ourselves; defer later-stage asks until their stage. For each likely answer, state what we will do so the recipient can reply in one line.
- **Lead with the ask or finding.** Name the recipient and requested action; include only context needed to answer or act. Distinguish observations from hypotheses and questions; do not present an inference as an established diagnosis.
- **Audience-aware context.** When invoking a procedure, rule, contract, form, or ownership boundary, link the relevant canonical instruction and identify the specific gap or decision. Assume recipients know their system; explain only what they need to respond. Prefer a short linked phrase over a tutorial: “The [onboarding guide](url) covers X; does it also apply to Y?”
- **Ownership and action.** For cross-team requests, name the specific system/team and link its applicable support route to inspected ownership instructions, not an umbrella organization. Link recommendations to the exact tool record or form where the recipient acts. When proposing a non-Slack support route, also link the most relevant verified Slack alternative and explain the choice; never invent channels or imply Slack is unsupported without evidence.
- **Link presentation.** Link every named Walmart tool/platform. Use descriptive Markdown links, not bare URLs; identify the relevant field, row, or instruction in the label when relevance is non-obvious. Convert links to the destination's native format when sending. For catalog entities, follow [Catalog Entity Presentation](#catalog-entity-presentation).

### Substantiate

Every distinct empirical or diagnostic clause needs inline primary evidence. Use one of these verification paths:

- **Direct result:** Link the exact record or result showing the claimed entity/data, preserving filters and time range. Open it cold: the claimed data must be visible without reconstructing the investigation. A landing page alone, unrelated Slack discussion, unfiltered live stream, or internal evidence-glyph/footnote anchor does not qualify.
- **Reproduction recipe:** If no direct result permalink exists, link the tool and give the complete copy-pasteable query or exact click-path in the same sentence. Include the entity, filters, environment, and time range needed to reproduce the observation. Do not offer “query available on request” or spend prose explaining why a permalink is unavailable. This path permits a tool-entry link only when paired with the recipe; it does not permit agents to bypass access or execution restrictions.

**Source versus interpretation:** Our incident docs, memos, SQL files, and analyses do not independently establish the operational facts they describe. Cite the underlying primary records instead. A code commit can establish code behavior; a canonical rule can establish policy, regardless of authorship. Neither alone proves live operational state. Include an owning project/incident link once at the end for context when useful or required, never as substitute evidence.

Illustrative wording, not a verified finding:

- **Good:** “In [Lenses SQL Studio](url), run `SELECT * FROM example_topic WHERE _key = 'example-key' AND event_time >= '2026-10-22T14:00:00Z' AND event_time < '2026-10-22T15:00:00Z'` on the named cluster to inspect the matching events.” Actual drafts must use a verified URL, cluster, schema, and executable query.
- **Bad:** “The [topic browser](url) confirms duplicate processing; query available on request.” A live stream without the matching records/filter neither establishes the claim nor lets the recipient reproduce it.

### Verify

- **Inspect every unique destination through [safe-browse](../../commands/safe-browse.md) before finalizing.** Open the fully loaded human-visible page, including evidence, quoted comments, context, manuals, support routes, catalog glyphs, and provenance links. HTTP status, backend responses, and another agent's assurance do not count.
- **Apply the matching gate.** Direct evidence must visibly show the claimed records and scope. Recipe links must open the named tool, and the recipe must reproduce the observation; where execution is reserved to the user, obtain their result rather than running it yourself. Context/action links must visibly identify the relevant instruction or destination. Check redirects, filters, anchors, and channel/form names. Replace or remove failed links and recheck changed URLs.
- **Record verification outside the paste-ready body.** Record inspected destinations and what they establish, plus any remaining blockers. An uninspected or blocked link prevents claiming verification complete; follow the applicable auth/blocking workflow rather than silently weakening the claim.
- **Sign and obtain approval.** Follow [Communication Signing](https://github.com/BrianHoltz/tools/blob/main/docs/AgentRules.md#communication-signing) for provenance discovery, required versions, formatting, and publication gates. Use triage when that command is in play; otherwise name/link the responsible workflow, omit `via` when none applies, and never name doc-audit. Get explicit user approval before sending to other humans.

**Final check:** Clear ask; audience-appropriate context; every factual clause supported; every destination inspected; recipes complete; applicable owner/action/entity rules satisfied; provenance valid; send approval obtained before transmission. If a check fails, fix it or report the specific blocker outside the draft.

### Maintain

- **Unsent drafts only.** In Draft Next Comms, use a plain `###` heading naming the target, followed immediately by the paste-ready body, never a blockquote. Omit status labels, approval reminders, editorial comments, and lead-ins.
- **Blocked tasks:** When a task awaits a reply, its Notes link to the draft and the draft names the blocked task.
- **After sending:** Remove the draft entirely and add one Work Log entry with destination and message permalink or Slack `ts`. For the recurring [Next Daily Jira Update](#next-daily-jira-update), overwrite the draft for the next cadence instead of deleting its section.

## Rules About Pending Work

### Tasks Pipeline

Tasks flow through the document deterministically: Tasks → Active Work → Work Log.

- **Tasks ↔ Active Work**: Active Work subtasks relate only to ▶️ tasks; once ▶️ tasks complete, details move to Work Log
- **Active Work ↔ Work Log**: Concluded items are cleared from Active Work (not duplicated)
- **Tasks**: kept sorted (done → in-progress → not-started) so readers can scan for current status directly; Status section is omitted in projects

### Where Pending Work Lives

- **Tasks** — planned work with defined scope; search here when deciding what to do next
- **Active Work** — in-progress subtasks/blockers; search here when resuming an interrupted session
- **TODO** — low-priority work items that block no other work; can be used as code/doc comments. If it blocks something, it's a Task. TODOs are never links.

### Where Pending Questions Live

**External Queries:**

- **Draft Next Comms** — unsent communications waiting to be sent to other teams or stakeholders. Queries we depend on other teams to answer. If blocked Task is waiting for the response, the blocked task and draft must name each other — see [Cross-References for Pending Work/Questions](#cross-references-for-pending-workquestions).

**Team Decisions:**

- **Pending Decisions** — unresolved choices your team must make. "Should we do X?" or "Which approach?" If resolving requires doing something, that doing is a Task; the decision stays here until answered. If a question turns out to need external input, *convert* it: remove it from here, create a Draft Next Comms entry, and mark any blocking Task 🛑. Never leave the question in both places. Every Pending Decision that blocks a Task must have a corresponding ▶️ (or 🛑) row in the Tasks table. Closed by moving to Decisions section — never delete.

**Empirical Investigations:**

- **Pending Investigations** — empirical unknowns *we can answer ourselves*. Record specific, named questions about state, metrics, or facts. You control the investigation through logs, testing, measurement, or analysis. Minor clarifications from other teams are fine; the core work is ours. Minor questions within an investigation don't demote it to Draft Comms — but if *they* control the outcome and you're waiting for their decision, it's Draft Comms instead. When completed: findings are absorbed into doc edits (Task notes, Context, Evidence, Work Log), or archived in [Resolved Investigations](#resolved-investigations) if they have no natural home elsewhere.
- **Resolved Investigations** — completed investigations whose findings have no natural home in Interfaces, Engineering Considerations, Task notes, or Work Log. Archive only insights that are important to preserve but do not fit the narrative. Subject to distillation — findings that belong in the body should be absorbed there instead, and this archive entry omitted.

**Inline Placeholders:**

- **TBD** — placeholder for unknown value or fact; use inline where the value will live. "Latency budget: TBD", "Customer impact: TBD". TBDs are never links.

### Cross-References for Pending Work/Questions

When pending work or questions are *mentioned* outside their canonical sections, they must link back to that section. This prevents invisible dead-ends where a problem is flagged but the reader has no path to the owning entry.

**Antipattern — lone ⚠️ is forbidden:**
A ⚠️ glyph used in a table cell, heading, or prose WITHOUT a link to a canonical pending entry is an explicit antipattern and must be fixed on audit. The glyph signals a problem; the link points to where it is being tracked. The same rule applies to other problem glyphs (❗, 🔔) used as out-of-section signals.

**Standard inline reference forms:**


| What you're referencing | Inline form                                                     |
| ----------------------- | --------------------------------------------------------------- |
| In-progress Task        | `▶️ Task: [task name](#tasks)`                                |
| Blocked Task            | `🛑 Task: [task name](#tasks)`                                  |
| Pending Decision        | `❓ Decision: [question summary](#pending-decisions)`           |
| Pending Investigation   | `🔍 Investigation: [question summary](#pending-investigations)` |
| Draft Next Comms item   | `📤 Draft: [draft heading](#draft-next-comms)`                  |
| Inline TODO             | write `TODO` inline — no link (TODOs are never linked)         |

## Doc-audit interview

Invoke with “doc-audit interview [document]” to audit first, then agree cleanups interactively—not rewrite first and request approval afterward.

- Read the document deeply and skeptically under the [governing rule](#governing-rule). Verify current-behavior claims against their authoritative sources; distinguish stale claims from unimplemented intentions.
- Give a short prioritized queue: misleading current truth first, then obsolete narrative, duplication, and overlapping future plans. Organize by named, cohesive cleanup—not line order or arbitrary size targets.
- Present one proposal at a time: **Change** (what and why), **Scope** (affected sections and what stays), one short verbatim **Worst passage**, and **Uncertainties** (specific sub-cleanups needing judgment). Recommend a disposition for each uncertainty; do not manufacture questions.
- End with one decision request: apply, adjust, or keep? Wait before editing that proposal. Do not ask the user to redesign the document or approve an opaque whole-document rewrite.
- Apply the answer precisely; preserve unresolved ideas and deliberate edits. A shipped feature does not automatically obsolete a similarly named future proposal. Clarify consequential ambiguity before deleting it.
- Re-read immediately before writing and follow the host’s write/coordination rules. Validate links, headings, vocabulary, and factual consistency; commit the approved cohesive pass separately when authorized. Then give a terse outcome and present the next proposal.
- Adapt to answers: carry forward stated preferences and settled distinctions. “Apply this and show the next” authorizes that proposal, not the entire queue; “do all these cleanups” covers the presented batch, not unrelated future deletions. Do not repeatedly re-ask settled questions.
- Keep judgment with the user, mechanics with the agent. Recommend deletion/linking rather than relocating clutter or narrating the cleanup. Preserve recoverability through clear commit messages, not in-document tombstones without reader value.
- When finished, summarize remaining decisions and verification gaps. Keep the interview in chat; the document contains only the resulting current truth and useful future paths.

**Proposal shape:** “Change: … Scope: … Worst passage: ‘…’ Uncertainties: … Recommendation: … Apply this pass?” Omit empty uncertainty sections.

## Doc Audit Checklist

Run in full on every non-trivial edit. All items apply; domain-knowledge items require cross-referencing with production state.

- ✅ TOC matches actual headings
- ✅ No orphaned sections (all sections referenced in TOC or prior section)
- ✅ All links resolve (no broken anchors, no dead URLs)
- ✅ No links from tracked files to untracked files (aidocs/, tmp/, etc.)
- ✅ For docs with Confluence mirrors: no relative links (they work in markdown/GHE but break in Confluence)
- ✅ **Mortal docs (projects, incidents, releases, memos) have their required sections**
- ✅ **For mortal docs with a Tasks table:**
  - Tasks table is sorted done → in-progress → not-started, preserving each group's existing relative order (see [Task Discipline Rules](#task-discipline-rules)). A well-sorted Tasks table IS the status display — Status sections are omitted in projects.
  - Active Work sections match in-progress tasks exactly: one `###` subsection per ▶️ task (no more, no fewer), in the same order as the Tasks table
  - **Active Work heading matches task title exactly or is a verbatim prefix** — if task is `**Foo bar baz qux**`, then Active Work heading is `### Foo bar baz qux` or `### Foo bar baz` (prefix), never `### Baz qux foo` (reordered) or `### Foo's bar activity` (paraphrased). Task title anchors must be stable and resolvable.
  - Task titles that are ▶️ in-progress have an anchor link to their Active Work subsection: `[**Task Title**](#task-title)`
  - Active Work contains only current, mutable state; no completed work descriptions or past-tense status updates
  - Concluded items are cleared from Active Work, moved to Work Log (not duplicated)
  - Current conversation's work is accurately timestamped in Work Log
- ✅ Endpoints exist and are correct
- ✅ Schemas are current
- ✅ Kafka topics match production
- ✅ CCM keys match production configuration
- ✅ Code citations reflect current codebase
- ✅ URLs are reachable and current
- ✅ Every acronym expansion is either (a) footnoted with an evidence link (file path, doc URL, code reference) or (b) hyperlinked directly to its canonical page. Unexpanded acronyms are acceptable; confidently wrong expansions are not. If no source exists, use the acronym without expansion.
- ✅ If the team has a vocabulary guide, audit for compliance.

### Task Creep Audit

Forensic check that the Tasks table has not been used as a work log (invoked on demand, not every session). Requires checking git history (`git log -p` on Tasks section) for violations:

- ✅ Rows added and marked ✅ in same commit or same day's commits
- ✅ Rows backfilled after work completed (added with status already set)
- ✅ Tasks describing work that happened (not work that was scoped)

**Remediation**: Move violating task content to Work Log entries. Keep the task row only if work was genuinely planned in advance; otherwise delete it.

### Active Work Hygiene Audit

Forensic check that Active Work contains only current in-progress state (invoked on demand during doc review, or when a ▶️ task completes). Red flags:

- ❌ **Heading mismatch with task title** — Active Work heading must be verbatim (or a prefix of) the corresponding task title. If task is `**Create new AD group**` but Active Work heading is `### AD group setup (blocked)`, fix the heading to match the task. This preserves anchor stability so task-table links don't break.
- ❌ **Completed work described in past tense** — "we fixed X", "findings from yesterday", "issue was resolved" belong in Work Log, not Active Work
- ❌ **Sections for non-▶️ tasks** — if a task is ✅/🎯/🛑/etc., it has no business in Active Work; its content belongs in Work Log or Evidence
- ❌ **Missing sections for ▶️ tasks** — every in-progress task must have a corresponding subsection; if one is missing, add it immediately
- ❌ **Out-of-order sections** — Active Work subsections should mirror Tasks table order; reorder them if Tasks table order changes
- ❌ **Free-form narrative at top level** — all Active Work prose should live under a `###` task-specific heading, never as section-level intro text

**Remediation**: For each violation, remove the violating content from Active Work and place it in Work Log (with a session timestamp). Completed task sections should be deleted entirely, not repurposed or archived. For heading mismatches, rename the `###` heading to match the task title exactly.

### When to Audit

- Full checklist: every non-trivial edit.
- Task Creep audit: on demand.

### What to Audit

- Any doc with any of the standard pre-defined sections
- But never any ephemeral ad hoc docs e.g. under `aidocs/` or `tmp/`

## See Also

If this repo uses the Agent Toolkit (i.e. has a toplevel `shared` symlink), then see:

- [AGENTS.md](../../../AGENTS.md) — agent contract, entry points, doc placement rules
- [WibeyProjectMgt.md](../../../docs/WibeyProjectMgt.md) — rationale for the toolkit and project structure (marketing/adoption doc)
- [Project.md](../../../docs/templates/Project.md) — template and inline guidance for new project docs

## Temporal Writing Rules

All prose in non-ephemeral docs (both mortal and immortal) must read as timeless — durable observations, not corrections of earlier drafts. Exceptions:

- Work Log of course is narrative
- Memos are often narrative or make temporal references

### Timeless Perspective

Every sentence should seem as if it were always there. If a sentence only makes sense to someone who read a previous version of the document, it's narrative, not analysis. Narrative belongs in git commits and Work Log. Test every single sentence against this standard.

- **Expunge version-history debris.** When auditing, identify and delete any sentence that presupposes prior-version knowledge. Do not collapse, summarize, or label it — delete it. The reader has never seen earlier drafts and doesn't care what changed since them.
  - **Falsified hypotheses:** once a hypothesis is ruled out, remove it from the body entirely. Do not write "Hypothesis X was FALSIFIED" — that sentence only means something to someone who remembers when X was the hypothesis. Instead, state the current best understanding without mentioning what it replaced. Record the falsification path in the Work Log and git history, where it belongs.
  - **Investigation narrative:** phrases like "our earlier hypothesis", "we previously thought", "upon further investigation", "it turned out that", "we initially believed" are all narrative markers — they describe the journey, not the destination. Every reader begins at the current state; the journey is irrelevant to them.
  - **Status transitions:** avoid "now confirmed", "no longer unknown", "finally resolved" — these are only meaningful relative to a prior reading. Write the current state directly: "as of YYYY.MM.DD, cause established" not "cause is now confirmed."
- No Relative Temporal References in Non-Ephemeral Files
  - Use absolute dates, never relative ones. Exception: quotes of communications.
  - **Computed durations rot.** Never write "for 13 days", "17 days stale", "for 2 weeks" — these are correct only on the day written and mislead every subsequent reader. Write the date range instead: "04.07–04.17", "since 04.21". The reader can compute the duration; the doc cannot update itself.
- No Future Dates Unless Capturing a Commitment
  - Future work lives in task rows and TODOs only, never as prose promises.

## Content Brittleness

Keep docs maintainable and resilient to code changes.

- **Avoid redundancy with code.** Don't write comments that just repeat what the code says. Use comments for interfaces (e.g. JavaDoc) and non-obvious considerations.
- **Code should be self-documenting** through naming — avoid comments redundant with plain reading.
- **Never reference file line numbers** in tracked docs (exception: Evidence entries anchored to a specific commit SHA).
- **Never label things sequentially. Use names.** Sequential labels are opaque and brittle and lazy. **One narrow exception:** numbered steps in a table-format procedure where the steps are too short or parallel to name meaningfully — and even then, prefer names if you can find them.
- **Keep TOC in sync** with actual headings when you update the doc.
- **Never link to untracked files** from tracked files

## Ad Hoc Documents

Short-lived conversation artifacts that don't belong in permanent reference docs.

### Placement

- **With shared/ symlink**: Place in `shared/aidocs/yyyy-mm-dd/` (any repo, same location via symlink)
- **Without shared/ symlink**: Place in `<repo>/aidocs/yyyy-mm-dd/`
- Never create per-repo `aidocs/` folders in team setups; use the shared location

### Naming

Format: `hhmm_CamelCase.md` where `hhmm` is create time, not modification time.

If updating a doc created on an earlier date, move it into the current date folder and use modtime for `hhmm`.

### When to Create

- Use for analysis, investigation notes, or conversation artifacts
- Don't check into VCS
- Only create if the content is substantial (&gt;100 lines) or you're building incrementally
- Avoid creating multiple ad hoc docs at once — combine into a single TOC'd document to prevent WETness
- Never link to ad hoc docs from tracked files
- **After creating or updating an aidocs file, always open it** using `open -a "IntelliJ IDEA" <filepath>`

---

## Styling Discipline

Standardized formatting so agents and humans produce visually consistent docs.

For citations and explanatory footnotes in tables or prose, use the neutral linked glyphs and document-wide unique-target mapping in [Evidence](#evidence); no separate table-footnote glyph vocabulary applies. Problem or question signals belong to [pending-work references](#cross-references-for-pending-workquestions), not citation markers.

### Table Cell Vocabulary

Standard special values:

- **— (emdash)** — not applicable; the concept doesn't apply to this cell.
- **TBD** — value or fact is unknown and will be determined via investigation. Placeholder for pending empirical questions. Blocks nothing alone; work to investigate it may be a Task or Pending Investigation.
- **TODO** — work is needed to produce the value. Blocks nothing, blocked by nothing. Use for mini-tasks only.
- **?** — unknown whether the value can, should, or does exist
- **⚠️** — alarming situation; must link to a canonical pending entry (a Task row, Pending Decision, Pending Investigation, a Draft Next Comms item, or an inline TODO). A lone ⚠️ with no such link is a forbidden antipattern — see [Cross-References for Pending Work/Questions](#cross-references-for-pending-workquestions).
- **blank cell** — only for visual spacing/grouping (e.g. subheader rows). Otherwise use emdash, ?, or TBD.
- **^^^** — same link/value as the row above

### Escaping

- **Dollar signs in prose**: Escape as `\$` (IntelliJ treats `$...$` as inline LaTeX math, so two unescaped `$` in the same paragraph render the text between as italic math)
- **Dollar signs in table cells**: Safe (pipes prevent cross-cell pairing)

### Hyperlinks

Link the relevant text; don't parenthetically name the target.

- **Good**: `dates to at least [2014](#history)`
- **Bad**: `dates to at least 2014 (see [History](#history))` or `dates to at least 2014 ([evidence](#history))`

When mentioning a document by title, link the title itself — not a separate "link" word. Append `(yyyy)` or `(Mon yyyy)` after the title if the date provides context:

- **Good**: `the [Variant Detailed Design](url) (Jan 2025) specifies...`
- **Bad**: `the Variant Detailed Design page ([Jan 2025](url)) specifies...`

When citing a dated source (incident, analysis, ADR), put the parenthetical date *after* the action/verb:

- **Good**: `Rohith cataloged ([2025.09](#e-item)) 5 manifestations`
- **Bad**: `Rohith (Sep 2025) cataloged 5 manifestations`

### Mandatory Links

Every mention of the following must carry a hyperlink — no bare references. First-mention-per-doc is the minimum; re-link on first mention per section in long docs.

**Tickets and change records:**

- Jira ticket IDs (any key: CATGTRLSHP, OPIF, RCTMEXP, CQP, GM, STRCASS, RCTBVAR, …) — every mention — `https://jira.walmart.com/browse/TICKET-ID`
- CRQ / change request numbers (CHG-NNNNNNN) → `https://walmartglobal.service-now.com/nav_to.do?uri=change_request.do?number=CHGNNNNNNN`
- ServiceNow incidents (INC-NNNNNNN) → same ServiceNow base URL
- Jira board IDs (board NNN) → `https://jira.walmart.com/secure/RapidBoard.jspa?rapidView=NNN`

**Code and repos:**

- PRs (#NNN) — every mention — `https://gecgithub01.walmart.com/<org>/<repo>/pull/NNN`
- Git commit SHAs (first 7–8 chars) → `https://gecgithub01.walmart.com/<org>/<repo>/commit/SHA`. Always use commit SHA, not branch, for durability.
- GHE repo names (relationship-service, qarth-group-service, variant-grouping-stream, etc.) on first mention per doc → link to repo root
- GHE code file/line (specific file path or line range) → `https://gecgithub01.walmart.com/<org>/<repo>/blob/COMMIT_SHA/path/to/file.ext#L123-L456`. Always link via commit SHA (not branch) for durability. Line numbers are perishable; use only in Evidence entries or dated sources; avoid in timeless prose per [Content Brittleness](#content-brittleness).

**Catalog entities:**

- WPID, itemId, GTIN, SKU — every mention in analysis, diagnosis, or evidence — link to [Editorial](https://editorial.prod.walmart.com) by default, or [Atom](https://atom.prod.walmart.com) if in Atom-specific context
- offerId, feedId — every mention — link to [Atom](https://atom.prod.walmart.com) only

### Catalog Entity Presentation

On the first mention of a catalog entity in each section, use this compact treatment:

```markdown
`0ZAS081TRVPO` ([🛒](https://www-teflon.walmart.com/product/0ZAS081TRVPO) [📝](https://editorial.stg.walmart.com/pg_product_details/product/canonical/0ZAS081TRVPO?tenantId=0&locale=en_US) [⚛](https://atom.walmart.com/item-management/all-about-an-item?product_id=0ZAS081TRVPO) *Apple Services Promo 28*)
```

- Put the literal entity ID in monospace using backticks; do not bold it.
- Put the shopping page, Editorial, and Atom links, followed by the italicized title, inside one pair of parentheses immediately after the ID. Their link labels are exactly `🛒`, `📝`, and `⚛`; use `📝` and no other glyph for Editorial.
- Use the live Walmart.com item page or Teflon item page for `🛒`, the entity’s direct Editorial record for `📝`, and the entity’s direct Atom record for `⚛`. Omit a glyph only when that platform has no entity-specific URL; never substitute a landing page.
- Follow the links with the literal entity title, normally italicized, inside the same parentheses as the glyph links. Omit the title when space is genuinely constrained or no title is available.
- Apply the same treatment to WPIDs, item IDs, GTINs, SKUs, offer IDs, and other catalog entities, including offers. The ID determines the linked records; do not turn descriptive prose into the link label.
- After the full first mention, repeated mentions in the same section may use only the styled literal ID. A new section starts a new first-mention obligation.

**Slack:**

- Slack threads → `https://walmart.slack.com/archives/CHANNEL_ID/pTIMESTAMP`
- Slack channels (#channel-name) → `https://walmart.slack.com/archives/CHANNEL_ID`
- **Space after `#` in channel names** — write `# channel-name`, not `#channel-name`. Without the space, some markdown renderers treat `#word` at certain positions as a heading or anchor. The space defeats this. Applies in link text (`[# qarth-support](url)`), prose, and table cells.
- **No backticks inside link text** — write `[VENDOR_API](#vendor-api)`, not ``[`VENDOR_API`](#vendor-api)``. Backticks inside `[...]` produce nested inline code inside a hyperlink, which renders inconsistently across viewers and breaks some parsers.

**Confluence pages:**

- Any Confluence page cited by title → full `https://confluence.walmart.com/...` URL; look up the URL — do not guess or leave bare

**Walmart internal platform resources:**

- APM IDs (APM0019024) → `https://dx.walmart.com/services/APM_ID`
- SSP IDs (SSP00002947) → DX SSP page
- Named DX pages (DevOps Maturity Index, DX Cost, Kafka DX console, etc.) → direct URL
- TUNR/CCM config paths and service names → `https://admin.tunr.prod.walmart.com/services/<name>`
- Astra programs, suites, or flows cited by name or UUID → `https://astra.cloud.stg.walmart.com/...`
- OLS/Grafana dashboards or saved searches cited as sources → direct URL (also required by Evidence protocol)
- DX documentation pages → full `https://dx.walmart.com/...` URL

**External references:**

- Any cited standard, spec, or guide → canonical authoritative URL

**What does NOT need a link:**

- People's names (linking to Slack profiles is fine but not required)
- Kafka topic names (not linkable — include cluster context in prose instead)
- Feature flag / CCM key names (reference the config file path or CCM service; the key itself is not directly URL-addressable)
- Repeated back-references within the same paragraph

### Define Terms on First Use

Don't assume shared context — what's obvious to the writer is opaque to the reader and to any future agent. When there is any doubt a term is understood, define it on its first use in each context. Preferred order:

1. **Link to the canonical shared definition** in shared docs (e.g. `CatalogRelationships.md`, `CatalogIDs.md`, a `repos/*.md`). If our docs define it well — especially with their own links to authoritative references — link there rather than repeating the definition inline or in the current doc. A hyperlink on the term itself is sufficient. If the definition isn't there but should be, add it. Link the term everywhere it is used.
2. **Link to present doc's concepts/glossary**. If the definition doesn't warrant adding to our shared docs but is used multiple times in the current doc, define it in the doc's Concepts/Glossary and link it everywhere it is used.
3. **Inline definition** (parenthetical or em-dash) if no canonical source exists and the definition is brief and doesn't merit (or the doc lacks) a Concepts/Glossary section.

### Stylistic Restraint

- **Never include parenthetical comments in section headers.** `## Evidence (optional)` or `### Root Cause (Confirmed)` are both violations — parentheticals in headers corrupt search, anchor links, and any downstream tooling that parses headings. Put the qualification in the section body instead.
- **Never use text styles or parentheses inside section headings, ever.** No bold, italic, code spans, or link markup in a `#`/`##`/`###` heading line — headings are plain text only. This includes the `### [**Task Title**](#anchor)` pattern sometimes seen in Active Work: the heading itself must be plain (`### Task Title`); only the Tasks-table *cell* linking to that heading may use `[**Task Title**](#anchor)` markup. Rationale: markup and parentheticals inside a heading corrupt the anchor slug, break search, and confuse anchor-stability tooling that assumes headings are plain text.
- **Never insert hard newlines inside a markdown paragraph.** A paragraph is one unbroken line of text. Mid-paragraph newlines produce ragged source that wraps differently in every viewer and causes visual layout bugs in rendered output (e.g. a trailing code-span on a short wrapped line can render as a block). Write the full paragraph on one line; let the editor wrap visually.
- Avoid wasting space with horizontal rules — trust headings
- Never use all-caps for emphasis (only when quoting literal all-caps strings)
- Use bold/italics sparingly; bold is fine for list-item titles or table headers

## DRY Principles

### Rule Change Management

When a doc rule or template changes, **do not bulk-update all existing docs to match**. Bulk updates poison modification times, making it impossible to tell whether a doc was genuinely reviewed or just mechanically reformatted. Existing docs should migrate to new conventions organically — on their next substantive edit or audit.

Bulk-update only when the change is a correctness fix (broken links, wrong service names) or when the cost of stale format is higher than the cost of false mod-time recency. State the reason in the commit message.

### Banned Words and Phrases

Never use these. They are imprecise, imply unstated alternatives, or create confusion about certainty.

- **"root cause (confirmed):"** — if you're calling something root cause, you've confirmed it. Adding "(confirmed)" implies that sometimes you label something root cause without having confirmed it. Either it's root cause (say so directly) or it's a hypothesis or leading cause (say that instead).
- **"root cause (unconfirmed):"** — this is a hypothesis or leading cause. Call it that.
- **"(tentative)"**, **"(preliminary)"**, **"(working)"** as parenthetical qualifiers on section headers — put the qualification in prose inside the section.
- **"Note:"**, **"Important:"**, **"Warning:"** as standalone paragraph prefixes — use bold inline or a callout glyph (⚠️) where severity warrants it. These labels add no information beyond emphasis.
- **"As of [date]"** at the start of sentences — write the claim timelessly; if the date matters, cite it as evidence with a † link.
- **"currently"**, **"at this time"**, **"now"** in non-Work-Log prose — these rot immediately. Write the claim as a timeless fact or use absolute dates.
- **"deprioritized", "low/high priority", "urgent", "critical", "immediate"** as editorial labels on any task, item, or work — anywhere in the doc, not just Tasks tables. Priority is conveyed by position: order the list. If a decision to lower/raise priority happened at a point in time, record that fact once in Work Log; do not carry the adjective forward as a live status.
- **"executive summary"** — write "summary" instead. There are no executives here; the title is redundant. "Summary" is clear and sufficient.
