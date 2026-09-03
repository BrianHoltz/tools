# ToDo Management

This document is about systems for managing pending work.

## Solution

### Principles

* Separate domains: Brian, HoltzLusin, Walmart
  * A domain is defined by the set of humans that are authorized for it
* Primay work sources are source of truth
* Human controls admin via markdown edits (e.g via voice interaction)
* Admin controls human by operating on work sources
* Admin has no state other than git-controlled markdown artifacts

### Artifacts

* Ledger/log/history: read-only except for reformatting
* Values
* Goals
* Projects

## Pending Work Sources

### Professional

#### Apple Notes ✅ Full read/write confirmed

**Capabilities:**

- **Read:** find any note by title, search by keyword, list all note titles
- **Read:** read full text content of any note
- **Read:** identify checklist items and their checked/unchecked state
- **Edit:** reorder checklist items (e.g. move completed items to bottom)
- **Edit:** mark items done or undone
- **Edit:** create new notes, append or rewrite note body

**Access method:** Direct SQLite + protobuf — requires VS Code Full Disk Access.

**Setup required (one-time):** System Settings → Privacy & Security → Full Disk Access → add **Visual Studio Code**. Without this, all reads/writes fail with `authorization denied`.

**Implementation notes:**

- DB path: `~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite`
- Note record: `ZICCLOUDSYNCINGOBJECT` — `ZISPINNED`, `ZTITLE`, `ZHASCHECKLIST`, `ZNOTEDATA` (FK)
- Note data: `ZICNOTEDATA.ZDATA` — gzip-compressed protobuf
- Protobuf structure: outer → field 2 (NoteData) → field 3 (TextData) → field 2 (text string UTF-8), field 5 repeated (attribute runs)
- Checklist items: attribute run field 2 (paragraph style) → field 1 = 103 means checklist item; field 5 (ChecklistItem) → field 2 = `isDone` (0/1), field 1 = UUID bytes
- All attribute runs use **Unicode code point counts** for length (not UTF-8 bytes)
- To edit: modify `ZDATA` + bump `ZMODIFICATIONDATE` on `ZICCLOUDSYNCINGOBJECT` to Apple epoch time (`time.time() - 978307200`)
- Must quit + reopen Notes for DB changes to take effect (`osascript -e 'tell application "Notes" to quit'`)
- Always backup DB before writes: `shutil.copy2(DB, "/tmp/NoteStore_backup_YYYYMMDD.sqlite")`
- AppleScript `body` property: readable without FDA, but **strips all checklist state** — useless for checked/unchecked

**Known limitations:**

- Encrypted notes (`ZISPASSWORDPROTECTED=1`): content is not readable
- Notes stored only in iCloud (`ZNEEDSTOBEFETCHEDFROMCLOUD=1`): ZDATA may be empty until synced locally
- Rich content (images, drawings, handwriting): present as attachment references, not modifiable via this method

---

#### Outlook Tasks (Microsoft To Do)

**Capabilities:**

- **Read:** list all task lists and every task (title, due date, status, notes)
- **Read:** filter by status (not started, in progress, completed), due date, importance
- **Edit:** create tasks with title, due date, body, reminder
- **Edit:** mark complete, update due date, modify body
- **Edit:** move between lists, delete tasks

**Access method:** `msgraph` skill via MS Graph API — requires valid Microsoft 365 session.

---

#### Slack: Later

#### Outlook Email

#### Pull Request Comments

#### Jira

#### Task Lists in Current Project Docs

#### Outlook Calendar

---

### Personal

#### Google Tasks

#### Gmail

#### Google Keep

#### Google Calendar

#### SMS

#### Google Chat

#### Discord

#### YouTube Playlists

#### Twitter Bookmarks

#### LinkedIn Messages

---

### Both (Work & Personal)

#### Browser Tabs

#### Downloads Folder

#### Desktop Files

## Existing Solutions

### Cross-platform integration research prompt

Use the following prompt independently with Gemini and ChatGPT:

```text
Act as a skeptical technology researcher and systems architect. Deeply research
existing solutions for a unified personal task-management and agent-orchestration
system. This is an evidence-based research assignment, not a request for generic
product recommendations.

## User context

I want my AI agents (Claude or GPT) to read, write, organize, reconcile, and
manage as many of my task and work sources as is practically feasible. The agents
may run in GitHub Copilot or Walmart's equivalent harnesses, Wibey and Code Puppy,
from IntelliJ IDEA or VS Code. The system should work across macOS, Android,
Google Assistant/Home, and Wear OS, with useful support for both desktop and
mobile/voice/wearable interactions.

My sources are:

- Professional: Apple Notes, Outlook Tasks/Microsoft To Do, Slack, Outlook Email,
  pull-request comments, Jira, task lists in project documentation, and Outlook
  Calendar.
- Personal: Google Tasks, Gmail, Google Keep, Google Calendar, SMS, Google Chat,
  Discord, YouTube Playlists, Twitter/X Bookmarks, and LinkedIn Messages.
- Both work and personal: browser tabs, Downloads, and Desktop files.

The basic requirement is broad read/write/manage coverage, not merely a unified
dashboard. Prefer solutions that can safely create, update, complete, defer,
prioritize, move, link, search, summarize, and reconcile items across sources.
Treat source-specific capabilities and permissions as important constraints.

I am also interested in "Continual Orchestration": real-time coordination of
attention, execution, and interrupts; management of a laptop's entire day;
personal-versus-work separation; short- versus long-horizon priorities; time
management; and long-term life management. "Continual" includes both always-on
operation and coordination across the continuum of teleological considerations
(values, goals, priorities, intentions, and plans). Evaluate whether current
products can provide this, what scaffolding is required, and where human approval
must remain in the loop.

## Research scope

Investigate both:

1. Legacy and current automation/integration solutions: task managers, universal
   inboxes, personal information managers, workflow automation, APIs, webhooks,
   sync layers, desktop automation, mobile automation, voice assistants, and
   open-source/self-hosted tools.
2. AI-agentic solutions: agent harnesses, MCP servers, connectors, skills,
   plugins, computer-use tools, background agents, event-driven agents, memory
   systems, personal operating systems, and multi-agent orchestration frameworks.

Search broadly enough to find overlooked or recently changed options. Include
solutions that can be composed into an architecture; do not assume one product
will solve everything. Research current documentation, API references, pricing
and licensing, release status, platform support, permissions, rate limits,
automation limits, and evidence of active maintenance. Also identify relevant
legacy products that remain useful or whose design informs current options.

## Required analysis

For every serious candidate, report:

- What it is, its status, and its primary role.
- Which of my sources it can read, write, search, trigger, or synchronize.
- Whether access is official API, OAuth connector, MCP, export/import, local
  database, browser automation, OS automation, or an undocumented workaround.
- Support for macOS, Android, Google Assistant/Home, Wear OS, IntelliJ IDEA,
  VS Code, Copilot, Wibey, and Code Puppy.
- Whether it supports Claude, GPT, or both, and how model/harness integration
  actually works.
- Data flow, canonical-source behavior, conflict resolution, identifiers,
  deduplication, history, auditability, and recovery from partial failure.
- Authentication, privacy, local versus cloud execution, encryption, data
  retention, vendor lock-in, reliability, cost, and operational complexity.
- Read/write asymmetries, missing permissions, brittle assumptions, and likely
  breakage points. Do not describe a source as integrated if it is read-only,
  export-only, or merely visible in a dashboard.

Then produce:

- A capability matrix covering every source and every meaningful operation.
- A ranked shortlist of viable architectures, including a recommended
  architecture and at least one lower-complexity fallback.
- A comparison of centralized, federated, and event-driven designs.
- A practical design for an agent control plane that can run from my stated
  harnesses and IDEs, including connectors, tool contracts, queues, schedules,
  event handling, memory, approvals, observability, and fail-safe behavior.
- A specific assessment of how to implement Continual Orchestration today:
  what is genuinely achievable, what requires custom development, what cannot
  be made reliable, and how to evaluate it.
- A phased implementation roadmap with milestones, prerequisites, approximate
  effort, recurring costs, and migration strategy that preserves existing data.
- Concrete experiments or proof-of-concept tests to validate the highest-risk
  integrations before committing to a platform.
- A risk register covering accidental edits/deletions, duplicate tasks, privacy
  leakage between work and personal contexts, stale state, prompt injection,
  excessive autonomy, vendor/API changes, and loss of service.

## Evidence and output requirements

Use primary sources wherever possible: official documentation, API references,
product changelogs, source repositories, and published pricing/licensing. Cite
URLs for material claims and include the access date. Clearly label facts,
inferences, estimates, and unanswered questions. Verify that each cited product
and integration still exists and is available to an individual user; do not
repeat marketing claims without testing them against documented capabilities.

Start with an executive conclusion, then the capability matrix, candidate
analyses, architecture recommendation, Continual Orchestration assessment,
roadmap, proof-of-concept plan, and risk register. Optimize for maximum useful
coverage and reliable read/write control rather than the smallest number of
applications.
```
