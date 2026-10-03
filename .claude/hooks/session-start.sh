#!/bin/bash
# Reinstalls headless FreeCAD (conda-forge) so the freecad-mcp server's
# execute_code_headless tool works in Claude Code cloud sessions.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

MAMBA_ROOT_PREFIX="${MAMBA_ROOT_PREFIX:-/opt/mamba}"
MM_VERSION="2.9.0-0"
MM_BIN="$MAMBA_ROOT_PREFIX/bin/micromamba"
FREECAD_BIN="$MAMBA_ROOT_PREFIX/envs/freecad/bin"
export MAMBA_ROOT_PREFIX

# Bootstrap micromamba from conda-forge (micro.mamba.pm is not reachable via the proxy).
if [ ! -x "$MM_BIN" ]; then
  tmp="$(mktemp -d)"
  curl -fsSL --retry 4 --retry-delay 2 \
    "https://conda.anaconda.org/conda-forge/linux-64/micromamba-${MM_VERSION}.tar.bz2" \
    -o "$tmp/mm.tar.bz2"
  mkdir -p "$MAMBA_ROOT_PREFIX/bin"
  tar -xjf "$tmp/mm.tar.bz2" -C "$tmp" bin/micromamba
  mv "$tmp/bin/micromamba" "$MM_BIN"
  rm -rf "$tmp"
fi

# Create the FreeCAD env only if missing (idempotent; container state is cached afterwards).
if [ ! -x "$FREECAD_BIN/freecadcmd" ]; then
  "$MM_BIN" create -y -q -n freecad -c conda-forge freecad
fi

# freecad-mcp auto-detects freecadcmd on PATH.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$FREECAD_BIN:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi

echo "FreeCAD ready: $FREECAD_BIN/freecadcmd" >&2
