"""Contract checks for the reproducible, side-effect-free package baseline."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import tomllib
from email import message_from_bytes
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = ROOT / "pyproject.toml"
LOCKFILE = ROOT / "uv.lock"


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
