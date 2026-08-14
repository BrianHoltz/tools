# Doc Audit Skill

Consolidated reference for documentation authoring, project document formatting, and audit standards. Describes patterns for any repo: immortal (timeless) vs mortal (time-bound) docs, mortal doc structure, evidence, temporal writing, and consistency audits.

## Contents

- [Immortal vs Mortal Docs](#immortal-vs-mortal-docs) — timeless reference vs time-bound work docs
- [Mortal Doc Structure](#mortal-doc-structure) — sections, consistency, task tracking
  - [Summary](#summary)
  - [Status](#status)
  - [Contents](#contents-1)
  - [Tasks](#tasks)
    - [Status Glyphs](#status-glyphs)
    - [Format Rules](#format-rules)
    - [Task Table Columns](#task-table-columns)
    - [Task Discipline Rules](#task-discipline-rules)
  - [Active Work](#active-work)
  - [Draft Next Comms](#draft-next-comms)
  - [Diagnosis](#diagnosis)
  - [Evidence](#evidence)
  - [Work Log](#work-log)
- [Rules About Pending Work](#rules-about-pending-work)
  - [Tasks Pipeline](#tasks-pipeline)
  - [Where Pending Work Lives](#where-pending-work-lives)
  - [Where Pending Questions Live](#where-pending-questions-live)
  - [Cross-References for Pending Work/Questions](#cross-references-for-pending-workquestions)
- [Doc Audit Checklist](#doc-audit-checklist) — run on every non-trivial edit
  - [Task Creep Audit](#task-creep-audit)
  - [When to Audit](#when-to-audit)
  - [What to Audit](#what-to-audit)
- [Audit Date Format](#audit-date-format) — format and placement
- [See Also](#see-also)
- [Temporal Writing Rules](#temporal-writing-rules) — timeless perspective, absolute dates, no future prose
  - [Timeless Perspective](#timeless-perspective)
- [Content Brittleness](#content-brittleness) — sync with code, avoid line numbers, maintain TOC
- [Ad Hoc Documents](#ad-hoc-documents) — placement, naming, when to create
  - [Placement](#placement)
  - [Naming](#naming)
  - [When to Create](#when-to-create)
- [Styling Discipline](#styling-discipline) — footnotes, table cells, links, escaping
  - [Footnote Glyphs](#footnote-glyphs-in-tables)
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

## Mortal Doc Structure

Organize mortal docs with the following sections:

**● required, ○ optional, — not applicable:**


| Section          | Projects | Incidents, Releases | Memos |
| ---------------- | -------- | -------------------- | ----- |
| Summary          | ●       | ●                   | ●    |
| Status           | ●       | ●                   | ○    |
| Contents         | ●       | ○                   | ○    |
| References       | ●       | ○                   | ●    |
| Tasks            | ●       | ○                   | —    |
| Active Work      | ●       | ○                   | —    |
| Draft Next Comms    | ○       | ●                   | ○    |
| Pending Investigations | ○       | ●                   | ○    |
| Pending Decisions | ○       | ○                   | ○    |
| Decisions        | ○       | ○                   | ○    |
| Diagnosis           | —       | ●                   | —    |
| Evidence            | ●       | ●                   | ●    |
| Work Log         | ●       | ●                   | ○    |

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

Two variants depending on doc type:

- **Projects**: verbatim selection of rows from the Tasks table — the just-finished, current, and next tasks. Sits near the top for easy scanning. Always a Tasks excerpt, never prose.
- **Incidents**: a status token from [StatusVocabulary.md](../../../docs/StatusVocabulary.md), optionally qualified with an em-dash (e.g. `INVESTIGATING — root cause undiagnosed`). Updated each session.
- **Memos**: optional; use when the memo is not yet complete. Applicable tokens: `INVESTIGATING`, `PAUSED`, `DONE`, `UNDER_REVIEW`, `AWAITING`, `BLOCKED`, `CANCELED`. Omit the Status section entirely for memos written and completed in one session.

The following rules apply to the project variant:

- **Status rows are verbatim copies of Tasks rows** — never paraphrased or reworded. This includes the Status *cell*: copy only the glyph+date (or blank, for unstarted rows) that appears in the Tasks table. Never append extra links, annotations, or follow-up notes to the excerpt's Status cell that aren't in the source Tasks row — that content belongs in the Notes column, not bolted onto the glyph.
- Excerpt includes: all ▶️ in-progress tasks; completed tasks: all from the last 2 business days, plus enough older ones to reach exactly 2 total — no more; the next 2 upcoming tasks by priority
- **Not-yet-started rows have a blank Status cell — in both the Tasks table and the Status section.** Never fill with `⬜` or any other placeholder. Blank IS the correct status for work that has not yet entered its lifecycle. (Per [StatusVocabulary.md](../../../docs/StatusVocabulary.md): `⬜ UNSTARTED` is reserved for contexts where blank would be ambiguous, such as a mixed-use dashboard. Task tables are never that context.)
- **Sort order — group first, preserve order within group:** (1) completed rows, (2) ▶️ in-progress rows, (3) not-yet-started rows — in that order, with no interleaving. **Within each group, preserve the rows' existing relative order** (position already encodes priority per [Task Discipline Rules](#task-discipline-rules) — don't invent a secondary sort key like date). A resort operation must never reorder two rows that were already in the same group relative to each other.
- Update whenever Tasks change: new tasks, completions, blockers, phase transitions
- **Never backdate status changes** — reflect what is true now

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

See [StatusVocabulary.md](../../../docs/StatusVocabulary.md) for the canonical glyph-to-status mapping.

#### Format Rules

- **No space between glyph and date**: `✅03.14` not `✅ 03.14` so they don't line-break in tables
- **Dates in MM.DD format** (never DD.MM): `03.14` not `14.03` or `Mar 14` so they alphabetize
- **Glyph + date appear in Status column**, with detailed explanation in Notes column

#### Task Table Columns

Acceptable columns (not all required):

- **Task** — terse, permanent title/description designed not to change
- **LOE** — prior estimated person-days. Only for planning; remove after Jira tickets created. Never log effort after completion.
- **Jira** — only if &gt;1 ticket exist for this project; terse anchor text linked to ticket
- **Status** — glyph + MM.DD date
- **Notes** — detailed explanation, blockers, rationale

#### Task Discipline Rules

- **Never add a task and mark it complete in the same work session.** Work already finished when the task would be written belongs in the Work Log, not the task table.
- **Never backfill completed work into Tasks.** Completed rows stay in the table (useful record), but Tasks is forward-looking only. If work was completed before the task was planned, it belongs in Work Log.
- **Future work appears only in Tasks, Draft Next Comms, Pending Decisions, Pending Investigations, and TODOs.** No "Critical/Important/Urgent/Deprioritized" labels — use order. No capitalized exclamations (Bug, Gap, Pending, Next). No ⚠️ in task tables — see [Cross-References for Pending Work/Questions](#cross-references-for-pending-workquestions) for the ⚠️ antipattern rule.

### Active Work

Mutable working state for in-progress items. Answers: "What are we doing right now?"

- Reflects only ▶️ (in-progress) tasks
- Contains subtasks, blockers, partial results, dependencies
- Next agent or human picks up here after an interruption
- Cleared when subtasks complete — concluded items move to Work Log, never duplicated

### Draft Next Comms

Holds **only unsent** outbound communications (Slack replies, email drafts, PR comments). A draft that has been sent **must not appear here in any form** — not as a full message body, not as a compressed stub, not as a SENT status line.

- Each draft is a `###` sub-heading with target, status line (`Status: DRAFT` or `Status: READY`), and blockquoted message body
- **When a draft is sent: delete it from this section entirely.** Add one Work Log entry recording when and to whom it was sent (and the Slack `ts` or message URL if available). That is the complete record.
- **On audit: any entry with `Status: SENT` or any other indication it was sent is a violation.** Remove it immediately — the section must contain only unsent drafts.
- **Cross-reference with blocked Tasks:** If a draft is blocking a Task (the Task cannot proceed until the external party responds), the blocked task's Notes column must name the draft (`📤 Draft: [draft heading](#draft-next-comms)`) and the draft must name the blocked task (`🛑 blocks Task: <task name>`).
- **Never append a "do not send without approval" (or "review before sending", etc.) annotation to a draft.** The `Status: DRAFT`/`Status: READY` line already means unsent; the requirement to get approval before contacting other humans is a standing global agent rule (not a per-draft warning to restate). Adding it anyway is noise — same category as writing "don't `rm -rf $HOME`" next to every `rm` command.

### Diagnosis

**Incident docs only.** Structured record of the investigation's epistemic state regarding causation. Two subsections:

- **Differential Diagnosis** — ranked table of candidate causes (Theory | P% | Status). P% is a betting odd on the theory being a significant contributor; need not sum to 100%. Ordered highest probability first; reordering is a claim that must be justifiable from the Work Log. Status glyphs: ▶️ Active · ⏭️ Queued · ✅ Ruled out. Ruled-out rows stay in the table as a record of losing bets — do not delete; log the reasoning in Work Log. P% on ruled-out rows stays at its last active value: the historical weight is informative. *(Exception to the prose falsified-hypothesis deletion rule in [Temporal Writing Rules](#temporal-writing-rules): that rule applies to narrative prose, not to Differential Diagnosis table rows, which are a structured record.)*
- **Cause** — withheld from the template; add only when a theory is Leading: tested against named alternatives with none falsifying it. Never create speculatively. Distinguish the proximate trigger (immediate cause) from the systemic root cause (underlying condition). Use "supported by [†]" for each supporting claim and "leading" to characterize the overall theory. When written, update Status to `🎯 DIAGNOSED`. See [IncidentRCA.md](../../../docs/IncidentRCA.md#counterfactual-analysis) for the counterfactual methodology.

*Note: Pending investigative threads belong in the top-level [Pending Investigations](#pending-investigations) section, not here. Diagnosis is for the epistemic state of causation (what could cause this?), while Pending Investigations captures what we don't yet know (what can we answer ourselves?).*

Ruled-out theories never reach Decisions — their closure path is the Work Log (how they were eliminated) and the Differential Diagnosis table (their P% and ✅ status preserved as record). Decisions is for team choices only.

### Evidence

**Required in all project, incident, release, and memo docs.** Every verifiable empirical claim must cite its source.

**Placement:** Dedicated `## Evidence` section near the bottom, above Work Log.

**Inline citation:** Unicode dagger † (U+2020), no space before: `claim text[†](#e-descriptive-slug)`

Example: "Latency dropped 40%[†](#e-latency-drop)."

**Entry structure** — each entry is a `###` heading:

```
### Brief description of what is being evidenced

<a id="e-descriptive-slug"></a>

- **Claim**: the specific assertion being backed
- **Source**: URL, file path, git commit SHA, dashboard name, or person name + role
- **Dates**: source vintage (when authored/published) and collection date (YYYY.MM.DD.Dow, when retrieved)
- **Quote / data**: exact text excerpt, metric value, or command output
```

Omit any field that genuinely doesn't apply; include as many as possible.

**Additional rules:**

- **Many items (&gt;5):** use `[†A1](#a1-slug)`, `[†A2](#a2-slug)`, etc.
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

**Required in all project, incident, release, and memo docs.** Audit trail of effort — what we spent time on, what the problems were, how we moved closer to the goal. Git commits describe *what* changed; the Work Log describes *how* we got there.

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

## Rules About Pending Work

### Tasks Pipeline

Tasks flow through the document deterministically: Tasks → Status + Active Work → Work Log.

- **Tasks ↔ Status**: Status rows are verbatim copies (never paraphrased)
- **Tasks ↔ Active Work**: Active Work subtasks relate only to ▶️ tasks
- **Active Work ↔ Work Log**: Concluded items are cleared from Active Work (not duplicated)

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

- **Pending Investigations** — empirical unknowns *we can answer ourselves*. Record specific, named questions about state, metrics, or facts. You control the investigation through logs, testing, measurement, or analysis. Minor clarifications from other teams are fine; the core work is ours. Minor questions within an investigation don't demote it to Draft Comms — but if *they* control the outcome and you're waiting for their decision, it's Draft Comms instead. When completed: findings are absorbed into doc edits (Task notes, Context, Evidence, Work Log). No archive needed — the knowledge remains in the doc.

**Inline Placeholders:**

- **TBD** — placeholder for unknown value or fact; use inline where the value will live. "Latency budget: TBD", "Customer impact: TBD". TBDs are never links.

### Cross-References for Pending Work/Questions

When pending work or questions are *mentioned* outside their canonical sections, they must link back to that section. This prevents invisible dead-ends where a problem is flagged but the reader has no path to the owning entry.

**Antipattern — lone ⚠️ is forbidden:**
A ⚠️ glyph used in a table cell, heading, or prose WITHOUT a link to a canonical pending entry is an explicit antipattern and must be fixed on audit. The glyph signals a problem; the link points to where it is being tracked. The same rule applies to other problem glyphs (❗, 🔔) used as out-of-section signals.

**Standard inline reference forms:**

| What you're referencing | Inline form |
| --- | --- |
| In-progress Task | `▶️ Task: [task name](#tasks)` |
| Blocked Task | `🛑 Task: [task name](#tasks)` |
| Pending Decision | `❓ Decision: [question summary](#pending-decisions)` |
| Pending Investigation | `🔍 Investigation: [question summary](#pending-investigations)` |
| Draft Next Comms item | `📤 Draft: [draft heading](#draft-next-comms)` |
| Inline TODO | write `TODO` inline — no link (TODOs are never linked) |

## Doc Audit Checklist

Run in full on every non-trivial edit. All items apply; domain-knowledge items require cross-referencing with production state.

- ✅ TOC matches actual headings
- ✅ No orphaned sections (all sections referenced in TOC or prior section)
- ✅ All links resolve (no broken anchors, no dead URLs)
- ✅ No links from tracked files to untracked files (aidocs/, tmp/, etc.)
- ✅ For docs with Confluence mirrors: no relative links (they work in markdown/GHE but break in Confluence)
- ✅ **Mortal docs (projects, incidents, releases, memos) have their required sections**
- ✅ **For mortal docs with a Tasks table:**
  - Tasks rows are accurately reflected in Status rows (verbatim copies, not paraphrased)
  - Active Work subtasks relate only to ▶️ (in-progress) tasks
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

### When to Audit

- Full checklist: every non-trivial edit.
- Task Creep audit: on demand.

### What to Audit

- Any doc with any of the standard pre-defined sections
- But never any ephemeral ad hoc docs e.g. under `aidocs/` or `tmp/`

## Audit Date Format

Place at the bottom of the `## Status` section (if present), else at the end of the `## Contents` section (if present), else at the end of the doc. Format as a single italic non-list-item line where `doc-audit` links to this skill:

```
*[doc-audit](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared/blob/main/.wibey/skills/doc-audit/SKILL.md): YYYY.MM.DD.Dow*
```

Example: `*[doc-audit](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.06.19.Thu*`

Update the date whenever the full checklist is run.

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
- **After creating or updating an aidocs file, always open it in VS Code** using `code <filepath>`

---

## Styling Discipline

Standardized formatting so agents and humans produce visually consistent docs.

### Footnote Glyphs in Tables

Footnotes hyperlinked from text use daggers as described above. In tables, the footnotes are so nearby/small that it's often better to link to particular footnotes using visual markers rather than hyperlinked daggers. In that case, use these:

**Informational** (neutral, no action needed):

- † (dagger)
- ‡ (double dagger)
- ⁑ (double asterisk)
- 📌 (pushpin)

**Problem** (needs remediation/investigation):

- ⚠️ (yellow triangle)
- ❗ (red exclamation)
- 📣 (megaphone)
- 🔔 (bell)

The glyph *is* the cell content when the cell otherwise has no data; otherwise append it to the value.

Within a given table or list, each glyph type maps to exactly one footnote. Glyphs may be freely reused across different tables/docs.

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

- Jira ticket IDs (any key: CATGTRLSHP, OPIF, RCTMEXP, CQP, GM, STRCASS, RCTBVAR, …) → `https://jira.walmart.com/browse/TICKET-ID`
- CRQ / change request numbers (CHG-NNNNNNN) → `https://walmartglobal.service-now.com/nav_to.do?uri=change_request.do?number=CHGNNNNNNN`
- ServiceNow incidents (INC-NNNNNNN) → same ServiceNow base URL
- Jira board IDs (board NNN) → `https://jira.walmart.com/secure/RapidBoard.jspa?rapidView=NNN`

**Code and repos:**

- PRs (#NNN) → `https://gecgithub01.walmart.com/<org>/<repo>/pull/NNN`
- Git commit SHAs (first 7–8 chars) → `https://gecgithub01.walmart.com/<org>/<repo>/commit/SHA`
- GHE repo names (relationship-service, qarth-group-service, variant-grouping-stream, etc.) on first mention per doc → link to repo root

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
