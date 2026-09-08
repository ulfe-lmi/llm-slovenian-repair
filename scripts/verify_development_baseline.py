#!/usr/bin/env python3
"""Run the complete development baseline in owned native temporary paths."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
import zipfile
from dataclasses import dataclass
from pathlib import Path
from time import monotonic
from typing import Any

PYTHON_SELECTOR = "3.12"
DEFAULT_COMMAND_TIMEOUT = 300.0
REQUIRED_PACKAGES = (
    "llm-slovenian-repair",
    "pydantic",
    "pydantic-core",
    "httpx",
)


class DriverError(RuntimeError):
    """A bounded verification-driver policy or execution failure."""


class CommandFailure(DriverError):
    """A named command timed out or returned a non-zero status."""

    def __init__(self, label: str, result: str, returncode: int | None = None) -> None:
        self.label = label
        self.result = result
        self.returncode = returncode
        detail = f"{label}:{result}"
        if returncode is not None:
            detail += f":{returncode}"
        super().__init__(detail)


@dataclass(frozen=True)
class WorkspacePaths:
    """All disposable paths owned by one driver invocation."""

    root: Path
    project_environment: Path
    cache: Path
    ruff_cache: Path
    mypy_cache: Path
    output: Path
    offline_environment: Path
    offline_home: Path
    outside_repository: Path
    pytest_workspace: Path
    wheelhouse: Path


@dataclass(frozen=True)
class CommandSpec:
    label: str
    argv: tuple[str, ...]
    cwd: Path


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_temp_parent(repo: Path, candidate: str | os.PathLike[str]) -> Path:
    """Resolve an existing native parent without creating caller paths."""

    repo_resolved = repo.resolve()
    parent = Path(candidate).expanduser().resolve(strict=True)
    if parent == repo_resolved or repo_resolved in parent.parents:
        raise DriverError("TEMP_PARENT_INSIDE_REPOSITORY")
    if not parent.is_dir() or parent.is_symlink():
        raise DriverError("TEMP_PARENT_NOT_DIRECTORY")
    return parent


def workspace_paths(root: Path) -> WorkspacePaths:
    return WorkspacePaths(
        root=root,
        project_environment=root / "project-environment",
        cache=root / "cache",
        ruff_cache=root / "ruff-cache",
        mypy_cache=root / "mypy-cache",
        output=root / "artifacts",
        offline_environment=root / "offline-environment",
        offline_home=root / "offline-home",
        outside_repository=root / "outside-repository",
        pytest_workspace=root / "pytest-workspace",
        wheelhouse=root / "wheelhouse",
    )


def venv_python(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def build_environment(paths: WorkspacePaths) -> dict[str, str]:
    """Build child-process environment without exposing or logging its values."""

    env = os.environ.copy()
    for name in (
        "PYTHONHOME",
        "PYTHONPATH",
        "VIRTUAL_ENV",
        "UV_OFFLINE",
        "UV_NO_INDEX",
        "PIP_NO_INDEX",
    ):
        env.pop(name, None)
    env.update(
        {
            "UV_PROJECT_ENVIRONMENT": str(paths.project_environment),
            "UV_CACHE_DIR": str(paths.cache),
            "UV_LINK_MODE": "copy",
            "UV_PYTHON": PYTHON_SELECTOR,
            "PYTHONNOUSERSITE": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "RUFF_CACHE_DIR": str(paths.ruff_cache),
            "MYPY_CACHE_DIR": str(paths.mypy_cache),
        }
    )
    return env


def offline_environment(base: dict[str, str], paths: WorkspacePaths) -> dict[str, str]:
    env = base.copy()
    env.update(
        {
            "UV_OFFLINE": "1",
            "UV_NO_INDEX": "1",
            "PIP_NO_INDEX": "1",
            "UV_PROJECT_ENVIRONMENT": str(paths.offline_environment),
            "HOME": str(paths.offline_home),
        }
    )
    return env


def uv_executable() -> str:
    return shutil.which("uv") or "uv"


def locked_versions(repo: Path) -> dict[str, str]:
    try:
        lock = tomllib.loads((repo / "uv.lock").read_text(encoding="utf-8"))
        packages = lock["package"]
        versions = {
            package["name"]: package["version"]
            for package in packages
            if package["name"] in REQUIRED_PACKAGES
        }
    except (KeyError, OSError, TypeError, tomllib.TOMLDecodeError) as exc:
        raise DriverError("LOCK_METADATA_INVALID") from exc
    if set(versions) != set(REQUIRED_PACKAGES):
        raise DriverError("LOCKED_RUNTIME_VERSIONS_MISSING")
    return versions


def runtime_package_names(repo: Path) -> list[str]:
    try:
        lock = tomllib.loads((repo / "uv.lock").read_text(encoding="utf-8"))
        packages = {package["name"]: package for package in lock["package"]}
        pending = ["llm-slovenian-repair"]
        names: list[str] = []
        while pending:
            name = pending.pop()
            if name in names:
                continue
            package = packages[name]
            names.append(name)
            pending.extend(dependency["name"] for dependency in package.get("dependencies", []))
    except (KeyError, OSError, TypeError, tomllib.TOMLDecodeError) as exc:
        raise DriverError("LOCK_RUNTIME_GRAPH_INVALID") from exc
    return names


def _pytest_args(*paths: str, ignore_repository_venv: bool = False) -> tuple[str, ...]:
    args = ["pytest", "-p", "no:cacheprovider"]
    if ignore_repository_venv:
        args.extend(("--ignore=.venv",))
    args.extend(paths)
    return tuple(args)


def initial_command_specs(
    repo: Path,
    paths: WorkspacePaths,
    uv: str,
    test_repo: Path | None = None,
) -> list[CommandSpec]:
    test_cwd = test_repo or repo
    python = str(venv_python(paths.project_environment))
    return [
        CommandSpec("uv lock --check", (uv, "lock", "--check"), repo),
        CommandSpec(
            "frozen dependency sync",
            (uv, "sync", "--frozen", "--all-groups", "--all-extras", "--python", PYTHON_SELECTOR),
            repo,
        ),
        CommandSpec(
            "focused contract tests",
            (
                uv,
                "run",
                "--frozen",
                "--python",
                PYTHON_SELECTOR,
                *_pytest_args("tests/contract/test_objective_001.py", "-q"),
            ),
            repo,
        ),
        CommandSpec(
            "full pytest",
            (
                uv,
                "run",
                "--frozen",
                "--python",
                PYTHON_SELECTOR,
                *_pytest_args("-q", ignore_repository_venv=True),
            ),
            test_cwd,
        ),
        CommandSpec(
            "Ruff",
            (
                uv,
                "run",
                "--frozen",
                "--python",
                PYTHON_SELECTOR,
                "ruff",
                "check",
                "src",
                "scripts",
                "tests",
            ),
            repo,
        ),
        CommandSpec(
            "mypy",
            (uv, "run", "--frozen", "--python", PYTHON_SELECTOR, "mypy", "src", "tests/contract"),
            repo,
        ),
        CommandSpec(
            "OAP unittest discovery",
            (python, "-B", "-m", "unittest", "discover", "-s", "oap/tests", "-v"),
            test_cwd,
        ),
    ]


def build_command_spec(repo: Path, paths: WorkspacePaths, uv: str) -> CommandSpec:
    return CommandSpec(
        "sdist and wheel build",
        (uv, "build", "--no-sources", "--out-dir", str(paths.output)),
        repo,
    )


def offline_command_specs(
    paths: WorkspacePaths,
    uv: str,
    wheel: Path,
    wheelhouse: Path,
    versions: dict[str, str],
) -> list[CommandSpec]:
    offline_python = str(venv_python(paths.offline_environment))
    import_code = (
        "import importlib.metadata as metadata; "
        "import llm_slovenian_repair, httpx, pydantic, pydantic_core; "
        f"expected = {versions!r}; "
        "assert llm_slovenian_repair.__version__ == expected['llm-slovenian-repair']; "
        "assert all(metadata.version(name) == version and "
        "metadata.metadata(name)['Name'].lower().replace('_', '-') == "
        "name.lower().replace('_', '-') "
        "for name, version in expected.items())"
    )
    return [
        CommandSpec(
            "create fresh offline venv",
            (uv, "venv", "--python", PYTHON_SELECTOR, str(paths.offline_environment)),
            paths.root,
        ),
        CommandSpec(
            "offline wheel installation with dependencies",
            (
                uv,
                "pip",
                "install",
                "--python",
                offline_python,
                "--offline",
                "--no-index",
                "--find-links",
                str(wheelhouse),
                str(wheel),
            ),
            paths.outside_repository,
        ),
        CommandSpec(
            "offline runtime import and metadata",
            (offline_python, "-B", "-c", import_code),
            paths.outside_repository,
        ),
    ]


def record_command(records: list[dict[str, Any]], label: str, result: str, timeout: float) -> None:
    records.append(
        {
            "label": label,
            "result": result,
            "timeout_seconds": timeout,
        }
    )


def run_command(
    spec: CommandSpec,
    *,
    env: dict[str, str],
    timeout: float,
    records: list[dict[str, Any]],
) -> None:
    started = monotonic()
    try:
        completed = subprocess.run(
            list(spec.argv),
            cwd=spec.cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        record_command(records, spec.label, "TIMEOUT", timeout)
        raise CommandFailure(spec.label, "TIMEOUT") from exc
    except OSError as exc:
        record_command(records, spec.label, "FAILED", timeout)
        raise CommandFailure(spec.label, "FAILED") from exc
    elapsed = monotonic() - started
    if completed.returncode != 0:
        record_command(records, spec.label, "FAILED", timeout)
        raise CommandFailure(spec.label, "FAILED", completed.returncode)
    record_command(records, spec.label, "PASSED", timeout)
    if elapsed < 0:  # pragma: no cover - monotonic is only sanity-protected.
        raise DriverError("CLOCK_INVALID")


def select_wheel(output: Path, records: list[dict[str, Any]], timeout: float) -> Path:
    wheels = sorted(output.glob("*.whl"))
    if len(wheels) != 1:
        record_command(records, "select built wheel", "FAILED", timeout)
        raise DriverError("EXPECTED_ONE_WHEEL")
    record_command(records, "select built wheel", "PASSED", timeout)
    return wheels[0]


def materialize_cached_runtime_wheels(
    repo: Path,
    paths: WorkspacePaths,
    records: list[dict[str, Any]],
    timeout: float,
) -> None:
    """Expose frozen-sync cache entries to the offline wheel resolver."""

    cache_root = paths.cache / "wheels-v6" / "pypi"
    try:
        lock = tomllib.loads((repo / "uv.lock").read_text(encoding="utf-8"))
        packages = {package["name"]: package for package in lock["package"]}
        paths.wheelhouse.mkdir()
        for name in runtime_package_names(repo):
            if name == "llm-slovenian-repair":
                continue
            version = packages[name]["version"]
            candidates = sorted(
                path
                for path in (cache_root / name).glob(f"{version}-*")
                if path.is_dir()
            )
            if len(candidates) != 1:
                record_command(records, "materialize cached runtime wheelhouse", "FAILED", timeout)
                raise DriverError("CACHED_RUNTIME_WHEEL_MISSING")
            source = candidates[0]
            destination = paths.wheelhouse / f"{name.replace('-', '_')}-{source.name}.whl"
            with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for path in source.rglob("*"):
                    if path.is_file():
                        archive.write(path, path.relative_to(source).as_posix())
    except (KeyError, OSError, TypeError, tomllib.TOMLDecodeError, zipfile.BadZipFile) as exc:
        record_command(records, "materialize cached runtime wheelhouse", "FAILED", timeout)
        raise DriverError("CACHED_RUNTIME_WHEELHOUSE_INVALID") from exc
    record_command(records, "materialize cached runtime wheelhouse", "PASSED", timeout)


def validate_owned_root(root: Path, repo: Path) -> None:
    resolved = root.resolve()
    repo_resolved = repo.resolve()
    if resolved == repo_resolved or repo_resolved in resolved.parents:
        raise DriverError("TEMP_ROOT_INSIDE_REPOSITORY")
    info = resolved.lstat()
    if not stat.S_ISDIR(info.st_mode) or resolved.is_symlink() or info.st_uid != os.getuid():
        raise DriverError("TEMP_ROOT_NOT_OWNED_DIRECTORY")


def prepare_test_workspace(repo: Path, paths: WorkspacePaths) -> Path:
    """Copy readable source into the owned root while excluding review residue."""

    ignored_names = {
        ".git",
        ".venv",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "build",
        "dist",
    }

    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name in ignored_names or name.startswith(".oap-immutable-")
        }

    shutil.copytree(repo, paths.pytest_workspace, symlinks=True, ignore=ignore)
    if (paths.pytest_workspace / ".venv").exists():
        raise DriverError("PYTEST_WORKSPACE_CONTAINS_REPOSITORY_VENV")
    return paths.pytest_workspace


def run_verification(
    repo: Path, temp_parent: str | os.PathLike[str], timeout: float
) -> dict[str, Any]:
    if sys.version_info[:2] != (3, 12):
        return {
            "result": "FAILED",
            "failure": "PYTHON_3_12_REQUIRED",
            "commands": [],
            "cleanup": "NOT RUN",
        }
    if timeout <= 0:
        return {
            "result": "FAILED",
            "failure": "TIMEOUT_MUST_BE_POSITIVE",
            "commands": [],
            "cleanup": "NOT RUN",
        }

    records: list[dict[str, Any]] = []
    owned_root: Path | None = None
    cleanup = "NOT RUN"
    failure: str | None = None
    try:
        parent = resolve_temp_parent(repo, temp_parent)
        with tempfile.TemporaryDirectory(prefix="llm-slovenian-repair-", dir=parent) as temporary:
            owned_root = Path(temporary)
            validate_owned_root(owned_root, repo)
            paths = workspace_paths(owned_root)
            paths.output.mkdir()
            paths.outside_repository.mkdir()
            paths.offline_home.mkdir()
            test_repo = prepare_test_workspace(repo, paths)
            env = build_environment(paths)
            versions = locked_versions(repo)
            uv = uv_executable()
            for spec in initial_command_specs(repo, paths, uv, test_repo):
                run_command(spec, env=env, timeout=timeout, records=records)
            run_command(
                build_command_spec(repo, paths, uv), env=env, timeout=timeout, records=records
            )
            wheel = select_wheel(paths.output, records, timeout)
            materialize_cached_runtime_wheels(repo, paths, records, timeout)
            offline_env = offline_environment(env, paths)
            for spec in offline_command_specs(paths, uv, wheel, paths.wheelhouse, versions):
                run_command(spec, env=offline_env, timeout=timeout, records=records)
        cleanup = "PASSED" if owned_root is not None and not owned_root.exists() else "FAILED"
    except (CommandFailure, DriverError) as exc:
        failure = str(exc)
        if owned_root is not None:
            cleanup = "PASSED" if not owned_root.exists() else "FAILED"
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        failure = type(exc).__name__
        if owned_root is not None:
            cleanup = "PASSED" if not owned_root.exists() else "FAILED"
    result: dict[str, Any] = {
        "result": "PASSED" if failure is None else "FAILED",
        "commands": records,
        "cleanup": cleanup,
    }
    if failure is not None:
        result["failure"] = failure
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--temp-parent",
        default="/tmp",
        help="existing native directory for the owned TemporaryDirectory",
    )
    parser.add_argument(
        "--command-timeout",
        type=float,
        default=DEFAULT_COMMAND_TIMEOUT,
        help="finite timeout in seconds for every subprocess",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    summary = run_verification(repository_root(), args.temp_parent, args.command_timeout)
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["result"] == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
