#!/bin/bash
# phantom-agent: Bare-minimum off-VPN task registry
#
# Runs only the BARE MINIMUM commands agents need executed while VPN is disconnected.
# Completely rewritten for each blocking episode as new network constraints emerge.
# Git history tracks the evolution of what must run offline.
#
# Before disconnecting VPN: phantom-agent
# Reconnect VPN when done.

set -e

# ============================================================================
# VSCode Markdown Editor: pnpm install
# ============================================================================
job:vscode-markdown-install() {
    echo "→ VSCode Markdown: pnpm install"
    cd /Users/b0h0166/src/vscode-markdown-editor
    pnpm install
}

# ============================================================================
# VSCode Markdown Editor: add @vscode/vsce devDependency (one-time)
# Not in the existing lockfile, so pnpm must fetch new tarballs from
# registry.npmjs.org. On VPN this gets ECONNRESET / 403 MediaTypeBlocked
# from Zscaler content filtering on several packages (commander, marked,
# @azure/msal-*, etc.) — same binary-block pattern as gradle/jetbrains.
# A failed attempt leaves pnpm-lock.yaml modified with no package.json
# change; if this job fails, run `git checkout -- pnpm-lock.yaml` in that
# repo to restore a clean state before retrying.
# ============================================================================
job:vscode-markdown-add-vsce() {
    echo "→ VSCode Markdown: add @vscode/vsce devDependency"
    cd /Users/b0h0166/src/vscode-markdown-editor
    pnpm add -D -w @vscode/vsce
}

# ============================================================================
# IDEA Markdown Editor: full plugin build (gradlew buildPlugin)
# ~/.gradle/gradle.properties mixes two kinds of settings:
#   (a) on-VPN-only network config: corporate proxy host/port/nonProxyHosts
#       and a custom truststore (walmart_cacerts) built for MITM'd traffic
#       through that proxy — proxy-intlho.wal-mart.com doesn't resolve
#       off-VPN, and the custom truststore likely lacks public root CAs
#       (confirmed: the JDK *default* cacerts handles public HTTPS fine
#       off-VPN once the whole file was removed in an earlier episode).
#   (b) settings needed regardless of VPN state: org.gradle.java.home
#       (Gradle 9.6.1 requires JVM 17+ just to launch — removing this
#       wholesale broke the build with "Gradle requires JVM 17 or later...
#       configured to use JVM 8" once the file was fully moved aside) and
#       org.jetbrains.intellij.platform.versionOverride=2.11.0 (consumed by
#       settings.gradle.kts resolutionStrategy — omitting it off-VPN resolves
#       platform 2.18.1 from build.gradle.kts instead, a cache miss against
#       what the on-VPN build actually wants).
# Fix: strip only the proxy/truststore lines, keep everything else, restore
# unconditionally by overwriting (not swapping) so the file's inode survives.
#
# `buildPlugin` (not `help` or `--version`) forces full resolution of the
# buildscript classpath (foojay-resolver, org.jetbrains.intellij.platform,
# de.undercouch.download, changelog + transitives from mavenCentral()) AND
# the IntelliJ Platform SDK download + compile/test configurations. Both
# plugins.gradle.org and mavenCentral() are Zscaler-blocked on VPN (403
# MediaTypeBlocked, confirmed on foojay-resolver-1.0.0.jar); `help` only
# covers the buildscript classpath and would leave the SDK download as the
# next surprise. Off-VPN has full internet, so build the real artifact
# outright instead of just priming the cache.
# ============================================================================
job:idea-markdown-gradle() {
    echo "→ IDEA Markdown: gradle full plugin build"
    local props=~/.gradle/gradle.properties
    local backup=~/.gradle/gradle.properties.phantom-backup
    local restored=0
    if [ -f "$props" ]; then
        cp "$props" "$backup"
        restored=1
        grep -vE '^systemProp\.(https?\.proxy(Host|Port)|https?\.nonProxyHosts|javax\.net\.ssl\.trustStore(Password)?)=' \
            "$backup" > "$props"
    fi
    local status=0
    (cd /Users/b0h0166/src/idea-markdown-editor && ./gradlew buildPlugin) || status=$?
    if [ "$restored" = 1 ]; then
        cat "$backup" > "$props"
        rm -f "$backup"
        echo "(restored ~/.gradle/gradle.properties)"
    fi
    if [ "$status" = 0 ]; then
        echo "Build artifacts:"
        ls -l /Users/b0h0166/src/idea-markdown-editor/build/distributions/*.zip 2>/dev/null
    fi
    return "$status"
}

# ============================================================================
# JetBrains Marketplace: Air plugin download
# Zscaler SSLO inspection (SSL_Decryption_Authority_SSLO_*.wal-mart.com) hangs
# with 0 bytes received on this binary via both corporate proxies on VPN.
# Confirmed network-wide, not proxy-specific or IDE-config-specific.
#
# Use the EXACT URL IntelliJ's own error dialog reports, not a simplified
# "stable" pluginId-only URL — that 404s for this plugin (confirmed off-VPN).
# The full URL (with updateId/family/uuid/build params) is confirmed to reach
# a real TLS handshake and start a real download; only Zscaler's on-VPN
# content inspection blocks it, so off-VPN it should complete.
# ============================================================================
job:jetbrains-air-plugin-download() {
    echo "→ JetBrains Marketplace: Air plugin zip"
    curl -fL --max-time 60 -o ~/Downloads/air-plugin.zip \
        "https://downloads.marketplace.jetbrains.com/files/33314/1189348/air-plugin-262.8665.490.zip?updateId=1189348&pluginId=33314&family=INTELLIJ&uuid=1408232d48feb78-be60-4c4f-8226-aa686ac14508&updatedFrom=code=IU&build=262.10968.63"
    echo "Saved to ~/Downloads/air-plugin.zip — install via Settings > Plugins > ⚙ > Install Plugin from Disk"
}

# ============================================================================
# Execute all registered phantom jobs
# `set -e` would otherwise abort the whole script at the first job's nonzero
# return, silently skipping every job listed after it — confirmed in a real
# run where the gradle job's failure left the Air plugin job never attempted.
# Capture each job's status and keep going so one failure doesn't starve the
# rest of the off-VPN window.
# ============================================================================
failures=0
for func in $(compgen -A function | grep '^job:'); do
    $func || { echo "✗ $func FAILED"; failures=$((failures + 1)); }
    echo ""
done

if [ "$failures" -gt 0 ]; then
    echo "⚠ $failures job(s) failed — see output above. Reconnect VPN and report back."
else
    echo "✓ Phantom work complete. Safe to reconnect VPN."
fi
