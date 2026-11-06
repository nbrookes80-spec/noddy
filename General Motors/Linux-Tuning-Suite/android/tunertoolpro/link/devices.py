"""Finding the scan adapter over Bluetooth: the paired-device list and the checks before connecting.

rank_devices and normalise_address are plain Python and are tested on a desktop. The functions below
them call Android through pyjnius and only work inside the app.

Bluetooth Classic adapters (ELM327 clones, OBDLink, vLinker, Veepeak and similar) have to be paired
once in Android's own Bluetooth settings, which is where the PIN prompt appears (usually 1234 or
0000). After that they show up in this list. BLE-only adapters are not supported here.
"""

import re

LIKELY_WORDS = ('obd', 'elm', 'v-link', 'vlink', 'vgate', 'veepeak', 'obdlink', 'scan', 'konnwei',
                'carista', 'vlinker', 'icar', 'viecar', 'can-bus')
PERMISSIONS = ('android.permission.BLUETOOTH_CONNECT', 'android.permission.BLUETOOTH_SCAN')

READY, NEEDS_PERMISSION, BLUETOOTH_OFF, UNAVAILABLE = 'ready', 'permission', 'off', 'unavailable'


def normalise_address(text):
    """'00-1d-a5-68-98-8b' or '001DA568988B' -> '00:1D:A5:68:98:8B'. None if it is not an address."""
    if not isinstance(text, str):
        return None
    digits = re.sub(r'[\s:\-]', '', text).upper()
    if not re.fullmatch(r'[0-9A-F]{12}', digits):
        return None
    return ':'.join(digits[i:i + 2] for i in range(0, 12, 2))


def rank_devices(pairs):
    """[(name, address), ...] -> dicts, scan-adapter-looking names first, no duplicates or bad addresses."""
    seen, devices = set(), []
    for name, address in pairs:
        clean = normalise_address(address)
        if clean is None or clean in seen:
            continue
        seen.add(clean)
        name = (name or '').strip() or 'Unnamed device'
        likely = any(word in name.lower() for word in LIKELY_WORDS)
        devices.append({'name': name, 'address': clean, 'likely': likely})
    devices.sort(key=lambda d: (not d['likely'], d['name'].lower()))
    return devices


# --- Android only ---------------------------------------------------------------------------------

def _autoclass():
    try:
        from jnius import autoclass
    except ImportError:
        return None
    return autoclass


def _activity(autoclass):
    return autoclass('org.kivy.android.PythonActivity').mActivity


def _missing_permissions(autoclass):
    """Android 12 and newer need Nearby devices at run time; older versions grant it at install."""
    if autoclass('android.os.Build$VERSION').SDK_INT < 31:
        return []
    try:
        from android.permissions import check_permission
    except ImportError:
        return []
    return [p for p in PERMISSIONS if not check_permission(p)]


def request_permissions():
    """Show Android's Nearby devices prompt. Returns once it has been asked, not once it is answered."""
    autoclass = _autoclass()
    if autoclass is None:
        return
    needed = _missing_permissions(autoclass)
    if needed:
        from android.permissions import request_permissions as ask
        ask(needed)


def adapter_state():
    """(state, message) for the phone's Bluetooth: ready, permission, off or unavailable."""
    autoclass = _autoclass()
    if autoclass is None:
        return UNAVAILABLE, 'Bluetooth only works in the Android app. Use Wi-Fi on this computer.'
    if _missing_permissions(autoclass):
        return NEEDS_PERMISSION, 'Allow "Nearby devices" so the app can see your paired adapters.'
    adapter = autoclass('android.bluetooth.BluetoothAdapter').getDefaultAdapter()
    if adapter is None:
        return UNAVAILABLE, 'This phone has no Bluetooth.'
    if not adapter.isEnabled():
        return BLUETOOTH_OFF, 'Bluetooth is off. Turn it on to see your paired adapters.'
    return READY, ''


def paired_devices():
    """Paired Bluetooth devices as ranked dicts. Empty if Bluetooth is not ready."""
    state, _ = adapter_state()
    if state != READY:
        return []
    autoclass = _autoclass()
    adapter = autoclass('android.bluetooth.BluetoothAdapter').getDefaultAdapter()
    bonded = adapter.getBondedDevices().toArray()
    return rank_devices([(d.getName(), d.getAddress()) for d in bonded])


def ask_to_turn_on():
    """Android's own "Allow Bluetooth to turn on?" dialog."""
    autoclass = _autoclass()
    if autoclass is None:
        return
    intent = autoclass('android.content.Intent')(autoclass('android.bluetooth.BluetoothAdapter').ACTION_REQUEST_ENABLE)
    _activity(autoclass).startActivityForResult(intent, 4601)


def open_pairing_settings():
    """Android's Bluetooth settings, where a new adapter is paired (and its PIN entered)."""
    autoclass = _autoclass()
    if autoclass is None:
        return
    intent = autoclass('android.content.Intent')(autoclass('android.provider.Settings').ACTION_BLUETOOTH_SETTINGS)
    _activity(autoclass).startActivity(intent)


def bind_to_wifi():
    """Keep this app's traffic on Wi-Fi even when that network has no internet.

    A Wi-Fi scan adapter makes its own hotspot with no internet, so Android may quietly send traffic over
    mobile data instead and the adapter looks unreachable. Returns True if the app is now tied to Wi-Fi.
    Best effort: any failure just leaves Android's normal choice in place.
    """
    autoclass = _autoclass()
    if autoclass is None:
        return False
    try:
        manager = _activity(autoclass).getSystemService(autoclass('android.content.Context').CONNECTIVITY_SERVICE)
        transport_wifi = autoclass('android.net.NetworkCapabilities').TRANSPORT_WIFI
        for network in manager.getAllNetworks():
            caps = manager.getNetworkCapabilities(network)
            if caps is not None and caps.hasTransport(transport_wifi):
                return bool(manager.bindProcessToNetwork(network))
    except Exception:  # noqa: BLE001 - Java exceptions come through pyjnius as plain Exceptions
        return False
    return False


def release_wifi():
    autoclass = _autoclass()
    if autoclass is None:
        return
    try:
        _activity(autoclass).getSystemService(
            autoclass('android.content.Context').CONNECTIVITY_SERVICE).bindProcessToNetwork(None)
    except Exception:  # noqa: BLE001
        pass
