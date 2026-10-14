# IntelliJ window frame colors

## Summary

- **Where:** `/Users/brian/IdeaProjects/Personal`, with the checkpoint in `~/src/tools/docs/`.
- **What:** Determine whether IntelliJ IDEA has a plugin equivalent to the VS Code extension that applies a bright project-specific color to the whole title bar and window frame; create one if no suitable plugin exists.
- **Why:** Distinctive window chrome makes multiple IDEA projects easier to identify, matching the workflow enabled by VS Code's Peacock-style project coloring.
- **How:** Identify the VS Code reference behavior, search JetBrains Marketplace and open-source plugins, verify IntelliJ Platform APIs and operating-system limitations, then choose reuse, fork, or implementation.
- **Which:** VS Code extension behavior, JetBrains Marketplace, IntelliJ Platform window APIs, and the local personal-project workspace.
- **When:** Research started 2026.10.13.Tue.2204 PDT; checkpoint recorded 2026.10.13.Tue.2256 PDT.
- **Confidence:** 0.55 that the feature is implementable as an IntelliJ plugin; 0.35 that an existing plugin already provides the complete native title-bar/window-frame behavior; confidence will increase after the three research tracks finish.

## Contents

- [Tasks](#tasks)
- [Active Work](#active-work)
- [Pending Decisions](#pending-decisions)
- [Evidence](#evidence)
- [Work Log](#work-log)

## Tasks

| Task | Status | Notes |
| --- | --- | --- |
| **Identify the VS Code reference** | ▶️10.13 | Confirm the extension name, exact settings, project-scoped behavior, and platform coverage. |
| **Check existing IDEA plugins** | ▶️10.13 | Search Marketplace and source repositories for native title-bar or full-window frame coloring rather than editor-only accents. |
| **Verify IntelliJ implementation path** | ▶️10.13 | Establish supported APIs and platform-specific limits for macOS, Windows, and Linux. |
| Choose reuse or implementation |  | Depends on the preceding research; select an existing plugin, fork, or new plugin architecture. |
| Build and validate the IDEA plugin |  | Scope depends on the selected path; include installation artifact validation. |

## Active Work

### Identify the VS Code reference

- Research track is checking whether the intended extension is Peacock and documenting its title-bar/window-frame behavior.
- The requested target is the visible native window chrome, not merely editor tabs, tool windows, or the IDE color scheme.

### Check existing IDEA plugins

- Research track is checking JetBrains Marketplace listings and project repositories.
- A plugin that changes only editor colors or tool-window headers will not satisfy the requested equivalence.

### Verify IntelliJ implementation path

- Research track is checking `WindowManagerEx`, `IdeFrame`, Swing window properties, custom title-bar support, and OS-specific constraints.
- The implementation must preserve normal IDEA behavior and avoid assuming that all platforms expose the same native decoration controls.

## Pending Decisions

- **Scope of the first implementation:** native title-bar/frame coloring on all supported desktop platforms versus a best-effort implementation with explicit platform limitations.
- **Color source:** manual per-project color, generated palette, or reuse of the VS Code extension's project-color conventions.
- **Review gate:** invoke a Sol/Astra review after the research report and before scaffolding or editing plugin code if the API path or native-window feasibility remains uncertain.

## Evidence

### Workspace baseline ❀

<a id="e-workspace-baseline"></a>

- **Claim:** The target workspace contains IntelliJ project metadata and personal files, but no existing IntelliJ plugin source, Gradle plugin build, `plugin.xml`, or matching title-bar implementation.
- **Source:** `/Users/brian/IdeaProjects/Personal`; workspace search for `title.?bar|window.?frame|frame.?color|plugin.xml|build.gradle`.
- **Dates:** Collected 2026.10.13.Tue.2256 PDT.

### Research tracks ❁

<a id="e-research-tracks"></a>

- **Claim:** Independent research is in progress for existing IDEA plugins, official IntelliJ APIs, and the VS Code reference behavior.
- **Source:** Research notes under `/Users/brian/IdeaProjects/Personal/research_notes/IntelliJ window frame colors/`.
- **Dates:** Started 2026.10.13.Tue.

## Work Log

### 10.13 Tue Established the investigation boundary

- **22:04:** Interpreted the requested VS Code feature as project-specific coloring of the complete title bar and window frame, likely the behavior associated with Peacock.
- **22:04:** Confirmed the local workspace is not an existing plugin implementation and started separate marketplace, API, and VS Code reference investigations.
- **22:56:** Created this checkpoint with implementation confidence at 0.55 and a review decision deferred until research establishes the available plugin/API path.

*[doc-audit](https://github.com/BrianHoltz/tools/blob/main/.wibey/skills/doc-audit/SKILL.md): 2026.10.13.Tue*
