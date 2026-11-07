# Installing TunerToolPro

This page covers installing, starting, updating and removing TunerToolPro on Linux.
For what the tool does, see the [README](../README.md). For how to use it, see the
[user guide](USER_GUIDE.md).

Tested on **Zorin OS 18.1** (Ubuntu 24.04 base) with Python 3.12.

There are two ways to install. Pick one:

| Way | Best for | What the user needs |
|---|---|---|
| **[The AppImage](#the-appimage-one-file-nothing-to-install)** | Running it, and sharing it with someone else | Any Linux desktop |
| **[The Setup wizard](#install-from-source-with-the-setup-wizard)** | Working on the code, or installing from a clone | Python 3.10+, Tkinter, venv, internet |

---

## The AppImage: one file, nothing to install

Download `TunerToolPro-0.1.1-x86_64.AppImage`, then:

```bash
chmod +x TunerToolPro-0.1.1-x86_64.AppImage
./TunerToolPro-0.1.1-x86_64.AppImage
```

That is the whole install. No Python, no `pip`, no root, no clone of this repository. Python,
PyQt6, pandas, pyserial and the Qt libraries are all inside the file, including
`libxcb-cursor0` — the one that otherwise lets the app install but not open.

**It runs on** any x86-64 Linux **desktop** with glibc 2.35 or newer: Ubuntu 22.04+, Zorin 17
and 18, Mint 21+, Debian 12+, Fedora 36+.

**The one thing it does not carry** is the host's graphics stack: `libgl1` and `libegl1`. Every
desktop Linux install already has them, because the desktop itself needs them, so in practice
there is nothing to install. They are deliberately left out rather than forgotten: the host's
`libGL` has to match the host's GPU driver, so a bundled copy would break hardware acceleration
on a machine with, for example, an NVIDIA driver. A bare server image without a desktop does
need `sudo apt install libgl1 libegl1` first.

**Settings** go to `~/.config/TunerToolPro`, the same folder a wizard-installed copy uses, so
you can move between the two without losing your vehicle profile or your AI key.

**It does not add itself to the applications menu.** Today it is a file you run from wherever
you saved it. Your desktop may offer to integrate it, or you can use AppImageLauncher.

**To build one** (Docker is the only requirement):

```bash
./packaging/linux/build_appimage.sh
# -> dist/TunerToolPro-0.1.1-x86_64.AppImage
```

See [packaging/linux/README.md](../packaging/linux/README.md) for how the build works and why.

---

## Install from source with the Setup wizard

## 1. Check what you need

| Need | How to check | How to get it |
|---|---|---|
| Python 3.10 or newer | `python3 --version` | Included with Zorin OS and Ubuntu 24.04 |
| Tkinter (for the Setup wizard) | `python3 -c "import tkinter"` | `sudo apt install python3-tk` |
| venv (for the private Python environment) | `python3 -m venv --help` | `sudo apt install python3-venv` |
| Internet access | — | Needed once, to download PyQt6 and pandas |
| git (to download the code) | `git --version` | `sudo apt install git` |
| Qt window library (xcb-cursor) | `ldconfig -p \| grep libxcb-cursor` | `sudo apt install libxcb-cursor0` |

If the Setup wizard reports a missing module, run both commands:

```bash
sudo apt install python3-tk python3-venv
```

The program window also needs `libxcb-cursor0`. Without it the app installs but does not open, and the
Setup log shows a warning. Install it with:

```bash
sudo apt install libxcb-cursor0
```

---

## 2. Get the code

```bash
git clone -b claude/keen-hawking-ite6nw https://github.com/nbrookes80-spec/noddy.git
cd noddy/"General Motors/Linux-Tuning-Suite"
```

You can also download the repository as a ZIP from GitHub and unpack it. The installer
must be run from inside the `Linux-Tuning-Suite` folder.

---

## 3. Run the Setup wizard

```bash
python3 installer/install_tunertoolpro.py
```

The wizard has these pages:

1. **Welcome.** Click **Next**.
2. **License and terms.** Read the terms and accept them to continue.
3. **Install folder.** The default is `~/.local/share/TunerToolPro`. Change it if you want
   the program somewhere else.
4. **Select options.** Choose:
   - the desktop shortcut and the applications-menu entry;
   - whether to enable the **AI Assistant**. If you enable it, enter your Anthropic API key
     here, or add it later in the AI Assistant tab.
5. **Ready to install.** Click **Install**.
6. **Installing.** The first install takes a few minutes, because it downloads PyQt6 and
   pandas.
7. **Completed.** Click **Finish**. You can start the program straight away.

### What the installer puts on your computer

| Item | Location |
|---|---|
| Program and private Python environment | `~/.local/share/TunerToolPro` |
| Applications-menu entry | `~/.local/share/applications/` |
| Desktop shortcut | `~/Desktop` (if you chose it) |
| Command | `~/.local/bin/tunertoolpro` |
| Settings and AI key | `~/.config/TunerToolPro/settings.json` (readable only by your account) |
| Vehicle profile | `~/.config/TunerToolPro/vehicle.json` |

Settings are kept when you uninstall, unless you tick **Also delete my settings and AI key**.

---

## 4. Start TunerToolPro

Use any of these:

- open **TunerToolPro** from the applications menu or the desktop shortcut;
- run `tunertoolpro` in a terminal;
- run `~/.local/share/TunerToolPro/run-tunertoolpro.sh`.

If `tunertoolpro` is not found, open a new terminal first. If it is still not found, use
the launcher path above. The command lives in `~/.local/bin`, which must be on your `PATH`.

The app opens on the **Shift Points** tab. A good first step is the **Vehicle** tab, to
enter your car, engine and transmission, then run **Check consistency**.

---

## 5. Check the install

Start the app with one of the methods in section 4. If the window opens, the install works.
To run the developers' test suite from the source folder, see [COMMANDS.md](COMMANDS.md#tests).

---

## 6. Update

The installer copies the program into the install folder. To update:

1. Download the new version (`git pull` in the repository folder, or a new ZIP).
2. Run the installer again from the `Linux-Tuning-Suite` folder and choose the same
   install folder.

Your settings and vehicle profile are kept. **The reinstall path has not been tested on a
desktop yet.** Back up `~/.config/TunerToolPro` before you update, if the profile matters to you.

---

## 7. Uninstall

Either:

- choose **Uninstall TunerToolPro** from the applications menu; or
- run the uninstaller directly:

  ```bash
  python3 ~/.local/share/TunerToolPro/uninstall_tunertoolpro.py
  ```

  or, from the repository folder:

  ```bash
  python3 installer/install_tunertoolpro.py --uninstall
  ```

The uninstall window removes the program folder, the menu entry, the desktop shortcut
and the command. It keeps your settings unless you tick **Also delete my settings and AI
key**.

**Note:** the graphical uninstall window has not yet been tested on a desktop.

---

## Troubleshooting

| Problem | What to do |
|---|---|
| The wizard says Tkinter is missing | `sudo apt install python3-tk`, then run the wizard again |
| The wizard says venv is missing | `sudo apt install python3-venv`, then run the wizard again |
| The install stops while downloading | Check your internet connection, then run the installer again |
| `tunertoolpro: command not found` | Open a new terminal, or run `~/.local/share/TunerToolPro/run-tunertoolpro.sh` |
| The window does not open from the terminal | Run `~/.local/share/TunerToolPro/run-tunertoolpro.sh` and copy the error text into a GitHub issue |
| The AI Assistant says no key is set | Enter the key in the AI Assistant tab, or in the installer's options page |
| You want to run without installing | See [COMMANDS.md](COMMANDS.md#run-from-the-source-folder-no-install) |
| The AppImage does nothing when double-clicked | Mark it executable: `chmod +x TunerToolPro-*.AppImage`, or run it from a terminal to see the error |
| The AppImage says something about FUSE | Run it as `./TunerToolPro-*.AppImage --appimage-extract-and-run` |
| The AppImage reports a GLIBC version error | The machine is older than Ubuntu 22.04. Use the Setup wizard instead |
| The AppImage says `libGL.so.1` or `libEGL.so.1` is missing | A system with no desktop installed: `sudo apt install libgl1 libegl1` |

If none of these fix it, open an issue on GitHub and include the output of
`python3 --version` and the exact error text. Do not post your API key or your VIN.
