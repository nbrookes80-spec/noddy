# TunerToolPro for Android (early build)

A phone version of the Shift Points calculator and Dyno simulation, with an OBD-II scanner and a
read-only link to a scan adapter. Demo mode runs the whole scanner with no adapter and no car.

- **Shift Points.** Change any input or gear ratio and all four shift tables (upshift, downshift,
  TCC unlock, TCC lock) recalculate at once. It uses the same calculation code as the desktop app.
- **Dyno.** Shows a power and torque curve and a simulated launch to the quarter mile. With no
  file loaded, the curve is estimated from the Shift Points settings (RWHP, shift RPM, idle RPM).
  Load a dyno CSV (`rpm,hp,tq`) with **Load dyno CSV** to use your own curve. The launch
  re-runs whenever a Shift Points value changes.
- **Sliders.** Each shift input has a slider and a typed box that stay in step.
- **Scan.** The VE CALAIS Scanner's live dashboard and PID catalogue (111 Mode 01 and GM Mode 22 PIDs),
  four readings to a page with a bar or a short graph, a stored trouble code read (Mode 03), and a log
  of what was sent. Readings marked unconfirmed have not been checked against a real vehicle.
- **Demo mode.** A switch on the Link tab. The Scan and Link screens then show a simulated drive
  (idle, a launch through four gears, a cruise, a stop) and sample trouble codes. Nothing is sent to
  any adapter, so it works anywhere. The header chip shows DEMO, LIVE or OFFLINE.
- **Link.** Connects to an ELM327-compatible adapter over **Bluetooth** (paired first in phone
  settings) or **Wi-Fi** (the adapter's own network, usually 192.168.0.10 port 35000). It shows
  engine speed, vehicle speed, throttle and coolant temperature once a second.

The link only sends adapter set-up commands, reads of PIDs in the scanner catalogue (Mode 01, and GM
Mode 22 through the engine 7E0 or transmission 7E2 address), a Mode 03 stored-code read, and a header
switch to one of four known addresses. It never clears codes, runs tests, sweeps unlisted Mode 22
addresses, or writes to the controller. `link/obd.py` refuses any other command before it is sent.
The original scanner's Clear codes (Mode 04), PID sweep and enhanced code services are not included.

## Status

| Part | State |
|---|---|
| Shift calculation | Same code as the desktop app. Unit tests cover live recalculation. |
| Scanner catalogue | Generated from the VE CALAIS Scanner source (`tools/gen_pid_table.py`). Formulas are tested; 'probable' PIDs are unconfirmed on a real vehicle. |
| Demo mode | Simulated drive, tested for range and gear order. Not a measurement of any car. |
| Wi-Fi link | Tested against a simulated ELM327 over TCP, including a Mode 22 read and a code read. Not yet tried with a real adapter. |
| Bluetooth link | Written, not tested with a real adapter. Asks for the Nearby devices permission on Android 12 and newer. |
| Dyno and launch simulation | Same engine as the desktop Dyno & Drag tab. Not yet checked against a measured dyno run. |
| CSV loading | Dyno CSV loads on a desktop. On a phone it uses the system file picker (plyer), which is untested on a device. |
| Other desktop tabs | Not ported yet (Vehicle, Pressure and Timing, Datalog, XDF, BCT, AI). |
| Vehicle validation | None. Check every value against your car and a road test. |

## Layout

| Path | What it is |
|---|---|
| `main.py` | The Shift Points, Dyno and Link screens, the header and the bottom bar |
| `scan_ui.py` | The Scan screen: live dashboard, codes, log |
| `ui_kit.py` | Shared colours, one corner radius and gap, cards, chips, buttons |
| `scanner/` | PID catalogue (`pid_table.py` is generated), demo drive, shared data source |
| `tools/gen_pid_table.py` | Rebuilds the PID catalogue from the VE CALAIS Scanner Kotlin source |
| `dyno_live.py` | Simulated curve, dyno CSV loading and the launch simulation |
| `icons/` | App icon and the screen icons. `make_icons.py` redraws them (needs Pillow) |
| `shift_live.py` | Input rules and the calculation call, with no UI code |
| `link/obd.py` | Read-only ELM327 protocol, Wi-Fi and Bluetooth transports |
| `tunertoolpro/` | Copy of the desktop calculation package, made by `sync_core.py` |
| `sync_core.py` | Refreshes the copy from `app/tunertoolpro`. Run it after a desktop change. |
| `buildozer.spec` | Android build settings (Kivy and pyjnius, arm64 and armeabi-v7a) |
| `tests/` | Unit tests. They run on a desktop without Android. |

## Run the tests

```bash
cd "General Motors/Linux-Tuning-Suite/android"
python3 -I -m unittest discover -s tests -t .
```

`test_core_in_sync.py` fails if `tunertoolpro/` no longer matches the desktop package. Fix it with
`python3 sync_core.py`.

## Build the APK

Needs Java 17, the Android SDK and buildozer. Buildozer downloads the NDK itself.

```bash
pip install buildozer cython "sh<2"
buildozer -v android debug
```

- buildozer refuses a path that contains spaces. This folder sits under `General Motors/`, so
  copy `android/` to a path without spaces first (for example `~/tunertoolpro-build`) and build
  there.
- `buildozer.spec` pins python-for-android to `v2024.01.21`, which builds Python 3.11. Newer
  defaults build Python 3.14 and fail on the bundled pip.
- Copy the APK from `bin/` to the phone and install it, allowing installs from unknown sources.
  Buildozer is slow the first time (it compiles Python for Android).

## Bluetooth set-up

1. Plug the ELM327 adapter in. Pair it in Android Settings > Bluetooth (PIN is often 1234 or 0000).
2. In the app's Link tab, choose **Bluetooth adapter** and enter the adapter's address.
3. Allow the Nearby devices permission when Android asks.

## Notes

- Android Back returns to the Shift screen first, then leaves the app.
- Nothing is sent to the internet. The app has no account and no logging.
- Calculated values need checking against your vehicle before use. See the desktop user guide.
