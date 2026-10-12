#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")" && pwd -P)"
source_root="$repo_root/.wibey/skills"
skill_names=(commitz convo)
agent_skill_roots=(
  "$HOME/.agents/skills"
  "$HOME/.claude/skills"
  "$HOME/.copilot/skills"
  "$HOME/.github/skills"
)

for agent_root in "${agent_skill_roots[@]}"; do
  mkdir -p "$agent_root"
  for skill_name in "${skill_names[@]}"; do
    source="$source_root/$skill_name"
    target="$agent_root/$skill_name"
    if [[ -L "$target" ]]; then
      current_target="$(readlink "$target")"
      if [[ "$current_target" == "$source" ]]; then
        continue
      fi
      printf 'Refusing to replace conflicting skill symlink: %s -> %s\n' \
        "$target" "$current_target" >&2
      exit 1
    fi
    if [[ -e "$target" ]]; then
      printf 'Refusing to replace existing skill path: %s\n' "$target" >&2
      exit 1
    fi
    ln -s "$source" "$target"
  done
done
