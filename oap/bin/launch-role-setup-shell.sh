#!/usr/bin/env bash
set -euo pipefail
oap_bin_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
exec python3 -B "$oap_bin_dir/oap_cli.py" setup-shell "$@"
