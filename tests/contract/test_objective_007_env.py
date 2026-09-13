"""Focused 007-k machine-local development environment contract tests.

These tests use a controlled fake HOME on a native temporary filesystem and a
clean POSIX shell environment. They never require the network: the helper
performs only local path operations and the bootstrap is exercised in --check
mode (plus its error paths), so no uv sync, download, or service call is made.
"""

from __future__ import annotations

import hashlib
import shutil
import socket
import stat
import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts" / "project_env.sh"
BOOTSTRAP = ROOT / "scripts" / "bootstrap_dev_env.sh"
ENVRc = ROOT / ".envrc"
PROJECT_NAME = "llm-slovenian-repair"

TIMEOUT = 180

# Captured once at import so any test mutation is detectable.
PYPROJECT_SHA = hashlib.sha256((ROOT / "pyproject.toml").read_bytes()).hexdigest()
LOCK_SHA = hashlib.sha256((ROOT / "uv.lock").read_bytes()).hexdigest()

# The fake HOME must live on a native filesystem outside the real $HOME and
# outside the repository, so no real user path can leak into the assertions.
_FAKE_HOME_BASE = Path(tempfile.gettempdir())


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture()
def fake_home() -> Iterator[Path]:
    directory = tempfile.TemporaryDirectory(prefix="oap-env-home-", dir=str(_FAKE_HOME_BASE))
    home = Path(directory.name) / "home"
    home.mkdir()
    yield home
    directory.cleanup()


def _base_path() -> str:
    parts = ["/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "/bin"]
    uv = shutil.which("uv")
    if uv:
        parts.insert(0, str(Path(uv).parent))
    return ":".join(dict.fromkeys(parts))


def _run(
    argv: list[str],
    *,
    home: Path,
    cwd: Path = ROOT,
    extra: dict[str, str] | None = None,
    path: str | None = None,
) -> subprocess.CompletedProcess[str]:
    env = {
        "HOME": str(home),
        "PATH": path or _base_path(),
        "OAP_PROJECT_ROOT": str(ROOT),
        "SHLVL": "1",
    }
    if extra:
        env.update(extra)
    return subprocess.run(
        argv,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )


def _parse_dumps(stdout: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in stdout.splitlines():
        if line.startswith("DUMP|"):
            name, _, value = line[len("DUMP|") :].partition("=")
            values[name] = value
    return values


def _source_helper(
    home: Path,
    *,
    source_twice: bool = False,
    extra: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    source = (
        f'. {HELPER}\nrc=$?\nif [ $rc -ne 0 ]; then printf "SOURCE_RC=%d\\n" $rc; exit $rc; fi\n'
    )
    if source_twice:
        source += f". {HELPER}\n"
    script = (
        source + "for v in UV_PROJECT_ENVIRONMENT VIRTUAL_ENV PATH PYTHONPYCACHEPREFIX "
        "RUFF_CACHE_DIR MYPY_CACHE_DIR PYTEST_ADDOPTS TMPDIR; do\n"
        + '  eval "val=\\${$v:-UNSET}"\n'
        + '  printf "DUMP|%s=%s\\n" "$v" "$val"\n'
        + "done\n"
        + 'printf "DUMP|ENV_DIR_EXISTS=%s\\n" '
        + '"$([ -d "${UV_PROJECT_ENVIRONMENT}" ] && printf yes || printf no)"\n'
        + 'printf "DUMP|ENV_PARENT_EXISTS=%s\\n" '
        + '"$([ -d "$(dirname "${UV_PROJECT_ENVIRONMENT}")" ] && printf yes || printf no)"\n'
    )
    return _run(["sh", "-c", script], home=home, extra=extra)


def test_helper_exports_exact_machine_local_paths(fake_home: Path) -> None:
    home = fake_home
    result = _source_helper(home)
    assert result.returncode == 0, result.stderr
    env = _parse_dumps(result.stdout)
    assert env["UV_PROJECT_ENVIRONMENT"] == f"{home}/envs/{PROJECT_NAME}"
    assert env["VIRTUAL_ENV"] == f"{home}/envs/{PROJECT_NAME}"
    expected_bin = f"{home}/envs/{PROJECT_NAME}/bin"
    path_entries = env["PATH"].split(":")
    assert path_entries[0] == expected_bin
    assert path_entries.count(expected_bin) == 1
    assert env["PYTHONPYCACHEPREFIX"] == f"{home}/.cache/python-pycache/{PROJECT_NAME}"
    assert env["RUFF_CACHE_DIR"] == f"{home}/.cache/ruff/{PROJECT_NAME}"
    assert env["MYPY_CACHE_DIR"] == f"{home}/.cache/mypy/{PROJECT_NAME}"
    assert env["PYTEST_ADDOPTS"] == f"-o cache_dir={home}/.cache/pytest/{PROJECT_NAME}"
    assert env["TMPDIR"] == f"{home}/.cache/tmp/{PROJECT_NAME}"
    # The helper creates the parent and caches, never the uv environment.
    assert env["ENV_PARENT_EXISTS"] == "yes"
    assert env["ENV_DIR_EXISTS"] == "no"
    for sub in ("python-pycache", "ruff", "mypy", "pytest", "tmp"):
        assert (home / ".cache" / sub / PROJECT_NAME).is_dir()
    # Every exported path is derived from the fake HOME only: no repository
    # path and no real hostname may appear.
    for name in (
        "UV_PROJECT_ENVIRONMENT",
        "VIRTUAL_ENV",
        "PYTHONPYCACHEPREFIX",
        "RUFF_CACHE_DIR",
        "MYPY_CACHE_DIR",
        "TMPDIR",
    ):
        assert str(home) in env[name]
        assert str(ROOT) not in env[name]
    assert socket.gethostname() not in result.stdout


def test_helper_sourcing_is_idempotent(fake_home: Path) -> None:
    result = _source_helper(fake_home, source_twice=True)
    assert result.returncode == 0, result.stderr
    env = _parse_dumps(result.stdout)
    expected_bin = f"{fake_home}/envs/{PROJECT_NAME}/bin"
    assert env["PATH"].split(":").count(expected_bin) == 1
    assert env["PATH"].split(":")[0] == expected_bin
    assert env["UV_PROJECT_ENVIRONMENT"] == f"{fake_home}/envs/{PROJECT_NAME}"
    assert env["PYTEST_ADDOPTS"] == f"-o cache_dir={fake_home}/.cache/pytest/{PROJECT_NAME}"


def test_helper_paths_stay_outside_the_repository(fake_home: Path) -> None:
    result = _source_helper(fake_home)
    assert result.returncode == 0, result.stderr
    env = _parse_dumps(result.stdout)
    for name in (
        "UV_PROJECT_ENVIRONMENT",
        "PYTHONPYCACHEPREFIX",
        "RUFF_CACHE_DIR",
        "MYPY_CACHE_DIR",
        "TMPDIR",
    ):
        assert not env[name].startswith(str(ROOT))
    assert (fake_home / "envs").is_dir()
    assert not (fake_home / "envs" / PROJECT_NAME).exists()


def test_helper_execution_fails_with_instruction(fake_home: Path) -> None:
    for argv in (
        ["sh", "-c", f"sh {HELPER}"],
        ["sh", "-c", f"dash {HELPER}"],
    ):
        result = _run(argv, home=fake_home)
        assert result.returncode != 0
        assert "sourced" in result.stderr


def test_helper_rejects_missing_or_relative_home(fake_home: Path) -> None:
    for bad_home in ("", "relative/home"):
        result = _run(
            ["sh", "-c", f". {HELPER}"],
            home=fake_home,
            extra={"HOME": bad_home},
        )
        assert result.returncode != 0, (bad_home, result.stdout, result.stderr)
        assert "HOME" in result.stderr


def test_helper_preserves_unrelated_environment_options(fake_home: Path) -> None:
    home = fake_home
    extra = {
        "PYTHONPYCACHEPREFIX": f"{home}/custom-pycache",
        "RUFF_CACHE_DIR": f"{home}/custom-ruff",
        "MYPY_CACHE_DIR": f"{home}/custom-mypy",
        "TMPDIR": f"{home}/custom-tmp",
        "PYTEST_ADDOPTS": "--strict-markers",
    }
    result = _source_helper(home, extra=extra)
    assert result.returncode == 0, result.stderr
    env = _parse_dumps(result.stdout)
    assert env["PYTHONPYCACHEPREFIX"] == f"{home}/custom-pycache"
    assert env["RUFF_CACHE_DIR"] == f"{home}/custom-ruff"
    assert env["MYPY_CACHE_DIR"] == f"{home}/custom-mypy"
    assert env["TMPDIR"] == f"{home}/custom-tmp"
    assert env["PYTEST_ADDOPTS"] == (
        f"--strict-markers -o cache_dir={home}/.cache/pytest/{PROJECT_NAME}"
    )
    # Canonical project environment variables are always the project target.
    assert env["UV_PROJECT_ENVIRONMENT"] == f"{home}/envs/{PROJECT_NAME}"


def test_helper_root_resolution_without_override(fake_home: Path) -> None:
    script = (
        f"cd {ROOT}\n. {HELPER}\n"
        'printf "DUMP|UV_PROJECT_ENVIRONMENT=%s\\n" "$UV_PROJECT_ENVIRONMENT"\n'
        'printf "DUMP|ENV_PARENT_EXISTS=%s\\n" '
        + '"$([ -d "$(dirname "$UV_PROJECT_ENVIRONMENT")" ] && printf yes || printf no)"\n'
    )
    result = _run(["sh", "-c", script], home=fake_home, extra={"OAP_PROJECT_ROOT": ""})
    assert result.returncode == 0, result.stderr
    env = _parse_dumps(result.stdout)
    assert env["UV_PROJECT_ENVIRONMENT"] == f"{fake_home}/envs/{PROJECT_NAME}"
    assert env["ENV_PARENT_EXISTS"] == "yes"


def test_envrc_only_delegates_to_the_canonical_helper() -> None:
    assert ENVRc.is_file()
    commands = [
        line.strip()
        for line in ENVRc.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert commands == ['. "$PWD/scripts/project_env.sh"']
    text = ENVRc.read_text(encoding="utf-8")
    assert "curl" not in text and "wget" not in text and "export" not in text


def test_gitignore_retains_environment_ignores(fake_home: Path) -> None:
    # Hermetic since 007-l: exercise the real Git ignore engine in a
    # disposable repository owned by the test, independent of the source
    # tree's .git (the baseline driver copies the source without it).
    repo = fake_home / "ignore-repo"
    repo.mkdir()
    init = subprocess.run(
        ["git", "init", "-q", str(repo)],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
    )
    assert init.returncode == 0, (init.stdout, init.stderr)
    (repo / ".gitignore").write_bytes((ROOT / ".gitignore").read_bytes())
    # Directory-only patterns need the directory type to be verifiable.
    for directory in (".pytest_cache", ".mypy_cache", ".ruff_cache"):
        (repo / directory).mkdir()

    def ignored(path: str) -> bool:
        result = subprocess.run(
            ["git", "-C", str(repo), "check-ignore", "--no-index", "-q", path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        # 0 = ignored, 1 = not ignored; anything else is a Git error and is
        # a test failure, not a clean "not ignored".
        assert result.returncode in (0, 1), (path, result.stdout, result.stderr)
        return result.returncode == 0

    for path in (
        ".venv",
        ".venv/bin/python",
        "foo/__pycache__/",
        "module.pyc",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "sub/.envrc",
    ):
        assert ignored(path), path
    assert not ignored(".envrc")


def test_bootstrap_check_mode_prints_plan_without_syncing(fake_home: Path) -> None:
    if shutil.which("uv") is None:
        pytest.skip("uv is not available in this test environment")
    result = _run(["sh", str(BOOTSTRAP), "--check"], home=fake_home)
    assert result.returncode == 0, result.stderr
    assert f"{fake_home}/envs/{PROJECT_NAME}" in result.stdout
    assert "--check" in result.stdout
    assert not (fake_home / "envs" / PROJECT_NAME).exists()


def test_bootstrap_rejects_unknown_or_excess_arguments(fake_home: Path) -> None:
    for argv in (["sh", str(BOOTSTRAP), "--bogus"], ["sh", str(BOOTSTRAP), "a", "b"]):
        result = _run(argv, home=fake_home)
        assert result.returncode != 0
        assert result.stderr != ""


def test_bootstrap_rejects_relative_home(fake_home: Path) -> None:
    result = _run(
        ["sh", str(BOOTSTRAP), "--check"],
        home=fake_home,
        extra={"HOME": "relative/home"},
    )
    assert result.returncode != 0
    assert "HOME" in result.stderr


def test_bootstrap_rejects_repository_overlap() -> None:
    result = _run(
        ["sh", str(BOOTSTRAP), "--check"],
        home=ROOT,
        extra={"HOME": str(ROOT), "OAP_PROJECT_ROOT": str(ROOT)},
    )
    assert result.returncode != 0
    assert "overlap" in result.stderr


def test_bootstrap_rejects_symlink_environment(fake_home: Path) -> None:
    target = fake_home.parent / "outside-env"
    target.mkdir()
    env_dir = fake_home / "envs" / PROJECT_NAME
    env_dir.parent.mkdir(parents=True)
    env_dir.symlink_to(target)
    result = _run(["sh", str(BOOTSTRAP), "--check"], home=fake_home)
    assert result.returncode != 0
    assert "symlink" in result.stderr


def test_bootstrap_rejects_unsupported_uv_version(fake_home: Path) -> None:
    if shutil.which("uv") is None:
        pytest.skip("uv is not available in this test environment")
    fake_bin = fake_home.parent / "fake-bin"
    fake_bin.mkdir()
    fake_uv = fake_bin / "uv"
    fake_uv.write_text(
        "#!/bin/sh\n"
        'if [ "$1" = "--version" ]; then echo "uv 0.10.4 (x86_64-unknown-linux-gnu)"; fi\n',
        encoding="utf-8",
    )
    fake_uv.chmod(fake_uv.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    result = _run(
        ["sh", str(BOOTSTRAP), "--check"],
        home=fake_home,
        path=f"{fake_bin}:{_base_path()}",
    )
    assert result.returncode != 0
    assert "required-version" in result.stderr


def test_bootstrap_rejects_missing_lockfile(fake_home: Path) -> None:
    fake_root = fake_home.parent / "fake-root"
    fake_root.mkdir()
    (fake_root / "pyproject.toml").write_text(
        '[project]\nname = "llm-slovenian-repair"\nversion = "0.0.0"\n', encoding="utf-8"
    )
    result = _run(
        ["sh", str(BOOTSTRAP), "--check"],
        home=fake_home,
        extra={"OAP_PROJECT_ROOT": str(fake_root)},
    )
    assert result.returncode != 0
    assert "uv.lock" in result.stderr


def test_helper_and_bootstrap_have_no_hardcoded_host_paths() -> None:
    forbidden = {"ubuntu", "/home/ubuntu", socket.gethostname()}
    for path in (HELPER, BOOTSTRAP):
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text, (path.name, token)


def test_project_metadata_unchanged_by_environment_workflow() -> None:
    assert _sha256(ROOT / "pyproject.toml") == PYPROJECT_SHA
    assert _sha256(ROOT / "uv.lock") == LOCK_SHA
