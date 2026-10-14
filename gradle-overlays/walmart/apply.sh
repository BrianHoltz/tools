#!/usr/bin/env bash
# Apply the Walmart-network Gradle overlay to a local repo checkout.
#
# Never commit the effect of this script — it only touches files outside
# the repo's git history (gradle-wrapper.properties is modified in the
# working tree but intentionally left uncommitted; everything else lands in
# ~/.gradle/, outside any repo). Safe to rerun after every clone/pull.
#
# Usage:
#   ~/src/tools/gradle-overlays/walmart/apply.sh <repo-path> [plugin.id=version ...]
#
# Example:
#   ~/src/tools/gradle-overlays/walmart/apply.sh ~/src/idea-markdown-editor \
#     org.jetbrains.intellij.platform=2.11.0

set -euo pipefail

OVERLAY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
REPO="${1:?Usage: apply.sh <repo-path> [plugin.id=version ...]}"
shift || true

WRAPPER_PROPS="$REPO/gradle/wrapper/gradle-wrapper.properties"
if [ ! -f "$WRAPPER_PROPS" ]; then
  echo "ERROR: $WRAPPER_PROPS not found — is this a Gradle-wrapped repo?" >&2
  exit 1
fi
WRAPPER_REL="gradle/wrapper/gradle-wrapper.properties"

# Keep the public wrapper configuration in the index while allowing the
# Walmart-only URL to remain in this checkout. This prevents repository-wide
# sync commands from publishing an internal hostname.
if git -C "$REPO" rev-parse --show-toplevel >/dev/null 2>&1; then
  git -C "$REPO" update-index --no-skip-worktree -- "$WRAPPER_REL"
fi

CURRENT_URL=$(grep -m1 '^distributionUrl=' "$WRAPPER_PROPS" | cut -d= -f2-)
GRADLE_VERSION=$(echo "$CURRENT_URL" | grep -oE 'gradle-[0-9]+\.[0-9]+(\.[0-9]+)?-bin' | sed -E 's/gradle-(.*)-bin/\1/')
if [ -z "$GRADLE_VERSION" ]; then
  echo "ERROR: couldn't parse Gradle version out of distributionUrl: $CURRENT_URL" >&2
  exit 1
fi
echo "== Detected Gradle version: $GRADLE_VERSION =="

echo "== Overwriting $WRAPPER_PROPS (local, uncommitted) =="
sed "s/GRADLE_VERSION/$GRADLE_VERSION/g" "$OVERLAY_DIR/gradle-wrapper.properties.template" > "$WRAPPER_PROPS"
if git -C "$REPO" rev-parse --show-toplevel >/dev/null 2>&1; then
  git -C "$REPO" update-index --skip-worktree -- "$WRAPPER_REL"
fi

echo "== Installing Maven/plugin-portal mirror init script =="
mkdir -p "$HOME/.gradle/init.d"
cp -p "$OVERLAY_DIR/init.d/walmart-maven-mirrors.init.gradle.kts" "$HOME/.gradle/init.d/"

if [ "$#" -gt 0 ]; then
  echo "== Recording plugin version overrides in ~/.gradle/gradle.properties =="
  touch "$HOME/.gradle/gradle.properties"
  for override in "$@"; do
    plugin_id="${override%%=*}"
    key="${plugin_id}.versionOverride"
    value="${override#*=}"
    if grep -q "^${key}=" "$HOME/.gradle/gradle.properties" 2>/dev/null; then
      sed -i '' "s|^${key}=.*|${key}=${value}|" "$HOME/.gradle/gradle.properties"
    else
      echo "${key}=${value}" >> "$HOME/.gradle/gradle.properties"
    fi
    echo "  $key=$value"
  done
  echo "(This only takes effect if the project's settings.gradle.kts declares the"
  echo " matching pluginManagement.resolutionStrategy.eachPlugin hook — see"
  echo " ~/src/idea-markdown-editor/settings.gradle.kts for the pattern.)"
fi

echo
echo "Done. $REPO is ready to build on the Walmart network."
echo "Remember: $WRAPPER_PROPS is now locally modified — never 'git add' it."
