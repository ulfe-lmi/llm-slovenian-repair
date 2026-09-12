"""Contract checks for the reproducible, side-effect-free package baseline."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import sysconfig
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
EXPECTED_EXPORTS = [
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
]


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


def child_environment(home: Path, *, source_tree: bool = False) -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["HOME"] = str(home)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    if source_tree:
        env["PYTHONPATH"] = str(ROOT / "src")
    return env


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
    code = f"""
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

before_modules = set(sys.modules)
module = __import__("llm_slovenian_repair")
after_modules = set(sys.modules)
assert importlib.metadata.version("llm-slovenian-repair") == "0.0.0"
assert module.__version__ == "0.0.0"
assert module.__all__ == {EXPECTED_EXPORTS!r}
assert set(module.__all__).issubset(dir(module))
assert not any(
    name == "pydantic"
    or name.startswith(("pydantic.", "pydantic_core", "httpx"))
    for name in after_modules - before_modules
)
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


def test_source_root_import_succeeds_without_runtime_dependencies() -> None:
    code = r"""
import builtins
import pathlib
import sys

blocked = ("pydantic", "pydantic_core", "httpx")
original_import = builtins.__import__

def guarded_import(name, *args, **kwargs):
    if any(name == dependency or name.startswith(dependency + ".") for dependency in blocked):
        raise ModuleNotFoundError(f"blocked dependency: {name}")
    return original_import(name, *args, **kwargs)

builtins.__import__ = guarded_import
root = pathlib.Path.cwd()
before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
module = __import__("llm_slovenian_repair")
assert module.__version__ == "0.0.0"
assert module.__all__[0] == "__version__"
assert set(module.__all__).issubset(dir(module))
assert not any(
    name == "pydantic"
    or name.startswith(("pydantic.", "pydantic_core", "httpx"))
    for name in sys.modules
)
after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
assert before == after
"""
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-source-import-") as temp_dir:
        temp = Path(temp_dir)
        completed = subprocess.run(
            [sys.executable, "-B", "-c", code],
            cwd=temp,
            env=child_environment(temp / "home", source_tree=True),
            capture_output=True,
            text=True,
            check=False,
        )
    assert completed.returncode == 0, completed.stderr or completed.stdout


def test_source_lazy_export_loads_dependencies_only_on_first_typed_access() -> None:
    code = r"""
import importlib
import pathlib
import sys

module = __import__("llm_slovenian_repair")
before = set(sys.modules)
directory = dir(module)
try:
    module.not_a_documented_export
except AttributeError:
    pass
else:
    raise AssertionError("unknown exports must raise AttributeError")
assert dir(module) == directory
assert "llm_slovenian_repair.contracts" not in sys.modules
assert "llm_slovenian_repair.policy" not in sys.modules
assert "pydantic" not in sys.modules
assert "httpx" not in sys.modules

policy_config = module.PolicyConfig
assert policy_config is importlib.import_module(
    "llm_slovenian_repair.policy"
).PolicyConfig
assert module.PolicyConfig is policy_config
assert "pydantic" in sys.modules
assert "httpx" not in sys.modules
assert "llm_slovenian_repair.source_manifest" not in sys.modules
assert dir(module) == directory
assert pathlib.Path.cwd().is_dir()
"""
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-source-lazy-") as temp_dir:
        temp = Path(temp_dir)
        completed = subprocess.run(
            [sys.executable, "-B", "-c", code],
            cwd=temp,
            env=child_environment(temp / "home", source_tree=True),
            capture_output=True,
            text=True,
            check=False,
        )
    assert completed.returncode == 0, completed.stderr or completed.stdout


def test_built_wheel_metadata_and_payload() -> None:
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-wheel-") as temp_dir:
        temp = Path(temp_dir)
        output_dir = temp / "artifacts"
        output_dir.mkdir()
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
                or name.endswith(
                    (
                        "__init__.py",
                        "contracts.py",
                        "policy.py",
                        "source_manifest.py",
                        "unigram_importer.py",
                        "py.typed",
                    )
                )
                for name in names
            )
            assert not any(
                token in name.lower()
                for name in names
                for token in ("model", "corpus", "weights")
            )

        wheel_environment = temp / "wheel-environment"
        completed = subprocess.run(
            ["uv", "venv", "--python", sys.executable, str(wheel_environment)],
            cwd=temp,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout
        wheel_python = wheel_environment / (
            "Scripts/python.exe" if os.name == "nt" else "bin/python"
        )
        completed = subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--python",
                str(wheel_python),
                "--offline",
                "--no-deps",
                str(wheels[0]),
            ],
            cwd=temp,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout

        outside_repository = temp / "outside-repository"
        outside_repository.mkdir()
        bare_import = f"""
import importlib.metadata as metadata
import pathlib
import sys

root = pathlib.Path.cwd()
before_files = sorted(path.relative_to(root).as_posix() for path in root.rglob('*'))
before_modules = set(sys.modules)
module = __import__('llm_slovenian_repair')
after_modules = set(sys.modules)
assert metadata.version('llm-slovenian-repair') == '0.0.0'
assert module.__version__ == '0.0.0'
assert module.__all__ == {EXPECTED_EXPORTS!r}
assert set(module.__all__).issubset(dir(module))
assert not any(
    name == 'pydantic'
    or name.startswith(('pydantic.', 'pydantic_core', 'httpx'))
    for name in after_modules - before_modules
)
after_files = sorted(path.relative_to(root).as_posix() for path in root.rglob('*'))
assert before_files == after_files
"""
        completed = subprocess.run(
            [str(wheel_python), "-B", "-c", bare_import],
            cwd=outside_repository,
            env=child_environment(temp / "home"),
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout

        lazy_access = r"""
import importlib
import sys

module = __import__("llm_slovenian_repair")
assert "pydantic" not in sys.modules
assert "httpx" not in sys.modules
policy_config = module.PolicyConfig
assert policy_config is importlib.import_module(
    "llm_slovenian_repair.policy"
).PolicyConfig
assert "pydantic" in sys.modules
assert "httpx" not in sys.modules
"""
        dependency_environment = child_environment(temp / "home")
        dependency_environment["PYTHONPATH"] = sysconfig.get_path("purelib") or ""
        completed = subprocess.run(
            [str(wheel_python), "-B", "-c", lazy_access],
            cwd=outside_repository,
            env=dependency_environment,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout


def test_driver_environment_uses_owned_native_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    driver = load_driver()
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-driver-test-") as temp_dir:
        paths = driver.workspace_paths(Path(temp_dir))
        paths.child_tmp.mkdir(mode=0o700)
        monkeypatch.setenv("PYTHONPATH", "synthetic-private-value")
        monkeypatch.setenv("TMPDIR", "/tmp/unsafe-inherited-value")
        monkeypatch.setenv("RUNNER_TEMP", "/runner-owned-temp")
        env = driver.build_environment(paths)
        assert env["UV_PROJECT_ENVIRONMENT"] == str(paths.project_environment)
        assert env["UV_CACHE_DIR"] == str(paths.cache)
        assert env["UV_LINK_MODE"] == "copy"
        assert env["UV_PYTHON"] == "3.12"
        assert "PYTHONPATH" not in env
        assert env["RUFF_CACHE_DIR"] == str(paths.ruff_cache)
        assert env["MYPY_CACHE_DIR"] == str(paths.mypy_cache)
        assert env["TMPDIR"] == str(paths.child_tmp)
        assert Path(env["TMPDIR"]).resolve().parent == paths.root.resolve()
        assert env["TMPDIR"] != "/tmp/unsafe-inherited-value"
        assert env["TMPDIR"] != "/runner-owned-temp"


def test_github_runner_temp_runs_a_copied_research_fixture_with_owned_tmpdir(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    driver = load_driver()
    with tempfile.TemporaryDirectory(prefix="llm-slovenian-runner-temp-") as temp_dir:
        runner_temp = Path(temp_dir) / "runner-temp"
        runner_temp.mkdir()
        root = runner_temp / "driver-root"
        root.mkdir()
        paths = driver.workspace_paths(root)
        paths.child_tmp.mkdir(mode=0o700)
        test_repo = driver.prepare_test_workspace(ROOT, paths)
        monkeypatch.delenv("TMPDIR", raising=False)
        monkeypatch.setenv("RUNNER_TEMP", str(runner_temp))
        env = driver.build_environment(paths)
        records: list[dict[str, Any]] = []
        driver.run_command(
            driver.CommandSpec(
                "copied research fixture",
                (
                    sys.executable,
                    "-m",
                    "pytest",
                    "-p",
                    "no:cacheprovider",
                    "research/tests/test_strategic_replay_fidelity.py::StrategicReplayFidelity::test_english_preservation_has_zero_review_and_retry_calls",
                    "-q",
                ),
                test_repo,
            ),
            env=env,
            timeout=30,
            records=records,
            repository=ROOT,
            temporary_root=root,
        )
        assert records[-1]["result"] == "PASSED"
        assert Path(env["TMPDIR"]).resolve().is_relative_to(root.resolve())
        assert Path(env["TMPDIR"]).resolve().is_dir()


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
