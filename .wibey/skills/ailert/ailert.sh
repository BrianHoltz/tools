#!/bin/bash
# ailert.sh — Executable wrapper for the ailert skill
# Usage: TIMEOUT=30 MSG="Your message here" bash ~/.wibey/skills/ailert/ailert.sh
# Or: bash ~/.wibey/skills/ailert/ailert.sh 30 "Your message here"

set -e

# Consume options before interpreting timeout/message; flags are never messages.
TIMEOUT="${TIMEOUT-30}"
MSG="${MSG:-Wibey needs your attention}"
SLACK_ENABLED=${AILERT_SLACK:-0}
SMS_ENABLED=0
TEST_MODE=0
POSITIONAL=()
while [ $# -gt 0 ]; do
  case "$1" in
    --no-slack) SLACK_ENABLED=0 ;;
    --sms) SMS_ENABLED=1 ;;
    --test) TEST_MODE=1 ;;
    --) shift; POSITIONAL+=("$@"); break ;;
    -*) echo "ERROR: unknown ailert option: $1" >&2; exit 2 ;;
    *) POSITIONAL+=("$1") ;;
  esac
  shift
done
set -- "${POSITIONAL[@]}"
if [ $# -gt 0 ] && [[ "$1" =~ ^[0-9]+$ ]]; then
  TIMEOUT="$1"
  shift
fi
[ $# -eq 0 ] || MSG="$*"
if ! [[ "$TIMEOUT" =~ ^[0-9]+$ ]]; then
  echo "ERROR: ailert timeout must be a non-negative integer" >&2
  exit 2
fi
TIMEOUT=$((10#$TIMEOUT))

# --test: dry run only; no dialog, sounds, speech, or external messages.
if [ "$TEST_MODE" = 1 ]; then
  [ "$SLACK_ENABLED" = 1 ] && [ -f "$HOME/.claude/skills/slack/scripts/message.ts" ] && echo "Slack: available" || echo "Slack: unavailable"
  [ "$SMS_ENABLED" = 1 ] && [ -n "${AILERT_SMS_COMMAND:-}" ] && [ -x "$AILERT_SMS_COMMAND" ] && echo "SMS: available" || echo "SMS: unavailable"
  exit 0
fi

# Resolve assets next to this script first, then through installed adapters.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for D in "$SCRIPT_DIR/assets" \
         "$HOME/.wibey/skills/ailert/assets" \
         "$HOME/bin/.wibey/skills/ailert/assets"; do
  [ -d "$D" ] && ASSETS="$D" && break
done

if [ -z "$ASSETS" ]; then
  echo "ERROR: ailert assets not found; using fallback (no sounds)" >&2
  ASSETS="/dev/null"
fi

# Level 1: visible dialog
osascript - "$MSG" <<'APPLESCRIPT' &
on run argv
  display alert "🌀 Wibey" message (item 1 of argv) giving up after 300
end run
APPLESCRIPT
DIALOG_PID=$!

# Level 2/3: distinctive sounds (if assets found)
if [ "$ASSETS" != "/dev/null" ] && [ -f "$ASSETS/trek_communicator.mp3" ]; then
  ( sleep "$((TIMEOUT / 3))" && afplay "$ASSETS/trek_communicator.mp3" ) & SND1_PID=$!
else
  SND1_PID=""
fi

if [ "$ASSETS" != "/dev/null" ] && [ -f "$ASSETS/cylon_attention.wav" ]; then
  ( sleep "$((TIMEOUT * 2 / 3))" && afplay "$ASSETS/cylon_attention.wav" ) & SND2_PID=$!
else
  SND2_PID=""
fi

# Wait for timeout
ELAPSED=0
while [ "$ELAPSED" -lt "$TIMEOUT" ] && kill -0 "$DIALOG_PID" 2>/dev/null; do
  sleep 1
  ELAPSED=$((ELAPSED + 1))
done

# Level 4: speech if still showing
if kill -0 "$DIALOG_PID" 2>/dev/null; then
  say "$MSG" 2>/dev/null || true
  kill "$DIALOG_PID" 2>/dev/null || true
else
  [ -n "$SND1_PID" ] && kill "$SND1_PID" 2>/dev/null || true
  [ -n "$SND2_PID" ] && kill "$SND2_PID" 2>/dev/null || true
fi

[ -n "$DIALOG_PID" ] && wait "$DIALOG_PID" 2>/dev/null || true
[ -n "$SND1_PID" ] && wait "$SND1_PID" 2>/dev/null || true
[ -n "$SND2_PID" ] && wait "$SND2_PID" 2>/dev/null || true
