# TunerToolPro User Guide

TunerToolPro is a Linux application for calculating GM 4L60E and 6L80E transmission
calibration values. It combines the shift-point calculator, the pressure and timing
tables, a dyno and drag simulator, a datalog analyzer, an XDF/BIN viewer, and the BC
Trans tune tools.

## Read this first

- **Check every value before you use it.** TunerToolPro calculates numbers. It does not
  know your engine, your converter, your cooler, or your road. Every value must be
  checked against your vehicle and a road test before it goes into a controller.
- **Verification status.** The calculation engines were rebuilt by reading the
  original program's compiled code, then checked against it on random inputs. The
  shift-point calculator matched on 22,400 checks. The pressure, timing, torque curve,
  boost, drag simulator, datalog and XDF/BIN readers matched on a further 12,285 checks.
  Every check matched. Two edge cases are not covered: a datalog row with zero RPM
  during wide-open throttle, which the original would crash on and this app skips, and
  the pandas code path.
- **Use at your own risk.** A transmission tune can damage a transmission, void a
  warranty, or cause an accident. The About menu shows the full disclaimer.

## Install

You need Linux with Python 3.10 or newer. Python 3.12 is what the original program
used, and it is what the tests were run with.

**Graphical installer**

```
python3 installer/install_tunertoolpro.py
```

Choose an install folder, leave the menu-entry box ticked if you want it, and press
**Install**. The installer creates a private Python environment, installs PyQt6 and
pandas into it, copies the application, and writes a launcher. It needs internet
access for the first install.

**Without a window** (for scripts or a server):

```
python3 installer/install_tunertoolpro.py --cli --target ~/TunerToolPro [--no-desktop]
```

**Starting the app.** Open the TunerToolPro menu entry, or run
`~/.local/share/TunerToolPro/run-tunertoolpro.sh`, or type `tunertoolpro` if the
installer added the command.

## Tabs at a glance

| Tab | What it does | What you need |
|---|---|---|
| Shift Points | Calculates upshift, downshift, TCC unlock and TCC lock speeds, and exports TPS x Gear matrices for VCM Editor or TunerPro | A starter profile (or your own numbers) |
| Pressure & Timing | Shows base shift, TCC apply and coast pressure tables, 4-speed shift times, and TCC duty maximums | Max torque and a driving intent |
| Dyno & Drag | Loads a dyno curve, adds an optional boost model, and runs a launch-to-quarter-mile simulation | A dyno CSV with rpm, hp, tq columns |
| Datalog | Imports a scan-tool CSV, lists the columns it recognized, and reports stall RPM, WOT slip, shift events and transmission temperature | A datalog CSV |
| XDF / BIN | Browses an XDF definition and reads values from a calibration BIN | An XDF file and a BIN file that you own |
| BCT Tunes | Opens and edits Bluecat `.BTC` tune files, applies transmission and slope presets, and shows shift speeds | `.BTC` files and the `Trans_Presets.txt` and `Slope_Presets.txt` files |

## Shift Points

1. Pick a **Profile**. Each profile sets the transmission ratios, tire size, axle,
   stall speed, shift RPMs and lock settings for a common setup. Start with the one
   that matches your car, then change the values to match yours.
2. Pick an **Intent** (for example *Racing* or *Eco*). The intent adds or replaces some
   values, such as shift RPM and firmness, and clamps the results to the ranges the
   original program uses. Choose *Custom* to keep the values exactly as the profile
   sets them.
3. Edit the values in the form. Changing the profile or intent resets the form, so
   make the profile and intent choices first.
4. Press **Calculate**. Four tables appear, one per tab: upshift MPH, downshift MPH,
   TCC unlock MPH and TCC lock MPH. Rows are shifts or gears. Columns are throttle
   position in steps of 6.25% from 0% to 100%.
5. Press **Export TPS x Gear** to save a tab-separated text file. Each block has a
   title, a header row of TPS percentages, and one row per shift or gear. Paste it into
   the VCM Editor or TunerPro tables, and check that the paste lines up.

Notes:
- **Lead mode** switches between an RPM-based and a torque-based lead. The torque-based
  lead uses 75% of the rated horsepower in this release. It does not yet read the dyno
  curve from the Dyno & Drag tab. **Stall-based lock floor** adds the stall-based floor
  to the lock tables.
- The per-gear **delays** use the original program's fallback of 0.5 s up and 0.15 s
  down for every gear. The original's own delay table was not recovered, so per-gear
  delays cannot be set here yet.

## Pressure & Timing

1. Pick a **Table**: base shift pressure, TCC apply pressure, coast pressure, 4-speed
   shift time, or TCC duty maximum.
2. Pick an **Intent**. The pressure tables use the pressure intents (*Daily*,
   *Towing / Heavy Load*, *Racing / Drag*, *Eco / Cruise*, *Hot ATF Protection*). The
   shift-time table uses *Normal*, *Performance*, *Towing* and *Eco*.
3. For the pressure tables, set **Max torque** (lb-ft) and the **psi cap**.
4. Press **Show**. Rows and columns are labelled with the table axes shown in the
   caption under the controls: for the pressure tables, rows are temperatures in °F and
   columns are torque in lb-ft; for shift time, rows are shifts and columns are torque
   in lb-ft; for TCC duty, rows are temperatures in °F and columns are line pressure
   in psi.

Not in this release: the TCC apply ramp tables (they depend on a model-year era and
have their own axes) and the 4-speed base table (its axes are not yet confirmed).

## Dyno & Drag

**Dyno curve**
1. Press **Load dyno CSV**. The file is rows of `rpm,hp,tq`, with an optional header
   row. Enter `0` for torque to have it calculated from horsepower
   (`hp x 5252 / rpm`). A blank cell is not allowed: the parser drops any row with a
   blank cell, and if no rows are left the app reports the problem. Rows with RPM of
   zero or less are also dropped.
2. The summary shows the peak horsepower and torque and the RPM where they occur.

**Forced induction (optional)**
Set the spool RPM, peak boost, peak RPM, redline boost and the torque gained per PSI,
then press **Apply boost**. Torque is multiplied by `1 + PSI x (torque per PSI) / 100`.
Leave the peak PSI at zero for a naturally aspirated engine.

**Drag simulation**
1. Pick a **Profile** and set the **Weight**.
2. Press **Run drag simulation**. The results show 0–30, 0–60 and 0–100 mph times, the
   eighth- and quarter-mile times and speeds, and the shift points. The chart shows
   speed and RPM over time.

The simulation assumes a fixed grip limit of 1.1 g, a drag coefficient of 9.0 and a
rolling resistance of 0.012. It does not model the converter's slip beyond the
calculated stall. Use it to compare setups, not to predict a time.

## Datalog

1. Export a CSV from your scan tool (for example VCM Scanner or HP Tuners). Turn on
   the PIDs for engine RPM, vehicle speed, throttle position, current gear, and, if you
   want temperature, transmission temperature.
2. Press **Open datalog CSV** and pick the file. The **Detected columns** table shows
   which of your headers were matched to each quantity. Check it first.
3. Pick the **Ratios and tire from** profile so WOT slip uses the right ratios.
4. The analysis shows:
   - **Shift events**: each gear change where the throttle was above 70%.
   - **Stall peak RPM**: the highest RPM seen with the vehicle under 5 mph and the throttle above 80%, which is a standstill WOT launch.
   - **WOT slip (%)**: the average converter slip under wide-open throttle.
   - **Trans temp range**: the lowest and highest temperature in the log, in the units
     the scan tool logged.

If the warning says there is no gear column, enable the *Current Gear* PID on the TCM.

## XDF / BIN

1. Press **Open XDF** and pick a definition file.
2. Press **Open BIN** and pick a calibration file that you own. The status line shows
   the size, the definition title and the number of parameters.
3. Type in the filter box to find a parameter. Select one to see its category, units
   and description, and its values from the BIN.

Tables show their axis values as row and column labels. Scalars show a single value.

The app does not include any XDF or BIN files. Use only files you have the right to
use.

## BCT Tunes

1. Press **Open .BTC tune** to load a Bluecat tune. The key and value list is
   editable. Changes stay in memory until you press **Save** or **Save As**.
2. The speed table shows the MPH each gear reaches at the RPMs you list (comma
   separated). It uses the tune's ratios, final drive (*Gear*) and tire size.
3. Press **Load presets folder** and pick the folder that holds `Trans_Presets.txt`
   and `Slope_Presets.txt`. Choose a preset and press **Apply**:
   - A transmission preset sets the gear count, ratios, VSS and lead values.
   - A slope preset sets the factor, offset, and up and down firmness.

The tune file is written byte-for-byte the way Bluecat wrote it, apart from the keys you
changed. Keep a copy of the original.

## Files and data

| File | Source | Used by |
|---|---|---|
| `*.BTC` tunes | Bluecat BC Trans | BCT Tunes |
| `Trans_Presets.txt`, `Slope_Presets.txt` | Bluecat BC Trans | BCT Tunes |
| Datalog `.csv` | Your scan tool | Datalog |
| Dyno `.csv` (rpm, hp, tq) | Your dyno | Dyno & Drag |
| `.xdf` and `.bin` | Your own calibration files | XDF / BIN |

## Troubleshooting

- **"PyQt6 not installed"** or a blank window: run the installer again, or start the app
  from the launcher so it uses its own environment.
- **"Cannot calculate"**: check the gear ratios. Enter at least two, separated by commas,
  with no units.
- **Datalog columns are missing**: open the log and compare the headers with the
  *Detected columns* table. Headers are matched by name, so rename them in a copy if
  they are unusual.
- **"no usable rows" when loading a dyno file**: a blank cell drops that row. Enter `0`
  in the torque column, or fill in every cell.

## Known limits (this release)

- Per-gear delays are fixed at the original's fallback values.
- The TCC apply ramp and 4-speed base pressure tables are not in the Pressure tab yet.
- The BCT tune file is not yet converted into shift-point inputs. The two tools share
  the data files, not the calculation.
- The BCT speed table uses the same 3.14 value for pi as the original. The Shift Points
  tab uses the exact value, so the two can differ by about 0.05%.
