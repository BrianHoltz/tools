# AI/IDE Toolchain

## Local Modifications in Use

- [Shuzijun Markdown Editor — IDEA](ToolMods.md#shuzijun-source-build)
  - Type in search without editing the document.
  - Save immediately from the toolbar.
  - Confirm before reloading unsaved work.
  - Follow IDEA's light/dark theme changes.
  - Match preview fonts and IDEA zoom.
  - Wrap tables within the pane.
  - Keep list spacing intact when deleting empty bullets.
  - Jump to linked files and headings.
  - See the number of search matches as you type.
  - Reach hidden toolbar buttons through an overflow menu.
  - Read tooltips even in narrow panes.
  - Remember whether the toolbar is hidden.
  - Hide raw HTML without changing the file.
- [Zaaack Markdown Editor — VS Code](ToolMods.md#zaaack-source-build)
  - Search text in each editing mode.
  - Jump to headings from the Explorer outline.
  - Follow links to files and headings.
  - Keep each file in its own editor tab.
  - Read text and code comfortably in dark themes.
  - Keep list spacing intact (fix not yet installed).
  - Reach hidden toolbar buttons through an overflow menu.
  - Read tooltips even in narrow panes.
  - Remember whether the toolbar is hidden.
  - Hide raw HTML without changing the file.
  - Attach visual-editor files to Copilot.
  - Show readable, translated toolbar labels.
- [Code Puppy — IDEA / VS Code](ToolMods.md#code-puppy-maintained-source-builds)
  - Paste images and files into IDEA chat.
  - Offer the current file as a chat attachment.
  - Offer each selected passage as a chat attachment.
  - Open VS Code chat file links in the editor.
  - Keep VS Code chat links readable in dark themes.
  - Keep terminal links readable in dark themes.
- [TypeDown Markdown Editor — VS Code / Cursor](ToolMods.md#typedown-patches)
  - Keep the cursor in place when saving.
  - Tighten prose line spacing.
  - Make table rows more compact.
  - Compact list spacing.
- [Codex File Context — VS Code, personal Macs](ToolMods.md#codex-file-context)
  - Attach the current file from visual-editor tabs.
- [Wibey — VS Code](ToolMods.md#wibey-vs-code-new-conversation-patch)
  - Start new chats without showing the old conversation.

## Contents

- [Choosing an IDE](#choosing-an-ide)
- [Agent harnesses](#agent-harnesses)
- [Markdown editors](#markdown-editors)
- [Everyday shortcuts](#everyday-shortcuts)
- [IDEA](#idea)
- [VS Code and Cursor](#vs-code-and-cursor)
- [Troubleshooting](#troubleshooting)

Builds, patches, configuration internals and verification belong in [ToolMods](ToolMods.md).

## Choosing an IDE

- **IntelliJ IDEA:** Brian's primary IDE; strongest fit for integrated database, HTTP, debugging and refactoring work.
- **VS Code:** strongest confirmed Markdown workflow with the local Zaaack editor and independent previews.
- **Cursor:** an alternative with parallel agents; its installed Markdown and harness builds differ from VS Code.

### Installed work-laptop versions

Disk metadata checked 2026.10.25.Sun; IDEA Markdown Editor rechecked 2026.10.31.Sat. Installed files do not prove which build an already-running editor has loaded.

| Component | IDEA | VS Code | Cursor |
| --- | --- | --- | --- |
| IDE | 2026.2.3 | 1.143.1 | 3.21.13 |
| Code Puppy | 0.31.2, native local build | 0.28.2, local build | 0.27.0 |
| Wibey | 1.0.32_20261023.Fri.1532 | 1.0.31 | 1.0.18 |
| Markdown Editor | Shuzijun 2.0.7-local.22 | Zaaack 0.1.22-local.6 | Zaaack 0.1.20 |
| TypeDown | — | 1.1.7 | 1.1.7 |

Code Puppy and Wibey are Walmart-internal and maintained only on the work laptop. Their absence from the personal laptop is expected. Zaaack source is newer than the installed VS Code extension; see [build state](ToolMods.md#zaaack-source-build).

### Reported IDE behavior

These are Brian's workflow observations, not a fresh benchmark of the installed builds. ✅✅ denotes a strong preference, ✅ available, 🟡 partial, ❌ unavailable, and ? unestablished.

| Feature | IDEA | VS Code | Cursor |
| --- | --- | --- | --- |
| AI diff review                 | ✅ per delta  | 🟡 per file  | 🟡 per file             |
| AI diff in linked repo         | ✅            | ❌            | ❌                       |
| git ops in linked repo         | ✅            | ✅            | ✅                       |
| approval UX                    | ✅            | ✅            | ✅                       |
| md preview                     | ✅            | ✅✅ independent | ✅✅ wysiwyg              |
| md preview search              | ✅            | ✅            | ❌❌ neither              |
| md table format                | ✅✅ auto      | 🟡 manual    | 🟡 manual               |
| md pastes details block        | ❌            | ✔️           | ✔️                      |
| md headers paste bold to Slack | ✅            | ❌            | ❌                       |
| search/find                    | ✅            | ✅            | ✅                       |
| git                            | 🟡           | ✅✅           | ✅✅                      |
| debug                          | ✅            | ?            | ?                       |
| database                       | ✅            | ❌            | ❌                       |
| http                           | ✅            | ❌            | ❌                       |
| editor history UI              | ✅            | 🟡           | 🟡                      |

The observations are not combined into a score: they cover different builds and verification scopes.

## Agent Harnesses

- **Voice input:** Brian preferred Claude Code's live, word-by-word text in VS Code over Copilot and Codex's record-then-transcribe experience, with a reported 2–3s delay (2026.10.12). This is a host-specific observation, not an accuracy benchmark.
- **Code Puppy rule loading:** Brian set `/set agents_md_max_chars=65536`, up from the 10,000-character default, during the 2026.10.30.Fri session to prevent long `AGENTS.md` files from being truncated. This records the session setting; persistence across new sessions remains to be verified.
- **Current context:** the local Code Puppy builds suggest the active file or selection for explicit attachment. Suggestions are not automatic submission. The maintained JetBrains 0.32.1 source build adds an × dismissal control; repeated editor refreshes do not restore a dismissed suggestion. The installed IDEA build remains 0.31.2 until installation/restart.
- **Parallel work:** Wibey and Code Puppy support parallel conversations across the observed IDEs; exact behavior depends on the host/build.
- **Follow-up prompts:** queuing waits until the current task ends; steering changes the running task. Do not treat them as interchangeable. Current native implementations include queue UI; installed-host interaction still needs confirmation.
- **Permissions:** IDEA's JetBrains AI chat offers **Allow All**. Copilot's terminal confirmations depend on its host; no persistent IDEA bypass is established. [Configuration details](ToolMods.md#agent-permissions) are for maintenance, not a promise that OS or authentication prompts disappear.

TODO: recheck queue/steer behavior and active-context shortcuts in the installed native Code Puppy and Compose Wibey builds.

## Markdown Editors

### Shuzijun in IDEA

- **Agent edits on disk:** local.22 polls visible local Markdown tabs every two seconds, including split panes and IDEA's built-in preview. Hidden tabs are skipped; no project scan runs. Unsaved-edit protections remain. Install local builds through **Settings → Plugins → ⚙ → Install Plugin from Disk**, then restart IDEA. See [build and validation](ToolMods.md#build-and-validation); live refresh latency is not yet measured.
- **Search safely:** ⌘F focuses and selects the query; the count tracks visible literal matches. Brian confirmed the search-input fix in local.14 (2026.10.18); local.16 includes later list-editing and theme-refresh fixes.
- **Save and reload:** the floppy disk force-saves; dim means saved, red means failure. Reload is immediately beside it. If the buffer is dirty, click reload again within three seconds to discard it.
- **Read comfortably:** the upper-right toggle hides the toolbar, annotations and raw HTML. The toolbar also has an independent raw-HTML toggle, sometimes under `»`.
- **Navigate:** plain-click links; Option-click to edit. The toolbar's `»` tray keeps controls reachable in narrow panes.
- **Match IDEA:** rendered typography follows the shared Markdown Preview font size and IDE appearance; source stays monospace.

### Zaaack in VS Code

- **Find and navigate:** ⌘F and the toolbar share search; Markdown Outline appears in Explorer. Plain-click links and headings; Option-click edits links.
- **Keep panes usable:** files retain independent editors; the toolbar collapses into `»` in narrow panes. The upper-right toggle reclaims toolbar and annotation space.
- **Read dark code:** the local build supplies dark fenced-code styling and theme-aware content. The installed local.6 lacks local.7's nested-list Backspace fix.
- **Keep the local build:** disable extension auto-update if retaining local behavior. A Marketplace replacement can lose modifications even when its version appears similar.

Brian confirmed VS Code find, anchor links, adaptive toolbar and independent previews (2026.10.12). External-file reread, image rendering and Cursor parity remain unverified.

### Other editors

TypeDown provides a compact alternative, with locally patched spacing and focus handling. IDEA's built-in Markdown preview/editor remain separate choices; the Compose editor ignores custom preview CSS. Cursor's registered Zaaack 0.1.20 is not the VS Code source build.

| Behavior                 | IDEA viewer | IDEA editor | typedown     | zaaack                            | Cursor native |
| ------------------------ | ----------- | ----------- | ------------ | --------------------------------- | ------------- |
| >1 tab at a time         | ✅          | ✅✅        | ✅✅         | ✅✅                              | ✅✅          |
| re-read changed file     | ?           | ?           | ✅           | ?                                 | ?             |
| wide tables              | ✅          | ✅          | ❌ truncates | ✅✅                              | ❌ truncates  |
| non-bloated side padding | ✅          | ✅          | ❌           | ✅                                | ❌            |
| shows images             | ✅          | ✅          | ?            | ?                                 | ?             |
| find in file             | ✅          | ✅          | ❌           | ✅ unified Cmd+F | ❌            |
| structure                | ✅          | ✅          | ❌           | ✅                           | ❌            |
| internal links           | ✅          | ❌          | ?            | ✅ plain-click anchors | ?             |
| link editing             | ?           | ✔️        | ❌           | ✔️                              | ❌            |
| toolbar                  | -           | ✔️        | ✔️         | ✅ single row + overflow | ❌            |

The comparison records earlier observations. In particular, it does not establish current Cursor behavior or parity between IDEA's built-in editor and Shuzijun.

## Everyday Shortcuts

### Navigation

| Action | IDEA | VS Code / Cursor |
| --- | --- | --- |
| Zoom | ⌘= / ⌘- | ⌘= / ⌘- |
| Open file | ⌘P | ⌘P |
| Search project | ⇧⌘F | ⇧⌘F |
| Toggle line numbers | ⌥L | Command Palette |
| Find in rich Markdown | ⌘F | ⌘F in local Zaaack |

IDEA's zoom and open-file shortcuts are local overrides; [keymap maintenance](ToolMods.md#idea-keybindings) covers their action IDs.

### VS Code and Cursor editors

- **Zaaack:** ⌃⌥⌘M opens Markdown Editor.
- **TypeDown:** ⌥⇧⌘M toggles its WYSIWYG editor.
- **Markdown preview:** ⇧⌘V opens Markdown Preview Enhanced in VS Code and the built-in preview in Cursor, in the current editor column.
- **Split editor:** ⌘\ creates another editor group.

### Attach the active file

- **Copilot in VS Code:** ⌃⌥⌘⇧C attaches the active file through the local Zaaack command, including visual-editor tabs. It targets the active/last-focused chat without sending a prompt.
- **Codex helper:** ⌃⌥⌘C attaches the focused local file, including TypeDown and Zaaack tabs, when the helper and Codex extension are installed. The helper is not registered on this work laptop and Codex is absent, so this shortcut is unavailable here.

The Codex helper attaches a path, not unsaved buffer contents; it rejects untitled and non-file tabs. Neither shortcut implies selection attachment or support in other harnesses.

## IDEA

### Typography and theme

Use **Settings → Languages & Frameworks → Markdown → Preview font size**. The work-laptop setting is 14px. Shuzijun follows this preference and IDE scaling; raw source retains the editor font.

Built-in preview CSS and Shuzijun styling are independent. The Compose Markdown editor ignores preview CSS and hardcodes some table behavior. Close and reopen a built-in preview after changing its font size if needed.

### Install local plugins

Use **Settings → Plugins → ⚙ → Install Plugin from Disk…**, select the timestamped Downloads ZIP, then restart IDEA. Marketplace updates can replace local builds; ask for a rebuild rather than assuming modifications survived.

Leave JCEF at its default mode. Code Puppy is native and no longer needs a browser workaround. Shuzijun and the built-in preview still use their own rendering paths.

### Workspace safety

Project roots affect more than indexing: changing them can disrupt layout and Copilot session identity. Use the [work-project allowlist](GitScheme.md#work-project-roots), not a bulk “add every repository” action. Project tint is a separate setting.

## VS Code and Cursor

### Independent previews

Preview reuse is disabled on this work laptop. Markdown Preview Enhanced uses **Multiple Previews**; reload after changing that preference. Open each file and split editor groups as needed.

### Typography and theme

The built-in preview and TypeDown are configured at 13px. TypeDown and Zaaack have separate typography controls; changing the raw Markdown editor font does not change either rich editor. Keep source monospace for pipe tables.

Markdown Preview Enhanced uses `systemColorScheme`, which follows the OS color scheme; do not confuse it with editor-theme synchronization. Zaaack's local build handles editor-theme changes separately.

### Human-versus-agent conflict diffs

When VS Code shows **(in file) ↔ (in Visual Studio Code)**, green lines represent your buffer and red lines represent disk. Save or accept writes the entire buffer; revert discards the buffer. This view has no per-hunk accept buttons.

In IDEA agent reviews, avoid **Accept All** after making your own edits: it can collapse or overwrite them. Prefer per-chunk review and inspect the resulting file.

### Move a panel

Open the Command Palette, run **Move View**, select the panel and choose **Move to Opposite Sidebar**.

## Troubleshooting

- **Lost plugin behavior:** check the loaded build after restart; an automatic update may have replaced a local package.
- **Unreadable terminal links:** Code Puppy's terminal color remap is separate from native Markdown colors; [maintenance details](ToolMods.md#terminal-link-color-configuration).
- **Network trouble off VPN:** work-laptop VS Code/Cursor use a corporate proxy; GitHub bypass entries and machine-specific differences are in [proxy configuration](ToolMods.md#proxy-configuration).
- **Empty Copilot history:** project identity, profile and cloud-session settings need diagnosis before any workspace cleanup; [session-state precautions](ToolMods.md#copilot-session-state).
- **Stale usage dashboard:** regenerate with `~/.wibey/usage/wibey-usage dash`; do not assume SessionEnd refreshes the HTML. [Usage maintenance](ToolMods.md#wibey-skills-usage-dashboard) records the actual hook behavior.
- **Services panel interrupts:** the old MCP suppression is not present in the installed descriptor; it is not an active modification. [Patch details](ToolMods.md#suppress-services-panel-auto-pop).

*[doc-audit](https://github.com/BrianHoltz/tools/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.10.25.Sun*
