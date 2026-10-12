---
name: convo
description: Render the standard timestamped conversation banner with a concise conversation title, repository context, summary, recent-turn description, and optional central-document metadata.
user-invocable: true
disable-model-invocation: true
---

# Convo

When the user invokes `/convo`, render only the completed Markdown template
below. Do not add commentary, bullets, code fences, or extra whitespace.

## Gather values

- Use the official conversation title from the IDE/history when it is
  substantive. Otherwise synthesize a terse 2–6 word title for the whole
  conversation. If the current harness has a title-setting tool, set the
  synthesized title; otherwise do not claim to have changed the official title.
- Use the local date/time in `yyyy.mm.dd.Dow.hhmm` format.
- Use the current repository name and branch when available. Do not guess when
  the workspace is not a Git repository; use `no-repo` and `no-branch`.
- Summarize the whole conversation in one line.
- Describe the last three conversational turns in one line. Never mention
  invoking, running, rendering, or displaying `/convo` or the banner.
- Identify one central document only if it was substantively read, edited, or
  discussed. A passing mention does not qualify. If the document is available,
  include its parent/filename and creation/modification timestamps when
  obtainable. If the harness offers an editor-opening tool, open that document.
  Omit the document line when there is no clear central document.
- Use available shell and IDE tools to obtain these values. Use an available
  title-setting or editor-opening tool only when it exists; do not probe for
  unavailable tools or fabricate successful actions.

## Output

```text
---
# terse conversation title
### yyyy.mm.dd.Dow.hhmm repo:branchname
### All: one-line summary of entire conversation
### Latest: one-line description of last 3 turns, excluding any mention of /convo or banner rendering
### Doc: <parent/filename.md>  created:<yyyy.mm.dd.hhmm>  modified:<yyyy.mm.dd.hhmm>
---
```

The `### Doc:` line is conditional. Omit `created:` if unavailable or identical
to `modified:`. Replace all placeholders; never print the angle-bracketed
placeholders literally.
