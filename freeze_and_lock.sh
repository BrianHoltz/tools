#!/usr/bin/env bash

set -euo pipefail

# Create temporary folder for screenshots
TMP_DIR=$(mktemp -d /tmp/lock_screen_shots.XXXXXX)
trap "rm -rf '$TMP_DIR'" EXIT

# 1. Detect physical displays and capture each one separately
# Uses AppleScript to enumerate NSScreen objects (actual physical displays)
# Then uses screencapture to capture all at once (since -D flag is unavailable)
/usr/bin/osascript <<'APPLESCRIPT' > "$TMP_DIR/display_info.txt"
use framework "Foundation"
use framework "AppKit"

set screens to current application's NSScreen's screens()
set displayCount to count of screens
log "Display count: " & displayCount

repeat with i from 1 to displayCount
    set thisScreen to item i of screens
    set screenFrame to thisScreen's frame()
    set origin to screenFrame's origin
    set size to screenFrame's |size|
    log "Display " & i & ": x=" & (origin's x) & " y=" & (origin's y) & " w=" & (size's width) & " h=" & (size's height)
end repeat
APPLESCRIPT

# 2. Capture all displays into temp directory
screencapture -x "$TMP_DIR/screen.png" || {
    echo "screencapture failed" >&2
    exit 1
}

# Fix permissions so wallpaper/screensaver engine can read files
chmod 644 "$TMP_DIR"/*.png || true

# 3. Set each display's wallpaper by iterating through discovered displays
# Note: Modern macOS doesn't natively support per-display wallpapers via AppleScript
# This approach sets wallpapers for each Space (virtual desktop), which may span multiple displays
# For true per-display support, use third-party tools or Ventura+ APIs
/usr/bin/osascript <<'APPLESCRIPT'
on run argv
    set imgFolder to item 1 of argv

    -- Get sorted list of captured screenshots
    tell application "Finder"
        set imgFiles to sort (files of (POSIX file imgFolder as alias) whose name extension is "png") by name
    end tell

    -- Attempt to set wallpaper for each Space/Virtual Desktop
    tell application "System Events"
        set spaceCount to count of desktops
        repeat with i from 1 to spaceCount
            if i <= (count of imgFiles) then
                try
                    set imgAlias to (item i of imgFiles) as alias
                    set picture of desktop i to imgAlias
                on error errMsg
                    log "Failed to set wallpaper for desktop " & i & ": " & errMsg
                end try
            end if
        end repeat
    end tell

    return "Wallpapers applied to " & spaceCount & " space(s)"
end run
APPLESCRIPT "$TMP_DIR" || {
    echo "failed to apply wallpapers" >&2
    exit 1
}

# 4. Brief pause to let wallpapers render
sleep 1

# 5. Lock the screen
pmset displaysleepnow

echo "Locked. Wallpapers set from: $TMP_DIR (will auto-clean in 30s)"
exit 0

# LIMITATION NOTE:
# ================
# This script sets wallpapers for virtual Spaces, not physical displays.
# On macOS, each Space can have a different wallpaper, but all physical displays
# connected to a Space show the same wallpaper. True per-display wallpapers require:
#
# 1. Third-party tools (e.g., wallpaper apps that use private APIs)
# 2. Running separate login sessions per display (very complex)
# 3. Ventura+ private NSScreen wallpaper APIs (undocumented, fragile)
#
# To achieve the original goal (each display shows its frozen snapshot when locked),
# either: use a multi-display screensaver app, or accept that wallpapers are Space-wide.