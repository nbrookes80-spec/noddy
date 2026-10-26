# Installing TunerToolPro

This page covers installing, starting, updating and removing TunerToolPro on Linux.
For what the tool does, see the [README](../README.md). For how to use it, see the
[user guide](USER_GUIDE.md).

Tested on **Zorin OS 18.1** (Ubuntu 24.04 base) with Python 3.12.

---

## 1. Check what you need

| Need | How to check | How to get it |
|---|---|---|
| Python 3.10 or newer | `python3 --version` | Included with Zorin OS and Ubuntu 24.04 |
| Tkinter (for the Setup wizard) | `python3 -c "import tkinter"` | `sudo apt install python3-tk` |
| venv (for the private Python environment) | `python3 -m venv --help` | `sudo apt install python3-venv` |
| Internet access | — | Needed once, to download PyQt6 and pandas |
| git (to download the code) | `git --version` | `sudo apt install git` |

If the Setup wizard reports a missing module, run both commands:

```bash
sudo apt install python3-tk python3-venv
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

If none of these fix it, open an issue on GitHub and include the output of
`python3 --version` and the exact error text. Do not post your API key or your VIN.
