# Mobile Agentic Development

## Summary

- Goal: reproduce the productive parts of the personal MacBook agentic-development workflow on Android without turning the phone into a miniature IDE or terminal.
- The essential human loop has two distinct services:
  - **Agent Conversation Service** — rich, native-quality conversation UI for steering agents, reviewing plans and tool activity, queuing follow-ups, seeing history, approvals, model/cost information, and parallel work.
  - **Markdown Rendering Service** — fast navigation through the current rendered Markdown folder tree: project state, architecture, decisions, pending decisions, investigations, tasks, work history, rules, and reference documents.
- Git should remain the durable history, rollback mechanism, and device-handoff protocol. It should not be the live synchronization mechanism between an agent edit and the rendered document being read on the same device.
- Device handoff may require a clean commit/push to origin. That is an acceptable discipline and is much simpler than exposing dirty MacBook working trees to Android.
- IntelliJ IDEA remains the preferred desktop work surface. The mobile architecture does not require replacing it with Cursor, VS Code, Claude Code, Codex, or a terminal UI.
- The always-on M4 Mac Mini is a useful optional execution host, not necessarily the canonical personal-development workstation.
- The strongest current near-term architecture is **Android rich remote control of an agent running against a real multi-repo working directory on an always-on host**, paired with a near-real-time Android Markdown mirror rendered by Obsidian.
- GitHub Copilot Remote Control is especially promising because it already uses the existing Copilot subscription/model ecosystem, supports GitHub Mobile, JetBrains, and local CLI sessions, and supports sessions started in a parent directory containing multiple repositories.
- A cloud-agent architecture remains worth investigating because it removes dependence on the Mini, but isolated cloud workspaces and branch/PR-oriented state may conflict with the desired shared mutable document model.
- ChatGPT is a particularly strong candidate for the mobile Agent Conversation Service because its Android and Live voice experience is already excellent and it can read the connected GitHub repository. The standard GitHub connection currently cannot write repository contents; a writable custom MCP path should be investigated.
- Security philosophy: maximize agent autonomy *inside a deliberately bounded capability envelope*. Prefer architectural capability limits over repeated interactive approval prompts.

## Existing Workflow

### Cognitive State

- Markdown is the durable human/agent cognitive state, not incidental documentation.
- Project documents preserve information that cannot safely be reconstructed from source code or chat history:
  - goals and principles
  - architecture and schemas
  - workflow rules
  - pending and resolved decisions
  - pending and resolved investigations
  - planned tasks
  - active work
  - rationale and rejected approaches
  - work history
- The project-document templates formalize this distinction:
  - **Tasks** preserve project-level planned work.
  - **Active Work** is the mutable present and explicit cross-session handoff state.
  - **Pending Decisions / Decisions** preserve choice state and rationale.
  - **Pending Investigations / Resolved Investigations** preserve epistemic state.
  - **Work Log** preserves why effort was spent and how the project moved toward its goal.
- This state layer is intentionally richer than chat history and more semantic than Git history.
- Conversation history is chronological; project state is semantic. The Markdown tree continuously compiles conversations, investigations, code changes, and decisions into current state.

### Agent Constitution

- `docs/AgentRules.md` in the tools repo is the global, cross-repo, cross-model constitution.
- Project-level `AGENTS.md` supplements it rather than replacing it.
- The tools repo is canonical; home-directory and workspace-specific instruction files are adapters.
- Code Puppy automatically loads the global `AGENTS.md` adapter.
- GitHub Copilot uses repo-local `.github/copilot-instructions.md` adapters.
- Any viable mobile agent environment must preserve automatic constitution loading rather than depending on Brian remembering to paste or mention the rules.
- The tools repo is not merely documentation. Its skills, commands, templates, rules, and other machinery are part of the execution environment.
- Therefore a viable agent workspace must support the target project repo plus the tools repo simultaneously.

### Concurrent Mutation

- Multiple agents may operate concurrently on shared Markdown.
- AgentRules defines `fhold` and `safewrite` coordination for Git-tracked Markdown.
- Agents re-read immediately before writes and use lightweight coordination/CAS-style protection where needed.
- The intent is to preserve a shared mutable working state rather than creating branch/worktree/PR overhead for every concurrent agent.
- Git history remains important for recovery when an agent makes a mistake that is noticed only after subsequent changes.

### Desktop Work Surface

- IntelliJ IDEA is currently preferred because the aggregate workflow matters more than any single AI feature:
  - linked/content-root handling
  - Git integration
  - strong diff review
  - multiple rendered Markdown documents
  - Markdown find/structure/table behavior
  - agent integrations
  - general database/debug/HTTP IDE capability
- Cursor and VS Code observations in `Tools.md` should be treated as potentially stale where they have not been re-tested recently.
- Code Puppy has a shared webview/protocol implementation across JetBrains, VS Code, and Cursor, but it is not currently part of the personal home workflow.
- GitHub Copilot is the normal personal agent harness. Model flexibility and cheap capable models are materially valuable.

## Mobile Requirements

### Agent Conversation Service

Hard requirements:

- Android-optimized rich GUI, not a terminal emulator.
- Rich Markdown/rich-text conversation rendering.
- Good scrolling and long-session navigation.
- Persistent conversation/session history.
- Prompt history that can be inspected without flooding the main transcript.
- Tool and shell activity shown as compact expandable elements.
- Approval UI appropriate to agent operations.
- Ability to queue or steer follow-up prompts.
- Visibility into model selection and usage/cost.
- Practical support for parallel agents or sessions.
- Access to the active project repo and the tools repo in the same effective workspace.
- Automatic access to AgentRules and relevant skills/commands.
- Agent writes must become visible to the Markdown Rendering Service without requiring a Git commit as synchronization.
- Voice interaction is highly valuable; ChatGPT Live is currently the benchmark.

### Markdown Rendering Service

Hard requirements:

- Android-native or equivalently good touch UI.
- Rendered Markdown, not raw source as the normal reading mode.
- Folder-tree navigation across a substantial document hierarchy.
- Fast search and document navigation.
- Multiple project documents, not a single-note workflow.
- Wide-table behavior that remains usable on a phone.
- External file changes must be noticed promptly.
- Must be able to render the same evolving state the agent is editing.

Obsidian is the current leading candidate. GitHub's Android Markdown rendering is also usable enough to serve as an interim fallback.

## Git Boundary

Git has two valuable roles:

- **History / recovery** — frequent commits provide known-good checkpoints and precise rollback.
- **Device handoff** — switching among MacBook, Mac Mini, and Android may require commit/push from the departing device and pull/synchronization on the arriving device.

Git should not mediate the interactive mobile loop:

```text
tell agent
    ↓
agent changes Markdown
    ↓
switch to renderer
    ↓
read changed rendered Markdown
```

There should be no required commit/push/pull between the middle two steps.

## Candidate Architectures

### ChatGPT Android + Writable Repository / MCP

Potentially the best human interface if write access can be solved.

- ChatGPT Android and Live provide a strong rich conversation and voice surface.
- The connected GitHub integration can read the tools repo, including AgentRules, templates, and other machinery.
- A direct attempt to create `docs/MobileAgenticDevelopment.md` through the standard GitHub integration failed with GitHub `403 Resource not accessible by integration`.
- ChatGPT-side permission was already configured as **Allow all actions**, so the failure is downstream in the GitHub integration's granted repository permissions.
- The standard OpenAI GitHub connection is effectively read-oriented for this use.
- A custom writable MCP app should be investigated.
- The especially interesting architecture is not merely GitHub API write access, but:

```text
ChatGPT Android / Live
        │
        │ custom MCP
        ▼
M4 Mini execution environment
        │
        ├── tools/
        ├── target project repos
        ├── AgentRules
        ├── skills / commands
        ├── fhold / safewrite
        └── normal filesystem + shell tools
```

- If supported cleanly on the personal ChatGPT plan, this could make ChatGPT itself the preferred Agent Conversation Service.

### Copilot Remote Control on an Always-On Host

Strong prototype candidate.

- Copilot Remote Control allows a local Copilot CLI session to be monitored and steered from GitHub Mobile or the web.
- The execution remains on the host machine; GitHub is the control plane.
- A session can be started from a parent directory containing multiple repositories rather than requiring the working directory itself to be one Git repo.
- That maps well to a host layout such as:

```text
~/src/
├── tools/
├── EpiLog/
├── CaptainsLog/
└── other-project/
```

- The always-on M4 Mini is a natural host for Android sessions.
- The MacBook remains the normal desktop workstation.
- Device handoff can use Git origin rather than attempting to synchronize dirty MacBook and Mini working trees.
- Copilot CLI supports highly permissive execution, including YOLO/allow-all modes and deny overrides.
- This may provide a better high-autonomy execution environment than the IDEA Copilot tool host, whose approval prompts can be controlled by the IDE/plugin rather than by the model.

### Copilot Cloud Agent

Worth investigating, but not yet preferred.

Advantages:

- No personal execution host needs to remain available.
- Android becomes a genuine control surface for cloud-running work.
- Agent work can continue while personal computers are unavailable.

Concerns:

- Cloud coding-agent workflows naturally favor isolated workspaces, branches, PRs, and review.
- The desired cognitive workflow instead favors a shared mutable Markdown state with lightweight write coordination.
- The cloud workspace must expose both the target repo and tools machinery reliably.
- The Markdown Rendering Service must somehow see current cloud-workspace Markdown before a Git handoff; otherwise Git returns to the live cognitive loop.

### OpenAI Codex Remote / Cloud

Strong comparison candidates.

- The mobile Remote model treats the phone as a control plane rather than a tiny terminal.
- Remote execution can preserve a rich phone interface while work happens on a host.
- Cloud execution removes the host dependency but tends toward isolated workspaces.
- Multi-repo access, automatic AgentRules loading, subscription economics, and exposure of current Markdown to the renderer need direct testing.

### Claude Code Mobile / Remote

Important benchmark because the Claude Code team is visibly pushing phone-first agent supervision.

- Public high-end workflows emphasize many parallel local/cloud agent sessions.
- Phone usage centers on starting, checking, steering, and reviewing delegated work.
- The dominant model is delegation and supervision rather than making the phone itself a miniature development workstation.

### Android-Local Agent

Architecturally elegant but currently weak on human UX.

- Termux can provide a local Unix userland, real Git, shell tools, and an agent process.
- A local checkout could be opened directly by both the agent and Obsidian, eliminating live synchronization entirely.
- The failure is the Agent Conversation Service: a terminal agent UI is explicitly unacceptable.
- This path becomes interesting again only if a mature Android-native frontend can attach to a local agent protocol while retaining rich conversation/history/tool UX.
- Code Puppy's shared webview/protocol architecture may eventually provide building blocks.

### Codespaces / Browser IDE

Fallback rather than target.

- Technically supplies repository access, agent capability, editor, Git, and Markdown preview.
- Human experience is a desktop IDE compressed into a phone browser.
- It solves compute availability by degrading the interaction model, which is the wrong trade for this workflow.

## What Leading Agentic Developers Actually Do

### Mobile as Control Plane

The leading public workflows increasingly treat agents as parallel delegated workers:

```text
human intent
    ↓
agent session(s)
    ↓
code / tests / running application / PR
    ↓
human review and steering
```

Phone-first power users are generally not reproducing a complete desktop IDE on the phone. The phone becomes a manager's console for remote/local/cloud workers.

This explains how highly productive developers can report that the phone has become a major work surface even when it lacks a rich project-document tree.

### Where Their State Lives

Many public agentic-development demonstrations do not expose a durable human-readable project-state tree comparable to the tools/project-document system.

State is commonly distributed among:

- source code
- tests
- issue/PR descriptions
- Git history
- agent conversation history
- temporary agent plans
- instruction files such as `AGENTS.md` / `CLAUDE.md`
- the running application
- human memory

This can work especially well when the primary artifact is directly inspectable: a web application, test suite, compiler output, or bounded code change. The running product itself becomes a major human feedback surface.

It becomes weaker for multi-month work where important state is not inferable from implementation: rationale, architectural intent, unresolved decisions, rejected alternatives, operational constraints, investigation state, and the exact next work to resume.

### Assessment

The current workflow is not behind the state of the art in the important sense.

It is **ahead of the mainstream in externalizing durable cognitive state**, while the mainstream is ahead in **delegation mobility and parallel remote-agent orchestration**.

The opportunity is to combine them:

```text
             Agent Conversation Service
                       │
                       ▼
            shared project working state
              /                  \
      executable state       cognitive state
      code/tests/app         Markdown tree
                                  │
                                  ▼
                      Markdown Rendering Service
```

The target is therefore not to imitate phone-first developers by discarding the document tree. It is to import their mobile control-plane model while preserving the document tree as a first-class human feedback surface.

## Why Conversation Alone Is Insufficient Here

Conversation history is optimized for chronology. Project state is organized semantically.

A long-running project needs questions such as these answered directly:

- What is currently decided?
- What is still undecided?
- What empirical questions remain?
- What is actively being worked?
- What must not be forgotten?
- Why was this architecture selected?
- What was rejected?
- Which constraints govern all future work?
- What should a fresh agent know before acting?

A chat transcript can contain every answer and still be a poor representation of current state because later turns supersede earlier ones and relevant facts are scattered across chronology.

The project-document model continuously compiles chronology into current semantic state.

The Markdown tree is effectively a materialized view over conversations, experiments, code changes, and decisions. Git supplies history for that materialized state.

## Security and Autonomy

### Philosophy

The desired model is not “trust the agent.”

It is:

> **Maximum autonomy inside deliberately bounded authority.**

Agents are assumed capable of serious mistakes. Interactive approval prompts are not the primary defense.

### Existing Hard Boundaries

- **Financial authority** — agents should not have unrestricted access to money or financial actions.
- **Communication authority** — strict rules govern agents communicating as Brian to other humans. Reading/drafting and actually sending/publishing should remain distinct capabilities.
- **Recoverability** — important state is backed by Git origins, cloud storage, backups, and other recoverable systems so destructive filesystem behavior has a bounded cost.

### Additional Boundary: Credentials and Exfiltration

Backups protect integrity and availability but do not reverse:

- leaked credentials
- leaked private data
- public publication
- messages sent to humans
- destructive external API actions
- irreversible account/security changes

Therefore external authority should be scoped independently of local filesystem autonomy.

### Chrome Canary as Capability Compartment

The existing use of Chrome Canary is a good example of capability-oriented security.

- Agents drive a browser profile with a deliberately limited set of cookies and credentials.
- At work, the profile can reach tools the agent needs, such as Lenses and Grafana, without automatically inheriting every credential from Brian's normal browser identity.
- The browser profile functions as a practical capability compartment.

This should be preserved and generalized.

### Valet-Key Accounts

Agentic AI increases the value of service-level delegated credentials analogous to a valet key.

Ideal web services would allow an agent-specific identity/session with restrictions such as:

- read but not write
- create but not delete
- modify individual objects but not perform mass destructive operations
- no billing/payment changes
- no account recovery/security changes
- no user/permission administration
- bounded transaction or resource limits
- explicit audit trail
- independently revocable credentials

Where a service offers OAuth scopes, fine-grained tokens, service accounts, roles, or separate profiles, prefer those over giving the agent Brian's full interactive identity.

### Permission UX

The preferred security architecture is Unix-like:

- grant the agent process the capabilities it needs
- withhold capabilities it should never exercise
- inside the permitted envelope, avoid repetitive confirmation prompts

This is superior to asking for approval on routine shell/file operations dozens of times per day.

The M4 Mini could therefore become a deliberate high-autonomy agent appliance:

```text
agent environment
 │
 ├── filesystem       broad
 ├── shell            broad
 ├── git              broad
 ├── compilers        broad
 ├── browser          scoped Canary profile
 ├── GitHub repos     broad where appropriate
 │
 ├── financial auth   absent / tightly scoped
 ├── send-as-Brian    gated
 └── crown-jewel creds minimized
```

Inside this capability envelope, YOLO-style execution is reasonable.

## Markdown Rendering

Obsidian is the current leading Android candidate.

Potential topology:

```text
M4 Mini working directory
        │
  continuous file mirror
        │
Android device-storage vault
        │
     Obsidian
```

The Android copy can initially be read-mostly during phone sessions if the agent is authoritative on the Mini. That removes most conflict complexity.

GitHub Android Markdown rendering is an acceptable interim fallback if direct repository commits are the available transport.

## Current Recommendation

Prototype the architecture that changes the fewest existing assumptions while separately testing the potentially superior ChatGPT path.

Near-term Copilot prototype:

```text
Android GitHub Mobile
  Agent Conversation Service
            │
            │ Copilot Remote Control
            ▼
Always-on M4 Mini
  parent workspace containing
  tools + target repos
            │
            ├── frequent Git checkpoints
            │
            └── live Markdown edits
                        │
                 filesystem mirror
                        ▼
Android Obsidian
  Markdown Rendering Service
```

Potential preferred architecture if writable ChatGPT MCP works well:

```text
Android ChatGPT + Live
  Agent Conversation Service
            │
            │ writable custom MCP
            ▼
bounded M4 Mini agent environment
  tools + target repos + agent machinery
            │
            └── live Markdown edits
                        │
                 filesystem mirror
                        ▼
Android Obsidian
  Markdown Rendering Service
```

## Pending Investigations

### Writable ChatGPT MCP

- Determine exactly what writable custom MCP capabilities are available on the personal ChatGPT plan.
- Determine whether an MCP service on the M4 Mini can expose filesystem/shell/repository operations safely to ChatGPT Android.
- Determine whether ChatGPT Live conversations can invoke the same connected tools smoothly.
- Preserve AgentRules, skills, commands, `fhold`, and `safewrite`.
- Prefer actual working-tree operations over GitHub-API-only commits if possible.

### Copilot Remote Multi-Repo Behavior

- Test a Remote Control session started at the common parent of `tools` and one target repo.
- Verify read/write access across both repos.
- Verify the sandbox/approval configuration needed for sibling access.
- Verify which Copilot instruction files load automatically when the working directory is above repo roots.
- Determine the cleanest adapter that guarantees AgentRules is always loaded.
- Test YOLO/allow-all behavior on the personal Mini and document the remaining host-enforced prompts.

### GitHub Mobile Conversation UX

- Evaluate the current Android interface directly against the Agent Conversation Service requirements:
  - rich rendering
  - tool-call collapse/expansion
  - prompt/session history
  - queued prompts
  - parallel sessions
  - plan review
  - approvals
  - model selection
  - usage visibility
  - voice input

### Copilot Cloud Agent

- Test whether one cloud environment/session can access both a target repo and tools.
- Determine how global rules/skills can be installed into every cloud task.
- Determine whether current Markdown can be exposed to an Android renderer before Git commit/push.
- Compare cost/model-selection behavior with the existing Copilot personal workflow.

### Codex Remote and Codex Cloud

- Compare Android conversation UX with GitHub Mobile.
- Test multi-repo host access and automatic AgentRules loading.
- Determine how ChatGPT-plan Codex usage compares economically with Copilot usage.
- Test whether cloud environments can install the tools constitution and multiple repositories without making isolated workspaces too expensive cognitively.

### Markdown Mirror

- Prototype Obsidian Android with a device-storage vault.
- Mirror one Mini project folder to Android using a continuous filesystem synchronizer.
- Measure agent-write-to-rendered-visible latency.
- Verify that external writes update an already-open document reliably.
- Test large Markdown documents, wide tables, search, outline navigation, internal links, and folder navigation.
- Keep Android read-only initially to eliminate synchronization conflicts.

### Agent Credential Architecture

- Inventory the credentials currently visible to agent-driven Chrome Canary and local agent processes.
- Preserve the Canary-profile compartment.
- Prefer scoped OAuth tokens, fine-grained GitHub tokens, service accounts, and role-limited identities where services support them.
- Identify irreversible external authorities that should remain unavailable even in YOLO execution.
- Document the intended capability envelope in the tools repo so every harness can implement the same policy.

### Android-Local Rich Agent Client

- Continue watching the ecosystem for an Android-native client that can drive a local agent process against an Android checkout.
- Revisit if it reaches GitHub Mobile / ChatGPT quality.
- Do not accept terminal interaction as the normal human interface.

### Cursor Re-evaluation

- Re-test current Cursor rather than trusting older observations in `Tools.md`.
- Focus on native WYSIWYG Markdown search, wide tables, structure/outline, external-file reread, multi-root behavior, and compatibility with the locally built Code Puppy extension.
- Cursor is an optional desktop alternative, not a prerequisite for mobile work.

## Proposed Next Steps for Investigation

The investigation should prioritize the smallest experiments that can falsify the current recommendation before expanding into broad product comparisons.

### Establish the host and workspace boundary

- Create a disposable M4 Mini workspace containing the tools repo and one non-critical target repo.
- Start a Copilot Remote Control session from their common parent directory.
- Verify repository discovery, instruction loading, AgentRules availability, sibling-repo read/write behavior, and the actual approval prompts.
- Record the exact host layout and setup steps needed to reproduce the session.

### Prove the live Markdown loop

- Select one small project-state document and one folder-tree renderer.
- Have the remote agent make a visible edit without committing it.
- Confirm that Android sees the external change while the document is already open.
- Measure edit-to-visible latency, stale-cache behavior, conflict behavior, and recovery after the host or synchronizer restarts.
- Keep Android read-only until this loop is reliable.

### Define the minimum viable security envelope

- Inventory which credentials and browser sessions are visible to the Mini agent.
- Remove or isolate financial, account-recovery, send-as-Brian, and other irreversible authorities before enabling permissive execution.
- Test scoped GitHub and service credentials with an explicit destructive-operation boundary.
- Document the resulting capability envelope and the remaining host-enforced prompts.

### Test the ChatGPT MCP alternative

- Build the smallest read/write MCP proof of concept against a disposable directory, not the canonical tools or project repositories.
- Verify authentication, Android invocation, Live compatibility, concurrent access, auditability, and failure handling.
- Re-run the same live Markdown loop and security tests.
- Treat the MCP path as preferred only if it beats Copilot Remote Control on both interaction quality and operational safety.

### Compare only after the baseline works

- Use a compact scorecard for GitHub Mobile, ChatGPT Android/Live, Codex Remote, and cloud-agent options.
- Compare them against the same requirements: rich conversation, multi-repo access, constitution loading, live file visibility, voice, parallel sessions, cost, and recoverability.
- Stop investigating candidates that fail a hard requirement rather than accumulating feature notes.

## Success Criterion

A phone session should feel like this:

```text
open rich agent conversation
        ↓
discuss architecture / decision / investigation
        ↓
agent reads constitution + project state
        ↓
agent edits one or more Markdown documents
        ↓
switch apps
        ↓
browse the changed documents rendered in their folder tree
        ↓
switch back
        ↓
steer the agent again
```

No terminal interaction is visible to the user. No PR review is required merely to read current state. No Git operation is required between agent edit and human reading. Git remains available underneath for frequent recovery checkpoints and for handoff among MacBook, Mini, and Android.

## Work Log

### 10.04 Sun Mobile Agentic Workflow Investigation

- Distilled the Android agentic-development investigation into a durable document.
- Identified the separation between Agent Conversation Service and Markdown Rendering Service.
- Established Git as history/device-handoff rather than live edit/render synchronization.
- Identified Copilot Remote Control on the always-on M4 Mini as a strong prototype because it preserves existing Copilot economics, real filesystem/tool access, and the multi-repo workspace model.
- Identified ChatGPT Android + Live + writable custom MCP as a potentially superior Agent Conversation Service if writable personal-plan MCP access proves viable.
- Verified that the standard connected GitHub integration can read the tools repo but a direct repository-content write was rejected with HTTP 403.
- Compared the document-centric workflow with public state-of-the-art agentic development and concluded that mobile control-plane orchestration is mainstreaming faster than durable human-readable cognitive-state management; the target architecture should combine both.
- Refined the security model from “YOLO plus backups” to maximum autonomy inside bounded authority.
- Preserved Chrome Canary as a deliberate credential/capability compartment and identified valet-key service identities as the desirable long-term model for agent web access.
