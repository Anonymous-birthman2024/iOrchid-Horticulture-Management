#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$SCRIPT_DIR"

if [[ -f "$PROJECT_DIR/venv/bin/activate" ]]; then
    source "$PROJECT_DIR/venv/bin/activate"
fi

exec python3 "$SCRIPT_DIR/webServer2026.py"
