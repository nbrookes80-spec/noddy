# Build environment for the TunerToolPro Linux AppImage.
#
# Ubuntu 22.04 (glibc 2.35) is the oldest system the finished AppImage promises to run on.
# An AppImage carries its own libraries but still calls the host's glibc, and glibc is only
# backwards compatible, so the build base sets the floor: build here, run on 22.04 and newer
# (Zorin 17/18, Mint 21+, Debian 12+, Fedora 36+). Building on the Zorin 18.1 host instead
# would raise that floor to glibc 2.39 and lock out most other users.
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# python3.10 is Ubuntu 22.04's own Python. The Qt libraries matter even though nothing here
# opens a window: PyInstaller's dependency scan copies the ones Qt's xcb platform plugin links
# against into the bundle. That is what removes "sudo apt install libxcb-cursor0" from the
# user's install steps, which is the single most common reason the app installs but won't open.
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3.10 python3.10-venv python3-pip libpython3.10 \
      ca-certificates wget file binutils desktop-file-utils \
      libgl1 libegl1 libglib2.0-0 libdbus-1-3 libfontconfig1 libfreetype6 \
      libxkbcommon0 libxkbcommon-x11-0 \
      libxcb1 libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
      libxcb-randr0 libxcb-render0 libxcb-render-util0 libxcb-shape0 \
      libxcb-shm0 libxcb-sync1 libxcb-util1 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 \
      libx11-xcb1 libsm6 libice6 \
    && rm -rf /var/lib/apt/lists/*

# appimagetool packs the finished AppDir into the single .AppImage file. It ships as an
# AppImage itself; APPIMAGE_EXTRACT_AND_RUN lets it run without FUSE inside a container.
# Upstream publishes only a rolling "continuous" release, so this is not pinned.
RUN wget -q -O /usr/local/bin/appimagetool \
      https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage \
 && chmod +x /usr/local/bin/appimagetool

ENV APPIMAGE_EXTRACT_AND_RUN=1 ARCH=x86_64
