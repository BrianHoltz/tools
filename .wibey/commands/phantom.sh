#!/bin/bash
# Disconnect VPN, run this script, reconnect VPN.
#
# Agent-managed registry: add off-VPN work commands here.
# This is the standard place for any task that requires disconnected network access
# (npm/pnpm installs, gradle downloads, etc. blocked by Zscaler on VPN).
#
# Usage: disconnect-vpn-do-work.sh [job...]
# If no job specified, runs all.

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
# Entry point
# ============================================================================
if [ $# -eq 0 ]; then
    # Run all jobs
    for func in $(compgen -A function | grep '^job:'); do
        $func
        echo ""
    done
else
    # Run specified jobs
    for job in "$@"; do
        "job:$job"
        echo ""
    done
fi

echo "✓ Off-VPN work complete. Safe to reconnect VPN."
