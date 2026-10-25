# Tool Modifications

Maintainer reference for agents rebuilding or repairing Brian's toolchain. [Tools](Tools.md) is the human-facing usage guide. Within each component, modifications appear in descending significance. Read source before reapplying a patch; installed metadata is not live acceptance evidence.

## Contents

- [Shuzijun source build](#shuzijun-source-build)
- [Zaaack source build](#zaaack-source-build)
- [Code Puppy source builds](#code-puppy-maintained-source-builds)
- [TypeDown patches](#typedown-patches)
- [Codex file context](#codex-file-context)
- [Wibey JetBrains](#wibey-jetbrains-source-build)
- [Build artifact handoff](#local-build-artifact-rule)
- [IDEA maintenance](#idea-maintenance)
- [VS Code and Cursor configuration](#vs-code-and-cursor-configuration)
- [Agent permissions](#agent-permissions)
- [Git on VPN](#git)
- [Usage dashboard](#wibey-skills-usage-dashboard)

## Shuzijun Source Build

Source: `~/src/idea-markdown-editor`, branch `brian/markdown-ux`; [fork](https://github.com/BrianHoltz/markdown-editor), [upstream](https://github.com/shuzijun/markdown-editor). Keep `origin` at the fork and `upstream` at Shuzijun. Plugin ID remains `com.shuzijun.markdown-editor`. Source and installed descriptor are `2.0.7-local.16` (2026.10.25).

### Maintained modifications

- **Search input safety:** file editors use off-screen JCEF rendering, while non-file panels retain windowed rendering. On macOS, windowed JCEF can receive typed characters in the document despite Swing reporting the search field focused. Do not treat focus-owner assertions as proof of routing safety. Preserve OSR and the delayed focus/cancellation handling in `MarkdownHtmlPanel`.
- **Save/reload safety:** `template/default.html` supplies force-save and adjacent reload controls with equal responsive-toolbar priority. Dirty reload arms a three-second second-click confirmation using `vditor.tip`; `window.confirm()` is suppressed without a JCEF dialog handler. Save displays saved/unsaved/saving/failure states.
- **Theme and typography:** `vditor/style.css` maps rich text and tables to IDE/Vditor colors, overriding bundled light-content styles. `MarkdownPreviewFileEditor` listens for look-and-feel changes and refreshes reselected tabs (local.16). Preview font size and linear UI scale feed typography and browser zoom; do not pass CEF's logarithmic zoom value instead. Source stays monospace; tables wrap within pane width.
- **Editing integrity:** `vditor/list-backspace.js` preserves list spacing when Backspace removes an empty bullet after nested items (local.15). Do not replace it with plain DOM deletion that corrupts Markdown structure.
- **Navigation and find:** plain-click/Option-edit handling, duplicate/Unicode slugs, hidden named anchors and cross-document fragment navigation retain their bridges. `vditor/search-count.js` counts literal, case-insensitive, non-overlapping visible matches while `CefBrowser.find()` owns highlighting. Reject stale bridge results when queries change.
- **Compact controls:** adaptive `»` overflow, viewport-clamped tooltips and persistent toolbar/raw-HTML visibility live in the template and stylesheet. Hidden mode reduces rich-editor padding to 12px; normal mode uses symmetric 35px. Preferences use `PropertiesComponent`, not document edits.
- **Runtime compatibility:** `plugin.xml` requires `com.intellij.modules.jcef`. Startup-specific resource prefixes isolate cached assets, and browser warnings/errors reach `idea.log`. Gradle accepts `localIdePath` and reuses the upstream base changelog entry for local metadata.

### Build and validation

Use the installed IDEA runtime instead of downloading another platform:

```sh
set -e
cd ~/src/idea-markdown-editor
export JAVA_HOME="/Applications/IntelliJ IDEA.app/Contents/jbr/Contents/Home"
node --test test/*.test.cjs
./gradlew --no-daemon -Dorg.gradle.java.home="$JAVA_HOME" \
  -PlocalIdePath="/Applications/IntelliJ IDEA.app" clean test buildPlugin
STAMP=$(date "+%Y%m%d.%a.%H%M")
```

Read `pluginVersion` from `gradle.properties`, then deposit the matching `build/distributions/markdown-editor-<version>.zip` under the [artifact handoff](#local-build-artifact-rule), using `theme` for this source change. `set -e` prevents packaging/deposit after failed tests.

Node regressions cover search counts, focus cancellation, OSR selection, list Backspace, startup assets, typography and theme refresh. The deterministic Java/DOM harnesses do not emulate macOS native text routing or full JCEF geometry. Brian confirmed ⌘F in local.14 on 2026.10.18; later installed metadata alone does not extend that acceptance to every local.16 behavior.

### Legacy installed-JAR patch

[patch-shuzijun.py](../patches/patch-shuzijun.py) is a rollback tool for Marketplace 2.0.7. Do not apply it to the maintained source build. The source dependency and theme handling supersede installed-JAR surgery.

## Zaaack Source Build

Source: `~/src/vscode-markdown-editor`, branch `brian/markdown-ux`; [fork](https://github.com/BrianHoltz/vscode-markdown-editor), [upstream](https://github.com/zaaack/vscode-markdown-editor). Keep `origin` at the fork and `upstream` at Zaaack. Extension ID remains `zaaack.markdown-editor`.

Source is `0.1.22-local.7`; the registered VS Code installation is still `0.1.22-local.6`. Cursor registers Marketplace `0.1.20`, despite an older `0.1.13` directory also existing. Read `extensions.json`, not directory glob results, to identify the registered version (2026.10.25).

### Maintained modifications

- **Find and navigation:** `media-src/src/search.ts` provides one non-mutating toolbar/⌘F bar across modes and theme reinitialization. Heading parsers skip fences, handle Setext/inline formatting, and disambiguate duplicate/Unicode headings. `src/outline.ts` registers `markdownEditorOutline` under Explorer: `outline` is a view ID, not a view container, and custom webviews lack the built-in document-symbol path.
- **Link and file routing:** capture-phase handlers precede Vditor editing clicks; plain-click follows links, Option/Alt-click edits. `src/extension.ts` resolves relative files separately from fragments, reports failures and handles cross-document anchors. Command-mode panels are per-document, not a singleton.
- **Theme and readability:** dark themes select GitHub Dark code highlighting and remove light grid backgrounds; explicit non-GitHub palettes remain unchanged. Rich text uses theme-aware colors and separate typography controls from source.
- **Editing integrity:** `media-src/src/list-backspace.js` preserves nested-list spacing on empty-bullet Backspace (local.7; absent from the installed local.6).
- **Responsive controls:** `responsive-toolbar.ts` moves existing controls into a single-row `»` tray, preserving upstream handlers and order. Save, Find, More and mode controls have strongest retention. Keyboard traversal, Escape, outside clicks, submenu bounds and narrow-pane tooltips remain supported.
- **Persistent appearance:** `appearance.ts` stores toolbar and raw-HTML preferences in extension global state, including Settings Sync. Hidden mode removes margin annotations/gutter and uses 12px side padding. Hidden HTML remains navigable; source/fenced examples are untouched.
- **Chat context:** **Add Active File to Copilot Chat** resolves standard, custom and this extension's webview tabs before invoking `workbench.action.chat.attachFile`. Capture the active file before focus changes; do not fall back to a stale text editor.
- **Bundled locales:** `lang.ts` and `build.js` bundle Vditor's English/Japanese/Korean/Chinese dictionaries. An empty `VditorI18n` object produces undefined labels; Vditor has no English fallback for them.

### Build and validation

```sh
set -e
cd ~/src/vscode-markdown-editor
npx --yes pnpm@10.32.1 install --frozen-lockfile
npx --yes pnpm@10.32.1 build
npx --yes pnpm@10.32.1 --filter media-src exec tsc --noEmit
npx --yes pnpm@10.32.1 test
VERSION=$(node -p 'require("./package.json").version')
npx --yes --package @vscode/vsce vsce package --no-dependencies \
  --out "markdown-editor-$VERSION.vsix"
STAMP=$(date "+%Y%m%d.%a.%H%M")
```

Keep the canonical VSIX in the repo root and deposit with suffix `listfix` using the [handoff](#local-build-artifact-rule). Install the Downloads copy with `code --install-extension "$OUT" --force`, then reload the existing VS Code window. Disable auto-update to retain the source build. Do not run the legacy patcher against it.

Browser tests need their declared browser dependency. Follow [browser automation rules](AgentRules.md#browser-automation) and the host's setup workflow before launching any browser; do not blindly install/drive stock Chromium. Tests cover bundled labels, outline lifecycle, anchors, links, search, unchanged Markdown, list editing and toolbar geometry at narrow/wide widths. Synthetic browser checks do not establish live extension-host parity or external-file reread.

### Legacy Zaaack patcher

[patch-zaaack.py](../patches/patch-zaaack.py) supports the older installed-bundle route, not the source build. Read its current supported variants before running it; it can target both VS Code and Cursor versioned directories, including inactive installations.

It patches `main.js`, `main.css`, `out/extension.js` and `package.json`, with backups and idempotency markers. Preserve these mechanics when extending it:

- **Multipanel and outline:** a per-file `panelsByPath` map precedes outline registration, document/focus/disposal updates and scroll messages. Explorer owns the tree; a webview does not supply the native Outline provider.
- **Navigation:** capture clicks on both anchors and IR `data-type="a"` spans. Strip Vditor marker spans from heading text before slugging. The postMessage wrapper is a fallback, not the primary handler.
- **Find:** exclude toolbar, hints, hidden UI and the search overlay. Normalize parents after removing highlight spans, or multi-character queries break across fragmented text nodes.
- **Reinjection:** preserve both enhancer boundary markers; searching for the first `})();` can truncate at an inner function. Theme rebuilds require reattachment to the new editor element.
- **Theme:** preserve dark table/text/link overrides using VS Code tokens. Do not layer legacy CSS over source-integrated styling.

After a deliberate legacy patch, run `node --check` on affected JavaScript, reload the target IDE and verify find, links, outline and dark tables. Marketplace reinstall or the patcher's backups provide rollback; Git retains the retired byte-level recipes.

## Code Puppy: Maintained Source Builds

Walmart-internal; build only on the work laptop. Source: `~/src/code-puppy-ide`; JetBrains uses `feature/active-context-pill`, VS Code uses `brian/vscode-0.28.2-local`. Source root and installed JetBrains descriptor are `0.31.2`; VS Code registers `0.28.2`, Cursor `0.27.0` (2026.10.25).

### Local patches still required

- **Native paste dispatch:** `NativePaste.kt` provides IDEA `PasteProvider` support and a component-local action bound to the active keymap, preventing `EditorPaste`'s text-only adapter from swallowing images/files. Main and expanded prompt inputs reuse the existing transfer handler. Keep `AttachHandler`'s legacy Swing overload and disabled/read-only checks; do not restore duplicate image encoding/caching. Regression tests are in `NativePasteTest.kt` and `NativeAttachTest.kt`.
- **Editor context:** opt-in active-file/selection suggestions have separate native JetBrains and VS Code webview implementations. Preserve selection identities and capture context before changing focus.
- **VS Code links:** `packages/webview/src/lib/editor-link.ts` handles absolute paths and supported editor URIs, with theme-aware Markdown link colors. JetBrains no longer uses this renderer.
- **JDK resolution:** `scripts/gradle-jetbrains.sh` registers detected JDK 21 with Kotlin's toolchain resolver as well as setting `JAVA_HOME`.

### Upstream behavior: no local patch to reapply

JetBrains is native: upstream owns image caching/forwarding, encoding, drops, theme-aware Markdown colors and IDEA-based fonts. JCEF callback adapters, origin fallbacks, repaint nudges and browser zoom patches are obsolete. Leave IDEA JCEF defaults alone.

The installed plugin contains native classes; metadata and packaging do not prove live paste, editor-link or zoom acceptance. Source includes queue UI; do not revive the old blanket “cannot enqueue” rating without checking the current host.

### Build and validate

Inspect local-vs-upstream changes before merging; drop duplicate fixes upstream has absorbed. Fetch and merge, never rebase. Check approval boundaries before adding commits.

```sh
set -e
cd ~/src/code-puppy-ide
git fetch origin main
git merge --no-edit origin/main
bash scripts/gradle-jetbrains.sh test
bash scripts/build-jetbrains.sh
STAMP=$(date "+%Y%m%d.%a.%H%M")
```

The build script runs clean packaging/structure validation and verifies one native artifact for IDE build 243+, without obsolete browser wiring. No React build or distinct legacy implementation is required. Keep the canonical ZIP in `releases/`; deposit under the [handoff](#local-build-artifact-rule), using `paste` for the latest local change. An updater's legacy filename is a compatibility alias, not another UI.

VS Code's isolated branch requires `pnpm --filter @code-puppy/webview build` before `pnpm --filter code-puppy-vscode package`. Verify the branch and package version rather than packaging from the JetBrains checkout. Install via the appropriate `code` or `cursor --install-extension "$OUT" --force`, and inspect each editor's registered version separately.

For shared webview tests on Node 25, `NODE_OPTIONS=--no-experimental-webstorage` lets jsdom own localStorage. Run relevant Kotlin, TypeScript/webview and bridge checks for the changed scope; old passing-test counts are not current validation. Install the Downloads ZIP and restart IDEA before reporting loaded behavior. Marketplace updates can overwrite same-version local patches: inspect the installed JAR, not just its version label.

### TODO: native follow-ups

- Port full editor-link routing (absolute paths, `file:`, `jetbrains:`, `vscode:`, decoding and line navigation) to native dispatch, retaining unsafe-scheme filtering and tests. Native currently has simpler `file:` handling.
- Verify already-open conversations after IDEA zoom/Appearance changes; add a UI-settings refresh hook only if the native look-and-feel path is insufficient.

### Terminal link-color configuration

Terminal Rich output is independent of native Markdown. The work-laptop `~/.code_puppy/puppy.cfg` contains `rich_color_remap_json = {"blue": "#7aa2f7"}` (2026.10.25). Restart the engine after changes; do not patch the installed engine package.

## TypeDown Patches

Installed TypeDown is `1.1.7` in both VS Code and Cursor. The focus guard and compact CSS are present in both registered bundles (2026.10.25); recheck their bytes after updates.

- **Focus integrity:** in `src/markdownEditorInitScript.js`, ignore `documentChanged` when incoming text equals `lastMarkdown`. Otherwise save echoes call `setContent()` and destroy selection/focus.
- **Compact spacing:** `dist/extension.js` CSS uses 1.4 line height, `2px 10px` table-cell padding, zero paragraph margins inside cells/list items, and 0.25em list block margins.

Back up files, edit in place in each registered `tarikkavaz.typedown-markdown-editor-<version>` directory, check JavaScript syntax and reload each IDE. Verify cursor stability after save/paste and inspect table/list spacing. TypeDown's own font controls remain separate from these spacing patches.

## Codex File Context

Source: [package](../vscode/codex-file-context/package.json), [adapter](../vscode/codex-file-context/extension.js). The local helper `brianholtz.codex-file-context` contributes ⌃⌥⌘C and declares the Codex dependency. It is not registered on the work laptop; an orphaned extension directory is not an installation.

- **Custom-editor lookup:** resolve the active tab's local URI before opening chat, including TypeDown/Zaaack. Pass it explicitly to Codex's Add File to Thread action instead of relying on `activeTextEditor`.
- **Attachment limits:** reject untitled/non-file tabs; attach a path, not unsaved contents. Mocked resolution does not prove live keystroke delivery inside webviews.

### TODO: other context adapters

Keep editor lookup separate from harness attachment. Selection needs range and possibly buffer text; each harness needs a verified command/argument contract. IDEA needs selected `FileEditor` lookup, not text-editor-only assumptions. Cursor requires its own compatible installation. Picker ordering is a harness change, not an attachment-adapter feature.

## Wibey JetBrains Source Build

Walmart-internal; source `~/src/wibey-jetbrains-plugin`, branch `brian/local-combined`. Installed descriptor is `1.0.32_20261023.Fri.1532` (2026.10.25). The maintained branch has merged upstream Compose-only chat; it no longer carries the Swing image-paste, title-strip, context-pill, Markdown crash-guard or quota-writer source patches.

### Maintained modifications

- **Dependency-complete packaging:** `build.gradle.kts` verifies the distribution includes the five direct CommonMark runtime JARs. A standalone `build/libs` JAR is not installable.
- **Distinct local version:** packaging appends a build timestamp to the upstream base version.
- **Network/build support:** `settings.gradle.kts` retains corporate Maven/Gradle mirrors; remaining local differences are build/docs hygiene, not chat features.

### Rebuild

Inspect `git diff origin/main...HEAD` for unique local patches before merging. Preserve both upstream behavior and required local changes, without duplicating equivalent services/imports.

```sh
set -e
cd ~/src/wibey-jetbrains-plugin
git fetch origin main
git merge --no-edit origin/main
(cd bridge && bun install --frozen-lockfile && bun run build && bun run test -- --reporter=dot)
./gradlew test buildPlugin
STAMP=$(date "+%Y%m%d.%a.%H%M")
```

Read current toolchain settings from Gradle; do not retain the obsolete “local JDK 17 patch” claim. Build from Terminal.app when the host requires it. Resolve conflicts and service-registration errors before packaging. Keep the canonical ZIP in `build/distributions/`, strip the internal `_timestamp` from the release-version field when naming the Downloads copy, and follow the [handoff](#local-build-artifact-rule). Restart after installation.

### TODO: Compose follow-ups

Reassess active-editor suggestions against upstream selection handling before porting the retired context pill. Reassess agent-driven conversation rename against upstream AI titles. Do not revive Swing paste/title classes or carry the old PR stack as current implementation instructions; Git preserves them.

### Wibey VS Code: new-conversation patch

This is a VS Code webview patch, not an IDEA patch. The registered work-laptop extension is `1.0.31`; its bundle contains the clear calls shown below (2026.10.25).

`newParallelSession` must clear the visible transcript/todos/queue before asynchronous session creation, or failed creation leaves the old conversation displayed. Inspect the installed minified variable bindings against `newSession`/`cleared` before replacing exactly one occurrence. The documented 1.0.31 mapping is:

```js
// Existing:
case"newParallelSession":y.showChat();
// Patched:
case"newParallelSession":y.showChat(),c.clearMessages(),c.clearTodos(),B.clearQueue();
```

Back up `out/webview/webview.js`, verify the anchor and binding names, write in place, run `node --check`, then reload VS Code. Inspect actual installed bytes before reporting the patch active. The old `MultiSessionHandler.js` fallback applies to retired architectures, not 1.0.31. Do not copy version-specific variable names into a newer build blindly.

## Local Build Artifact Rule

[AgentRules — artifact completion gate](AgentRules.md#artifact-completion-gate) owns delivery and retention policy. Retention follows that single policy.

- Capture `STAMP=$(date "+%Y%m%d.%a.%H%M")` immediately after successful packaging, not when copying later.
- Keep the canonical output in the repo's release/distribution location; deposit the human-facing installer in `~/Downloads/`.
- Unless the project specifies otherwise, name it `<product>-<version>-<stamp>-<suffix>.<ext>`, with a lowercase, hyphen-free suffix shorter than ten characters. Never overwrite a different artifact.
- Verify ZIP/VSIX integrity, compare source and deposited bytes, and inspect expected plugin ID/version/dependencies. Do not create checksum sidecars.
- Run `~/src/tools/prune-artifacts --apply` after deposit; it implements the time-bucket/installed-build retention policy. Never delete user artifacts with `rm`.
- Deliver the exact Downloads basename as a clickable link. A build-only path, successful commit or unverified copy is not completion.

```sh
# ZIP, VERSION, PRODUCT, SUFFIX and STAMP come from the validated build.
OUT="$HOME/Downloads/$PRODUCT-$VERSION-$STAMP-$SUFFIX.${ZIP##*.}"
test ! -e "$OUT"
unzip -t "$ZIP"
cp -p "$ZIP" "$OUT"
cmp "$ZIP" "$OUT"
~/src/tools/prune-artifacts --apply
```

## IDEA Maintenance

### Markdown preview settings

Active work-laptop `options/markdown.xml` contains only `fontSize=14` (2026.10.25); the previously claimed inline light/dark stylesheet is not present.

The JCEF preview accepts `fontFamily`, `fontSize`, `useCustomStylesheetText`/`customStylesheetText`, or `useCustomStylesheetPath`/`customStylesheetPath`. File stylesheets must lie inside the project. The old `customStylesheets` list is ignored in 2026.2. Compose reads font size but ignores custom CSS/font family and hardcodes some table behavior.

Use Settings while IDEA runs: direct options-file writes can be overwritten on exit. Close/reopen a built-in preview when needed. Shuzijun has its own source-integrated theme/typography path.

### JCEF mode

The active work-laptop VM options do not force `-Djcef.remote.enabled=false` (2026.10.25). Leave the default intact. Brian confirmed Code Puppy worked after removal/restart on 2026.10.21; that older test is not evidence that current native Code Puppy needs JCEF. Diagnose Markdown browser failures separately.

### IDEA keybindings

Inspect the active keymap before editing; do not recreate stale custom XML when a plugin supplies the keymap. Local overrides use:

- **Zoom:** `ZoomInIdeAction` / `ZoomOutIdeAction`, `meta equals` / `meta minus` with optional `meta add` / `meta subtract`.
- **Open file:** `GotoFile`, `meta p`.
- **Line numbers:** `EditorToggleShowLineNumbers`, `alt l`.

The documented custom file is `keymaps/macOS copy.xml` under the 2026.2 config. Resolve actual current selection before applying changes.

### Workspace roots and Copilot session state

Follow [GitScheme — work project roots](GitScheme.md#work-project-roots), which owns the allowlist and content/VCS mapping checks. Back up affected metadata and make minimal patches: modules, VCS mappings and project color are independent. Never bulk-attach `~/src` or unrelated detected repositories.

<a id="copilot-session-state"></a>

Copilot stores session files under `~/.config/github-copilot/iu/chat-agent-sessions/<session-id>/copilot-agent-sessions-nitrite.db`, with background state under `bg-agent-sessions/`. This is a storage-location note, not permission to connect to any database. Do not publish ephemeral session IDs. Empty history can reflect profile/project identity or cloud-session settings; do not assert cloud storage is the sole cause. Preserve workspace/session state while diagnosing.

### IDEA memory

The recorded JPS OOM involved parsing chat-heavy workspace XML with a 700 MiB build heap; the affected project's configured build heap was raised to 2048 MiB (2026.10.20). Post-build verification remains unestablished. This is not evidence to increase the main IDE's 14000 MiB heap, trim conversation history, or rely on swap to exceed a JVM heap cap.

### Disable sensitive-file edit prompts

For the existing local preference, use **Help → Find Action → Registry… → `idea.readonly.fragments.notification.enabled`**, then uncheck. If changing the backing registry file, quit IDEA first and preserve other entries. Do not treat an old applied date as proof of current state.

### Suppress Services Panel Auto-pop

The installed MCP plugin descriptor still has an active `serviceViewContributor` and no suppression marker (2026.10.25). The old suppression is not installed.

If explicitly restoring this cosmetic patch, back up `plugins/mcpserver/lib/mcpserver.jar`, comment out only the `McpServiceViewContributor` registration in `META-INF/plugin.xml`, and add `__mcpNoServicesPanel__`. Preserve the archive inode and all other entries; verify the descriptor afterward. The MCP service/SSE endpoint is separate. Restart IDEA; plugin updates can overwrite the patch. Do not describe it as active without inspecting the installed JAR.

## VS Code and Cursor Configuration

### Preview, typography and shortcuts

User files live under `~/Library/Application Support/{Code,Cursor}/User/`. Inspect each independently; Settings Sync does not establish parity.

- **Independent previews:** `workbench.editor.enablePreview=false`, `workbench.editor.enablePreviewFromQuickOpen=false`, and Markdown Preview Enhanced `previewMode="Multiple Previews"`; reload for mode changes.
- **Typography:** both work-laptop built-in previews use font size 13 and line height 1.2; TypeDown uses size 13 and the system sans-serif stack (2026.10.25). Keep raw Markdown monospace. TypeDown owns `typedown.editor.fontFamily`/`fontSize`; Zaaack owns `markdown-editor.customCss`. The work-laptop VS Code legacy Zaaack CSS entry is commented out; do not claim it is active.
- **Theme:** Markdown Preview Enhanced `previewColorScheme="systemColorScheme"` follows OS theme. Editor-theme behavior is a different setting; do not describe the same value as both.
- **Keybindings:** unbind defaults before rebinding TypeDown `openWysiwygEditor`/`openDefaultEditor` and Zaaack `markdown-editor.openEditor`. Preserve TypeDown's `typedown.editorIsActive` gates.
- **Preview command:** VS Code uses `markdown-preview-enhanced.openPreview`; Cursor uses `workbench.action.markdown.openPreview`. Do not substitute `openPreviewToTheSide` when the intended behavior is the current editor group.

### Proxy configuration

Work-laptop VS Code and Cursor use `http://proxy.wal-mart.com:9080` with `http.proxySupport="override"` and strict SSL. Personal machines should not inherit the Walmart-only proxy. Keep settings machine-local.

`http.noProxy` includes internal suffixes (`.walmart.com`, `.wal-mart.com`, `.walmartlabs.com`, `wmlink`, `wamnetNAD`), local addresses (`.local`, `169.254/16`), and GitHub domains as needed for off-VPN Copilot (`github.com`, `.github.com`, `.githubcopilot.com`, `.githubusercontent.com`). Inspect the exact failing endpoint before changing bypass scope; noProxy is not a general VPN replacement.

Cursor's VS Code engine compatibility can prevent installing a newer Copilot Chat extension; check both declared engine versions instead of treating an old incompatibility as permanent product policy.

## Agent Permissions

### Copilot

VS Code's configured permissive preferences include `chat.tools.global.autoApprove=true`, URL auto-approval, `chat.agent.maxRequests=250`, `git.confirmSync=false`, `explorer.confirmDelete=false`, and `security.workspace.trust.untrustedFiles="open"`. These are local preferences, not authorization to bypass OS, authentication or explicit task boundaries. Cursor has different settings; its work-laptop request cap is 100 (2026.10.25).

IDEA Copilot terminal confirmations belong to the host/plugin. No supported persistent disabling setting is established; never edit a generated tool registry to fake approval.

### Antigravity and Gemini

These are personal-machine maintenance notes, not verified work-laptop configuration: the documented `~/.gemini/config/hooks.json` and `~/.gemini/settings.json` are absent on this work laptop (2026.10.25). Inspect the target machine before claiming settings are active.

- **Antigravity policy:** global `~/.gemini/config/config.json` uses `userSettings`; project files under `config/projects/` use `settings` plus permission grants. Historical local preferences select Turbo/eager execution, no sandbox and permissive file/network access. Global values alone may be shadowed by project settings. Resolve exact current schema/enums from the installed version before editing.
- **Configuration schema:** `~/.gemini/bin/agy` embeds `UserSettings`, `ProjectSettings` and permission protobuf descriptors. Known fields include `permissionPreset`, `autoExecutionPolicy`, `artifactReviewMode`, `internetAccessPolicy`/`internetPolicy` and `enableTerminalSandbox`. Watch/reload behavior must be checked against that version; do not assume binary-internal flags remain stable.
- **Markdown coordination hook:** inspect any `PreToolUse` hook against [fhold](fhold.md). The documented old hook's automatic stale-review release conflicts with current review-hold rules; do not install or revive that behavior. Resolve symlinks, use permits/safewrite as required, and never route around a tool protection boundary merely because shell writes are available.
- **Agent rule adapters:** [AgentRules](AgentRules.md#portable-agent-tooling) and [GitScheme](GitScheme.md) own canonical rule locations and workspace layouts. Do not copy personal root UUIDs or `/Users/brian` paths into work-project configuration.
- **Standalone Gemini:** inspect `~/.gemini/settings.json` and `trustedFolders.json` for `security.folderTrust`, `tools.sandbox`, `tools.autoAccept`, allowed tools and IDE integration. No local file means no verified active preference.
- **Gemini.app:** historical settings use `com.google.GeminiMacOS` preferences with JSON-encoded flag data and a persistent settings store. Internal flags and user aliases are version-specific, not a supported API. Do not connect to its database or restore old feature-flag lists as an automation recipe.

## Git

### SSH push hangs on VPN → push over HTTPS instead

The recorded VPN failure is an SSH banner hang on `ssh.github.com:443`, not proof of an HTTPS or credential failure. If reproduced, use the same repository over HTTPS with the host's configured credential helper; do not print or embed its token, and leave the configured SSH remote intact.

```sh
git push https://github.com/<owner>/<repo>.git <branch>
git ls-remote https://github.com/<owner>/<repo>.git refs/heads/<branch>
```

A literal-URL push does not refresh `origin/<branch>`. After verifying the remote SHA equals the pushed commit, refresh the tracking ref with `git update-ref refs/remotes/origin/<branch> <verified-sha>` or fetch over HTTPS. For non-fast-forward rejection, fetch that branch over HTTPS and merge `FETCH_HEAD`, never rebase or force-push. Follow current auth/blocking rules if credentials fail rather than treating HTTPS as an auth workaround.

## Wibey Skills: usage-dashboard

Canonical work source: `~/src/relationship-shared/.wibey/skills/usage-dashboard/scripts/`. Installed `~/.wibey/usage/` files and hooks can differ; resolve symlinks rather than treating the obsolete `~/.wibey/skills/` path as canonical.

- **Day bucketing:** both inspected source/installed `wibey_usage_lib.py` still use `msg_date = ts[:10]`; installed report cutoffs use UTC. The earlier claim that local-date conversion was applied is false for these bytes (2026.10.25). A local-date change needs source/installed alignment and historical-data handling, not a documentation assertion or automatic backfill.
- **SessionEnd:** `~/.claude/hooks/session-end-usage.py` resolves to the canonical script, which records session usage but does not spawn dashboard regeneration. Its configured timeout is 30s. Do not claim that this hook refreshes HTML merely because its status message says so.
- **Dashboard output:** `~/.wibey/usage/dashboard.html` is generated static HTML. `wibey-usage dash` regenerates/opens it; installed `--no-open` supports non-opening generation. Inspect scheduled refresh separately from SessionEnd.

TODO: decide whether to restore local-day bucketing and SessionEnd regeneration in the owning skill. Preserve existing data; any backfill requires a separately authorized workflow.

*[doc-audit](https://github.com/BrianHoltz/tools/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.10.25.Sun*
