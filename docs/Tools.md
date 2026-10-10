# AI/IDE Toolchain

## Local Modifications in Use

- **Code Puppy JetBrains + VS Code + Cursor 0.27.0** — same `feature/active-context-pill` branch of `~/src/code-puppy-ide` builds all three; the active-editor-context suggestion is implemented in the shared webview/protocol packages so it applies everywhere. JetBrains additionally carries local JDK 21 build detection and the JCEF-proxy-warm startup workaround (no JCEF in VS Code/Cursor, so those don't need it). The VS Code/Cursor extension was built and installed for the first time 2026.10.02 — previously source-only, never packaged. (Editable conversation titles and universal-constructor visibility shipped upstream and no longer need a local patch.)
- **Wibey JetBrains 1.0.28** — upstream GPT model support and context-window work, combined locally with persistent editable conversation titles, editable queued follow-up prompts, image paste, focused-editor file/selection context, prompt queuing, and quota snapshots.
- **Zaaack Markdown Editor for VS Code and Cursor** — adds multipanel editing, outline navigation, find, anchor links, and dark-theme/readability improvements.
- **TypeDown for VS Code and Cursor** — compacts prose, table, and list spacing; preserves editor focus and cursor position through paste.
- **Shuzijun Markdown Editor for IntelliJ IDEA** — improves body-text readability and supplies the JCEF dependency required by IDEA 2026.2.
- **IntelliJ IDEA MCP Server plugin** — prevents MCP connections from stealing focus to the Services tool window.



### Local Build Artifact Rule

This is the canonical personal policy for local IDE/plugin artifacts.

Every locally built IDE/plugin artifact must be copied to `~/Downloads/` for installation and review. Keep the canonical build output in its repository's normal release folder, but treat the Downloads copy as the human-facing local build.

Name each Downloads artifact `<product>-<version>-yyyymmdd.Dow.hhmm-<blah>.<ext>`. The timestamp is the actual build-completion time; capture it with `date "+%Y%m%d.%a.%H%M"` immediately after the build succeeds, not when copying or renaming the artifact. `<blah>` is a lowercase, hyphen-free description of the newest included fix, shorter than 10 characters. Example: `code-puppy-jetbrains-0.23.0-20260918.Fri.1146-imgpaste.zip`.

### Rebuilding the Local Wibey JetBrains Plugin

Build from `~/src/wibey-jetbrains-plugin` on `brian/local-combined`; this branch combines local modifications with upstream updates. Fetch and merge `origin/main` (never rebase), resolve overlapping edits by preserving both upstream behavior and local features, then confirm no unmerged paths or conflict markers remain. Keep the timestamped build version and update its base version to the release version from upstream. Preserve local PR changes, inspect new upstream `@Service` classes against `plugin.xml`, and let the Gradle service-registration validation run as part of `buildPlugin`.

Run the bridge checks and build the installable distribution ZIP from Terminal.app. `set -e` ensures the Gradle build cannot run after a failed bridge check:

```bash
set -e
cd ~/src/wibey-jetbrains-plugin
git fetch origin main
git merge --no-edit origin/main
# Resolve all conflicts before continuing; retain local mods and upstream behavior.
(cd bridge && bun install --frozen-lockfile && bun run build && bun run test -- --reporter=dot)
./gradlew buildPlugin
```

After `buildPlugin` succeeds, capture the actual completion time and stage the newest built distribution. The Downloads version is the release version (before `_` in Gradle's timestamped filename); the separate timestamp is when the build completed. `gpt` is the short included-change label for this upstream GPT model-support release; change it when a different update is newest:

```bash
STAMP=$(date "+%Y%m%d.%a.%H%M")
ZIP=$(ls -t build/distributions/wibey-jetbrains-plugin-*.zip | head -n 1)
VERSION=${ZIP##*/wibey-jetbrains-plugin-}
VERSION=${VERSION%%_*}
OUT="$HOME/Downloads/wibey-jetbrains-plugin-$VERSION-$STAMP-gpt.zip"
unzip -t "$ZIP"
cp -p "$ZIP" "$OUT"
cmp "$ZIP" "$OUT"
shasum -a 256 "$ZIP" "$OUT"
```

The ZIP must be the dependency-complete installable artifact, not a JAR from `build/libs/`. Confirm the archive test succeeds and both hashes match. Keep the canonical ZIP in `build/distributions/`; install from the timestamped copy in `~/Downloads/`.

### Rebuilding the Local Code Puppy JetBrains Plugin

Repo: `~/src/code-puppy-ide` (fork `r0b0m29/code-puppy-ide`, monorepo for both the VS Code extension and the JetBrains plugin), branch `feature/active-context-pill`. That branch merges local-only commits (active-editor-context suggestion, JDK 21 build detection, JCEF-proxy-warm startup fix) onto upstream `main`. Full release flow lives in `docs/ai/RELEASING.md` in that repo — this is the shortcut for a local-only install build, no release/tag/publish:

```bash
cd ~/src/code-puppy-ide
git fetch origin main
git merge --no-edit origin/main
# Resolve conflicts: diff each hunk, prefer upstream when it has absorbed a
# local fix (check for a same-purpose class/import on the other side before
# keeping both — duplicated fixes are a DRY violation, not a safe default).
bash scripts/build-jetbrains-variants.sh
```

The script builds the webview once, then both JetBrains variants (`legacy` for IDE builds 243–261, unsuffixed `main` for 262+) into `releases/`. IDEA 2026.2.x needs the unsuffixed `code-puppy-jetbrains-<version>.zip`. JDK 21 is auto-detected (`scripts/gradle-jetbrains.sh`) — no `PATH` changes needed, see that repo's RELEASING.md if it can't find one. First build is slow (Gradle daemon + IntelliJ SDK warm-up, ~2 min); reruns are fast.

After `buildPlugin` succeeds, stage the timestamped Downloads copy per the [Local Build Artifact Rule](#local-build-artifact-rule):

```bash
STAMP=$(date "+%Y%m%d.%a.%H%M")
ZIP="releases/code-puppy-jetbrains-<version>.zip"
OUT="$HOME/Downloads/code-puppy-jetbrains-<version>-$STAMP-<blah>.zip"
unzip -t "$ZIP"
cp -p "$ZIP" "$OUT"
cmp "$ZIP" "$OUT"
shasum -a 256 "$ZIP" "$OUT"
```

Install from Downloads: Settings → Plugins → ⚙ → Install Plugin from Disk…, then restart IDEA. **Marketplace auto-update will silently overwrite this with a stock build** — after any Code Puppy update notification, verify the installed jar's version against this branch before trusting that local mods survived (see the 2026.10.02 lesson above). Commit and push the merge to `origin/feature/active-context-pill` so the combined branch stays ahead of upstream and the mods aren't local-only residue.

The same repo's `apps/vscode` builds the VS Code/Cursor side of the identical feature (`pnpm --filter code-puppy-vscode run package` instead of the Gradle step — produces `releases/code-puppy-vscode-<version>.vsix`). Install/update either editor via CLI, no marketplace involved since this extension isn't published there:

```bash
code --install-extension ~/Downloads/code-puppy-vscode-<version>-<stamp>-<blah>.vsix
cursor --install-extension ~/Downloads/code-puppy-vscode-<version>-<stamp>-<blah>.vsix
```

Verify with `code --list-extensions --show-versions | grep puppy` (same flag works for `cursor`). Unlike the JetBrains side, there's no marketplace auto-update to silently clobber this — it only changes when you rebuild and reinstall it yourself.

## IDEs


| Feature                        | IDEA         | VS Code      | Cursor                  |
| ------------------------------ | ------------ | ------------ | ----------------------- |
| Score                          | 33.5         | 20.5         | 19.5                    |
| IDE                            | 2026.2.3     | 1.135.0      | 3.21.13                 |
| VSCode engine                  | —            | —            | 1.105.1                 |
| Wibey                          | 1.0.28       | 1.0.20       | 1.0.18                  |
| Code Puppy                    | 0.27.0       | 0.27.0       | 0.27.0                  |
| └ parallel agents              | ✅            | ✅            | ✅                       |
| └ enqueue next prompt          | ❌            | ✅            | ✅                       |
| └ context += @ file            | ✅            | 🟡<100KB     | 🟡<100KB                |
| └ context += selection         | ✅ cmd-' pill | ✅ cmd-L pill | 🟡 cmd-L pill via Agent |
| └ image paste                  | ✅            | ✅            | ✅                       |
| └ convo title edit             | ✅✅           | ✅            | ✅                       |
| └ convo title auto             | ✅            | ✅            | ✅                       |
| └ convo search                 | ✅            | ✅            | ✅                       |
| └ convo timestamps             | ✅            | ✅            | ✅                       |
| └ convo bookmark               | ✅            | ✅            | ✅                       |
| └ rich/linked paste            | ❌            | ❌            | ❌                       |
| Github Copilot                 | 1.11.2-251   | 0.39.0       | 1.388.0 ????            |
| └ parallel agents              | ✅            | ✅            | ✅                       |
| └ context += selection         | ✅ auto       | ❌            | ❌                       |
| └ convo title                  | 🟡 manual    | ✅ auto       | ✅ auto                  |
| AI diff review                 | ✅ per delta  | 🟡 per file  | 🟡 per file             |
| AI diff in linked repo         | ✅            | ❌            | ❌                       |
| git ops in linked repo         | ✅            | ✅            | ✅                       |
| approval UX                    | ✅            | ✅            | ✅                       |
| md preview                     | ✅            | 🟡 only 1    | ✅✅ wysiwyg              |
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


Score rubric

- Glyph values: ✅✅ = 2 pts, ✅ = 1 pt, 🟡 / ✔️ = 0.5 pts, ❌ / ? = 0 pts, ❌❌ = −1 pt
- Version/text-only cells (version numbers, descriptive text) = excluded
- Copilot rows excluded from IDE score
- **IDEA patches (baked-in as of 2026.09.29):** image-paste-fix + conversation-title-features are merged into local `brian/local-combined` build (Wibey 1.0.28), alongside upstream 1.0.28 updates. Scores reflect working features; ⚙️ notation removed. Recount after IDE/extension updates.
- Editor score: each IDE gets the maximum score achievable by any editor available to it
  - IDEA: native WYSIWYG editor (8.0 pts); beats viewer (7.0) and shuzijun (3.5)
  - VS Code: typedown (3.5 pts); zaaack broken ~2026.06.01 (was 7 pts w/ patch)
  - Cursor: typedown (3.5 pts); zaaack broken ~2026.06.01 (was 7 pts w/ patch)
- Final score = IDE row subtotal + best editor subtotal



## Markdown Viewers/ Editors

- VSCode md preview hangs for big files, but zaaack handles them
  - zaaack lacks: string search; intra-doc link nav; outline view. Wibey fixed them all!
- typedown and zaaack work in both VS Code and Cursor


| Behavior                 | IDEA viewer | IDEA editor | typedown    | zaaack                            | Cursor native |
| ------------------------ | ----------- | ----------- | ----------- | --------------------------------- | ------------- |
| version                  | 2026.2      | 2026.2      | 1.1.7       | 0.1.17 (VSCode) / 0.1.13 (Cursor) | 2.6.19        |
| >1 tab at a time         | ✅           | ✅✅          | ✅✅          | ✅✅                                | ✅✅            |
| re-read changed file     | ?           | ?           | ✅           | ?                                 | ?             |
| wide tables              | ✅           | ✅           | ❌ truncates | ✅✅                                | ❌ truncates   |
| non-bloated side padding | ✅           | ✅           | ❌           | ✅                                 | ❌             |
| shows images             | ✅           | ✅           | ?           | ?                                 | ?             |
| find in file             | ✅           | ✅           | ❌           | ✅ ⚙️                              | ❌             |
| structure                | ✅           | ✅           | ❌           | ✅ ⚙️                              | ❌             |
| internal links           | ✅           | ❌           | ?           | ✅ ⚙️                              | ?             |
| link editing             | ?           | ✔️          | ❌           | ✔️                                | ❌             |
| toolbar                  | -           | ✔️          | ✔️          | ✔️                                | ❌             |




### IDE Keybindings


| Action         | IDEA             | VS Code     | Cursor      |
| -------------- | ---------------- | ----------- | ----------- |
| zoom in / out  | `^⌥=` / `^⌥-` ⚠️ | `⌘=` / `⌘-` | `⌘=` / `⌘-` |
| open file      | `⇧⌘O` ⚠️         | `⌘P`        | `⌘P`        |
| search project | `⇧⌘F`            | `⇧⌘F`       | `⇧⌘F`       |
| Wibey history  | ?                | ?           | ?           |
| Wibey new chat | ?                | ?           | ?           |


IDEA keybinding overrides (defaults shown in table, actual bindings below):

- ⚠️ **zoom** `^⌥=` / `^⌥-` (`ZoomInIdeAction` / `ZoomOutIdeAction`) → remapped to `⌘=` / `⌘-`. Displaced `CollapseRegion` / `ExpandRegion` (fold/unfold) — unbound and unneeded.
- **open file** `⇧⌘O` (`GotoFile`) → remapped to `⌘P`. Displaced `FileChooser.TogglePathBar` from `⌘P` — unneeded.



### IDEA — Code Puppy tool window font size

Code Puppy (JetBrains plugin) scales its webview text from **IDEA's UI font size**. It reads
`UIUtil.getLabelFont().getSize()` and sets JCEF `CefBrowser.setZoomLevel()` so the app's base
13px styling ends up matching the UI label font.

What this means in practice:

- If you want the Code Puppy window **one point bigger**, bump the UI font size by 1:
Preferences → Appearance & Behavior → Appearance → enable **Use custom font** (if needed) →
increase **Size**.
- If you want Code Puppy to **match Markdown preview / Wibey tool windows**, make the UI font
size match your editor font size (Preferences → Editor → Font).
- There is no per-tool-window font setting; this is global UI font. (If you don’t want the whole
IDE bigger, you’re into "open DevTools and inject CSS" territory.)



### Keybindings (swapped from defaults in VS Code and Cursor)

The default keybindings collided with preference — typedown's simpler shortcut was wasted on the less-preferred editor. Swapped via `keybindings.json` in both VS Code and Cursor:

- **typedown** "Open in WYSIWYG mode": default `^ ⌥ ⌘ M` → swapped to `⌥ ⇧ ⌘ M`
- **zaaack** "Open with markdown editor": default `⌥ ⇧ ⌘ M` → swapped to `^ ⌥ ⌘ M`
- **Markdown Preview Enhanced** (`shd101wyy.markdown-preview-enhanced`): bound `⇧ ⌘ V` to `markdown-preview-enhanced.openPreview` (NOT `openPreviewToTheSide`) — MPE handles intra-doc anchor links correctly where the built-in sometimes breaks them. Using `openPreview` keeps the preview in the same editor column without splitting.

Each swap uses a `-` (unbind) entry to remove the extension default, then a positive binding with the other shortcut. typedown also has a toggle pair (`openWysiwygEditor` / `openDefaultEditor` gated on `typedown.editorIsActive`), so both commands are rebound.

Extension command IDs:

- `typedown.openWysiwygEditor` (when `!typedown.editorIsActive`) / `typedown.openDefaultEditor` (when `typedown.editorIsActive`)
- `markdown-editor.openEditor` (when `editorTextFocus && editorLangId == markdown`)



## Top Frictions

- **All IDEA patches currently applied and stable** (verified 2026.09.29). Wibey 1.0.28 from `brian/local-combined` includes upstream main plus image-paste-fix and conversation-title-features. Rebuild from that branch to keep the local plugin current.
- Parallel Wibey agents now available in all three IDEs (as of 2026.06).
- Top silly frictions: let me buffer up my next prompt, and make it super-easy to reference the current file and selection.
  - Wibey allows enqueuing the next prompt while busy in VS Code and Cursor, but not in IDEA. Allowing this in IDEA would give 30% of the value of parallel agents. I don't like interrupting agents to add their next prompt and then tell them to first finish the previous one.
  - In no IDE does Wibey automatically track the current selection as context, which Github Copilot does in IDEA and VSCode, probably Cursor too.
  - Cursor+Wibey: Cmd-L broke! It now inserts selection context into builtin chat, not Wibey Chat.



## Copilot

### Agent shell-command approvals

For VS Code and Cursor, put these settings in each IDE's user
`settings.json` to maximize automatic approval of agent tool calls and avoid
routine sync/delete prompts:

```json
{
  "chat.tools.global.autoApprove": true,
  "chat.tools.urls.autoApprove": { "*": true },
  "chat.agent.maxRequests": 250,
  "git.confirmSync": false,
  "explorer.confirmDelete": false,
  "security.workspace.trust.untrustedFiles": "open"
}
```

These settings do not bypass macOS authorization, `sudo` passwords, GitHub
authentication, or other OS/security boundaries. IntelliJ IDEA's Copilot
`run_in_terminal` confirmation is controlled by the IDE/plugin tool host; no
supported persistent user setting was found that disables that confirmation.
When IDEA offers an **Always allow** or equivalent command approval, choose it
for trusted local agent work. Do not edit the plugin's generated tool registry
to fake approval; updates can overwrite it and the host may still enforce the
confirmation.

- **Works with VS Code, Intellij IDEA, Android Studio**
- **Unlimited use of GPT4.1**
- **Supports Gemini3Pro**
- **Displays premium request usage (in IDEA and VSCode)**
- Extra Info from Claude Opus 4.5:
  - **Free tier available (2000 completions/month, 50 chat messages)**
  - **Native GitHub integration (PR summaries, issue context)**
  - **Multi-file edits in agent mode with @workspace**
  - *No MCP (Model Context Protocol) support*



### IDEA Copilot Session History

Copilot chat history is stored per session in `~/.config/github-copilot/iu/chat-agent-sessions/<session-id>/copilot-agent-sessions-nitrite.db`; background agent state lives under `bg-agent-sessions/`. Cross-session history and sync only work when `cloudSessionStorageEnabled` is on, so an empty history pane after restart usually means either a fresh session/profile or that cloud session storage is disabled for this account/org. Current local session DBs I saw were `3FMXwLrUerHmiiZCqfXVjWufjm7`, `3FLCWBn65rrleMeg45Km2BjhCNf`, `3FjwlRcsTTFtmIbTOVR9yags5jH`, and `3GCdRF0lFhyiiQ9zf2TUGxaFHGH`.

**Caution:** IDEA project/root cleanup is not purely cosmetic. Editing attached roots, `.idea/modules.xml`, `*.iml`, `.idea/vcs.xml`, or Copilot-related project state can make IDEA reopen as a different project/session, which can reset UI customizations and cause Copilot to reconnect to a different set of local conversations after restart. Before agent edits, back up the affected IDEA config files and treat root changes as a smallest-possible patch, not a broad "tidy up" pass.

## Cursor

**GitHub Copilot Chat is not supported in Cursor** — the Chat extension requires VS Code ^1.111.0 and Cursor is on 1.105.x, so it cannot be installed.

### Proxy (Walmart vs personal laptop)

Proxy is configured **per machine** in Cursor User settings. Personal laptop has proxy disabled; Walmart laptop should keep proxy so Cursor can reach the internet via corporate proxy.

- **Where:** `~/Library/Application Support/Cursor/User/settings.json` (macOS). Each laptop has its own file.
- **Personal laptop (no proxy):** Remove or leave unset: `http.proxy`, `http.proxySupport`, and the Walmart-only `http.noProxy` entries. Keep `http.noProxy` with just `.local` and `169.254/16` if you like.
- **Walmart laptop (restore proxy):** Add or restore these in the same `settings.json`:

```json
"http.noProxy": [
    ".walmart.com",
    ".wal-mart.com",
    ".walmartlabs.com",
    "wmlink",
    "wamnetNAD",
    ".local",
    "169.254/16"
],
"http.proxy": "http://proxy.wal-mart.com:9080",
"http.proxySupport": "override",
"http.proxyStrictSSL": true,
"http.systemCertificates": true,
"http.fetchAdditionalSupport": true,
"http.systemCertificatesNode": false,
```

Then restart Cursor. If you use Settings Sync, turning off sync on the Walmart laptop (or re-adding these after a sync) keeps the proxy from being overwritten.

### Panel Management (Move to Opposite Sidebar)

To move a sidebar panel (Explorer, Search, etc.) to the opposite side of the UI:

1. Press `⌘⇧P` to open the command palette
2. Run `Move View`
3. Select the panel to move (e.g., Explorer)
4. Choose **"Move to Opposite Sidebar"**

This is useful for repositioning panels between left and right sidebars as needed.

- *every model request counts against monthly budget*
- **seamless parallel agents**
- **Displays premium usage summary (cf. "usage summary")**
- **in-context edit prompt**
- Extra Info from Claude Opus 4.5:
  - **Composer mode for multi-file refactoring**
  - **Built-in codebase indexing for semantic search**
  - **Tab completion with diff preview**
  - *Closed source, can't self-host or audit*



## VS Code

- **Supports Copilot**
- **Supports parallel agents as of 2025-12**
- Extra Info from Claude Opus 4.5:
  - **Free, open source, massive extension ecosystem**
  - **Native Copilot integration with Edit mode**
  - **Remote development (SSH, containers, WSL)**
  - *Chat panel context limited vs dedicated AI IDEs*
- *Accept All in diff review simply accepts what's on disk and ends the review — safe even if the user made local edits during review.*



### Human-vs-Agent Conflict Diff

When an agent writes to a file while you have unsaved edits in your buffer, VS Code opens a `(in file) ↔ (in Visual Studio Code)` diff. The green `+` lines are your buffer; the red `-` lines are what's on disk. Options:

- **Edit the green lines** — make any adjustments you want right in the diff view, then ⌘S to save your version to disk.
- **Toolbar ✓ (Accept)** — writes your entire buffer to disk as-is.
- **Toolbar ↩ (Revert)** — discards your buffer and reverts to the disk version.

There are no per-hunk accept buttons in this diff type (those only appear in the 3-way merge editor).

### Proxy / GitHub Copilot off VPN

When VPN is off, `proxy.wal-mart.com:9080` is unreachable, blocking GitHub Copilot. Fix: add GitHub domains to `http.noProxy` so Copilot bypasses the proxy entirely (internal traffic still routes through it).

Current `http.noProxy` in `~/Library/Application Support/Code/User/settings.json` (as of 2026.04.26):

```json
"http.noProxy": [
    ".local",
    "169.254/16",
    ".walmart.com",
    ".wal-mart.com",
    ".walmartlabs.com",
    "wmlink",
    "wamnetNAD",
    "github.com",
    ".github.com",
    ".githubcopilot.com",
    ".githubusercontent.com"
]
```

`http.proxy` and `http.proxySupport: override` remain in place for all other traffic.

### Markdown Preview Font Size

**Locked configuration (2026.04.29):**

- **Markdown Preview Enhanced (MPE) preview rendering**: `14px`, `line-height: 1.2` in `~/.local/state/crossnote/style.less`
- **VS Code built-in preview** (`markdown.preview.fontSize`): `13`, `line-height: 1.2` (fallback setting; MPE uses its own renderer)
- **Apply in both Code and Cursor** for parity: `~/Library/Application Support/{Code,Cursor}/User/settings.json`

```json
"markdown.preview.fontSize": 13,
"markdown.preview.lineHeight": 1.2,
```



### Markdown WYSIWYG Editor Font → Match Preview Font

VS Code's `[markdown]` language-specific `editor.fontFamily` applies to the raw source editor — setting it to a proportional font breaks pipe-delimited tables. **Do not use it.** Each WYSIWYG editor has its own font control:

- **TypeDown**: has `typedown.editor.fontFamily` and `typedown.editor.fontSize` settings — current matching settings in `settings.json`:
  ```json
  "typedown.editor.fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe WPC', 'Segoe UI', system-ui, 'Ubuntu', 'Droid Sans', sans-serif",
  "typedown.editor.fontSize": 13
  ```
- **Zaaack**: uses `markdown-editor.customCss` in settings.json with font-size `13px` and `line-height: 1.2`:
  ```json
  "markdown-editor.customCss": ".vditor .vditor-reset, .vditor-ir pre.vditor-reset, .vditor-sv { font-family: -apple-system, BlinkMacSystemFont, 'Segoe WPC', 'Segoe UI', system-ui, 'Ubuntu', 'Droid Sans', sans-serif !important; font-size: 13px !important; line-height: 1.2 !important; } .vscode-light .vditor--dark .vditor-reset { color: #111111 !important; background: #ffffff !important; } .vscode-light .vditor--dark .vditor-ir pre { color: #111111 !important; }"
  ```

Learned behavior: if a markdown tab still looks fixed-width after changing `typedown.editor.fontFamily`, the tab is likely Zaaack (`markdown-editor.openEditor`) rather than TypeDown (`typedown.openWysiwygEditor`). In that case, `markdown-editor.customCss` is the correct knob.

### Multiple Markdown Tabs (No Reuse)

To stop VS Code from reusing a single preview/pseudo-preview tab and allow side-by-side markdown panes, set in `~/Library/Application Support/Code/User/settings.json`:

```json
"workbench.editor.enablePreview": false,
"workbench.editor.enablePreviewFromQuickOpen": false
```

For Markdown Preview Enhanced specifically, also set:

```json
"markdown-preview-enhanced.previewMode": "Multiple Previews"
```

Without this, MPE defaults to **Single Preview** and keeps one preview tab that follows whichever markdown source tab is active.
MPE notes this setting requires a window reload/restart to take effect.

Practical workflow:

- Open Markdown Preview Enhanced with `⇧⌘V` (already rebound to MPE in this setup).
- Use `⌘\\` (Split Editor) or `Open Preview to the Side` to place additional previews/editors side-by-side.
- For WYSIWYG editors, use `Reopen Editor With...` and choose either TypeDown or Markdown Editor (Zaaack); with preview reuse disabled, each opened editor stays in its own tab.

Observed result: this workflow successfully enables independent previews per markdown file.

### Zaaack Find / Outline / Anchor Nav (patched)

⚙️ rows — find in file, structure, internal links — are added by `~/bin/patches/patch-zaaack.py`. Run after each Zaaack update; the script globs both `~/.vscode/extensions/` and `~/.cursor/extensions/` so one run covers both IDEs. Full patch procedure and implementation notes: **ToolMods.md → Zaaack**.

### Markdown Preview Theme (auto-switch)

If your Markdown preview (for example, Markdown Preview Enhanced) does not switch between light/dark automatically when VS Code or your OS changes theme, add this to your user `settings.json`:

```json
"markdown-preview-enhanced.previewColorScheme": "systemColorScheme"
```

This makes the preview follow the active VS Code editor theme (and thus `window.autoDetectColorScheme`). If you prefer the preview to follow the OS system color scheme directly, use `"systemColorScheme"` instead of `"editorColorScheme"`.

### Cmd+Shift+V → Markdown Preview

**VS Code:** `keybindings.json` unbinds `⇧⌘V` from the built-in and rebinds it to `markdown-preview-enhanced.openPreview` (NOT `openPreviewToTheSide`) — MPE handles intra-doc anchor links correctly where the built-in sometimes breaks them. Using `openPreview` keeps the preview in the same editor column without splitting.

**Cursor:** `⇧⌘V` uses the built-in `workbench.action.markdown.openPreview` (preference). MPE's default binding is unbound via `-markdown-preview-enhanced.openPreview` in Cursor's `keybindings.json`.

### Zaaack Markdown Editor Patches

Dark theme, font, and link color patches. Full procedure: **ToolMods.md → Zaaack**.

### TypeDown Patches

Line-height, table padding, list spacing, and focus bug patches. Full procedure: **ToolMods.md → TypeDown**.

## IDEA

- **Superior features: search/find, git, debug, database, http, yaml preview**
- **Currently on 2026.2 GA/stable** (build 262.8665.258, released 2026.07.16; installed on Walmart laptop 2026.07.16). The 2026.2 EAP (auto-updated ~2026.06.27) has now shipped as stable — the config dir (`IntelliJIdea2026.2`) carried over from EAP → GA, so all EAP-era JAR patches survived the upgrade. The two 2026.2 breaking changes still require JAR patches (see ToolMods.md).
- **Current local tool versions (2026.10.02):** IntelliJ IDEA 2026.2.3; Wibey 1.0.28 from `brian/local-combined`; Code Puppy JetBrains 0.27.0 from the local `feature/active-context-pill` build (repo `~/src/code-puppy-ide`, fork `r0b0m29/code-puppy-ide`); Code Puppy Desktop 0.3.0. The Code Puppy artifact includes active-editor context suggestion, JDK 21 build detection, and the JCEF startup workaround — image paste and universal-constructor rendering are now stock upstream behavior, so the local `ImageAttachmentCache` duplicate was retired in favor of upstream's `ImageCache`.
- **2026.10.02 lesson:** the JetBrains marketplace plugin update silently replaced the local-combined build with a stock v0.27.0 build, dropping the active-context-pill feature. After any Code Puppy JetBrains marketplace update, re-check the installed plugin version/jar against `~/src/code-puppy-ide`'s `feature/active-context-pill` branch before assuming local mods survived — `unzip -p <plugin jar> META-INF/plugin.xml | grep version` against the installed plugin dir shows the truth.
- **Patch audit 2026.10.09 (personal Mac, 2026.2.3):** restored the missing JCEF remote-mode override (`idea.vmoptions`), Shuzijun 2.0.7 JCEF dependency + 13px font, MCP Server Services-panel suppression, sensitive-file dialog suppression, and built-in Markdown preview light/dark stylesheet. The active `VSCode OSX` keymap is supplied by the installed `keymap-vscode` plugin; no stale custom keymap XML was recreated.
- *command-approval constipation*
- *Parallel agents now supported (as of 2026.06)*
- *Cannot paste file/line reference!?*
- *Pending Changes panel sometimes fails to show agent-written files (new untracked files, or edits via MCP/Write tool). Check* `git status` *to catch anything the panel missed.*
- *⚠️ Accept All hazard: if the user makes local edits (including undos) while reviewing an agent diff, Accept All collapses those edits into the accept gesture and reverts them. Use per-chunk accept/reject instead.*
- Extra Info from Claude Opus 4.5:
  - **AI Assistant with JetBrains' own models + cloud options**
  - **Unmatched refactoring for Java/Kotlin (type-aware renames, extract method)**
  - **Built-in profiler and memory analysis**
  - *Expensive ($249/yr commercial, $169 w/ AI Assistant)*



### IDEA Keybindings

IDEA keybinding overrides are stored in `~/Library/Application Support/JetBrains/IntelliJIdea2026.2/keymaps/macOS copy.xml`. Edit this file to add standard bindings:

- **Zoom**: `⌘=` / `⌘-` (remapped from `^⌥=` / `^⌥-`)
  - Action IDs: `ZoomInIdeAction` / `ZoomOutIdeAction`
  - Keystroke format: `meta equals` / `meta minus` (with alternates `meta add` / `meta subtract`)
- **Open File**: `⌘P` (remapped from `⇧⌘O`)
  - Action ID: `GotoFile`
  - Keystroke format: `meta p`
- **Toggle Line Numbers**: `⌥L`
  - Action ID: `EditorToggleShowLineNumbers`
  - Keystroke format: `alt l`



### IDEA Workspace Roots

- On the personal Mac and the Mac mini, the Project view should expose these
  bounded content roots:

  ```text
  ~/Documents
  ~/lpscc
  ~/My Drive
  ~/src
  ```

  This corresponds to the personal laptop layout shown as `Documents`,
  `lpscc`, `My Drive [GDrive]`, and `src`. Attach the real directories in IDEA
  rather than only opening `~/src/tools`; the tools checkout is nested under
  `~/src` but should also have its own VCS mapping when it is being edited.

- Preferred LPSCC root: `~/lpscc` (the symlink to the shared-drive root).
- In Project view and attached directories, use `~/lpscc` rather than `~/My Drive/Libertarian/LPSCC`.
- For the tools repo, attach the **real repo path** `~/src/tools` as both an IDEA content root and a VCS root. Do **not** rely on the `~/bin` symlink for IDE root configuration.
- If a module file exists on disk but the root does not appear in IDEA, check `~/IdeaProjects/Personal/.idea/modules.xml` first. A stray `*.iml` file is inert until `modules.xml` actually lists it.
- If the folder appears in Project view but git status does not surface in the Commit tool window, check `~/IdeaProjects/Personal/.idea/vcs.xml` for a matching `<mapping ... vcs="Git" />` entry.
- For the tools repo specifically, the desired pair is a module pointing at `file://$USER_HOME$/src/tools` and a VCS mapping for `$USER_HOME$/src/tools`.
- If the wrong root shows up, remove the direct `My Drive/.../LPSCC` entry and reattach the symlinked root so the workspace stays stable across Drive remounts.
- Do not let agents rewrite unrelated module/root config while doing this cleanup; even removing one stale root can have side effects on IDEA layout state and Copilot's local session/history mapping after restart.



### Markdown Preview

The built-in Markdown preview uses `options/markdown.xml` under `MarkdownSettings`. Font size is 15px.

**Rendering engines (2026.2):**

- **JCEF preview** (`MarkdownJCEFHtmlPanel`) — right pane in "Markdown Split Editor" and the standalone Preview tab. Respects custom CSS. Default body font: `Helvetica, Arial, freesans, sans-serif` (bundled `default.css`).
- **Compose WYSIWYG editor** (`intellij.markdown.compose.preview.jar`, class `JcefLikeMarkdownStylingKt`) — the "Markdown Editor" tab (H/B/I toolbar). Hardcodes `FontFamily.SansSerif` (= SF Pro on macOS); reads `fontSize` from settings; ignores `fontFamily` and all CSS. **Table font size and cell wrapping are also hardcoded** — not configurable without patching the JAR.

**Valid** `MarkdownSettingsState` **fields in 2026.2:**

- `fontSize` (int) — affects both JCEF preview and Compose editor
- `fontFamily` (string) — passed to JCEF preview; ignored by Compose editor
- `useCustomStylesheetPath` (bool) + `customStylesheetPath` (string) — single external CSS file; path **must be inside the open project**, otherwise IDEA rejects it with an "unsafe custom stylesheet" warning and falls back to the default
- `useCustomStylesheetText` (bool) + `customStylesheetText` (string) — inline CSS text embedded in the XML; no path restriction, preferred approach

**⚠️ Dead field in 2026.2:** `customStylesheets` (the list form used by 2025.3 and earlier) is silently ignored in 2026.2. IDEA never logs an error — the CSS is simply never applied.

**To apply custom CSS in 2026.2:** Settings → Languages & Frameworks → Markdown → choose "Custom stylesheet text" (inline mode) and paste CSS there. Do not use the file-path option unless the CSS file lives inside the current project.

**Light/dark fix (2026.2.3):** the inline stylesheet is restored in
`~/Library/Application Support/JetBrains/IntelliJIdea2026.2/options/markdown.xml`.
It supplies explicit light colors and a `prefers-color-scheme: dark` block for
the page background, body text, links, code blocks, blockquotes, and tables.
If IDEA is running while this file is changed, restart IDEA before judging the
result; the Markdown preview tab may also need to be closed and reopened.

Quick notes:

- `MarkdownSettings.fontSize` lives in `options/markdown.xml`, not `editor-font.xml`.
- Editing `markdown.xml` while IDEA is running has no effect — IDEA reads settings at startup and writes them on exit (overwriting any manual edits made while running). Use the Settings UI instead.
- After changing font size via the Settings UI, close/reopen the Markdown tab to see the change in the JCEF preview.



### Disable "Allow Edits to Sensitive Files" Dialog

Set registry key `idea.readonly.fragments.notification.enabled` to `false`.

**Status 2026.07.17:** APPLIED on the Walmart laptop's 2026.2 GA config (file method, IDEA quit first).

**Preferred (IDEA running):** Help → Find Action (`⇧⌘A`) → "Registry..." → search `idea.readonly.fragments.notification.enabled` → uncheck. Takes effect immediately, no restart.

**File method (IDEA must be QUIT first):** append to `~/Library/Application Support/JetBrains/IntelliJIdea2026.2/early-access-registry.txt`, then restart:

```
idea.readonly.fragments.notification.enabled
false
```

⚠️ Do NOT edit this file while IDEA is running — IDEA reads the registry at startup and rewrites this file on exit, clobbering any manual additions.

### Shuzijun Markdown Editor Patches

Currently applied to Shuzijun 2.0.7: font size patch (13px body text) and
IDEA 2026.2 compat fix (`JBCefApp` classloader). The JCEF dependency is
required, not optional. The MCP Server plugin Services panel suppression is
also applied. Full procedures: **ToolMods.md → Shuzijun** and
**ToolMods.md → MCP Server Plugin**.

### JCEF Remote Mode (built-in Markdown preview + Shuzijun both broken)

**Symptom:** Built-in IDEA Markdown preview shows nothing / "No subscribers for documentReady"; Shuzijun WYSIWYG tab throws NPE in `JBCefApp.createMessageRouter()`. Both broken simultaneously.

**Root cause:** IDEA 2026.2 enables JCEF out-of-process (remote) mode by default; native CEF objects are null in remote mode, breaking all JCEF consumers. Full root cause chain and fix: **ToolMods.md → JCEF Remote Mode**.

**Fix summary:** add `-Djcef.remote.enabled=false` to `~/Library/Application Support/JetBrains/IntelliJIdea2026.2/idea.vmoptions`. Restart IDEA. **Applied:** 2026.07.02; restored for the 2026.2.3 config on 2026.10.09.

### Wibey Extension Patches

New conversation bug fix (`clearMessages` on `newParallelSession`). Full procedure: **ToolMods.md → Wibey Extension**.

### Wibey IDEA — Image Paste Fix

**Problem:** Cmd+V with any clipboard image was silently broken. Root cause: `IdeEventQueue` intercepts Cmd+V before any Swing handler — `paste()`, input maps, and `TransferHandler` are all bypassed.

**Fix:** `IdeEventQueue.addDispatcher()` in `InputAttachmentManager.setupClipboardPaste()`. Dispatcher tied to panel `Disposable` (not project) to avoid accumulating stale handlers.

**Files:** `InputAttachmentManager.kt`, `UserInputPanel.kt` — 7 unit tests.

**PR:** [#170](https://gecgithub01.walmart.com/genaica/wibey-jetbrains-plugin/pull/170) · **Project doc:** [WibeyIDEAImagePaste.md](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared/blob/main/projects/WibeyIDEAImagePaste.md)

### Wibey IDEA — Conversation Title Features

Three fixes/features on top of stock 1.0.20:

- **Sidecar persistence:** `autoNameFromMessage()` now persists to sidecar JSON; History panel no longer reverts to last prompt on refresh.
- **Active-chat title strip:** 28px strip (label + pencil) above the chat area; inline rename with Enter/Escape. Previously rename only existed in the History panel.
- **Agent-driven rename:** "rename this conversation to X" triggers `wibey_set_conversation_title` in-process MCP tool; title updates mid-stream. Requires `createSdkMcpServer` + `queryOptions.mcpServers` (not `Options.tools`).
- **User-title guard:** once a user manually renames, subsequent prompts don't overwrite it.

**Files:** `ConversationManager.kt`, `SessionManager.kt`, `NativeChatToolWindowPanel.kt`, `ChatStreamHandler.kt`, `BunBridge.kt`, `StreamChunk.kt`, bridge TS files — 22 unit tests.

**PR:** [#169](https://gecgithub01.walmart.com/genaica/wibey-jetbrains-plugin/pull/169) · **Project doc:** [WibeyTitleFeatures.md](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared/blob/main/projects/WibeyTitleFeatures.md)

### Upgrading the Local Wibey Plugin

`brian/local-combined` combines local image-paste and conversation-title features with upstream main. Check the branch and current `origin/main` history to determine which local mods remain unique before merging.

To install the build in the active IDEA instance, run `./gradlew buildAndInstall` from Terminal.app, then restart IDEA. For a reviewed artifact, install the timestamped ZIP from `~/Downloads/` using **Settings → Plugins → Install Plugin from Disk**.

---



## Wibey Skills



### usage-dashboard: UTC day-boundary bug

Sessions after ~7 PM CDT credited to tomorrow due to UTC bucketing. Patch applied to `wibey_usage_lib.py` + `wibey-usage`. Full procedure: **ToolMods.md → usage-dashboard**.

### usage-dashboard: auto-regeneration via SessionEnd hook

The dashboard HTML at `~/.wibey/usage/dashboard.html` is static — baked at generation time. It must be regenerated to show new sessions. The `SessionEnd` hook in `~/.claude/settings.json` calls `session-end-usage.py`, which records to the DB and then spawns `wibey-usage dash --no-open` to regenerate the HTML automatically after each session.

**Hook config** (`~/.claude/settings.json`):

```json
{
  "type": "command",
  "command": "~/.claude/hooks/session-end-usage.py",
  "timeout": 30,
  "statusMessage": "Recording usage metrics and refreshing dashboard..."
}
```

Timeout is 30s (not 10) to allow time for the dash regeneration subprocess.

`**--no-open` flag** — `wibey-usage dash --no-open` generates the HTML without opening a browser tab. Supported in both installed (`~/.wibey/usage/wibey-usage`) and skill source (`~/.wibey/skills/usage-dashboard/scripts/wibey-usage`).

**If today's data is missing:** the HTML is stale — regenerate manually: `~/.wibey/usage/wibey-usage dash`

Files that implement auto-regen (keep in sync):

- `~/.claude/hooks/session-end-usage.py` (active hook)
- `~/.wibey/skills/usage-dashboard/scripts/session-end-usage.py` (skill source)
