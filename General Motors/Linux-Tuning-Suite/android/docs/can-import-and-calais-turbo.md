# CALAIS TURBO profile, start-up settings, and CAN log import

Status: implemented on branch `feature/dashboard-bands-units-hud`, not yet tested on a car.
Owner: Nathan (2011 Holden VE Calais Turbo, 6L80E automatic, 3.9 differential).

Terms: Mode 01 and Mode 22 are the standard and GM-specific read requests an OBD adapter sends; a DID is the 16-bit id in a Mode 22 request; PWM is pulse width; 6L80E is the GM 6-speed automatic; the APK is the Android app file; adb copies files to the phone over USB. Live and Scan are the app's sensor screens; Shift is the shift-point tab; the sniffer is the Sniff tab's CAN
capture; a PID is one logger reading; the TCM is the transmission controller; a DBC file names the signals inside CAN frames.

## Problem statement

1. The logger is missing 16 GM readings the owner wants on the Calais: AC high side pressure, EGR duty and
   voltage, H2O sensor, ignition 1 voltage, injector PWM for both banks, misfire history for all eight
   cylinders, and oil pressure. They exist in `data/torque_gm_predefined.csv` but no car profile loads them.
2. A new install, or a phone that has been reset, starts with the default car, no vehicle chosen on the Shift tab,
   the transmission readings off, and no theme music in the intro. The owner's own car and settings are kept
   across starts, so this only affects a first start or a reset.
3. The owner has CAN bus logs (the sniffer's own captures, and logs from other tools) and a DBC file that
   describes them. There is no way to show the decoded signals on Live or Scan, or to log them.

## Goals

- G1. A saved car, "2011 Holden CALAIS TURBO", that loads the 16 PIDs (they show on Scan and are written to a data log; the Live grid is the fixed engine and transmission stream), is the active car on start, and is
  created on the first start.
- G2. The Shift tab's vehicle is a registered 'CALAIS TURBO (6L80E)' starter profile: transmission
  '6L80 (2006-Current)' (the same name as the saved car) and final drive 3.9. It is chosen on first start only if
  the owner has not already picked a vehicle.
- G3. Start-up settings that apply once to an existing install, and are the defaults on a fresh install: the TCM
  readings are on in Live, the CALAIS car is the active car, and the intro plays its theme music. After
  that, the owner's own choices are kept.
- G4. The intro plays `assets/intro_theme.ogg` (converted from the owner's `audio.mp3`, 22.2 s) while the
  pictures show, and stops when the intro ends or is tapped. The `intro_music` preference turns it off; there is no menu switch for it yet (Q5).
- G5. A CAN log and its DBC can be played back on Live and Scan. Each decoded signal becomes a sensor card
  under an "Imported from a CAN log" group, and is written to the data log with the other sensors.

## Non-goals

- Sending anything to the car from imported data. Imported signals are never requested from the adapter.
- Live capture from a CAN adapter. Playback only.
- Choosing a DBC automatically. The owner picks the log and the DBC on each play.
- Remembering the last played log across starts (v1; see Q2).
- Decoding raw bytes without a DBC.
- Verifying the decoded values on the Calais. See Open questions.

## Design

Paths are relative to `android/`. Files at the root are named without a folder.

### Car and vehicle (G1, G2)

- `scanner/calais.py` (pure, no Kivy). `ensure_car(cars_dir)` saves the car through the existing
  `predefined.save_to_profile` path, using a `PredefinedList` whose filter keeps the 16 names listed in
  `NAMES`. It returns None when the car exists already.
- `PROFILE_NAME = 'CALAIS TURBO (6L80E)'`, `BASE_PROFILE = 'LS3 Camaro SS (6L80)'`, `FINAL_DRIVE = 3.9`.
  `register_profile()` adds a copy of the base profile to `tunertoolpro.engines.constants.STARTER_PROFILES` with
  `axle=3.9`. It is safe to repeat, and it must run before the Shift settings screen reads its saved choice.
- `ensure_vehicle(choice_path)` registers the profile, then writes the Shift tab's vehicle choice file
  (`vehicle.json` in the app folder) through `tunertoolpro.vehicles` as Holden / '6L80 (2006-Current)' /
  CALAIS TURBO (6L80E). It does this only when the file has no profile and no transmission, so an owner's choice is
  never replaced. `vehicles.save` ignores a folder it cannot write. Its other values are the base profile's own (see R12).
- `main.restore_car()` calls `ensure_car` once, gated by `prefs['calais_saved']`, and logs an `OSError` instead of
  stopping. `main.py` calls `ensure_vehicle` on each start, before `SettingsScreen` is built.

### Start-up settings (G3)

- `prefs.py`: `SETTINGS_VERSION = 1`, `START_SETTINGS` (`live_transmission`, `scan_profile`, `intro_music`).
  `DEFAULTS` takes the same values, so a missing file (fresh install) gets them. `load()` applies
  `START_SETTINGS` when the saved `settings_version` is not the current one, and then stores the current
  version. A file saved by this version keeps its values. `calais_saved` (default False) records that
  `restore_car()` has made the car once, so a car the owner deletes or renames stays that way.

### Intro music (G4)

- `splash_ui.SplashOverlay(music=...)` loads `assets/intro_theme.ogg` through `kivy.core.audio.SoundLoader`.
  A load failure leaves the intro silent. `finish()` stops the sound.
- `buildozer.spec` includes `ogg` in `source.include_exts`.

### CAN log import (G5)

- `scanner/dbc.py` (pure). Parses `BO_` and `SG_` lines into `Signal` records, with the byte order, sign,
  scale, offset, range, unit and multiplexer role. `raw_value()` reads a signal from a frame's bytes.
  Intel and Motorola bit numbering are handled. Comment, attribute and value-table lines are ignored.
- `scanner/can_replay.py` (pure). `decode()` turns frames and signals into a time series per signal. A
  multiplexed signal reads only when its multiplexer matches. `ReplaySource` plays the series back at real
  speed, loops at the end, and answers `poll()`, `read()`, `listen()` as the adapter and demo do. Each signal
  becomes a `Pid` whose id is `CAN<message ID hex>[X for a 29-bit ID].<index in DBC>` (for example `CAN0C9.0` or `CAN1F5X.3`), with `trusted=False`.
- `scanner/can_import.py`. `load(log, dbc)` reads the files (2 MB limit per file), runs the frame parser in
  `tunertoolpro/canbus/frames.py`, decodes, and returns a `Loaded` with a message for the user. Problems
  raise `ImportProblem` with a message the user can act on.
- `scanner/pids.py`: `REPLAY` holds the imported PIDs. `get()` falls back to it. `valid_id()` is unchanged, so
  an imported id is never a Mode 01 or 22 read and can never reach the adapter.
- `scanner/session.py`: `set_replay(source)`. While a replay is set, `active()` returns it ahead of the demo
  and the adapter, and `status` is `REPLAY`. The header shows REPLAY in the accent colour.
- `live.py`: a round reads the `REPLAY` ids only when the source is a replay (`source.replay` is set), so the
  adapter is never asked for them. `step()` appends the `REPLAY` ids after the ordered built-in ids, so they come last in
  each round. `_ordered()` itself only places an id that is not in the built-in list after the engine readings and
  before the TCM readings.
  `snapshot()` covers them. History is created on first use.
- `live_ui.py`: a replay adds its signals to the Live grid, under the Imported group. Built-in cards that the
  log does not carry show "not in the CAN log" rather than "no reply".
- `scanner/dashboard_layout.py`: group `Imported` (last), and `dashboard_pids()` includes the replay PIDs, so
  Scan shows them.
- `main.py`: `play_can_log(log, dbc)` and `record_columns()` (the replay PIDs are always logged).
- `menu_pages.can_card()`: on the menu's "GM and Holden PID lists" page. It lists log files from the sniffer's `captures` folder and
  from `CAN imports` under the app's storage folder, and DBC files from the same two folders. Play and Stop
  call `play_can_log`. The folder is created when the menu opens.

## Risks and mitigations

- **R1. The Caprice DBC is not the Calais DBC.** `caprice_ppv.dbc` (in `T43_6L80E_reference/caprice-ppv-can-database/`) has messages for 28 of the 52 message IDs in
  one of the owner's captures and 29 of the 54 in the other, and it is a different car's file. Signals can decode to the wrong values, and the decoder
  cannot tell. Mitigation: the owner chooses the DBC on each play. Its file name is shown in the load message and in
  each imported sensor's description. Open question Q1 asks for a DBC that is verified for this car.
- **R2. Implausible decoded values.** The engine speed decodes to a range of 7.5 to 16,338 rpm on the owner's
  capture, which points to a few frames being read as the wrong signal or to a wrong DBC. Mitigation: the
  DBC range is used for the gauge, values are shown as decoded, and this is listed as Q4 under Open questions.
- **R3. Held values.** A signal that stops arriving keeps its last value on screen. Accepted risk for v1, owner
  Nathan. Follow-up (not in v1): after 5 s with no new reading a card shows its age, and the reading turns grey.
- **R4. Memory on the phone.** Measured on the desktop: a frame costs about 180 bytes of Python objects and a
  reading about 100 bytes. The file limit (2 MB, about 57,000 frames) and the reading cap (200,000, about 20 MB)
  bound the peak to roughly 30 MB. The reading cap is the limit that bites first on a busy bus: with about 6 signals
  per frame, about 33,000 frames already reach it. Frames are kept only for the DBC's messages and the gear message,
  but `load()` holds every parsed frame (and both texts) until it returns, so the peak is all parsed frames plus the readings, which is the roughly 30 MB above.
- **R5. Columns fixed at the start of a recording.** A log played after a recording starts is not in that
  file. Mitigation: documented in `scanner/data_log.py` (columns are fixed when the recording starts).
- **R6. A saved car on start for existing installs.** The start-up set changes `scan_profile` once for an
  install that had another car selected. Mitigation: the owner can select another car in the same menu, and
  the choice is kept.
- **R7. Accidental send.** An imported signal cannot be sent to the car. Layers: `LiveStream` adds the imported ids only
  when the source is a replay; the adapter's read path (`link/obd.py` `_read_catalog` and `_poll`) looks ids up in
  the built-in `CATALOG` only, not in `pids.get()` (which also finds replay ids), so an imported id raises
  `UnsafeCommand` from `read()` and is reported as an error by `poll()` before any command or header is sent; and
  `is_allowed()` checks the same `CATALOG`. Tests: `test_the_adapter_refuses_an_imported_signal`,
  `test_an_imported_can_signal_is_never_sent_to_the_adapter` (drives `Elm327.read` and `poll` against a fake adapter and
  asserts nothing is sent) and `test_live_only_asks_for_imported_signals_from_a_replay`. An earlier version relied on
  `pids.get()` returning None, which the replay fallback defeated; the adapter now looks ids up in `CATALOG` directly.
- **R8. Unreadable or hostile files.** Both files are read as text with replacement for bad bytes, limited to
  2 MB, and parsed line by line. A signal line whose numbers cannot be read, whose length is over 64 bits, or whose
  scale or offset is not finite is skipped; any other parse failure in the DBC or the log (for example an unreadable timestamp) becomes an `ImportProblem` message, never a crash.
- **R9. No engine data while a log plays.** While a replay is set, Live and Scan read only the log, so a recording made
  then has blank columns for the built-in engine and transmission readings. Mitigation: the Live cards say "not in the
  CAN log", and the debug log names the source (`REPLAY`) when a recording starts.
- **R10. Imported ids depend on the DBC.** An id is `CAN<message>.<index in DBC>`, so the same id can mean a different
  signal under another DBC, and per-sensor settings saved by id (red line, display mode) would then apply to the
  wrong signal. Accepted for v1: Live and Scan show the DBC file name in each sensor's description. A change of
  DBC during a recording writes new data under the old column labels. Fix when needed: key by message id and
  signal name.
- **R11. Many signals.** Every decoded signal becomes a card. A DBC with hundreds of signals present in the log can
  slow Live (2 Hz refresh of every card) and the phone's memory. No cap or picker in v1; Q6 asks for one.
- **R12. Shift profile values are not the Calais's.** The 'CALAIS TURBO (6L80E)' profile copies the LS3 Camaro SS 6L80
  starter profile and changes only the axle to 3.9. Tyre, weight, RPM limits and converter lock are the base
  profile's, and they feed the Live shift grading. Mitigation: they are editable on the Shift tab.
- **R13. The 16 PIDs are unverified on the Calais.** They are real Mode 22 requests taken from the Torque Pro list in `data/torque_gm_predefined.csv`;
  `[GM]Oil Pressure <2005` is named for older cars. A wrong DID can return a plausible but wrong number. Verification
  step: compare each reading with a scan tool before trusting it.
- **R14. Codes while a log plays.** `ReplaySource.read_dtcs()` and `clear_dtcs()` raise an error that says a CAN log is
  playing, so Scan > Codes cannot show "no stored codes" or report a clear that did not happen.
- **R15. A car that cannot be made at start.** If the CALAIS car cannot be saved, `calais_saved` stays False so it is tried
  again next start (and, because that retry has just made the car, it is then also made the active car), and `scan_profile` is cleared rather than left pointing at a car that does not exist. The previous
  selection is not restored (the start-up set had already replaced it when the file loaded).

## Test plan

- The whole suite has 486 unit tests; those for this feature are in `tests/test_calais.py`, `tests/test_can_import.py` and `tests/test_obd.py`. They cover: the 16 PIDs
  load from the saved car; the car is created once (`ensure_car` returns None when it exists); the
  'CALAIS TURBO (6L80E)' starter profile is the 6L80 base profile with a 3.9 axle, the base is untouched, and
  registering twice leaves one profile; a new install gets the CALAIS TURBO vehicle; a vehicle already chosen is not
  replaced and a second start does nothing; a folder that cannot be written does not raise; the start-up set applies
  once and keeps later choices (`StartSettingsTests`); DBC parsing (Intel, Motorola, signed, offset, multiplexed,
  extended IDs); decoding; replay looping, hold and listen; imported ids fail `valid_id`; load errors give
  readable messages. `tests/test_prefs.py` was adjusted so its existing tests keep their values.
- The adapter refusal tests are in `tests/test_obd.py` and `tests/test_can_import.py` (`ReplayGuardTests`); see R7.
- Not covered by unit tests: the `calais_saved` gate in `main.restore_car()`, the Imported group and
  `dashboard_pids()`, the header REPLAY colour, the Live "not in the CAN log" text, and the splash music. These are
  checked by hand below.
- One-off headless Kivy check (not kept in `tests/`): the CAN card and the Live screen build with a replay running.
- Manual on the phone: install the APK, check the CALAIS car is active, check the TCM cards show on Live,
  play a capture on Live and Scan, record, and compare the log columns; hear the intro theme; see REPLAY in the header and "not in the CAN log" on the built-in cards while a log plays.

## Alternatives

- **Send the 16 PIDs through the adapter only.** Rejected for the replay feature: CAN traffic the car sends
  without a request cannot be read with Mode 01 or 22. Those PIDs are fine as a saved car (G1), which uses
  the adapter.
- **Add imported signals to the PID catalogue with an id that passes `valid_id`.** Rejected: that would let an
  imported signal reach the adapter. A separate `REPLAY` table keeps the read-only rule in one place.
- **Use the Android file picker (plyer) to choose files.** Rejected for v1: the file URIs it returns are not
  always readable as paths on Android 11 and later. A fixed folder is predictable and needs no picker.
  Cost: the owner copies files into the folder (adb, or the app's storage over USB).
- **Decode on a background thread.** Rejected for v1: measured on the desktop, the 323 KB capture (9,309 frames)
  parses in 0.14 s and decodes in 0.38 s. The load runs on the screen's own thread, so the file limit is 2 MB
  (about 3 s on the desktop at that rate) to stay well under Android's 5 s input timeout; the phone is slower.
  A background decode with a "Loading" status is the next step if larger files are needed.
- **Build the CALAIS car into the app's built-in profiles.** Rejected: built-in profiles cannot be removed
  or edited, and the owner may want to change the car. A saved car can be edited and is listed with the
  others.
- **Re-apply the start-up settings on every start.** Rejected: that would undo the owner's choices. A version
  number applies them once.
- **Default the TCM readings on through `DEFAULTS` only.** Rejected for existing installs: their saved file
  already has `live_transmission: false`. The version migration covers both cases.

## Open questions

- Q1. Which DBC describes the owner's Calais? Candidate: `caprice_ppv.dbc`, from the owner's research folder (`T43_6L80E_reference/caprice-ppv-can-database/`).
  It needs checking against a known reading (for example, the transmission temperature on the scan tool).
- Q2. Should the last played log and DBC be remembered across starts? Not in v1.
- Q3. Should imported signals keep their dashboard order and hidden state? Their ids are not `valid_id`, so
  the saved order and the hidden list drop them. Needs a new key format if wanted.
- Q4. The engine speed outliers in R2: is that a wrong DBC, or a capture problem?
- Q5. Should the intro music have a switch in the menu? Today only the `intro_music` preference turns it off, and
  the theme plays at full volume on every start.
- Q6. Should imported signals be capped or picked from a list, for a DBC with many signals?
