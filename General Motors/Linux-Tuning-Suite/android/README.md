# TunerToolPro for Android (early build)

A phone version of the Shift Points calculator, with a read-only link to an OBD-II scan adapter.

- **Shift Points.** Change any input or gear ratio and all four shift tables (upshift, downshift,
  TCC unlock, TCC lock) recalculate at once. It uses the same calculation code as the desktop app.
- **Dyno.** Shows a power and torque curve and a simulated launch to the quarter mile. With no
  file loaded, the curve is estimated from the Shift Points settings (RWHP, shift RPM, idle RPM).
  Load a dyno CSV (`rpm,hp,tq`) with **Load dyno CSV** to use your own curve. The launch
  re-runs whenever a Shift Points value changes.
- **Sliders.** Each shift input has a slider and a typed box that stay in step.
- **Link.** Connects to an ELM327-compatible adapter over **Bluetooth** (paired first in phone
  settings) or **Wi-Fi** (the adapter's own network, usually 192.168.0.10 port 35000). It shows
  engine speed, vehicle speed, throttle and coolant temperature once a second.

The Link tab only sends set-up commands and Mode 01 reads. It never clears codes, runs tests, or
writes to the controller. `link/obd.py` refuses any other command before it is sent.

## Status

| Part | State |
|---|---|
| Shift calculation | Same code as the desktop app. Unit tests cover live recalculation. |
| Wi-Fi link | Tested against a simulated ELM327 over TCP. Not yet tried with a real adapter. |
| Bluetooth link | Written, not tested. Needs a real adapter and an Android phone. |
| Dyno and launch simulation | Same engine as the desktop Dyno & Drag tab. Not yet checked against a measured dyno run. |
| CSV loading | Dyno CSV loads on a desktop. On a phone it uses the system file picker (plyer), which is untested on a device. |
| Other desktop tabs | Not ported yet (Vehicle, Pressure and Timing, Datalog, XDF, BCT, AI). |
| Vehicle validation | None. Check every value against your car and a road test. |

## Layout

| Path | What it is |
|---|---|
| `main.py` | The Kivy screens (Shift Points, Dyno and Link) and the bottom bar |
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

- Nothing is sent to the internet. The app has no account and no logging.
- Calculated values need checking against your vehicle before use. See the desktop user guide.
