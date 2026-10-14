# Idea Peacock

## Summary

- **Goal:** Provide an IntelliJ IDEA equivalent to the VS Code project-coloring experience: a bright, project-specific color that makes each open IDE window easy to identify.
- **Current status:** Research is complete enough to choose an implementation direction. No plugin source has been created yet.
- **Finding:** A convincing project-colored IntelliJ window accent is feasible. Arbitrary recoloring of the native operating-system title bar and outer frame is not exposed through a supported public IntelliJ Platform API.
- **Closest existing options:** [GlowStick MHL](https://plugins.jetbrains.com/plugin/32984-glowstick-mhl) is the strongest current candidate; [Project Color Bar](https://plugins.jetbrains.com/plugin/31880-project-color-bar) is another current candidate. Both paint Swing/client-area surfaces rather than proving control of native OS chrome.
- **Recommendation:** Test GlowStick MHL first. If its appearance or controls are insufficient, create a small plugin using a project-scoped color and a plugin-owned client-area border/header. Treat native title-bar coverage as an optional, explicitly unsupported optimization rather than the core contract.
- **Confidence:** High (0.9) that a useful Peacock-like client-area plugin can be built; high (0.9) that no supported cross-platform public API exists for arbitrary native frame colors; medium (0.7) that an existing plugin will meet the desired visual standard without modification.
- **Checkpoint:** 2026.10.14.Wed.0145 PDT.

## Current status

### Research completed

- The likely VS Code reference is Peacock-style project coloring: the important behavior is persistent project identity, not merely a theme change.
- The local `/Users/brian/IdeaProjects/Personal` workspace contains IntelliJ project metadata but no existing IDEA plugin source or build.
- Marketplace research found several related plugins:
  - **GlowStick MHL** is listed and has a 2026 release line. Its source obtains the project `JFrame`, installs a border component on the root-pane glass pane, and paints colored edge strips.
  - **Project Color Bar** is listed and targets IDEA 2024.1–2026.3 in Marketplace metadata. Its source paints top/left/right/bottom gradient bands, a content-pane border, and root-pane/frame backgrounds using Swing.
  - **Material Theme UI Project Frame** provides a narrow top stripe and depends on Material Theme UI.
  - **Project-Color** is a historical analogue with an obsolete 211.0–230.* build range.
  - **Colorized-Project** is an unmaintained historical fork limited to an old 231.* build range.
- Official IntelliJ API review found no public `setTitleBarColor`, `setFrameColor`, or equivalent operation. Public `WindowManager` and `IdeFrame` APIs locate frames and set title text, but do not expose native-caption painting.
- IntelliJ’s internal custom-decoration implementation and JetBrains Runtime `WindowDecorations` API can merge client content with native title-bar controls on supported Windows/macOS configurations. These are internal/runtime-specific mechanisms, not a stable third-party plugin contract.
- OS behavior differs materially:
  - Windows native caption color is controlled by DWM/system decoration unless the application replaces the title bar.
  - macOS title-bar composition is AppKit/JBR-specific.
  - Linux decoration is mediated by X11/Wayland and the selected window manager.

### What is not established

- No candidate plugin was verified to recolor every native caption pixel, caption button, resize border, compositor shadow, taskbar/dock representation, or system menu.
- Marketplace compatibility ranges are declarations, not proof of runtime success on every IDE build, operating system, JBR version, UI mode, fullscreen state, or HiDPI configuration.
- A plugin that calls IntelliJ implementation classes or JBR decoration APIs would need narrow version/runtime gates and safe fallback behavior.

## Proposed plan

### Evaluate existing plugins

- Install GlowStick MHL in the target IDEA build.
- Test several projects with manual and automatic colors.
- Record coverage for the editor/client area, IDE header, native caption, caption buttons, resize border, maximized state, fullscreen state, external display/HiDPI, and project switching.
- Repeat the same test with Project Color Bar if GlowStick MHL does not meet the visual requirement.

### Decide whether to build

- Reuse an existing plugin if it provides the desired appearance, project persistence, color controls, and target-IDE compatibility.
- If neither candidate is sufficient, scaffold a new IntelliJ Platform plugin rather than modifying the personal project container.
- Use a project service for persisted color state and public lifecycle/frame lookup APIs.
- Paint a plugin-owned root-pane/glass-pane border or header on the EDT.
- Reapply on project activation and relevant Look-and-Feel changes; dispose listeners and components with the project/plugin lifecycle.

### Define the product contract

- Call the supported feature a **project-colored IDE window accent** or **project-colored header/border**.
- Do not promise native OS-frame recoloring.
- If an optional custom-decoration integration is attempted, gate it by exact IDE/JBR/OS capability and retain the client-area fallback.
- Keep the first version deliberately narrow: manual per-project color, automatic color derived from project identity, opacity/width controls, and a reset action.

### Validate and package

- Test on the actual target IntelliJ IDEA build first.
- Add compatibility checks for the supported build range.
- Verify project reopen, multiple simultaneous projects, theme changes, plugin reload/unload, maximized/fullscreen modes, and disposal.
- Build the plugin artifact and copy the rebuilt ZIP to the Downloads folder after each implementation fix, per the standing extension-build preference.

## Review recommendation

A Sol/Astra review is not needed to decide whether to investigate or prototype the client-area implementation; the research is already sufficiently converged for that. Invoke a Sol/Astra review before using internal IntelliJ/JBR decoration APIs, or before publishing any claim that the plugin controls native title-bar pixels. The review should specifically challenge API stability, fallback behavior, cross-platform claims, and compatibility gating.

## Evidence

### Existing plugins

- [GlowStick MHL Marketplace](https://plugins.jetbrains.com/plugin/32984-glowstick-mhl)
- [GlowStick MHL Marketplace metadata](https://plugins.jetbrains.com/api/plugins/32984)
- [GlowStick MHL source](https://raw.githubusercontent.com/MarcinOrlowski/idea-glowstick-mhl/master/src/main/kotlin/com/marcinorlowski/glowstick/ProjectColorApplier.kt)
- [Project Color Bar Marketplace](https://plugins.jetbrains.com/plugin/31880-project-color-bar)
- [Project Color Bar Marketplace metadata](https://plugins.jetbrains.com/api/plugins/31880)
- [Project Color Bar source](https://github.com/papalugo/project-color-bar-plugin/blob/b6e0bb2eeed4915ab7653348d9bd5b2c8032efc2/src/main/kotlin/com/papalugo/projectcolorbar/ProjectColorApplier.kt)
- [Project-Color Marketplace updates](https://plugins.jetbrains.com/api/plugins/19463/updates)
- [Colorized-Project Marketplace metadata](https://plugins.jetbrains.com/api/plugins/20920)

### IntelliJ and JBR APIs

- [IdeFrame](https://github.com/JetBrains/intellij-community/blob/master/platform/ide-core/src/com/intellij/openapi/wm/IdeFrame.java)
- [WindowManager](https://github.com/JetBrains/intellij-community/blob/master/platform/ide-core/src/com/intellij/openapi/wm/WindowManager.java)
- [WindowManagerEx](https://github.com/JetBrains/intellij-community/blob/master/platform/platform-impl/src/com/intellij/openapi/wm/ex/WindowManagerEx.java)
- [IdeFrameDecorator](https://github.com/JetBrains/intellij-community/blob/master/platform/platform-impl/src/com/intellij/openapi/wm/impl/IdeFrameDecorator.kt)
- [CustomWindowHeaderUtil](https://github.com/JetBrains/intellij-community/blob/master/platform/platform-impl/src/com/intellij/openapi/wm/impl/customFrameDecorations/header/CustomWindowHeaderUtil.kt)
- [JBR WindowDecorations](https://github.com/JetBrains/JetBrainsRuntime/blob/a8a5398a738fab3daa559874e779faad9c85e746/src/jetbrains.api/src/com/jetbrains/WindowDecorations.java)
- [IntelliJ plugin compatibility](https://plugins.jetbrains.com/docs/intellij/plugin-compatibility.html)
- [IntelliJ dynamic plugins](https://plugins.jetbrains.com/docs/intellij/dynamic-plugins.html)

## Work log

- **2026.10.13:** Established that the local workspace was not an existing IntelliJ plugin and started separate research tracks for the VS Code reference, Marketplace candidates, and IntelliJ/JBR APIs.
- **2026.10.13:** Research converged on a client-area implementation boundary: public frame/lifecycle APIs plus Swing painting are viable; arbitrary native frame-color control is not a supported portable API.
- **2026.10.14:** Wrote this report with the implementation plan, confidence assessment, and Sol/Astra review gate.

*[doc-audit](https://github.com/BrianHoltz/tools/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.10.14.Wed*
