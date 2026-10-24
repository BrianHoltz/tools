# Agent Debates

A terse log of disagreements where an agent changed Brian's mind or Brian changed an agent's. Newest first.

Format: `## Date — topic` (with agent and context), then `### Point` per disagreement with **Brian**, **Agent** and **Changed** bullets.

## 2026.10.24.Sat — Downloads artifact retention

Code Puppy (gpt-6.1-sol); result: [artifact completion gate](AgentRules.md#artifact-completion-gate).

### Count cap versus spread

- **Brian:** keep at most 3–4, but include the latest two from today and the latest from yesterday, last week, last month and last year.
- **Agent:** that spread needs up to six files; one goal must give.
- **Changed:** Brian's mind; the period rule supersedes the cap.

### Single coarse slots

- **Brian:** use restic's `--keep-weekly 1 --keep-monthly 1 --keep-yearly 1`.
- **Agent:** a count of one always selects the newest build, never last week's, month's or year's.
- **Changed:** Brian's mind; keep three per period.

### Oldest and newest per period

- **Brian:** keep each period's oldest and newest build.
- **Agent:** a period's oldest nearly duplicates the prior period's newest and doubles the count for little rollback value.
- **Changed:** Brian's mind; keep the newest only.
