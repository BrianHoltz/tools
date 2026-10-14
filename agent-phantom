#!/bin/bash
# phantom: Ghost work registry for off-VPN tasks
#
# Before disconnecting VPN: phantom
# Reconnect VPN when done.
#
# Agent-managed registry of work that must run while disconnected
# (pnpm installs, gradle downloads, etc. blocked by Zscaler on VPN).

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
# ============================================================================
job:idea-markdown-gradle() {
    echo "→ IDEA Markdown: gradle wrapper download"
    cd /Users/b0h0166/src/idea-markdown-editor
    ./gradlew --version
}

# ============================================================================
# Execute all registered phantom jobs
# ============================================================================
for func in $(compgen -A function | grep '^job:'); do
    $func
    echo ""
done

echo "✓ Phantom work complete. Safe to reconnect VPN."
