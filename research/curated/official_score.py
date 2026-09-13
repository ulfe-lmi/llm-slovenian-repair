"""Pinned official-scoring command records; execution remains an explicit private recipe."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path


def command_record(tool: str, args: Sequence[str], *, version: str, data_root: str | Path) -> dict[str, object]:
    """Describe a scorer invocation without running a tool or reading dataset rows."""
    if not tool or any(not isinstance(arg, str) or "\x00" in arg for arg in args):
        raise ValueError("invalid scorer command")
    root = Path(data_root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("scorer data root must be an explicit real directory")
    return {
        "tool": tool,
        "args": list(args),
        "version": version,
        "data_root_supplied": True,
        "executed": False,
        "network_calls": 0,
        "model_calls": 0,
    }
