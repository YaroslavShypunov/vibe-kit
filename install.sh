#!/bin/bash
set -euo pipefail
kit_root="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$kit_root/scripts/install.py" "$@"
