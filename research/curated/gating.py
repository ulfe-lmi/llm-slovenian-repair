"""The actual frozen post-review unigram gate and case-boundary mechanics."""

from __future__ import annotations

import sqlite3
import stat
from pathlib import Path
from typing import Callable

from .corpus import CorpusError
from .patching import mechanical
from .review import Proposal


class UnigramIndex:
    """Read-only view of the frozen unigram table; no n-gram fallback exists."""

    def __init__(self, path: str | Path):
        db_path = Path(path)
        info = db_path.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise CorpusError("unigram index must be a regular non-symlink file")
        self.connection = sqlite3.connect(db_path.as_uri() + "?mode=ro&immutable=1", uri=True)
        self.queries = 0

    def lookup(self, word: str) -> dict[str, object]:
        self.queries += 1
        key = word.casefold()
        row = self.connection.execute("SELECT count FROM unigram WHERE word=?", (key,)).fetchone()
        return {"key": key, "state": "EXACT" if row else "UNAVAILABLE", "count": row[0] if row else None}

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> UnigramIndex:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def check(
    text: str,
    candidate: dict[str, object],
    proposal: Proposal,
    lookup: Callable[[str], dict[str, object]],
) -> dict[str, object]:
    """Apply the historical mechanical gate, then require exact unigram words."""
    mechanics = mechanical(text, candidate, proposal)
    if not mechanics["applied"]:
        return {"accepted": False, "mechanical": mechanics, "unigram": None, "reason": mechanics["reason"]}
    assert isinstance(proposal.replacement, str)
    words = [lookup(word) for word in proposal.replacement.casefold().split()]
    passed = all(word["state"] == "EXACT" for word in words)
    return {
        "accepted": passed,
        "mechanical": mechanics,
        "unigram": {"passed": passed, "words": words},
        "reason": "unigram-exact" if passed else "replacement-unigram-uncertain",
    }
