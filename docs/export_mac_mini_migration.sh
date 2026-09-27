#!/bin/bash

set -u
umask 077

DEST_ROOT="/Volumes/Archive/MacMiniTransfers"
MAX_KB=102400

log() {
  printf '[%s] %s\n' "$(date '+%H:%M:%S')" "$*" >&2
}

section() {
  printf '\n=== %s ===\n' "$*" >&2
}

copy_file() {
  label="$1"
  source="$2"
  relative="$3"
  destination="$DEST_ROOT/$relative"

  log "$label: checking $source"

  if [ ! -f "$source" ]; then
    log "$label: not present; skipping"
    return 0
  fi

  mkdir -p "$(dirname "$destination")"
  log "$label: copying $source"
  cp -p "$source" "$destination"
  printf '%s\t%s\n' "$label" "$source" >> "$DEST_ROOT/manifest.tsv"
}

copy_dir_if_small() {
  label="$1"
  source="$2"
  relative="$3"
  destination="$DEST_ROOT/$relative"

  log "$label: checking $source"

  if [ ! -d "$source" ]; then
    log "$label: not present; skipping"
    return 0
  fi

  log "$label: measuring selected state directory with du"
  size_kb="$(du -sk "$source" 2>/dev/null | awk '{print $1}')"

  if [ -z "$size_kb" ]; then
    log "$label: could not determine size; skipping"
    return 0
  fi

  size_mb=$((size_kb / 1024))
  log "$label: size is approximately ${size_mb} MB"

  if [ "$size_kb" -gt "$MAX_KB" ]; then
    log "$label: OVER 100 MB; not copying automatically"
    printf '%s\tSKIPPED_OVER_100MB\t%s\t%s MB\n' \
      "$label" "$source" "$size_mb" >> "$DEST_ROOT/large-or-skipped.tsv"
    return 0
  fi

  mkdir -p "$(dirname "$destination")"
  log "$label: copying selected state directory"
  ditto "$source" "$destination"
  printf '%s\t%s\t%s MB\n' \
    "$label" "$source" "$size_mb" >> "$DEST_ROOT/manifest.tsv"
}

if [ ! -d "/Volumes/Archive" ]; then
  echo "ERROR: /Volumes/Archive is not mounted." >&2
  exit 1
fi

if [ ! -d "$DEST_ROOT" ]; then
  echo "ERROR: destination does not exist: $DEST_ROOT" >&2
  exit 1
fi

mkdir -p "$DEST_ROOT"
chmod 700 "$DEST_ROOT"

section "Migration export"
log "Destination: $DEST_ROOT"
log "Directories larger than 100 MB will be measured and skipped"

{
  echo "Mac mini migration export"
  date
  echo "Source host: $(scutil --get ComputerName 2>/dev/null || hostname)"
  echo "macOS: $(sw_vers -productVersion 2>/dev/null || true)"
  echo "Architecture: $(uname -m)"
  echo "Size limit: 100 MB per selected state directory"
} > "$DEST_ROOT/manifest.txt"

: > "$DEST_ROOT/manifest.tsv"
: > "$DEST_ROOT/large-or-skipped.tsv"

section "Plex Media Server"
log "Raw Plex media directories are intentionally excluded"
log "Raw Plex metadata and thumbnails are intentionally excluded from this config export"

copy_file \
  "Plex database" \
  "$HOME/Library/Application Support/Plex Media Server/Database/com.plexapp.plugins.library.db" \
  "Plex/Database/com.plexapp.plugins.library.db"

copy_file \
  "Plex database WAL" \
  "$HOME/Library/Application Support/Plex Media Server/Database/com.plexapp.plugins.library.db-wal" \
  "Plex/Database/com.plexapp.plugins.library.db-wal"

copy_file \
  "Plex database SHM" \
  "$HOME/Library/Application Support/Plex Media Server/Database/com.plexapp.plugins.library.db-shm" \
  "Plex/Database/com.plexapp.plugins.library.db-shm"

copy_file \
  "Plex Preferences.xml" \
  "$HOME/Library/Application Support/Plex Media Server/Preferences.xml" \
  "Plex/Preferences.xml"

copy_file \
  "Plex macOS preferences plist" \
  "$HOME/Library/Preferences/com.plexapp.plexmediaserver.plist" \
  "Plex/com.plexapp.plexmediaserver.plist"

copy_file \
  "Plex HTPC preferences plist" \
  "$HOME/Library/Preferences/tv.plex.Plex HTPC.plist" \
  "Plex/tv.plex.Plex HTPC.plist"

copy_dir_if_small \
  "Plex plug-in support" \
  "$HOME/Library/Application Support/Plex Media Server/Plug-in Support" \
  "Plex/Plug-in Support"

copy_dir_if_small \
  "Plex plug-ins" \
  "$HOME/Library/Application Support/Plex Media Server/Plug-ins" \
  "Plex/Plug-ins"

section "SecuritySpy"
log "Captured video, backup files, and logs are intentionally excluded"

copy_file \
  "SecuritySpy main preferences" \
  "$HOME/Library/Preferences/com.bensoftware.SecuritySpy.plist" \
  "SecuritySpy/com.bensoftware.SecuritySpy.plist"

copy_file \
  "SecuritySpy Preferences v82" \
  "$HOME/Library/Preferences/SecuritySpy Preferences v82" \
  "SecuritySpy/SecuritySpy Preferences v82"

copy_file \
  "SecuritySpy upload queue" \
  "$HOME/Library/Preferences/SecuritySpy Upload Queue" \
  "SecuritySpy/SecuritySpy Upload Queue"

copy_dir_if_small \
  "SecuritySpy application support" \
  "$HOME/Library/Application Support/SecuritySpy" \
  "SecuritySpy/Application Support"

copy_dir_if_small \
  "SecuritySpy scripts" \
  "$HOME/SecuritySpy/Scripts" \
  "SecuritySpy/Scripts"

copy_dir_if_small \
  "SecuritySpy web files" \
  "$HOME/SecuritySpy/Web" \
  "SecuritySpy/Web"

copy_dir_if_small \
  "SecuritySpy sounds" \
  "$HOME/SecuritySpy/Sounds" \
  "SecuritySpy/Sounds"

section "Calibre"
log "The actual Calibre ebook library is intentionally excluded until confirmed"

copy_dir_if_small \
  "Calibre preferences directory" \
  "$HOME/Library/Preferences/calibre" \
  "Calibre/Preferences/calibre"

copy_file \
  "Calibre preferences plist" \
  "$HOME/Library/Preferences/net.kovidgoyal.calibre.plist" \
  "Calibre/net.kovidgoyal.calibre.plist"

section "Komga"
log "Comic files are intentionally excluded"

copy_dir_if_small \
  "Komga application state" \
  "$HOME/.komga" \
  "Komga/.komga"

copy_file \
  "Komga launcher archive" \
  "/Applications/komga-0.157.1.jar" \
  "Komga/komga-0.157.1.jar"

section "Vuze"
log "Vuze downloads are intentionally excluded"

copy_dir_if_small \
  "Vuze application support" \
  "$HOME/Library/Application Support/Vuze" \
  "Vuze/Application Support/Vuze"

copy_file \
  "Vuze preferences" \
  "$HOME/Library/Preferences/com.azureus.vuze.plist" \
  "Vuze/com.azureus.vuze.plist"

section "Reolink, YiHome, and HIP2P"
log "Camera recordings are intentionally excluded"

copy_dir_if_small \
  "Reolink application support" \
  "$HOME/Library/Application Support/reolink" \
  "Cameras/Reolink/reolink"

copy_dir_if_small \
  "Reolink client support" \
  "$HOME/Library/Application Support/com.reolink.app.client" \
  "Cameras/Reolink/com.reolink.app.client"

copy_file \
  "Reolink preferences" \
  "$HOME/Library/Preferences/com.reolink.app.plist" \
  "Cameras/Reolink/com.reolink.app.plist"

copy_dir_if_small \
  "YiHome container" \
  "$HOME/Library/Containers/com.xiaoyi.yihome.international.mac" \
  "Cameras/YiHome/container"

copy_dir_if_small \
  "HIP2P container" \
  "$HOME/Library/Containers/com.hichip.HIP2PForMac" \
  "Cameras/HIP2P/container"

section "Selected utility preferences"

copy_dir_if_small \
  "Barrier application support" \
  "$HOME/Library/Application Support/barrier" \
  "Utilities/Barrier/Application Support"

copy_file \
  "Barrier preferences" \
  "$HOME/Library/Preferences/com.github.Barrier.plist" \
  "Utilities/Barrier/com.github.Barrier.plist"

copy_dir_if_small \
  "PeakHour application support" \
  "$HOME/Library/Application Support/PeakHour" \
  "Utilities/PeakHour/Application Support"

copy_dir_if_small \
  "PeakHour 4 application support" \
  "$HOME/Library/Application Support/PeakHour 4" \
  "Utilities/PeakHour 4/Application Support"

copy_file \
  "PeakHour preferences" \
  "$HOME/Library/Preferences/com.digitician.peakhour4.plist" \
  "Utilities/PeakHour/com.digitician.peakhour4.plist"

copy_file \
  "MenuMeters preferences" \
  "$HOME/Library/Preferences/com.yujitach.MenuMeters.plist" \
  "Utilities/MenuMeters/com.yujitach.MenuMeters.plist"

section "Inventory and launch-item manifest"

copy_file \
  "Previously collected inventory" \
  "$HOME/Documents/old_mac_mini_inventory.txt" \
  "Inventory/old_mac_mini_inventory.txt"

log "Recording login items and launch-agent paths"
{
  echo "=== Login items ==="
  osascript -e 'tell application "System Events" to get the name of every login item' 2>/dev/null || true
  echo
  echo "=== User launch agents ==="
  find "$HOME/Library/LaunchAgents" -maxdepth 1 -type f -print 2>/dev/null | sort
  echo
  echo "=== System launch agents ==="
  find /Library/LaunchAgents /Library/LaunchDaemons \
    -maxdepth 1 -type f -print 2>/dev/null | sort
} > "$DEST_ROOT/Inventory/login-items-and-agents.txt"

section "Finished"
log "Migration export complete: $DEST_ROOT"
log "Review these files before moving anything to the new Mac:"
log "  $DEST_ROOT/manifest.txt"
log "  $DEST_ROOT/manifest.tsv"
log "  $DEST_ROOT/large-or-skipped.tsv"
