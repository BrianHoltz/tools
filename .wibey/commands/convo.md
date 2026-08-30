---
description: Display a conversation banner
allowed-tools: Bash, mcp__jetbrains-mcp__open_file_in_editor, mcp__wibey_bridge__wibey_set_conversation_title
code-puppy-tools: agent_run_shell_command
---

**Agent detection (run first):** If you are Code Puppy (no `mcp__jetbrains-mcp__*` or `mcp__wibey_bridge__*` tools in your toolset), you are in **Code Puppy mode**: use `agent_run_shell_command` everywhere this doc says `Bash`, and skip both MCP-only steps entirely (IDE title lookup, `wibey_set_conversation_title`, `open_file_in_editor`) rather than attempting and catching a failure — those tools simply do not exist in this environment. Everything else in this command works identically.

Interpolate values into the template block below and render it as Markdown exactly as shown.

**Rules:**

- Output exactly the interpolated template block. Ordering is fixed; the `### Doc:` line is conditional — include it only when a doc is identified (see below), omit it entirely otherwise.
- Do not add commentary, bullets, code fences, or extra whitespace.
- For the `### Latest:` line: never mention invoking, running, rendering, or displaying `/convo` or the conversation banner itself.

**Conversation title (`#` line):**

**Code Puppy mode:** there is no IDE/agent-history sidebar and no title-setting tool — always synthesize the title directly from conversation content (2–6 words, terse one-line summary of the whole conversation) and render it. Do not attempt to look up or set an official title.

**IDE mode (Wibey/JetBrains):** Check whether the current conversation has an official title visible in the IDE or agent history sidebar. Use it verbatim if it is substantive — not a single-prompt echo, not a default like "New Conversation", and not merely the most recent message rephrased. If the official title is good, use it. If you must synthesize a title: generate a terse one-line summary of the whole conversation, then call `mcp__wibey_bridge__wibey_set_conversation_title` with a concise title (2–6 words, ≤60 chars) to set the official IDE conversation title — skip silently if the tool is unavailable.

**Doc detection (run before rendering):**

Identify the single doc that is the **central focus** of this conversation — the one most substantively read, edited, or discussed. Mere appearance in `git status` output or as a passing mention does not qualify. Pick only one; omit `### Doc:` if no doc is clearly central.

Candidates in priority order:
1. `incidents/**/*.md` or `projects/**/*.md` — incident/project work
2. `.wibey/skills/<name>/SKILL.md` — if the work is improving a skill
3. `.wibey/commands/<name>.md` or `shared/.wibey/commands/<name>.md` — if the work is improving a command
4. `docs/**/*.md`, `shared/docs/**/*.md`, or any other reference doc that was the primary subject

If a doc is identified, run this Bash block (substituting the absolute path):

```bash
DOC_PATH="<absolute path>"
DOC_PARENT=$(basename "$(dirname "$DOC_PATH")")
DOC_FILE=$(basename "$DOC_PATH")
DOC_DISPLAY="${DOC_PARENT}/${DOC_FILE}"
DOC_CTIME=$(stat -f "%SB" -t "%Y.%m.%d.%H%M" "$DOC_PATH" 2>/dev/null)
# Fall back to mtime if birth time unavailable (non-APFS or pre-2000 result)
[[ "${DOC_CTIME%%.*}" -lt 2000 ]] 2>/dev/null && \
  DOC_CTIME=$(stat -f "%Sm" -t "%Y.%m.%d.%H%M" "$DOC_PATH" 2>/dev/null)
DOC_MTIME=$(stat -f "%Sm" -t "%Y.%m.%d.%H%M" "$DOC_PATH" 2>/dev/null)
echo "display=$DOC_DISPLAY ctime=$DOC_CTIME mtime=$DOC_MTIME"
```

**Code Puppy mode:** skip this call entirely — there is no JetBrains MCP connection in this environment. The `### Doc:` line in the template is still rendered from the Bash block's output above; only the editor-opening side effect is skipped.

**IDE mode:** call `mcp__jetbrains-mcp__open_file_in_editor` with `DOC_PATH` as the `filePath` — skip silently if the tool is unavailable (personal laptop / no IDE connection).

**Template:**

```
---
# terse conversation title (prefer official IDE/agent history title if substantive; synthesize and attempt to set it otherwise)
### yyyy.mm.dd.Dow.hhmm repo:branchname
### All: one-line summary of entire conversation
### Latest: one-line description of last 3 turns, excluding any mention of /convo or banner rendering
### Doc: <parent/filename.md>  created:<yyyy.mm.dd.hhmm>  modified:<yyyy.mm.dd.hhmm>
---
```

Omit `### Doc:` entirely if no central doc was identified.
Omit `created:` if unavailable or identical to `modified:`.
