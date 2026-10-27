"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Runtime corpus."""

from __future__ import annotations

import contextlib
import os
import sqlite3
import stat
from pathlib import Path
from urllib.parse import quote

from config import RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS

from corpus import Corpus, Evidence

# Fixed content-free failure labels (order 016-a, requirement 4).  They
# reflect no SQL text, path, value, target or credential; ``detail``
# carries at most the Python exception class name of the underlying
# sqlite3 error, never its message.
REASON_UNAVAILABLE = "RUNTIME_EVIDENCE_UNAVAILABLE"
REASON_CORRUPT = "RUNTIME_EVIDENCE_CORRUPT"
REASON_INCOMPATIBLE = "RUNTIME_EVIDENCE_INCOMPATIBLE"
REASON_INVALID_COUNT = "RUNTIME_EVIDENCE_INVALID_COUNT"
REASON_LOCKED = "RUNTIME_EVIDENCE_LOCKED"
REASON_UNSUPPORTED_JOURNAL = "RUNTIME_EVIDENCE_UNSUPPORTED_JOURNAL"

# SQLite official file format (bounded read-only header preflight):
# 16-byte magic, then bytes 18/19 are the file write/read version where
# 1 = rollback journal and 2 = WAL.  The supported prepared index uses
# the rollback (DELETE) journal; a WAL database is rejected BEFORE any
# SQLite open because even read-only SQLite access to it creates
# persistent -wal/-shm auxiliary files.
_SQLITE_HEADER_MAGIC = b"SQLite format 3\x00"
_JOURNAL_ROLLBACK = 1
_JOURNAL_WAL = 2


def _preflight_header(path: Path) -> None:
    """Fail closed on unusable, non-database or WAL-journal indexes.

    The exact configured file is opened read-only and NON-BLOCKING and
    its type is checked with ``fstat`` before any byte is read: a
    non-regular resource (an anonymous pipe or FIFO reachable through
    ``/proc/self/fd``, a device node, a socket) is rejected without
    waiting for a peer that may never write, while ordinary regular
    files - including symlink and hardlink paths that open as regular
    files - continue.  The bounded 100-byte header read then creates
    nothing: a short file or a non-SQLite magic is corrupt; write/read
    version byte 2 (WAL) is an unsupported journal mode for the
    read-only runtime (it would persist -wal/-shm auxiliary files); any
    other version byte is corrupt.  No conversion, sidecar cleanup or
    ``immutable``/no-lock assumption is made.
    """
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        raise RuntimeCorpusError(REASON_UNAVAILABLE) from None
    try:
        try:
            info = os.fstat(descriptor)
        except OSError:
            raise RuntimeCorpusError(REASON_UNAVAILABLE) from None
        if not stat.S_ISREG(info.st_mode):
            raise RuntimeCorpusError(REASON_UNAVAILABLE)
        try:
            header = os.read(descriptor, 100)
        except OSError:
            raise RuntimeCorpusError(REASON_UNAVAILABLE) from None
    finally:
        with contextlib.suppress(OSError):
            os.close(descriptor)
    if len(header) < 100 or header[:16] != _SQLITE_HEADER_MAGIC:
        raise RuntimeCorpusError(REASON_CORRUPT)
    if header[18] != _JOURNAL_ROLLBACK or header[19] != _JOURNAL_ROLLBACK:
        if header[18] == _JOURNAL_WAL or header[19] == _JOURNAL_WAL:
            raise RuntimeCorpusError(REASON_UNSUPPORTED_JOURNAL)
        raise RuntimeCorpusError(REASON_CORRUPT)

# The exact tables and columns the runtime queries access.  An index
# missing an accessed table or column is an incompatible accessed schema
# before any data read; no version metadata is invented from the index.
_ACCESSED_TABLES = {
    "unigram": ("word", "count"),
    "bigram": ("phrase", "count"),
    "trigram": ("phrase", "count"),
    "middle": ("left_word", "right_word", "middle_word", "count"),
}


class RuntimeCorpusError(ValueError):
    """One finite technical evidence failure with a fixed content-free label."""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(reason)
        self.reason = reason
        self.detail = detail


def _classify(exc: sqlite3.Error) -> RuntimeCorpusError:
    message = exc.args[0] if exc.args and isinstance(exc.args[0], str) else ""
    detail = type(exc).__name__
    if "file is not a database" in message:
        return RuntimeCorpusError(REASON_CORRUPT, detail)
    if "database is locked" in message:
        return RuntimeCorpusError(REASON_LOCKED, detail)
    if "no such table" in message or "no such column" in message:
        return RuntimeCorpusError(REASON_INCOMPATIBLE, detail)
    return RuntimeCorpusError(REASON_UNAVAILABLE, detail)


def _validated_count(value: object) -> int:
    """Exact nonnegative Python integer only (order 016-a, requirement 3).

    The returned value must be a nonnegative Python ``int``
    (type-strict): text, NULL, negative, fractional or any other
    non-integer value is a technical evidence failure, with no
    ``int()`` repair or truncation and no invented zero.  A bound
    boolean is stored by SQLite as integer 1, so no boolean origin
    is detected.  A valid zero stays EXACT(0) and a missing row
    stays UNAVAILABLE/CENSORED (count scope preserved).
    """
    if type(value) is not int or value < 0:
        raise RuntimeCorpusError(REASON_INVALID_COUNT)
    return value


class RuntimeCorpus(Corpus):
    """Read-only runtime evidence adapter over the existing SQLite index.

    Inherits the nominal ``Corpus`` interface (so the frozen detector and
    acceptance code type-check unchanged) while overriding the constructor
    and every runtime data-access method with the strict read-only,
    exact-count-validation behavior ordered for the runnable proxy; the
    frozen ``corpus.py`` module itself is byte-identical.

    The index is opened as ``file:<uri>?mode=ro`` from the configured path
    made absolute and percent-escaped (Unicode, spaces, ``#`` and ``?``
    included), so the exact configured path spelling is the only path
    used: a relative path keeps its previous semantics (resolved against
    the process working directory for the URI only), with no
    Python-level path resolution and no alternate-file search; ordinary
    regular-file symlink and hardlink spellings are followed by the OS
    open and remain supported.  No ``immutable=1`` assumption is made,
    and no file creation, normalization or write of any kind.  The
    finite busy wait
    (``config.RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS``, 0.25 s) bounds lock
    waiting per query; it is not a total CPU/query deadline.  Handles are
    closed on success and on construction or context failure (order 016-a,
    requirement 2).
    """

    def __init__(self, path: str | Path) -> None:
        # The configured path spelling keeps its previous semantics:
        # absolute or relative (the working directory is prefixed for
        # relative paths), with no Python-level path resolution and no
        # alternate-file search; ordinary regular-file symlink and
        # hardlink spellings are followed by the OS open and remain
        # supported.  The escaped URI always names a real absolute
        # file.  An embedded NUL is rejected before URI encoding:
        # decoded back by SQLite and truncated by the platform path
        # handling, it would silently name another (shorter) file
        # instead of the exact configured path.
        configured = Path(path).absolute().as_posix()
        if "\x00" in configured:
            raise RuntimeCorpusError(REASON_UNAVAILABLE)
        _preflight_header(Path(configured))
        uri = "file://" + quote(configured, safe="/") + "?mode=ro"
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(
                uri, uri=True, timeout=RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS
            )
            self._validate_accessed_schema(connection)
        except RuntimeCorpusError:
            if connection is not None:
                with contextlib.suppress(sqlite3.Error):
                    connection.close()
            raise
        except sqlite3.Error as exc:
            if connection is not None:
                with contextlib.suppress(sqlite3.Error):
                    connection.close()
            raise _classify(exc) from None
        self.connection = connection

    @staticmethod
    def _validate_accessed_schema(connection: sqlite3.Connection) -> None:
        """Detect accessed incompatible schema without any full-index scan."""
        try:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            for table, columns in _ACCESSED_TABLES.items():
                if table not in tables:
                    raise RuntimeCorpusError(REASON_INCOMPATIBLE)
                info = connection.execute(f"PRAGMA table_info({table})").fetchall()
                present = {row[1] for row in info}
                if not set(columns) <= present:
                    raise RuntimeCorpusError(REASON_INCOMPATIBLE)
        except RuntimeCorpusError:
            raise
        except sqlite3.Error as exc:
            raise _classify(exc) from None

    def close(self) -> None:
        with contextlib.suppress(sqlite3.Error):
            self.connection.close()

    def __enter__(self) -> RuntimeCorpus:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def unigram(self, word: str) -> Evidence:
        key = word.casefold()
        try:
            row = self.connection.execute(
                "SELECT count FROM unigram WHERE word=?", (key,)
            ).fetchone()
        except sqlite3.Error as exc:
            raise _classify(exc) from None
        if row is None:
            return Evidence("UNAVAILABLE", None, key)
        return Evidence("EXACT", _validated_count(row[0]), key)

    def ngram(self, phrase: str, length: int) -> Evidence:
        if length not in (2, 3):
            raise ValueError("only bigrams and trigrams are supported")
        table = "bigram" if length == 2 else "trigram"
        key = " ".join(part.casefold() for part in phrase.split())
        try:
            row = self.connection.execute(
                f"SELECT count FROM {table} WHERE phrase=?", (key,)
            ).fetchone()
        except sqlite3.Error as exc:
            raise _classify(exc) from None
        if row is None:
            return Evidence("CENSORED", None, key)
        return Evidence("EXACT", _validated_count(row[0]), key)

    def alternatives(self, left: str, right: str) -> list[tuple[str, int]]:
        try:
            rows = self.connection.execute(
                "SELECT middle_word,count FROM middle WHERE left_word=? AND "
                "right_word=? ORDER BY count DESC,middle_word",
                (left.casefold(), right.casefold()),
            ).fetchall()
        except sqlite3.Error as exc:
            raise _classify(exc) from None
        return [(str(row[0]), _validated_count(row[1])) for row in rows]
