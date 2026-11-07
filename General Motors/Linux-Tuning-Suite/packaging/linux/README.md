# Linux packaging: the AppImage

One file. The user downloads it, marks it executable, and double-clicks it. No Python, no
`pip`, no `apt install`, no root, no clone of this repository.

```bash
./packaging/linux/build_appimage.sh
# -> dist/TunerToolPro-<version>-x86_64.AppImage
```

Docker is the only requirement on the build machine.

## How a user runs it

```bash
chmod +x TunerToolPro-0.1.1-x86_64.AppImage
./TunerToolPro-0.1.1-x86_64.AppImage
```

## The one host dependency

The AppImage carries Python, PyQt6, pandas, pyserial, Qt and `libxcb-cursor0`. It does **not**
carry `libgl1` and `libegl1`, and that is deliberate: the host's `libGL` has to match the host's
GPU driver, so a bundled Mesa copy breaks hardware acceleration on a machine running, say, an
NVIDIA driver. Both are on the AppImage project's exclude list for that reason, and every Linux
desktop has them already. `tests/test_appimage_runs_clean.py` pins this down — it starts the
AppImage in a bare container with those two packages and nothing else, so if the bundle ever
starts leaning on a third host library, that test fails.

## How a user's settings carry over

Settings land in `~/.config/TunerToolPro`, the same folder `settings.py` uses everywhere, so a
user can move between an AppImage and a wizard-installed copy without losing their vehicle
profile or their AI key.

## Why these choices

**Why AppImage and not Flatpak or a .deb.** The app talks to ELM327 adapters over USB serial
and Bluetooth RFCOMM. An AppImage is unsandboxed, so `/dev/ttyUSB*` and RFCOMM work exactly as
they do from a terminal. Flatpak would sandbox both and need portal work before the Link tab
could see an adapter at all. A `.deb` would cover only Debian and Ubuntu derivatives, and would
still have to pull PyQt6 from the distro rather than carrying a known-good copy.

**Why the build runs in a container.** An AppImage carries its own libraries but calls the
host's glibc, and glibc is backwards compatible only. The oldest system the build runs on
becomes the oldest system the result runs on. Building on the Zorin 18.1 development machine
would set that floor at glibc 2.39 and lock out most other users; the Ubuntu 22.04 container
sets it at 2.35, which covers Ubuntu 22.04+, Zorin 17 and 18, Mint 21+, Debian 12+ and
Fedora 36+.

**Why PyInstaller.** The app was already written for it: `gui/splash.py` resolves its assets
through `sys._MEIPASS`, and `app/run_tunertoolpro.py` exists because PyInstaller cannot start a
module that uses relative imports. The Windows build in `../windows` uses the same tool.

**Why the Qt libraries are installed in the build container.** Nothing in the container opens a
window, but PyInstaller's dependency scan copies the libraries Qt's xcb platform plugin links
against into the bundle. That is what removes `sudo apt install libxcb-cursor0` from the user's
install steps — the single most common reason the app installs but will not open.

**Why onedir rather than onefile.** The AppImage is already a single file. A onefile build would
unpack a second copy of itself into `/tmp` on every start, for no gain.

## What this does not replace, yet

`installer/install_tunertoolpro.py` is the Tkinter Setup wizard: it builds a virtual
environment, downloads PyQt6 and pandas, copies the app, and writes the menu entries, the
desktop shortcut and the `~/.local/bin/tunertoolpro` command.

Inside an AppImage none of the first half applies — Python and every dependency are already in
the file, and the image is read-only. Only the second half still has a job: putting the app in
the applications menu so it is not just a file in `~/Downloads`.

**This is an open decision, not a settled one.** Three ways out:

1. **Leave both.** The wizard stays the "install from source" path; the AppImage is the
   "just run it" path. Two paths to document and keep working.
2. **Retire the wizard; integrate from inside the app.** First run offers "add TunerToolPro to
   your applications menu", which writes one `.desktop` file pointing at wherever the AppImage
   sits. This is what most AppImages do, and it deletes 666 lines of installer.
3. **Retire the wizard; let the desktop do it.** Ship nothing, and point users at AppImageLauncher
   or their desktop's own "integrate" prompt. Least code, least control over the experience.

Option 2 is the recommendation, but it is a product call about what a first run should feel
like, and it is tangled up with the Basic/Advanced mode question — both are "what does a new
user meet first". Worth deciding together rather than separately.

## Known limits

- **x86-64 only.** An arm64 AppImage needs an arm64 build container and an arm64 appimagetool.
  Nothing in the design prevents it; it is not built.
- **`appimagetool` is not pinned.** Upstream publishes a rolling `continuous` release only, so a
  rebuild months from now may use a newer tool.
- **FUSE.** Older AppImage tooling needed FUSE 2 on the user's machine. The AppImage built here
  can always be run with `--appimage-extract-and-run` if a host lacks it.
