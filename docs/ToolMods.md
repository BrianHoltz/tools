# Tool Modifications

Patch and modification procedures. See Tools.md for tool preferences, standings, and configuration.

⚙️ in a comparison table = capability added by a local patch documented here. Reapply after tool updates.

---

## Code Puppy: maintained source builds

Source: `~/src/code-puppy-ide`; JetBrains uses [feature/active-context-pill](https://gecgithub01.walmart.com/r0b0m29/code-puppy-ide/tree/feature/active-context-pill), while the isolated VS Code build uses [brian/vscode-0.28.2-local](https://gecgithub01.walmart.com/r0b0m29/code-puppy-ide/tree/brian/vscode-0.28.2-local). See [Tools.md](Tools.md#rebuilding-the-local-code-puppy-jetbrains-plugin) for builds, artifact naming, installation, and Marketplace overwrite precautions.

- **Editor context:** active-file and selection suggestions preserve distinct selection identities. Shared webview changes serve both IDE hosts; JetBrains-only runtime fixes do not apply to VS Code.
- **JDK discovery and startup:** `scripts/gradle-jetbrains.sh` locates and validates JDK 21; the JetBrains host warms proxy settings before JCEF initialization.
- **CEF callback compatibility:** `WebviewAssetScheme.ResourceHandler` extends the runtime `CefResourceHandlerAdapter`, supplying defaults for newer CEF callbacks instead of directly implementing an older interface. This avoids the IDEA 2026.2.3 / Chromium 144 callback incompatibility.
- **Navigation fallback:** `CpWebviewSchemeSetup.CUSTOM_SCHEME_ENABLED` is false in the maintained build. Registration succeeded but custom-scheme main-frame navigation failed on IDEA build 262.10968.63; the verified rendering path uses `http://cpwebview/`. The registration code and contract tests remain for future compatibility probes.
- **IDE zoom:** `CodePuppyWebviewPanel` listens to UI settings as well as look-and-feel and editor-scheme changes. It refreshes theme tokens and whole-browser zoom from IDEA's label-font size, including fixed-pixel controls and code. Conversation font harmonization remains separate from this zoom fix.

Validation: the 2026.10.12 JetBrains build and all 205 JVM tests pass. The built Downloads ZIP includes the callback, navigation, and zoom fixes; source changes do not establish that a running IDE has loaded the rebuilt plugin. VS Code 0.28.2 installation and its separate validation are recorded in [Tools.md](Tools.md#local-modifications-in-use).

## VS Code / Cursor: Zaaack Markdown Editor

### Zaaack source build

The editable source checkout is `~/src/vscode-markdown-editor`, branch `brian/markdown-ux`, in the [BrianHoltz GitHub fork](https://github.com/BrianHoltz/vscode-markdown-editor), based on the [MIT-licensed upstream extension](https://github.com/zaaack/vscode-markdown-editor). Local version `0.1.22-local.6` retains extension ID `zaaack.markdown-editor` and the existing custom editor ID, settings, and shortcuts. The source build is intended for VS Code; the Cursor installation is separate.

Source ownership:

- `media-src/src/lang.ts` and `media-src/build.js`: bundle Vditor's own locale dictionaries for English, Japanese, Korean, and Chinese. The legacy i18n intercept initialized `window.VditorI18n` to `{}`, which produced `undefined` toolbar tooltips and submenu labels; there is no English fallback for those strings.
- `src/outline.ts`: registers `markdownEditorOutline` under the valid `explorer` view container. The built-in `outline` is a view ID, not a view container. VS Code's public extension API does not expose a built-in Outline provider for these webview editors; Markdown Outline is a separate tree in Explorer. Both custom-editor and command-mode panels register with the same provider. Sidebar focus does not clear the tree; text-editor activation does.
- `media-src/src/headings.ts` and `src/headings.ts`: Vditor parses the full Markdown document into headings, skipping code fences and handling Setext headings and inline formatting. Sidebar navigation uses heading indexes to distinguish duplicates; anchor links use Unicode-aware slugs with duplicate suffixes.
- `media-src/src/utils.ts`: capture-phase link handling precedes Vditor's editing click handler. Plain click follows links; Option/Alt-click edits them. `markdown-editor.followLinksOnClick=false` requires Cmd/Ctrl-click instead.
- `src/extension.ts`: resolves relative file links separately from fragments, reports opening failures, and supports cross-document Markdown anchors. Command-mode editors keep independent per-document panels. **Add Active File to Copilot Chat** resolves text, custom-editor, and this extension's webview tabs, then sends the URI to VS Code Chat's native attachment action.
- `media-src/src/search.ts`: toolbar and Cmd/Ctrl+F share one non-mutating find bar. The active Vditor mode selects the search root, and matches can span inline formatting. The stable app host is observed across theme and mode changes.
- `media-src/src/responsive-toolbar.ts` and `media-src/src/main.css`: a single-row toolbar with a `»` overflow tray. ResizeObserver moves existing Vditor controls into the tray in their original order, preserving upstream handlers. Save, Find, More, and edit-mode controls have the strongest retention preference. The optional line-number gutter does not pad the toolbar. Escape and outside clicks dismiss the tray; keyboard Tab reaches the overflow controls. Submenus anchor below the tray to fit narrow panes.
- `media-src/src/appearance.ts`: persistent toolbar and raw-HTML visibility. The upper-right button hides/restores the toolbar; hidden mode removes the row, H1-H6 and other margin annotations, and line-number gutter, reducing rich-editor side padding to 12px. The raw-HTML toolbar button hides tag syntax and HTML-only rows without hiding rendered HTML blocks or fenced examples. Source mode is unaffected. Named HTML anchors remain navigable; search ignores hidden HTML markup. Show raw HTML or switch to source mode to edit tags. Preferences live in extension global state and participate in Settings Sync, without modifying documents.
- `media-src/src/main.ts` and `media-src/src/main.css`: dark editor themes switch the default GitHub code palette to GitHub Dark and remove Vditor's repeating light-grid image from fenced code blocks. Explicitly selected non-GitHub code palettes remain unchanged.

For another Mac, download the VSIX from [GitHub Releases](https://github.com/BrianHoltz/vscode-markdown-editor/releases) and run **Extensions: Install from VSIX**, then reload the window. For source work, clone the fork into `~/src/vscode-markdown-editor` and select `brian/markdown-ux`. The fork's default branch is the maintained local branch. The local checkout keeps `upstream` pointed at Zaaack and `origin` pointed at BrianHoltz.

Hiding the toolbar also hides raw HTML markup automatically; restoring the toolbar restores the independent HTML preference. The raw-HTML toggle can be in the `»` tray in narrow panes. Toolbar and menu hover/focus tooltips use a viewport-clamped overlay, avoiding Vditor's CSS suppression below 520px.

Build, validate, and install from the source checkout:

```sh
cd ~/src/vscode-markdown-editor
npx --yes pnpm@10.32.1 install --frozen-lockfile
npx --yes pnpm@10.32.1 build
npx --yes pnpm@10.32.1 --filter media-src exec tsc --noEmit
npx --yes pnpm@10.32.1 exec playwright install chromium
npx --yes pnpm@10.32.1 test
npx --yes --package @vscode/vsce vsce package --no-dependencies --out markdown-editor-0.1.22-local.6.vsix
STAMP=$(date "+%Y%m%d.%a.%H%M")
OUT="$HOME/Downloads/markdown-editor-0.1.22-local.6-$STAMP-copilot.vsix"
cp -p markdown-editor-0.1.22-local.6.vsix "$OUT"
cmp markdown-editor-0.1.22-local.6.vsix "$OUT"
code --install-extension "$OUT" --force
```

Keep the canonical VSIX in the repository root (`vsce package`'s normal output location) and install from the timestamped Downloads copy, following the [Local Build Artifact Rule](Tools.md#local-build-artifact-rule). Capture the completion timestamp immediately after successful packaging; `darkcode` is the newest-fix label. GitHub release uploads use the same timestamped filename as the Downloads copy. Delete previous Markdown Editor Downloads installers after verifying the replacement.

Reload VS Code with **Developer: Reload Window**. Disable auto-update for Markdown Editor through its extension gear menu to retain the source build. Do not run `patch-zaaack.py` against it; maintain fixes in source and rebuild. Marketplace installation remains the rollback route.

Automated validation covers the real bundled Vditor toolbar and submenu labels, sidebar hierarchy and focus lifecycle, duplicate/Unicode/inline-formatted heading navigation, relative and external link dispatch, Option-click editing, all three search modes, theme reinitialization, and unchanged Markdown after search. Toolbar geometry is checked at 240, 320, 450, 700, and 1200 pixels, including the real line-number script, keyboard traversal, overflow dismissal, and submenu bounds. The browser harness loads synthetic Markdown and Vditor assets locally. Live VS Code rendering requires a reload and an interactive check of Markdown Outline in Explorer; the standard Outline view can still show its unsupported-editor message.

### Multi-panel Editor + Outline + Find + Anchor Nav (`patch-zaaack.py`)

This section describes the legacy installed-bundle patcher, not the source build above.

The ⚙️ rows in the comparison table — find in file, structure, internal links — are added by `~/src/tools/patches/patch-zaaack.py` (canonical, lives in the `~/src/tools` repo and syncs across laptops via git). The `~/bin/patches/patch-zaaack.py` compatibility path resolves to the same script. It patches four files — `media/dist/main.js`, `media/dist/main.css`, `out/extension.js`, and `package.json` — in **both** `~/.vscode/extensions/zaaack.markdown-editor-<version>/` and `~/.cursor/extensions/zaaack.markdown-editor-<version>/` (each IDE has its own extensions dir). **Supports Zaaack 0.1.13, 0.1.15, 0.1.17, and 0.1.21**; the script globs all matching versioned dirs and supports their bundled Vditor variants via `P2_VARIANTS`.

**Why patch instead of switching editors.** Every webview-based WYSIWYG competitor (typedown, IDEA shuzijun, Mark Sharp, Unotes, vscode-markdown-wysiwyg, Teddy Editor) shares the same Cmd+F gap — VS Code's find UI doesn't reach into webview content, and vditor doesn't expose a public search API. The only extension with native find is `remcohaszing.markdown-decorations`, but it's decoration-only and loses the rich WYSIWYG rendering that makes zaaack the best choice. So patching zaaack beats every alternative on the market as of 2026.05.

**The `main.js` + `main.css` patch sites** — all are uniquely addressable and idempotent:

1. **after()-hook bridge** — call our enhancer once vditor finishes initializing:

- Anchor (vditor 3.8.4 / Zaaack ≤0.1.13): `after(){V_(),Y_(),sB(),K_()}`
- Anchor (vditor 3.11.2 / Zaaack 0.1.15+): `after(){vE(),wE(),VH(),bE()}`
- `P2_VARIANTS` in the script covers both; add new entries for future vditor bumps.
- Replace with the same + `,window.__zaaackEnhance&&window.__zaaackEnhance()}`
- Why this works: `after()` fires after vditor mounts the DOM — `window.vditor` is live and the editor `<div id="app">` is populated.

2. **Enhancer definition** — append `window.__zaaackEnhance` body just before the closing IIFE:

- Anchor: `vscode.postMessage({command:"ready"});})();`
- Insert before `})();`: the enhancer JS bracketed by markers `/*__zaaackEnhance__*/` … `/*__zaaackEnhance_end__*/`.
- Marker pair lets the script strip + re-inject cleanly (the old single-marker approach broke because `})();` inside the enhancer's `injectCssFixes` IIFE matched before the file's IIFE close).

3. **vscode.postMessage wrap** — drop intra-doc anchor `open-link` messages so VS Code does not try to open them as files:

- Anchor: `window.vscode=window.acquireVsCodeApi&&window.acquireVsCodeApi();window.global=window;`
- Insert between the two assignments: a wrapper that intercepts `vscode.postMessage({command:"open-link", href})` and, when the href is non-http and contains `#`, scrolls the matching heading via `window.__zaaackGotoAnchor(frag)` instead of forwarding the message.
- Marker `/*__zk_postwrap__*/` for idempotency.
- **Belt-and-suspenders, not the primary chokepoint.** In practice the capture-phase click handler in patch site #2 stops the click before vditor ever calls `window.open` / `postMessage`, so this wrap rarely fires. It exists as a fallback for any code path that bypasses the click listener (e.g. programmatic `vditor.api` calls, or a future vditor version that posts directly).

4. **Dark-table + optional vditor outline-width CSS block** — append one idempotent style patch to `main.css`:

- Marker: `/*__zaaackCssPatch__*/`
- Fixes dark-theme tables by overriding hardcoded light row/cell styles under `.vditor--dark .vditor-reset table ...` with vditor variables.
- Aligns markdown link colors with VS Code Markdown Preview tokens (`--vscode-textLink-foreground` / `--vscode-textLink-activeForeground`) so links are readable in dark themes and no longer render as electric blue defaults.
- Adds `.vditor-outline{width:var(--zaaack-outline-width,250px);resize:horizontal;...}` for installs that still expose vditor outline UI.

**The `extension.js` patch sites** (6 blocks, each bracketed by `/*__zk_outline_*__*/` markers):

1. **E_CLASS** — `MarkdownOutlineProvider` class + `_ZkHeading` + `_zkSlugify` helper, inserted before `class EditorPanel {`. Parses headings from `TextDocument` text (skips code fences + YAML frontmatter), builds a tree where h2 nests under h1 etc., exposes `getTreeItem()` / `getChildren()` for VS Code's TreeView.
2. **E_ACTIVATE** — registers the TreeView (`markdownEditorOutline`) and the `scrollTo` command in `activate()`. The command iterates `panelsByPath` to find the active panel and posts `{command:'scroll-to-heading', slug}` to its webview.
3. **E_VIEWSTATE** — `onDidChangeViewState` handler in the `EditorPanel` constructor. Sets context `markdownEditorActive` on focus (which shows the "Markdown Outline" view via the `when` clause in `package.json`) and refreshes the tree. On deactivate, checks if any panel is still active; if none, hides the outline.
4. **E_DOCCHANGE** — outline refresh on `onDidChangeTextDocument`, fires even when the webview is active (before the existing `if (this._panel.active) return` guard that suppresses content sync). Debounced at 500 ms.
5. **E_DISPOSE** — clears outline context + tree when the last panel closes.
6. **E_CREATE** — eagerly populates the outline in `createOrShow()` right after `panelsByPath.set`, so the tree is ready before `onDidChangeViewState` fires.

**The `package.json` patches** (idempotency marker: `"markdownEditorOutline"` anywhere in file):

1. **activationEvent** — adds `"onView:markdownEditorOutline"` so the extension activates when VS Code tries to show the view.
2. **views declaration** — adds `contributes.views.explorer` with `{id:"markdownEditorOutline", name:"Markdown Outline", when:"markdownEditorActive"}`. The `when` clause makes the view appear only when a Zaaack editor is focused.

**Why a TreeView instead of the built-in Outline.** Zaaack uses `createWebviewPanel` (not `CustomTextEditorProvider`), so when the webview is focused `activeTextEditor` is `undefined` and the built-in Outline goes blank — there's no `DocumentSymbol` source. A `TreeDataProvider` registered via `contributes.views` is the VS Code-sanctioned way to add custom sidebar views that track non-editor content.

**Enhancer responsibilities** (defined in the appended JS):

- **Anchor link nav.** Two layers, defense in depth:
  - *Primary*: a capturing `click` listener on `window`, `document`, and `documentElement`. Capture phase is critical so we fire **before** vditor's bubble-phase click handler on the editor element (at `main.js` byte ~388578: `var k=Object(H.d)(m.target,"data-type","a"); ...; window.open(k.querySelector(":scope > .vditor-ir__marker--link").textContent)`). The handler matches both `closest('a')` (preview-mode anchors) and `closest('[data-type="a"]')` (vditor's IR-mode link wrapper, which renders `[txt](url)` as `<span data-type="a"><span class="vditor-ir__marker--bracket">[</span><span class="vditor-ir__link">txt</span>...<span class="vditor-ir__marker--link">url</span>...</span>` — i.e. clicking the visible "txt" hits a SPAN, not an A, so a vanilla `closest('a')` walk returns null). For IR-mode hits the URL comes from `markerLink.textContent.trim()`. On any non-http URL: `e.preventDefault() + e.stopImmediatePropagation() + e.stopPropagation()`, then call `__zaaackGotoAnchor(frag)`.
  - *Secondary*: the postMessage wrap (patch site #3). Belt-and-suspenders for any path that bypasses the click listener.
  - `__zaaackGotoAnchor(frag)` resolves headings inside `.vditor-ir__content` / `.vditor-ir` / `.vditor-reset` / `#app` (first that exists). Lookup order: (a) `ed.querySelector('[id="' + CSS.escape(frag) + '"]')` (works when the markdown explicitly assigns ids), else (b) slug-match every `h1..h6`. The slug pipeline must use a `headingText()` walker that **skips child elements with class containing `vditor-ir__marker`** — vditor IR mode renders `## History

- 2026.07.15 Wed (3): Post-restart features broken (image paste no-op, no pencil). Root cause: Gradle incremental Kotlin compile cache served stale NativeChatToolWindowPanel.class (stock, no title bar fields). `./gradlew clean buildAndInstall` forced full recompile — all three patch fields confirmed in JAR via javap (sessionTitleLabel, sessionRenameTrigger, sessionTitleBar, startSessionRenameInline). Note: IdeEventQueue.addDispatcher(EventDispatcher, Disposable?) is deprecated in 2026.2 (non-nullable overload preferred) but still compiles + runs. Restart IDEA required.
- 2026.07.15 Wed (2): Wibey auto-updated to 1.0.23. Merged origin/main (v1.0.22+v1.0.23: commit attribution WIBEYCL-947, typescript-eslint pin) into brian/local-combined — clean merge, no conflicts. Rebuilt + installed: 1.0.23.jar with image-paste + title-features patches intact. Restart IDEA.
- 2026.07.15 Wed: Patch audit via Code Puppy. Already applied: JCEF remote disabled, readonly fragments dialog, MCP Services panel suppression, Shuzijun 2026.2 compat, usage-dashboard UTC fix, Wibey IDEA plugin from brian/local-combined (InputAttachmentManager/setupClipboardPaste + ConversationManager patches confirmed in installed 1.0.21 JAR). Newly applied: Zaaack re-patched in VS Code 0.1.17 + Cursor 0.1.13 (CSS upgraded, outline patches freshened, postMessage wrap reinstalled; both main.js + extension.js syntax-verified). VS Code Wibey 1.0.20 webview.js newParallelSession patch applied: var map `j.showChat(), l.clearMessages(), l.clearTodos(), T.clearQueue()`. Requires: Developer: Reload Window in VS Code + Cursor; restart IDEA.` as `<h2><span class="vditor-ir__marker--heading">## </span>History</h2>`, so the naive `h.textContent` is `"## History"` and would slugify to `"-history"` (the `#` chars are stripped, replacing leading whitespace with `-`), which never matches the `#history` fragment. With marker spans excluded, the visible text is just `"History"` → slug `"history"` → match. The `slugify()` itself also strips leading `[#*\-_\s]+` as a second-line defense. On hit: `t.scrollIntoView({behavior:'smooth', block:'start'})`.
- **Scroll-to-heading listener.** `window.addEventListener('message', ...)` receives `{command:'scroll-to-heading', slug}` messages posted by the `extension.js` TreeView's `scrollTo` command handler (triggered when the user clicks a heading in the sidebar outline). Calls `__zaaackGotoAnchor(slug)` to scroll the webview. The slug is generated by `_zkSlugify()` in extension.js, which uses the same pipeline as the webview's `slugify()`. Known limitation: headings with inline markdown links (e.g. `## Heading with [link](url)`) may not match — the extension includes the URL in the slug while the webview's `headingText()` skips vditor marker spans containing the URL.
- **Find-in-page (⌘F).** Capturing `keydown` on `document` matches `(metaKey||ctrlKey) && key==='f'/'F'`. Opens a fixed-position overlay (`#__zk-bar`) at top-right. Search algorithm:
  - Build a `TreeWalker` over `#app` `SHOW_TEXT`. Reject nodes inside `#__zk-bar` (own UI), `vditor-toolbar`, `vditor-outline`, `vditor-hint`, `vditor-panel` so toolbar tooltips and the find overlay itself don't pollute results.
  - For each accepted text node, run `new RegExp(escapedQuery, 'gi')` and replace matches in-place by splitting the node into a `DocumentFragment` of plain text + `<span class="__zk-hit">match</span>`.
  - Track all hit spans in a `hits[]` array. Current hit gets `background:#ff9800`, others `background:#ffd54f`, both `color:#000`. `scrollIntoView({behavior:'smooth', block:'center'})` on selection.
  - Clearing replaces every span back with a text node, then calls `parent.normalize()` on every parent that lost a span — **critical**: without normalization, sibling text nodes left behind by `replaceChild` stay fragmented across span boundaries, so the next regex run can't find matches that span the boundary (e.g. typing "p" then "i": "Hello pillow" becomes `["Hello ","p","illow"]` after clearing the first hit, and `re.exec("p")`/`re.exec("illow")` separately never match `"pi"`). Bug symptom: 1-char queries highlight, 2+ char queries return 0/0. Fix: track unique parents in a `Set`, run `.normalize()` on each, then re-query.
  - Bindings: `⌘F` open, type to live-search (120 ms debounce), `Enter` / `Shift+Enter` next/prev, `Esc` close. Buttons in the bar do the same.
  - Styling uses VS Code CSS vars (`--vscode-editorWidget-background`, `--vscode-input-foreground`, `--vscode-widget-border`, etc.) so the bar matches the active theme.
- **Idempotency guard:** sets `ed.__zaaackEnhanced = true` on the `#app` element so re-firing of `after()` (theme switch triggers a full vditor re-init via `extension.js`'s `onDidChangeActiveColorTheme`, which destroys+recreates vditor — the new `#app` is a fresh element so the guard doesn't block legitimate re-attaches).

**CSP note.** The webview HTML in `extension.js`'s `_getHtmlForWebview()` sets no `Content-Security-Policy` meta tag, so inline scripts in `main.js` execute freely. If a future Zaaack version adds CSP, the enhancer needs to move to a separate file registered via `webview.asWebviewUri()`.

**Vditor localization.** The legacy CDN intercept suppresses localization loading and supplies an empty dictionary. This breaks toolbar and submenu labels; Vditor does not supply an English fallback. The [source build](#zaaack-source-build) bundles the dictionaries instead.

**Reapply procedure** (after Zaaack extension update, OS migration, or fresh checkout):

1. Confirm installed version(s): `ls ~/.vscode/extensions/ ~/.cursor/extensions/ 2>/dev/null | grep zaaack`. The script auto-globs every matching dir under both IDEs.
2. `python3 ~/src/tools/patches/patch-zaaack.py` — for each target dir: applies multi-file editor patch to `extension.js` (step MP1–MP5), then patches `main.js` (3 sites), `main.css` (1 site), `extension.js` outline (6 sites), and `package.json` (2 sites). Re-running strips + re-injects where applicable (marker-based idempotency) and creates `.bak.<unix-ts>` backups of all files before patching.
   - If a new Zaaack version ships a new vditor version, add a new tuple to `P2_VARIANTS` and update `MULTIPANEL_SINGLETON_OLD` if TypeScript recompilation changed the `_a` var references.
3. Sanity check:

- `node -c ~/.vscode/extensions/zaaack.markdown-editor-*/media/dist/main.js` and `node -c ~/.vscode/extensions/zaaack.markdown-editor-*/out/extension.js` should print no errors.
- `rg -n "__zaaackCssPatch__" ~/.vscode/extensions/zaaack.markdown-editor-*/media/dist/main.css ~/.cursor/extensions/zaaack.markdown-editor-*/media/dist/main.css` should find the marker.

4. Reload VS Code / Cursor window (`Developer: Reload Window`) for each affected window.
5. Open a markdown file with `^⌥⌘M` and verify: "Markdown Outline" tree view appears in the Explorer sidebar showing heading hierarchy, clicking a heading scrolls the webview, dark-theme table rows are no longer white, `[link](#some-heading)` jumps in-place (no new tab opens), and `⌘F` opens the find bar with multi-char search working. When switching to a non-Zaaack editor, the Markdown Outline view hides and the standard Outline view reappears.

**Multi-file editor patch baked in.** `patch_extension_js_multipanel()` runs automatically before the outline patches, converting the singleton `EditorPanel.currentPanel` to a per-file `EditorPanel.panelsByPath` Map. Idempotent: re-running is safe. The outline patches depend on `panelsByPath` and are skipped if it is absent.

**Recreating the patch from scratch** (if `~/src/tools/patches/patch-zaaack.py` is ever lost): use the main.js anchor strings + enhancer/TreeView responsibilities described above, add one marker-guarded CSS block in `main.css` for dark tables/outline width, and add the `extension.js` + `package.json` TreeView patches. All patch sites use anchor checks plus marker-comment idempotency.

**Fallbacks if the patch ever breaks:**

1. **Switch to source markdown view**: `^⌥⌘M` toggles back to the plain markdown source editor where `⌘F` works natively.
2. **Use Markdown Preview Enhanced**: `⇧⌘V` opens a preview tab whose webview supports browser search.
3. **Restore from backup**: every run leaves `<file>.bak.<unix-ts>` next to each patched file.

**Cursor parity status:**

- Applied matching Cursor user settings in `~/Library/Application Support/Cursor/User/settings.json`:
  - `workbench.editor.enablePreview=false`
  - `workbench.editor.enablePreviewFromQuickOpen=false`
  - `markdown-preview-enhanced.previewMode="Multiple Previews"`
  - `markdown-preview-enhanced.previewColorScheme="systemColorScheme"`
  - `markdown.preview.fontSize=11`, `markdown.preview.lineHeight=1.2`
  - `typedown.editor.fontFamily` / `typedown.editor.fontSize`
  - `markdown-editor.customCss` override for proportional Zaaack editing font
- Applied matching Cursor keybindings in `~/Library/Application Support/Cursor/User/keybindings.json`:
  - `⇧⌘V -> workbench.action.markdown.openPreview` (built-in; preference over MPE in Cursor)
  - typedown / zaaack WYSIWYG shortcut swap parity with VS Code
- `patch-zaaack.py` globs both `~/.vscode/extensions/` and `~/.cursor/extensions/` so a single run patches `main.js`, `extension.js`, and `package.json` in both IDEs.

### Dark Theme + Font Patches

Zaaack WYSIWYG markdown editor (zaaack.markdown-editor) has broken dark theme support: hardcoded light-theme colors for tables, text, borders, and no live theme tracking. Patches to the extension files:

- CSS in `media/dist/main.css`:
  - Extended `body[data-use-vscode-theme-color="1"] .vditor` block to also override `--textarea-text-color`, `--toolbar-icon-color`, and `--border-color` using VSCode CSS variables (`--vscode-editor-foreground`, `--vscode-panel-border`)
  - Added `body[data-use-vscode-theme-color="1"] .vditor-reset` color override using `var(--vscode-editor-foreground)`
  - Added `.vditor--dark .vditor-reset` overrides for: text color, table `tr`/`td`/`th` backgrounds and borders, `hr`, `blockquote`, `kbd`, `.vditor-panel::after` — all the hardcoded light-theme colors that the original `.vditor--dark` CSS variables didn't reach
  - Changed `font-family` on `.vditor .vditor-reset` from `var(--vscode-editor-font-family)` (monospace) to the system sans-serif stack (`-apple-system, BlinkMacSystemFont, 'Segoe WPC', 'Segoe UI', system-ui, ...`) to match the built-in Markdown preview font
  - Set `font-size` on `.vditor .vditor-reset` to `13px` to match `markdown.preview.fontSize` (Cursor: use `12px`)
- Theme change listener in `out/extension.js`:
  - Added `vscode.window.onDidChangeActiveColorTheme` listener that re-sends `type: 'init'` to the webview with the new theme, so the editor re-initializes with correct dark/light mode when VSCode theme changes
  - Fixed initial theme detection to treat `HighContrast` as dark (was only checking `Dark`)
- Patches apply to `~/.vscode/extensions/` under `zaaack.markdown-editor-<version>/`. Patches are overwritten on extension update — reapply after each update. Reload the window (Developer: Reload Window) after patching.

If rendered markdown in Zaaack still appears oversized after settings changes, patch `~/.vscode/extensions/zaaack.markdown-editor-0.1.13/out/extension.js` theme overrides from `font-size: 13px;` to `font-size: 11px !important;` and add matching `11px !important` for `.vditor-ir pre.vditor-reset` and `.vditor-sv`.

---

## VS Code / Cursor: TypeDown

### TypeDown Patches

TypeDown WYSIWYG markdown editor (tarikkavaz.typedown-markdown-editor) has no settings for line-height, table padding, or list spacing. Patches to the extension files:

- CSS in `dist/extension.js`:
  - `.ProseMirror` `line-height`: changed from `1.7` to `1.4`
  - `.ProseMirror table td, .ProseMirror table th` `padding`: changed from `6px 10px` to `2px 10px`
  - Added `.ProseMirror table td p, .ProseMirror table th p { margin: 0; }` — ProseMirror wraps cell content in `<p>` tags with browser-default `1em` margins, which is the main source of tall rows
  - Added `.ProseMirror ul, .ProseMirror ol { margin-top: 0.25em; margin-bottom: 0.25em; }` and `.ProseMirror li p { margin: 0; }` — same `<p>`-in-`<li>` issue as tables
- Focus bug fix in `src/markdownEditorInitScript.js`: after a brief pause in typing, cursor/focus warped to end of document. Root cause: `onDidSaveTextDocument` sends `documentChanged` back to the webview, which calls `setEditorContent()` → `editor.commands.setContent()`, replacing the entire ProseMirror doc and destroying the selection. Fix: skip `setEditorContent()` in the `documentChanged` handler when the incoming text matches `lastMarkdown`.
- All patches apply to both `~/.vscode/extensions/` and `~/.cursor/extensions/` under `tarikkavaz.typedown-markdown-editor-<version>/`. Patches are overwritten on extension update — reapply after each update. Reload the window (Developer: Reload Window) after patching.

---

## IDEA: Shuzijun Markdown Editor

### Shuzijun source build

The editable IDEA source checkout is `~/src/idea-markdown-editor`, branch `brian/markdown-ux`, in the [BrianHoltz fork](https://github.com/BrianHoltz/markdown-editor) of the [Apache-licensed upstream plugin](https://github.com/shuzijun/markdown-editor). Keep `origin` pointed at the fork and `upstream` at Shuzijun; the fork makes these local improvements available to other machines without pushing personal changes to the upstream maintainer. Maintained source version `2.0.7-local.11` retains plugin ID `com.shuzijun.markdown-editor` and builds against the installed IDEA 2026.2.3 runtime instead of downloading another IntelliJ distribution.

The VS Code improvements map to IDEA as follows:

- Shuzijun already has JCEF browser find through `CefBrowser.find()`, IntelliJ Structure View through `getStructureViewBuilder()`, Vditor outline, one `FileEditor` instance per Markdown file, and locally bundled Vditor translations. The VS Code search overlay, Explorer TreeView, multipanel registry, and locale bundler are unnecessary.
- `src/main/resources/template/default.html` and `vditor/style.css` supply a single-row adaptive toolbar with a keyboard-accessible `»` overflow tray, viewport-clamped tooltips for narrow panes, a persistent upper-right distraction-free toggle, and a raw-HTML visibility toggle. The visibility toggle lives inside the Vditor root so it inherits light/dark icon colors, with full opacity in both modes. The leftmost floppy-disk button saves on click; its icon is dim when saved, full opacity when unsaved or saving, and red when saving fails. Hidden-toolbar mode also removes rich-editor margin annotations and hides raw HTML markup without changing the Markdown source.
- Plain clicks use Vditor's link handling; Option-click positions the caret for editing. Same-document fragments resolve duplicate and Unicode heading slugs plus named HTML anchors, including anchors whose raw markup is hidden. Relative Markdown links with fragments open the target IDEA editor and queue navigation until its JCEF page finishes loading.
- `MarkdownHtmlPanel` persists the two appearance preferences in IntelliJ `PropertiesComponent`, so they apply across Markdown files and IDE restarts.
- IDE appearance synchronization is source-integrated: theme changes wait for Vditor initialization, replace or create the generated stylesheet safely, and reapply Vditor's light or dark content theme.
- `META-INF/plugin.xml` declares `com.intellij.modules.jcef` as a required dependency, replacing the installed-JAR compatibility patch.
- `build.gradle.kts` accepts `-PlocalIdePath=...`, avoiding the slow platform download, and reuses the base `2.0.7` changelog entry for local version metadata.
- Bundled JavaScript, CSS, locales, icons, and Lute use a startup-specific resource URL prefix, preventing cached assets from another plugin installation from mixing with the active bundle. Browser console warnings and errors are forwarded to `idea.log`.
- Rich text projects the built-in Markdown preview's bundled prose, heading, bold, and code typography into Vditor selectors. The editor uses the raw shared Preview font-size preference and passes IDEA’s current linear UI scale to `JBCefBrowserBase.setZoomLevel`, avoiding confusion with CEF’s logarithmic zoom. The preview supplies the 1.6 prose line height, heading size ratios and weights, and relative code sizes. Source mode retains IDEA's editor font. Open tabs refresh on preview-size and UI-settings changes. Tables inherit the rich-text font, occupy the available content width, and wrap cells, including long unbroken URLs. Symmetric 35px rich-editor padding prevents Vditor's centered-column padding from wasting pane width; distraction-free mode uses 12px.
- The custom stylesheet explicitly maps rendered text, tables, borders, rules, blockquotes, keyboard tags, and the panel overflow marker to Vditor theme variables. This prevents the bundled light content-theme stylesheet from restoring white table cells and black text after IDEA switches to Darcula or another dark scheme.

The target shared Markdown Preview font-size preference is 14px; change it through Settings while IDEA is running. Typography comes from the bundled preview stylesheet; custom preview CSS is independent of the editor.

`node --test test/asset-compatibility.test.cjs` checks Lute's Vditor initialization API, cache-isolated template references, typography/table CSS invariants, and theme-variable overrides. A jsdom smoke test verifies startup and computed typography and cell-wrapping styles for synthetic nine-column tables in IR and WYSIWYG modes. It does not measure browser layout geometry or establish interactive feature parity in installed JCEF.

Build and preserve the installable ZIP:

```sh
cd ~/src/idea-markdown-editor
export JAVA_HOME="$HOME/Applications/IntelliJ IDEA 2026.2.3.app/Contents/jbr/Contents/Home"
./gradlew --no-daemon \
  -PlocalIdePath="$HOME/Applications/IntelliJ IDEA 2026.2.3.app" \
  clean buildPlugin
STAMP=$(date "+%Y%m%d.%a.%H%M")
OUT="$HOME/Downloads/markdown-editor-2.0.7-local.11-$STAMP-zoom.zip"
cp -p build/distributions/markdown-editor-2.0.7-local.11.zip "$OUT"
cmp build/distributions/markdown-editor-2.0.7-local.11.zip "$OUT"
```

Install the Downloads copy with **Settings → Plugins → gear → Install Plugin from Disk**, then restart IDEA. The source build replaces the Marketplace plugin because it retains the same plugin ID.

### Legacy installed-JAR patch

`~/src/tools/patches/patch-shuzijun.py` remains a rollback tool for Marketplace 2.0.7. It patches `template/default.html` in the installed JAR to synchronize Vditor with IDEA appearance changes. Do not apply it to the local source build; maintain changes in `~/src/idea-markdown-editor` and rebuild.

---

## IDEA: MCP Server Plugin

### Suppress Services Panel Auto-pop

**MCP Server plugin — suppress Services panel auto-pop** — The bundled `com.intellij.mcpServer` plugin registers a `serviceViewContributor` that causes IDEA's Services tool window to auto-focus every time a Wibey/Claude session connects (SSE). The `serviceViewContributor` is a **display-only widget** — it has no connection to the actual MCP server (`McpServerService`), SSE endpoint, or tool calls. Removing it is purely cosmetic: Wibey/Claude MCP integration continues working exactly as before. To suppress the pop-up, comment out the line in `META-INF/plugin.xml` inside `mcpserver.jar`:

```sh
# Backup and patch (2026.2 user-plugin copy takes precedence over bundled):
JAR=~/Library/Application\ Support/JetBrains/IntelliJIdea2026.2/plugins/mcpserver/lib/mcpserver.jar
cp "$JAR" "${JAR}.bak.$(date +%s)"
mkdir /tmp/mcpserver_patch && cd /tmp/mcpserver_patch
jar xf "$JAR" META-INF/plugin.xml
# Comment out this line in META-INF/plugin.xml:
#   <serviceViewContributor implementation="com.intellij.mcpserver.services.McpServiceViewContributor" />
# Marker: __mcpNoServicesPanel__  (for idempotency checks)
jar uf "$JAR" META-INF/plugin.xml
rm -rf /tmp/mcpserver_patch
```

Applied to 2026.2 on 2026.06.30. Reapply after any MCP Server plugin update (it is a bundled plugin that auto-updates with IDEA). Restart IDEA after patching. The Services panel still exists but won't auto-open; you can open it manually via View → Tool Windows → Services if needed.

---

## IDEA: Wibey Extension

### New Conversation Bug Fix (v1.0.10 and v1.0.16+)

**Bug:** Clicking "+" (new conversation button) shows the old/most-recent conversation instead of opening a blank chat.

**Root cause:** The `newParallelSession` webview handler — which replaced the old `newSession` flow in the parallel-session (MSM) architecture — does not call `clearMessages()`. So the previous conversation stays visible while the async `createParallelSession` round-trip runs. When that round-trip fails (e.g. `MultiSessionManager` not yet injected, or `buildSessionServices()` throws), `parallelSessionSwitched` never arrives and the old conversation is shown permanently.

**Files patched:**

1. `~/.vscode/extensions/wibey.wibey-vscode-extension-1.0.10/out/webview/webview.js` (minified) — add `clearMessages` to `newParallelSession` handler:

```python
# Run from shell:
python3 - <<'EOF'
path = '$HOME/.vscode/extensions/wibey.wibey-vscode-extension-1.0.10/out/webview/webview.js'
import os; path = os.path.expandvars(path)
c = open(path).read()
old = 'case"newParallelSession":c.showChat();{const e=bi.getState();'
new = 'case"newParallelSession":c.showChat(),o.clearMessages(),o.clearTodos(),h.clearQueue();{const e=bi.getState();'
assert c.count(old) == 1
open(path, 'w').write(c.replace(old, new, 1))
print("webview.js patched")
EOF
```

2. `~/.vscode/extensions/wibey.wibey-vscode-extension-1.0.10/out/handlers/MultiSessionHandler.js` (readable) — two changes:

**a.** In `handle()`, replace the silent return when MSM is null:

```js
// BEFORE (lines 46-49):
if (!this.multiSessionManager) {
    logger_js_1.logger.warn('[MultiSessionHandler] MultiSessionManager not initialized');
    return;
}

// AFTER:
if (!this.multiSessionManager) {
    logger_js_1.logger.warn('[MultiSessionHandler] MultiSessionManager not initialized');
    if (message.type === 'createParallelSession') {
        // Fall back to legacy new-session flow so the webview always lands on a blank chat.
        this.context.webviewController.postMessage({ type: 'newSession' });
    }
    return;
}
```

**b.** In `handleCreateSession()` catch, replace the non-limit `streamError` path:

```js
// BEFORE:
else {
    this.context.webviewController.postMessage({
        type: 'streamError',
        error: `Failed to create new session: ${errorMessage}`,
    });
}

// AFTER:
else {
    // Session creation failed — fall back to legacy new-session flow so the
    // webview shows a blank chat rather than staying on the old conversation.
    logger_js_1.logger.warn('[MultiSessionHandler] Falling back to legacy new-session after createSession failure');
    this.context.webviewController.postMessage({ type: 'newSession' });
}
```

After patching, run `Developer: Reload Window` in VS Code. Patches are overwritten on Wibey extension update — reapply after each update (adapt paths for new version).

**v1.0.16 patch** — `MultiSessionHandler.js` no longer exists (architecture changed). Only `webview.js` needs patching. Variable names changed (`c`→`C`, `bi`→`te`, `o`→`l`, `h`→`L`):

```python
python3 - <<'EOF'
import os, shutil, time
path = os.path.expanduser('~/.vscode/extensions/wibey.wibey-vscode-extension-1.0.16/out/webview/webview.js')
src = open(path).read()
old = 'case"newParallelSession":C.showChat();'
new = 'case"newParallelSession":C.showChat(),l.clearMessages(),l.clearTodos(),L.clearQueue();'
assert src.count(old) == 1
shutil.copy2(path, f'{path}.bak.{int(time.time())}')
open(path, 'w').write(src.replace(old, new, 1))
print("webview.js patched")
EOF
```

**v1.0.31 patch (2026.10.09)** — upstream `useMessageHandler.ts` `newParallelSession` still lacks the clear calls. Variable map (from `case"newSession"`): `y.showChat()`, `c.clearMessages()`, `c.clearTodos()`, `B.clearQueue()`:

```python
old = 'case"newParallelSession":y.showChat();'
new = 'case"newParallelSession":y.showChat(),c.clearMessages(),c.clearTodos(),B.clearQueue();'
```

If variable names change again in a future version, search for `case"newParallelSession"` and `case"cleared"` (which shows the correct `clearMessages`/`clearTodos`/`clearQueue` variable names) to find the right substitution.

---

## Wibey Skills: usage-dashboard

### UTC Day-boundary Bug

The `usage-dashboard` skill buckets sessions by UTC date, not local time. Sessions after ~7 PM CDT (midnight UTC) are credited to tomorrow's bar in the chart.

**Root cause** — two places in the installed scripts:

- `~/.wibey/usage/wibey_usage_lib.py`: `msg_date = ts[:10]` slices the first 10 chars of a UTC `Z` timestamp without converting to local time first.
- `~/.wibey/usage/wibey-usage`: `DATE(s.ended_at)` in the SQL GROUP BY, plus the `--days` cutoff uses `datetime.now(timezone.utc)`.

**Fix** — in both the installed files AND the skill source (`~/.wibey/skills/usage-dashboard/scripts/`):

In `wibey_usage_lib.py`, replace the raw slice with a local-time conversion:

```python
# Before (UTC):
msg_date = ts[:10] if ts and len(ts) >= 10 else None

# After (local):
from datetime import timezone
import datetime as _dt
def _utc_ts_to_local_date(ts):
    if not ts or len(ts) < 10:
        return None
    try:
        dt = _dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone().strftime("%Y-%m-%d")
    except Exception:
        return ts[:10]
msg_date = _utc_ts_to_local_date(ts)
```

In `wibey-usage`, replace the SQL `DATE(s.ended_at)` fallback with a local-time equivalent. SQLite has no built-in local-time function; easiest fix is to store the local date in the DB at record time (fix the lib above) so the fallback is rarely hit, and additionally change the `--days` cutoff:

```python
# Before:
cutoff = (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()

# After:
cutoff = (datetime.now().astimezone() - timedelta(days=args.days)).isoformat()
```

Patches needed in two locations each time the skill is reinstalled:

- `~/.wibey/skills/usage-dashboard/scripts/wibey_usage_lib.py` (canonical)
- `~/.wibey/skills/usage-dashboard/scripts/wibey-usage` (canonical)
- `~/.wibey/usage/wibey_usage_lib.py` (installed copy)
- `~/.wibey/usage/wibey-usage` (installed copy)

After patching, existing DB rows with UTC `usage_date` values won't be retroactively corrected — they'll remain on the UTC-bucketed dates.

---

## History

History of tool use practices and modifications.

- 2026.03.26 Thu: Opus gets stuck in IDEA last few days, switching to Sonnet
- 2026.05.09 Sat: Fixed the last three Zaaack gaps — Cmd+F find-in-page, outline view, and intra-doc anchor link nav — via `~/bin/patches/patch-zaaack.py` (4 idempotent patch sites in `media/dist/main.js`). Zaaack jumped from `🟡` to `✅✅` parity with IDEA's md preview, and (since the patch globs both `~/.vscode/extensions/` and `~/.cursor/extensions/`) Cursor now matches VS Code on markdown editing too. Upstream is MIT (`github.com/zaaack/vscode-markdown-editor`) but with low maintainer activity (108 open issues, 5+ stale PRs); the anchor-link-opens-directory bug appears unreported, so worth filing one issue. Find-in-page (#153) and outline (#24, #155) are already requested upstream. Added draggable resize handle between outline and editor: 5px `#__zk-outline-resize` div injected after `.vditor-outline` in the flex row; highlights on hover/drag; clamps 60–800px.
- 2026.05.11 Mon: Moved Zaaack outline from vditor's built-in webview panel to a VS Code sidebar TreeView (`markdownEditorOutline`). The vditor outline consumed horizontal editor space and couldn't integrate with VS Code's sidebar; now the outline appears in the Explorer sidebar only when a Zaaack editor is focused, showing a hierarchical heading tree with click-to-scroll. Patch script expanded from 1 file (`main.js`) to 3 (`main.js`, `extension.js`, `package.json`). Fixed a strip-and-re-inject bug: old enhancer strip logic used `src.find('})();')` which matched the `injectCssFixes` IIFE inside the enhancer instead of the file's IIFE close; fixed by adding `/*__zaaackEnhance_end__*/` bracket marker. Removed the draggable outline resizer (no longer needed — sidebar resize is built into VS Code).
- 2026.05.12 Tue: Updated `~/bin/patches/patch-zaaack.py` CSS patch to force link colors to VS Code Markdown Preview theme tokens (`--vscode-textLink-foreground` and `--vscode-textLink-activeForeground`) for both anchor tags and vditor IR link spans (`.vditor-ir__link`). Re-ran patch script across both extension roots (`~/.vscode/extensions/zaaack.markdown-editor-*` and `~/.cursor/extensions/zaaack.markdown-editor-*`).
- 2026.05.18 Sun: Investigated "intra-doc links and outline click-to-scroll not working." Verified all three patch files (`main.js`, `extension.js`, `package.json`) are correctly applied in both VS Code and Cursor; JS syntax valid; all anchors present. Root cause: stale webview running pre-patch `main.js`. The `?v=${Date.now()}` cache-buster (E7) ensures fresh `main.js` load, but only takes effect after a window reload triggers the updated `extension.js`. Fix: **`Developer: Reload Window`** in each IDE. Re-ran `patch-zaaack.py` to freshen the patch timestamp; confirmed idempotent. No patch logic changes needed.
- 2026.06.15 Sun: VS Code upgraded, Zaaack updated to 0.1.15 (vditor 3.8.4 → 3.11.2). Updated `patch-zaaack.py`: (1) replaced single `P2_OLD`/`P2_NEW` with `P2_VARIANTS` list to support multiple vditor versions without per-version edits; (2) baked multi-file editor patch (`currentPanel` → `panelsByPath` Map) into `patch_extension_js_multipanel()` so it's no longer a manual prerequisite; (3) added `PKG_AE_CANDIDATES` for package.json activationEvents (0.1.15 added a 4th activation event, breaking the old anchor). Applied Wibey 1.0.16 webview.js `newParallelSession` patch (variable names changed from 1.0.10: `c`→`C`, `o`→`l`, `h`→`L`; `MultiSessionHandler.js` gone). Cosmetic: vditor 3.11.2 i18n 404 on CDN is benign — noted in doc, not fixed.
- 2026.06.30 Mon: IDEA Services panel auto-popped on every Wibey/Claude session connect. Root cause: `com.intellij.mcpServer` plugin registers a `serviceViewContributor` (`McpServiceViewContributor`) that causes IDEA's Services tool window to auto-activate on each new SSE connection. Fix: commented out the `<serviceViewContributor>` line in `META-INF/plugin.xml` inside `mcpserver.jar` (user-plugin copy in IntelliJIdea2026.2/plugins/). Restart IDEA to take effect.
- 2026.06.30 Mon: Shuzijun WYSIWYG editor tab disappeared in IDEA. Root cause: IDEA auto-updated from 2025.3.3 to 2026.2 EAP (build 262.8377.35) on ~2026.06.27. In 2026.2, `com.intellij.ui.jcef.JBCefApp` was moved from core to `com.intellij.modules.jcef` plugin module; Shuzijun 2.0.5 has no dependency on that module, causing `NoClassDefFoundError` in `MarkdownPreviewFileEditorProvider.accept()` on every markdown open. IDEA suppresses the error and omits the tab. Fix: added `<depends>com.intellij.modules.jcef</depends>` to `META-INF/plugin.xml` inside `markdown-editor-2.0.5.jar` (2026.2 copy only). Restart IDEA to pick up the change.
- 2026.07.02 Wed: Both built-in Markdown preview and Shuzijun WYSIWYG tab broken in IDEA simultaneously. Root cause: IDEA 2026.2 defaults `ide.browser.jcef.out-of-process.enabled` registry key to true, causing `JBCefApp.init()` to call `System.setProperty("jcef.remote.enabled", "true")` at startup. `cef_server.app` exists in the jcef-plugin so `isRemoteSupported()=true`; combined with the property → JCEF runs in remote/OSR mode. `createMessageRouter()` NPEs (native CEF objects null in remote mode), built-in preview pipe never gets `documentReady`. Fix: add `-Djcef.remote.enabled=false` to `~/Library/Application Support/JetBrains/IntelliJIdea2026.2/idea.vmoptions`; `JBCefApp.init()` sees the property already set and skips its override. Restart IDEA.
- 2026.06.17 Tue: Zaaack stopped working ~2026.06.01 (exact cause TBD); VS Code and Cursor fall back to typedown (3.5 pts) as best available editor. Editor subtotals drop from 7 → 3.5 for both.
- 2026.06.18 Wed: Switched primary IDE from VS Code to IDEA. Added "IDEA editor" column to markdown table (native WYSIWYG, replaces shuzijun column). Native editor scores 8.0 pts (vs shuzijun 3.5), lifting IDEA total from 21.5 → 28.5. Parallel agents now ✅ in IDEA (was ❌); "type @ busy Wibey" renamed to "enqueue next prompt" and inverted — VS Code/Cursor now ✅, IDEA ❌. Score recalc: IDEA 28.5, VS Code 20.5, Cursor 19.5.
- 2026.08.06 Thu: Reinstalled all IDEA mods on request. Wibey JetBrains plugin had silently auto-updated to stock `1.0.24.jar` (no custom fields — title-bar rename patch gone, though upstream now ships its own native clipboard-paste). First pass rebuilt `~/src/wibey-jetbrains-plugin` branch `brian/local-combined` as-is (still based on upstream 1.0.23) via `./gradlew clean buildAndInstall`, confirming our patches restore correctly. Then, per follow-up request, merged `origin/main` into `brian/local-combined` (38 commits, including the 1.0.24 bump, bridge-daemon rewrite, and workspace-path fixes) — clean merge, no conflicts, our patched files (`NativeChatToolWindowPanel.kt`, `InputAttachmentManager.kt`) merged without collision. Rebuilt + reinstalled again; `javap` confirmed the installed JAR is genuinely `1.0.24` **and** still has `sessionTitleLabel`/`sessionRenameTrigger`/`sessionTitleBar`/`startSessionRenameInline` (title rename) and `setupClipboardPaste`/`handleImagePaste` (image paste) compiled in. Re-verified the other four mods untouched throughout: JCEF remote disabled, readonly-fragments-notification, Shuzijun `com.intellij.modules.jcef` depends + 13px font, MCP Server `serviceViewContributor` suppression — all still present. Merge commit made locally on `brian/local-combined`; not pushed. Restart IDEA required.
- 2026.07.17 Thu: IDEA 2026.2 EAP shipped as GA/stable (build 262.8665.258, released 2026.07.16) on the Walmart laptop. Config dir `IntelliJIdea2026.2` carried over intact from EAP → GA, so all EAP-era patches survived the upgrade. Full audit (Code Puppy) of the running GA build confirmed present: JCEF remote disabled (`-Djcef.remote.enabled=false` in `idea.vmoptions`), Shuzijun `com.intellij.modules.jcef` depends + 13px font (`markdown-editor-2.0.5.jar`), MCP Server `serviceViewContributor` suppression (`mcpserver.jar`, `__mcpNoServicesPanel__` marker), keymap overrides (`macOS copy.xml`: zoom/GotoFile/line-numbers), and the patched Wibey plugin `1.0.23.jar` from `brian/local-combined` — verified via `javap` that `InputAttachmentManager.setupClipboardPaste()`/`handleImagePaste(Clipboard)` (image paste) and `NativeChatToolWindowPanel.sessionTitleLabel`/`sessionTitleBar`/`startSessionRenameInline` (title features) are all compiled in. Source repo on `brian/local-combined`, up to date with origin/main (nothing to merge). **One gap, now closed:** `idea.readonly.fragments.notification.enabled=false` was missing from `early-access-registry.txt` after the EAP→GA carry-over. Reapplied 2026.07.17 via the file method after quitting IDEA (appended key+value, `.bak` created). Restart IDEA to take effect. Updated Tools.md: IDE version cells `2026.2 EAP` → `2026.2`, IDEA status bullet, Markdown Preview section headers.
- 2026.10.09 Fri: VS Code mods refreshed. Wibey 1.0.31 (marketplace auto-update) had lost the `newParallelSession` clear patch — reapplied to `webview.js` (backup `.bak.<ts>`, `node --check` ok); reload window. Code Puppy: merged `origin/main` (native CLI update tray, 1 commit) into `feature/active-context-pill` (clean, local merge commit 7fb72c1, not pushed), built `releases/code-puppy-vscode-0.28.0.vsix` (update tray + active-context pill both confirmed in dist), staged `~/Downloads/code-puppy-vscode-0.28.0-20261009.Fri.1119-updtray.vsix`, installed in VS Code (0.27.0 → 0.28.0). Cursor Code Puppy left at 0.27.0.

*[doc-audit](https://github.com/BrianHoltz/tools/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.10.11.Sun*
