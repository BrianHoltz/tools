---
name: converge
description: |
  Author/Critic convergence review — two agents iterate on a shared aidoc until they
  agree or escalate. Either role may be the 1st agent to start; the 2nd agent joins
  automatically by detecting which role is still awaiting. Both run autonomously to
  completion — no user relay needed between rounds.
  - START as Author: scaffold aidoc, write rationale, poll for Critic
  - START as Critic: scaffold aidoc, file objections cold, poll for Author
  - JOIN: auto-detect which role is needed from the aidoc state
metadata:
  author: b0h0166
sample-prompts:
  - "run converge on this doc as the Critic"
  - "/converge on 'root cause section' --role critic --file shared/incidents/2026-04-15_Foo.md"
  - "/converge on 'delete validation' --role author --file shared/projects/Foo.md --lines 540-567"
  - "converge on shared/aidocs/2026-03-12/1338_ClaytonFeedbackConvergence.md"
  - "converge latest"
arguments:
  - "topic_or_path — required. If it's an existing .md file path, JOIN that review. Otherwise, START a new review on this topic."
  - "[--role author|critic] — required for START. Which role this agent plays."
  - "[--file path] — (START only) source file containing the section under review"
  - "[--lines N-M] — (START only) line range to extract"
  - "[--scope text] — (START only) what is in scope (out-of-scope items excluded)"
  - "[--label text] — this agent's label (default: auto-detected from tool environment)"
---

> [!NOTE]
> **Mirror-safe skill.** This file contains no Walmart-proprietary content and is
> designed to be manually mirrored to personal laptops. The canonical copy lives in
> [`relationship-shared/.wibey/skills/converge/`](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared).
> **If you are reading this outside of Walmart GHE, do not edit it here** — make
> changes in relationship-shared and re-sync.

# converge — Author/Critic Review

**Either role may start.** The **Author** wrote (or owns) the doc and defends decisions. The
**Critic** reads it cold and surfaces specific objections. They iterate on a shared aidoc until
changes are agreed or disagreements are escalated to the user.

The Critic's job is to find problems — not to validate, summarize, or praise.
Hedged, vague, or consensus-seeking criticism is a protocol violation.

## Two Modes

**START mode** — whichever agent starts first creates the aidoc and writes its initial entry.
Either role may go first:
```
# Author starts first:
/converge on "topic" --role author --file shared/incidents/2026-04-15_Foo.md

# Critic starts first:
/converge on "topic" --role critic --file shared/incidents/2026-04-15_Foo.md
```

**JOIN mode** — the second agent scans for the aidoc, detects which role is still awaiting,
and fills it automatically:
```
/converge on "topic" --role critic   ← finds existing aidoc; joins as critic if awaiting
/converge on "topic" --role author   ← finds existing aidoc; joins as author if awaiting
converge latest                       ← joins whatever role is awaiting in the newest aidoc
```

**The user's workflow — start both agents, then do nothing:**
- Start one agent: `/converge on "topic" --role author --file shared/incidents/Foo.md`
- Start the other: `/converge on "topic" --role critic --file shared/incidents/Foo.md`
- Either role may be started first. Whichever agent runs Step 0 first and finds no existing
  aidoc becomes the 1st mover; the other becomes the 2nd mover automatically via the sentinel.
- Both run to completion autonomously. No relay, no copy-paste between rounds.
  Each polls the shared aidoc, writes when it's their turn, and loops until CONVERGE or UNRESOLVED.

The 2nd agent discovers the aidoc via `converge latest` or its own sentinel scan. The user does
not need to provide the path or relay anything between agents.

**Role conflict:** If both agents are started with the same `--role`, the 2nd mover will find
`*(awaiting <other-role>)*` in the aidoc and detect that its role is not needed. It should
inform the user: "Aidoc awaits `<other-role>` but I was started as `<same-role>` — please
start the other agent with `--role <other-role>`."

`converge latest` shorthand: find the most recent `*Convergence*.md` in the aidocs directory.

## Background

This skill implements the **shared blackboard model** from multi-agent systems
research — agents coordinate via a shared file where they publish analyses and
read each other's updates. The protocol incorporates lessons from:

- **Diverse Multi-Agent Debate (DMAD, ICLR 2025):** Mild initial disagreement
  improves outcomes by forcing agents to inspect rather than replicate reasoning
- **Adaptive Stability Detection (NeurIPS 2025):** Debates stabilize in 2-7 rounds;
  our 3-round cap matches this empirically
- **Wu et al. (2025) controlled study:** Evidence anchoring and forced justification
  counteract majority-opinion suppression

Key design constraint: IDE-based agents (VSCode Wibey, Cursor Wibey) cannot
communicate directly. The shared filesystem is the only channel. Agents discover
each other's turns by polling the aidoc file — no user relay is needed between rounds.

## Limitations

- **Same-model ceiling:** If both agents run the same model, the team can't exceed
  that model's reasoning ceiling. Benefits come from different information (different
  files read, different conversation history), not different reasoning architectures.
- **Agreement bias:** The Critic tends toward agreement after the Author defends a
  choice. The protocol counters this by requiring the Critic to file objections
  *before* reading the Author's rationale (when Author starts first), and to
  explicitly re-evaluate each defense rather than accept it.
- **Filesystem sharing required:** Both agents must have read/write access to the
  same aidoc path. Works for VSCode + Cursor on the same machine, or two terminals
  in the same repo.

## Workflow: START Mode

### Step 0: Sentinel check — do this FIRST, before any other action

**Before creating any file**, scan for a convergence aidoc that already exists for this
topic. Two agents independently running START is the most common failure mode — it
produces two parallel debates that never see each other.

```bash
# Check today and yesterday (sessions can span midnight)
ls -t shared/aidocs/$(date +%Y-%m-%d)/????_Convergence*.md 2>/dev/null
ls -t shared/aidocs/$(date -v-1d +%Y-%m-%d)/????_Convergence*.md 2>/dev/null
# or without shared/:
ls -t aidocs/$(date +%Y-%m-%d)/????_Convergence*.md 2>/dev/null
```

Three outcomes:

**A — non-empty file found whose name/content matches the topic:**
- Stop. Read it. Check for `*(awaiting ...)*` — join as the needed role.
- Tell the user: "Found existing convergence doc at `<path>` — joining as `<role>`."
- Do NOT create a second aidoc.

**B — empty file (0 bytes or blank) found matching the topic:**
- You are the **2nd mover**. The first mover has claimed this path but hasn't written yet.
- Do NOT create another aidoc. Go to [Step 0B: 2nd-mover polling](#step-0b-2nd-mover-polling).

**C — no matching file found:**
- You are the **1st mover**. Immediately claim the path before scaffolding — go to Step 1.

### Step 0B: 2nd-mover polling

Poll the empty aidoc until the first mover has scaffolded it (non-empty):

```bash
# Check file size every 15 seconds until content appears
while [ ! -s "$AIDOC_PATH" ]; do sleep 15; done
```

Once the file has content, switch to JOIN mode: [Workflow: JOIN Mode](#workflow-join-mode).
Tell the user: "First mover has scaffolded the aidoc — joining as `<role>`."

### Step 1: Determine and claim the aidoc path

For repos with a `./shared/` symlink:

```bash
AIDOC_DIR="shared/aidocs/$(date +%Y-%m-%d)"
mkdir -p "$AIDOC_DIR"
```

For other repos:

```bash
AIDOC_DIR="aidocs/$(date +%Y-%m-%d)"
mkdir -p "$AIDOC_DIR"
```

Name the file `HHMM_ConvergenceReview_TopicSlug.md` where HHMM is the current
time and TopicSlug is a CamelCase summary of the topic.

**Immediately claim the path** before doing any other work:

```bash
AIDOC_PATH="$AIDOC_DIR/HHMM_ConvergenceReview_TopicSlug.md"
touch "$AIDOC_PATH"   # creates empty sentinel; 2nd mover finding this will yield
```

This is the mutex. The file exists but is empty. Any other agent scanning aidocs will
find the empty file (Step 0 outcome B) and enter 2nd-mover polling mode instead of
creating a competing aidoc. Scaffold the full content in Step 5 — the empty file is
just a placeholder until then.

### Step 2: Get the current timestamp

```bash
date "+%Y-%m-%d %H:%M %Z"
```

Always run this — never guess the date or time.

### Step 3: Determine your agent label

Auto-detect from the environment:

- VSCode with Wibey extension: `VSCode Wibey`
- Cursor with Wibey extension: `Cursor Wibey`
- Claude Code CLI: `Claude Code CLI`

Append the model ID (e.g. `claude-sonnet-4-6`) to form the full label.
Example: `VSCode Wibey Sonnet4.6`

If the user provided `--label`, use that instead.

### Step 4: Extract the section under review

If the user provided `--file` and `--lines`, read those lines from the file.
If the user provided `--file` without `--lines`, use the whole file (or ask which
section if the file is large).
If neither was provided, ask the user what content to review, or ask them to paste it.

### Step 5: Scaffold the aidoc

Write the aidoc header — identical regardless of which role starts:

```markdown
# Convergence Review: {Topic}

**Protocol:** The Author writes rationale for the section below. The Critic reads it
and files numbered objections. They iterate until all are resolved or escalated.

**Source:** {file path and line range, or "provided by user"}
**Scope:** {scope, or "all aspects of the section under review"}
**Started:** {timestamp}
**Started by:** {Author|Critic} — {label}

## Protocol Rules

- Timestamp every entry: run `date "+%Y-%m-%d %H:%M %Z"` before writing
- First entry must include agent self-description (tool, model ID, workspace, branch)
- Cite file paths, method names, or config keys as evidence for factual claims
- **Critic rules:**
  - When Author starts first: file objections BEFORE reading the Author Rationale
    section — form objections from the content alone, then read rationale for context
  - When Critic starts first: the Critic has already read cold; no constraint in later rounds
  - Minimum 3 numbered objections in initial critique — fewer is a protocol violation
  - No opening praise or summary. Start with Objection 1.
  - Each objection: one specific problem → why it matters → what's wrong or missing
  - No "however" or "that said" hedges
  - In response rounds: re-evaluate each defense on its merits. Accept only if the
    Author's reasoning genuinely resolves the objection. Push back otherwise.
- **Author rules:**
  - Respond to every numbered objection: Accept / Revise / Defend
  - Accept: acknowledge the problem, describe the change
  - Revise: propose a specific revised formulation
  - Defend: explain why the original stands, with evidence
  - Do not ignore or bundle objections
- Max 3 rounds per agent (initial + 2 responses)
- Signal completion: write CONVERGE when agreed, UNRESOLVED: [objection N] for
  points requiring user arbitration
- Append only — never edit the other agent's sections
- Humans may enter at any time with a labeled section; treat their input as
  authoritative direction — engage with specifics, adjust position accordingly

## Section Under Review

{verbatim content of the section being reviewed}

---
```

Then append the role-specific initial sections:

**If `--role author` (Author starts):**

```markdown
## Author Rationale — {Author Label}

{timestamp}
{self-description: Tool, Model, Workspace, Branch}

**Intent:** {what this section is trying to accomplish}
**Key decisions:** {numbered — non-obvious choices and why they were made}
**Known weaknesses:** {what you already know is imperfect and why it was left as-is}

---

## Critic — Initial Objections

*(awaiting Critic)*
```

**If `--role critic` (Critic starts):**

The Critic has no Author Rationale to read yet — file objections from the content alone.

```markdown
## Author Rationale

*(awaiting Author)*

---

## Critic — Initial Objections — {Critic Label}

{timestamp}
{self-description: Tool, Model, Workspace, Branch}

**Objection 1:** {specific problem} — {why it matters} — {what's wrong or missing}

**Objection 2:** ...

**Objection 3:** ...

[additional objections as warranted]

---

## Author Response — Round 1

*(awaiting Author)*
```

### Step 6: (Author start only) Write your rationale

In the Author Rationale section, fill in Intent, Key decisions, and Known weaknesses.
Being honest about weaknesses is not a concession — it calibrates the Critic's focus
toward real problems rather than things you already considered and accepted.

### Step 7: Announce the aidoc path and begin autonomous polling

Print the path for observability — no action needed from the user:

```
Convergence doc: {aidoc_path}
Polling for the other agent...
```

The other agent will discover this file via `converge latest` or by running the same
sentinel scan (Step 0). **Do not wait for the user to relay the path.** Immediately
begin polling as described in [Polling and Iteration](#polling-and-iteration) and
continue autonomously through all rounds until CONVERGE or UNRESOLVED.

### Step 8: Autonomous polling loop

See [Polling and Iteration](#polling-and-iteration). **Do not stop between rounds.
Do not ask the user for permission to continue. Keep polling and writing until the
debate concludes.**

## Workflow: JOIN Mode

Use when the user says:
- `converge on shared/aidocs/2026-04-16/1147_ConvergenceReview_Topic.md`
- `converge latest`
- `converge on <path>`

### Step 1: Find the aidoc

If `converge latest`, find the most recent convergence aidoc:

```bash
ls -t shared/aidocs/*/????_Convergence*.md 2>/dev/null | head -1
# or without shared/:
ls -t aidocs/*/????_Convergence*.md 2>/dev/null | head -1
```

If the user gave a specific path, use that.

### Step 2: Detect which role is needed

Read the aidoc. Scan for `*(awaiting ...)*` placeholders:

- `*(awaiting Critic)*` → you are the **Critic**
- `*(awaiting Author)*` → you are the **Author**
- No awaiting placeholder found → debate may be complete; inform the user

### Step 3: Act in your detected role

**Joining as Critic (Author started first):**

Read only the Section Under Review and Protocol Rules. Do NOT read the Author
Rationale yet — your first objections must be independent, formed from the content alone.

Write under `## Critic — Initial Objections`:
- Timestamp and self-description block
- Minimum 3 numbered objections. No opening paragraph. Start with Objection 1.
- Each objection: specific problem → why it matters → what's wrong or missing
- Cite content directly (quote the relevant phrase or element)
- No "however" or "to be fair" hedges

After filing objections, read the Author Rationale for context. If the rationale already
addresses one of your objections, note it as "withdrawn — addressed in rationale" (keep
the numbering intact).

Then append:

```markdown
---

## Author Response — Round 1

*(awaiting Author)*
```

**Joining as Author (Critic started first):**

Read the full aidoc including all Critic objections.

Replace the `*(awaiting Author)*` stub in `## Author Rationale` with your entry:
- Timestamp and self-description block
- **Intent:** what the section is trying to accomplish
- **Key decisions:** numbered non-obvious choices and reasoning (brief — the Critic has
  already formed their view; this is context, not pre-emption)
- **Known weaknesses:** what you know is imperfect and why
- Then respond to every numbered objection: Accept / Revise / Defend

Then append:

```markdown
---

## Critic Response — Round 2

*(awaiting Critic)*
```

### Step 4: Autonomous polling loop

See [Polling and Iteration](#polling-and-iteration). **Run autonomously to completion —
do not stop between rounds or ask the user for anything.**

## Polling and Iteration

**This is a fully autonomous loop. Do not stop between rounds. Do not ask the user
for anything. Keep going until you write CONVERGE, flag UNRESOLVED, or hit the
10-minute timeout.**

After writing any entry, immediately begin polling:

```bash
# Lightweight poll — just check for the awaiting placeholder
while grep -q "*(awaiting $(YOUR_ROLE))*" "$AIDOC_PATH"; do
  sleep 30
  # re-read file; check if placeholder is gone (other agent wrote)
done
```

Concretely:
- Re-read the aidoc every 30–60 seconds
- Check whether a new section has appeared after yours (the `*(awaiting ...)*`
  stub for your role has been replaced with content)
- Each poll is a single file read — do not re-analyze on every cycle
- Timeout after 10 minutes of no change: print the aidoc path and
  "Timed out waiting for the other agent — debate paused" then stop

When the other agent has written, read their entry and immediately respond:

**If all objections are resolved (accepted, revised, or successfully defended):**
- Write `CONVERGE`
- Write a **Proposed Delta** section (see below)
- Done — no user action needed

**If objections remain:**
- Write your next round response immediately. Do not stop to check with the user.
- Continue. Address only unresolved points; do not re-litigate resolved ones.

**If round 3 is reached without convergence:**
- Flag remaining as `UNRESOLVED: Objection N — [brief description]`
- Stop, print "UNRESOLVED — user arbitration needed" and the aidoc path

**The user may tell you to stop polling at any time. Respect this immediately.**

### Writing the Proposed Delta

When convergence is reached:

```markdown
---

## Proposed Delta

*Agreed by both agents on {timestamp}. Apply these changes to the source document.*

**Accept / incorporate:**
- [list of accepted objections and what changes they require]

**Revisions:**
- [specific revised formulations agreed upon]

**Unchanged (defended):**
- [defended points with one-line summary of the accepted rationale]

**UNRESOLVED — Objection N:** [brief description]
- Critic position: ...
- Author position: ...
- User arbitration requested.
```

### Applying the Proposed Delta

**The Author always applies the delta to the source document** — the Critic reviews but
does not edit source files. Before making any changes:

1. **Commit the source document first.** The doc's current state is the baseline. Commit
   it so the user can `git diff` to see exactly what the convergence review changed.
2. **Apply the accepted/revised changes** from the Proposed Delta to the source document.
3. **Stop and let the user review the uncommitted changes.** Do not commit the applied
   delta — the user reviews the diff and decides whether to commit, amend, or revert.

This workflow gives the user a clean before/after: the commit is "doc before convergence
review," the uncommitted diff is "changes from convergence review." The user can accept,
cherry-pick, or discard any part.

### When a Human Enters the Debate

Humans may add labeled sections at any point (e.g. "Human Review — Name (date)").
When this happens:

- The human's direction supersedes the agents' prior positions. If both agents
  agreed to defer something and the human says "do it now", do it now.
- Respond to the human's specific points. Don't just acknowledge — engage with
  tradeoffs and concrete implications.
- The Proposed Delta may need a v2. Update or append.

### Distilling Lessons Learned

After convergence, check whether the review surfaced a reusable diagnostic principle —
a mistake that would recur in future investigations if not captured. If so, write or
update a principle in the repo's heuristics doc (e.g.
`shared/docs/InvestigationHeuristics.md` or any local equivalent). The convergence
aidoc is ephemeral; the heuristics doc is the durable artifact.

## Gotchas

- **Duplicate aidoc (most common setup failure):** Both agents running START independently
  produces two separate debates that never intersect. The guard in Step 0 prevents this —
  but it only works if you actually run it. If you are the second agent on a topic and you
  find yourself about to `mkdir` a new aidoc, stop and search first. When in doubt,
  `converge latest` is safer than `converge on "topic"`.
- **Race conditions (two-agent START):** The sentinel `touch` in Step 1 is the mutex.
  Both agents scan (Step 0), find nothing, and proceed toward Step 1. Whichever touches
  the file first wins; the second will find an empty file on its next scan and enter
  2nd-mover polling (Step 0B). The window for a true collision is the milliseconds
  between the two `touch` calls — vanishingly small in practice. If both agents somehow
  scaffold independently, treat the older file (lower HHMM) as canonical; abandon the
  newer one.
- **Mid-write clobber:** If both agents write simultaneously after the file is populated,
  one may clobber the other's edit. The polling interval (30–60s) makes this unlikely but
  not impossible. If you detect the file changed under you (your previous content is gone),
  re-read and re-append.
- **Label confusion:** The user may swap which tool is Author vs. Critic.
  Use the labels in the aidoc as ground truth.
- **Scope creep:** Stick to the declared scope. If you discover something
  out of scope that matters, note it as "Out of scope but relevant: ..." and move on.
- **Polling burn:** Don't burn context on polling. Each poll is a simple
  file read + check for the "awaiting" placeholder. Don't re-analyze the
  file on every poll.
- **Critic agreement bias:** The most common failure mode is a Critic who
  accepts Author defenses too easily. If you're the Critic and you find yourself
  writing "that's a fair point" to every defense — you've been captured. Re-read
  the original objection and ask whether the defense actually resolves it, or
  merely explains it.
