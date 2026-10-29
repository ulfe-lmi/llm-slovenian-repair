"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Runtime corpus."""

from __future__ import annotations

import contextlib
import os
import sqlite3
import stat
from pathlib import Path
from typing import NoReturn
from urllib.parse import quote

from config import RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS
from evidence_budget import (
    EVIDENCE_FETCH_CHUNK_ROWS,
    EvidenceBudgetState,
    EvidenceLimits,
    make_progress_handler,
)

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
# Bound-evidence failures (order 024-a, requirement 3): only the
# adapter's own sticky exhaustion maps EXCEEDED; an invalid startup
# policy is INVALID.  Both stay fixed content-free labels; any other
# SQLite error or interrupt keeps the older fixed labels/causes.
REASON_BUDGET_EXCEEDED = "RUNTIME_EVIDENCE_BUDGET_EXCEEDED"
REASON_BUDGET_INVALID = "RUNTIME_EVIDENCE_BUDGET_INVALID"

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


def _is_caller_control(exc: BaseException | None) -> bool:
    """Whether ``exc`` is caller control that must keep its exact identity.

    Nonordinary BaseExceptions (KeyboardInterrupt, SystemExit, and any
    other non-Exception BaseException) are caller control, as is
    MemoryError explicitly although it subclasses Exception (order
    024-a, requirement 6); ordinary Exceptions are not.
    """
    if exc is None:
        return False
    if not isinstance(exc, Exception):
        return True
    return isinstance(exc, MemoryError)


def _close_cursor(cursor: sqlite3.Cursor, in_flight: BaseException | None) -> None:
    """Close an owned cursor without replacing the current operation's
    propagating caller control.

    ``in_flight`` is the current owned operation's own exception,
    explicitly tracked through that operation's exception/cleanup
    path: ambient exception context from another (already handled)
    frame is never used as authority.  While a caller control is
    propagating from the current operation, a later close failure
    (ordinary, or a later distinct control) may not replace its exact
    identity.  sqlite3.Error close failures stay suppressed as
    before; any other close failure propagates unchanged, including a
    new control on a clean flow (order 024-a, requirement 6).
    """
    try:
        cursor.close()
    except BaseException as exc:
        if isinstance(exc, sqlite3.Error) or _is_caller_control(in_flight):
            return
        raise


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

    def __init__(
        self,
        path: str | Path,
        *,
        max_statements: int | None = None,
        max_rows_per_query: int | None = None,
        max_rows_total: int | None = None,
        progress_interval: int | None = None,
        max_progress_callbacks: int | None = None,
    ) -> None:
        # Optional trusted keyword-only limits (order 024-a,
        # requirement 2): None always resolves to the current finite
        # config defaults, never to disabled or unbounded.  The
        # complete policy is resolved and validated BEFORE the exact
        # file is touched, so an invalid policy is a fixed budget
        # failure, not an I/O failure, and opens nothing.
        try:
            limits = EvidenceLimits.from_values(
                max_statements=max_statements,
                max_rows_per_query=max_rows_per_query,
                max_rows_total=max_rows_total,
                progress_interval=progress_interval,
                max_progress_callbacks=max_progress_callbacks,
            )
        except ValueError:
            raise RuntimeCorpusError(REASON_BUDGET_INVALID) from None
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
        self._budget = EvidenceBudgetState(limits)
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(
                uri, uri=True, timeout=RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS
            )
            # The real native progress handler is attached immediately
            # after connect, BEFORE any claimed budgeted SQL (order
            # 024-a, requirement 3); one cumulative callback counter
            # per connection/answer, never reset per query.
            connection.set_progress_handler(
                make_progress_handler(self._budget),
                limits.progress_interval,
            )
            self._validate_accessed_schema(connection)
        except RuntimeCorpusError as exc:
            self._teardown(connection, pending=exc)
            raise
        except sqlite3.Error as exc:
            self._teardown(connection, pending=exc)
            raise _classify(exc) from None
        except BaseException as exc:
            # A preserved caller-control identity (or any other
            # nonordinary control) re-raises AFTER owned cleanup;
            # nothing is swallowed, and a cleanup failure may never
            # replace the caller's own exception (order 024-a,
            # requirement 6).
            self._teardown(connection, pending=exc)
            raise
        self.connection = connection

    def _validate_accessed_schema(self, connection: sqlite3.Connection) -> None:
        """Detect accessed incompatible schema without any full-index scan.

        Every statement is charged to the connection budget like data
        work and fetched through the same bounded rows path, so schema
        probing cannot materialize unbounded metadata (order 024-a,
        requirements 3 and 4); metadata rows count as actual rows.
        """
        cursor: sqlite3.Cursor | None = None
        pending: BaseException | None = None
        mapped: BaseException | None = None
        try:
            cursor = self._execute(
                connection, "SELECT name FROM sqlite_master WHERE type='table'"
            )
            names = self._fetch_all_bounded(cursor)
            _close_cursor(cursor, None)
            cursor = None
            tables = {row[0] for row in names}
            for table, columns in _ACCESSED_TABLES.items():
                if table not in tables:
                    raise RuntimeCorpusError(REASON_INCOMPATIBLE)
                cursor = self._execute(connection, f"PRAGMA table_info({table})")
                info = self._fetch_all_bounded(cursor)
                _close_cursor(cursor, None)
                cursor = None
                present = {row[1] for row in info}
                if not set(columns) <= present:
                    raise RuntimeCorpusError(REASON_INCOMPATIBLE)
        except RuntimeCorpusError as exc:
            pending = exc
            raise
        except sqlite3.Error as exc:
            try:
                self._raise_budget_aware(exc)
            except BaseException as mapped_exc:
                mapped = mapped_exc
                raise
        except BaseException as exc:
            pending = exc
            raise
        finally:
            if cursor is not None:
                _close_cursor(
                    cursor, pending if pending is not None else mapped
                )

    def _teardown(
        self,
        connection: sqlite3.Connection | None,
        pending: BaseException | None = None,
    ) -> None:
        """Remove the callback and close the owned connection, if any.

        A callback-removal failure never skips the close attempt.
        Exception priority (order 024-a, requirement 6): the FIRST
        caller control keeps its exact identity over later cleanup
        failures (including a later distinct control): a caller
        control in ``pending`` is preserved by the caller, and when
        ``pending`` is ordinary or absent, a caller control raised
        during removal or close propagates instead of the ordinary
        error (an ordinary pending must not swallow a later caller
        control).  With no caller control at all, ordinary/fixed-label
        behavior is kept: a pending ordinary exception is not replaced
        by ordinary cleanup failures, and a normal close propagates
        its first non-sqlite removal or close failure after the close
        attempt.  sqlite3.Error teardown failures stay suppressed as
        before.
        """
        if connection is None:
            return
        removal_error: BaseException | None = None
        try:
            connection.set_progress_handler(None, 0)
        except BaseException as exc:
            if not isinstance(exc, sqlite3.Error):
                removal_error = exc
        close_error: BaseException | None = None
        try:
            connection.close()
        except BaseException as exc:
            if not isinstance(exc, sqlite3.Error):
                close_error = exc
        if _is_caller_control(pending):
            return
        for error in (removal_error, close_error):
            if error is not None and _is_caller_control(error):
                raise error
        if pending is not None:
            return
        if removal_error is not None:
            raise removal_error
        if close_error is not None:
            raise close_error

    def close(self) -> None:
        self._teardown(self.connection)

    def __enter__(self) -> RuntimeCorpus:
        return self

    def __exit__(self, *args: object) -> None:
        # Base-compatible variadic signature (the frozen Corpus declares
        # ``*_``); the context machinery passes (type, exception,
        # traceback), so the pending exception is recovered at position 1.
        # While the body's own exception is propagating, teardown failures
        # may not replace it (exact identity preserved); a clean body keeps
        # the normal close exception semantics (order 024-a, requirement 6).
        pending: BaseException | None = None
        if len(args) >= 2 and isinstance(args[1], BaseException):
            pending = args[1]
        self._teardown(self.connection, pending=pending)

    def unigram(self, word: str) -> Evidence:
        key = word.casefold()
        cursor: sqlite3.Cursor | None = None
        pending: BaseException | None = None
        mapped: BaseException | None = None
        try:
            cursor = self._execute(
                self.connection, "SELECT count FROM unigram WHERE word=?", (key,)
            )
            rows = self._fetch_all_bounded(cursor)
        except sqlite3.Error as exc:
            try:
                self._raise_budget_aware(exc)
            except BaseException as mapped_exc:
                mapped = mapped_exc
                raise
        except BaseException as exc:
            pending = exc
            raise
        finally:
            if cursor is not None:
                _close_cursor(
                    cursor, pending if pending is not None else mapped
                )
        if not rows:
            return Evidence("UNAVAILABLE", None, key)
        return Evidence("EXACT", _validated_count(rows[0][0]), key)

    def ngram(self, phrase: str, length: int) -> Evidence:
        if length not in (2, 3):
            raise ValueError("only bigrams and trigrams are supported")
        table = "bigram" if length == 2 else "trigram"
        key = " ".join(part.casefold() for part in phrase.split())
        cursor: sqlite3.Cursor | None = None
        pending: BaseException | None = None
        mapped: BaseException | None = None
        try:
            cursor = self._execute(
                self.connection,
                f"SELECT count FROM {table} WHERE phrase=?",
                (key,),
            )
            rows = self._fetch_all_bounded(cursor)
        except sqlite3.Error as exc:
            try:
                self._raise_budget_aware(exc)
            except BaseException as mapped_exc:
                mapped = mapped_exc
                raise
        except BaseException as exc:
            pending = exc
            raise
        finally:
            if cursor is not None:
                _close_cursor(
                    cursor, pending if pending is not None else mapped
                )
        if not rows:
            return Evidence("CENSORED", None, key)
        return Evidence("EXACT", _validated_count(rows[0][0]), key)

    def _execute(
        self,
        connection: sqlite3.Connection,
        sql: str,
        params: tuple[object, ...] = (),
    ) -> sqlite3.Cursor:
        """Charge one SQL start, then execute it on the owned connection.

        Every statement start is counted BEFORE execute/prepare,
        including schema work and late acceptance; at most
        ``max_statements`` actual starts, the next is denied before
        execute and leaves no partial state (order 024-a,
        requirement 3).  Counts starts, not exact opcode totals or
        time.
        """
        state = self._budget
        if state.exhausted:
            raise RuntimeCorpusError(REASON_BUDGET_EXCEEDED)
        if state.statements >= state.limits.max_statements:
            state.exhausted = True
            raise RuntimeCorpusError(REASON_BUDGET_EXCEEDED)
        state.statements += 1
        return connection.execute(sql, params)

    def _fetch_all_bounded(self, cursor: sqlite3.Cursor) -> list[tuple[object, ...]]:
        """Fetch a complete result set only within both row quotas.

        At most one row beyond ``min(per-query cap, remaining total)``
        may be fetched, solely to detect overflow; an overflowing
        result is discarded WHOLE, never truncated and presented as
        complete.  Actual rows (metadata included) count, exact-quota
        EOF and empty results work, and no query resets the cumulative
        quota or exhaustion (order 024-a, requirement 4).
        """
        state = self._budget
        limits = state.limits
        allowed = min(
            limits.max_rows_per_query, max(limits.max_rows_total - state.rows_total, 0)
        )
        probe = allowed + 1
        rows: list[tuple[object, ...]] = []
        while len(rows) < probe:
            chunk = cursor.fetchmany(min(EVIDENCE_FETCH_CHUNK_ROWS, probe - len(rows)))
            if not chunk:
                break
            rows.extend(chunk)
        if len(rows) > allowed:
            state.rows_total += len(rows)
            state.exhausted = True
            raise RuntimeCorpusError(REASON_BUDGET_EXCEEDED)
        state.rows_total += len(rows)
        return rows

    def _raise_budget_aware(self, exc: sqlite3.Error) -> NoReturn:
        """Translate a sqlite3 error with budget awareness.

        A preserved caller-control exception re-raises its EXACT
        original identity from Python after owned cleanup, never
        mislabeled as a quota failure; only this adapter's own sticky
        exhaustion maps BUDGET_EXCEEDED; every other SQLite error
        keeps the old fixed labels and causes (order 024-a,
        requirement 3).
        """
        state = self._budget
        control = state.pending_control
        if control is not None:
            state.pending_control = None
            raise control
        if state.exhausted:
            raise RuntimeCorpusError(REASON_BUDGET_EXCEEDED) from None
        raise _classify(exc) from None

    def alternatives(self, left: str, right: str) -> list[tuple[str, int]]:
        cursor: sqlite3.Cursor | None = None
        pending: BaseException | None = None
        mapped: BaseException | None = None
        try:
            cursor = self._execute(
                self.connection,
                "SELECT middle_word,count FROM middle WHERE left_word=? AND "
                "right_word=? ORDER BY count DESC,middle_word",
                (left.casefold(), right.casefold()),
            )
            rows = self._fetch_all_bounded(cursor)
        except sqlite3.Error as exc:
            try:
                self._raise_budget_aware(exc)
            except BaseException as mapped_exc:
                mapped = mapped_exc
                raise
        except BaseException as exc:
            pending = exc
            raise
        finally:
            if cursor is not None:
                _close_cursor(
                    cursor, pending if pending is not None else mapped
                )
        return [(str(row[0]), _validated_count(row[1])) for row in rows]
