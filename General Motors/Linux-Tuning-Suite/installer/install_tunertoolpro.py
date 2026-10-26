#!/usr/bin/env python3
"""TunerToolPro installer.

Creates a private Python virtual environment, installs the requirements, copies the
application, and writes a launcher. It can also add a desktop menu entry.

Run the GUI installer:      python3 install_tunertoolpro.py
Run it without a window:    python3 install_tunertoolpro.py --cli --target DIR [--no-desktop]

Only the standard library is needed to run the installer itself. Tkinter is used for
the window and is optional in --cli mode.
"""

import argparse
import shutil
import subprocess
import sys
import venv
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP_SRC = HERE.parent / 'app'
REQUIREMENTS = APP_SRC / 'requirements.txt'
DEFAULT_TARGET = Path.home() / '.local' / 'share' / 'TunerToolPro'
MIN_PYTHON = (3, 10)


def check_python():
    if sys.version_info < MIN_PYTHON:
        raise RuntimeError(f'Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is required; '
                           f'this is {sys.version.split()[0]}')


def create_venv(target, log):
    venv_dir = target / 'venv'
    log(f'Creating virtual environment in {venv_dir}')
    venv.EnvBuilder(with_pip=True, clear=True).create(venv_dir)
    return venv_dir


def install_requirements(venv_dir, log):
    pip = venv_dir / 'bin' / 'pip'
    log('Installing PyQt6 and pandas (this can take a few minutes)')
    subprocess.run([str(pip), 'install', '--upgrade', 'pip'], check=True)
    subprocess.run([str(pip), 'install', '-r', str(REQUIREMENTS)], check=True)


def copy_app(target, log):
    dest = target / 'app'
    log(f'Copying application to {dest}')
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(APP_SRC, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    return dest


def write_launcher(target, venv_dir, log):
    launcher = target / 'run-tunertoolpro.sh'
    launcher.write_text(
        '#!/bin/sh\n'
        f'cd "{target / "app"}" || exit 1\n'
        f'exec "{venv_dir / "bin" / "python"}" -m tunertoolpro "$@"\n'
    )
    launcher.chmod(0o755)
    log(f'Wrote launcher {launcher}')
    return launcher


def write_desktop_entry(launcher, log):
    apps = Path.home() / '.local' / 'share' / 'applications'
    apps.mkdir(parents=True, exist_ok=True)
    entry = apps / 'tunertoolpro.desktop'
    entry.write_text(
        '[Desktop Entry]\n'
        'Type=Application\n'
        'Name=TunerToolPro\n'
        'Comment=GM 4L60E / 6L80E transmission calibration tools\n'
        f'Exec="{launcher}"\n'
        'Terminal=false\n'
        'Categories=Utility;Engineering;\n'
    )
    bin_dir = Path.home() / '.local' / 'bin'
    bin_dir.mkdir(parents=True, exist_ok=True)
    link = bin_dir / 'tunertoolpro'
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(launcher)
    log(f'Added menu entry {entry} and command {link}')


def install(target, desktop=True, log=print):
    """Install into target. Returns the launcher path."""
    check_python()
    if not REQUIREMENTS.exists():
        raise FileNotFoundError(f'missing {REQUIREMENTS}')
    target = Path(target).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    venv_dir = create_venv(target, log)
    install_requirements(venv_dir, log)
    copy_app(target, log)
    launcher = write_launcher(target, venv_dir, log)
    if desktop:
        write_desktop_entry(launcher, log)
    log(f'Done. Start TunerToolPro with: {launcher}')
    return launcher


def run_gui():
    import threading
    import tkinter as tk
    from tkinter import filedialog, messagebox, scrolledtext

    root = tk.Tk()
    root.title('TunerToolPro installer')
    root.geometry('640x460')

    target_var = tk.StringVar(value=str(DEFAULT_TARGET))
    desktop_var = tk.BooleanVar(value=True)

    row = tk.Frame(root)
    row.pack(fill='x', padx=12, pady=(12, 4))
    tk.Label(row, text='Install folder').pack(side='left')
    tk.Entry(row, textvariable=target_var, width=56).pack(side='left', padx=6, fill='x', expand=True)

    def browse():
        chosen = filedialog.askdirectory(initialdir=target_var.get())
        if chosen:
            target_var.set(chosen)

    tk.Button(row, text='Browse...', command=browse).pack(side='left')
    tk.Checkbutton(root, text='Add a menu entry and a tunertoolpro command',
                   variable=desktop_var).pack(anchor='w', padx=12)
    log_box = scrolledtext.ScrolledText(root, height=18, state='disabled')
    log_box.pack(fill='both', expand=True, padx=12, pady=8)
    install_btn = tk.Button(root, text='Install')
    install_btn.pack(pady=(0, 12))

    def write_log(msg):
        def append():
            log_box.configure(state='normal')
            log_box.insert('end', msg + '\n')
            log_box.see('end')
            log_box.configure(state='disabled')
        root.after(0, append)

    def worker():
        try:
            install(target_var.get(), desktop=desktop_var.get(), log=write_log)
            root.after(0, lambda: messagebox.showinfo('TunerToolPro', 'Installation finished.'))
        except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
            message = str(exc)
            write_log(f'FAILED: {message}')
            root.after(0, lambda: messagebox.showerror('Installation failed', message))
        finally:
            root.after(0, lambda: install_btn.configure(state='normal'))

    def start():
        install_btn.configure(state='disabled')
        threading.Thread(target=worker, daemon=True).start()

    install_btn.configure(command=start)
    root.mainloop()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Install TunerToolPro')
    parser.add_argument('--cli', action='store_true', help='install without a window')
    parser.add_argument('--target', default=str(DEFAULT_TARGET), help='install folder')
    parser.add_argument('--no-desktop', action='store_true', help='skip the menu entry')
    args = parser.parse_args(argv)
    if not args.cli:
        run_gui()
        return 0
    try:
        install(args.target, desktop=not args.no_desktop, log=print)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f'FAILED: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
