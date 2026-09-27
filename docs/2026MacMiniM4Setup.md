# 2026 Mac mini M4 Setup

## SecuritySpy configuration

Migrate this camera configuration from the old Mac mini:

| Setting | Value |
| --- | --- |
| Address | `uuid:12010007-0500-1114-0302-ec71db036cbd` |
| ONVIF/HTTP port | Not configured |
| Use SSL for HTTP | Off |
| RTSP port | Not configured |
| Username | `admin` |
| Password | Retrieve securely from the old Mac mini; do not store in this document |
| Profile | `ONVIF` |
| Format | `RTSP (video and audio)` |
| Input or stream number | `1` |
| Recompress video data | Off |
| Recompress audio data | Off |

Use **Auto-Detect Profiles...** and **Auto-Detect Streams...** if SecuritySpy
does not populate the profile or stream automatically. The screenshot showed
the Device tab; verify the Setup, Triggers, Audio, Continuous Capture, Motion
Capture, and Actions tabs against the old Mac mini before considering the
migration complete.

The old configuration includes a camera password. It is intentionally omitted
from this repository document; transfer it through the old Mac mini or another
secure password-management channel.

### Continuous Capture

Configure the **Continuous Capture** tab as follows:

| Setting | Value |
| --- | --- |
| Capture movie continuously | Off |
| Create new | Every time continuous capture is armed |
| Movie upload | Don't upload |
| Capture images continuously | On |
| Image capture frequency | Every 60 seconds |
| Image upload destination | `MarketLiberal Cam archive` |
| Webcam image filename | `cam.jpg` |
| Webcam image upload frequency | Every 60 seconds |
| Webcam image upload destination | `MarketLiberal Cam` |
| Delete old files after | Not configured |

The capture-rate and playback-rate fields for movie capture are unused while
continuous movie capture is disabled.

### Upload Servers

Configure both servers on the **Uploads** tab:

| Server | Protocol | Server address | Username | Server path |
| --- | --- | --- | --- | --- |
| `MarketLiberal Cam` | FTP | `holtz.org` | `holtzorg` | `~/public_html/MarketLiberal/cam` |
| `MarketLiberal Cam archive` | FTP | `holtz.org` | `holtzorg` | `~/public_html/MarketLiberal/cam/archive` |

For both servers:

- Leave **S3 bucket** blank.
- Leave **Append camera name to path** unchecked.
- Leave **Append day folder name to path** unchecked.
- Retrieve the FTP password securely from the old Mac mini; do not store it in
  this document.
- Use the **Test** button after entering the credentials.

### Web

Configure the **Web** tab as follows:

| Setting | Value |
| --- | --- |
| HTTP web server | Enabled on port `9090` |
| HTTPS web server | Enabled on port `9091` |
| HTTP Internet access port forwarding | Auto-configure router (NAT-PMP / UPnP) |
| HTTPS Internet access port forwarding | Auto-configure router (NAT-PMP / UPnP) |
| Dynamic DNS name | `siliconvalley.viewcam.me` |
| HTTPS security level | `2 - Disable ciphers using RC4, MD5, DES` |
| Advertise via Bonjour | Off |
| Make movies Fast Start on-the-fly | On |
| Write log file of all connections | On |
| Allow Screen Control for Administrator accounts | Off |

Web accounts shown in the old configuration:

| Username | Permissions |
| --- | --- |
| `admin` | Administrator |
| `guest` | Custom |

Retrieve both web-account passwords securely from the old Mac mini; do not
store them in this document.

## Old Mac mini application inventory

The following items were present in `/Applications` and should be reviewed
for installation or data migration on the new Mac mini:

```text
/Applications/BZFlag-2.4.24.app
/Applications/Barrier.app
/Applications/Blackmagic Disk Speed Test.app
/Applications/Chrome Remote Desktop Host Uninstaller.app
/Applications/Fitbit Connect.app
/Applications/Folx.app
/Applications/Google Chrome.app
/Applications/Google Docs.app
/Applications/Google Drive.app
/Applications/Google Drive.localized
/Applications/Google Earth Pro.app
/Applications/Google Sheets.app
/Applications/Google Slides.app
/Applications/HIP2PClient.app
/Applications/Kiwix.app
/Applications/MenuMeters.app
/Applications/Minecraft.app
/Applications/Network Connect.app
/Applications/NicePlayer.app
/Applications/OmniDiskSweeper.app
/Applications/Origin.app
/Applications/PeakHour 4.app
/Applications/Plex HTPC.app
/Applications/Plex Media Server.app
/Applications/PokerStars.app
/Applications/Reolink.app
/Applications/Safari.app
/Applications/Seashore.app
/Applications/SecuritySpy.app
/Applications/Simple Comic.app
/Applications/Uninstaller for Vuze.app
/Applications/VLC.app
/Applications/Video Edit Pro - Video Trim.app
/Applications/Visual Studio Code.app
/Applications/Vuze.app
/Applications/World of Tanks Blitz.app
/Applications/YiHomeMacInt.app
/Applications/calibre.app
/Applications/gConnect.app
/Applications/komga-0.157.1.jar
/Applications/zoom.us.app
/Applications/Utilities
```

Prioritize migration review for SecuritySpy, Plex Media Server, Google Drive,
Reolink, YiHomeMacInt, HIP2PClient, Vuze, calibre, Kiwix, Visual Studio Code,
and any application with local libraries, recordings, plugins, or settings.
Some entries are uninstallers, support components, or Java archives rather
than standalone applications.

## Migration next steps

- The old Mac mini's Google Drive uploads were initially stuck because its
  system clock was three minutes fast. Correcting the clock restored network
  access; confirm both inventory files finish uploading.
- Review the inventories for Plex Media Server, calibre, Komga, SecuritySpy,
  Vuze, and any associated launch agents or library paths.
- Reinstall applications on the new Mac mini rather than copying application
  bundles when a current installer or Homebrew cask is available.
- Stop each server before copying its application state. Preserve databases,
  metadata, configuration, plugins, and library paths; do not blindly copy
  large media directories.
- Verify the new Mac mini can access the media and ebook/comic library
  locations before starting Plex, calibre, or Komga.
- Keep passwords, API keys, and server credentials out of this document and
  transfer them through a secure channel.

The pasted inventory has been reviewed and is stored at
`/Users/brian/Documents/old_mac_mini_inventory.txt`. Exact library roots still
need to be confirmed from each application's settings.

The bounded export script
[`docs/export_mac_mini_migration.sh`](export_mac_mini_migration.sh) writes
selected migration state to `/Volumes/Archive/MacMiniTransfers/`. It reports
each application and source path to stderr, measures selected directories with
`du`, and skips any selected directory larger than 100 MB. It deliberately
excludes media libraries, recordings, downloads, Plex metadata/thumbnails,
logs, caches, credentials in command output, and other raw data.

### New Mac mini agent handoff

The Copilot agent running in IntelliJ IDEA on the new Mac mini should take over
the migration from this point. The human operator remains on the old Mac mini
to run the export script and attach or copy the resulting transfer directory.

1. Open `~/src/tools/docs/2026MacMiniM4Setup.md` and
   `docs/export_mac_mini_migration.sh` from the real `~/src/tools` checkout.
2. Have the old Mac operator run the export script with
   `/Volumes/Archive/MacMiniTransfers/` as the destination. The script's
   progress log is `export_mac_mini_migration.log`; the inventory is
   `old_mac_mini_inventory.txt`. Both are expected to be saved in Google Drive
   alongside one another for the new agent to inspect.
3. Do not treat a completed script as proof that all state was copied. Review
   `manifest.txt`, `manifest.tsv`, and `large-or-skipped.tsv`. Anything over
   100 MB is intentionally skipped and requires an explicit decision.
4. Mount the transfer disk at the same `/Volumes/Archive` path on the new Mac,
   mount the external `media library` volume at the same path as the old Mac,
   and verify both before restoring anything.
5. Install fresh Apple-silicon versions of applications. Restore only the
   selected state from the transfer directory, starting with Plex.
6. Follow the Plex runbook below, preserving rollback copies and not deleting
   old state until playback and server identity are verified.
7. Continue with SecuritySpy, Calibre, Komga, Vuze, and camera applications
   only after Plex is stable. Ask the human before copying any skipped large
   directory or raw media.

The new agent must not reset the old Mac, delete source state, expose transfer
contents publicly, or commit credentials, tokens, databases, or copied
application data to the public tools repository.

## Inventory findings

The pasted inventory is from an Intel Mac mini (`Macmini7,1`) running macOS
12.7.6 with 8 GB of memory. The new M4 Mac should receive current Apple
silicon-compatible application versions rather than copied application bundles.

### Plex Media Server

Plex is actively running version `1.43.1.10611-1e34174b1` and is configured as a
login item. Stop Plex completely before migration. Its application state is:

```text
/Users/brian/Library/Application Support/Plex Media Server
/Users/brian/Library/Preferences/com.plexapp.plexmediaserver.plist
/Users/brian/Library/Application Support/Plex HTPC
/Users/brian/Library/Preferences/tv.plex.Plex HTPC.plist
```

The Plex state directory contains `Media`, `Metadata`, `Plug-in Support`,
`Plug-ins`, `Scanners`, `Thumbnails`, and `Codecs`. These are application state
and metadata, not necessarily the actual movie and television media. The
inventory also identifies likely media-related paths:

```text
/Users/brian/Movies/TV
/Users/brian/PlexTmp
```

Before copying, determine the library paths from Plex's server settings and
preserve the Plex database and metadata. Do not copy `Crash Reports`, caches,
or incomplete update directories unless needed.

#### Plex migration plan

This follows Plex's supported Mac-to-Mac migration method. Install a fresh
Apple-silicon Plex application, then transfer the complete Plex data directory
and the macOS preferences plist. Do not copy the Intel application bundle and
do not create a new Plex server if the existing server state can be restored.

Plex references:

- [Move an Install to Another System](https://support.plex.tv/articles/201370363-move-an-install-to-another-system/)
- [Plex Media Server data directory](https://support.plex.tv/articles/202915258-where-is-the-plex-media-server-data-directory-located/)
- [Backing Up Plex Media Server Data](https://support.plex.tv/articles/201539237-backing-up-plex-media-server-data/)

Assumption: the external volume named `media library` will be mounted on the
new Mac mini at exactly the same path used by the old Mac. This avoids changing
the absolute paths stored in the Plex database.

##### Prepare the old Mac

1. Confirm the external volume's exact mount path:

   ```sh
   mount | grep -i 'media library'
   ```

2. In Plex Web, open **Settings → Server → Library** and turn off
   **Empty trash automatically after every scan**. This prevents a missing
   volume during the move from removing library items.
3. Record every library name and exact folder path from the library's
   **Manage Library → Edit → Add folders** screen. Confirm that every path is
   on `media library` and will be identical on the M4.
4. Record a few verification-only settings. They should come across with the
   state transfer, so do not manually recreate them unless verification fails:

   - **Server version:** in Finder select `/Applications/Plex Media Server.app`,
     choose **Get Info**, and record the version. The inventory recorded
     `1.43.1.10611-1e34174b1`.
   - **Plex account:** identify the account shown under **Settings → Account**;
     do not write the account password into this document.
   - **Remote access:** open **Settings → Server → Remote Access** and record
     whether it is enabled, whether the connection is successful, the external
     port, and whether the router uses automatic or manual forwarding.
   - **Scheduled tasks:** open **Settings → Server → Scheduled Tasks** and
     record which task checkboxes are enabled and any maintenance schedule.
   - **Agents and metadata:** inspect **Settings → Server → Agents** if
     present, plus each library's metadata-agent and subtitle settings. Note
     only non-default choices.
   - **Custom metadata and subtitles:** spot-check a library and record any
     custom agents, preferred subtitle language, subtitle mode, or manually
     added artwork that must be verified after migration.
5. Stop Plex from its menu-bar item or Dock controls, then verify that no Plex
   processes remain:

   ```sh
   pgrep -afil 'Plex' || true
   ```

6. Make a safety copy of the complete Plex state directory to the external USB
   drive. Do not rely on Google Drive for this large, frequently changing
   directory:

   ```sh
   mkdir -p "/Volumes/TRANSFER/Plex Migration"
   ditto "$HOME/Library/Application Support/Plex Media Server" \
     "/Volumes/TRANSFER/Plex Migration/Plex Media Server"
   cp -p "$HOME/Library/Preferences/com.plexapp.plexmediaserver.plist" \
     "/Volumes/TRANSFER/Plex Migration/"
   ```

   Replace `TRANSFER` with the actual USB volume name. Copy the entire data
   directory, including its `Preferences.xml`, database, metadata, thumbnails,
   plugins, and library state. Do not omit subdirectories based only on their
   names.

7. Verify the transfer copy exists before changing anything else:

   ```sh
   ls -ld "/Volumes/TRANSFER/Plex Migration/Plex Media Server"
   ls -l "/Volumes/TRANSFER/Plex Migration/com.plexapp.plexmediaserver.plist"
   ```

   Keep this copy private; it contains server identity data and may contain
   sensitive account information.

##### Install Plex on the M4

1. Mount `media library` at the exact path used by the old Mac and verify all
   media directories are readable before installing or starting Plex.
2. Install the current Plex Media Server for Apple silicon. Do not copy
   `/Applications/Plex Media Server.app` from the Intel Mac.
3. If Plex starts a setup wizard, exit it without creating or configuring a
   replacement server. If Plex was launched, sign out under **Settings →
   Server → General** and quit it completely.
4. Confirm no Plex processes remain before replacing application state:

   ```sh
   pgrep -afil 'Plex' || true
   ```

##### Restore Plex state

1. Rename any newly created state directory as a rollback copy; do not delete
   it:

   ```sh
   mv "$HOME/Library/Application Support/Plex Media Server" \
     "$HOME/Library/Application Support/Plex Media Server.new-install"
   ```

2. Copy the complete old `Plex Media Server` directory into
   `~/Library/Application Support/` and restore the macOS preference file:

   ```sh
   ditto "/Volumes/TRANSFER/Plex Migration/Plex Media Server" \
     "$HOME/Library/Application Support/Plex Media Server"
   cp -p "/Volumes/TRANSFER/Plex Migration/com.plexapp.plexmediaserver.plist" \
     "$HOME/Library/Preferences/"
   ```

3. Ensure the restored files belong to the logged-in user:

   ```sh
   chown -R "$USER":staff \
     "$HOME/Library/Application Support/Plex Media Server"
   chown "$USER":staff \
     "$HOME/Library/Preferences/com.plexapp.plexmediaserver.plist"
   ```

4. Reboot the M4 before starting Plex. macOS can retain preference files in
   memory, and Plex's migration instructions specifically call for a reboot.
5. Start Plex and wait for the server to become available locally before
   changing any settings.
6. Verify that the existing libraries appear with their old names, posters,
   watched status, collections, playlists, users, and server settings. Confirm
   that media paths resolve without creating duplicate libraries.
7. Verify the recorded remote-access, scheduled-task, agent, metadata, and
   subtitle settings. Test playback from at least one movie and one television
   episode, then check subtitles, artwork, and remote access.
8. If the media paths do not resolve, edit each library and add the identical
   `media library` path. Scan the library, confirm matching rather than
   duplicate items, and remove any obsolete path only after verification.
9. Re-enable **Empty trash automatically after every scan** and any scheduled
   maintenance only after the libraries and media volume are confirmed healthy.
   Keep the `.new-install` rollback directory and USB transfer copy until the
   migrated server has been stable.

##### Plex rollback

If the restored server does not start or the database is damaged, stop Plex,
move the restored directory aside, and put
`Plex Media Server.new-install` back in place. Do not run database repair or
delete files until the original state directory and the transfer copy are
both preserved.

### Calibre

Calibre is installed and has both application preferences and a configuration
directory:

```text
/Applications/calibre.app
/Users/brian/Library/Preferences/calibre
/Users/brian/Library/Preferences/net.kovidgoyal.calibre.plist
```

The inventory does not identify the ebook library's actual folder. Locate that
library from Calibre's current library selector before migration; do not infer
it from the application or preference paths.

### Komga

Komga is represented by:

```text
/Applications/komga-0.157.1.jar
/Users/brian/.komga
```

The inventory did not capture a running Komga process or the comic-library
root. Inspect `.komga` for the database and configuration, and identify the
library path from the Komga web interface or service configuration before
copying. Keep the same Java-compatible Komga version initially, then upgrade
only after the migrated instance is working.

### SecuritySpy migration findings

SecuritySpy is installed, configured as a login item, and has state in all of
these locations:

```text
/Applications/SecuritySpy.app
/Users/brian/SecuritySpy
/Users/brian/Library/Application Support/SecuritySpy
/Users/brian/Library/Preferences/com.bensoftware.SecuritySpy.plist
/Users/brian/Library/Preferences/SecuritySpy Preferences v77
/Users/brian/Library/Preferences/SecuritySpy Preferences v78
/Users/brian/Library/Preferences/SecuritySpy Preferences v79
/Users/brian/Library/Preferences/SecuritySpy Preferences v80
/Users/brian/Library/Preferences/SecuritySpy Preferences v81
/Users/brian/Library/Preferences/SecuritySpy Upload Queue
```

`~/SecuritySpy` contains `Captured Files`, `Backup Files`, `Scripts`, `Web`,
`Sounds`, and `Log.txt`. Preserve configuration and scripts; decide separately
whether captured files and logs are needed. The credentials documented above
still need to be transferred securely.

### Other migration-relevant findings

- Vuze has state at `~/Library/Application Support/Vuze`,
  `~/Library/Preferences/com.azureus.vuze.plist`, and downloads may be under
  `~/Vuze Downloads`.
- Reolink has state under `~/Library/Application Support/reolink`,
  `~/Library/Application Support/com.reolink.app.client`, and recordings under
  `~/Movies/reolink`.
- Google Drive has multiple login items and containers; configure it fresh on
  the new Mac using the documented mirrored-My-Drive design.
- The old Mac has login agents for Google, Chrome Remote Desktop, Fitbit, EA
  Origin, and other utilities. Recreate only the agents belonging to software
  intentionally migrated.
