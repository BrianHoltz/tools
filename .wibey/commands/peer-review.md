---
name: peer-review
description: Review a PR or CRQ against the team's ReviewStandards, including Walmart pr-review as a subset, and create or update the review under shared/aidocs/.
---

# Peer Review

Review the PR or CRQ supplied in `$ARGUMENTS`. Infer the target from the active editor or conversation when omitted; ask only if it remains ambiguous. This is an analysis-and-drafting command, not authorization to post, approve, merge, deploy, or modify the reviewed code.

## Review Contract

Read the applicable agent rules and the team's `shared/docs/ReviewStandards.md` in full on every invocation. The standards are authoritative and non-comprehensive: apply them alongside independent source-level review, not as an exhaustive checklist. Do not copy the standards into this personal command.

Resolve `shared/` to the team shared repository. When working inside that repository, use its root directly. Outside a consuming workspace on the work laptop, resolve the checkout specified by AgentRules. If the team reference is unavailable, stop and identify the missing prerequisite; do not invent standards or substitute a generic review.

Read relevant service references and project/release records for context. Load the team's doc-audit skill for document placement, evidence, draft formatting, and signing. Follow the team's tool/auth recovery and safe-browse workflow whenever applicable.

## Review Record

Search `shared/aidocs/` for an existing review of the same PR or CRQ before creating another. Create or update one review document there, using `yyyy-mm-dd/hhmm_CamelCase.md` naming and the date/update rules from doc-audit. Create the document even for a short review; write findings incrementally and preserve human edits and existing comment dispositions. Re-read before each write and follow AgentRules' write protocol.

Record the linked target, review timestamp, exact reviewed PR head/base or CRQ release artifact, scope, findings, evidence, and unavailable checks/scans. Include the exact headings `Draft PR Comments`, `Posted PR Comments`, and `Overruled PR Comments` when reviewing PRs, including PRs comprising a CRQ. Use named findings with severity, precise file/line links, impact, and actionable guidance; never sequential finding labels. Keep CRQ-only findings distinct from proposed PR comments.

Open the review document in the active IDE as soon as it exists and after updating it. Keep aidocs artifacts out of git. End chat with a link to the record and a terse conclusion or blocker, not a duplicate report.

## PR Review

- Verify repository, PR URL, head/base, existing reviews/comments, changed files, coverage evidence, and every reported check. Use `gh pr diff` or `gh pr view --json files` as the authoritative merge scope, never `git diff main..branch`. Read surrounding source at the reviewed revision; exclude unrelated working-tree changes.
- Perform an independent review against ReviewStandards and relevant service contracts: correctness, regressions, security, dependencies, tests/coverage, logging, operational safety, naming, and production change-control scope. Record evidence rather than assuming a passing gate proves adequate tests or safe behavior.
- Load and invoke Walmart's `pr-review` skill for the same target as a **subset** of peer-review. Discover its installed canonical skill file through the host's skill registry or filesystem; read it before invoking. Its report is input, not the final verdict, and it cannot override ReviewStandards, authoritative PR scope, or permission boundaries.
- Also execute the separate PR Agent review pass required by ReviewStandards, including its security-audit and dependency-scan tracks. Walmart `pr-review` and the PR Agent plugin's `pr-agent-review` are distinct; neither substitutes for the other. Follow the standards' setup, execution, scope reconciliation, and unavailable-result rules.
- Request analysis only from all supporting skills/plugins: no posting, labels, remediation, commits, or pushes. Independently validate and deduplicate their findings against source and existing comments before adding drafts.
- If the PR head changes, re-ground the affected review and check/scan evidence before concluding. Never describe a PR as merge-ready or recommend merging unless all reported checks pass, including non-required checks, and review blockers are resolved. Missing, skipped, cancelled, pending, or failed checks are not green. Diagnose and monitor within authorized scope; report any verified human-action blocker without claiming readiness.

## CRQ Review

- Verify the exact change record, production target, release version/artifact, implementation/validation/rollback plans, test evidence, and the PRs mechanically or materially affecting production behavior. Reconcile the release against the prior deployed version; do not infer release scope from a branch name or a handpicked PR list.
- Apply ReviewStandards' CRQ requirements, including release-PR inclusion/exclusion, the prescribed PR-list heading and coverage presentation, production-scope separation, and evidence-record restrictions. Identify missing evidence and unsafe or incomplete operational procedures.
- Run the full PR Review workflow above for each in-scope PR, including Walmart `pr-review` as a subset and the required PR Agent tracks. Reuse verified evidence for an unchanged revision rather than rerunning blindly; distinguish historical release evidence from live checks on a different head.
- Keep the review in shared/aidocs/; do not edit submitted/frozen testing evidence or the external CRQ. Link the canonical release/testing records rather than turning evidence payloads into review work logs.

## Permission Boundaries

Drafting is not posting or approval. Obtain explicit user permission before publishing comments, approving a code review, changing the CRQ, or applying fixes. Respect the approved-PR commit boundary. Supporting skills' automation does not grant permission or bypass policy-disabled scans. Record unavailable results as incomplete, never as a clean review.
