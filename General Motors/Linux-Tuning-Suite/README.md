# TunerToolPro

**A Linux desktop tool for GM 4L60E and 6L80E transmission calibration work.**

TunerToolPro calculates shift points, pressure and timing tables, TCC values and
dyno/drag results. It reads the files that common GM tuning tools export, and it keeps
your vehicle details in one place. It is a calculator and a planning aid. It never
writes to a vehicle or a controller.

> **Read before use.** Every value it produces must be checked against your vehicle,
> your converter, your cooler and a road test before it goes into a controller. A
> transmission calibration can damage the transmission, void a warranty or cause an
> accident. You use this tool at your own risk. See [Safety](#safety).

---

## Contents

- [What it does](#what-it-does)
- [What it can read](#what-it-can-read)
- [What it does not do](#what-it-does-not-do)
- [Requirements](#requirements)
- [Install](#install)
- [Documentation](#documentation)
- [Status](#status)
- [Help wanted](#help-wanted)
- [Safety](#safety)
- [Licence and attribution](#licence-and-attribution)

---

## What it does

TunerToolPro opens with seven tabs. Each tab is one job.

| Tab | What it does |
|---|---|
| **Shift Points** | Calculates upshift, downshift, TCC unlock and TCC lock speeds from your gear ratios, final drive, tyre size, stall speed and shift settings. Exports TPS x Gear matrices for VCM Editor or TunerPro. Can load a Bluecat `.BTC` tune and calculate it the way BC Trans does. |
| **Vehicle** | Stores your car, engine, transmission, final drive, tyre, weight, power, torque, ECU torque limit and redline in a profile. Runs consistency checks that flag contradictory or risky values. Imports an EFILive calibration or comparison export. |
| **Pressure & Timing** | Builds base shift, TCC apply and coast pressure tables, 4-speed shift times and TCC duty maximums from torque and driving intent. |
| **Dyno & Drag** | Loads a dyno curve, adds an optional boost model, and simulates a launch to a quarter mile. |
| **Datalog** | Imports a scan-tool CSV, lists the columns it recognised, and reports stall RPM, wide-open-throttle slip, shift events and transmission temperature. |
| **XDF / BIN** | Browses an XDF definition and reads values from a calibration BIN file that you own. |
| **BCT Tunes** | Opens and edits Bluecat `.BTC` tune files, applies transmission and slope presets, and shows the resulting shift speeds. |
| **AI Assistant** *(optional)* | Answers questions about your values using an Anthropic API key. It can propose changes, but a change takes effect only when you press **Apply** in the tab that owns that setting. |

### Highlights

- **Calculation engines rebuilt from the original program.** The shift-point, pressure,
  timing, torque-curve, boost, drag and reader engines were re-derived from the compiled
  code of the original Windows tools and checked against them. Every check matched:
  34,685 comparisons, with the two edge cases listed in
  [Status](#status).
- **Vehicle library.** Built-in transmission data for the stock 6L80, a modified 6L80,
  ZF 8HP45/8HP70, and the 2-speed Powerglide, with the source of each ratio listed.
- **Plain-language consistency checks.** Findings are labelled *Error*, *Check* or *Note*,
  so you can see what contradicts what before you change a setting.
- **Safe AI use.** The assistant reads your settings and proposes changes. It cannot
  write to a controller, and every value it proposes must fall inside the allowed range
  of that setting.
- **Runs on Linux and Windows.** On Linux it installs with a Start-menu entry, a desktop
  shortcut and a `tunertoolpro` command. On Windows, download the `TunerToolPro-<version>-setup.exe`
  installer built by the *Windows build* workflow (Actions tab, or a release). Settings live in
  `%APPDATA%\TunerToolPro` and are kept when you uninstall. The Windows build is new and has only
  been built by CI, not yet tried on a Windows PC.

---

## What it can read

| File | Source | Used by |
|---|---|---|
| EFILive calibration or comparison export (`.csv`, "EFILive Calibration Export" / "EFILive Comparison Export") | EFILive Tune, *Export* | Vehicle tab |
| Scan-tool datalog (`.csv`) | Any scan tool that writes CSV | Datalog tab |
| Dyno curve (`.csv` with rpm, hp, tq) | Your dyno | Dyno & Drag tab |
| XDF definition and calibration BIN (files you own) | Your tuning tools | XDF / BIN tab |
| Bluecat `.BTC` tunes, `Trans_Presets.txt`, `Slope_Presets.txt` | Bluecat Transmission Tool | BCT Tunes and Shift Points tabs |

## What it does not do

- **It does not connect to a vehicle, a scan tool or a controller.** It has no live
  data link and does not flash or write calibrations.
- **It does not read every tuning-tool format.** HP Tuners `.hpt`, `.hpl` and `.HPTdb`
  files are encrypted and are not read. EFILive `.calz` and `.ctz` files are not read.
  EFILive datalog `.log` files are not read yet. The EFILive **CSV export** is the route
  that works today.
- **It does not know your vehicle.** It uses only the numbers you give it.
- **It does not send your data anywhere** unless you turn on the AI Assistant and press
  Ask. Then only your question and the values shown in the tab go to the Anthropic API.

---

## Requirements

- Linux with a desktop: tested on **Zorin OS 18.1** (based on Ubuntu 24.04).
- **Python 3.10 or newer**, with Tkinter and venv for the installer:
  `sudo apt install python3-tk python3-venv`
- The `libxcb-cursor0` system package for the program window: `sudo apt install libxcb-cursor0`.
- An internet connection for the first install (it downloads PyQt6 and pandas).
- Optional: an Anthropic API key for the AI Assistant.

---

## Install

The full steps, with troubleshooting, are in **[docs/INSTALL.md](docs/INSTALL.md)**.
The short version:

```bash
git clone -b claude/keen-hawking-ite6nw https://github.com/nbrookes80-spec/noddy.git
cd noddy/"General Motors/Linux-Tuning-Suite"
python3 installer/install_tunertoolpro.py
```

The Setup wizard installs the program, creates a private Python environment, and adds
the menu entries and the `tunertoolpro` command. To remove it, choose
**Uninstall TunerToolPro** from the applications menu.

To run it from the source folder without installing, see
[docs/COMMANDS.md](docs/COMMANDS.md).

---

## Documentation

| Guide | For |
|---|---|
| [docs/INSTALL.md](docs/INSTALL.md) | Installing, starting, updating and removing the tool |
| [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | How to use each tab, with the limits of this release |
| [docs/COMMANDS.md](docs/COMMANDS.md) | Commands, tests, settings locations and environment variables |
| [docs/ECU_TOOLS.md](docs/ECU_TOOLS.md) | Working alongside EFILive and HP Tuners, and why the AI does not write to a car |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Project layout, how the engines were rebuilt, and the verification results |
| [docs/DESIGN_TEMPLATE.md](docs/DESIGN_TEMPLATE.md) | The colour palette and interface components |

---

## Status

**Version 0.1.0.** Early release.

| Area | State |
|---|---|
| Calculation engines | Matched against the original program on 34,685 checks, with 0 failures. Two edge cases are not covered (see the user guide). |
| Automated tests | 111 app tests pass headless (one skipped when a reference file is absent). 9 installer tests pass. |
| Installer | Tested in command-line mode. The graphical uninstall window and reinstall path are not yet tested on a desktop. |
| On a real vehicle | **Not yet validated.** No calibration produced by this tool has been road-tested and reported back. |
| EFILive | CSV export import works, and it has been checked against six sample exports. The EFILive log format is not yet read. |
| HP Tuners | Not read. The encrypted files cannot be used without HP Tuners' own text or CSV export, and no reader for that export exists yet. |

---

## Help wanted

- **Sample files.** EFILive datalogs (`.log`) and HP Tuners text or CSV exports, so the
  readers can be extended. Share only files you are allowed to share, and remove any
  VIN or personal data first.
- **Testers on Zorin OS and Ubuntu**, especially for the install, uninstall and
  reinstall steps.
- **Road-test reports.** Tell us what you checked and what you changed. Honest reports,
  including ones where a value was wrong, are the most useful feedback.
- **Bug reports and suggestions**, through GitHub issues.

---

## Safety

- TunerToolPro calculates. **You** decide what goes into a controller, and you make each
  change yourself in your own tuning tool.
- Check every value against your vehicle and your road test. Do not rely on the
  consistency checks alone. They catch common contradictions, not every mistake.
- A transmission calibration can cause damage, loss of control or a crash. Do not use
  values you do not understand.
- The AI Assistant can be wrong. Treat its answers and proposals as suggestions to check.
- Only use tuning files, calibrations and data that you own or have permission to use.

---

## Licence and attribution

TunerToolPro is free software: you can redistribute it and/or modify it under the terms of
the **GNU General Public License v3.0**. See [LICENSE](LICENSE). It is distributed without
any warranty.

Some of the material used to rebuild the calculations came from third-party sources. It is
not included in this folder, and its own licences apply to it.

Bluecat, HP Tuners, EFILive and GM are the names of their owners. This project is not
affiliated with or endorsed by any of them.
