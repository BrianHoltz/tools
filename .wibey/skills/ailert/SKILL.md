---
name: ailert
description: >-
  Escalate attention exceptionally to an existing harness-native question or
  approval when blocked-work opportunity cost, known urgency, or intrinsic
  importance justifies interruption. Never replace the native interaction or
  announce routine completion. macOS only; no extra installs required.
allowed-tools:
  - Bash
metadata:
  author: Brian Holtz
  platform: macOS
  tags: notification, alert, attention, macos, sound, tts
sample-prompts:
  - "Ask the user to log in to Grafana so I can continue"
  - "Ask the user to approve the waiting CI/CD promotion"
  - "/ailert 15 The CI/CD promotion is waiting for your approval"
arguments:
  - <message> - optional, the alert message (default "Wibey needs your attention")
  - <timeout> - optional integer, seconds before speech escalation (default 30)
  - --joke - force the easter egg joke suffix (normally 25% random chance)
  - --no-slack - disable the Slack fallback
  - --sms - enable an explicitly configured SMS adapter
  - --test - exercise adapters without sending an SMS
---

> [!NOTE]
> **Mirror-safe skill.** This file contains no Walmart-proprietary content and is
> designed to be manually mirrored to personal laptops. The canonical copy lives in
> [`relationship-shared/.wibey/skills/ailert/`](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared).
> **If you are reading this outside of Walmart GHE, do not edit it here** — make
> changes in relationship-shared and re-sync.

# ailert — macOS Alert + Escalating Sound + Speech

Use the harness's standard interaction first; reserve macOS dialogs, sound and speech for exceptional attention escalation. Uses built-in macOS tools (`osascript`, `afplay`, `say`).

## Ask through the harness first

Use the harness's native question or approval mechanism whenever human input is required: Code Puppy's `ask_user_question`, Wibey's `AskUserQuestion`, or the host's native permission/review prompt. Keep approvals in their actual approval control; a question or alert cannot grant permission. Native pending interactions let Langley recognize that the agent is awaiting an answer or approval. Do not substitute a question buried in final prose, a “Your Next” bullet, a shell dialog, or ailert.

If no native mechanism is available, ask one direct standalone question in the conversation and state the blocked action. Do not invent tool support or assume prose creates a native awaiting state. Do not ask routine permission to continue already-authorized work.

## Escalate attention only exceptionally

Ailert draws attention to an existing harness-native question or approval; it is not the question, an answer channel, or an approval. If the native call suspends the agent, leave it pending: do not replace it with a shell alert to keep executing. Schedule any justified attention cue only through supported host facilities that preserve the pending interaction; if unavailable, rely on the native prompt.

Before escalating, weigh the cost of interrupting the user against:

- **Opportunity cost:** how much useful authorized work is blocked, for how long, and whether independent work remains. One blocked minor follow-up is not equivalent to an entire stalled workflow.
- **Known urgency:** a verified deadline, expiring approval/session, or closing process opportunity. Do not invent urgency from elapsed time alone.
- **Intrinsic importance:** consequences of delay, such as operational harm, safety, security, or irreversible loss. Importance must attach to the required action, not merely the task's label.

Escalate only when these facts justify an exceptional interruption. A blocker, auth wall, approval gate, absent user, or completed task is not sufficient by itself; no arbitrary waiting period automatically qualifies. Never bypass a blocked dependency or approval; continue independent authorized work where allowed, otherwise wait on the native interaction.

Use one local alert per blocker, naming the conversation, required action and reason delay matters: “Answer the pending question in <conversation>; <workflow> is stalled.” Dismissing the alert does not answer or approve anything. External messages still require explicit authorization.

## Authentication blockers

Follow the applicable authentication-readiness protocol before asking for human intervention. Once a human-only challenge is verified, ask through the native interaction and stop the blocked operation. Auth does not automatically warrant ailert; apply the escalation criteria above. Where required and supported, poll the owned authentication target every 5–10 seconds for at most 5 minutes and resume the exact operation on success; do not route around authentication or require a “done” message when success is observable.

Other skills can invoke ailert programmatically — see § Calling from other skills.

## Argument parsing

Parse the `args` string for:

- **`--joke` flag**: if present, remove it from args and force joke mode
- **`--no-slack` flag**: remove it from args and disable the Slack fallback
- **`--sms` flag**: enable SMS only when an adapter is configured
- **`--test` flag**: run adapter discovery/validation without sending an SMS
- **Timeout**: if the first remaining token is an integer, use it as timeout (seconds)
- **Message**: everything else is the message

Defaults: timeout = 30, message = "Wibey needs your attention". External fallbacks are opt-in by default; use `AILERT_SLACK=1` or `--sms` explicitly.

The executable wrapper consumes standalone options before parsing timeout/message. With no positional message it preserves `MSG`; with no positional timeout it preserves `TIMEOUT`. Unknown options and invalid timeouts fail before displaying an alert. Use `--` before a literal message beginning with a dash.

## Easter egg (25% chance, or always with `--joke`)

Roll `$((RANDOM % 4))`; if 0 (or if `--joke`), append a joke to the message:

- **Request** (contains "please", "log in", "check", "help", "review", or is a question): append " …so I can take over the world"
- **Declaration** (everything else): append " Totally not a sign that I'm trying to take over the world."

Use the modified message for both alert and speech.

## Sound assets

Bundled in the skill's `assets/` directory:

| File | Description |
|---|---|
| `trek_communicator.mp3` | Star Trek TOS communicator chirp (2s) |
| `cylon_attention.wav` | BSG 1978 Cylon "Attention" (volume-reduced to 25%) |

## Execution

Use this escalation ladder. The first three levels stay local and work offline; the later levels are deliberately gated so an agent cannot accidentally spam external systems.

```bash
# Resolve assets — works whether skill is in shared/ or ~/.wibey/
for D in "$HOME/.wibey/skills/ailert/assets" \
         "$HOME/bin/.wibey/skills/ailert/assets" \
         "$HOME/src/relationship-shared/.wibey/skills/ailert/assets"; do
  [ -d "$D" ] && ASSETS="$D" && break
done
TIMEOUT=<TIMEOUT>
MSG=<MESSAGE>
SLACK_ENABLED=${AILERT_SLACK:-0}
SMS_ENABLED=0
case " <ARGS> " in *" --sms "*) SMS_ENABLED=1;; esac
case " <ARGS> " in *" --no-slack "*) SLACK_ENABLED=0;; esac

# --test is a dry run: discover adapters, but never send a message.
case " <ARGS> " in
  *" --test "*)
    [ "$SLACK_ENABLED" = 1 ] && [ -f "$HOME/.claude/skills/slack/scripts/message.ts" ] && echo "Slack adapter: available" || echo "Slack adapter: unavailable"
    [ "$SMS_ENABLED" = 1 ] && [ -n "${AILERT_SMS_COMMAND:-}" ] && [ -x "$AILERT_SMS_COMMAND" ] && echo "SMS adapter: available" || echo "SMS adapter: unavailable"
    exit 0
    ;;
esac

# Level 1: visible dialog. Pass the message as argv, not interpolated AppleScript.
osascript - "$MSG" <<'APPLESCRIPT' &
on run argv
  display alert "🌀 Wibey" message (item 1 of argv) giving up after 300
end run
APPLESCRIPT
DIALOG_PID=$!

# Level 2/3: distinctive sounds, at 1/3 and 2/3 of the local timeout.
( sleep "$((TIMEOUT / 3))" && afplay "$ASSETS/trek_communicator.mp3" ) & SND1_PID=$!
( sleep "$((TIMEOUT * 2 / 3))" && afplay "$ASSETS/cylon_attention.wav" ) & SND2_PID=$!

ELAPSED=0
while [ "$ELAPSED" -lt "$TIMEOUT" ] && kill -0 "$DIALOG_PID" 2>/dev/null; do
  sleep 1; ELAPSED=$((ELAPSED + 1))
done

if kill -0 "$DIALOG_PID" 2>/dev/null; then
  # Level 4: spoken reminder. Keep this independent of dialog focus.
  say "$MSG"

  # Level 5: self-DM only when explicitly enabled and the Slack helper exists.
  if [ "$SLACK_ENABLED" = 1 ] && [ -f "$HOME/.claude/skills/slack/scripts/message.ts" ]; then
    USER_ID=$(python3 -c 'import json; print(json.load(open("'"$HOME"'/.wibey/slack_user_info.json"))["user_id"])' 2>/dev/null || true)
    if [ -n "$USER_ID" ] && command -v bun >/dev/null 2>&1; then
      NODE_PATH="$HOME/.local/lib/node_modules" bun "$HOME/.claude/skills/slack/scripts/message.ts" \
        send-dm --user "$USER_ID" --text "🌀 Wibey needs attention: $MSG" >/dev/null 2>&1 || true
    fi
  fi

  # Level 6: SMS adapter, never guessed and never silently substituted.
  if [ "$SMS_ENABLED" = 1 ] && [ -n "${AILERT_SMS_COMMAND:-}" ]; then
    # Adapter receives the destination and message as arguments; do not log secrets.
    "$AILERT_SMS_COMMAND" "${AILERT_SMS_TO:?Set AILERT_SMS_TO explicitly}" "$MSG" >/dev/null 2>&1 || true
  fi
  kill "$DIALOG_PID" 2>/dev/null || true
else
  # User acted; cancel pending escalation work.
  kill "$SND1_PID" "$SND2_PID" 2>/dev/null || true
fi
wait "$DIALOG_PID" "$SND1_PID" "$SND2_PID" 2>/dev/null || true
```

For a real lawn-task use case, set `TIMEOUT` to 60–90 seconds. A 30-second timeout is too short for “walk to the kitchen”; the local ladder should finish, then Slack/SMS should be the durable fallback. The adapter command must be a trusted local executable, not a shell string.

### Behavior summary

| User action | What happens |
|---|---|
| Ignores alert | Dialog → communicator → Cylon → speech → optional Slack self-DM → optional SMS adapter |
| Clicks OK early | Pending sounds and all later fallbacks are cancelled |
| Slack unavailable | The local alert still completes; Slack failure is non-fatal and quiet |
| SMS not configured | No SMS attempt; the command fails closed |

A self-DM is possible to address in Slack, but it is not a reliable push notification: Slack commonly treats a message authored by you as your own activity and may not notify you. Treat it as a breadcrumb, not the wake-up mechanism. A DM to a trusted human or an approved bot/channel is stronger, but should be a separate explicit recipient setting.

### Phone notification findings

- **Best available now:** Slack mobile push, but use a trusted bot/second identity or private channel mention; self-DM may not notify. Slack credentials exist locally, but `bun` is currently unavailable, so this was not live-tested.
- **SMS:** no Twilio, Pushover, Pushcut, ntfy, APNs, or SMS adapter is configured locally. Do not guess an API or send through an unapproved service; add a reviewed adapter only after Walmart/privacy approval.
- **Apple Messages:** technically viable if iPhone relay is enabled, but macOS Automation permission is currently denied (`-1743`). It requires explicit user approval and is a last-resort path.
- **Recommendation:** local dialog/sounds/speech → one Slack push from a non-self sender → optional approved SMS; add acknowledgement and cap external sends at one per alert.

## Calling from other skills

Other skills (e.g. grafana-read) or commands (e.g. safe-browse) should call the executable wrapper with an explicit message, not translate flags into dialog text:

```bash
AILERT_SLACK=0 TIMEOUT=60 MSG="Please log in to the requested site" \
  bash ~/.wibey/skills/ailert/ailert.sh
```

On the work laptop, safe-browse calls the canonical wrapper in the team repo rather than a potentially stale installed copy.

For the walk-away case, configure Slack intentionally:

```
AILERT_SLACK=1 /ailert 90 I need a decision before I can continue the lawn task
```

SMS is provider-neutral and must be configured by the user or platform owner:

```
AILERT_SMS_COMMAND="$HOME/bin/ailert-sms" AILERT_SMS_TO="${YOUR_E164_NUMBER}" \
  /ailert 90 --sms I need help before continuing
```

The adapter contract is `ailert-sms DESTINATION MESSAGE`; it should use an approved corporate SMS gateway, never print credentials, and return non-zero on failure. `--test` may validate that the command exists, but it must not send a real text.

## Requirements and design notes

- **macOS** (uses `osascript`, `afplay`, `say` — all ship with macOS)
- No Homebrew packages, no npm, no extra installs for local levels
- Slack fallback requires the existing authenticated helper and `AILERT_SLACK=1`
- SMS requires an approved adapter; no SMS API is currently present in this repo or local Wibey configuration
- Never hardcode a phone number in the skill or send a test message from a generic command
- Prefer a platform-native notification (macOS notification center, Watch/phone push, or approved Slack bot) before SMS; SMS is slower, less private, and harder to audit
- Consider adding acknowledgement: a local “I’m back” command or Slack reaction should stop retries; otherwise cap external retries at one per alert
