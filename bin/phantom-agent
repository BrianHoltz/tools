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
# IDEA Markdown Editor: Gradle wrapper download
# ~/.gradle/gradle.properties deliberately hardcodes the on-VPN corporate
# proxy (proxy-intlho.wal-mart.com) for use when actually building on VPN.
# That host doesn't resolve off-VPN, but services.gradle.org resolves fine
# directly off-VPN — so the wrapper bootstrap only needs the proxy config
# gone for this one invocation. Move it aside, download, always restore.
# ============================================================================
job:idea-markdown-gradle() {
    echo "→ IDEA Markdown: gradle wrapper download"
    local props=~/.gradle/gradle.properties
    local backup=~/.gradle/gradle.properties.phantom-backup
    local restored=0
    if [ -f "$props" ]; then
        mv "$props" "$backup"
        restored=1
    fi
    local status=0
    (cd /Users/b0h0166/src/idea-markdown-editor && ./gradlew --version) || status=$?
    if [ "$restored" = 1 ]; then
        mv "$backup" "$props"
        echo "(restored ~/.gradle/gradle.properties)"
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
# ============================================================================
for func in $(compgen -A function | grep '^job:'); do
    $func
    echo ""
done

echo "✓ Phantom work complete. Safe to reconnect VPN."
