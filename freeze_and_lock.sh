#!/usr/bin/env bash

set -euo pipefail

# Create temporary folder for screenshots
TMP_DIR=$(mktemp -d /tmp/lock_screen_shots.XXXXXX)
trap "rm -rf '$TMP_DIR'" EXIT

# 1. Capture all displays (one file per display)
# -x: disable camera shutter sound
# -D: specify display(s) — captures all by default
screencapture -x "$TMP_DIR/screen.png" || {
    echo "screencapture failed" >&2
    exit 1
}

# Fix permissions so wallpaper engine can read files
chmod 644 "$TMP_DIR"/*.png || true

# 2. Apply screenshots as wallpapers via AppleScript
# Key: sort files numerically/lexicographically to match display order
# Then pair each file to its display index
/usr/bin/osascript <<'APPLESCRIPT'
on run argv
    set imgFolder to item 1 of argv
    tell application "Finder"
        set imgFiles to sort (files of (POSIX file imgFolder as alias) whose name extension is "png") by name
    end tell

    tell application "System Events"
        set dCount to count of desktops
        repeat with i from 1 to dCount
            if i <= (count of imgFiles) then
                try
                    set imgAlias to (item i of imgFiles) as alias
                    set picture of desktop i to imgAlias
                end try
            end if
        end repeat
    end tell
end run
APPLESCRIPT "$TMP_DIR" || {
    echo "failed to apply wallpapers" >&2
    exit 1
}

# 3. Brief pause to let wallpapers render
sleep 1

# 4. Lock the screen
pmset displaysleepnow

exit 0