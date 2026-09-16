# VE CALAIS Scanner (Android)

An Android OBD2 diagnostic app built specifically for a 2011 Holden VE Calais Redline L77 running an **E38 ECU** and **T43 (6L80E) TCM**, with a Killaboost G42-1450 turbo kit and E85/98 flex fuel tune. Connects to any ELM327-compatible Bluetooth OBD2 adapter.

**Current version:** 2.1.0

## What it does

- **Live Data dashboard** - paginated 4-sensor-per-page view, swipeable, tap a card to cycle Digital → Graph → Histogram display, drag-free page reordering via Up/Down controls
- **140+ PID database** - standard SAE Mode 01 PIDs plus GM enhanced Mode 22 DIDs for the E38 ECU and T43 TCM (per-cylinder misfire/injector data, transmission line pressure, TCC slip, shift times, etc.)
- **46 PIDs verified** directly against this car's own scan export (not just generic/assumed addresses)
- **3-bar MAP sensor scaling** - correctly reads 0-300 kPa instead of the factory 1-bar sensor's 0-255 kPa range
- **DTC Codes** - standard SAE Mode 03 read / Mode 04 clear, with a confirmation dialog before clearing (this is a write to the vehicle)
- **PID Scanner** - in-app Mode 22 DID sweep across the ECM (7E0), TCM (7E2), and FPCM (7E3) headers, to find which enhanced PIDs a given VIN actually answers
- **Sniffer** - live raw TX/RX traffic log for debugging adapter/header issues
- **Auto-logging** - every successful adapter connection starts a session; CSV + JSON export, date-stamped filenames
- **Demo Mode** - random-walk simulated data for trying the UI without a car connected

## Not yet implemented

- GM bi-directional actuator tests / module coding - these need real per-module routine IDs confirmed via the PID Scanner's DID sweep on the actual VIN before they can be trusted; not something safe to guess at
- CAN bus raw frame scanning (beyond the Mode 22 DID sweep the PID Scanner already does)
- Full drag-and-drop per-cell dashboard layout editor (page-level reordering is implemented; per-cell placement/resize is a planned follow-up)

## Building

Requires Android Studio (or just the Gradle wrapper) and JDK 17+.

```bash
./gradlew assembleDebug
```

Output: `app/build/outputs/apk/debug/app-debug.apk`

Min SDK 26 (Android 8.0), target SDK 34.

## Project structure

```
app/src/main/java/com/brookes/ve_calais_obd2/
├── OBD2Protocol.kt        - Mode 01/22/03/04 command formatting + response parsing
├── BluetoothManager.kt    - ELM327 communication (multi-line response handling, header switching)
├── BluetoothSession.kt    - shared connection singleton across screens
├── PIDDatabase.kt         - the 140+ PID definitions
├── DashboardPager.kt      - groups monitored PIDs into swipeable pages
├── SessionManager.kt      - auto-logging session lifecycle
├── DataLogger.kt          - CSV/JSON/DTC export
├── PidScanner.kt          - Mode 22 DID sweep logic
├── CarbonFiberDrawable.kt - procedural background texture
└── ui/                    - fragments (Home, LiveData, PidScanner, Sniffer, Dtc, Settings)
```

`docs/` contains earlier build/setup notes from this app's development history.

## Hardware notes

- ELM327 Bluetooth adapter (any generic clone works)
- T43 TCM answers on CAN header **7E2**, not the more commonly assumed 7E1
- MAP sensor PID (010B) is scaled for this car's aftermarket 3-bar sensor - if you fork this for a stock 1-bar VE, change the scaling in `PIDDatabase.kt`
