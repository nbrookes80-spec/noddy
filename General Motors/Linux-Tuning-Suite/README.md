# 6L80e TunerToolPro — Linux-Tuning-Suite

Merged Linux port of two Windows tools:

1. **Pro Transmission Calibration Studio** (`Ewalts Auto Tuning Transmission Calibration Studio v2.0.exe`, PyInstaller bundle, Python 3.12 + PyQt6)
2. **Bluecat Transmission Tool** (`BC_Trans.exe` v1.1.9.0 + `BCGrid.dll` v3.1.3.2, .NET Framework 2.0 WinForms)

Merged product name: **6L80e TunerToolPro**.

## Status

| Step | State |
|---|---|
| Static analysis of both programs | Done |
| Decompile BC_Trans.exe + BCGrid.dll to C# | Done — `recovered/bct-csharp/` |
| Disassemble the Python app's bytecode | Done — `recovered/6l80e-python-disasm/` (379 functions + `_index.json`) |
| Readable Python source for the app | In progress — `CalcEngine` done and verified (see below) |
| Port to Linux / merge | Not started |

## Folder layout

```
recovered/
  bct-csharp/
    BC_Trans/   C# project from ILSpy 9.1 (Main_Form.cs holds Calc_Shifts, Gen_Table, Update_VSS, ...)
    BCGrid/     C# project for the grid control (BCGridControl.cs)
  6l80e-python-disasm/
    NNNNN_<function>.dis.txt   CPython 3.12 disassembly, one file per code object, named by source line
    _index.json                function name, line, op count and string constants
```

Recovered sources are kept here for reference and porting. The original binaries are not copied into this folder.

## How the Python side was decompiled

The first attempt was `pycdc` (zrax/pycdc). Building it meant fetching and compiling external code, and the action was blocked, so it was not built. Instead the code objects were loaded with the standard library `marshal` module and disassembled with `dis` (Python 3.12.3 matches the bytecode). That gives complete, accurate disassembly, but not readable Python. Turning it into source is the next step.

## Key findings so far

- **Shared shift math (BC_Trans `Calc_Shifts`):** speed at each gear is `RPM / (ratio × final drive) × tire × π × 60 / 12 / 5280` (MPH). The stall slip is `(stall/1000)^1.7 / 100`. Upshift and downshift points are interpolated between `MinSpeed` and the per-gear speed using slope factors from the Slope table, with an optional override table.
- **Lock/unlock:** `MinTCCSpeed` sets the floor for TCC unlock/lock speeds. Lock/unlock spreads and the stall-logic floor are applied after that.
- **Data format:** `.BTC` tune files are CRLF text with one key line and one value line per field. `Trans_Presets.txt` and `Slope_Presets.txt` are tab-separated with a `#` comment header.
- **Python app:** the module docstring describes an output of TPS × Gear matrices for HP Tuners VCM Editor and TunerPro paste. It includes engines for shift points, pressure/TCC, shift time, TCC duty, a drag simulator, and XDF/BIN and datalog import.

## Reconstructed and verified so far

| Module | Status | Verification |
|---|---|---|
| `reconstructed/python/engines/calc_engine.py` — `CalcEngine` (mph, stall_slip, base/up/downshift slope, vss_calibration, calculate) | Hand-transcribed from the disassembly, every line cites its source line | `reconstructed/python/tests/verify_calc_engine.py`: 22,400 differential checks against the original bytecode, 0 failures |
| `reconstructed/python/engines/constants.py` — 54 plain-data constants | Generated from the original by `tests/gen_constants.py` (this ran the original module once, before the execution restriction; see below) | Not differentially checked |
| `reconstructed/python/engines/pressure_engine.py` — `PressureEngine` | Transcribed from the disassembly and corrected against it (e.g. the 07_14 negative-torque branch goes through cap and round; shudder relief has no intent multiplier) | Hand checks only (e.g. 68 °F row at 100 lb-ft = 121.5 psi). `tcc_apply_pressure_ramp` takes a `max_torque` argument the original never uses |
| `reconstructed/python/engines/torque_curve.py` — `TorqueCurve` | Transcribed from `TorqueCurve` disassembly (`01293..01457`) | Smoke tests only. `from_csv` drops rows with rpm ≤ 0 or unparseable cells |
| `reconstructed/python/engines/boost_curve.py` — `BoostCurve` | Transcribed from `01214..01280` | Smoke tests only |
| `reconstructed/python/engines/drag_simulator.py` — `DragSimulator` | Transcribed from `01863..01960`. `last_rpm` and `post_shift_clamp` are assigned but never read in the original, so they are omitted | Smoke test: 0–60 mph ≈ 5.56 s on a synthetic curve |
| `reconstructed/python/engines/bin_reader.py` — `BinReader` | Transcribed from `01160..01204` | Not yet tested |
| `reconstructed/python/engines/xdf.py` — `XDFAxis`, `XDFParameter`, `XDFDefinition` | Transcribed from `00905..01157`. `_apply_math` evaluates a charset-restricted expression from the XDF with empty builtins. `**` is allowed, so a crafted XDF can force heavy computation; treat as hardening to-do | All 22 XML `.xdf` files under `General Motors/` parse (357–1,177 parameters each). The other 30 `.xdf` files are 17 binaries and 13 empty placeholders, which are not XDFs |
| `reconstructed/python/engines/logimporter.py` — `LogImporter` | Transcribed from `01499..01831`. The WOT section skips rows with `rpm ≤ 0`, a guard the original may not have | Smoke test on a synthetic log: pandas and csv-module paths give identical results |

The differential test loads only the `CalcEngine` class body from the original `.pyc` (no PyQt6, no GUI, no network) and runs it side by side with the reconstruction on random inputs. Run it with:

```
python3 -I reconstructed/python/tests/verify_calc_engine.py "<path to the extracted .pyc>"
```

Found and fixed during verification: `vss_calibration` takes `(mode_idx, tire_dia, axle_ratio, vss_count, metric)`, modes 2 and 3 use the key `Gear Ratio`, and `TorqueCurve.is_empty` is a property.

Still not reconstructed: `ShiftTimeEngine`, `TCCDutyEngine`.

Only `CalcEngine` has a differential test. The other modules are hand-transcribed and checked by reading the disassembly and by smoke tests. Differential tests need the original run, and that is blocked until the user approves it.

Known issues noted in review (not yet fixed):
- `calc_engine.py`: the `init_lock_logic` option is read but never used. `calculate` has an unreachable `else base = min_speed` branch.
- `xdf.py`: `_apply_math` eval hardening (see above).

The differential test loads only the `CalcEngine` class body from the original `.pyc` (no PyQt6, no GUI, no network) and runs it side by side with the reconstruction on random inputs. Run it with:

```
python3 -I reconstructed/python/tests/verify_calc_engine.py "<path to the extracted .pyc>"
```

Found and fixed during verification: `vss_calibration` takes `(mode_idx, tire_dia, axle_ratio, vss_count, metric)`, modes 2 and 3 use the key `Gear Ratio`, and `TorqueCurve.is_empty` is a property.

Not yet reconstructed: `PressureEngine`, `ShiftTimeEngine`, `TCCDutyEngine`, `DragSimulator`, `TorqueCurve`, `LogImporter`, `XDFDefinition`/`BinReader`.

## Next steps

1. Reconstruct `ShiftTimeEngine` and `TCCDutyEngine` the same way.
2. Get approval to run the original under the oracle, then add differential tests for `PressureEngine`, `TorqueCurve`, `BoostCurve`, `DragSimulator`, and the readers.
3. Check the readers against the 33 `.BTC` files and the GM `.xdf`/`.bin` references (`BinReader` has not been run against a real `.bin` yet).
4. Build the merged Python 3.12 + PyQt6 app (6L80e TunerToolPro) and the GUI installer, then write the user guide.

## Attribution

Reference material under `General Motors/T43_6L80E_reference/` is third-party and carries its own licences (see that folder's README).
