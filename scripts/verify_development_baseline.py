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
from dataclasses import dataclass
from pathlib import Path
from threading import Thread
from time import monotonic
from typing import Any

PYTHON_SELECTOR = "3.12"
DEFAULT_COMMAND_TIMEOUT = 300.0
PROJECT_PACKAGE = "llm-slovenian-repair"
FORWARD_RECOVERY_HISTORY_SOURCE = "OAP_FORWARD_RECOVERY_HISTORY_SOURCE"
DIAGNOSTIC_CAPTURE_BYTES = 8192
DIAGNOSTIC_MAX_BYTES = 4096
PUBLIC_EXPORTS = (
    "__version__",
    "AcceptanceClass",
    "ContextDenominatorState",
    "Edit",
    "EvidenceCompleteness",
    "EvidenceRecord",
    "EvidenceState",
    "OriginalCoordinateEdit",
    "Policy",
    "PolicyConfig",
    "RepairDisposition",
    "RepairMode",
    "RepairReason",
    "RepairResult",
    "RepairSpan",
    "ReviewProposal",
    "ReviewProposalBatch",
    "SelectedSpan",
    "SelectionBatch",
    "SpanSelection",
    "StageTimings",
    "DEFAULT_MAX_MANIFEST_BYTES",
    "DEFAULT_MAX_PAYLOAD_BYTES",
    "DEFAULT_MAX_RECORDS",
    "ManifestDenominatorKnowledge",
    "ManifestVerificationError",
    "QueryKind",
    "RightsStatus",
    "SourceManifest",
    "SyntheticCorpus",
    "SyntheticCountRecord",
    "VerifiedSyntheticCorpus",
    "VerificationFailure",
    "verify_manifest_payload",
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
    )


def venv_python(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def validate_git_worktree(source: Path) -> Path:
    """Validate the caller-owned history source used by copied OAP tests."""

    try:
        resolved = source.expanduser().resolve(strict=True)
    except OSError as exc:
        raise DriverError("FORWARD_RECOVERY_HISTORY_SOURCE_UNAVAILABLE") from exc
    if not resolved.is_dir() or resolved.is_symlink():
        raise DriverError("FORWARD_RECOVERY_HISTORY_SOURCE_NOT_DIRECTORY")
    try:
        result = subprocess.run(
            ["git", "-C", str(resolved), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise DriverError("FORWARD_RECOVERY_HISTORY_SOURCE_NOT_GIT") from exc
    if result.returncode != 0:
        raise DriverError("FORWARD_RECOVERY_HISTORY_SOURCE_NOT_GIT")
    try:
        top_level = Path(result.stdout.strip()).resolve(strict=True)
    except OSError as exc:
        raise DriverError("FORWARD_RECOVERY_HISTORY_SOURCE_NOT_GIT") from exc
    if top_level != resolved:
        raise DriverError("FORWARD_RECOVERY_HISTORY_SOURCE_NOT_WORKTREE_ROOT")
    return resolved


def build_environment(
    paths: WorkspacePaths, *, forward_recovery_history_source: Path | None = None
) -> dict[str, str]:
    """Build child-process environment without exposing or logging its values."""

    env = os.environ.copy()
    for name in (
        "PYTHONHOME",
        "PYTHONPATH",
        "VIRTUAL_ENV",
        "UV_OFFLINE",
        FORWARD_RECOVERY_HISTORY_SOURCE,
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
    if forward_recovery_history_source is not None:
        env[FORWARD_RECOVERY_HISTORY_SOURCE] = str(
            validate_git_worktree(forward_recovery_history_source)
        )
    return env


def offline_environment(base: dict[str, str], paths: WorkspacePaths) -> dict[str, str]:
    env = base.copy()
    env.update(
        {
            "UV_OFFLINE": "1",
            "UV_PROJECT_ENVIRONMENT": str(paths.offline_environment),
            "HOME": str(paths.offline_home),
        }
    )
    return env


def uv_executable() -> str:
    return shutil.which("uv") or "uv"


def locked_runtime_versions(repo: Path) -> dict[str, str]:
    """Return the exact versions in the project's locked runtime closure."""

    try:
        lock = tomllib.loads((repo / "uv.lock").read_text(encoding="utf-8"))
        packages = {package["name"]: package for package in lock["package"]}
        pending = list(packages[PROJECT_PACKAGE].get("dependencies", []))
        versions: dict[str, str] = {PROJECT_PACKAGE: packages[PROJECT_PACKAGE]["version"]}
        while pending:
            name = pending.pop()["name"]
            if name in versions:
                continue
            package = packages[name]
            versions[name] = package["version"]
            pending.extend(package.get("dependencies", []))
    except (KeyError, OSError, TypeError, tomllib.TOMLDecodeError) as exc:
        raise DriverError("LOCK_METADATA_INVALID") from exc
    if not versions:
        raise DriverError("LOCKED_RUNTIME_VERSIONS_MISSING")
    return versions


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
    repo: Path,
    paths: WorkspacePaths,
    uv: str,
    wheel: Path,
    versions: dict[str, str],
) -> list[CommandSpec]:
    offline_python = str(venv_python(paths.offline_environment))
    import_code = (
        "import importlib.metadata as metadata, pathlib, sys; "
        f"expected = {versions!r}; "
        "root = pathlib.Path.cwd(); "
        "before_files = sorted(path.relative_to(root).as_posix() for path in root.rglob('*')); "
        "before_modules = set(sys.modules); "
        "package = __import__('llm_slovenian_repair'); "
        "after_modules = set(sys.modules); "
        f"expected_exports = {list(PUBLIC_EXPORTS)!r}; "
        "assert not {name for name in after_modules - before_modules if "
        "name == 'pydantic' or name.startswith('pydantic.') or "
        "name == 'pydantic_core' or name.startswith('pydantic_core.') or "
        "name == 'httpx' or name.startswith('httpx.')}; "
        "assert package.__all__ == expected_exports; "
        "assert package.__version__ == "
        f"expected['{PROJECT_PACKAGE}']; "
        "after_files = sorted(path.relative_to(root).as_posix() for path in root.rglob('*')); "
        "assert before_files == after_files; "
        "import httpx, pydantic, pydantic_core; "
        "assert package.PolicyConfig is "
        "__import__('llm_slovenian_repair.policy', fromlist=['PolicyConfig']).PolicyConfig; "
        "assert all(metadata.version(name) == version and "
        "metadata.metadata(name)['Name'].lower().replace('_', '-') == "
        "name.lower().replace('_', '-') for name, version in expected.items()); "
        "assert all(metadata.version(name) for name in ('pydantic', 'pydantic-core', 'httpx'))"
    )
    return [
        CommandSpec(
            "create fresh offline venv",
            (uv, "venv", "--python", PYTHON_SELECTOR, str(paths.offline_environment)),
            paths.root,
        ),
        CommandSpec(
            "offline runtime-only frozen sync",
            (
                uv,
                "sync",
                "--frozen",
                "--no-dev",
                "--no-install-project",
                "--python",
                PYTHON_SELECTOR,
            ),
            repo,
        ),
        CommandSpec(
            "offline wheel installation with dependencies",
            (uv, "pip", "install", "--python", offline_python, "--offline", str(wheel)),
            paths.outside_repository,
        ),
        CommandSpec(
            "offline runtime import and metadata",
            (offline_python, "-B", "-c", import_code),
            paths.outside_repository,
        ),
    ]


def record_command(
    records: list[dict[str, Any]],
    label: str,
    result: str,
    timeout: float,
    *,
    returncode: int | None = None,
    diagnostic: str | None = None,
) -> None:
    record: dict[str, Any] = {
        "label": label,
        "result": result,
        "timeout_seconds": timeout,
    }
    if result in {"FAILED", "TIMEOUT"}:
        if returncode is not None:
            record["returncode"] = returncode
        record["diagnostic"] = diagnostic or ""
    records.append(record)


def _tail(data: bytearray, chunk: bytes) -> None:
    data.extend(chunk)
    if len(data) > DIAGNOSTIC_CAPTURE_BYTES:
        del data[:-DIAGNOSTIC_CAPTURE_BYTES]


def _read_tail(stream: Any, target: bytearray) -> None:
    try:
        while True:
            chunk = stream.read(4096)
            if not chunk:
                return
            _tail(target, chunk)
    finally:
        stream.close()


def _redaction_forms(path: Path) -> tuple[str, ...]:
    resolved = path.resolve(strict=False)
    return tuple(dict.fromkeys((str(path), str(resolved), resolved.as_posix())))


def sanitize_diagnostic(
    data: bytes | str,
    *,
    repository: Path | None = None,
    temporary_root: Path | None = None,
) -> str:
    """Redact owned paths and bound a diagnostic to valid UTF-8 bytes."""

    text = data.decode("utf-8", errors="replace") if isinstance(data, bytes) else data
    for path, replacement in (
        (repository, "<repository>"),
        (temporary_root, "<temporary-root>"),
    ):
        if path is not None:
            for form in sorted(_redaction_forms(path), key=len, reverse=True):
                text = text.replace(form, replacement)
    text = "".join(char if ord(char) >= 32 and ord(char) != 127 else " " for char in text)
    text = " ".join(text.split())
    encoded = text.encode("utf-8")
    if len(encoded) > DIAGNOSTIC_MAX_BYTES:
        encoded = encoded[-DIAGNOSTIC_MAX_BYTES:]
        text = encoded.decode("utf-8", errors="ignore")
    return text


def failure_diagnostic(
    stdout: bytes,
    stderr: bytes,
    *,
    repository: Path | None = None,
    temporary_root: Path | None = None,
) -> str:
    parts: list[bytes] = []
    if stdout:
        parts.append(b"stdout: " + stdout)
    if stderr:
        parts.append(b"stderr: " + stderr)
    return sanitize_diagnostic(
        b" | ".join(parts), repository=repository, temporary_root=temporary_root
    )


def run_command(
    spec: CommandSpec,
    *,
    env: dict[str, str],
    timeout: float,
    records: list[dict[str, Any]],
    repository: Path | None = None,
    temporary_root: Path | None = None,
) -> None:
    started = monotonic()
    stdout_tail = bytearray()
    stderr_tail = bytearray()
    try:
        process = subprocess.Popen(
            list(spec.argv),
            cwd=spec.cwd,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        diagnostic = sanitize_diagnostic(
            f"{type(exc).__name__}: {exc}",
            repository=repository,
            temporary_root=temporary_root,
        )
        record_command(records, spec.label, "FAILED", timeout, diagnostic=diagnostic)
        raise CommandFailure(spec.label, "FAILED") from exc
    readers = [
        Thread(target=_read_tail, args=(process.stdout, stdout_tail), daemon=True),
        Thread(target=_read_tail, args=(process.stderr, stderr_tail), daemon=True),
    ]
    for reader in readers:
        reader.start()
    timed_out = False
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()
    finally:
        for reader in readers:
            reader.join(timeout=1)
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
    diagnostic = failure_diagnostic(
        bytes(stdout_tail),
        bytes(stderr_tail),
        repository=repository,
        temporary_root=temporary_root,
    )
    elapsed = monotonic() - started
    if timed_out:
        record_command(records, spec.label, "TIMEOUT", timeout, diagnostic=diagnostic)
        raise CommandFailure(spec.label, "TIMEOUT")
    if process.returncode != 0:
        record_command(
            records,
            spec.label,
            "FAILED",
            timeout,
            returncode=process.returncode,
            diagnostic=diagnostic,
        )
        raise CommandFailure(spec.label, "FAILED", process.returncode)
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
            if (repo / ".git").exists():
                env[FORWARD_RECOVERY_HISTORY_SOURCE] = str(validate_git_worktree(repo))
            versions = locked_runtime_versions(repo)
            uv = uv_executable()
            for spec in initial_command_specs(repo, paths, uv, test_repo):
                run_command(
                    spec,
                    env=env,
                    timeout=timeout,
                    records=records,
                    repository=repo,
                    temporary_root=owned_root,
                )
            run_command(
                build_command_spec(repo, paths, uv),
                env=env,
                timeout=timeout,
                records=records,
                repository=repo,
                temporary_root=owned_root,
            )
            wheel = select_wheel(paths.output, records, timeout)
            offline_env = offline_environment(env, paths)
            for spec in offline_command_specs(repo, paths, uv, wheel, versions):
                run_command(
                    spec,
                    env=offline_env,
                    timeout=timeout,
                    records=records,
                    repository=repo,
                    temporary_root=owned_root,
                )
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
