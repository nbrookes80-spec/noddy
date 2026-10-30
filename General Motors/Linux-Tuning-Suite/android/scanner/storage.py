"""Where the user's saved files go. No Kivy.

Everything is kept in one folder called "Tuner Tool Info", with a sub folder for each kind of file:

    Tuner Tool Info/Data logs    the sensor recordings (one CSV per recording)
    Tuner Tool Info/Debug logs   what the app and the adapter said (one text file per run)

Every file is named by the date and time it was started, e.g. 2026-10-31_14-05-33.csv.

Android keeps an app's own files out of sight of the Files app, so the live files are written to the app's
storage on the phone and a copy is published to the phone's Documents folder (publish) when a recording
stops, when the app is put away and now and then in between. Both copies use the same folder names.
"""

import os
import re
import shutil
import time

ROOT = 'Tuner Tool Info'
DATA_LOGS = 'Data logs'
DEBUG_LOGS = 'Debug logs'
STAMP = re.compile(r'^\d{4}-\d\d-\d\d_\d\d-\d\d-\d\d')


def stamp(moment=None):
    """The date and time as a file name, e.g. 2026-10-31_14-05-33."""
    return time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(moment if moment is not None else time.time()))


def folder(base, kind):
    """The folder for one kind of file inside the Tuner Tool Info folder under base."""
    return os.path.join(base, ROOT, kind)


def base_folder(fallback):
    """The phone's storage for this app (visible over USB), or the fallback folder when not on Android."""
    try:
        from jnius import autoclass
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        found = activity.getExternalFilesDir(None)
        if found is not None:
            return str(found.getAbsolutePath())
    except Exception:   # not Android, or the storage is not available: use the app's own folder
        pass
    return fallback


def publish(path, kind):
    """Copy a file to the phone's Documents/Tuner Tool Info/<kind>, replacing an earlier copy of the same name.

    Returns (done, message). Never raises: a copy that cannot be made leaves the original where it is."""
    if not path or not os.path.exists(path):
        return False, 'There is nothing to copy yet.'
    try:
        from jnius import autoclass
    except ImportError:
        return False, 'Copying to Documents works only on the phone.'
    try:
        return _publish_android(autoclass, path, kind)
    except Exception as exc:   # Java errors come through pyjnius as plain exceptions
        return False, f'Could not copy to Documents: {exc}'


def _publish_android(autoclass, path, kind):
    name = os.path.basename(path)
    relative = f'Documents/{ROOT}/{kind}'
    sdk = autoclass('android.os.Build$VERSION').SDK_INT
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
    if sdk < 29:   # older Android: Documents can be written directly
        environment = autoclass('android.os.Environment')
        target = os.path.join(str(environment.getExternalStoragePublicDirectory('Documents').getAbsolutePath()),
                              ROOT, kind)
        os.makedirs(target, exist_ok=True)
        shutil.copyfile(path, os.path.join(target, name))
        return True, f'Copied to {relative}/{name}'
    resolver = activity.getContentResolver()
    files = autoclass('android.provider.MediaStore$Files').getContentUri('external')
    existing = resolver.query(files, ['_id'], '_display_name=? AND relative_path=?', [name, relative + '/'], None)
    uri = None
    try:
        if existing is not None and existing.moveToFirst():
            uri = autoclass('android.content.ContentUris').withAppendedId(files, existing.getLong(0))
    finally:
        if existing is not None:
            existing.close()
    if uri is None:
        values = autoclass('android.content.ContentValues')()
        values.put('_display_name', name)
        values.put('mime_type', 'text/csv' if name.endswith('.csv') else 'text/plain')
        values.put('relative_path', relative)
        uri = resolver.insert(files, values)
    if uri is None:
        return False, 'Android would not make the file in Documents.'
    out = resolver.openOutputStream(uri, 'wt')
    try:
        source = autoclass('java.io.FileInputStream')(path)
        try:
            autoclass('android.os.FileUtils').copy(source, out)
        finally:
            source.close()
    finally:
        out.close()
    return True, f'Copied to {relative}/{name}'
