// Gradle init script — Walmart-network overlay.
//
// Installed to ~/.gradle/init.d/ on Walmart laptops only (never committed to
// any project repo). Injects Walmart's Artifactory mirrors ahead of the
// public Maven Central / Gradle Plugin Portal so dependency and plugin jar
// downloads don't hit Zscaler's binary-content block. Applies to every
// Gradle build on this machine; harmless no-op on the unrestricted home
// network since it only prepends extra repositories, never removes the
// public ones. See ~/src/tools/gradle-overlays/walmart/README.md.

val walmartMavenCentralRepository = "https://generic.ci.artifacts.walmart.com/artifactory/central-mvn-release-remote"
val walmartGradlePluginRepository = "https://generic.ci.artifacts.walmart.com/artifactory/grails-core-mvn-release-remote"

settingsEvaluated {
    pluginManagement.repositories {
        maven { url = uri(walmartGradlePluginRepository) }
        maven { url = uri(walmartMavenCentralRepository) }
    }
}

allprojects {
    repositories {
        maven { url = uri(walmartGradlePluginRepository) }
        maven { url = uri(walmartMavenCentralRepository) }
    }
}
