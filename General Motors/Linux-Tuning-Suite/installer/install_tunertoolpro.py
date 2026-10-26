#!/usr/bin/env python3
"""TunerToolPro Setup for Linux: a Windows-style installer wizard.

Pages: Welcome, Terms, Install folder, Options (shortcuts and the optional AI assistant),
Ready, Installing, Finish. Uninstalling uses the same window.

Run the installer:       python3 install_tunertoolpro.py
Uninstall:               "Uninstall TunerToolPro" in the applications menu, or
                         python3 "<install folder>/uninstall_tunertoolpro.py"

Layout (Windows equivalent in brackets):
  <install folder>                 program files [C:\\Program Files\\TunerToolPro]
    app/  venv/  run-tunertoolpro.sh  uninstall_tunertoolpro.py  install.json
  ~/.config/TunerToolPro           settings and the AI key [%APPDATA%\\TunerToolPro]
  ~/.local/share/applications      Start menu entries [Start menu]
  ~/Desktop                        desktop shortcut [Desktop shortcut]
  ~/.local/bin/tunertoolpro        command [PATH entry]

Uninstall removes the program, shortcuts and command. Settings are kept unless you tick the
box to delete them.

Needs Python 3.10+ with Tkinter and venv. On Zorin OS or Ubuntu:
  sudo apt install python3-tk python3-venv
"""

import ctypes.util
import importlib.util
import json
import queue
import re
import shutil
import subprocess
import sys
import threading
import traceback
import venv
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP_SRC = HERE.parent / 'app'
REQUIREMENTS = APP_SRC / 'requirements.txt'
MIN_PYTHON = (3, 10)
UNINSTALLER = 'uninstall_tunertoolpro.py'
MANIFEST = 'install.json'
DEFAULT_TARGET = Path.home() / '.local' / 'share' / 'TunerToolPro'
PRODUCT = 'TunerToolPro'
SHORTCUT_COMMENT = 'GM 4L60E and 6L80E transmission calibration tools'


# ---------------------------------------------------------------- app-side shared modules

def app_version():
    text = (APP_SRC / 'tunertoolpro' / '__init__.py').read_text(encoding='utf-8')
    match = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    return match.group(1) if match else '0.0.0'


def app_modules():
    """legal and settings from the source tree. Both use only the standard library.

    Only the setup needs these. The uninstaller runs from the install folder, where the
    source tree is not present.
    """
    if str(APP_SRC) not in sys.path:
        sys.path.insert(0, str(APP_SRC))
    from tunertoolpro import legal, settings
    return legal, settings


# ---------------------------------------------------------------- checks

def check_python():
    if sys.version_info < MIN_PYTHON:
        raise RuntimeError(f'Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is required; '
                           f'this is {sys.version.split()[0]}')


def missing_qt_libraries(find=ctypes.util.find_library):
    """System packages the Qt window needs that are not installed, as apt package names."""
    missing = []
    if not find('xcb-cursor'):
        missing.append('libxcb-cursor0')
    return missing


def preflight():
    """Return the problems that would stop an install. Empty when all is well."""
    problems = []
    if sys.version_info < MIN_PYTHON:
        problems.append(f'Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer is needed.')
    if importlib.util.find_spec('ensurepip') is None:
        problems.append('The venv module is missing. Install it with: sudo apt install python3-venv')
    if not REQUIREMENTS.exists():
        problems.append(f'The installer is missing its application files ({REQUIREMENTS}).')
    return problems


def check_target(target):
    """Raise ValueError with a readable message when the folder cannot be used."""
    target = Path(target).expanduser()
    if not target.is_absolute():
        raise ValueError(f'Choose a full folder path, for example {DEFAULT_TARGET}')
    resolved = target.resolve()
    if resolved in (Path.home().resolve(), Path('/').resolve()):
        raise ValueError('Choose a folder of its own, not your home folder.')
    if resolved == APP_SRC.resolve() or APP_SRC.resolve() in resolved.parents:
        raise ValueError('Choose a folder outside the installer files.')
    if target.exists() and any(target.iterdir()) and not (target / MANIFEST).exists():
        raise ValueError('That folder is not empty and is not a TunerToolPro install. '
                         'Choose an empty folder.')


def desktop_dir():
    try:
        out = subprocess.run(['xdg-user-dir', 'DESKTOP'], capture_output=True, text=True,
                             timeout=5).stdout.strip()
        if out:
            return Path(out)
    except (OSError, subprocess.SubprocessError):
        pass
    return Path.home() / 'Desktop'


# ---------------------------------------------------------------- install

def _write_executable(path, text):
    path.write_text(text, encoding='utf-8')
    path.chmod(0o755)


def _mark_trusted(path):
    """GNOME-based desktops (Zorin, Ubuntu) will not run a desktop shortcut unless it is trusted."""
    try:
        subprocess.run(['gio', 'set', str(path), 'metadata::trusted', 'true'],
                       capture_output=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        pass


def _desktop_entry(name, comment, exec_line, categories='Utility;Engineering;'):
    return ('[Desktop Entry]\n'
            'Type=Application\n'
            f'Name={name}\n'
            f'Comment={comment}\n'
            f'Exec={exec_line}\n'
            'Terminal=false\n'
            f'Categories={categories}\n')


def _run_pip(pip, args):
    result = subprocess.run([str(pip), *args], capture_output=True, text=True)
    if result.returncode != 0:
        tail = (result.stderr or result.stdout)[-800:]
        raise RuntimeError(f'pip failed: {tail.strip()}')


def install(target, options, log=print, pip_install=True):
    """Install into target and return the launcher path.

    options keys: desktop, menu, command (bools); ai_enabled (bool), ai_key (str),
    ai_model (str). The AI key is saved only when ai_enabled is set. Other settings are kept.
    pip_install=False skips the package download; the tests use it.
    """
    check_python()
    check_target(target)  # checks the path as typed, before it is resolved
    target = Path(target).expanduser().resolve()
    _, settings = app_modules()
    target.mkdir(parents=True, exist_ok=True)
    recorded = []

    venv_dir = target / 'venv'
    log(f'Creating the Python environment in {venv_dir}')
    venv.EnvBuilder(with_pip=True, clear=True).create(venv_dir)
    if pip_install:
        pip = venv_dir / 'bin' / 'pip'
        log('Downloading PyQt6 and pandas. This can take a few minutes.')
        _run_pip(pip, ['install', '--upgrade', 'pip'])
        _run_pip(pip, ['install', '-r', str(REQUIREMENTS)])

    dest = target / 'app'
    log(f'Copying the application to {dest}')
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(APP_SRC, dest, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

    uninstaller = target / UNINSTALLER
    shutil.copy2(Path(__file__).resolve(), uninstaller)
    uninstaller.chmod(0o755)

    launcher = target / 'run-tunertoolpro.sh'
    _write_executable(launcher, '#!/bin/sh\n'
                      f'cd "{dest}" || exit 1\n'
                      f'exec "{venv_dir / "bin" / "python"}" -m tunertoolpro "$@"\n')
    log(f'Wrote the launcher {launcher}')

    apps = Path.home() / '.local' / 'share' / 'applications'
    apps.mkdir(parents=True, exist_ok=True)
    if options.get('menu'):
        entry = apps / 'tunertoolpro.desktop'
        entry.write_text(_desktop_entry(PRODUCT, SHORTCUT_COMMENT, f'"{launcher}"'), encoding='utf-8')
        recorded.append(str(entry))
        log(f'Added the applications menu entry {entry}')
    remove_entry = apps / 'tunertoolpro-uninstall.desktop'
    remove_entry.write_text(_desktop_entry(
        f'Uninstall {PRODUCT}', 'Remove TunerToolPro from this computer',
        f'"{sys.executable}" "{uninstaller}"', 'System;'), encoding='utf-8')
    recorded.append(str(remove_entry))

    if options.get('desktop'):
        desk = desktop_dir()
        if desk.is_dir():
            shortcut = desk / 'TunerToolPro.desktop'
            shortcut.write_text(_desktop_entry(PRODUCT, SHORTCUT_COMMENT, f'"{launcher}"'), encoding='utf-8')
            shortcut.chmod(0o755)
            _mark_trusted(shortcut)
            recorded.append(str(shortcut))
            log(f'Added the desktop shortcut {shortcut}')
        else:
            log(f'No desktop folder at {desk}, so no desktop shortcut was added.')

    if options.get('command'):
        bin_dir = Path.home() / '.local' / 'bin'
        bin_dir.mkdir(parents=True, exist_ok=True)
        link = bin_dir / 'tunertoolpro'
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(launcher)
        recorded.append(str(link))
        log(f'Added the command {link}')

    if options.get('ai_enabled'):
        data = settings.load()
        data['ai'] = {
            'enabled': bool(options.get('ai_enabled')),
            'api_key': (options.get('ai_key') or '').strip(),
            'model': options.get('ai_model') or settings.DEFAULTS['ai']['model'],
        }
        path = settings.save(data)
        log(f'Saved the AI assistant settings to {path} (readable by your account only)')

    manifest = {
        'product': PRODUCT,
        'version': app_version(),
        'installed_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'target': str(target),
        'launcher': str(launcher),
        'recorded': recorded,
        'user_dir': str(settings.user_dir()),
    }
    (target / MANIFEST).write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    for package in missing_qt_libraries():
        log(f'Warning: TunerToolPro needs the system package {package} to show its window. '
            f'Install it with: sudo apt install {package}')
    log(f'Installed {PRODUCT} {manifest["version"]}. Start it from the applications menu, '
        f'or run {launcher}')
    return launcher


# ---------------------------------------------------------------- uninstall

def uninstall(target, delete_settings=False, log=print):
    """Remove an install made by install(). Settings are kept unless delete_settings is True."""
    target = Path(target).expanduser().resolve()
    manifest_path = target / MANIFEST
    if not manifest_path.exists():
        raise ValueError(f'{target} is not a TunerToolPro install (no {MANIFEST}).')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    launcher = Path(manifest['launcher']).resolve()
    for item in manifest.get('recorded', []):
        path = Path(item)
        if path.is_symlink() and path.resolve() != launcher:
            log(f'Left {path} alone: it points somewhere else now.')
            continue
        if path.is_symlink() or path.exists():
            path.unlink()
            log(f'Removed {path}')
    shutil.rmtree(target)
    log(f'Removed the program folder {target}')
    user = Path(manifest.get('user_dir', ''))
    if delete_settings and user.name == 'TunerToolPro' and user.is_dir():
        shutil.rmtree(user)
        log(f'Removed your settings in {user}')
    elif delete_settings:
        log(f'Did not delete {user}: the folder name is not TunerToolPro. Remove it by hand if wanted.')
    else:
        log(f'Kept your settings in {user}.')
    log(f'{PRODUCT} has been removed.')


# ---------------------------------------------------------------- wizard (Tk)

def run_wizard(uninstall_mode=False):
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except ImportError:
        sys.stderr.write('TunerToolPro Setup needs Tkinter. On Zorin OS or Ubuntu run:\n'
                         '  sudo apt install python3-tk python3-venv\n')
        return 1

    manifest = {}
    if uninstall_mode:
        legal = settings = None
        manifest_path = HERE / MANIFEST
        if not manifest_path.exists():
            sys.stderr.write('This uninstaller is not inside a TunerToolPro install folder.\n')
            return 1
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        version = manifest.get('version', '')
        problems = []
    else:
        version = app_version()
        legal, settings = app_modules()
        problems = preflight()

    try:
        root = tk.Tk()
    except tk.TclError as exc:
        sys.stderr.write(f'Setup needs a graphical desktop to show its window: {exc}\n')
        return 1
    root.title(('Uninstall ' if uninstall_mode else 'Setup - ') + PRODUCT)
    style = ttk.Style(root)
    if 'clam' in style.theme_names():
        style.theme_use('clam')
    # Size from the screen, centred slightly above middle, and let the user resize further.
    root.update_idletasks()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    width, height = min(780, int(sw * 0.7)), min(640, int(sh * 0.78))
    root.geometry(f'{width}x{height}+{max(0, (sw - width) // 2)}+{max(0, (sh - height) // 3)}')
    root.minsize(600, 480)
    root.configure(background='#f0f0f0')

    def reflow(label, pad=40):
        """Re-wrap a label whenever its parent is resized, so text never clips."""
        label.bind('<Configure>', lambda e: label.configure(wraplength=max(200, e.width - pad)))

    banner = tk.Frame(root, background='white', padx=20, pady=14)
    banner.pack(fill='x')
    header = tk.Label(banner, background='white', font=('Helvetica', 14, 'bold'), anchor='w', justify='left')
    subtitle = tk.Label(banner, background='white', anchor='w', justify='left')
    header.pack(fill='x')
    subtitle.pack(fill='x', pady=(4, 0))
    reflow(subtitle)
    ttk.Separator(root).pack(fill='x')
    body = ttk.Frame(root, padding=20)
    body.pack(fill='both', expand=True)
    ttk.Separator(root).pack(fill='x')
    footer = ttk.Frame(root, padding=(12, 10))
    footer.pack(fill='x')
    cancel_btn = ttk.Button(footer, text='Cancel', command=root.destroy, width=12)
    next_btn = ttk.Button(footer, text='Next >', width=12)
    back_btn = ttk.Button(footer, text='< Back', width=12)
    cancel_btn.pack(side='right', padx=(8, 0))
    next_btn.pack(side='right')
    back_btn.pack(side='right', padx=(0, 8))

    default_model = settings.DEFAULTS['ai']['model'] if settings else ''
    state = {
        'page': None, 'history': [], 'result': None,
        'accepted': tk.BooleanVar(value=False),
        'target': tk.StringVar(value=str(DEFAULT_TARGET)),
        'desktop': tk.BooleanVar(value=desktop_dir().is_dir()),
        'menu': tk.BooleanVar(value=True), 'command': tk.BooleanVar(value=True),
        'ai_on': tk.BooleanVar(value=False), 'ai_key': tk.StringVar(value=''),
        'ai_model': tk.StringVar(value=default_model),
        'delete_settings': tk.BooleanVar(value=False), 'launch': tk.BooleanVar(value=True),
    }

    def clear_body():
        for child in body.winfo_children():
            child.destroy()

    def set_header(title, text):
        header.configure(text=title)
        subtitle.configure(text=text)

    def wrapped(parent, text, **pack):
        label = ttk.Label(parent, text=text, justify='left', anchor='w')
        reflow(label, pad=50)
        label.pack(fill='x', **({'anchor': 'w'} | pack))
        return label

    def text_box(parent, content, height):
        """A bordered, read-only text area with a theme scrollbar."""
        frame = ttk.Frame(parent)
        box = tk.Text(frame, wrap='word', height=height, background='white', relief='solid', bd=1,
                      highlightthickness=0, padx=10, pady=8, cursor='arrow', font=('Helvetica', 10))
        scroll = ttk.Scrollbar(frame, orient='vertical', command=box.yview)
        box.configure(yscrollcommand=scroll.set)
        box.insert('1.0', content)
        box.configure(state='disabled')
        box.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        frame.text = box
        return frame

    def build_welcome():
        set_header(f'Welcome to the {PRODUCT} Setup Wizard',
                   f'Version {version}. This wizard installs the program and its shortcuts on this computer.')
        if problems:
            ttk.Label(body, text='Setup cannot continue yet:', foreground='#a00').pack(anchor='w')
            for problem in problems:
                wrapped(body, '  - ' + problem)
        else:
            wrapped(body, 'Click Next to continue. The first install downloads PyQt6 and pandas, so it needs '
                          'an internet connection and takes a few minutes.')

    def build_uninstall_confirm():
        set_header(f'Remove {PRODUCT}',
                   f'This removes {PRODUCT} from {manifest.get("target", "")}, with its shortcuts and command.')
        wrapped(body, 'Your settings are kept by default. They hold your AI key and any saved data.')
        ttk.Checkbutton(body, text='Also delete my settings and AI key',
                        variable=state['delete_settings']).pack(anchor='w', pady=14)

    def build_terms():
        set_header('License and terms',
                   'Read the terms below. You must accept them to install TunerToolPro.')
        text_box(body, legal.DISCLAIMER + '\n\n' + legal.AI_NOTICE, 12).pack(fill='both', expand=True)
        ttk.Checkbutton(body, text='I accept the terms in this notice', variable=state['accepted'],
                        command=refresh_buttons).pack(anchor='w', pady=(12, 0))

    def browse():
        chosen = filedialog.askdirectory(initialdir=state['target'].get() or str(Path.home()))
        if chosen:
            state['target'].set(str(Path(chosen) / PRODUCT))

    def build_folder():
        set_header('Choose install folder',
                   'Setup installs the program in this folder. It is the program files folder, '
                   'like C:\\Program Files on Windows.')
        row = ttk.Frame(body)
        row.pack(fill='x')
        ttk.Entry(row, textvariable=state['target']).pack(side='left', fill='x', expand=True)
        ttk.Button(row, text='Browse...', command=browse).pack(side='left', padx=(8, 0))
        wrapped(body, f'Your settings are kept separately, in {settings.user_dir()}. Uninstall keeps them '
                      'unless you choose to delete them.', pady=(16, 0))

    def build_options():
        set_header('Select options', 'Choose the shortcuts you want, and whether to enable the AI assistant.')
        shortcuts = ttk.LabelFrame(body, text='Shortcuts', padding=12)
        shortcuts.pack(fill='x')
        ttk.Checkbutton(shortcuts, text='Desktop shortcut', variable=state['desktop']).pack(anchor='w')
        ttk.Checkbutton(shortcuts, text='Applications menu entry', variable=state['menu']).pack(anchor='w')
        ttk.Checkbutton(shortcuts, text='tunertoolpro command (in ~/.local/bin)',
                        variable=state['command']).pack(anchor='w')
        ai = ttk.LabelFrame(body, text='AI assistant (optional)', padding=12)
        ai.pack(fill='x', pady=(14, 0))
        ttk.Checkbutton(ai, text='Enable the AI assistant', variable=state['ai_on'],
                        command=refresh_ai).pack(anchor='w')
        grid = ttk.Frame(ai)
        grid.pack(fill='x', pady=(8, 0))
        ttk.Label(grid, text='API key').grid(row=0, column=0, sticky='w')
        state['key_entry'] = ttk.Entry(grid, textvariable=state['ai_key'], show='*')
        state['key_entry'].grid(row=0, column=1, sticky='we', padx=8)
        ttk.Label(grid, text='Model').grid(row=1, column=0, sticky='w', pady=(6, 0))
        state['model_box'] = ttk.Combobox(grid, textvariable=state['ai_model'], state='readonly',
                                          values=settings.AI_MODELS, width=26)
        state['model_box'].grid(row=1, column=1, sticky='w', padx=8, pady=(6, 0))
        grid.columnconfigure(1, weight=1)
        wrapped(ai, 'Leave this off and add a key later in the AI Assistant tab if you prefer. The key is stored '
                    'in your settings file, which only your account can read. ' + legal.AI_NOTICE, pady=(10, 0))
        refresh_ai()

    def refresh_ai():
        on = state['ai_on'].get()
        state['key_entry'].configure(state='normal' if on else 'disabled')
        state['model_box'].configure(state='readonly' if on else 'disabled')

    def build_ready():
        set_header('Ready to install', 'Setup has what it needs. Click Install to begin.')
        ai_line = f'on, model {state["ai_model"].get()}' if state['ai_on'].get() else 'off'
        lines = [
            f'Install folder: {state["target"].get()}',
            f'Desktop shortcut: {"yes" if state["desktop"].get() else "no"}',
            f'Applications menu entry: {"yes" if state["menu"].get() else "no"}',
            f'tunertoolpro command: {"yes" if state["command"].get() else "no"}',
            f'AI assistant: {ai_line}',
        ]
        text_box(body, '\n'.join(lines), 8).pack(fill='both', expand=True)

    def build_progress(title, text, run):
        set_header(title, text)
        bar = ttk.Progressbar(body, mode='indeterminate')
        bar.pack(fill='x', pady=(0, 12))
        bar.start(12)
        log_frame = text_box(body, '', 14)
        log_frame.pack(fill='both', expand=True)
        log_box = log_frame.text

        # Tk is not thread-safe: the worker only queues lines, and the window drains the queue.
        messages = queue.Queue()
        done = {'flag': False}

        def write(msg):
            messages.put(msg)

        def drain():
            while True:
                try:
                    msg = messages.get_nowait()
                except queue.Empty:
                    break
                log_box.configure(state='normal')
                log_box.insert('end', msg + '\n')
                log_box.see('end')
                log_box.configure(state='disabled')
            if done['flag'] and messages.empty():
                finished()
            else:
                root.after(150, drain)

        def worker():
            try:
                state['result'] = ('ok', run(write))
            except Exception as exc:  # any failure must reach the Finish page, not crash the window
                write(f'FAILED: {exc}')
                write(traceback.format_exc().rstrip())
                state['result'] = ('error', str(exc))
            done['flag'] = True

        def finished():
            bar.stop()
            bar.configure(mode='determinate', value=100)
            cancel_btn.configure(state='normal')
            root.protocol('WM_DELETE_WINDOW', root.destroy)
            go_next(force=True)

        # Cancel and the window close button stay off until the work has ended.
        cancel_btn.configure(state='disabled')
        root.protocol('WM_DELETE_WINDOW', lambda: None)
        threading.Thread(target=worker, daemon=True).start()
        root.after(150, drain)

    def start_install():
        options = {
            'desktop': state['desktop'].get(), 'menu': state['menu'].get(),
            'command': state['command'].get(), 'ai_enabled': state['ai_on'].get(),
            'ai_key': state['ai_key'].get(), 'ai_model': state['ai_model'].get(),
        }
        target = state['target'].get()
        build_progress('Installing', f'Installing {PRODUCT} {version}. Please wait.',
                       lambda write: install(target, options, log=write))

    def start_uninstall():
        delete = state['delete_settings'].get()
        build_progress('Removing', f'Removing {PRODUCT}. Please wait.',
                       lambda write: uninstall(HERE, delete_settings=delete, log=write))

    def build_finish():
        status, detail = state['result'] or ('error', 'No result was returned.')
        if status == 'ok' and uninstall_mode:
            set_header(f'{PRODUCT} has been removed', 'Click Finish to close this window.')
        elif status == 'ok':
            set_header(f'Completed the {PRODUCT} Setup Wizard',
                       'TunerToolPro is installed. Click Finish to close Setup.')
            ttk.Checkbutton(body, text=f'Start {PRODUCT} now', variable=state['launch']).pack(anchor='w')
        else:
            set_header('Setup failed' if not uninstall_mode else 'Removal failed', detail)
            wrapped(body, 'Setup did not finish. Fix the problem above and run Setup again. Your settings '
                          'are not removed.')

    def finish():
        if not uninstall_mode and state['result'] and state['result'][0] == 'ok' and state['launch'].get():
            subprocess.Popen([str(state['result'][1])], start_new_session=True)
        root.destroy()

    def refresh_buttons():
        if state['page'] == 'terms':
            next_btn.configure(state='normal' if state['accepted'].get() else 'disabled')

    pages = {
        'welcome': build_welcome, 'terms': build_terms, 'folder': build_folder,
        'options': build_options, 'ready': build_ready, 'finish': build_finish,
        'uninstall': build_uninstall_confirm,
    }
    flow = (['uninstall', 'progress', 'finish'] if uninstall_mode
            else ['welcome', 'terms', 'folder', 'options', 'ready', 'progress', 'finish'])

    def target_ok():
        try:
            check_target(state['target'].get())
            return True
        except ValueError as exc:
            messagebox.showwarning('Install folder', str(exc), parent=root)
            return False

    def show(name):
        state['page'] = name
        clear_body()
        if name == 'progress':
            # Buttons stay disabled while the work runs; the finish page re-enables them.
            back_btn.configure(state='disabled')
            next_btn.configure(state='disabled')
            (start_uninstall if uninstall_mode else start_install)()
            return
        pages[name]()
        back_btn.configure(state='disabled' if name in ('welcome', 'uninstall', 'finish') else 'normal')
        if name == 'finish':
            next_btn.configure(text='Finish', state='normal', command=finish)
        else:
            label = {'ready': 'Install', 'uninstall': 'Uninstall'}.get(name, 'Next >')
            next_btn.configure(text=label, state='normal', command=go_next)
        if name == 'terms':
            refresh_buttons()
        if name == 'welcome' and problems:
            next_btn.configure(state='disabled')

    def go_next(force=False):
        page = state['page']
        if not force and page == 'folder' and not target_ok():
            return
        if page not in flow:
            return
        idx = flow.index(page)
        if idx + 1 < len(flow):
            state['history'].append(page)
            show(flow[idx + 1])

    def go_back():
        if state['history']:
            show(state['history'].pop())

    back_btn.configure(command=go_back)
    show('uninstall' if uninstall_mode else 'welcome')
    root.mainloop()
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv != ['--uninstall']:
        sys.stderr.write('Usage: install_tunertoolpro.py [--uninstall]\n')
        return 2
    # Running from inside an install folder means uninstall; the setup copy sits beside app/.
    uninstall_mode = bool(argv) or (HERE / MANIFEST).exists()
    try:
        return run_wizard(uninstall_mode=uninstall_mode)
    except (OSError, RuntimeError, ValueError) as exc:
        sys.stderr.write(f'FAILED: {exc}\n')
        return 1


if __name__ == '__main__':
    sys.exit(main())
