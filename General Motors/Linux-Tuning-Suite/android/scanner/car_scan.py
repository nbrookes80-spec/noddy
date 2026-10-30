"""Scan a car once and save which readings it answers, so the app only offers what the car gives. No Kivy.

A scan sends each catalogued Mode 01 or Mode 22 reading once, through Elm327.read(), so it can only send
the same read-only requests the app already allows. It records the module address that answered for each
reading. The result is saved per profile (scan folder/<profile key>.scan.json) and loaded whenever that
profile is chosen, so readings the car does not answer are not offered, and readings that need another
module (for example the transmission at 7E2) are asked for on that module.

A scan that was stopped by a lost adapter is saved only if no complete scan is already there, so a
cut-off run can never replace a good one.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import prefs as app_prefs
from link.obd import (AdapterLost, BluetoothTransport, DEFAULT_WIFI, Elm327, OBDError, SerialTransport,
                      WifiTransport)
from scanner import pids

SCAN_SUFFIX = '.scan.json'
VERSION = 1
AUTO = 'Auto'      # the header for "let the adapter pick", as Elm327.set_header uses it
LINK_WIFI, LINK_BLUETOOTH, LINK_CABLE = 'wifi', 'bluetooth', 'cable'
LINKS = (LINK_WIFI, LINK_BLUETOOTH, LINK_CABLE)


def scan_ids(profile_pids, mode01_only=False):
    """The readings to try: the dashboard set first, then the profile's own, each once and only if valid."""
    ids = []
    for pid in list(pids.DEFAULT_MONITOR) + list(profile_pids):
        if pid in ids or not pids.valid_id(pid) or pids.get(pid) is None:
            continue
        if mode01_only and not pid.startswith('01'):
            continue
        ids.append(pid)
    return ids


def scan(elm, ids, progress=None):
    """Try each reading once. Returns the result dict. A lost adapter stops the run and marks it incomplete."""
    answered, silent = {}, []
    complete = True
    for index, pid in enumerate(ids):
        if progress:
            progress(index, len(ids), pid)
        try:
            value, unit = elm.read(pid)
        except AdapterLost:
            complete = False
            break
        except OBDError:
            silent.append(pid)
            continue
        answered[pid] = {
            'name': pids.get(pid).name,
            'header': elm.header_for(pid) or AUTO,
            'unit': unit,
            'sample': value,
        }
    return {
        'version': VERSION,
        'scanned_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'complete': complete,
        'tried': list(ids),
        'answered': answered,
        'silent': silent,
    }


def _path(folder, key):
    return Path(folder) / f'{key}{SCAN_SUFFIX}'


def save_scan(folder, key, result):
    """Write the scan for a profile. Returns the path, or None when a cut-off scan would replace a complete one."""
    path = _path(folder, key)
    if not result['complete']:
        existing = load_scan(folder, key)
        if existing is not None and existing['complete']:
            return None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2), encoding='utf-8')
    return path


def load_scan(folder, key):
    """The saved scan for a profile, or None when there is none or the file is damaged."""
    try:
        data = json.loads(_path(folder, key).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get('version') != VERSION:
        return None
    answered = data.get('answered')
    if not isinstance(answered, dict) or not all(pids.valid_id(p) for p in answered):
        return None
    if not isinstance(data.get('complete'), bool):
        return None
    return data


def enforce(ids, scan_result):
    """Split the readings into (shown, hidden). Without a complete scan nothing is hidden, and the
    reason is an empty dict, so the screen can say that the car has not been checked yet."""
    if scan_result is None or not scan_result['complete']:
        return list(ids), {}
    answered = scan_result['answered']
    shown = [p for p in ids if p in answered]
    hidden = {p: 'no reply from this car' for p in ids if p not in answered}
    return shown, hidden


def headers(scan_result):
    """The module address to ask for each answered reading, only where it is not the broadcast address."""
    if scan_result is None or not scan_result['complete']:
        return {}
    return {p: info['header'] for p, info in scan_result['answered'].items() if info['header'] != AUTO}


# --- which link to scan over ---------------------------------------------------------------------

def link_from_prefs(prefs):
    """The link the user last picked on the Link screen: 'bluetooth' or 'wifi'."""
    return LINK_BLUETOOTH if prefs.get('link_kind') == 'Bluetooth' else LINK_WIFI


def transport_for(link, bt_address='', wifi='', serial_port='', baud=38400):
    """The transport for one link, built but not opened. Bluetooth works only on the phone; a cable only
    where pyserial is installed (desktop)."""
    if link == LINK_WIFI:
        host, _, port = (wifi or '').strip().partition(':')
        try:
            return WifiTransport(host or DEFAULT_WIFI[0], int(port or DEFAULT_WIFI[1]))
        except ValueError as exc:
            raise OBDError(f'The Wi-Fi adapter address {wifi!r} needs a port number, e.g. 192.168.0.10:35000') from exc
    if link == LINK_BLUETOOTH:
        if not bt_address:
            raise OBDError('No Bluetooth adapter is chosen. Pick it on the Link screen first.')
        return BluetoothTransport(bt_address)
    if link == LINK_CABLE:
        if not serial_port:
            raise OBDError('No cable port is given.')
        return SerialTransport(serial_port, baud)
    raise OBDError(f'Unknown link {link!r}')


def choose_link(session_elm, prefs, serial_port='', baud=38400):
    """Returns (elm, owned). If the app is already connected, its adapter is reused over whatever link it
    uses. Otherwise a new connection is opened over the saved link (or the cable when a port is given).
    owned is True when this call opened the connection, so the caller must close it."""
    if session_elm is not None:
        return session_elm, False
    link = LINK_CABLE if serial_port else link_from_prefs(prefs)
    elm = Elm327(transport_for(link, bt_address=prefs.get('bt_address', ''), wifi=prefs.get('wifi', ''),
                               serial_port=serial_port, baud=baud))
    try:
        elm.open()
    except Exception:
        elm.close()
        raise
    return elm, True


def saved_prefs(path=None):
    """The app's saved link choices, or the defaults when no file is given."""
    return app_prefs.load(path) if path else dict(app_prefs.DEFAULTS)
