#!/bin/bash
# vpn-bypass-build: Run network-heavy package manager downloads off-VPN
# Usage: vpn-bypass-build.sh [project...]
#
# Supported projects: vscode-markdown, idea-markdown
# If no project specified, runs all known projects.
#
# Disconnect VPN, run this script, then reconnect VPN and run the actual builds.

set -e

run_vscode_markdown() {
    echo "=== VSCode Markdown Editor: pnpm install (network) ==="
    cd /Users/b0h0166/src/vscode-markdown-editor
    pnpm install
}

run_idea_markdown() {
    echo "=== IDEA Markdown Editor: download Gradle (network) ==="
    cd /Users/b0h0166/src/idea-markdown-editor
    ./gradlew --version
}

# Determine which projects to run
if [ $# -eq 0 ]; then
    projects=("vscode-markdown" "idea-markdown")
else
    projects=("$@")
fi

for project in "${projects[@]}"; do
    case "$project" in
        vscode-markdown|vscode)
            run_vscode_markdown
            ;;
        idea-markdown|idea)
            run_idea_markdown
            ;;
        *)
            echo "Unknown project: $project"
            exit 1
            ;;
    esac
    echo ""
done

echo "✓ Network downloads cached. Safe to reconnect VPN."
