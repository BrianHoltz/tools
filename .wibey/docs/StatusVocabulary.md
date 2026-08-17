# Status Vocabulary

## Status Definitions

**Task-table rule: unstarted tasks use a blank Status cell — never a glyph.** `⬜ UNSTARTED` and all other glyphs are for tasks that have entered their lifecycle (started, blocked, paused, canceled, done). A task that has not yet started has no lifecycle state to express; blank IS the status. Filling it with `⬜` or any other placeholder adds noise without adding information and is considered a formatting violation.


|      | Status        | Meaning                                                                | Jira                  | DX / Teflon                | PD / Statuspage    | SN / ITIL          | Google SRE |
| ---- | ------------- | ---------------------------------------------------------------------- | --------------------- | -------------------------- | ------------------ | ------------------ | ---------- |
|      | **Pending**   |                                                                        |                       |                            |                    |                    |            |
| 🔮   | FUTURE        | Beyond current scope; aspirational or follow-on work                   | —                    | —                         | —                 | —                 | —         |
| 📣   | INVOKED       | Our team notified; our incident doc opened                             | —                    | Triage Initial Assessment  | Acknowledged       | Assigned           | Response   |
| ➡️ | ROUTED        | Investigation handed off; incident still live                          | Won't Do (reassigned) | —                         | —                 | —                 | —         |
|      | **Working**   |                                                                        |                       |                            |                    |                    |            |
| 🔬 | INVESTIGATING | Actively working root cause. synonym: ENGAGED                          | In Progress           | Investigate                | Investigating      | In Progress        | Response   |
| 🎯   | DIAGNOSED     | Root cause confirmed; fix not yet deployed                             | In Progress           | —                         | Identified         | In Progress        | Response   |
| 🛠️ | FIXING        | Fix underway — PR open, CRQ in flight                                 | In Progress           | Investigate                | —                 | In Progress        | Mitigation |
| 👀   | UNDER_REVIEW  | Fix is awaiting feedback from another person/team                      | —                    | —                         | —                 | —                 | —         |
|      | **Waiting**   |                                                                        |                       |                            |                    |                    |            |
| ⏰   | AWAITING      | Time-bounded hold; unblocking event committed and expected             | On Hold               | —                         | —                 | On Hold            | —         |
| 🛑 ❓ | BLOCKED       | Stuck on external; no committed ETA — escalate. (🛑 = action needed; ❓ = answer/decision needed) | Blocked               | —                         | —                 | On Hold            | —         |
| ↗️ | RELAYED       | Our team's work handed off; other team carrying forward                | In Progress           | —                         | —                 | —                 | Resolution |
| ⏸️ | PAUSED        | Intentionally shelved; not active but not yet canceled                 | —                    | —                         | —                 | —                 | —         |
|      | **Iterating** |                                                                        |                       |                            |                    |                    |            |
| 💥   | FIX_FAILED    | Deployed fix confirmed not working; back to investigating              | Reopened              | Investigate                | Investigating      | In Progress        | Mitigation |
| 👎   | NOT_APPROVED  | Change/fix not approved and so was not deployed                        | Won't Do              | —                         | —                 | Canceled           | —         |
| ❌   | CANCELED      | Fix attempt canceled; back to investigating                            | Canceled / Won't Do   | —                         | —                 | Canceled           | —         |
|      | **Finishing** |                                                                        |                       |                            |                    |                    |            |
| ↩️ | ROLLED_BACK   | Deployment reverted as mitigation                                      | In Progress           | Mitigate                   | Investigating      | In Progress        | Mitigation |
| 🟡   | MITIGATED     | Customer impact reduced; root cause may remain                         | —                    | Mitigated but not Resolved | —                 | In Progress        | Mitigation |
| 🔭   | MONITORING    | Fix deployed and believed stable; watching metrics before closing      | In Progress           | —                         | Monitoring         | In Progress        | Resolution |
| 📌   | DEFERRED      | Planned and approved but intentionally scheduled for a later phase/sprint | Backlog               | —                         | —                 | —                 | —         |
| ✅   | RESOLVED      | Impact gone; root cause addressed (synonyms: CLOSED, DONE)             | Done / Resolved       | Resolved                   | Resolved           | Resolved           | Resolution |
| 🔵   | AS_DESIGNED   | Behavior matches spec; no fix needed                                   | Won't Fix / Invalid   | —                         | —                 | Resolved (w/ note) | —         |
| 🔹   | WONT_FIX      | Root cause known; consciously not fixing                               | Won't Fix             | —                         | Resolved (w/ note) | Resolved (w/ note) | —         |
| 🔕   | FALSE_ALARM   | Spurious or misunderstood signal; not an actual problem                | Won't Do / Invalid    | —                         | —                 | Canceled           | —         |

- **Jira** — Atlassian issue tracker; states shown are standard Jira workflow values (In Progress, On Hold, Blocked, Reopened, Done, Won't Do, Won't Fix, Canceled, Duplicate).
- **DX / Teflon** — DX Platform defines the triage phases (Triage → Investigate → Mitigate → Resolve) and the "Mitigated but not Resolved" intermediate state. Teflon is an incident management framework defining P0/P1/P2 severity and the Incident Commander role.
- **PD / Statuspage** — [PagerDuty](https://www.pagerduty.com/) on-call alerting (lifecycle: Triggered → Acknowledged → Investigating → Identified → Monitoring → Resolved) combined with Atlassian Statuspage for external status communication.
- **SN / ITIL** — ServiceNow Incidents ticketing system (lifecycle: New → Assigned → In Progress → On Hold → Resolved → Closed → Canceled; P1 Critical – P5 Very Low). [ITIL](https://en.wikipedia.org/wiki/ITIL) (IT Infrastructure Library) is the industry process standard that ServiceNow implements.
- **Google SRE** — [Google Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/) uses overlapping lifecycle *phases* rather than discrete states: Detection → Response → Mitigation → Resolution → Post-Incident. Column values indicate which phase each status falls within.

## Task Relationship Markers

Markers appearing in task-table Notes cells to express direct task dependencies. Not a status, but a relationship signal.

| Glyph | Label | Meaning | Usage |
| --- | --- | --- | --- |
| **⬆️** | `DEPENDS_ON` | This task depends on one or more prior tasks in the same table. Listed after the marker, comma-separated. | `⬆️ task-name`<br/>`⬆️ task-name-A, task-name-B` |

**Rules:**

- The marker is the **sole source of truth** for task dependencies. Row position is never a signal of dependency.
- The marker appears **at the start of the Notes cell** for any task with direct dependencies.
- List only **direct** dependencies by task name (terse, matching the Task column). Indirect dependencies are implicit (i.e., if A→B→C, only C marks B; C does not redundantly mark A).
- Row order *must respect* declared dependencies (no task before its prerequisites), but position alone never implies a prerequisite relationship. Multiple independent tasks may appear sequentially without dependencies between them.
- **Agent guardrail:** Never infer dependency from row order. Always check for the `⬆️` marker. For details, see [doc-audit SKILL.md § Task Discipline Rules § Task Dependencies](../../.wibey/skills/doc-audit/SKILL.md#task-dependencies).

**Example:**
```markdown
| Task | Status | Notes |
| --- | --- | --- |
| Create new AD group | ⏳08.14 | Blocked on org-level check... |
| Complete SailPoint integration | ⏳08.14 | ⬆️ Create new AD group. Do not submit until group exists... |
| Register GitHub App | 🔍08.14 | ⬆️ Create new AD group. Must use group name in request... |
| Check org webhooks | ⏳08.11 | Org-level check (no dependencies). Parallel to above tasks... |
| Submit GHEC Migration Request | | ⬆️ Complete SailPoint integration, Register GitHub App. Blocked on both... |
```

Note: "Check org webhooks" appears after "Register GitHub App" but does not depend on it — it is an independent investigation (parallel work). Dependency is declared only by the `⬆️` marker, never inferred from row position.

## Confidence Ladder

Vocabulary for characterizing the epistemic strength of a claim or theory during investigation. Use the lowest rung the evidence actually supports — never skip rungs to signal confidence you don't have.

| Term | Meaning | Use when |
| ---- | ------- | -------- |
| **Hypothesized** | Plausible; no supporting evidence yet | A theory has been named but not yet checked against any data |
| **Candidate** | Plausible; circumstantially supported | Early signals point toward it; no direct evidence yet |
| **Tenable** | Evidence fits; alternatives not yet tested | Direct evidence is consistent with the theory; no disconfirming check has been run |
| **Supported** | Specific evidence cited; alternatives not ruled out | One or more Evidence entries back the claim; alternatives still in play |
| **Corroborated** | Independently evidenced by 2+ sources | Multiple independent evidence entries converge on the same conclusion |
| **Leading** | Tested against named alternatives; none falsified it | Disconfirming checks were run against specific rival theories; all failed to falsify this one. This is the threshold for writing `### Cause` in a Diagnosis section and updating Status to `🎯 DIAGNOSED`. |
| **Established** | Multiple independent sources; all disconfirming tests passed | The strongest non-"confirmed" claim; appropriate post-incident in a finalized postmortem |

**"Confirmed" is not on this ladder.** It implies certainty that incident investigations almost never warrant. The word actively suppresses further inquiry — readers stop questioning; agents stop testing. Use **Established** for the strongest claims. See [AgentAntiPatterns.md](AgentAntiPatterns.md) for the canonical example of premature confirmation causing a 30-minute investigative detour.

## Sources

**Industry SOTA (general knowledge + external research 2026.04.24):**

- PagerDuty / Atlassian Statuspage: Triggered → Acknowledged → Investigating → Identified → Monitoring → Resolved
- ITIL / ServiceNow standard: New → Assigned → In Progress → On Hold → Resolved → Closed → Canceled
- Google SRE lifecycle phases: Detection → Response → Mitigation → Resolution → Post-Incident
- FireHydrant milestones (most granular public tool): Started · Detected · Acknowledged · Investigating · Identified · Mitigated · Resolved · Retrospective Started · Retrospective Completed · Closed
- incident.io: Triage → Investigating → Fixing → Monitoring → Impact Mitigated → Debrief Completed → Closed
- RFC 7970 IODEF (IETF standard, the only formal specification): new · in-progress · forwarded · resolved · future (5 states)
- MONITORING confirmed present in: Atlassian Statuspage, OpsGenie, GitHub Status, Cloudflare, incident.io — universally placed between fix deployment and resolved declaration; exits on clean metrics or IC judgment after a time window.
