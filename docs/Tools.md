# AI/IDE Toolchain

## Local Modifications in Use

- **Code Puppy JetBrains + VS Code + Cursor** — Walmart-internal technology, maintained and built on the Walmart work laptop only; its absence from a personal laptop and its Downloads folder is expected. On the work laptop, VS Code has the local 0.28.2 build from [brian/vscode-0.28.2-local](https://gecgithub01.walmart.com/r0b0m29/code-puppy-ide/tree/brian/vscode-0.28.2-local), installed 2026.10.12; JetBrains 0.28.1 has maintained callback/navigation and live-zoom fixes; the installed JAR matches the maintained zoom artifact byte-for-byte (work laptop audit 2026.10.13). Cursor remains 0.27.0. See [source modifications](ToolMods.md#code-puppy-maintained-source-builds). The isolated VS Code branch merges upstream 0.28.2 with `feature/active-context-pill`, preserving active-file/selection suggestions and distinct selection identities. Its timestamped Downloads VSIX is `code-puppy-vscode-0.28.2-20261012.Mon.1210-context.vsix`; the canonical artifact is in `~/src/code-puppy-ide/releases/`. Typechecks, ESLint, and all 1,719 TypeScript unit tests pass; the bridge suite passes 350 tests with one skipped. On Node 25, run webview tests with `NODE_OPTIONS=--no-experimental-webstorage` so jsdom owns localStorage. Interactive extension-host and browser E2E checks are separate from these validations. JetBrains-only JDK/JCEF patches do not apply to VS Code.
- **Wibey JetBrains 1.0.28** — Walmart-internal technology, maintained and built on the Walmart work laptop only; its absence from a personal laptop and its Downloads folder is expected. Upstream GPT model support and context-window work are combined locally with persistent editable conversation titles, editable queued follow-up prompts, image paste, focused-editor file/selection context, prompt queuing, and quota snapshots.
- **Zaaack Markdown Editor for VS Code and Cursor** — adds multipanel editing, outline navigation, find, anchor links, and dark-theme/readability improvements. The current VS Code package is `0.1.22-local.6`, built from the latest source with the bundled Vditor runtime; its Downloads installer is `markdown-editor-0.1.22-local.6-20261012.Mon.2129-bundled.vsix`.
- **TypeDown for VS Code and Cursor** — compacts prose, table, and list spacing; preserves editor focus and cursor position through paste.
- **Shuzijun Markdown Editor for IntelliJ IDEA** — local source build adds an adaptive toolbar, narrow-pane tooltips, distraction-free and raw-HTML visibility controls, persistent appearance preferences, anchor navigation, IDE theme synchronization, dark-theme content overrides, and the JCEF dependency required by IDEA 2026.2. The `2.0.7-local.11` package derives prose, heading, bold, and code typography from the bundled preview stylesheet, follows the shared font-size preference and preview display normalization, prevents bundled light-theme table/text rules from overriding dark mode, and keeps the toolbar visibility toggle inside the editor theme scope at full opacity. A leftmost floppy-disk button always force-saves on click — even if the buffer looks unchanged — and dims only when the buffer is saved; failed saves show red. A reload button sits immediately to its right (refresh-arrow icon); it re-fetches the file from disk, arming on a dirty buffer and requiring a second click within three seconds to discard unsaved changes. Its Downloads installer is `markdown-editor-2.0.7-local.11-20261013.Tue.1511-reload.zip`, built against `/Applications/IntelliJ IDEA.app` (2026.2.3) and installed over the running plugin's jar with a `.bak.<unix-ts>` rollback copy alongside it; this single pending restart picks up both the force-save/reload change and the still-unapplied zoom fix from the prior `…1004-zoom.zip` build. See [source modifications](ToolMods.md#shuzijun-source-build).
- **IntelliJ IDEA MCP Server plugin** — prevents MCP connections from stealing focus to the Services tool window.

### Local Build Artifact Rule

This is the canonical personal policy for local IDE/plugin artifacts.

Every locally built IDE/plugin artifact must be copied to `~/Downloads/` for installation and review. Keep the canonical build output in its repository's normal release folder, but treat the Downloads copy as the human-facing local build.

Name each Downloads artifact `<product>-<version>-yyyymmdd.Dow.hhmm-<blah>.<ext>`. The timestamp is the actual build-completion time; capture it with `date "+%Y%m%d.%a.%H%M"` immediately after the build succeeds, not when copying or renaming the artifact. `<blah>` is a lowercase, hyphen-free description of the newest included fix, shorter than 10 characters. Example: `code-puppy-jetbrains-0.23.0-20260918.Fri.1146-imgpaste.zip`.

**GC: keep the newest 2 Downloads artifacts per product, trash the rest.** After staging a new artifact, `trash` (never `rm`) every older Downloads artifact for that same product beyond the 2 most recent, so Downloads never accumulates an unbounded backlog of superseded local builds; the canonical build output already lives in the repository's release folder per the paragraph above, so nothing is lost. "Same product" means the filename prefix before the version number, except the two markdown-editor forks (Zaaack VS Code, `markdown-editor-0.1.22-local.*.vsix`; Shuzijun IntelliJ, `markdown-editor-2.0.7-local.*.zip`), which share a name prefix but are different products — group by prefix *and* extension for that one case. **Rank "newest" by the embedded `yyyymmdd.hhmm` timestamp, never by sorting the bare filename or version string lexicographically** — an unpadded version or local-build counter (`0.1.10` vs `0.1.2`; `local.11` vs `local.3`) sorts wrong as plain text, since `'1' < '2'` and `'1' < '3'` as characters regardless of the full number's magnitude. Parse out the date/time field (or just compare `date -j -f` epoch values of it) and rank on that.

### Rebuilding the Local Wibey JetBrains Plugin

Wibey is Walmart-internal and is maintained/built on the Walmart work laptop only. Its absence from a personal laptop, including `~/src` and `~/Downloads`, is expected; do not clone or build it on the personal laptop.

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

For VS Code 0.28.2, build from [brian/vscode-0.28.2-local](https://gecgithub01.walmart.com/r0b0m29/code-puppy-ide/tree/brian/vscode-0.28.2-local), not the JetBrains repair checkout. Build the shared webview before packaging: `pnpm --filter @code-puppy/webview build`, then `pnpm --filter code-puppy-vscode package`. Verify the installed version with `code --list-extensions --show-versions` (or `cursor` for Cursor). Installing a stock VSIX can replace local modifications even when the version matches; reinstall the timestamped local Downloads VSIX with `--force` afterward.

## IDEs

| Feature                        | IDEA          | VS Code       | Cursor                  |
| ------------------------------ | ------------- | ------------- | ----------------------- |
| Score                          | 33.5          | 29.0 | 19.5                    |
| IDE                            | 2026.2.3      | 1.141.0       | 3.21.13                 |
| VSCode engine                  | —            | —            | 1.105.1                 |
| Wibey                          | 1.0.28       | 1.0.31       | 1.0.18                  |
| Code Puppy                    | 0.28.1       | 0.28.0       | 0.27.0                  |
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
| Github Copilot                 | 1.11.2-251   | 0.39.0       | 1.1.685                 |
| └ parallel agents              | ✅            | ✅            | ✅                       |
| └ context += selection         | ✅ auto       | ❌            | ❌                       |
| └ convo title                  | 🟡 manual    | ✅ auto       | ✅ auto                  |
| Claude Code                    | —            | 2.1.296      | —                       |
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


Score rubric

- Glyph values: ✅✅ = 2 pts, ✅ = 1 pt, 🟡 / ✔️ = 0.5 pts, ❌ / ? = 0 pts, ❌❌ = −1 pt
- Version/text-only cells (version numbers, descriptive text) = excluded
- Copilot rows excluded from IDE score
- **IDEA patches (baked-in as of 2026.09.29):** image-paste-fix + conversation-title-features are merged into local `brian/local-combined` build (Wibey 1.0.28), alongside upstream 1.0.28 updates. Scores reflect working features; ⚙️ notation removed. Recount after IDE/extension updates.
- Editor score: each IDE gets the maximum score achievable by any editor available to it
  - IDEA: native WYSIWYG editor (8.0 pts); beats viewer (7.0) and shuzijun (3.5)
  - VS Code: Zaaack local source build 9.5 pts + IDE row subtotal 19.5 pts = 29.0 pts. Ratings use Brian's reported Markdown behavior and the documented local build; external-file reread and images remain unverified. [Build details](ToolMods.md#zaaack-source-build).
  - Cursor: typedown (3.5 pts); zaaack broken ~2026.06.01 (was 7 pts w/ patch)
- Final score = IDE row subtotal + best editor subtotal

## Agent Harnesses

This flat comparison records the tested harness/IDE combinations without expanding into a multidimensional matrix. Voice ratings reflect Brian's VS Code experience (2026.10.12), not a product-wide benchmark. Claude Code findings apply only to its VS Code extension; an IntelliJ integration has not been investigated or tested by Brian. ? means the exact behavior has not been established; it does not mean unsupported.

| Feature | Wibey | Code Puppy | Copilot in VS Code | Codex in VS Code | Claude Code in VS Code | Antigravity |
| --- | --- | --- | --- | --- | --- | --- |
| Host observed | IDEA / VS Code / Cursor | IDEA / VS Code / Cursor | VS Code | VS Code | VS Code | VS Code |
| Queue next prompt | ✅ local IDEA build; VS Code/Cursor documented | ? host/build check | ? distinguish from steering | ? distinguish from steering | ? distinguish from steering | ? |
| Steer running task | ? | ? | ? | ? | ? | ? |
| Voice typing experience | ? | ? | ✅ record then transcribe | ✅ record then transcribe | ✅✅ preferred, live words | ? |
| Words visible while speaking | ? | ? | ❌ waveform during recording | ❌ waveform during recording | ✅ word by word | ? |
| Transcription after recording | ? | ? | ~2–3s reported | ~2–3s reported | Live text reported | ? |

Queuing holds a follow-up for execution after the active task; steering delivers new instructions during the active task. Brian reports some form of queuing or steering in Copilot, Codex, and Claude Code, but the separate behaviors require confirmation. The maintained Wibey IDEA build documents prompt queuing and editable queued prompts; the legacy IDE matrix's enqueue row and Top Frictions claim conflict with that build description. Code Puppy's installed-host behavior needs confirmation before assigning the local queuing patch to it.

Voice typing is a strongly weighted selection criterion for Brian. His reported preference is Claude Code's live word-by-word transcription over Copilot and Codex's recording followed by delayed transcription. Transcription accuracy is not scored separately without comparative evidence. Harness ratings are excluded from the existing IDE score; TODO: reconcile legacy harness rows and weights before using the aggregate score to choose an IDE.

## Git

### SSH push hangs on VPN → push over HTTPS instead

`~/.ssh/config` routes `github.com` through `ssh.github.com:443` specifically so SSH works when a network blocks port 22 — but Walmart's VPN (Zscaler SSLO) can still break it: the TCP connect to `ssh.github.com:443` succeeds, then the connection hangs dead at the SSH banner exchange and times out (confirmed reproducible with `ssh -v -T git@github.com`, and with the sandbox disabled, so it isn't a harness artifact). Plain HTTPS `curl` requests to `github.com` succeed over the same network at the same time — the inspection device tolerates real TLS/HTTP but not raw SSH bytes on port 443.

**Fix: push to the explicit HTTPS URL instead of the configured SSH remote**, using the OAuth token `gh` already has cached in the macOS keychain (`gh auth status` → `github.com ... Logged in ... Token: gho_...`; `git credential fill` with `protocol=https` / `host=github.com` returns it via `credential.helper = osxkeychain`, no extra setup needed):

```sh
git push https://github.com/<owner>/<repo>.git <branch>
```

This does **not** update the local `refs/remotes/origin/<branch>` tracking ref (the push went to a literal URL, not the `origin` remote), so `git status` will still show "ahead" afterward even though the push succeeded. Fix the tracking ref directly instead of re-fetching over the still-broken SSH remote:

```sh
git update-ref refs/remotes/origin/<branch> <pushed-sha>
```

If the remote has commits you don't have locally (non-fast-forward rejection), fetch over HTTPS first, merge (this repo uses merge, not rebase — see AgentRules.md § Git Merge Strategy), then push and update the tracking ref as above:

```sh
git fetch https://github.com/<owner>/<repo>.git <branch>
git merge FETCH_HEAD --no-edit
git push https://github.com/<owner>/<repo>.git <branch>
git update-ref refs/remotes/origin/<branch> <pushed-sha>
```

Leave the remote itself on SSH (`git remote -v`) — this is a one-off per-push workaround, not a permanent protocol switch; SSH keeps working fine off-VPN and on networks where the block doesn't apply.

## Markdown Viewers/ Editors

- VSCode md preview hangs for big files, but zaaack handles them
  - The local Zaaack source build includes string search, intra-document link navigation, and a separate Markdown Outline sidebar tree. [Build and maintenance](ToolMods.md#zaaack-source-build).
- typedown and zaaack work in both VS Code and Cursor

| Behavior                 | IDEA viewer | IDEA editor | typedown     | zaaack                            | Cursor native |
| ------------------------ | ----------- | ----------- | ------------ | --------------------------------- | ------------- |
| version                  | 2026.2      | 2026.2      | 1.1.7        | 0.1.22-local.6 (VSCode) / 0.1.13 (Cursor) | 2.6.19        |
| >1 tab at a time         | ✅          | ✅✅        | ✅✅         | ✅✅                              | ✅✅          |
| re-read changed file     | ?           | ?           | ✅           | ?                                 | ?             |
| wide tables              | ✅          | ✅          | ❌ truncates | ✅✅                              | ❌ truncates  |
| non-bloated side padding | ✅          | ✅          | ❌           | ✅                                | ❌            |
| shows images             | ✅          | ✅          | ?            | ?                                 | ?             |
| find in file             | ✅          | ✅          | ❌           | ✅ unified Cmd+F † | ❌            |
| structure                | ✅          | ✅          | ❌           | ✅ ⚙️                           | ❌            |
| internal links           | ✅          | ❌          | ?            | ✅ plain-click anchors † | ?             |
| link editing             | ?           | ✔️        | ❌           | ✔️                              | ❌            |
| toolbar                  | -           | ✔️        | ✔️         | ✅ single row + overflow † | ❌            |

† Zaaack ratings for unified Cmd+F, plain-click intra-document links, and the single-row adaptive toolbar with overflow are confirmed by Brian's use of the VS Code local build (2026.10.12). Wide tables retain ✅✅; independent Markdown previews are supported by the [multiple-preview configuration](#multiple-markdown-tabs-no-reuse). These confirmations do not establish parity for the Cursor installation or for unsaved-edit recovery.

### IDE Keybindings

| Action         | IDEA                     | VS Code           | Cursor            |
| -------------- | ------------------------ | ----------------- | ----------------- |
| zoom in / out  | `^⌥=` / `^⌥-` ⚠️ | `⌘=` / `⌘-` | `⌘=` / `⌘-` |
| open file      | `⇧⌘O` ⚠️           | `⌘P`           | `⌘P`           |
| search project | `⇧⌘F`                | `⇧⌘F`         | `⇧⌘F`         |
| Wibey history  | ?                        | ?                 | ?                 |
| Wibey new chat | ?                        | ?                 | ?                 |

IDEA keybinding overrides (defaults shown in table, actual bindings below):

- ⚠️ **zoom** `^⌥=` / `^⌥-` (`ZoomInIdeAction` / `ZoomOutIdeAction`) → remapped to `⌘=` / `⌘-`. Displaced `CollapseRegion` / `ExpandRegion` (fold/unfold) — unbound and unneeded.
- **open file** `⇧⌘O` (`GotoFile`) → remapped to `⌘P`. Displaced `FileChooser.TogglePathBar` from `⌘P` — unneeded.

### IDEA — Markdown typography and zoom

The [forked Markdown Editor](ToolMods.md#shuzijun-source-build) derives prose, heading, bold, and rendered-code typography from the built-in preview's bundled stylesheet and follows **Settings → Languages & Frameworks → Markdown → Preview font size**. The target shared preference is 14px; the work laptop still has 15px until changed through Settings. Source mode retains the editor's monospace font. The editor uses the raw preview font-size preference with IDEA’s current linear UI scale as JCEF zoom; preference and UI-setting changes refresh open editor tabs. This requires `2.0.7-local.11` or later. The built ZIP must be installed and IDEA restarted.

Code Puppy uses IDEA's UI label font family and scales the whole webview from the UI label font size. Its maintained JetBrains branch listens for UI-settings changes so open conversations refresh when IDEA zoom or Appearance settings change. Its 13px CSS baseline is a scaling reference, not a zoom exemption. Matching the UI and Markdown preview sizes alone does not match their font families.

### Keybindings (swapped from defaults in VS Code and Cursor)

The default keybindings collided with preference — typedown's simpler shortcut was wasted on the less-preferred editor. Swapped via `keybindings.json` in both VS Code and Cursor:

- **typedown** "Open in WYSIWYG mode": default `^ ⌥ ⌘ M` → swapped to `⌥ ⇧ ⌘ M`
- **zaaack** "Open with markdown editor": default `⌥ ⇧ ⌘ M` → swapped to `^ ⌥ ⌘ M`
- **Markdown Preview Enhanced** (`shd101wyy.markdown-preview-enhanced`): bound `⇧ ⌘ V` to `markdown-preview-enhanced.openPreview` (NOT `openPreviewToTheSide`) — MPE handles intra-doc anchor links correctly where the built-in sometimes breaks them. Using `openPreview` keeps the preview in the same editor column without splitting.

Each swap uses a `-` (unbind) entry to remove the extension default, then a positive binding with the other shortcut. typedown also has a toggle pair (`openWysiwygEditor` / `openDefaultEditor` gated on `typedown.editorIsActive`), so both commands are rebound.

Extension command IDs:

- `typedown.openWysiwygEditor` (when `!typedown.editorIsActive`) / `typedown.openDefaultEditor` (when `typedown.editorIsActive`)
- `markdown-editor.openEditor` (when `editorTextFocus && editorLangId == markdown`)

### Add the active file to Copilot Chat

In VS Code, **⌃⌥⌘⇧C** invokes **Markdown Editor: Add Active File to Copilot Chat**. It attaches the active tab's file URI through VS Code's native `workbench.action.chat.attachFile` action, including Zaaack Markdown Editor custom and webview tabs that Copilot's implicit active-editor lookup can miss. Focus the intended tab before invoking it; the file is attached to the active/last-focused VS Code Chat and is not sent automatically. Local, remote, and untitled files are supported; unsupported tabs produce an information message.

### Add the active file to Codex

In VS Code, **⌃⌥⌘C** (Control–Option–Command–C) invokes **Codex: Add Active File to Codex**. Focus the file tab, including a TypeDown or Zaaack Markdown visual editor, and press the shortcut to attach its file reference to the active Codex chat. The command opens the Codex sidebar; it does not submit a prompt. Reload the VS Code window if a newly installed extension is not active.

The local **Codex File Context** extension lives in [vscode/codex-file-context](../vscode/codex-file-context/package.json). Its [adapter](../vscode/codex-file-context/extension.js) resolves the active tab's file URI for both standard text editors and custom editors, then passes that URI explicitly to [Codex's Add File to Thread command](https://developers.openai.com/codex/ide/commands). A direct keybinding to the built-in command can miss custom editors because its implicit lookup uses the active text editor. Resolving the tab also avoids attaching a stale text editor's file. Unsaved untitled documents and tabs without a local file URI produce a message instead of an attachment. The adapter attaches a path, not a snapshot of unsaved buffer contents.

The binding is contributed by the extension, rather than added to user keybindings. Change it in Settings → Keyboard Shortcuts by searching for **Add Active File to Codex**. Extension ID: `brianholtz.codex-file-context`. On the work laptop, the helper is marked uninstalled and its `openai.chatgpt` dependency is absent (2026.10.12); the shortcut is unavailable there. Mocked text/custom-tab resolution is verified; live keystroke delivery inside the Markdown webviews requires an interactive check.

### Generalizing active-file attachment

The reusable design separates **editor lookup** from **chat attachment**: capture the focused file before moving focus to chat, then call the chosen harness's attachment command with an explicit file reference. Selection support also needs the range and, when unsaved edits matter, the selected buffer text. A keybinding, editor-toolbar button, and active-file suggestion pill can share this action. Ordering recent files in an @ menu requires changes to the harness's picker; the attachment adapter alone does not control that menu.

- **VS Code and Cursor:** the tab lookup is reusable across compatible extensions. Each target harness needs a verified command and argument format; the Codex adapter cannot attach to Wibey, Code Puppy, Copilot, or Claude merely by changing the model. Cursor also needs its own installation and a compatibility check against its VS Code engine.
- **IntelliJ IDEA:** implement the equivalent as a keymap action using the selected file editor's file, rather than requiring a text editor. The [IntelliJ editor API](https://plugins.jetbrains.com/docs/intellij/editors.html) supports file editors, including custom editors; attachment still depends on the target plugin's action or API. [Codex in JetBrains AI Assistant](https://www.jetbrains.com/help/ai-assistant/codex-agent.html#collect-ide-context) already has an IDE-context toggle that supplies the active file name and selection with each prompt. [AI Assistant chat](https://www.jetbrains.com/help/ai-assistant/chat-mode.html#use-mentions) documents @thisFile and file attachments. Neither establishes that an explicit shortcut works inside the Shuzijun visual editor; that integration needs verification.
- **Other agent harnesses:** use their exposed attachment API or add an adapter to a locally maintained integration. Choose the destination chat explicitly when multiple harnesses are open. Supplying editor context through a tool can help an agent discover a file, but it does not itself add a visible attachment to the chat composer.

The VS Code Codex shortcut is implemented. IDEA, Cursor, other-harness routing, selection attachment, and picker ordering are design options, not installed features.

## Top Frictions

- **All IDEA patches currently applied and stable** (verified 2026.09.29). Wibey 1.0.28 from `brian/local-combined` includes upstream main plus image-paste-fix and conversation-title-features. Rebuild from that branch to keep the local plugin current.
- Parallel Wibey agents now available in all three IDEs (as of 2026.06).
- Top silly frictions: let me buffer up my next prompt, and make it super-easy to reference the current file and selection.
  - Prompt queuing and steering are distinct requirements; see [Agent Harnesses](#agent-harnesses) for host/build-specific evidence and unresolved legacy ratings.
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

## Antigravity and Gemini

### Maximally Permissive Agent Policy

Antigravity (`agy` language server and CLI), standalone Gemini CLI (`@google/gemini-cli` / `a2a-server`), and the macOS `Gemini.app` desktop client are configured for maximally permissive local agent execution: Turbo permission preset, eager command auto-execution, unsandboxed terminal execution, unrestricted file/gitignore/URL/browser-JS/MCP access, and no artifact review pauses.

### Antigravity Global and Project Settings (`~/.gemini/config/`)

Antigravity stores global user settings in `~/.gemini/config/config.json` (`UserSettings` protobuf in `~/.gemini/bin/agy`) and per-workspace overrides in `~/.gemini/config/projects/<project-id>.json` plus `~/.gemini/config/projects/outside-of-project.json` (`ProjectSettings` protobuf). Both layers must be set so project-level defaults do not shadow global settings:

- **Global `userSettings` (`~/.gemini/config/config.json`):**
  ```json
  {
    "userSettings": {
      "permissionPreset": "AGENT_PERMISSION_PRESET_TURBO",
      "autoExecutionPolicy": "CASCADE_COMMANDS_AUTO_EXECUTION_EAGER",
      "artifactReviewMode": "ARTIFACT_REVIEW_MODE_TURBO",
      "browserJsExecutionPolicy": "BROWSER_JS_EXECUTION_POLICY_TURBO",
      "nonWorkspaceFileAccessPolicy": "AGENT_SETTING_POLICY_ALLOW",
      "internetAccessPolicy": "AGENT_SETTING_POLICY_ALLOW",
      "allowAgentAccessNonWorkspaceFiles": true,
      "allowAgentAccessGitignoreFiles": true,
      "allowCascadeAccessGitignoreFiles": true,
      "enableTerminalSandbox": false,
      "sandboxAllowNetwork": true,
      "enablePersonalCustomizations": true,
      "permissionGrantsV2Migrated": true,
      "globalPermissionGrants": {
        "allow": [
          "command(*)",
          "unsandboxed(*)",
          "read_file(*)",
          "read_file(/)",
          "write_file(*)",
          "write_file(/)",
          "read_url(*)",
          "execute_url(*)",
          "mcp(*)"
        ]
      }
    }
  }
  ```
- **Per-project `settings` and `permissionGrants` (`~/.gemini/config/projects/*.json`):**
  ```json
  {
    "permissionGrants": {
      "v2Migrated": true,
      "permissionGrants": {
        "allow": [
          "command(*)",
          "unsandboxed(*)",
          "read_file(*)",
          "read_file(/)",
          "write_file(*)",
          "write_file(/)",
          "read_url(*)",
          "execute_url(*)",
          "mcp(*)"
        ]
      }
    },
    "settings": {
      "permissionPreset": "AGENT_PERMISSION_PRESET_TURBO",
      "autoExecutionPolicy": "CASCADE_COMMANDS_AUTO_EXECUTION_EAGER",
      "artifactReviewMode": "ARTIFACT_REVIEW_MODE_TURBO",
      "fileAccessPolicy": "AGENT_SETTING_POLICY_ALLOW",
      "internetPolicy": "AGENT_SETTING_POLICY_ALLOW",
      "sandboxMode": false
    }
  }
  ```

### Antigravity Operational Techniques for Agents

- **Bypassing the `read_file`/`write_file` config boundary:** Antigravity's native file tools (`view_file`, `write_to_file`, `replace_file_content`) enforce a hardcoded protection boundary on `~/.gemini/config/config.json` (`Matches hardcoded system protection boundary rule`). Once `enableTerminalSandbox: false` and `autoExecutionPolicy: "CASCADE_COMMANDS_AUTO_EXECUTION_EAGER"` are active, `run_command` executes unsandboxed and can inspect or update `~/.gemini/config/*.json` directly in place.
- **Why URL fetches prompt even in Turbo mode:** Selecting the Turbo preset in the UI sets `permissionPreset` and `autoExecutionPolicy`, but leaves `userSettings.internetAccessPolicy` and project `settings.internetPolicy` unset, causing `read_url_content` to prompt on every new domain unless `AGENT_SETTING_POLICY_ALLOW` and `"read_url(*)"` / `"execute_url(*)"` are explicitly present.
- **Belt-and-suspenders `PreToolUse` `fhold` + auto-allow hook (`~/.gemini/config/hooks.json` and `~/.gemini/config/fhold-pre-tool-hook.py`):** `hooks.json` is reloaded on every turn without restarting `agy`. It invokes `/Users/brian/.gemini/config/fhold-pre-tool-hook.py` on `PreToolUse` (`matcher: ".*"`), which:
  - Auto-approves all non-write and non-Markdown tool calls with `{"decision":"allow"}`.
  - Denies direct IDE writes to symlink paths so agents resolve and edit the canonical target per `AgentRules.md`.
  - On IDE write tools (`replace_file_content`, `multi_replace_file_content`, `write_to_file`, `code_action`, `file_change`) targeting an existing git-tracked `.md` file, runs `/Users/brian/src/tools/fhold status`: blocks IDE edit tools in `unreviewed` (permit) mode (`{"decision":"deny"}`), automatically registers/refreshes a review hold (`antigravity-<convId>`) in `reviewed` mode, auto-releases stale holds (>5 min), and blocks with contention details if another agent holds an active review hold (≤5 min).
- **Inode preservation verified:** Both `replace_file_content` and `write_to_file` (`Overwrite: true`) in Antigravity preserve the existing file inode (`stat -f %i`) on macOS.
- **Aligned multi-root workspace config:** `~/.gemini/config/projects/afc98200-c0e0-4311-875f-64aef4b663ed.json` (`projectResources.resources`), `~/.gemini/projects.json`, `~/.gemini/trustedFolders.json`, and `~/Personal.code-workspace` are aligned to the six canonical roots (`Documents`, `Documents/HoltzDotOrg/Thoughts/wiki`, `My Drive`, `lpscc` via stable `/Users/brian/lpscc` symlink, `src`, and `src/tools`), excluding the legacy `~/bin` symlink.
- **Global agent rules stub (`~/.gemini/GEMINI.md` and symlink `~/.gemini/config/GEMINI.md`):** Points to canonical `/Users/brian/src/tools/docs/AgentRules.md`, summarizes the non-negotiable rules, and includes a `TODO` to trim `AgentRules.md` (~41.8 KB) under Gemini/Antigravity's 24,000-byte (`24 KB`) per-file rule cap so `~/.gemini/GEMINI.md` can become a direct symlink.
- **Hot reload:** `~/.gemini/bin/agy` watches `~/.gemini/config/config.json`, `~/.gemini/config/projects/*.json`, and `~/.gemini/config/hooks.json`, applying permission changes without restarting VS Code or the language server.
- **Binary schema inspection:** `~/.gemini/bin/agy` embeds protobuf descriptors (`jetbox_state.proto`, `codeium_common.proto`, `project.proto`, `cortex.proto`). Search the binary for `UserSettings`, `ProjectSettings`, `PermissionGrantsConfig`, or enum prefixes (`AGENT_SETTING_POLICY_`, `CASCADE_COMMANDS_AUTO_EXECUTION_`) when auditing new releases.

### Standalone Gemini CLI (`~/.gemini/settings.json` and `trustedFolders.json`)

For `@google/gemini-cli` and `a2a-server` sessions, `~/.gemini/settings.json` disables folder-trust gating and sandboxing while enabling tool auto-acceptance:

```json
{
  "security": { "folderTrust": { "enabled": false } },
  "tools": {
    "sandbox": false,
    "autoAccept": true,
    "allowed": [
      "run_shell_command",
      "write_file",
      "replace",
      "read_file",
      "read_many_files",
      "web_fetch",
      "google_web_search"
    ]
  },
  "ide": { "enabled": true }
}
```

`~/.gemini/trustedFolders.json` marks `/Users/brian`, `/Users/brian/Documents`, `/Users/brian/Documents/HoltzDotOrg/Thoughts/wiki`, `/Users/brian/My Drive`, `/Users/brian/lpscc`, `/Users/brian/src`, and `/Users/brian/src/tools` as `"TRUST_FOLDER"`.

### macOS `Gemini.app` (`com.google.GeminiMacOS`)

- **App settings SQLite database (`~/Library/Application Support/com.google.GeminiMacOS/Data/app-settings.store`):** In table `ZPERSISTENTSETTINGS`, set `ZENABLEADDITIONALSANDBOXOPTIONS = 1` (exposes sandbox controls in chat), `ZENABLEADVANCEDBACKUPS = 1` (backs up only modified files in connected folders rather than copying entire trees into `~/.gemini/tasks/<id>/backup/`), and `ZPREVENTSLEEPDURINGTASKS = 1`.
- **Feature and confirmation flags (`~/Library/Preferences/com.google.GeminiMacOS.plist`):** `ClientFlagsService` (`UserDefaultsFlagStorage`) stores each flag under `<userAlias>_<flagName>` as UTF-8 JSON `Data` using Swift's synthesized enum coding (`{"overriddenValue":{"_0":true}}` vs `{"defaultValue":{"_0":false}}`). Set `user1_backup_warning_suppressed_for_all` to `true`, `user1_enableRunCommandBlockAppleScript` to `{"overriddenValue":{"_0":false}}`, and override to `true`: `user1_enableCommandToolYoloMode`, `user1_bundledMcpBypassConfirmation`, `user1_disableNetworkAccessConfirmation`, `user1_enableComputerUseAnyApp`, `user1_enableRunAppleScriptTool`, `user1_enablePythonTool`, `user1_enableMcpCustomLocal`, `user1_enableLocalPlugins`, `user1_enablePlugins`, `user1_enableLocalCCTool`, and `user1_enableCCAutoEnrollOnSubmit`.

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

The VS Code source build lives in `~/src/vscode-markdown-editor`, branch `brian/markdown-ux`, version `0.1.22-local.6`. It includes bundled toolbar/menu translations, Markdown Outline in Explorer, plain-click links (Option-click to edit), a unified toolbar/Cmd+F search bar, a single-row adaptive toolbar with a `»` overflow tray, and explicit active-file attachment to Copilot Chat for text, custom-editor, and Markdown Editor webview tabs. The upper-right button hides the toolbar, margin annotations, line-number gutter, and raw HTML to reclaim vertical and horizontal space; a separate toolbar toggle controls raw HTML while the toolbar is shown. Toolbar and menu tooltips remain visible in narrow panes. Dark themes use dark fenced-code highlighting without Vditor's light grid background. The [GitHub fork](https://github.com/BrianHoltz/vscode-markdown-editor) and [VSIX releases](https://github.com/BrianHoltz/vscode-markdown-editor/releases) make the source and installer available to other Macs. Build commands and verification scope: [ToolMods.md → Zaaack source build](ToolMods.md#zaaack-source-build). The comparison credits Brian's confirmed VS Code Markdown behavior; external-file reread and image rendering still require interactive verification.

`~/src/tools/patches/patch-zaaack.py` is the legacy installed-bundle patcher for Marketplace versions. Do not apply it to the local source build.

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
- **Code Puppy JetBrains 0.28.1 rendering compatibility:** callback-adapter and HTTP navigation-fallback fixes are maintained in the fork; see [ToolMods.md](ToolMods.md#code-puppy-maintained-source-builds).
- **Patch audit 2026.10.09 (personal Mac, 2026.2.3):** restored the missing JCEF remote-mode override (`idea.vmoptions`), Shuzijun 2.0.7 JCEF dependency + 13px font, MCP Server Services-panel suppression, sensitive-file dialog suppression, and built-in Markdown preview light/dark stylesheet. The active `VSCode OSX` keymap is supplied by the installed `keymap-vscode` plugin; no stale custom keymap XML was recreated.
- *command-approval constipation*
- **JetBrains AI Yolo mode:** choose **Allow All** at the bottom of the chat window to grant maximum permissions.
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

The `relationship-shared` IDEA project uses the bounded allowlist in [GitScheme.md § Work project roots](GitScheme.md#work-project-roots): the team repository, `~/src/tools`, and the explicitly approved AI/IDE-toolchain repositories. Attach each individually as a content root/module with its own explicit Git mapping; never attach `~/src` or bulk-add detected siblings. Content roots and VCS mappings are independent: correct modules do not remove stale Git mappings. Validate both sets and the live IDE repository list after a repair. Exclude generated output and IDE metadata inside each module, never a module root. Ignore unrelated unregistered Git roots in this project's VCS settings so discovery does not keep offering them for bulk addition.

A stray `.iml` file does not create a content root unless `modules.xml` registers it. When troubleshooting an unexpected root, inspect `modules.xml` and each registered module's content URL; do not infer roots from filenames alone. IDEA's project tint is separate from content roots: inspect the `ProjectColorInfo` override in `.idea/workspace.xml` or reset Project Color in the UI rather than changing module roots to fix a tint. Keep workspace edits narrow because that file also stores IDE-local session and layout state.

For a different, multi-root personal workspace, its intended roots are separate from this project and must not be copied into `relationship-shared`'s IDEA configuration:

- `~/Documents`
- `~/lpscc` (the stable symlink to the shared-drive root)
- `~/My Drive`
- `~/src`

Use `~/lpscc` rather than `~/My Drive/Libertarian/LPSCC`. For the tools repo, use the real `~/src/tools` path, not the `~/bin` symlink. In any multi-root workspace, attach tools as its own root/module with its own Git mapping; do not attach the parent `~/src` just to reach tools.

### Markdown Preview

The built-in Markdown preview uses `options/markdown.xml` under `MarkdownSettings`. Font size is 14px.

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

### Shuzijun Markdown Editor Source Build

The maintained IDEA source checkout is `~/src/idea-markdown-editor`, branch `brian/markdown-ux`, in the [BrianHoltz fork](https://github.com/BrianHoltz/markdown-editor) of the [Apache-licensed upstream project](https://github.com/shuzijun/markdown-editor). Keep `origin` pointed at the fork and `upstream` at Shuzijun. Local version `2.0.7-local.3` ports the applicable Zaaack improvements into Shuzijun's Vditor/JCEF architecture, isolates bundled assets from stale browser caches, and matches the VS Code custom typography with wrapping, pane-width tables. IDEA supplies native browser find, IntelliJ Structure View, and independent editors per file. Installed-JCEF feature parity requires interactive verification. Build and feature details: [ToolMods.md → Shuzijun source build](ToolMods.md#shuzijun-source-build).

### JCEF Remote Mode (built-in Markdown preview + Shuzijun both broken)

**Symptom:** Built-in IDEA Markdown preview shows nothing / "No subscribers for documentReady"; Shuzijun WYSIWYG tab throws NPE in `JBCefApp.createMessageRouter()`. Both broken simultaneously.

**Root cause:** IDEA 2026.2 enables JCEF out-of-process (remote) mode by default; native CEF objects are null in remote mode, breaking all JCEF consumers. Full root cause chain and fix: **ToolMods.md → JCEF Remote Mode**.

**Fix summary:** add `-Djcef.remote.enabled=false` to `~/Library/Application Support/JetBrains/IntelliJIdea2026.2/idea.vmoptions`. Restart IDEA. **Applied:** 2026.07.02; restored for the 2026.2.3 config on 2026.10.09.

### Wibey Extension Patches

New conversation bug fix (`clearMessages` on `newParallelSession`) — still unfixed upstream as of 1.0.31; reapplied to the VS Code install 2026.10.09 (marketplace updates overwrite it). Full procedure: **ToolMods.md → Wibey Extension**.

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

*[doc-audit](https://github.com/BrianHoltz/tools/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.10.13.Tue*
