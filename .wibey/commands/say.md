---
description: Set terminal + conversation title and display a banner
allowed-tools: Bash
---

Do all three steps in order, then render the template.

**Step 1 — Set terminal title.**
Run exactly this shell command (substitute `message` with the verbatim argument text):
```bash
printf '\033]0;message\007'
```

**Step 2 — Set conversation title (silent if tool unavailable).**
Call `mcp__wibey_bridge__wibey_set_conversation_title` with `message` as the title (2-6 words, max 60 chars — truncate if needed). Skip silently if the tool is not available.

**Step 3 — Render banner.**
Interpolate values into the template block below and render it as Markdown exactly as shown.

**Rules:**

- Output exactly the interpolated template block, same number of lines, same ordering.
- Do not add commentary, bullets, code fences, or extra whitespace.
- `yyyy.mm.dd.Dow.hhmm` — run `date "+%Y.%m.%d.%a.%H%M"` and substitute the output.
- `repo` — basename of the current git repo (`git rev-parse --show-toplevel | xargs basename`); use workspace folder name if not in a git repo.
- `branchname` — current git branch (`git rev-parse --abbrev-ref HEAD`); omit if not in a git repo.
- `message` — verbatim argument text from the user.

**Template:**

```
---
# message
### yyyy.mm.dd.Dow.hhmm repo:branchname
---
```
