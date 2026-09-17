# scripts/project_env.sh — canonical machine-local development environment.
#
# This file is data for your shell. Source it, do not execute it:
#
#     source scripts/project_env.sh
#
# Every persistent path is derived from $HOME and the checked-in project name
# (the [project] name in pyproject.toml). No username, hostname, or absolute
# path is hard-coded.
#
# Exports (repeated sourcing is idempotent):
#   UV_PROJECT_ENVIRONMENT  $HOME/envs/<project>            (always)
#   VIRTUAL_ENV             $HOME/envs/<project>            (always)
#   PATH                    $HOME/envs/<project>/bin exactly once, first
#   PYTHONPYCACHEPREFIX     $HOME/.cache/python-pycache/<project>  (if unset)
#   RUFF_CACHE_DIR          $HOME/.cache/ruff/<project>           (if unset)
#   MYPY_CACHE_DIR          $HOME/.cache/mypy/<project>           (if unset)
#   PYTEST_ADDOPTS          appends -o cache_dir=$HOME/.cache/pytest/<project>
#   TMPDIR                  $HOME/.cache/tmp/<project>            (if unset)
#
# The helper creates only the exact project-specific parent and cache
# directories. It never creates the uv environment itself; use
# scripts/bootstrap_dev_env.sh or `uv sync --frozen` for that. Existing
# nonempty user values for the cache and TMPDIR variables are preserved.

# Refuse direct execution: an executed child cannot export to your shell.
if [ "${OAP_PROJECT_ENV_EXEC_OK:-}" != "1" ]; then
    if [ -n "${BASH_SOURCE:-}" ] && [ "${BASH_SOURCE:-}" != "$0" ]; then
        : # sourced from bash; BASH_SOURCE is the helper path.
    elif [ -f "$0" ]; then
        echo "project_env.sh: this file must be sourced, not executed." >&2
        echo "project_env.sh: run:  source scripts/project_env.sh" >&2
        exit 1
    fi
fi

_oap_env_main() {
    # On any failure: print one concise reason and return 1 so the top-level
    # guard aborts the sourced script without touching the caller's shell.

    # Resolve the project root: explicit override, git worktree, then $PWD.
    if [ -n "${OAP_PROJECT_ROOT:-}" ]; then
        case "$OAP_PROJECT_ROOT" in
            /*) ;;
            *)
                echo "project_env.sh: OAP_PROJECT_ROOT must be an absolute path" >&2
                return 1
                ;;
        esac
        if [ ! -d "$OAP_PROJECT_ROOT" ]; then
            echo "project_env.sh: OAP_PROJECT_ROOT is not a directory" >&2
            return 1
        fi
        if [ ! -f "$OAP_PROJECT_ROOT/pyproject.toml" ]; then
            echo "project_env.sh: OAP_PROJECT_ROOT has no pyproject.toml" >&2
            return 1
        fi
        _oap_env_root="$OAP_PROJECT_ROOT"
    else
        _oap_env_root=""
        if command -v git >/dev/null 2>&1; then
            _oap_env_git_root=$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null) || _oap_env_git_root=""
            if [ -n "$_oap_env_git_root" ] && [ -f "$_oap_env_git_root/pyproject.toml" ]; then
                _oap_env_root="$_oap_env_git_root"
            fi
        fi
        if [ -z "$_oap_env_root" ] && [ -f "$PWD/pyproject.toml" ]; then
            _oap_env_root="$PWD"
        fi
        if [ -z "$_oap_env_root" ]; then
            echo "project_env.sh: cannot locate the project root from $PWD; run from inside the repository or set OAP_PROJECT_ROOT" >&2
            return 1
        fi
    fi
    if [ ! -f "$_oap_env_root/pyproject.toml" ]; then
        echo "project_env.sh: resolved project root has no pyproject.toml" >&2
        return 1
    fi

    # Derive the project name from the checked-in policy.
    _oap_env_name=$(sed -n 's/^name[[:space:]]*=[[:space:]]*"\([^"]*\)"[[:space:]]*$/\1/p' \
        "$_oap_env_root/pyproject.toml" | sed -n 1p)
    if [ -z "$_oap_env_name" ]; then
        echo "project_env.sh: pyproject.toml has no readable [project] name" >&2
        return 1
    fi
    case "$_oap_env_name" in
        *[!A-Za-z0-9._-]*)
            echo "project_env.sh: project name is not a safe path component" >&2
            return 1
            ;;
    esac

    # Validate $HOME.
    if [ -z "${HOME:-}" ]; then
        echo "project_env.sh: \$HOME is not set; source this file from a shell that has HOME" >&2
        return 1
    fi
    case "$HOME" in
        /*) ;;
        *)
            echo "project_env.sh: \$HOME must be an absolute path" >&2
            return 1
            ;;
    esac
    if [ ! -d "$HOME" ]; then
        echo "project_env.sh: \$HOME is not an existing directory" >&2
        return 1
    fi

    # Machine-local targets, all derived from $HOME and the project name.
    _oap_env_env_dir="$HOME/envs/$_oap_env_name"
    _oap_env_pycache_dir="$HOME/.cache/python-pycache/$_oap_env_name"
    _oap_env_ruff_dir="$HOME/.cache/ruff/$_oap_env_name"
    _oap_env_mypy_dir="$HOME/.cache/mypy/$_oap_env_name"
    _oap_env_pytest_dir="$HOME/.cache/pytest/$_oap_env_name"
    _oap_env_tmp_dir="$HOME/.cache/tmp/$_oap_env_name"
    _oap_env_bin="$_oap_env_env_dir/bin"

    # The environment must live outside the repository.
    case "$_oap_env_env_dir" in
        "$_oap_env_root"/*)
            echo "project_env.sh: development environment would overlap the repository; it must live under \$HOME outside the repository" >&2
            return 1
            ;;
    esac
    if [ -L "$_oap_env_env_dir" ]; then
        echo "project_env.sh: environment path is a symlink; refusing to use it" >&2
        return 1
    fi
    if [ -e "$_oap_env_env_dir" ] && [ ! -d "$_oap_env_env_dir" ]; then
        echo "project_env.sh: environment path exists and is not a directory" >&2
        return 1
    fi

    # Create only the exact project-specific parent and cache directories.
    # Never creates the uv environment itself. Refuses symlink targets.
    _oap_env_ensure_dir() {
        _oap_ed_target="$1"
        if [ -L "$_oap_ed_target" ]; then
            echo "project_env.sh: refusing symlinked path in machine-local layout" >&2
            return 1
        fi
        if [ -e "$_oap_ed_target" ]; then
            if [ ! -d "$_oap_ed_target" ]; then
                echo "project_env.sh: machine-local path exists and is not a directory" >&2
                return 1
            fi
            return 0
        fi
        if ! mkdir -p "$_oap_ed_target" 2>/dev/null; then
            echo "project_env.sh: cannot create machine-local directory" >&2
            return 1
        fi
        if [ ! -d "$_oap_ed_target" ] || [ -L "$_oap_ed_target" ]; then
            echo "project_env.sh: machine-local directory creation did not produce a real directory" >&2
            return 1
        fi
        if command -v stat >/dev/null 2>&1 && command -v id >/dev/null 2>&1; then
            _oap_ed_owner=$(stat -c '%u' "$_oap_ed_target" 2>/dev/null) || \
                _oap_ed_owner=$(stat -f '%u' "$_oap_ed_target" 2>/dev/null) || _oap_ed_owner=""
            if [ -n "$_oap_ed_owner" ] && [ "$_oap_ed_owner" != "$(id -u)" ]; then
                echo "project_env.sh: machine-local directory is not owned by the current user" >&2
                return 1
            fi
        fi
        return 0
    }
    if ! _oap_env_ensure_dir "$HOME/envs"; then return 1; fi
    if ! _oap_env_ensure_dir "$_oap_env_pycache_dir"; then return 1; fi
    if ! _oap_env_ensure_dir "$_oap_env_ruff_dir"; then return 1; fi
    if ! _oap_env_ensure_dir "$_oap_env_mypy_dir"; then return 1; fi
    if ! _oap_env_ensure_dir "$_oap_env_pytest_dir"; then return 1; fi
    if ! _oap_env_ensure_dir "$_oap_env_tmp_dir"; then return 1; fi

    # PATH: put the environment bin first, exactly once, keeping other entries.
    if [ -n "${IFS+x}" ]; then
        _oap_env_ifs="$IFS"
        _oap_env_ifs_set=1
    else
        _oap_env_ifs=""
        _oap_env_ifs_set=0
    fi
    # Drop every existing occurrence of the environment bin, then prepend it
    # exactly once so the position stays first across repeated sourcing.
    IFS=':'
    _oap_env_newpath=""
    for _oap_env_entry in $PATH; do
        if [ -z "$_oap_env_entry" ]; then
            continue
        fi
        if [ "$_oap_env_entry" = "$_oap_env_bin" ]; then
            continue
        fi
        if [ -z "$_oap_env_newpath" ]; then
            _oap_env_newpath="$_oap_env_entry"
        else
            _oap_env_newpath="$_oap_env_newpath:$_oap_env_entry"
        fi
    done
    if [ "$_oap_env_ifs_set" = "1" ]; then
        IFS="$_oap_env_ifs"
    else
        unset IFS
    fi
    if [ -n "$_oap_env_newpath" ]; then
        PATH="$_oap_env_bin:$_oap_env_newpath"
    else
        PATH="$_oap_env_bin"
    fi
    export PATH
    export UV_PROJECT_ENVIRONMENT="$_oap_env_env_dir"
    export VIRTUAL_ENV="$_oap_env_env_dir"
    if [ -z "${PYTHONPYCACHEPREFIX:-}" ]; then
        export PYTHONPYCACHEPREFIX="$_oap_env_pycache_dir"
    fi
    if [ -z "${RUFF_CACHE_DIR:-}" ]; then
        export RUFF_CACHE_DIR="$_oap_env_ruff_dir"
    fi
    if [ -z "${MYPY_CACHE_DIR:-}" ]; then
        export MYPY_CACHE_DIR="$_oap_env_mypy_dir"
    fi
    if [ -z "${TMPDIR:-}" ]; then
        export TMPDIR="$_oap_env_tmp_dir"
    fi
    _oap_env_pytest_opt="-o cache_dir=$_oap_env_pytest_dir"
    if [ -n "${PYTEST_ADDOPTS:-}" ]; then
        case " ${PYTEST_ADDOPTS} " in
            *" $_oap_env_pytest_opt "*) ;;
            *) export PYTEST_ADDOPTS="$PYTEST_ADDOPTS $_oap_env_pytest_opt" ;;
        esac
    else
        export PYTEST_ADDOPTS="$_oap_env_pytest_opt"
    fi

    unset _oap_env_git_root _oap_env_ifs _oap_env_ifs_set _oap_env_newpath \
        _oap_env_entry _oap_env_pytest_opt _oap_ed_target \
        _oap_ed_owner
    return 0
}

# Sourced: abort only this file on failure. Executed directly: exit nonzero.
if ! _oap_env_main; then
    return 1 2>/dev/null || exit 1
fi
