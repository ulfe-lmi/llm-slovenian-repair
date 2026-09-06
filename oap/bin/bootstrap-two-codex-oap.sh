#!/usr/bin/env bash
set -euo pipefail
oap_bin_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
oap_action=materialize
oap_args=()
for oap_arg in "$@"; do
  if [[ "$oap_arg" == --refresh-governance ]]; then
    oap_action=refresh-governance
  else
    oap_args+=("$oap_arg")
  fi
done
exec python3 -B "$oap_bin_dir/oap_cli.py" "$oap_action" "${oap_args[@]}"
