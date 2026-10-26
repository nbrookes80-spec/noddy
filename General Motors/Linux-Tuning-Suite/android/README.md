# TunerToolPro for Android (early build)

A phone version of the Shift Points calculator, with a read-only link to an OBD-II scan adapter.

- **Shift Points.** Change any input or gear ratio and all four shift tables (upshift, downshift,
  TCC unlock, TCC lock) recalculate at once. It uses the same calculation code as the desktop app.
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
| Other desktop tabs | Not ported yet (Vehicle, Pressure and Timing, Dyno, Datalog, XDF, BCT, AI). |
| Vehicle validation | None. Check every value against your car and a road test. |

## Layout

| Path | What it is |
|---|---|
| `main.py` | The Kivy screens (Shift Points and Link) |
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
pip install buildozer cython
buildozer -v android debug
```

The APK appears in `bin/`. Copy it to the phone and install it, allowing installs from unknown
sources. Buildozer is slow the first time (it compiles Python for Android).

## Bluetooth set-up

1. Plug the ELM327 adapter in. Pair it in Android Settings > Bluetooth (PIN is often 1234 or 0000).
2. In the app's Link tab, choose **Bluetooth adapter** and enter the adapter's address.
3. Allow the Nearby devices permission when Android asks.

## Notes

- Nothing is sent to the internet. The app has no account and no logging.
- Calculated values need checking against your vehicle before use. See the desktop user guide.
