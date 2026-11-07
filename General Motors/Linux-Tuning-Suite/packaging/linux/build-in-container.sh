#!/bin/bash
# Runs inside the container built from the Dockerfile beside this file.
# In:  /src  the Linux-Tuning-Suite folder, read-only
# Out: /out  the finished AppImage
set -euo pipefail

SRC=/src
OUT=/out
WORK=/work
HERE="$SRC/packaging/linux"

VERSION=$(sed -n 's/^__version__ = "\(.*\)"/\1/p' "$SRC/app/tunertoolpro/__init__.py")
[ -n "$VERSION" ] || { echo "could not read __version__ from app/tunertoolpro/__init__.py" >&2; exit 1; }
echo "==> TunerToolPro $VERSION"

# /src is read-only and PyInstaller writes beside its input, so work on a copy.
rm -rf "$WORK"; mkdir -p "$WORK"
cp -r "$SRC/app" "$WORK/app"

echo "==> Python environment"
python3.10 -m venv "$WORK/venv"
"$WORK/venv/bin/pip" install --quiet --upgrade pip wheel
"$WORK/venv/bin/pip" install --quiet -r "$WORK/app/requirements.txt" pyinstaller

echo "==> PyInstaller"
cd "$WORK"
# onedir, not onefile: the AppImage is already one file, and onefile would unpack a second
# copy to /tmp on every start. run_tunertoolpro.py exists for exactly this (PyInstaller
# cannot start a module that uses relative imports).
# The data files and splash assets are addressed by package-relative paths at runtime
# (profiles.DATA_DIR, splash.asset_path), so they must land under tunertoolpro/ in the bundle.
"$WORK/venv/bin/pyinstaller" --noconfirm --clean \
  --name TunerToolPro \
  --paths "$WORK/app" \
  --collect-submodules tunertoolpro \
  --add-data "$WORK/app/tunertoolpro/data:tunertoolpro/data" \
  --add-data "$WORK/app/tunertoolpro/gui/assets:tunertoolpro/gui/assets" \
  "$WORK/app/run_tunertoolpro.py"

test -x "$WORK/dist/TunerToolPro/TunerToolPro" || { echo "PyInstaller produced no binary" >&2; exit 1; }

echo "==> AppDir"
APPDIR="$WORK/AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/lib" "$APPDIR/usr/share/applications" \
         "$APPDIR/usr/share/icons/hicolor/256x256/apps" "$APPDIR/usr/share/metainfo"
cp -r "$WORK/dist/TunerToolPro" "$APPDIR/usr/lib/TunerToolPro"

# appimagetool reads the desktop entry and icon from the AppDir root; the copies under
# usr/share are what a desktop that integrates the AppImage picks up.
cp "$HERE/TunerToolPro.desktop" "$APPDIR/TunerToolPro.desktop"
cp "$HERE/TunerToolPro.desktop" "$APPDIR/usr/share/applications/TunerToolPro.desktop"
cp "$HERE/tunertoolpro.png" "$APPDIR/tunertoolpro.png"
cp "$HERE/tunertoolpro.png" "$APPDIR/.DirIcon"
cp "$HERE/tunertoolpro.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/tunertoolpro.png"
desktop-file-validate "$APPDIR/TunerToolPro.desktop"

cat > "$APPDIR/AppRun" <<'APPRUN'
#!/bin/sh
# Entry point of the AppImage. $HERE is the mounted read-only image, so nothing here is
# writable: the app keeps its settings in ~/.config/TunerToolPro (settings.py), which is
# the same place the Setup wizard uses, so an AppImage and an installed copy share them.
HERE="$(dirname "$(readlink -f "$0")")"
export TUNERTOOLPRO_PACKAGE=appimage
exec "$HERE/usr/lib/TunerToolPro/TunerToolPro" "$@"
APPRUN
chmod +x "$APPDIR/AppRun"

echo "==> appimagetool"
mkdir -p "$OUT"
TARGET="$OUT/TunerToolPro-$VERSION-x86_64.AppImage"
rm -f "$TARGET"
appimagetool --no-appstream "$APPDIR" "$TARGET"
chmod +x "$TARGET"

# The container runs as root; hand the file back to whoever started the build.
if [ -n "${HOST_UID:-}" ]; then chown "$HOST_UID:${HOST_GID:-$HOST_UID}" "$TARGET"; fi

echo
echo "==> built $TARGET"
ls -lh "$TARGET"
