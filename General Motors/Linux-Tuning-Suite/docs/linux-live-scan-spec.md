# Linux desktop: Link, Live and Scan (Android parity)

Status: draft spec, 2026-11-06. Branch `feature/linux-live-scan`, stacked on PR #21 (the Android work it copies).

## Problem

The Linux desktop app (PyQt6, 0.1.0) is a calculator: Shift Points, Vehicle, Pressure & Timing, Dyno & Drag, Datalog,
XDF/BIN, BCT Tunes, CAN Sniffer, AI Assistant. It cannot talk to a car. The Android app can: it connects to an ELM327
adapter, streams engine (ECU) and transmission (TCM) readings on Live, lists 36 PIDs on Scan, logs them, replays an
imported CAN log, and opens with the owner's car (CALAIS TURBO, 6L80E, 3.9 diff). None of that exists on Linux, so
the owner cannot use a laptop in the car, and the two apps drift apart.

## Decisions (from the owner, 2026-11-06)

- Scope: **both, in order**: Android parity first, then polish the existing 0.1.0 tabs and release.
- Adapters: **Bluetooth ELM327 via RFCOMM, USB serial, and demo / CAN-log replay**. Wi-Fi ELM327 already exists in
  the transports and stays, but is not a goal to test.
- Sharing: **move the engine into `tunertoolpro-core`** so Android and Linux use one copy.

## Goals

1. New desktop tabs **Link**, **Live** and **Scan**, behaviourally the same as Android's: connect, demo drive, grouped
   sensors (TCM, ECU, Fuel, Air, Boost, Imported), health tiles, shift grading, codes, data log and REC.
2. The same 36 PIDs, the CALAIS TURBO car and the same start-up defaults, saved per user in the desktop settings folder.
3. CAN log + DBC import and replay on Live and Scan, with the same safety design (imported signals are never sent).
4. One copy of the scanner / link / live code in `tunertoolpro-core`, pinned by `core.lock`, used by both apps.
5. Read-only stays. The only write is Mode 04 clear codes, behind a confirm, exactly as on Android.

## Non-goals

- Writing to any controller, flashing, or free-form Mode 22 sweeps.
- A new look: reuse the desktop theme (`gui/theme.py`); no Kivy on desktop.
- Windows or macOS testing (the Windows build stays paused until the friend tests it); the code must not stop them working.
- Intro music on desktop (Q3).

## Design

### Shared engine (move into core)
Today, outside Kivy, the Android app imports `scanner/*`, `link/*`, `live.py`, `grading.py` as top-level packages and
`link/obd.py` imports the Android-only `variant` module (a build flag for clear-codes). To share them:

- Core gains `tunertoolpro/scanner/`, `tunertoolpro/link/`, `tunertoolpro/live.py`, `tunertoolpro/grading.py`.
  `tools/update_core.py` already treats everything outside `gui/`, `__main__.py`, `__init__.py` as core, so the pin and
  hash check cover them with no tool change.
- `variant` is replaced by an argument: `Elm327(transport, allow_clear=False)`; the desktop passes the setting.
- Android's `sync_core.py` copies the new files to `android/tunertoolpro/`; Android imports change from
  `from scanner import x` to `from tunertoolpro.scanner import x`. That is a mechanical rename, covered by the
  existing 488 Android tests (they must stay green with no other change).
- Kivy-only modules stay in the apps: `*_ui.py`, `pid_card.py`, `main.py`, `app_menu.py`, `menu_pages.py`, `hud.py`.
- Transports: core keeps one `SerialTransport` / `TcpTransport` pair (today there is one in `canbus/transports.py`
  and a second in `link/obd.py`). The `link/obd.py` ones win (they carry the allow-list discipline); the sniffer uses
  them too. Android's `BluetoothTransport` (jnius) stays in the Android app and is passed in.

### Linux adapters
- **USB serial**: `/dev/ttyUSB*`, `/dev/ttyACM*`; listed with `serial.tools.list_ports`. Needs the user in `dialout`;
  the Link tab says so when open fails with permission denied.
- **Bluetooth**: v1 uses an RFCOMM device bound by the OS (`rfcomm bind` / `bluetoothctl` pairing -> `/dev/rfcomm0`),
  opened as a serial port. The Link tab lists paired adapters (`bluetoothctl devices`) and shows the exact command to
  bind one. A direct RFCOMM socket (`socket.AF_BLUETOOTH`) is a later ticket (T8) so no root helper is needed.
- **Demo / CAN replay**: unchanged sources (`scanner.demo.DemoSource`, `can_replay.ReplaySource`).

### Desktop screens
- **Link tab**: transport picker (Serial / Bluetooth / Wi-Fi / Demo), port list with Refresh, Connect / Disconnect,
  status line, "connect automatically when the app opens". Mirrors Android's Link screen text.
- **Live tab**: shift light, grouped tiles, shift-against-table list. Reuses `live.LiveStream`; reads on a worker
  thread (`QThread`) and posts snapshots to the GUI thread with a signal at about 5 Hz. No device I/O on the GUI thread.
- **Scan tab**: paged PID cards (same groups), Codes (read / clear with confirm), Log (start / stop, files in the
  desktop data folder). Card widgets are new Qt widgets (`PidCard`) drawing number, range/average and a bar.
- **Settings**: a "CAN log" panel on Link (log + DBC pickers using `QFileDialog`, Play / Stop) in place of Android's menu.
- REC button and the status badge (OFFLINE / DEMO / REPLAY) in the top bar, as on Android.

### Data and defaults
- User data under `settings.user_dir()` (already used for `vehicle.json`): `cars/`, `prefs.json`, `captures/`,
  `CAN imports/`, `data logs/`. The Android `storage.py` folder helper becomes a base-path argument.
- Start-up defaults and the CALAIS TURBO car (`scanner/calais.py`) come with the shared engine; the desktop calls
  `ensure_car` / `ensure_vehicle` at start-up the same way `main.py` does, gated by the same `calais_saved` flag.

### Safety (unchanged, must be tested on desktop)
`is_allowed` is the only gate to the wire. Imported (`pids.REPLAY`) signals are never in the catalogue the adapter
reads. Mode 04 only after the user confirms and `allow_clear` is on. Replay refuses Codes read/clear.

## Tickets (tracer bullets, blocking edges in brackets)

- **T1 Share the engine** (none). Move scanner/link/live/grading into core, remove `variant`, rename Android imports, sync, tag core.
  Done when Android's 488 tests and the desktop 58 pass (the README says 111; only 58 run today, so check what was lost), `core.lock` updated, an APK still builds.
- **T2 Desktop demo Live** [T1]. A Live tab on the demo drive: worker thread, snapshot signal, 13 built-in tiles, health tiles.
  Done when an offscreen test starts demo, gets rounds, and shows RPM / gear values; and a screenshot looks right.
- **T3 Link tab with serial and Bluetooth** [T1]. Port list, connect, status, auto-connect; fake serial adapter in tests.
  Done when a fake ELM327 (pty) is polled with only allowed commands, and a permission-denied message is shown.
- **T4 Scan tab** [T2]. Paged cards by group, 36 PIDs, edit limits and colour bands (reuse `pid_view`, `dashboard_layout`).
- **T5 Codes and clear** [T3, T4]. Read stored codes, confirm dialog, clear, replay refusal.
- **T6 Logging and REC** [T2]. CSV data log of the PIDs on screen with the same columns as Android; REC button.
- **T7 CAN import and replay** [T2]. Panel, `can_import.load`, Imported group, "not in log" on Scan.
- **T8 Direct Bluetooth RFCOMM socket** [T3]. No `rfcomm bind` step.
- **T9 Polish** [T1-T7]. Installer on a real desktop, EFILive log reader, README / user guide, tag 0.2.0.

## Test plan

- Core (no Qt): the 488 Android tests move with the code (run against core); add `allow_clear` tests.
- Desktop: offscreen Qt tests per screen (existing `test_gui.py` style); a pty-backed fake ELM327 for Link and Live.
- Safety: a test that records every byte written to the fake adapter while Live, Scan and a CAN replay run, and
  fails on anything outside `is_allowed`.
- Manual: demo drive screenshots (Xvfb); a real adapter on the car, reported by the owner (not yet possible here).

## Risks

- R1 Rewriting Android imports risks a regression in just-reviewed code. Mitigation: mechanical rename only, 488 tests, rebuild and retest the APK.
- R2 Two repos must move together (core, then app pins). Mitigation: tag core, update pin in one PR per app.
- R3 Bluetooth RFCOMM binding needs root on some distros. Mitigation: show the command; T8 removes it.
- R4 PyQt6 timing: Qt widgets for 36+ live tiles may be slow if redrawn naively. Mitigation: update only changed tiles, cap at 5 Hz.
- R5 Nothing here has run against a real adapter on Linux (same status as Android Bluetooth).
- R6 This branch is stacked on PR #21; if #21 changes in review, this branch needs a rebase.

## Open questions

- Q1 Name the core release for T1 (`v0.2.0`?) and when to push `tunertoolpro-core` (pushing is outward-facing: needs the owner's yes).
- Q2 Keep `canbus/transports.py` as a thin alias, or delete it once the sniffer uses the shared transports?
- Q3 Intro music on desktop (the Android intro theme): wanted later?
- Q4 Should the desktop default to the CALAIS TURBO car the way Android does, or ask on first run?
