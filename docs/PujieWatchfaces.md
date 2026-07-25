# Pujie watchfaces

## Search summary

Searched `~/src` first, then expanded across all of `$HOME`.

- No file name or file content match for the literal string `infovore` was found in the JS sources.
- The name **Infovore** does appear in personal notes/logs, which tie that watchface to the Pujie JS files below.

## Located JS files and backups

### `~/src/PujieUtils.js`

Main custom Pujie helper script currently found in home.

This is your custom JS library that you upload into the watchface to run on the **Pixel 1** watch. The newer **Pixel 3** setup does not allow this same custom-library machinery.

What it contains:

- Pujie meta-variable date/time shim via `[year]`, `[month_n]`, `[day_n]`, `[h24]`, `[m]`, `[s]`, `[ms]`, `[gmt_offset]`
- home location constants: `37.3813, -122.1447`
- distance and bearing to a target
- cached solar-system hour-angle table for Moon, Mercury, Venus, Mars, Jupiter, Saturn
- sunrise/sunset calculation
- exported values:
  - `PujieUtils.SolarSystem.Sunrise`
  - `PujieUtils.SolarSystem.Sunset`
  - `PujieUtils.SolarSystem.DawnHourAngle`
  - `PujieUtils.SolarSystem.DuskHourAngle`

### `~/src/PujieUtils.js.bak`

Backup of `PujieUtils.js`.

Observed differences vs current `PujieUtils.js`:

- older comments/debug remnants inside `hourAngleOf`
- older dawn/dusk representation:
  - `DawnHourAngle = 12 - (Sun_dayLength/2)`
  - `DuskHourAngle = 12 + (Sun_dayLength/2)`
- current file instead stores sunrise/sunset and uses:
  - `DawnHourAngle = 24 - (Sun_dayLength/2)`
  - `DuskHourAngle = Sun_dayLength/2`

### `~/src/PujieUtils20231125.js`

Dated snapshot from `2023.11.25`.

Characteristics:

- alternate implementation style using `global`
- appears to be an experiment/prototype around astronomy calculations
- likely related to the later cached hour-angle work mentioned in logs on `2023.11.30`

### `~/src/DeathClock.js`

Custom Pujie text automation script for **heartbeats until death**.

Current script:

- uses Pujie meta-variables
- counts heartbeats until `2052.03.30`
- returns a rounded string result for display

### `~/src/DeathClock.js~`

Backup/older draft of `DeathClock.js`.

Observed differences vs current `DeathClock.js`:

- older rough draft used modern JS (`const`, `let`)
- printed to console instead of returning a display string
- had a likely typo/bug: `h24l`
- did not yet adapt cleanly to Pujie meta-variables

## Related development source

### `~/src/PujieUtils/src/astronomy_lite.js`
### `~/src/PujieUtils/dist/astronomy_lite.js`

Standalone astronomy workbench/package.

Evidence:

- package exists at `~/src/PujieUtils/`
- package name: `pujieutils`
- files include `HourAngle`
- they hard-code the same home coordinates used in the watchface JS

This looks like the source/prototyping area behind the later watchface-friendly cached calculations.

## Notes that identify the watchface as "Infovore"

**Infovore** was the name of the custom watchface you designed in `2023`.

### `~/My Drive/HoltzBot/FamilyLogs.md`
### `~/My Drive/HoltzBot/Log Family.txt`

Timeline entries:

- `2023.11.12` — "BH starts creating Puji watchface."
- `2023.11.14` — `BH "Infovore" watchface: death clock, home bearing, unix time, etc.`
- `2023.11.30` — `BH implements cached solar system hour angle calculation for Pujie WearOS watchface.`
- `2023.12.05` — `BH adds to Infovore Pujie watchface: sun/moon/planets, sunrise/set times+horizons`

These line up well with:

- `DeathClock.js` for the death-clock feature
- `PujieUtils.js` for home bearing, Unix-time/date plumbing, and later astronomy additions

### `~/My Drive/Journal.txt`

Feature list for **Infovore**:

- distance and direction to home
- altitude and latest city
- lat/long and Unix time
- date and time
- rain, wind, temps low/high/current
- steps, heart rate low/high/current
- heartbeats until death (`2052.03.30` U.S. solar eclipse)
- battery % for watch and phone

Not all of these features appear in the recovered standalone JS backups, which is expected because much of the watchface uses built-in Pujie functionality exposed through its JS/meta-variable API. Relevant logic may therefore live in:

- Pujie designer configuration rather than standalone JS
- other unrecovered snippets
- Automate/Complication text expressions

## Attached screenshot clue (`2026.07.19`)

The screenshot shows a Pujie **Automate text** expression that appears to implement or display Unix time:

```js
var secondsSinceEpoch =
  computeSecondsSinceEpoch([year], [month_n], [day_n], [h24], [m], [s], [gmt_offset]);
return [com_evnt] == "No event"
  ? secondsSinceEpoch.toLocaleString()
  : [com_evnt];
```

The visible helper function starts with non-leap-year month lengths, so this looks like a custom seconds-since-epoch formatter inside Pujie text automation.

This screenshot matches the `2023.11.14` note that Infovore included **Unix time**.

## Pujie built-in Sun/Moon objects (`2026.07.24`)

Current conclusion: the **Pujie-supplied** sun/moon rise/set values appear accurate enough to trust directly.

Implication:

- custom/inlined astronomy rise/set calculations are **not needed** for current watchface behavior
- `PujieUtils.js` should remain focused on cached body-cycle/orrery support and other custom helpers
- watchface expressions should prefer `[sun_obj]` / `[moon_obj]` for rise/set/event display

### `[moon_obj]`

Observed fields in the Pujie Moon object:

- `next_rise`
- `next_set`
- `rise`
- `set`
- `culmination`
- `first_quarter`
- `altitude`
- `azimuth`
- `distance`
- `fraction`
- `phase`
- `closest_phase`
- `isSet`
- `moonlight_min`
- `min_to_rise`
- `min_to_set`

Observed event-object structure (used by `next_rise`, `next_set`, `rise`, `set`, `culmination`, `first_quarter`, and likely similar event fields):

- `day`
- `month`
- `year`
- `hour24`
- `hour12`
- `hour`
- `minutes`
- `ampm`
- `unix_minutes`
- `time`

Observed Moon values from screenshots:

- `next_rise.time = "17:07"`
- `next_set.time = "2:17"`
- `rise.time = "17:07"`
- `set.time = "1:34"`
- `altitude = -3.69`
- `azimuth = 122.03`
- `distance = 405286.0732213476`
- `fraction = 0.82`
- `phase = 129.12`
- `closest_phase = "waxing gibbous"`
- `isSet = true`
- `moonlight_min = 508`
- `min_to_rise = 22`
- `min_to_set = 572`

Interpretation:

- `next_rise` / `next_set` are the next upcoming crossing events, even if they occur on different calendar days.
- `rise` / `set` appear to be the rise/set events associated with the current local day/context, not necessarily the same as the next upcoming event.
- `azimuth` and `altitude` are directly useful for “where is it now?” style watchface semantics.
- `phase` is numeric phase angle; `closest_phase` is the human-readable bucket.

### `[sun_obj]`

Observed fields in the Pujie Sun object:

- `next_rise`
- `next_set`
- `rise`
- `set`
- `culmination`
- `altitude`
- `azimuth`
- `distance`

Observed event-object structure matches Moon event objects:

- `day`
- `month`
- `year`
- `hour24`
- `hour12`
- `hour`
- `minutes`
- `ampm`
- `unix_minutes`
- `time`

Observed Sun values from screenshots:

- `next_rise.time = "6:07"`
- `next_set.time = "20:23"`
- `rise.time = "6:06"`
- `set.time = "20:23"`
- `culmination.time = "13:15"`
- `altitude = 40.95`
- `azimuth = 264.19`

Interpretation:

- Pujie’s Sun rise/set times align with the values you expect on-device.
- `culmination` is especially useful if you want the orrery semantics to center on daily-cycle milestones instead of pure compass direction.
- The one-minute difference between `rise` and `next_rise` in the screenshot is a reminder that `next_*` and same-day event fields are related but not identical concepts.

## Orrery daily-cycle semantics (`2026.07.25`)

Desired meaning of the watchface body position:

- `0deg` = culmination / highest daily crossing
- `90deg` = setting
- `180deg` = anti-culmination / lowest daily crossing
- `270deg` = rising

Implications:

- **Azimuth is not the right driver** for the orrery ring. Azimuth answers “which compass direction is the body in right now?”, not “where is it in its rise/culminate/set cycle?”
- **Raw hour angle is also not sufficient** as the final display angle. `15 * hourAngle` correctly gives `0deg` at culmination and `180deg` at anti-culmination, but it only puts rise/set at `270deg/90deg` for bodies whose rise/set happen exactly 6 hours from transit. The Moon and planets do not obey that simplification.
- The right display quantity is a derived **cycle angle**: keep hour angle as the physical state variable, then remap it through the body's actual rise/set anchors for that date.

Current implementation direction:

- keep cached per-body `hourAngles` as the base “hours since culmination” table
- add cached per-body `setHourAngles` so each body/date has its own setting anchor
- derive `riseHourAngle = 24 - setHourAngle`
- expose `cycleAngleOf(body, localDate)` / `orreryAngleOf(...)` to map the body into the watchface semantic above
- expose `sunCycleAngleOf([sun_obj], nowDate)` / `sunCycleAngleOfNow()` so the Sun can use the same semantic without embedding a large Pujie expression
- continue using Pujie-native `[sun_obj]` / `[moon_obj]` for displayed Sun/Moon rise/set text and event metadata

This cleanly separates two ideas that were previously blurred together:

- **astronomical state**: hour angle, azimuth, altitude, rise/set events
- **watchface display semantic**: one ring angle whose quadrants mean culminate / set / anti-culminate / rise

## Other related artifact

### `~/My Drive/Pujie Watch Face Baseline Features V2.gdoc`

Google Drive shortcut/stub. Current contents expose:

- Google doc id: `1XHfhAW6AmrtjNeoZc95N8S00Rylz_Jpwf8C57EkDvnw`
- owner email: `brianholtz1965@gmail.com`

Probable URL:

<https://docs.google.com/document/d/1XHfhAW6AmrtjNeoZc95N8S00Rylz_Jpwf8C57EkDvnw/edit>

Additional evidence recovered locally:

- Chrome Docs IndexedDB cache confirms the same doc id and title
- unauthenticated direct export of the doc text returned HTTP 401
- authenticated browser-session export succeeded via a dedicated Chrome CDP profile

Recovered document contents (revised):

## Revised watch face design (top -> bottom)

### Top crescent (astronomy)

- **Left (sun, orange)**: top = sunset, bottom = sunrise, animated sun glyph traveling the perimeter.
- **Center**: altitude (if available). Future possibility: heading/distance-to-home if update reliability improves.
- **Right (moon, white)**: top = second moon event of the day (rise/set), bottom = first moon event of the day (rise/set), animated moon glyph traveling the perimeter, phase-aware if possible.

### Calendar band (full width)

- next calendar event (replaces the old sunrise/sunset header row)

### Center time block

- large current time
- seconds to the right (watch only)
- time zone label (`PST`/`PDT`) below or adjacent

### Bottom information grid

- **Activity (red)**: top = today's steps, mid = yesterday's steps, bottom = two days ago steps
- **Heart rate (red)**: top = daily high, mid = current, bottom = daily low
- **Current weather**: top = current temperature, mid = reserved blank, bottom = `°F` legend
  - current temperature color is dynamic: use forecast-high color when closer to today's high; forecast-low color when closer to today's low
- **Forecast columns** (`Today`, `Tomorrow`, `+2 Days`) share the same 3-row pattern:
  - top = forecast high
  - mid = rainfall or wind
  - bottom = forecast low

### Weather legend triangle (right of forecast grid)

Reserved for units/legend via conditional visibility:

- top: `°F` (temperature color)
- middle: `MPH` (white), shown only when middle-row values are wind
- bottom: `"` (cyan), shown only when middle-row values are rainfall

### Bottom edge

- watch battery %
- phone battery %
- center icon area may be obscured by Wear OS notification overlays

### Color scheme

- sun / warm / forecast highs: orange
- forecast lows: deep blue
- current temperature: dynamic orange or deep blue (based on proximity to today's high/low)
- rainfall: cyan
- wind: white
- heart/activity: red
- moon: white

### Deferred or removed

- location name
- GPS heading (too stale)
- distance to home (too stale)
- calories
- solar noon (derivable from sunrise/sunset)
- current weather conditions (until provider reliability improves)
