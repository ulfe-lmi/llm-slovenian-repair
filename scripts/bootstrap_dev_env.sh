#!/bin/sh
# scripts/bootstrap_dev_env.sh — machine-local development environment bootstrap.
#
# Usage:
#   scripts/bootstrap_dev_env.sh            validate, then run `uv sync --frozen`
#   scripts/bootstrap_dev_env.sh --check    validate and print the resolved plan only
#
# Sources scripts/project_env.sh for the canonical environment, validates the
# repository identity (pyproject.toml and the committed uv.lock), the uv
# version constraint from [tool.uv], and Python 3.12 availability, rejects an
# unsafe or repository-overlapping environment target, and creates the
# machine-local environment through uv. It never copies or moves a virtual
# environment. Dependency declarations live only in pyproject.toml and
# uv.lock; this script duplicates none of them.

set -u
LC_ALL=C
export LC_ALL

_oap_boot_fail() {
    echo "bootstrap_dev_env.sh: $1" >&2
    exit 1
}

_oap_boot_mode="sync"
if [ "$#" -gt 1 ]; then
    _oap_boot_fail "usage: scripts/bootstrap_dev_env.sh [--check]"
fi
if [ "$#" -eq 1 ]; then
    case "$1" in
        --check) _oap_boot_mode="check" ;;
        -h | --help)
            echo "usage: scripts/bootstrap_dev_env.sh [--check]"
            exit 0
            ;;
        *) _oap_boot_fail "unknown option: $1 (expected --check)" ;;
    esac
fi

_oap_boot_self_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || \
    _oap_boot_fail "cannot resolve this script's directory"
if [ ! -f "$_oap_boot_self_dir/project_env.sh" ]; then
    _oap_boot_fail "canonical helper project_env.sh not found next to this script"
fi

# Repository identity: pyproject.toml and the committed lockfile.
_oap_boot_root=""
if [ -n "${OAP_PROJECT_ROOT:-}" ]; then
    _oap_boot_root="$OAP_PROJECT_ROOT"
elif command -v git >/dev/null 2>&1; then
    _oap_boot_root=$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null) || _oap_boot_root=""
fi
if [ -z "$_oap_boot_root" ] && [ -f "$PWD/pyproject.toml" ]; then
    _oap_boot_root="$PWD"
fi
if [ -z "$_oap_boot_root" ]; then
    _oap_boot_fail "cannot locate the project root; run from inside the repository or set OAP_PROJECT_ROOT"
fi
if [ ! -f "$_oap_boot_root/pyproject.toml" ]; then
    _oap_boot_fail "project root has no pyproject.toml"
fi
if [ ! -f "$_oap_boot_root/uv.lock" ]; then
    _oap_boot_fail "project root has no uv.lock; the committed lockfile is the only dependency source"
fi

# Canonical environment; also validates $HOME and the environment target.
OAP_PROJECT_ROOT="$_oap_boot_root"
OAP_PROJECT_ENV_EXEC_OK=1
. "$_oap_boot_self_dir/project_env.sh" || _oap_boot_fail "canonical environment validation failed"

# uv availability and the checked-in version constraint.
if ! command -v uv >/dev/null 2>&1; then
    _oap_boot_fail "uv is not installed or not on PATH"
fi
_oap_boot_uv_version_line=$(uv --version 2>/dev/null) || _oap_boot_fail "uv --version failed"
case "$_oap_boot_uv_version_line" in
    "uv "*) ;;
    *) _oap_boot_fail "unrecognized uv version output" ;;
esac
_oap_boot_uv=$(printf '%s\n' "$_oap_boot_uv_version_line" | \
    sed -n 's/^uv \([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\).*$/\1/p')
if [ -z "$_oap_boot_uv" ]; then
    _oap_boot_fail "cannot parse the uv version"
fi
_oap_boot_constraint=$(sed -n 's/^required-version[[:space:]]*=[[:space:]]*"\([^"]*\)"[[:space:]]*$/\1/p' \
    "$_oap_boot_root/pyproject.toml" | sed -n 1p)
if [ -z "$_oap_boot_constraint" ]; then
    _oap_boot_fail "pyproject.toml has no [tool.uv] required-version"
fi

# Prints a dotted numeric version with each component zero-padded to 3 digits.
_oap_boot_vernorm() {
    _oap_vn_out=""
    if [ -n "${IFS+x}" ]; then
        _oap_vn_ifs="$IFS"
        _oap_vn_ifs_set=1
    else
        _oap_vn_ifs=""
        _oap_vn_ifs_set=0
    fi
    IFS='.'
    for _oap_vn_part in $1; do
        case "$_oap_vn_part" in
            '' | *[!0-9]*)
                if [ "$_oap_vn_ifs_set" = "1" ]; then IFS="$_oap_vn_ifs"; else unset IFS; fi
                return 1
                ;;
        esac
        _oap_vn_part=$(printf '%03d' "$_oap_vn_part")
        if [ -z "$_oap_vn_out" ]; then
            _oap_vn_out="$_oap_vn_part"
        else
            _oap_vn_out="$_oap_vn_out-$_oap_vn_part"
        fi
    done
    if [ "$_oap_vn_ifs_set" = "1" ]; then
        IFS="$_oap_vn_ifs"
    else
        unset IFS
    fi
    printf '%s\n' "$_oap_vn_out"
}

# Prints lt, eq, or gt comparing dotted numeric versions.
_oap_boot_vercmp() {
    _oap_vc_a=$(_oap_boot_vernorm "$1") || return 1
    _oap_vc_b=$(_oap_boot_vernorm "$2") || return 1
    while :; do
        _oap_vc_ac=$(printf '%s\n' "$_oap_vc_a" | cut -d'-' -f1)
        _oap_vc_bc=$(printf '%s\n' "$_oap_vc_b" | cut -d'-' -f1)
        [ -n "$_oap_vc_ac" ] || _oap_vc_ac=000
        [ -n "$_oap_vc_bc" ] || _oap_vc_bc=000
        if [ "$_oap_vc_ac" \< "$_oap_vc_bc" ]; then
            printf 'lt\n'
            return 0
        fi
        if [ "$_oap_vc_ac" \> "$_oap_vc_bc" ]; then
            printf 'gt\n'
            return 0
        fi
        case "$_oap_vc_a" in
            *-*) _oap_vc_a=${_oap_vc_a#*-} ;;
            *) _oap_vc_a="" ;;
        esac
        case "$_oap_vc_b" in
            *-*) _oap_vc_b=${_oap_vc_b#*-} ;;
            *) _oap_vc_b="" ;;
        esac
        if [ -z "$_oap_vc_a" ] && [ -z "$_oap_vc_b" ]; then
            break
        fi
    done
    printf 'eq\n'
    return 0
}

_oap_boot_min=""
_oap_boot_max=""
if [ -n "${IFS+x}" ]; then
    _oap_boot_ifs="$IFS"
    _oap_boot_ifs_set=1
else
    _oap_boot_ifs=""
    _oap_boot_ifs_set=0
fi
IFS=','
for _oap_boot_part in $_oap_boot_constraint; do
    _oap_boot_part=$(printf '%s\n' "$_oap_boot_part" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    case "$_oap_boot_part" in
        ">="*) _oap_boot_min=${_oap_boot_part#">="} ;;
        "<="*) _oap_boot_max=${_oap_boot_part#"<="} ;;
        "<"*) _oap_boot_max=${_oap_boot_part#"<"} ;;
        "") ;;
        *) _oap_boot_fail "unsupported uv constraint part: $_oap_boot_part" ;;
    esac
done
if [ "$_oap_boot_ifs_set" = "1" ]; then
    IFS="$_oap_boot_ifs"
else
    unset IFS
fi
if [ -n "$_oap_boot_min" ]; then
    _oap_boot_c=$(_oap_boot_vercmp "$_oap_boot_uv" "$_oap_boot_min") || \
        _oap_boot_fail "cannot compare uv versions"
    if [ "$_oap_boot_c" = "lt" ]; then
        _oap_boot_fail "uv $_oap_boot_uv does not satisfy required-version $_oap_boot_constraint"
    fi
fi
if [ -n "$_oap_boot_max" ]; then
    _oap_boot_c=$(_oap_boot_vercmp "$_oap_boot_uv" "$_oap_boot_max") || \
        _oap_boot_fail "cannot compare uv versions"
    if [ "$_oap_boot_c" != "lt" ]; then
        _oap_boot_fail "uv $_oap_boot_uv does not satisfy required-version $_oap_boot_constraint"
    fi
fi

# Python 3.12 availability (system interpreter or uv-managed, offline).
_oap_boot_python=""
if command -v python3.12 >/dev/null 2>&1; then
    _oap_boot_python="python3.12 ($(command -v python3.12))"
else
    _oap_boot_managed=$(uv python find '>=3.12,<3.13' 2>/dev/null) || _oap_boot_managed=""
    if [ -z "$_oap_boot_managed" ]; then
        _oap_boot_fail "no Python 3.12 interpreter found (python3.12 or uv-managed)"
    fi
    _oap_boot_python="uv-managed ($_oap_boot_managed)"
fi

# Environment target revalidation (defense in depth after the helper).
_oap_boot_env_dir="${UV_PROJECT_ENVIRONMENT:-}"
if [ -z "$_oap_boot_env_dir" ]; then
    _oap_boot_fail "environment target was not resolved"
fi
case "$_oap_boot_env_dir" in
    "$_oap_boot_root"/*) _oap_boot_fail "environment target overlaps the repository" ;;
esac
case "$_oap_boot_env_dir" in
    "$HOME"/*) ;;
    *) _oap_boot_fail "environment target is not under \$HOME" ;;
esac
if [ -L "$_oap_boot_env_dir" ]; then
    _oap_boot_fail "environment target is a symlink; refusing to use it"
fi
if [ -e "$_oap_boot_env_dir" ] && [ ! -d "$_oap_boot_env_dir" ]; then
    _oap_boot_fail "environment target exists and is not a directory"
fi

_oap_boot_project=$(sed -n 's/^name[[:space:]]*=[[:space:]]*"\([^"]*\)"[[:space:]]*$/\1/p' \
    "$_oap_boot_root/pyproject.toml" | sed -n 1p)

echo "bootstrap_dev_env.sh: mode $_oap_boot_mode"
echo "  project root:  $_oap_boot_root"
echo "  project:       $_oap_boot_project"
echo "  environment:   $_oap_boot_env_dir"
echo "  python:        $_oap_boot_python"
echo "  uv:            $_oap_boot_uv (required $_oap_boot_constraint)"

if [ "$_oap_boot_mode" = "check" ]; then
    echo "  sync:          not run (--check)"
    exit 0
fi

# The only mutation: the normal locked sync into the machine-local target.
if ! uv sync --frozen; then
    _oap_boot_fail "uv sync --frozen failed"
fi
echo "bootstrap_dev_env.sh: environment ready at $_oap_boot_env_dir"
exit 0
