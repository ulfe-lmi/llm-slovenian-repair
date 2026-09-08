"""Contract checks for the reproducible, side-effect-free package baseline."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import tomllib
from email import message_from_bytes
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import pytest

ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = ROOT / "pyproject.toml"
LOCKFILE = ROOT / "uv.lock"
DRIVER_PATH = ROOT / "scripts" / "verify_development_baseline.py"


def load_driver() -> Any:
    spec = importlib.util.spec_from_file_location("verify_development_baseline", DRIVER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_project() -> dict[str, object]:
    with PYPROJECT.open("rb") as handle:
        return tomllib.load(handle)


def test_project_metadata_and_dependency_boundaries() -> None:
    project = read_project()["project"]
    assert isinstance(project, dict)
    assert project["name"] == "llm-slovenian-repair"
    assert project["version"] == "0.0.0"
    assert project["requires-python"] == ">=3.12,<3.13"
    assert project["license"] == {"file": "LICENSE"}
    assert project["dependencies"] == ["httpx>=0.28.1,<1", "pydantic>=2.13.5,<3"]
    assert project["optional-dependencies"] == {"morphology": []}

    groups = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["dependency-groups"]
    assert groups == {
        "dev": ["mypy>=2.3.1,<3", "pytest>=9.1.1,<10", "ruff>=0.16.6,<0.17"]
    }


def test_lock_is_frozen_and_has_only_allowed_sources() -> None:
    assert LOCKFILE.is_file()
    lock_text = LOCKFILE.read_text(encoding="utf-8")
    lock = tomllib.loads(lock_text)
    assert lock["version"] == 1
    assert lock["revision"] == 3
    assert lock["requires-python"] == "==3.12.*"
    assert 'name = "llm-slovenian-repair"' in lock_text
    assert 'name = "fastapi"' not in lock_text
    assert 'name = "torch"' not in lock_text
    assert 'name = "transformers"' not in lock_text
    assert 'name = "spacy"' not in lock_text
    assert 'name = "stanza"' not in lock_text
    assert "source = { git" not in lock_text
    assert "source = { url" not in lock_text
    assert "source = { directory" not in lock_text
    assert "source = { path" not in lock_text

    packages = lock["package"]
    assert isinstance(packages, list)
    project_package = next(item for item in packages if item["name"] == "llm-slovenian-repair")
    assert project_package["version"] == "0.0.0"
    assert project_package["dependencies"] == [
        {"name": "httpx"},
        {"name": "pydantic"},
    ]
    assert project_package["metadata"]["provides-extras"] == ["morphology"]


def test_installed_import_isolation() -> None:
    code = r"""
import importlib.metadata
import pathlib
import socket
import sys
import urllib.request

root = pathlib.Path.cwd()
before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))

def blocked(*args, **kwargs):
    raise AssertionError("network access during package import")

socket.create_connection = blocked
socket.socket.connect = blocked
urllib.request.urlopen = blocked

module = __import__("llm_slovenian_repair")
assert importlib.metadata.version("llm-slovenian-repair") == "0.0.0"
assert module.__version__ == "0.0.0"
assert module.__all__ == ["__version__"]
assert "pydantic" not in sys.modules
assert "httpx" not in sys.modules
assert not any(
    name.startswith(("torch", "transformers", "spacy", "stanza")) for name in sys.modules
)
after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
assert before == after
"""
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-import-") as temp_dir:
        temp = Path(temp_dir)
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env["HOME"] = str(temp / "home")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [sys.executable, "-B", "-c", code],
            cwd=temp,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
    assert completed.returncode == 0, completed.stderr or completed.stdout


def test_built_wheel_metadata_and_payload() -> None:
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-wheel-") as temp_dir:
        output_dir = Path(temp_dir)
        completed = subprocess.run(
            ["uv", "build", "--no-sources", "--wheel", "--out-dir", str(output_dir)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout
        wheels = list(output_dir.glob("*.whl"))
        assert len(wheels) == 1
        with ZipFile(wheels[0]) as archive:
            names = archive.namelist()
            metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
            metadata = message_from_bytes(archive.read(metadata_name))
            assert metadata["Name"] == "llm-slovenian-repair"
            assert metadata["Version"] == "0.0.0"
            assert metadata["Requires-Python"] == "<3.13,>=3.12"
            assert metadata["License"].startswith("Apache License")
            assert metadata["License-File"] == "LICENSE"
            requires_dist = metadata.get_all("Requires-Dist") or []
            assert sorted(requires_dist) == [
                "httpx<1,>=0.28.1",
                "pydantic<3,>=2.13.5",
            ]
            assert all(
                not name.startswith("llm_slovenian_repair/")
                or name.endswith(("__init__.py", "py.typed"))
                for name in names
            )
            assert not any(
                token in name.lower()
                for name in names
                for token in ("model", "corpus", "weights")
            )


def test_driver_environment_uses_owned_native_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    driver = load_driver()
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-driver-test-") as temp_dir:
        paths = driver.workspace_paths(Path(temp_dir))
        monkeypatch.setenv("PYTHONPATH", "synthetic-private-value")
        env = driver.build_environment(paths)
        assert env["UV_PROJECT_ENVIRONMENT"] == str(paths.project_environment)
        assert env["UV_CACHE_DIR"] == str(paths.cache)
        assert env["UV_LINK_MODE"] == "copy"
        assert env["UV_PYTHON"] == "3.12"
        assert "PYTHONPATH" not in env
        assert env["RUFF_CACHE_DIR"] == str(paths.ruff_cache)
        assert env["MYPY_CACHE_DIR"] == str(paths.mypy_cache)


def test_driver_refuses_repository_temp_parent() -> None:
    driver = load_driver()
    with pytest.raises(driver.DriverError, match="TEMP_PARENT_INSIDE_REPOSITORY"):
        driver.resolve_temp_parent(ROOT, ROOT)


def test_driver_command_order_and_offline_dependency_policy() -> None:
    driver = load_driver()
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-driver-test-") as temp_dir:
        paths = driver.workspace_paths(Path(temp_dir))
        initial = driver.initial_command_specs(ROOT, paths, "uv")
        wheel = paths.output / "llm_slovenian_repair-0.0.0-py3-none-any.whl"
        offline = driver.offline_command_specs(
            ROOT,
            paths,
            "uv",
            wheel,
            {"httpx": "0.0.0", "pydantic": "0.0.0"},
        )
        labels = [
            spec.label
            for spec in initial + [driver.build_command_spec(ROOT, paths, "uv")] + offline
        ]
        assert labels == [
            "uv lock --check",
            "frozen dependency sync",
            "focused contract tests",
            "full pytest",
            "Ruff",
            "mypy",
            "OAP unittest discovery",
            "sdist and wheel build",
            "create fresh offline venv",
            "offline runtime-only frozen sync",
            "offline wheel installation with dependencies",
            "offline runtime import and metadata",
        ]
        sync = offline[1].argv
        assert sync[-6:] == (
            "sync",
            "--frozen",
            "--no-dev",
            "--no-install-project",
            "--python",
            "3.12",
        )
        install = offline[2].argv
        assert install == (
            "uv",
            "pip",
            "install",
            "--python",
            str(driver.venv_python(paths.offline_environment)),
            "--offline",
            str(wheel),
        )
        assert "--ignore=.venv" in initial[3].argv


def test_driver_diagnostic_is_bounded_redacted_and_control_free() -> None:
    driver = load_driver()
    records: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-diagnostic-") as temp_dir:
        temporary_root = Path(temp_dir)
        secret = "synthetic-secret-not-output"
        spec = driver.CommandSpec(
            "synthetic failure",
            (
                sys.executable,
                "-c",
                "import os, sys; "
                "sys.stderr.write('x' * 9000 + os.getcwd() + '\\x1b[31m\\n'); "
                "raise SystemExit(1)",
            ),
            temporary_root,
        )
        env = os.environ.copy()
        env["SYNTHETIC_SECRET"] = secret
        with pytest.raises(driver.CommandFailure, match="synthetic failure:FAILED:1"):
            driver.run_command(
                spec,
                env=env,
                timeout=1,
                records=records,
                repository=ROOT,
                temporary_root=temporary_root,
            )
    record = records[-1]
    diagnostic = record["diagnostic"]
    assert record["label"] == "synthetic failure"
    assert record["result"] == "FAILED"
    assert record["returncode"] == 1
    assert len(diagnostic.encode("utf-8")) <= driver.DIAGNOSTIC_MAX_BYTES
    assert "\x1b" not in diagnostic
    assert str(temporary_root) not in diagnostic
    assert str(ROOT.resolve()) not in diagnostic
    assert secret not in diagnostic
    assert "stdout" not in record or record["stdout"] is None


def test_driver_success_omits_output_and_timeout_differs_from_nonzero() -> None:
    driver = load_driver()
    records: list[dict[str, Any]] = []
    success = driver.CommandSpec(
        "synthetic success", (sys.executable, "-c", "print('success output')"), ROOT
    )
    driver.run_command(success, env=os.environ.copy(), timeout=1, records=records)
    assert records[-1] == {
        "label": "synthetic success",
        "result": "PASSED",
        "timeout_seconds": 1,
    }

    timeout_records: list[dict[str, Any]] = []
    spec = driver.CommandSpec(
        "synthetic timeout", (sys.executable, "-c", "import time; time.sleep(1)"), ROOT
    )
    with pytest.raises(driver.CommandFailure, match="synthetic timeout:TIMEOUT"):
        driver.run_command(spec, env=os.environ.copy(), timeout=0.01, records=timeout_records)
    assert timeout_records[-1]["result"] == "TIMEOUT"
    assert "returncode" not in timeout_records[-1]
    assert "diagnostic" in timeout_records[-1]

    failure_records: list[dict[str, Any]] = []
    spec = driver.CommandSpec(
        "synthetic failure", (sys.executable, "-c", "raise SystemExit(7)"), ROOT
    )
    with pytest.raises(driver.CommandFailure, match="synthetic failure:FAILED:7"):
        driver.run_command(spec, env=os.environ.copy(), timeout=1, records=failure_records)
    assert failure_records[-1]["result"] == "FAILED"
    assert failure_records[-1]["returncode"] == 7
    assert "diagnostic" in failure_records[-1]


def test_driver_synthetic_offline_path_has_no_cache_reconstruction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    driver = load_driver()

    def fake_run(
        spec: Any,
        *,
        env: dict[str, str],
        timeout: float,
        records: list[dict[str, Any]],
        **kwargs: Any,
    ) -> None:
        if spec.label == "sdist and wheel build":
            output = Path(spec.argv[-1])
            output.mkdir(exist_ok=True)
            (output / "llm_slovenian_repair-0.0.0-py3-none-any.whl").touch()
        if spec.label == "offline runtime-only frozen sync":
            driver.record_command(
                records,
                spec.label,
                "FAILED",
                timeout,
                returncode=1,
                diagnostic="offline cache unavailable",
            )
            raise driver.CommandFailure(spec.label, "FAILED", 1)
        records.append({"label": spec.label, "result": "PASSED", "timeout_seconds": timeout})

    monkeypatch.setattr(driver, "run_command", fake_run)
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-driver-test-") as temp_dir:
        repo = Path(temp_dir) / "repo"
        parent = Path(temp_dir) / "native-parent"
        repo.mkdir()
        parent.mkdir()
        (repo / "uv.lock").write_bytes(LOCKFILE.read_bytes())
        result = driver.run_verification(repo, parent, 1)
    assert result["result"] == "FAILED"
    assert result["failure"] == "offline runtime-only frozen sync:FAILED:1"
    assert result["commands"][-1]["label"] == "offline runtime-only frozen sync"
    assert result["cleanup"] == "PASSED"
