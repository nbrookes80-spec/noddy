# 6L80e TunerToolPro — Linux-Tuning-Suite

Merged Linux port of two Windows tools:

1. **Pro Transmission Calibration Studio** (`Ewalts Auto Tuning Transmission Calibration Studio v2.0.exe`, PyInstaller bundle, Python 3.12 + PyQt6)
2. **Bluecat Transmission Tool** (`BC_Trans.exe` v1.1.9.0 + `BCGrid.dll` v3.1.3.2, .NET Framework 2.0 WinForms)

Merged product name: **6L80e TunerToolPro**. Version 0.1.0.

## Status

| Step | State |
|---|---|
| Static analysis of both programs | Done |
| Decompile BC_Trans.exe + BCGrid.dll to C# | Done — `recovered/bct-csharp/` |
| Disassemble the Python app's bytecode | Done — `recovered/6l80e-python-disasm/` |
| Reconstruct the calculation engines | Done (see table below). All verified against the original |
| BC Trans data formats (`.BTC`, presets, speed math) | Done. All 33 shipped tunes round-trip byte-for-byte |
| BC Trans `Calc_Shifts` port | Ported to `app/tunertoolpro/bct/calc_shifts.py`. Matches the decompiled original on 433 cases (33 tunes + 400 random variants) within 5e-05. Not compared with BC Trans itself, which cannot be run here. Notes in `recovered/bct-csharp/CALC_SHIFTS_NOTES.md` |
| Merged PyQt6 application | Done — `app/`. Six tabs. Tests pass headless (58 tests) |
| GUI installer | Done — `installer/`. Tested in CLI mode |
| User guide | Done — `docs/USER_GUIDE.md` |
| Differential tests against the original | Done for all reconstructed engines and readers: 34,685 checks, 0 failures (see below) |
| Commits / push | Local commits only, when asked. Nothing pushed |

## Folder layout

```
app/                         the application (install copies this folder)
  requirements.txt           PyQt6, pandas
  tunertoolpro/
    __main__.py              python3 -m tunertoolpro
    core.py                  GUI-free logic: profiles, intents, tables, TPS x Gear export, dyno, drag, logs
    engines/                 reconstructed calculation engines (see table)
    bct/                     BC Trans data: tune.py (.BTC), presets.py, shiftmath.py, shift_cfg.py (.BTC to Shift Points inputs)
    gui/                     PyQt6 tabs: shift_tab, pressure_tab, dyno_tab, log_tab, xdf_tab, bct_tab
  tests/                     unittest suite (58 tests; one skipped if the XDF reference is absent)
installer/
  install_tunertoolpro.py    GUI installer (Tkinter) and --cli mode
docs/
  USER_GUIDE.md              how to use each tab, limits, troubleshooting
recovered/
  bct-csharp/
    BC_Trans/   C# project from ILSpy 9.1 (Main_Form.cs holds Calc_Shifts, Gen_Table, Update_VSS, ...)
    BCGrid/     C# project for the grid control (BCGridControl.cs)
  6l80e-python-disasm/
    NNNNN_<function>.dis.txt   CPython 3.12 disassembly, one file per code object, named by source line
    _index.json                function name, line, op count and string constants
```

Recovered sources are kept here for reference and porting. The original binaries are not copied into this folder.

## Running

```
python3 -m venv venv && . venv/bin/activate
pip install -r app/requirements.txt
cd app && python3 -m tunertoolpro
```

Install as a menu app with `python3 installer/install_tunertoolpro.py`.

Tests (from `app/`, offscreen for the GUI tests):

```
QT_QPA_PLATFORM=offscreen python3 -m unittest discover -s tests -t .
```

The BC Trans tests read the shipped `.BTC` and preset files from `BCT_DIR`, which defaults to
`/home/nathan/Downloads/BCT+1.42/Bluecat Transmission Tool`. Set `BCT_DIR` to point elsewhere.

## Reconstructed engines

| Module | Status | Verification |
|---|---|---|
| `engines/calc_engine.py` — `CalcEngine` | Hand-transcribed from the disassembly, each line cites its source line | Differential test `verify_calc_engine.py`: 22,400 checks, 0 failures |
| `engines/constants.py` — 54 plain-data constants | Generated from the original by `reconstructed/python/tests/gen_constants.py` | Not differentially checked |
| `engines/pressure_engine.py` — `PressureEngine` | Transcribed from the disassembly and corrected against it | Differential test `verify_engines.py`: all checks match. `tcc_apply_pressure_ramp` takes a `max_torque` argument the original never uses |
| `engines/shift_time_engine.py` — `ShiftTimeEngine` | Transcribed from `06308..06333` | Hand checks (first value 0.575 s, full-torque value 0.3 s) |
| `engines/tcc_duty_engine.py` — `TCCDutyEngine` | Transcribed from `06341..06372` | Hand check: 151 °F at 0 psi = 95.0% |
| `engines/torque_curve.py` — `TorqueCurve` | Transcribed from `01293..01457` | Smoke and unit tests. Rows with blank cells are dropped |
| `engines/boost_curve.py` — `BoostCurve` | Transcribed from `01214..01280` | Smoke tests |
| `engines/drag_simulator.py` — `DragSimulator` | Transcribed from `01863..01960` | Test: 0–60 mph within 3–9 s on a synthetic curve |
| `engines/bin_reader.py` — `BinReader` | Transcribed from `01160..01204` | Not yet run against a real `.bin` |
| `engines/xdf.py` — `XDFDefinition` | Transcribed from `00905..01157` | All 22 XML `.xdf` files under `General Motors/` parse. The other 30 are 17 binaries and 13 empty placeholders |
| `engines/logimporter.py` — `LogImporter` | Transcribed from `01499..01831` | Synthetic log test: pandas and csv-module paths give identical results |

Not yet reconstructed: nothing in the Python app's engine set is missing.

Known issues (not fixed):
- `calc_engine.py`: `init_lock_logic` is read but never used. `calculate` has an unreachable `else base = min_speed` branch.
- `xdf.py`: `_apply_math` evaluates an expression from the XDF with empty builtins. `**` is allowed, so a crafted XDF can force heavy computation. Treat as a hardening task.
- `logimporter.py`: the WOT section skips rows with `rpm <= 0`. The original divides by zero there.
- GUI: the Shift Points torque-lead mode uses 75% of rated HP, not the dyno curve. BC Trans's own `Calc_Shifts` also uses 75% of RWHP, so this matches BC here. Without a loaded tune, per-gear delays are the fixed fallback (0.5 s up, 0.15 s down).
- Shift Points has two engines, chosen by the **Engine** selector. *CalcEngine* maps a loaded `.BTC` tune's keys to its inputs (`bct/shift_cfg.py`; see the mapping table in `docs/USER_GUIDE.md`). *BC Trans (Calc_Shifts)* runs the `bct/calc_shifts.py` port on the tune as written. The port matches the decompiled `Calc_Shifts` on 433 cases within 5e-05. It is not checked against BC Trans running on a car, because BC Trans cannot be run here.
- `bct/shift_cfg.py` reads `Gear` as the final drive and sets the chain ratio to 1.0. BC Trans has no separate chain ratio.

Differential results (run 2026-10-26 with your approval, on the extracted main module `.pyc` only, in an empty folder with `python3 -I` and no network):
- `reconstructed/python/tests/verify_calc_engine.py`: 22,400 checks, 0 failures
- `reconstructed/python/tests/verify_engines.py`: 12,285 checks, 0 failures. Covers PressureEngine (including the TCC ramp eras), ShiftTimeEngine, TCCDutyEngine, TorqueCurve, BoostCurve, DragSimulator, BinReader and XDFDefinition on the reference XDF, and LogImporter.

Run both as: `python3 -I <script> "<path to orig.pyc>"`. Use `unshare -rn` to block network where available.

Not covered by the differential run: the pandas `from_dataframe` path (both sides used pandas when available, so only the path choice is shared), and `LogImporter` rows where RPM is zero with WOT slip. The original would divide by zero there; the reconstruction skips the row.

## How the Python side was decompiled

The first attempt was `pycdc` (zrax/pycdc). Building it meant fetching and compiling external code, and the action was blocked, so it was not built. Instead the code objects were loaded with the standard library `marshal` module and disassembled with `dis` (Python 3.12.3 matches the bytecode). That gives complete, accurate disassembly. The engines were then transcribed by hand from the disassembly.

## Key findings so far

- **Shared shift math (BC_Trans `Calc_Shifts`):** speed at each gear is `RPM / (ratio × final drive) × tire × 3.14 × 60 / 12 / 5280` (MPH). The original writes the literal 3.14 for π, and the port keeps it. The stall slip is `(stall/1000)^1.7 / 100`. Upshift and downshift points are interpolated between `MinSpeed` and the per-gear speed using slope factors from the Slope table, with an optional override table.
- **Lock/unlock:** `MinTCCSpeed` sets the floor for TCC unlock/lock speeds. Lock/unlock spreads and the stall-logic floor are applied after that.
- **Data format:** `.BTC` tune files are CRLF text with one key line and one value line per field. `Trans_Presets.txt` and `Slope_Presets.txt` are tab-separated with a `#` comment header.
- **Python app:** the module docstring describes an output of TPS × Gear matrices for HP Tuners VCM Editor and TunerPro paste. It includes engines for shift points, pressure/TCC, shift time, TCC duty, a drag simulator, and XDF/BIN and datalog import.

## Attribution

Reference material under `General Motors/T43_6L80E_reference/` is third-party and carries its own licences (see that folder's README).
