# AI Agent Session & Project Management — Comparative UX Research (Langley Comps)

2026.09.29 — Scope: UX patterns and tools for managing one user's current/recent AI-agent conversations, sessions, and multi-agent/multi-session projects, with emphasis on **cross-agent** solutions over single-vendor native history. The comparative survey uses product pages, documentation, and GitHub READMEs collected on 2026.09.29; the conversation-list comparison and JetBrains Air assessment use documentation and local inspection collected on 2026.10.14. Unverifiable claims are marked explicitly. Product capabilities and support status are dated observations, not guarantees about later releases.

## Key Takeaways

- **[JetBrains Air](#jetbrains-air) is a candidate active agent host, not just another chat-history sidebar.** Its custom Agent Client Protocol (ACP) integration separates the IDE frontend from the agent runtime. It is a potential JetBrains-side solution and architectural inspiration for Langley, but does not establish a shared control plane across IDE vendors or repositories.
- **Git-worktree-per-task isolation** is the dominant UX pattern for running parallel coding agents: Conductor, Crystal/Nimbalyst, Vibe Kanban, and Claude Squad all use it independently.
- **This category churns fast.** Of ~20 tools surveyed, three have been deprecated/sunset or gone stale within the last 12 months: Crystal (deprecated Feb 2026, successor Nimbalyst), Vibe Kanban (company BloopAI shut down Apr 2026; product survives only as community OSS), and the tmux-resurrect/tmux-continuum plugin pair (no commits since Aug 2024).
- **Vendor consolidation is visible in real time**: Windsurf's Cascade docs now redirect to Cognition/Devin Desktop documentation, reflecting the Windsurf↔Cognition merger — a single-vendor "native history" feature got absorbed into a different vendor's product overnight.
- **Cross-agent tools split into two families**: (1) passive history/index layers that sit beside your existing tools and capture transcripts (SpecStory, ThreadLens, Happier), and (2) active session hosts that actually launch/control multiple agent CLIs in isolated workspaces (Conductor, Claude Squad, Vibe Kanban).
- **Mobile/remote steering** ("start on desktop, approve from phone") is an emerging pattern: Happy, Factory.ai's Droid, and GitHub Copilot's mobile app all ship this today.
- **Cloud-async dashboards remain single-vendor**: OpenAI Codex Cloud, Google Jules, Cursor Background Agents, and Devin each have their own task list/dashboard, but none orchestrate a competitor's agent — the one clear cross-vendor dashboard is GitHub's Copilot "Agents" surface, which can invoke Claude and Codex alongside Copilot itself.
- **Terminal multiplexers (tmux/Zellij) are being repurposed** as the substrate for agent orchestration rather than replaced — Claude Squad and Tmux Orchestrator both wrap tmux rather than reinventing pane/session management.

## Agent Conversation List

- Status: queued/running/waiting/completed/failed state; pending approval or user input, unread activity, unsent draft, and errors
- Title
- Started
- Idle
- Cost
- uncommitted files
- model
- expanded
  - anchor file
  - current file
  - git diff lines
- expanded more
  - latest prompt with time
  - latest output with time
- obvious
  - repo, branch
  - harness
  - IDE
- out of scope
  - Conversation relationships** — parent/fork, related parallel sessions, peer chats, delegated agents, and whether workspaces are shared or isolated.
  - Attached context — linked repositories, issues or pull requests, files or selected code, and the originating request.
- **Organization and actions** — search, filters, grouping and sorting, pinned/favorite/archive state, and direct resume/open/fork/archive/delete actions.

### Conversation table mockups

**One conversation, one tight row.** No cards, timestamp sentences, or repeated badges. Titles come from the supplied screenshot; their completed endings and all other values below are illustrative mock data, not observed telemetry or Air capabilities.

#### Default: dense list

**Conversations**　⌕ Search…　All ▾　◴ ↑　＋

| | | | | | | |
| :---: | :--- | ---: | ---: | ---: | ---: | :--- |
| ▶️ | phantom-agent | ✦22m | ◴0m | $.18 | Δ2 | elite |
| ❓ | enable copilot in IDEA | ✦1d | ◴8m | $.42 | Δ1 | elite |
| ✅ | Wysiwyg editor: what doe… | ✦2d | ◴1d | $1.26 | Δ0 | elite |
| ! | code-puppy extension not… | ✦2d | ◴2d | $.63 | Δ3 | elite |

No visible column labels. Accessible column names and hover/focus labels explain the compact tokens. Status uses the vocabulary below. An unread dot sits beside the title; a tiny pencil marks an unsent draft. These are independent of lifecycle state. Render all status symbols in a fixed-width icon slot; platform emoji width must not shift the metrics.

Titles contain at most **25 displayed characters, including the single Unicode ellipsis `…`** when truncated: retain the first 24 grapheme clusters, then append `…`. Never split a composed character or emoji. Full titles appear on hover and keyboard focus, and remain the accessible names.

**✦** = born: age since conversation creation. **◴** = idle: time since the last agent/user activity, not a paused execution state. These are metric prefixes, not lifecycle statuses. Use one rounded-down unit, with minutes as the minimum resolution: ages below one minute display `0m`, never seconds (`◴0m`, `◴8m`, `✦3h`, `✦2d`); exact timestamps live on hover/focus. Spend retains its currency symbol but omits a leading zero below one dollar (`$.18`, `$1.26`, `$0`); unknown spend is `$?`, not zero. **Δ3** = three uncommitted files; **Δ0** = none. An optional breakdown **Δ2+3-1** means two modified, three added, and one deleted file; these categories are disjoint, not line counts. Exact paths and counts live in the expanded view. `elite` is the display alias for `auto-elite`.

Repository `relationship-shared`, branch `main`, harness Code Puppy, IDE IDEA, and permission mode YOLO live in a quiet scope line above the table—not four copies in every row. Mixed values become optional columns; shared values stay in the scope line.

#### Status glyphs

Reuse [Status Vocabulary](../.wibey/docs/StatusVocabulary.md#status-definitions) where its meaning fits; do not infer investigative or deployment phases from generic agent execution.

| Glyph | Conversation status | Meaning / vocabulary reuse |
| :---: | :--- | :--- |
| *(blank)* | Queued / unstarted | Not executing yet; preserve the vocabulary’s blank unstarted status. |
| ▶️ | Running | STARTED / IN_PROGRESS: agent is executing, not necessarily INVESTIGATING or FIXING. |
| 🛑 | Action needed | BLOCKED: approval, authentication, or another external action is required. |
| ❓ | Answer needed | BLOCKED: a question or decision requires the user. |
| ⏰ | Awaiting | A committed, expected event is pending; not generic inactivity. |
| 👀 | Under review | Awaiting another person’s feedback. |
| ⏸️ | Paused | Intentionally suspended; never use merely because idle time is increasing. |
| ! | Failed | Conversation-specific execution error; not FIX_FAILED, which means a deployed fix failed. |
| ❌ | Canceled | Explicitly canceled, not failed. |
| ✅ | Done | RESOLVED / DONE: the requested work is complete, not merely a finished response. |

Use accessible status names and shape as well as color. Creation and idle glyphs stay in their metric columns, never in the status slot. Unread and draft indicators remain independent.

#### Expanded: one extra line, not a detail form

Select **phantom-agent**, then expand with **→** or its disclosure control:

| | | | | | | |
| :---: | :--- | ---: | ---: | ---: | ---: | :--- |
| ▶️ | ▾ phantom-agent | ✦22m | ◴0m | $.18 | Δ2+3-1 | elite |

　↳ anchor `phantom-agent` → current `phantom-doctor`　 **+38 −6 lines**　[More ▾]

**More** adds the latest exchange inline, clipped to one line per message:

> **You · 3m**　Add a minimal off-VPN install job; preserve proxy settings.
>
> **Agent · 0m**　Restore trap added. Checking the failure path…

Files open on click; the change summary opens the diff. Keep the rest of the list visible. Expansion does not resume execution.

#### Sidebar: keep the signal, drop the columns

At narrow widths, retain status, the same 25-character title limit, and one right-aligned activity token. Available width may truncate titles further. No miniature spreadsheet and no three-line cards.

| | | |
| :---: | :--- | ---: |
| ▶️ | phantom-agent | ◴0m |
| ❓ | enable copilot in IDEA | ◴8m |
| ✅ | Wysiwyg editor: what doe… | ◴1d |
| ! | code-puppy extension not… | ◴2d |

#### Visual and interaction contract

- **Density:** 24px desktop rows, 12px text, 14px glyph column, and 4px inter-column gaps; tabular numerals and right-aligned metrics. Title is capped at 25 characters and absorbs remaining width up to that limit. Metrics size to their content; no visible header row, vertical gridlines, pill badges, or per-row action chrome. Blank header cells above are a Markdown rendering accommodation, not UI labels.
- **Hierarchy:** title high contrast; metrics quieter but still accessible. Very faint horizontal separators, a subtle selected-row tint and focus edge. Amber action/question glyphs, green running triangle, muted completion check, red error mark; shape and accessible names carry meaning without color.
- **Triage:** default activity age ascending (`◴ ↑`); an Attention filter isolates approvals, questions, and failures. A named Sort control selects the metric and direction without requiring visible column headers. Hover/focus reveals resume, archive, and overflow actions without shifting columns.
- **Keyboard:** ↑/↓ select, → expands, ← collapses, Enter opens the conversation, / focuses search, Esc clears it. Provide named buttons, announced sort/expansion state, and visible focus. Full truncated titles appear on hover and keyboard focus.
- **Touch:** use 44px rows and visible overflow controls for coarse pointers. Compact must not mean impossible to hit.

## Categorization Framework


| Category                                           | What it answers for the user                                                                    | Cross-agent?                                     |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 1. Cross-agent session indexes                     | "Show me every AI conversation I've had, across all my tools, in one searchable place"          | Yes, by design                                   |
| 2. Agent-work/project management                   | "Show me the list/board of tasks my async cloud agents are running or finished"                 | Mostly single-vendor; one cross-vendor exception |
| 3. Native IDE history                              | "Show me my past chats in this one IDE" (baseline/contrast)                                     | No — single product                             |
| 4. Cross-workspace/session managers                | "Let me save/restore/switch terminal or editor sessions that happen to be running an agent CLI" | Agent-agnostic by construction                   |
| 5. Desktop agent clients                           | "Give me an app to launch and watch several agent sessions running in parallel"                 | Varies (2–6 CLIs supported)                     |
| 6. Terminal multiplexers as agent-control surfaces | "Run a fleet of agent CLI instances from one terminal, each isolated"                           | Yes, multi-CLI                                   |
| 7. Agent-control surfaces (observability)          | "Trace/monitor/debug agent runs regardless of framework or vendor"                              | Yes, framework-agnostic                          |

---

## 1. Cross-Agent Session Indexes

**SpecStory** — https://github.com/specstoryai/getspecstory (specstory.com blocked automated fetch with HTTP 403; verified via GitHub instead). Saves AI coding conversations to local `.specstory/history/` Markdown, with optional sync to SpecStory Cloud for cross-device search/sharing. A "Lore" feature mines saved history into reusable agent skills. IDE extensions cover Cursor and VS Code/GitHub Copilot Chat; a CLI wrapper additionally covers Claude Code, Codex CLI, Cursor CLI, Droid CLI, Gemini CLI, DeepSeek TUI, Antigravity CLI, Qwen Code, Pi, Grok Build, and OpenCode. CLI/Lore are Apache-2.0 OSS; IDE extensions are free closed-source; Cloud tier requires signup with no published price found.

**ThreadLens** — https://github.com/hanityx/threadlens. Local-first, no-cloud/no-account tool to search, review, back up, and safely clean up AI coding session transcripts from one place. Explicitly supports Codex, Claude, Gemini, and Copilot with cross-provider keyword search and dry-run-before-delete cleanup; ships as TUI, Electron desktop, and web variants. MIT/free, actively maintained (v0.3.1, CI passing, public roadmap).

**Happier** — https://github.com/happier-dev/happier. Multi-device "control room" that doubles as a cross-agent session/history layer: one agent can spawn subagents on a different engine, and the underlying agent can be switched mid-session with context carried over. Supports Claude Code, Codex, OpenCode, Gemini CLI, Cursor, GitHub Copilot, Grok, Antigravity, Qwen Code, Kimi, and any ACP-speaking agent. MIT/free, self-hostable, optional hosted relay at cloud.happier.dev.

*Unverified, noted only:* a self-hosted "recensa" transcript viewer (Claude-Code-only, out of cross-agent scope) and a "Claude-Code-History-VSCode" extension surfaced via GitHub's chat-history topic — neither independently confirmed live.

---

## 2. Agent-Work / Project Management (async cloud-agent dashboards)

**OpenAI Codex Cloud** — https://learn.chatgpt.com/docs/cloud (chatgpt.com/codex and openai.com/codex returned 403 to automated fetch; docs mirror confirmed the behavior instead). Each cloud task runs in its own isolated workspace that keeps going while your machine is asleep/offline; reviewed via web, mobile, desktop app, or CLI ("list recent cloud chats and check their status"). Docs describe per-task review (diff/results/PR), not a single side-by-side multi-task board. Single-vendor (OpenAI models only); access via ChatGPT Plus/Pro/Business/Enterprise/Edu/Go plans.

**GitHub Copilot coding agent — Agents dashboard** — https://docs.github.com/en/copilot/concepts/agents/cloud-agent/agent-management. Two surfaces: a repo-scoped "Agents" tab listing active/past sessions with real-time logs, and a centralized page at github.com/copilot/agents. **This is the one clearly cross-vendor dashboard found**: it can invoke Anthropic Claude and OpenAI Codex as agents alongside Copilot itself, plus partner-built "agent apps." Requires a Copilot plan with coding-agent entitlement (consumes premium requests/credits).

**Google Jules** — https://jules.google/. Browser dashboard: pick repo/branch, get a plan, review a diff, receive a PR; can also trigger from a GitHub issue label. Single-vendor (Gemini only). Tiers double as the parallel-task cap: free (15 tasks/day, 3 concurrent), Jules in Pro (100/day, 15 concurrent, Gemini 3 Pro), Jules in Ultra (300/day, 60 concurrent).

**Cursor Background/Cloud Agents** — https://cursor.com/docs/cloud-agent. Dashboard at cursor.com/dashboard/cloud-agents lists runs with environment/version history; supports running many agents in parallel independent of local machine state. Single-vendor UI (Cursor's own agent runtime). Requires a paid Cursor plan; billed at model API rates plus a user-set spend limit.

**Devin (Cognition)** — app.devin.ai/sessions. **Not verified** — the URL requires auth and returned only a bare page title to an unauthenticated fetch. Search results describe a per-session status/timestamp/PR-link list, but this is unconfirmed and should not be cited as fact without a logged-in check.

**Factory.ai (Droid)** — https://factory.com/product/cli (factory.ai redirects to factory.com). Sessions/computers/skills sync across TUI, desktop, web, IDE, and Slack — start a task in a terminal, finish it on your phone; sessions can be forked, favorited, and resumed. The fetched page does not confirm a single visual multi-session board and appears single-vendor (Factory's own Droid agent).

**Vibe Kanban** — https://github.com/BloopAI/vibe-kanban. **Status flag: sunsetting.** README now leads with "Vibe Kanban is sunsetting," per BloopAI's April 2026 shutdown announcement (company cited an unsustainable business model). The paid $30/user/month cloud tier is discontinued with refunds; only the free, self-hosted OSS version (Apache-2.0) has a confirmed future. When self-hosted, it remains genuinely cross-vendor: kanban board plus per-task git-worktree workspaces for Claude Code, Codex, Gemini CLI, GitHub Copilot, Amp, Cursor, OpenCode, Droid, CCR, and Qwen Code.

---

## 3. Native IDE History (baseline/contrast, single-product)

**Cursor** — https://cursor.com/docs/agent/overview. Docs describe a searchable-transcript model (Cmd/Ctrl+K searches past agent transcripts via a local index) rather than a named "history sidebar"; a third-party guide separately describes a History icon that lists/renames/deletes past Composer sessions, but that specific UI was not confirmed on cursor.com.

**JetBrains AI Assistant / Junie** — https://plugins.jetbrains.com/plugin/26104-junie-the-ai-coding-agent-by-jetbrains. 2026.1 changelog (per search; full text didn't render on direct fetch) added "Move Project History to AI Chat"/"Move Project History to CLI" migration tools and an "Import History from Previous IDE Versions" consolidator. A JetBrains YouTrack bug ([LLM-26656](https://youtrack.jetbrains.com/projects/LLM/issues/LLM-26656)) confirms 2026.1 users briefly lost AI-answer content from chat history (since fixed).

**VS Code + GitHub Copilot Chat** — https://code.visualstudio.com/docs/copilot/chat/chat-sessions (companion: /docs/agents/run/sessions/session-history). Ships a Sessions List "central hub": in the Agents window it's a cross-workspace sidebar grouped by workspace/timeframe; in Chat view it's workspace-scoped, grouped by time period. Sessions can be archived, auto-cleaned, or exported as JSON — and it can surface external sessions from Copilot CLI, the GitHub Copilot mobile app, Claude Code, and Codex, making it partially cross-agent despite being a "native" IDE feature.

**Windsurf / Codeium Cascade** — https://docs.devin.ai/desktop/cascade/cascade (this URL is a 307 redirect from the original docs.windsurf.com/windsurf/cascade/cascade). Cascade is now documented as one of two local agents inside Cognition's "Devin Desktop," not a standalone Windsurf product page — a direct artifact of the Windsurf/Cognition merger. Supports @-mentioning past conversations for summarized/checkpoint retrieval and multi-conversation switching via dropdown; a long-reported ~20-conversation storage cap (oldest evicted) isn't addressed in current docs.

**Zed Agent Panel** — https://zed.dev/docs/ai/agent-panel and https://zed.dev/docs/ai/parallel-agents. "Thread History holds all your threads across all projects, sorted chronologically," restorable any time via the Threads Sidebar (⌘⌥J) or Thread History toggle (⌘G); archiving doesn't delete, and worktree-linked threads save/restore git state on archive/restore.

---

## 4. Cross-Workspace/Session Managers (agent-agnostic hosts)

**tmux** — https://github.com/tmux/tmux. Base multiplexer; no built-in persistence across reboots (needs the plugins below). Active: 49,575 stars, pushed 2026.09.29.

**tmux-resurrect** / **tmux-continuum** — https://github.com/tmux-plugins/tmux-resurrect (13,078★) and https://github.com/tmux-plugins/tmux-continuum (4,083★). Save/restore full tmux environment (panes, windows, cwds, running programs) across restarts, with auto-save/auto-restore layered on top. **Stale**: both last pushed 2024.08 — functionally stable but over two years without a commit.

**Zellij session-manager** — https://zellij.dev/news/session-manager-protobuffs/ and https://zellij.dev/documentation/session-manager-alias.html. Built-in plugin (since Zellij 0.38.0, bound to Ctrl-o+w) that resurrects exited sessions with full layout/commands, renames, kills, shows metadata, and controls web-sharing. Very active: 35,595★, pushed 2026.09.29.

**Warp terminal** — https://docs.warp.dev/agents/using-agents and .../blocks-as-context/. Agent conversations are multi-turn and tied to terminal sessions with a dedicated history/management UI; multiple conversations can run concurrently across windows/tabs/panes. Blocks (terminal output + agent context) are shareable as structured artifacts via Warp Drive. One open bug ([#5088](https://github.com/warpdotdev/Warp/issues/5088)) confirms an agent-block-attach UI defect as of this check.

**Wave Terminal** — https://docs.waveterm.dev/releasenotes, https://github.com/wavetermdev/waveterm. Open-source AI-integrated terminal; v0.14 added "Durable Sessions" for SSH (survive disconnects/restarts). Workspaces > Tabs > Blocks model; `wsh` commands share variables/files across sessions; Wave AI is BYOK across Claude/OpenAI/Gemini plus local Ollama/LM Studio. Active: 22,390★, pushed 2026.09.29, latest tag v0.14.5 (2026.04.16).

**iTerm2 session restoration** — https://iterm2.com/documentation-restoration.html. Two mechanisms: automatic Session Restoration (long-lived pane servers reconnect after crash/upgrade) and manual Window Arrangements (save/restore layout+profile+cwd, not running state).

---

## 5. Desktop Agent Clients (parallel-session launchers)

### JetBrains Air

[Air in JetBrains IDEs](https://www.jetbrains.com/help/air-ides/air-overview.html) is an in-development agent host. The [agent-management documentation](https://www.jetbrains.com/help/air-ides/air-manage-agents.html) describes custom ACP agents, sessions, and presets; the [authorization guide](https://www.jetbrains.com/help/air-ides/air-configure-authorization.html) distinguishes agent-owned login from JetBrains AI and configured providers. Assessment date: 2026.10.14.

**Fit for Langley:** an active, cross-harness host within a JetBrains frontend. Selecting a different model inside one proprietary runtime is not the same as hosting independent agent runtimes; ACP offers the latter boundary. This makes Air relevant to the desired multi-harness, multi-repository, multi-IDE agent driver, even if it does not satisfy the entire requirement.

#### Verified capabilities

- **External runtime registration:** custom agents are configured in `~/.jetbrains/acp.json` with an absolute executable path and ACP startup arguments. Existing IDE plugins do not automatically become Air agents.
- **Separate tool integration:** configuration includes `use_idea_mcp` and `use_custom_mcp`. ACP connects the host to the agent; Model Context Protocol (MCP) connects the agent to tools. These are separate interfaces, not interchangeable compatibility claims.
- **Independent authentication:** custom ACP agents do not require JetBrains AI to be enabled. That does not imply every provider, cloud execution mode, or telemetry setting is approved by an employer.
- **Local availability:** Air plugin 262.8665.490 was installed in IntelliJ IDEA 2026.2.3 during inspection. Installation and coexistence with other agent plugins are weaker evidence than a successful agent session.

#### Boundaries and evaluation gaps

- **Multi-harness is conditional:** each runtime needs working ACP support. An installed plugin, an MCP server, or an advertised ACP flag alone does not demonstrate successful initialization, permissions, streaming, cancellation, and file operations through Air.
- **Multi-repository scope is unverified:** the inspected evidence does not establish a global queue spanning repositories, dependency-aware cross-repository tasks, or workspace/worktree isolation and recovery guarantees. Parallel sessions alone would not prove these properties.
- **Multi-IDE is not a shared control plane:** availability in JetBrains IDEs does not establish shared state with VS Code, Cursor, terminal clients, or mobile clients. Discovery and attachment to sessions started outside Air were not demonstrated.
- **Persistence and portability are unverified:** survival after closing the IDE, restart recovery, cross-device steering, transcript export, and migration between different harnesses require explicit tests. ACP support alone does not guarantee any of them.
- **End-to-end evaluation is incomplete:** the inspection did not establish a production-ready workflow with the intended enterprise agent runtimes. This public comparison deliberately excludes private enterprise compatibility records.

#### Design inspiration

These are Langley design recommendations inferred from Air's host/runtime boundary, not claims that Air implements them:

- **Keep the driver independent of the editor:** use a durable session registry and runtime adapters, with thin IDE/CLI/web frontends. Treat Air as a possible frontend or comparator rather than assuming one IDE must own all state.
- **Use ACP where it fits:** preserve structured session updates and permission requests rather than depending entirely on terminal-output parsing. Retain adapters for runtimes without ACP; do not imply a universal cross-harness transcript format.
- **Model repository and host separately:** record repository/worktree, harness, frontend, parent task, lifecycle state, and approval ownership independently. A session should remain identifiable when its editor window changes.
- **Make blocked work visible:** aggregate permission requests and errors across sessions while keeping authorization scoped to the specific runtime, repository, and action. A global dashboard must not become blanket approval.
- **Separate interoperability from governance:** agent registration, tool access, authentication, data handling, and organizational approval are distinct checks.

**Assessment:** shortlist Air as a possible JetBrains-side solution and a useful protocol-oriented UX reference. It is not established as the complete Langley replacement. A buy-versus-build comparison needs the same concrete scenarios for Air and other candidates: independent runtimes across repositories, attention/approval aggregation, collision isolation, IDE-independent persistence, and attachment from multiple frontends.

**Conductor** — https://www.conductor.build. Mac app running parallel Claude Code, Codex, and Cursor agents, each in its own isolated git-worktree workspace (auto branch/terminal/diff/PR), with a UI to monitor, review, and merge multiple agents at once. Free app (bring your own subscription); separate /pricing and /enterprise pages imply paid tiers. Active, changelog at v0.89.1.

**Crystal** — https://github.com/stravu/crystal. **Deprecated as of February 2026** — README states this plainly and redirects to its successor, Nimbalyst. Was: Electron app running multiple Claude Code/Codex sessions in parallel git worktrees with diff review and rebase/squash tooling.

**Nimbalyst** — https://nimbalyst.com/crystal/. Crystal's official successor — "a full visual workspace for building with Claude Code and Codex" — adds a session kanban board, visual editors (markdown/mockups/diagrams/data models), inline reviewable diffs, and a companion iOS app. Supports Claude Code and Codex only. Free for individuals (OSS, no feature limits); paid "Nimbalyst Teams" tier for shared workspaces.

**Happy** — https://github.com/slopus/happy (happy.engineering's own page returned only a bare title on fetch; GitHub confirmed the product). Mobile/web/desktop remote-control client for Claude Code and Codex CLI sessions running on your own machine: start, steer, approve, and hand off control between phone/desktop instantly, end-to-end encrypted, no added cloud compute cost. Free, MIT/OSS, no telemetry; last tagged release v1.4.0 (2025.09) but repo shows continued activity (1,500+ commits, 44 contributors).

**Vibe Kanban** — see § 2 above; also fits here as a desktop-adjacent client, with the same sunsetting caveat.

**Claude Squad** — see § 6 below (fits both desktop-client and terminal-multiplexer framing).

---

## 6. Terminal Multiplexers as Agent-Control Surfaces

**Tmux Orchestrator** — https://github.com/Jedward23/Tmux-Orchestrator. Three-tier Orchestrator→Project Manager→Engineer hierarchy of Claude instances across tmux windows, with self-scheduled check-ins (`schedule_with_note.sh`) and inter-agent messaging (`send-claude-message.sh`). MIT/free. **Stale**: 1,809★ but last pushed 2025.07 — over a year without a commit upstream, though active forks/derivatives exist (mdwoicke, absmartly, primeline-ai, Dicklesworthstone/claude_code_agent_farm), suggesting the pattern lives on downstream rather than in the original repo.

**Claude Squad** — https://github.com/smtg-ai/claude-squad. TUI managing Claude Code, Codex, Gemini, OpenCode, and Amp (plus Aider via `-p`) as isolated tmux-backed sessions, each in its own git worktree, with background/auto-accept execution (`-y`/`--autoyes`). AGPL-3.0/free. Actively maintained: 8,551★, last pushed 2026.08.20, latest release v1.0.20 (2026.08.20), 54 open issues.

---

## 7. Agent-Control Surfaces (observability/orchestration, not coding-specific)

**LangSmith** — https://www.langchain.com/langsmith/observability. Real-time dashboards for cost, latency (P50/P99), error rate, LLM-as-judge/code evals, tool/trajectory monitoring, plus an "Insights" auto-clustering layer over traces. Framework-agnostic (OpenAI/Anthropic/Vercel AI SDK/LlamaIndex/custom, native OpenTelemetry) despite the LangChain branding. Free dev tier; paid plans scale with trace volume; cloud, BYOC, or fully self-hosted.

**Langfuse** — https://langfuse.com/. Unified tracing, a sessions view, prompt management, evals, datasets, dashboards; OpenTelemetry-native with 100+ integrations (LangChain, CrewAI, Pydantic AI, Google ADK, various model providers). Cloud (US/EU/JP/HIPAA regions) or fully free self-hosted (MIT, Docker/K8s/Terraform, no feature gates). Cloud pricing: free Hobby tier (50k observations/month), usage-based paid tiers, enterprise self-hosted adds SLA/SSO.

**AgentOps** — https://www.agentops.ai/. Session replay ("Time Travel Debugging") for full agent runs — LLM calls, tool use, multi-agent interactions — plus cost/token tracking and audit trail. Explicitly agnostic ("Agent Agnostic SDK," 400+ LLM/framework integrations: CrewAI, Autogen, OpenAI Agents SDK, LangChain). Pricing: Basic free (5,000 events/month), Pro from $40/month (unlimited events/retention), Enterprise custom (SSO, on-prem, SOC-2/HIPAA/NIST AI RMF).

---

## Verification Gaps (do not cite these as confirmed)

- **Devin's session dashboard** (app.devin.ai/sessions) — auth-walled, unconfirmed by fetch.
- **specstory.com** and **vibekanban.com/blog/shutdown** — blocked automated fetch (403); substituted GitHub/search corroboration.
- **Cursor's "History" sidebar icon** — claimed by a third-party guide, not confirmed on official cursor.com docs.
- **chatgpt.com/codex, openai.com/codex/** — blocked automated fetch (403); substituted the OpenAI docs mirror.
- **JetBrains Junie 2026.1 changelog** — full text didn't render on direct fetch; summarized from search snippets plus a corroborating YouTrack ticket.

## Sources

- [JetBrains Air overview](https://www.jetbrains.com/help/air-ides/air-overview.html)
- [JetBrains Air agent management and custom ACP registration](https://www.jetbrains.com/help/air-ides/air-manage-agents.html)
- [JetBrains Air session management](https://www.jetbrains.com/help/air-ides/air-start-a-new-session.html)
- [JetBrains Air authorization](https://www.jetbrains.com/help/air-ides/air-configure-authorization.html)
- [SpecStory (GitHub)](https://github.com/specstoryai/getspecstory)
- [ThreadLens](https://github.com/hanityx/threadlens)
- [Happier](https://github.com/happier-dev/happier)
- [OpenAI Codex Cloud docs](https://learn.chatgpt.com/docs/cloud)
- [GitHub Copilot coding agent management](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/agent-management)
- [Google Jules](https://jules.google/)
- [Cursor Cloud Agent docs](https://cursor.com/docs/cloud-agent)
- [Factory.ai CLI](https://factory.com/product/cli)
- [Vibe Kanban](https://github.com/BloopAI/vibe-kanban)
- [Cursor Agent overview](https://cursor.com/docs/agent/overview)
- [Junie plugin page](https://plugins.jetbrains.com/plugin/26104-junie-the-ai-coding-agent-by-jetbrains)
- [JetBrains YouTrack LLM-26656](https://youtrack.jetbrains.com/projects/LLM/issues/LLM-26656)
- [VS Code Copilot Chat sessions](https://code.visualstudio.com/docs/copilot/chat/chat-sessions)
- [VS Code Agents session history](https://code.visualstudio.com/docs/agents/run/sessions/session-history)
- [VS Code Agents window](https://code.visualstudio.com/docs/agents/run/agents-window)
- [VS Code manage agent sessions](https://code.visualstudio.com/docs/agents/run/sessions/manage-sessions)
- [Cascade docs (redirected under Devin Desktop)](https://docs.devin.ai/desktop/cascade/cascade)
- [Zed Agent Panel](https://zed.dev/docs/ai/agent-panel)
- [Zed parallel agents](https://zed.dev/docs/ai/parallel-agents)
- [tmux](https://github.com/tmux/tmux)
- [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)
- [tmux-continuum](https://github.com/tmux-plugins/tmux-continuum)
- [Zellij session-manager announcement](https://zellij.dev/news/session-manager-protobuffs/)
- [Zellij session-manager docs](https://zellij.dev/documentation/session-manager-alias.html)
- [Warp using agents](https://docs.warp.dev/agents/using-agents)
- [Warp blocks-as-context](https://docs.warp.dev/agents/local-agents/agent-context/blocks-as-context/)
- [Warp issue #5088](https://github.com/warpdotdev/Warp/issues/5088)
- [Wave Terminal release notes](https://docs.waveterm.dev/releasenotes)
- [Wave Terminal (GitHub)](https://github.com/wavetermdev/waveterm)
- [iTerm2 session restoration](https://iterm2.com/documentation-restoration.html)
- [Conductor](https://www.conductor.build)
- [Crystal](https://github.com/stravu/crystal)
- [Nimbalyst](https://nimbalyst.com/crystal/)
- [Happy (GitHub)](https://github.com/slopus/happy)
- [Tmux Orchestrator](https://github.com/Jedward23/Tmux-Orchestrator)
- [Claude Squad](https://github.com/smtg-ai/claude-squad/blob/main/README.md)
- [LangSmith observability](https://www.langchain.com/langsmith/observability)
- [Langfuse](https://langfuse.com/)
- [AgentOps](https://www.agentops.ai/)

*[doc-audit](https://github.com/BrianHoltz/tools/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.10.14.Wed*
