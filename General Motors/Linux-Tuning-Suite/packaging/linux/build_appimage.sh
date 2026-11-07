#!/usr/bin/env bash
# Build the TunerToolPro AppImage: one file, runs on any x86-64 Linux with glibc 2.35+
# (Ubuntu 22.04 and newer, Zorin 17/18, Mint 21+, Debian 12+, Fedora 36+), no apt installs,
# no Python on the user's machine, no root.
#
#   ./packaging/linux/build_appimage.sh
#
# Output: dist/TunerToolPro-<version>-x86_64.AppImage
#
# The build runs in a container so the result does not inherit this machine's glibc. Docker
# is the only thing needed on the build machine.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUITE="$(cd "$HERE/../.." && pwd)"
IMAGE=tunertoolpro-appimage-build
OUT="$SUITE/dist"

command -v docker >/dev/null || { echo "docker is not installed" >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "the docker daemon is not reachable (is it running? are you in the docker group?)" >&2; exit 1; }

mkdir -p "$OUT"
echo "==> build image"
docker build -t "$IMAGE" "$HERE"
echo "==> build AppImage"
docker run --rm \
  -e HOST_UID="$(id -u)" -e HOST_GID="$(id -g)" \
  -v "$SUITE:/src:ro" \
  -v "$OUT:/out" \
  "$IMAGE" bash /src/packaging/linux/build-in-container.sh
