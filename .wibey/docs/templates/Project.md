# Project Title

## Summary

<!-- AGENT GUIDE: two kinds of content below:
     LITERALS  = bold labels (Trackers, What/Why/How/Which/Who/When) and `PLACEHOLDER` values: keep the labels, replace the placeholders.
     META      = *italicized text*: guidance on what to write; replace with real content and drop the italics. Delete optional lines that don't apply.
     All content must be terse bullets, never paragraphs. Every PR must be hyperlinked—no free-text PR numbers.

     TRACKERS: one sub-bullet per ticket, oldest first. Typical order: OPIF (if any), Epic, then work tickets in order.
     Format: **YYYY.MM.DD.Dow** [`TICKET-ID`](url) title  — prefix "OPIF:" or "Epic:" where applicable.
   -->

- **Where** Tracked: *(all related tickets, chronologically oldest first; typical order: OPIF, Epic, Predecessor(s), Main)*
  - **YYYY.MM.DD.Dow** OPIF: [`OPIF-ID`](https://jira.megacorp.com/browse/OPIF-ID) *title* *(omit if no OPIF)*
  - **YYYY.MM.DD.Dow** Epic: [`EPIC-ID`](https://jira.megacorp.com/browse/EPIC-ID) *title*
  - **YYYY.MM.DD.Dow** [`FIRST-TICKET-ID`](https://jira.megacorp.com/browse/MAIN-TICKET-ID) *title*
- **What**: *what the project does*
- **Why**: *justification, rationale, business impact*
- **How**: *high-level approach; abstract enough to write on day one without needing updates later*
- **Which**: *our system(s) involved*
  - *Adjacent systems, if any*
- **Who**: *implementer(s)*
  - *Adjacent teams and stakeholders, if any*
- **When**: *omit sub-items that are N/A, else include a date with trialing question mark if it's uncommitted*
  - Started: `YYYY.MM.DD.Dow`
  - Ready for review: `YYYY.MM.DD.Dow`
  - Stg: `YYYY.MM.DD.Dow`
  - Prod: `YYYY.MM.DD.Dow`

## Status

*(Selected verbatim rows from [Tasks](#tasks) table)*

Verbatim excerpt of selected Tasks rows: recent completions and upcoming work. Update each work session. Rows here must be copy-pasted from the Tasks table, never paraphrased or summarized. The Tasks table is authoritative; Status is a view into it. If you find yourself writing a non-task bullet, it probably should be a Tasks row instead.

<!-- fill in the date you ran doc-audit -->
*doc-audit: YYYY.MM.DD.Dow*

## Contents

<!-- AGENT GUIDE: Interfaces and Engineering Considerations do not get sub-bullets in the Contents. Their subsections are standardized and predictable — sub-bullets add noise without aiding navigation. -->

- [Summary](#summary)
- [Status](#status)
- [Tasks](#tasks)
- [Active Work](#active-work)
- [Draft Next Comms](#draft-next-comms) *(optional)*
- [Pending Decisions](#pending-decisions)
- [Pending Investigations](#pending-investigations)
- [Ad Hoc Sections](#ad-hoc-sections)
- [Interfaces](#interfaces)
- [Engineering Considerations](#engineering-considerations)
- [Context](#context)
- [Decisions](#decisions)
- [Appendices](#appendices)
- [Evidence](#evidence)
- [Work Log](#work-log)

## Tasks

The Tasks table is a **planning device**: the list of things we must not forget to do in order to complete the project, and the dependency/priority relationships between them. Ideally all rows are added before work begins: after that, only statuses change, not the list itself. The ordering is partial, not total: multiple tasks can proceed in parallel. [Active Work](#active-work) tracks the fine-grained execution state within whichever tasks are in progress.

- **Litmus test: never add and complete a task in the same session.** If you did the work and are now recording it, that is a [Work Log](#work-log) entry, not a task. Tasks describe work that has not yet started. The Work Log describes work that happened.
- Only add tasks that were **planned before work began**. Do not backfill completed work into the task list as a record of what happened: that's what Work Log and git history are for. This is the single most common agent mistake on project docs.
- The only exception: extraordinary unplanned work that materially changed the project scope or timeline (e.g. a surprise production incident, a major design pivot from code review). Routine bug fixes, reviewer feedback, and incremental polish do not qualify.
- Do not include time estimates unless explicitly asked. Agents are usually too pessimistic about their own speed and too optimistic about humans.
- Agents and humans keep finer-grained session state in [Active Work](#active-work).

Status glyphs and meanings: see [StatusVocabulary.md](../StatusVocabulary.md). Format: no space between glyph and date (`07.14`); dates in MM.DD; glyph + date in Status column.

**Unstarted tasks have a blank Status cell — never use `⬜` or any other placeholder.** Blank IS the correct status for work that hasn’t started. Add a Note only when the blank cell could mislead — e.g. a task that looks redundant with an existing row but is genuinely distinct, or one that is out-of-scope until a predecessor completes. If nothing would be misunderstood, leave Notes blank too.

**Follow-on work** (tech debt, known gaps, future improvements explicitly out of scope) goes at the bottom of this table with "Follow-on." prefix in the Notes column. No status glyph — follow-on tasks were never in scope, so they have no lifecycle state. Point to Jira tickets or TODOs in code where applicable. If a follow-on item blocks or is blocked by something, it's not follow-on — it's a real task; move it up.

**Doc updates** (repo docs, playbooks, Confluence) that need doing as a result of this project are tasks — add them to this table. Static doc links belong in [References](#references).


| Task         | Jira                                                             | Status | Notes |
| -------------- | ------------------------------------------------------------------ | -------- | ------- |
| Example task | [CATGTRLSHP-NNN](https://jira.megacorp.com/browse/CATGTRLSHP-NNN) |        |       |

## Active Work

The mutable present: fine-grained subtasks and cached state for whichever [Tasks](#tasks) are in progress. Both agents and humans maintain this section as a shared workspace: if a session is interrupted, the next agent or human picks up here.

- Too granular for Tasks (which is project-level planning, not session-level execution)
- Guides whoever is doing the literal next piece of work: which file to open, which test to write, which config to change
- When subtasks are completed, write a terse [Work Log](#work-log) entry summarizing what was decided/discovered, then clear those items from here
- Update each work session as subtasks are completed or discovered
- **Strictly organized by `###` heading per ▶️ in-progress task** — one section per task, named exactly as it appears in the Tasks table. Do not use numbered lists or free-form prose at the top level.
- **DRY with Tasks and Status** — no information here that is not grounded in a ▶️ task row. If you find yourself writing subtasks for work that has no corresponding ▶️ task, add the task first.
- **Untasked work is a red flag** — it is acceptable only for brief, truly ephemeral state (e.g., "waiting for CI to finish"). If untasked work persists across sessions, it belongs in the Tasks table.

*(one `###` section per ▶️ task, subtask details here)*

## Draft Next Comms

*Optional.* Pre-composed outbound communications — stakeholder status updates, PR announcements, release notifications, team posts. Each draft is a `###` sub-heading with target, a `Status: DRAFT` or `Status: READY` line, and the message body in a blockquote. When a draft is sent, delete it from here entirely and record one Work Log entry with the destination and message URL.

## Pending Decisions

Unresolved choices your team must make — "Should we do X?" or "Which approach?" If resolving requires doing something, that doing is a Task; the question stays here until answered. If a question turns out to need an external answer, *convert* it: remove it from here, create a Draft Next Comms entry, and mark any blocking Task 🛑 — never leave a question in both places. Every decision that blocks a Task must have a corresponding ▶️ (or 🛑) row in the Tasks table. Move to Decisions once answered — never delete.

## Pending Investigations

Empirical unknowns *we can answer ourselves* — "Does this approach work?" or "What is the actual performance?" Record specific, named questions. You control the investigation through analysis, testing, measurement, or code review. Minor clarifications from other teams are fine; the core work is ours. When completed: findings are absorbed into doc edits (Task notes, Interfaces, Engineering Considerations, Work Log). No archive needed.

## Ad Hoc Sections

Project-specific sections live here, between Open Questions and Interfaces. Use them for anything that doesn't fit neatly into the standard sections below: e.g. Callers and Cutover, Migration Design, Data Provenance, Endpoint Design. These sections are often the primary narrative of a project; the standard sections that follow are frequently thin or N/A by comparison. Delete this placeholder heading and replace it with whatever the project needs.

## Interfaces

Sections below are parallel to the repo description. Each captures the delta introduced by this project. When a subsection is N/A, collapse it into a bullet in the list below instead of devoting a subsection heading to it. Only create a `###` subsection for interfaces that have real content.

<!-- AGENT GUIDE: The N/A list goes here, immediately after the Interfaces heading. Example:
- **Inbound API, Outbound API, Inbound Kafka, Outbound Kafka**: N/A — no changes.
Then only subsections with content follow as ### headings. -->

### Configuration

- New CCM keys, feature flags, and environment variables introduced by this project. Include NON-PROD and PROD values, and whether each key gates a specific phase.

### Inbound API

- New or modified REST endpoints introduced by this project: method, path, request/response schema, business logic, error codes.

### Inbound Kafka

- New or modified Kafka consumers introduced by this project: topic, consumer group, message schema, flow description.

### Outbound Kafka

- New or modified Kafka producers introduced by this project: topic, trigger conditions, message schema.

### Outbound API

- New or modified outbound service calls introduced by this project: base URL, endpoints called, timeout/retry strategy, error handling.

### Database Tables

- New or modified tables introduced by this project: schema, read/write operations by endpoint, migration notes.

## Engineering Considerations

Cross-cutting concerns that any reviewer or on-call engineer would want to know. Same N/A rule as Interfaces: collapse N/A subsections into a bullet list here instead of giving each a heading.

### Security

- Auth model changes, new consumer registrations in sr.yaml, policy exceptions, or encryption considerations introduced by this project.

### Risk Assessment

- Frank, honest bulleted list of biggest risks, in descending severity. Can be used to fill in CRQ risk and blast radius.

### Testing

- Terse summary of unit tests, postman suites, stage test plan, any manual or E2E (w/ partners) testing.

### Performance / Scalability

- Traffic volume assumptions, rate limit assertions, latency budget, and any load-test results relevant to this project. Might be terse or N/A.

### Alerting, Monitoring, Logging

- New or updated alerts, dashboards, and log patterns introduced by this project. What would page you at 3am and how would you diagnose it?

### Multi-Tenancy

- How this project's changes behave across tenants, marts, and locales. Note any tenant-specific feature flag gating or data partitioning.

## Context

### Related Projects

*Links to prior or related projects with one-line description of the relation — predecessor work, parallel initiatives, follow-on tickets.*

### Documents

*Relevant external links consulted on demand: Confluence pages, tooling (OneClick, DX, Akeyless), monitoring dashboards (Grafana, GCP console), team contacts (people, Slack channels). Omit links already in Trackers (Jira tickets) or Evidence (empirical citations with claims).*

### Concepts

*Optional. Definitions of terms, acronyms, or system components specific to this project. Define inline if brief; add an entry here if the explanation is longer than a parenthetical.*

## Decisions

Team decisions archived for audit trail. Each entry states what was decided, why, and when. Move entries here verbatim from Pending Decisions; do not delete. By default, Decisions should be all and only the choices that were previously in Pending Decisions. Do not add decisions here that were never pending: those belong in the narrative sections or appendices.

## Appendices

Things barely worth keeping, that don't (any longer) merit an ad hoc section above. When even appendix space isn't warranted, delete the content and leave a one-line tombstone in the doc (e.g. "Deep comparison removed: see git history YYYY-MM-DD") so readers know where to find it.

Appendix subsections are just `###` headings with descriptive names: don't prefix with "Appendix A:", "Appendix B:", etc. The numbering/lettering forces renumbering on insert/delete, and the "Appendix" label is WET with the parent section heading.

## Evidence

Every sourced claim uses a dagger footnote: `claim text[†](#e-descriptive-slug)`. Each entry gets an HTML anchor (`<a id="e-slug"></a>`), `###` heading, and Claim/Source/Dates/Quote fields. Label unsourced claims "Inference:" until evidenced. See the doc-audit skill for the Evidence protocol.

## Work Log

The append-only past: an audit trail of effort, not a replay of git or GitHub history. Git commits describe *what changed*. The work log describes *what we spent time on, why we went this direction instead of another, what the main costs were, what blocked us, and how we moved closer to the goal*. A reader should be able to justify the calendar time spent on this project from the work log alone. Items graduate here from [Active Work](#active-work) when concluded.

Agents should timestamp entries during active work sessions (**HH:MM:** prefix) to provide pacing visibility. One entry per significant decision or completion, roughly every ~30 minutes. Keep entries terse. Add YYYY. prefix at year boundaries.

### MM.DD Dow Title of The Day's Work

- **HH:MM:** Entry text here.
