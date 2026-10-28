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

The Setup wizard works like a Windows installer. Its pages are: Welcome, License and terms
(accept to continue), Install folder, Select options, Ready to install, Installing, and
Completed. Setup creates a private Python environment, installs PyQt6 and pandas into it,
copies the application, and writes a launcher. The first install needs internet access.

Setup needs Tkinter and venv. On Zorin OS or Ubuntu, if the wizard reports them missing:

```
sudo apt install python3-tk python3-venv
```

**Optional AI assistant.** On the Select options page you can enable the AI assistant and
enter an Anthropic API key. The key is saved in your settings file, which only your account
can read (`~/.config/TunerToolPro/settings.json`). You can also add it later in the
AI Assistant tab. Questions go to api.anthropic.com only when you press Ask.

**Uninstalling.** Choose "Uninstall TunerToolPro" in the applications menu. It removes the
program folder, the menu entries, the desktop shortcut and the command. Your settings are
kept unless you tick "Also delete my settings and AI key".

**Starting the app.** Open the TunerToolPro menu entry, or run
`~/.local/share/TunerToolPro/run-tunertoolpro.sh`, or type `tunertoolpro` if the
setup added the command.

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
4. Pick an **Engine**. *TunerToolPro (CalcEngine)* uses the form values. *BC Trans
   (Calc_Shifts)* uses a loaded `.BTC` tune as written (see below). It needs a tune loaded
   first.
5. Press **Calculate**. Four tables appear, one per tab: upshift MPH, downshift MPH,
   TCC unlock MPH and TCC lock MPH. Rows are shifts or gears. Columns are throttle
   position in steps of 6.25% from 0% to 100%.
6. Press **Export TPS x Gear** to save a tab-separated text file. Each block has a
   title, a header row of TPS percentages, and one row per shift or gear. Paste it into
   the VCM Editor or TunerPro tables, and check that the paste lines up.

Notes:
- **Lead mode** switches between an RPM-based and a torque-based lead. The torque-based
  lead uses 75% of the rated horsepower in this release. It does not yet read the dyno
  curve from the Dyno & Drag tab. **Stall-based lock floor** adds the stall-based floor
  to the lock tables.
- The per-shift **delays** come from the transmission: a starter profile uses the Blue Cat data for its
  own transmission, and **Use this transmission** loads the data for the one you pick. A loaded BC Trans
  tune supplies its own delays for each shift. The original program's 0.5 s up and 0.15 s down is only the
  fallback when no data is known.

### Car and transmission

Pick a **Make** (GM, Holden, Pontiac or Ford) and a **Transmission**, then press **Use this transmission**.
It loads the gear ratios, the shift delays, the lead, and the converter-lock rules (minimum lock RPM and
the minimum, accelerator and WOT lock gears) for that unit, and resets the converter to Stock. Your tyres,
diff, weight, power and engine speeds are left alone. The choice is remembered.

GM units use Blue Cat Transmission Tool data (the 4L60/65, 4L70, 4L80/85, 6L80/90, 8L90 and 10L90 presets
and its shipped tunes). Units Blue Cat has no data for (Ford, 5L40E, and so on) use the Blue Cat class with
the same number of gears. They are marked *derived* and are starting points to check. Ford and the extra
Holden and Pontiac ratios are from published specifications and have not been checked against a car.

### Torque converter and differential

**Torque converter** moves the stall, idle, shift RPM and minimum lock RPM to suit the converter fitted
(Stock, Mild stall, High stall single plate, High stall triple plate, Other / custom) and switches the stall
lock floor on for any non-stock converter. The steps follow what Blue Cat's own base tunes do for a
high-stall build: idle +100, shift RPM +200, minimum lock RPM +100 on a 4-speed or +200 on 5 gears and up.
Type the converter's true flash stall (full throttle, output stopped, not the maker's rating) into **Stall
RPM** first if you know it. Choosing a type again starts from the stock numbers, so steps do not stack.

The notes box lists the TCM settings the app cannot calculate but that go with a loose converter: TCC desired
slip, apply and release, engine and transmission torque management, and the turbine transition times. Each
line says whether it comes from the VCM Performance guide, the HP Tuners videos, Blue Cat, or is a starting
point chosen here. No published source separates single-plate from triple-plate calibrations, so triple plate
uses the same calculated numbers as high stall single plate.

**Differential presets** set the Axle ratio from a list of common ratios and report the cruise RPM at
100 km/h in top gear and the first-gear top speed at your shift RPM. The diff ratio changes road speeds, not
shift RPM, so the shift tables move with it. Set the speedometer calibration for the new ratio.

### Load a BC Trans tune

Press **Load .BTC tune...** to fill the form from a Bluecat `.BTC` file. The intent is set
to *Custom* so no clamp changes the tune's numbers. A note under the form lists any value
that was outside the form's range and was shown at its nearest limit.

**Engine: TunerToolPro (CalcEngine)** calculates from the form values, which the tune
filled in as the table below shows. **Engine: BC Trans (Calc_Shifts)** runs the BC Trans
calculation on the tune itself. The tune's per-cell TCC grids, delays and every other key
are read directly, and the form is disabled, because the tune file is the input. To change
a value in that mode, edit the tune in BC Trans and load it again.

| BC Trans key | Shift Points input |
|---|---|
| `Gear` (labelled *Final*) | Axle ratio. The chain ratio is set to 1.0 |
| `Tire` | Tire diameter |
| `Ratio1` to `RatioN` | Gear ratios |
| `Idle`, `Stall`, `DownRPM` | Idle RPM, stall RPM, downshift RPM |
| `RPM1` to `RPMN` | Shift RPM for each gear |
| `Prep1` to `Prep(N-1)`, `React1` to `React(N-1)` | Per-gear delays (Prep + React on upshift) |
| `DownTime` | Downshift time |
| `Weight`, `RWHP` | Weight, rear-wheel HP |
| `Lead`, `AdvancedLead` | Lead value. `AdvancedLead` 0 is RPM lead, 1 is torque lead |
| `Factor`, `Offset`, `UpFactor`, `DownFactor` | TPS factor, TPS offset, upshift and downshift firmness |
| `ShiftSpread`, `LockSpread`, `ShiftLockSpread`, `UnlockShiftSpread` | The four spreads |
| `TCC_MinRpm` | Minimum TCC RPM (one value) |
| `MinLockGear`, `AccelLockGear`, `WOTLockGear` | Minimum TCC, accelerator-lock and WOT-lock gears |
| `StallLogic` | Stall-based lock floor |

Not used by the CalcEngine path: the per-cell TCC grids (`MinTCCRPM*`,
`TCC_UlckBeforeDown*`), `Trans`, `TBSlope`, `VSS`, `Metric`, the lock and unlock options
(`Lock>Unlock`, `Up>Down`, `AccelGearLock` and the rest) and the `Exp_*` export options.

The two engines are different calculations and give different tables.

- **CalcEngine** is this app's own Shift Points algorithm, rebuilt from the Python app.
- **BC Trans (Calc_Shifts)** is a port of the BC Trans `Calc_Shifts` routine. It was checked
  against the decompiled BC Trans code on the 33 shipped tunes and 400 random variants. Every
  cell agrees within 5e-05. It has not been checked against BC Trans running on a car, so
  check the final numbers in BC Trans before you use them.

BC Trans markers show as-is in the BC tables. On 6+ gear tunes, `318` in a lock table and
`317` in an unlock table mark a disabled TCC cell. On 4-gear tunes the markers are `255` (lock)
and `254` (unlock).

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

The **TCC apply pressure ramp** table has a *Model years* selector (2007 to 2010, 2011 to
2014, or 2015 and later). Each era has its own shape. Max torque and the psi cap do not
change that table, because the original's ramp does not read them, so those inputs are off.

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

## Vehicle

Use this tab to describe the car. The values feed the consistency check and the AI.

- **Car, engine, transmission.** Pick the transmission from the list. Stock 6L80, a modified
  6L80 (Sonnax zip kit, TransGo shift kit, billet flex plate, Circle D triple-plate converter),
  ZF 8HP, and the two Powerglide ratios are in the library. The ratios shown under the list
  come from the library and cite their source. Check them against your own transmission.
- **Final drive, tire, weight.** Save copies these three into the Shift Points tab, which is
  where the calculation uses them.
- **Power and torque.** Engine power and torque, as measured or as rated.
- **ECU limits.** The ECU torque limit and the redline, typed in from your calibration or scan
  tool. TunerToolPro does not read ECU files for these.
- **Check consistency.** Lists findings with a level. *Error* means two inputs contradict each
  other, for example a shift point above the redline. *Check* means a value is likely wrong or
  risky, for example a stall speed near idle. *Note* means a value is missing or a point to
  remember. Read each one before you change a setting.
- **Import EFILive export.** Choose a calibration or comparison CSV from EFILive. The tab shows
  how many values and tables were read. The summary goes to the AI when you ask a question.
  The export is kept only in memory for this session.

## AI Assistant: proposals and questions

When the AI assistant is on, it can read your Shift Points and Vehicle values, and it can
suggest changes.

- **Proposed changes** appear in a table with the setting, its current value, the proposed
  value and the reason. Press **Apply** to make the change, or **Reject** to drop it. Nothing
  changes until you press Apply.
- Apply only accepts values inside each setting's allowed range. A value outside the range is
  refused, and the AI is told why.
- **Questions** appear under the answer when the AI needs a value it cannot find, such as the
  number of gears. Type the answer in the question box and press Ask.
- After you apply a change, check the Vehicle tab findings. A change can create a new finding.
- The AI does not write to your car. To use a suggestion, make the change yourself in
  EFILive or HP Tuners. See `docs/ECU_TOOLS.md`.

## Files and data

| File | Source | Used by |
|---|---|---|
| `*.BTC` tunes | Bluecat BC Trans | BCT Tunes |
| `Trans_Presets.txt`, `Slope_Presets.txt` | Bluecat BC Trans | BCT Tunes |
| Datalog `.csv` | Your scan tool | Datalog |
| Dyno `.csv` (rpm, hp, tq) | Your dyno | Dyno & Drag |
| `.xdf` and `.bin` | Your own calibration files | XDF / BIN |
| EFILive calibration or comparison `.csv` export | EFILive Tune, Export | Vehicle tab (Import EFILive export) |
| `vehicle.json` | Written by the Vehicle tab | Vehicle |

## Troubleshooting

- **"not an EFILive export"** when importing: the file must start with "EFILive Calibration
  Export" or "EFILive Comparison Export". Export it again as CSV from EFILive Tune.
- **"Not readable: check the gear ratios"** in the AI context: fix the ratios on the Shift Points
  tab first, so the AI sees your inputs.

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

- ECU limits and redline are typed in. TunerToolPro does not read ECU files for them.
- EFILive datalogs (`.log`) are not read yet. Their format is not confirmed.
- HP Tuners `.hpt`, `.hpl` and `.HPTdb` files are encrypted and are not read. Use an HP Tuners
  text or CSV export instead, once that reader exists.
- The `.ctz` and `.calz` EFILive files are not read. Use the CSV export.
- The AI cannot search the web. It asks you for missing values.
- TunerToolPro never writes to a controller. Make each change in EFILive or HP Tuners yourself.

- Without a loaded tune, per-gear delays are the original's fallback values.
- With the CalcEngine path, a loaded tune only sets the Shift Points inputs. Its per-cell
  TCC grids are not used. The BC Trans engine uses the whole tune.
- The BC Trans engine has no form. It cannot take changes made in the form.
- The 4-speed base pressure table's axes are not confirmed against the original.
- The BCT speed table uses the same 3.14 value for pi as the original. The Shift Points
  tab uses the exact value, so the two can differ by about 0.05%.
