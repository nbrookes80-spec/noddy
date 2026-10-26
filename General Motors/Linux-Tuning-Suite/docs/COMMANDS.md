# TunerToolPro commands

Every command here runs on Linux (Zorin OS 18.1 or Ubuntu 24.04 were the test systems).
Commands are shown from the folder they must run in. The tool never sends anything to a
vehicle. Nothing here writes to a controller.

## Install, start and remove

| Task | Command | Run from |
|---|---|---|
| Install with the Setup wizard | `python3 installer/install_tunertoolpro.py` | the project folder |
| Start the app (after install) | `tunertoolpro` | any folder |
| Start the app (menu entry) | open **TunerToolPro** in the applications menu | - |
| Start the app (launcher script) | `~/.local/share/TunerToolPro/run-tunertoolpro.sh` | any folder |
| Uninstall | open **Uninstall TunerToolPro** in the applications menu, or run `~/.local/share/TunerToolPro/uninstall_tunertoolpro.py` | - |
| Uninstall from the project copy | `python3 installer/install_tunertoolpro.py --uninstall` | the project folder |

The wizard needs Tkinter and venv on the first run:

```
sudo apt install python3-tk python3-venv
```

Setup creates a private Python environment and installs PyQt6 and pandas into it. The first
install needs internet access.

## Run from the source folder (no install)

```
cd "General Motors/Linux-Tuning-Suite/app"
python3 -m venv venv && . venv/bin/activate
pip install -r requirements.txt
python3 -m tunertoolpro
```

Run it from the `app` folder, because the package is found from there.

## Tests

Run the app tests from the `app` folder. Set `QT_QPA_PLATFORM=offscreen` so the window tests
run without a display:

```
cd "General Motors/Linux-Tuning-Suite/app"
QT_QPA_PLATFORM=offscreen python3 -m unittest discover -s tests -t .
```

Expected result at this commit: 111 tests, one skipped when the reference XDF file is absent.

Run the installer tests from the `installer` folder. They use a scratch home folder, so your
real settings are not touched:

```
cd "General Motors/Linux-Tuning-Suite/installer"
HOME=$(mktemp -d) python3 -m unittest discover -s tests
```

Expected result: 9 tests pass.

Check the code for mistakes with pyflakes (install it first with `pip install pyflakes`):

```
cd "General Motors/Linux-Tuning-Suite/app"
python3 -m pyflakes tunertoolpro tests
```

One warning is known and left in place: an unused variable `init_lock` in
`tunertoolpro/engines/calc_engine.py`.

## Summarise an EFILive calibration export

Prints the readable summary that the AI also receives. Read-only.

```
cd "General Motors/Linux-Tuning-Suite/app"
python3 -I -m tunertoolpro.efilive_export "/path/to/export.csv"
```

`-I` stops Python from loading modules from the current folder. Keep the export in its own
folder. Calibration and comparison exports are both accepted.

## Settings and data locations

| What | Where | Notes |
|---|---|---|
| App settings and AI key | `~/.config/TunerToolPro/settings.json` | Written with permissions 0600 |
| Vehicle profile | `~/.config/TunerToolPro/vehicle.json` | Car, engine, transmission, final drive, ECU limits |
| Install folder | `~/.local/share/TunerToolPro` | Holds `install.json` (what was installed) |
| Command | `~/.local/bin/tunertoolpro` | Created by the installer |
| Menu entries | `~/.local/share/applications/` | Desktop and applications menu |

To move the settings folder, set `TUNERTOOLPRO_HOME` to another folder before starting the app:

```
TUNERTOOLPRO_HOME=/path/to/folder tunertoolpro
```

`XDG_CONFIG_HOME` also changes the settings base folder when `TUNERTOOLPRO_HOME` is not set.

## Environment variables

| Variable | Effect |
|---|---|
| `TUNERTOOLPRO_HOME` | Folder for settings and the vehicle profile |
| `XDG_CONFIG_HOME` | Base folder for settings, when `TUNERTOOLPRO_HOME` is not set |
| `QT_QPA_PLATFORM=offscreen` | Runs the window without a display (tests and screenshots) |

## What the commands do not do

- They do not connect to EFILive, HP Tuners or any scan tool.
- They do not change a controller's calibration.
- The AI assistant only sends text to the Anthropic API when you press Ask, and only if you
  have turned it on and saved a key.
