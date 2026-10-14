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
