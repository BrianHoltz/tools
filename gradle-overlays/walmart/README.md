# Walmart Gradle overlay

Some personal Gradle-based repos (`~/src/idea-markdown-editor`, the Shuzijun
Markdown Editor fork) build fine on the unrestricted home network but hit
Zscaler's binary-content block on the Walmart network: small JSON/metadata
GETs succeed, but the actual Gradle distribution zip and dependency/plugin
jars get reset or 403 ("MediaTypeBlocked") even through the corporate proxy.

Those repos are public (`github.com/BrianHoltz/...`), so the fix must not
leak Walmart-internal Artifactory hostnames into their committed history.
This overlay keeps every repo's own files machine-agnostic and injects the
Walmart-specific bits entirely from outside the repo:

- `init.d/walmart-maven-mirrors.init.gradle.kts` → copied to
  `~/.gradle/init.d/`. Prepends Walmart's Artifactory mirrors (Maven Central
  + Gradle Plugin Portal proxies) ahead of the public ones for every Gradle
  build on this machine. No-op on the home laptop (just extra repositories
  that never get queried there).
- `gradle-wrapper.properties.template` → locally overwrites a repo's
  `gradle/wrapper/gradle-wrapper.properties` to fetch the Gradle
  distribution zip from Walmart's mirror instead of the public one. This one
  **does** modify a tracked file in the working tree — intentionally never
  committed, since `distributionUrl` is read by the wrapper bootstrap before
  any init script or gradle.properties can apply, and Gradle's wrapper cache
  is keyed by the exact URL text (no cache hit across different URLs for
  the same version).
- Plugin-version overrides (e.g. the IntelliJ Platform Gradle Plugin version
  not yet being mirrored internally) go in `~/.gradle/gradle.properties` as
  `<plugin.id>.versionOverride=<version>`, read by a generic
  `pluginManagement.resolutionStrategy.eachPlugin` hook that each repo's own
  `settings.gradle.kts` declares (see `idea-markdown-editor`'s for the
  pattern) — purely additive, no-op unless the property is set.

## Usage

```sh
~/src/tools/gradle-overlays/walmart/apply.sh <repo-path> [plugin.id=version ...]
```

Rerun after every fresh clone or `git pull` of an affected repo — the
wrapper-properties overwrite doesn't survive a pull. Never `git add` the
modified `gradle-wrapper.properties`; it's meant to stay a local diff.

## Why not just commit the Walmart mirrors?

The repos this applies to are personal public GitHub forks, not Walmart
GHE repos. Committing `generic.ci.artifacts.walmart.com` there would expose
internal infrastructure hostnames in public git history permanently, even
without opening a PR. Repos that are already Walmart-internal-only (GHE,
e.g. `wibey-jetbrains-plugin`) commit their Walmart mirror URLs directly —
that's fine, since the repo's own visibility already gates exposure.
