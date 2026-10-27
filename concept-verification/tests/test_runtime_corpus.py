"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Runtime corpus.

Order 016-a acceptance coverage for read-only runtime evidence access and
completed-original fallback:

* real-SQLite boundaries of the RuntimeCorpus adapter (read-only open,
  escaped absolute/relative paths, exact nonnegative-integer count
  validation across every query method, valid-zero/missing scopes,
  inaccessible and incompatible indexes, non-regular resource rejection
  without blocking, regular-file symlink/hardlink paths, WAL-journal
  rejection before any SQLite open without auxiliary-file creation,
  finite busy-wait degradation, handle cleanup on success and failure),
  and
* actual proxy HTTP (real ConceptProxy -> real RepairEngine with the
  qualified Pandoc and a real tiny SQLite index -> real ResponsesReviewer)
  technical-failure and fallback cases: healthy useful repair, early
  failures (missing path, corrupt bytes, incompatible schema, text/NULL/
  negative/fractional counts, lock contention) returning the exact
  completed original with zero review calls, the two-proposal late
  replacement-only failure aborting the whole optional pass from the
  immutable original while preserving the actual review call and known or
  unknown usage (including the persisted trace disposition), ordinary
  missing replacement evidence remaining an individual rejection, and
  recovery of the same proxy on the next healthy request.

Only the main upstream and the reviewer HTTP endpoint are synthetic.
"""

from __future__ import annotations

import hashlib
import http.client
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Sequence
from http.server import HTTPServer
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
import proxy  # noqa: E402
from config import RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS  # noqa: E402
from qwen_client import ResponsesReviewer  # noqa: E402
from runtime_corpus import (  # noqa: E402
    REASON_CORRUPT,
    REASON_INCOMPATIBLE,
    REASON_INVALID_COUNT,
    REASON_LOCKED,
    REASON_UNAVAILABLE,
    REASON_UNSUPPORTED_JOURNAL,
    RuntimeCorpus,
    RuntimeCorpusError,
)
from tests.test_responses_contract import (  # noqa: E402
    _ABSENT,
    _json_completed,
    _MainUpstream,
    _review_payload,
)
from tests.test_review_batch import (  # noqa: E402
    TEXT,
    _contract_body,
    _FakeUpstream,
    _prop,
    _real_spec,
    _tc_baseline,
)

HEALTHY_UNIGRAM = [
    ("to", 100),
    ("je", 100),
    ("tako", 100),
    ("presenetljiv", 50),
    ("zapisano", 50),
]
HEALTHY_BIGRAM = [
    ("je tako", 20),
    ("tako zapisano", 20),
    ("je presenetljiv", 20),
    ("je zapisano", 20),
]
HEALTHY_TRIGRAM = [("to je tako", 20), ("je tako zapisano", 20)]
HEALTHY_MIDDLE = [("je", "zapisano", "tako", 20)]


def _build_db(
    path: Path,
    unigram: Sequence[tuple[str, object]] = HEALTHY_UNIGRAM,
    bigram: Sequence[tuple[str, object]] = HEALTHY_BIGRAM,
    trigram: Sequence[tuple[str, object]] = HEALTHY_TRIGRAM,
    middle: Sequence[tuple[str, str, str, object]] = HEALTHY_MIDDLE,
    tables: set[str] | None = None,
    count_columns: dict[str, str] | None = None,
) -> None:
    # ``count_columns`` overrides the stored count column type (default
    # ``INTEGER NOT NULL``) so a technically invalid storage shape - a
    # TEXT-typed or nullable column, where SQLite affinity would not
    # coerce the value - can be exercised without schema drift.
    count_columns = count_columns or {}

    def _count() -> str:
        return count_columns.get("count", "count INTEGER NOT NULL")

    tables = (
        tables
        if tables is not None
        else {"unigram", "bigram", "trigram", "middle"}
    )
    connection = sqlite3.connect(path)
    if "unigram" in tables:
        connection.execute(
            f"CREATE TABLE unigram (word TEXT PRIMARY KEY, {_count()})"
        )
    if "bigram" in tables:
        connection.execute(
            f"CREATE TABLE bigram (phrase TEXT PRIMARY KEY, {_count()})"
        )
    if "trigram" in tables:
        connection.execute(
            f"CREATE TABLE trigram (phrase TEXT PRIMARY KEY, {_count()})"
        )
    if "middle" in tables:
        connection.execute(
            "CREATE TABLE middle (left_word TEXT, right_word TEXT, "
            f"middle_word TEXT, {_count()}, "
            "PRIMARY KEY(left_word,right_word,middle_word))"
        )
    for word, count in unigram:
        if "unigram" in tables:
            connection.execute("INSERT INTO unigram VALUES(?,?)", (word, count))
    for phrase, count in bigram:
        if "bigram" in tables:
            connection.execute("INSERT INTO bigram VALUES(?,?)", (phrase, count))
    for phrase, count in trigram:
        if "trigram" in tables:
            connection.execute("INSERT INTO trigram VALUES(?,?)", (phrase, count))
    for left_word, right_word, middle_word, count in middle:
        if "middle" in tables:
            connection.execute(
                "INSERT INTO middle VALUES(?,?,?,?)",
                (left_word, right_word, middle_word, count),
            )
    connection.commit()
    connection.close()


class RuntimeCorpusDirectTests(unittest.TestCase):
    """Real-SQLite boundaries of the read-only runtime adapter (no proxy)."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = self.root / "tiny.sqlite"
        _build_db(self.db)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_escaped_special_path_absolute_and_relative(self) -> None:
        special_dir = self.root / "ev idx #? \u017d\u0161"
        special_dir.mkdir()
        special = special_dir / "ev#1?x \u017d\u0161.sqlite"
        _build_db(special)
        with RuntimeCorpus(special) as corpus:
            self.assertEqual(corpus.unigram("je").state, "EXACT")
            self.assertEqual(corpus.ngram("je tako", 2).state, "EXACT")
        old_cwd = os.getcwd()
        try:
            os.chdir(special_dir)
            with RuntimeCorpus("ev#1?x \u017d\u0161.sqlite") as corpus:
                self.assertEqual(corpus.unigram("je").count, 100)
                self.assertEqual(
                    corpus.alternatives("je", "zapisano"), [("tako", 20)]
                )
        finally:
            os.chdir(old_cwd)

    def test_missing_path_unavailable_and_still_absent(self) -> None:
        missing = self.root / "absent-index.sqlite"
        with self.assertRaises(RuntimeCorpusError) as ctx:
            RuntimeCorpus(missing)
        self.assertEqual(ctx.exception.reason, REASON_UNAVAILABLE)
        self.assertFalse(missing.exists())

    def test_directory_path_unavailable(self) -> None:
        with self.assertRaises(RuntimeCorpusError) as ctx:
            RuntimeCorpus(self.root)
        self.assertEqual(ctx.exception.reason, REASON_UNAVAILABLE)

    def test_embedded_nul_rejected_before_uri_encoding(self) -> None:
        # A NUL would be percent-encoded, decoded by SQLite and truncated
        # by platform path handling, silently naming the shorter prefix
        # file; the exact configured path must fail closed instead.
        with self.assertRaises(RuntimeCorpusError) as ctx:
            RuntimeCorpus(f"{self.db}\x00different")
        self.assertEqual(ctx.exception.reason, REASON_UNAVAILABLE)

    def test_literal_percent00_filename_still_works(self) -> None:
        literal = self.root / "pct%00name.sqlite"
        _build_db(literal)
        with RuntimeCorpus(literal) as corpus:
            self.assertEqual(corpus.unigram("to").count, 100)

    def test_regular_file_symlink_and_hardlink_paths_still_work(self) -> None:
        # Ordinary regular-file paths that open as regular files -
        # including symlink and hardlink spellings - remain supported;
        # the exact configured path is still the only path used.
        with self.subTest(link="symlink"):
            link = self.root / "link.sqlite"
            link.symlink_to(self.db)
            with RuntimeCorpus(link) as corpus:
                self.assertEqual(corpus.unigram("to").count, 100)
        with self.subTest(link="hardlink"):
            hard = self.root / "hard.sqlite"
            os.link(self.db, hard)
            with RuntimeCorpus(hard) as corpus:
                self.assertEqual(corpus.unigram("to").count, 100)

    def test_nonregular_resource_rejected_without_blocking(self) -> None:
        # An owned anonymous pipe exposed through /proc/self/fd is a
        # real non-regular resource: a blocking read on it would wait
        # indefinitely for a writer that never comes.  The real
        # constructor therefore runs in an ordinary Python child (no
        # model agent) with a finite subprocess deadline - kill and
        # reap on timeout - so a regressed blocking read cannot hang
        # the suite.  The child inherits exactly the owned read fd;
        # the parent keeps the write end open for the duration (the
        # writer never writes, matching the observed boundary) and
        # closes both owned fds in finally.  No filesystem FIFO is
        # created for the OAP runtime.
        read_end, write_end = os.pipe()
        child_code = (
            "import sys\n"
            f"sys.path.insert(0, {str(ROOT)!r})\n"
            "import runtime_corpus as rc\n"
            "try:\n"
            f"    rc.RuntimeCorpus('/proc/self/fd/{read_end}')\n"
            "    print('NO_ERROR')\n"
            "except rc.RuntimeCorpusError as exc:\n"
            "    print('ERROR', exc.reason)\n"
        )
        started = time.monotonic()
        try:
            proc = subprocess.run(
                [sys.executable, "-B", "-c", child_code],
                cwd=str(ROOT),
                pass_fds=(read_end,),
                capture_output=True,
                text=True,
                timeout=10.0,
            )
        except subprocess.TimeoutExpired:
            self.fail(
                "constructor blocked on a non-regular resource; "
                "finite deadline exceeded, child killed and reaped"
            )
        finally:
            os.close(read_end)
            os.close(write_end)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("ERROR RUNTIME_EVIDENCE_UNAVAILABLE", proc.stdout)
        self.assertNotIn("NO_ERROR", proc.stdout)
        self.assertLess(time.monotonic() - started, 5.0)

    def test_wal_journal_rejected_before_open_without_auxiliary_files(
        self,
    ) -> None:
        # A WAL-journal index is rejected by the bounded header
        # preflight BEFORE any SQLite open, so no -wal/-shm auxiliary
        # file is ever created and the database bytes are untouched;
        # the directory file set and bytes are equal before and after
        # the (in-thread) constructor read.
        wal = self.root / "wal.sqlite"
        _build_db(wal)
        connection = sqlite3.connect(wal)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute(
            "UPDATE unigram SET count = count + 1 WHERE word = 'to'"
        )
        connection.commit()
        connection.close()
        before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        started = time.monotonic()
        with self.assertRaises(RuntimeCorpusError) as ctx:
            RuntimeCorpus(wal)
        elapsed = time.monotonic() - started
        self.assertEqual(ctx.exception.reason, REASON_UNSUPPORTED_JOURNAL)
        self.assertLess(elapsed, 10.0)
        after = {path.name: path.read_bytes() for path in self.root.iterdir()}
        self.assertEqual(after, before)
        self.assertNotIn("wal.sqlite-wal", after)
        self.assertNotIn("wal.sqlite-shm", after)

    def test_corrupt_bytes(self) -> None:
        corrupt = self.root / "corrupt.sqlite"
        corrupt.write_bytes(b"this is not a sqlite database")
        with self.assertRaises(RuntimeCorpusError) as ctx:
            RuntimeCorpus(corrupt)
        self.assertEqual(ctx.exception.reason, REASON_CORRUPT)

    def test_incompatible_accessed_schema(self) -> None:
        with self.subTest(missing_table=True):
            only_unigram = self.root / "only-unigram.sqlite"
            _build_db(only_unigram, tables={"unigram"})
            with self.assertRaises(RuntimeCorpusError) as ctx:
                RuntimeCorpus(only_unigram)
            self.assertEqual(ctx.exception.reason, REASON_INCOMPATIBLE)
        with self.subTest(missing_count_column=True):
            no_count = self.root / "no-count.sqlite"
            connection = sqlite3.connect(no_count)
            for table, column in (
                ("unigram", "word"),
                ("bigram", "phrase"),
                ("trigram", "phrase"),
            ):
                connection.execute(
                    f"CREATE TABLE {table} ({column} TEXT PRIMARY KEY)"
                )
            connection.execute(
                "CREATE TABLE middle (left_word TEXT, right_word TEXT, "
                "middle_word TEXT, frequency INTEGER, "
                "PRIMARY KEY(left_word,right_word,middle_word))"
            )
            connection.commit()
            connection.close()
            with self.assertRaises(RuntimeCorpusError) as ctx:
                RuntimeCorpus(no_count)
            self.assertEqual(ctx.exception.reason, REASON_INCOMPATIBLE)

    def test_read_only_never_creates_or_writes(self) -> None:
        before = hashlib.sha256(self.db.read_bytes()).hexdigest()
        with RuntimeCorpus(self.db) as corpus:
            corpus.unigram("to")
            corpus.ngram("je tako", 2)
            corpus.ngram("to je tako", 3)
            corpus.alternatives("je", "zapisano")
            with self.assertRaises(sqlite3.OperationalError):
                corpus.connection.execute(
                    "INSERT INTO unigram VALUES('x', 1)"
                )
            with self.assertRaises(sqlite3.OperationalError):
                corpus.connection.execute("CREATE TABLE scratch (x INTEGER)")
        self.assertEqual(hashlib.sha256(self.db.read_bytes()).hexdigest(), before)

    def test_count_validation_all_query_methods(self) -> None:
        cases: list[tuple[str, str, str, object, str]] = [
            # (label, table, count column type, stored value, query method)
            ("unigram-text", "unigram", "count TEXT", "5", "unigram"),
            ("unigram-null", "unigram", "count INTEGER", None, "unigram"),
            ("unigram-negative", "unigram", "count INTEGER NOT NULL", -5, "unigram"),
            ("unigram-fractional", "unigram", "count INTEGER NOT NULL", 2.5, "unigram"),
            ("bigram-text", "bigram", "count TEXT", "7", "bigram"),
            ("trigram-negative", "trigram", "count INTEGER NOT NULL", -1, "trigram"),
            ("middle-null", "middle", "count INTEGER", None, "middle"),
        ]
        for label, table, column_type, bad_value, method in cases:
            with self.subTest(case=label):
                path = self.root / f"bad-{label}.sqlite"
                if table == "unigram":
                    rows: list[tuple[str, object]] = [("to", bad_value)]
                    rows.extend(r for r in HEALTHY_UNIGRAM if r[0] != "to")
                    _build_db(path, unigram=rows, count_columns={"count": column_type})
                elif table == "bigram":
                    rows = [("je tako", bad_value)]
                    rows.extend(r for r in HEALTHY_BIGRAM if r[0] != "je tako")
                    _build_db(path, bigram=rows, count_columns={"count": column_type})
                elif table == "trigram":
                    rows = [("to je tako", bad_value)]
                    rows.extend(r for r in HEALTHY_TRIGRAM if r[0] != "to je tako")
                    _build_db(path, trigram=rows, count_columns={"count": column_type})
                else:
                    middle_rows: list[tuple[str, str, str, object]] = [
                        ("je", "zapisano", "tako", bad_value),
                    ]
                    _build_db(path, middle=middle_rows, count_columns={"count": column_type})
                # Verify the fixture actually stored the claimed shape
                # (SQLite affinity can otherwise coerce numeric strings).
                check = sqlite3.connect(path)
                key_column = (
                    "word" if table == "unigram" else "phrase"
                    if table in ("bigram", "trigram") else "middle_word"
                )
                key_value = (
                    "to" if table == "unigram"
                    else "je tako" if table == "bigram"
                    else "to je tako" if table == "trigram" else "tako"
                )
                stored = check.execute(
                    f"SELECT typeof(count), count FROM {table} "
                    f"WHERE {key_column}=?",
                    (key_value,),
                ).fetchone()
                check.close()
                expected_kind = (
                    "null" if bad_value is None
                    else "text" if isinstance(bad_value, str)
                    else "real" if isinstance(bad_value, float)
                    else "integer"
                )
                self.assertEqual(stored[0], expected_kind, label)
                if bad_value is None:
                    self.assertIsNone(stored[1])
                with RuntimeCorpus(path) as corpus:
                    with self.assertRaises(RuntimeCorpusError) as ctx:
                        if method == "unigram":
                            corpus.unigram("to")
                        elif method == "bigram":
                            corpus.ngram("je tako", 2)
                        elif method == "trigram":
                            corpus.ngram("to je tako", 3)
                        else:
                            corpus.alternatives("je", "zapisano")
                    self.assertEqual(ctx.exception.reason, REASON_INVALID_COUNT)
                    self.assertNotIn(str(bad_value), str(ctx.exception))

    def test_valid_zero_and_missing_scopes(self) -> None:
        zero_db = self.root / "zero.sqlite"
        rows = [
            ("to", 0),
        ] + [row for row in HEALTHY_UNIGRAM if row[0] != "to"]
        _build_db(zero_db, unigram=rows)
        with RuntimeCorpus(zero_db) as corpus:
            evidence = corpus.unigram("to")
            self.assertEqual(evidence.state, "EXACT")
            self.assertEqual(evidence.count, 0)
            self.assertEqual(corpus.unigram("nic").state, "UNAVAILABLE")
            self.assertIsNone(corpus.unigram("nic").count)
            self.assertEqual(corpus.ngram("to nic", 2).state, "CENSORED")
            self.assertIsNone(corpus.ngram("to nic", 2).count)

    def test_handle_closed_on_success_and_failure(self) -> None:
        corpus = RuntimeCorpus(self.db)
        corpus.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            corpus.connection.execute("SELECT 1")
        seen: list[bool] = []
        real_init = RuntimeCorpus.__init__

        def spy_init(self: RuntimeCorpus, path: str | Path) -> None:
            try:
                real_init(self, path)
            except Exception:
                seen.append(hasattr(self, "connection"))
                raise

        with mock.patch.object(
            RuntimeCorpus, "__init__", spy_init
        ), self.assertRaises(RuntimeCorpusError):
            RuntimeCorpus(self.root / "absent.sqlite")
        # A failed construction exposes no open connection handle.
        self.assertEqual(seen, [False])
        # A connect that succeeds but whose accessed-schema validation
        # fails (incompatible schema) must close the already-allocated
        # handle: observe the real connection through a wrapping
        # connector and prove it is unusable afterwards.  The corrupt
        # case is rejected by the header preflight before any SQLite
        # connection is allocated at all.
        real_connect = sqlite3.connect

        for label, bad_path in (
            ("corrupt", self.root / "closure-corrupt.sqlite"),
            ("incompatible", self.root / "closure-incompatible.sqlite"),
        ):
            with self.subTest(closure=label):
                if label == "corrupt":
                    bad_path.write_bytes(b"not a sqlite database")
                else:
                    _build_db(bad_path, tables={"unigram"})
                allocated: list[sqlite3.Connection] = []

                def spy_connect(
                    database: str,
                    *,
                    uri: bool,
                    timeout: float,
                    _allocated: list[sqlite3.Connection] = allocated,
                ) -> sqlite3.Connection:
                    connection = real_connect(
                        database, uri=uri, timeout=timeout
                    )
                    _allocated.append(connection)
                    return connection

                with mock.patch.object(
                    sqlite3, "connect", spy_connect
                ), self.assertRaises(RuntimeCorpusError):
                    RuntimeCorpus(bad_path)
                if label == "corrupt":
                    self.assertEqual(allocated, [])
                else:
                    self.assertEqual(len(allocated), 1)
                    with self.assertRaises(sqlite3.ProgrammingError):
                        allocated[0].execute("SELECT 1")

    def test_lock_contention_degrades_within_deadline_and_recovers(self) -> None:
        writer = sqlite3.connect(self.db)
        writer.execute("BEGIN EXCLUSIVE")
        try:
            # The accessed-schema validation is the first read on the
            # fresh connection, so the bounded degradation (finite busy
            # wait, then a locked label) is observed at construction;
            # no query result or write is attempted before it.
            started = time.monotonic()
            with self.assertRaises(RuntimeCorpusError) as ctx:
                RuntimeCorpus(self.db)
            elapsed = time.monotonic() - started
            self.assertEqual(ctx.exception.reason, REASON_LOCKED)
            self.assertLess(elapsed, 10.0)  # generous finite test deadline
            writer.rollback()
            with RuntimeCorpus(self.db) as corpus:
                # The configured finite busy wait (0.25 s) must be
                # actually in effect on the healthy connection: a
                # regression to the SQLite default (5 s) would still
                # pass the generous timing bound above but is wrong.
                self.assertEqual(
                    corpus.connection.execute(
                        "PRAGMA busy_timeout"
                    ).fetchone()[0],
                    int(RUNTIME_CORPUS_BUSY_TIMEOUT_SECONDS * 1000),
                )
                self.assertEqual(corpus.unigram("to").state, "EXACT")
        finally:
            writer.close()


class _EvidenceHarness:
    """One real proxy instance with recording fake main/review upstreams.

    The index path, optional trace directory and usage observer are
    per-instance; the main source, content type and reviewer payload are
    reset per request (class-attribute fakes shared by design, matching
    the established actual-HTTP fixtures).
    """

    def __init__(
        self,
        index: Path,
        usage_observer: list[dict[str, object]] | None = None,
        trace_dir: Path | None = None,
    ) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.observed: list[dict[str, object]] = (
            usage_observer if usage_observer is not None else []
        )
        self.main_server = HTTPServer(("127.0.0.1", 0), _MainUpstream)
        self.review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        for server in (self.main_server, self.review_server):
            threading.Thread(target=server.serve_forever, daemon=True).start()
        reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.review_server.server_port}/v1",
            "test-model",
            timeout=5.0,
            api_key="fake-review-key",
        )
        self.engine = proxy.RepairEngine(index, reviewer, pandoc=_real_spec())
        self.proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{self.main_server.server_port}",
            self.engine,
            usage_observer=(
                (lambda record: self.observed.append(record))
                if usage_observer is not None
                else None
            ),
            trace_dir=trace_dir,
        )
        threading.Thread(target=self.proxy_server.serve_forever, daemon=True).start()

    def request(
        self,
        source: bytes,
        content_type: str,
        stream: bool,
        review_payload: bytes,
        main_status: int = 200,
    ) -> tuple[int, bytes]:
        _MainUpstream.source = source
        _MainUpstream.content_type = content_type
        _MainUpstream.status = main_status
        _MainUpstream.recorded = []
        _FakeUpstream.payload = review_payload
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.recorded = []
        body = _contract_body(stream)
        client = http.client.HTTPConnection(
            "127.0.0.1", self.proxy_server.server_port, timeout=30
        )
        client.request(
            "POST",
            "/v1/responses",
            body=body,
            headers={
                "Content-Length": str(len(body)),
                "X-Concept-Request-ID": "req016a",
            },
        )
        response = client.getresponse()
        payload = response.read()
        client.close()
        return response.status, payload

    def traces(self) -> list[dict[str, object]]:
        if self.proxy_server.trace_dir is None:
            return []
        return [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(self.proxy_server.trace_dir.glob("*.json"))
        ]

    def close(self) -> None:
        for server in (self.proxy_server, self.main_server, self.review_server):
            server.shutdown()
        for server in (self.proxy_server, self.main_server, self.review_server):
            server.server_close()
        self.temp.cleanup()


def _replace_both_payload(usage: object = _ABSENT) -> bytes:
    return _review_payload(
        [_prop("t0", replacement="tako"), _prop("t1", replacement="tako")],
        usage=usage,
    )


class RuntimeEvidenceHttpTests(unittest.TestCase):
    """Actual HTTP: real ConceptProxy -> real engine (qualified Pandoc and
    real tiny SQLite) -> real ResponsesReviewer; synthetic upstreams only.
    """

    JSON_SOURCE = _json_completed(TEXT)
    SSE_SOURCE = _tc_baseline(TEXT)

    def _late_index(self, root: Path, canary: str) -> Path:
        late = root / "late.sqlite"
        rows = list(HEALTHY_UNIGRAM) + [("tako\u017e", canary)]
        _build_db(late, unigram=rows)
        return late

    def _late_payload(self) -> bytes:
        return _review_payload(
            [
                _prop("t0", replacement="tako"),
                _prop("t1", replacement="tako\u017e"),
            ],
            usage={"input_tokens": 11, "output_tokens": 5, "total_tokens": 16},
        )

    def _healthy_payload(self) -> bytes:
        return _review_payload(
            [
                _prop("t0", replacement="tako"),
                _prop("t1", replacement="tako"),
            ],
            usage={"input_tokens": 21, "output_tokens": 7, "total_tokens": 28},
        )

    # -- healthy useful repair (exactly one fresh batch) -------------------

    def test_http_healthy_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _build_db(root / "healthy.sqlite")
            harness = _EvidenceHarness(root / "healthy.sqlite")
            try:
                status, payload = harness.request(
                    self.JSON_SOURCE, "application/json", False, _replace_both_payload()
                )
                self.assertEqual(status, 200)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                value = json.loads(payload)
                part = value["output"][0]["content"][0]
                self.assertEqual(part["text"], "To je tako zapisano, to je tako zapisano.")
                status, payload = harness.request(
                    self.SSE_SOURCE, "text/event-stream", True, _replace_both_payload()
                )
                self.assertEqual(status, 200)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                self.assertIn(b"To je tako zapisano, to je tako zapisano.", payload)
            finally:
                harness.close()

    # -- early technical failures: exact original, zero calls --------------

    def _early_case(self, label: str, index: Path, stream: bool) -> None:
        with tempfile.TemporaryDirectory():
            harness = _EvidenceHarness(index)
            try:
                if stream:
                    status, payload = harness.request(
                        self.SSE_SOURCE, "text/event-stream", True,
                        _replace_both_payload(),
                    )
                    source = self.SSE_SOURCE
                else:
                    status, payload = harness.request(
                        self.JSON_SOURCE, "application/json", False,
                        _replace_both_payload(),
                    )
                    source = self.JSON_SOURCE
                self.assertEqual(status, 200, label)
                self.assertEqual(payload, source, label)
                self.assertEqual(len(_FakeUpstream.recorded), 0, label)
            finally:
                harness.close()

    def test_missing_index_early(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "canary-absent-index.sqlite"
            self._early_case("missing", missing, False)
            self._early_case("missing-sse", missing, True)
            self.assertFalse(missing.exists(), "missing index must stay absent")

    def test_corrupt_index_early(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            corrupt = Path(temp) / "canary-corrupt-index.sqlite"
            corrupt.write_bytes(b"not a sqlite database, garbage bytes")
            self._early_case("corrupt", corrupt, False)
            self._early_case("corrupt-sse", corrupt, True)

    def test_incompatible_schema_early(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            incompatible = Path(temp) / "canary-incompatible.sqlite"
            _build_db(incompatible, tables={"unigram"})
            self._early_case("incompatible", incompatible, False)
            self._early_case("incompatible-sse", incompatible, True)

    @staticmethod
    def _directory_state(root: Path) -> dict[str, bytes]:
        return {path.name: path.read_bytes() for path in root.iterdir()}

    def test_wal_index_early_no_auxiliary_files(self) -> None:
        # A WAL-journal index is rejected by the bounded preflight
        # before any SQLite open, so no -wal/-shm auxiliary file may
        # ever appear.  The bounded polling samples complement that
        # before-open proof (they do not by themselves establish
        # every transient instant); the deterministic bracket is the
        # direct constructor test around the in-thread read.  The
        # directory file set and bytes must be unchanged before,
        # across the sampled window, and after both requests.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            wal = root / "canary-wal.sqlite"
            _build_db(wal)
            connection = sqlite3.connect(wal)
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute(
                "UPDATE unigram SET count = count + 1 WHERE word = 'to'"
            )
            connection.commit()
            connection.close()
            before = self._directory_state(root)
            self.assertNotIn("canary-wal.sqlite-wal", before)
            self.assertNotIn("canary-wal.sqlite-shm", before)
            states: list[dict[str, bytes]] = []

            def monitor() -> None:
                deadline = time.monotonic() + 8.0
                while time.monotonic() < deadline:
                    states.append(self._directory_state(root))
                    time.sleep(0.005)

            monitor_thread = threading.Thread(target=monitor, daemon=True)
            monitor_thread.start()
            try:
                self._early_case("wal", wal, False)
                self._early_case("wal-sse", wal, True)
            finally:
                monitor_thread.join(timeout=10.0)
                self.assertFalse(monitor_thread.is_alive())
            self.assertTrue(states)
            for state in states:
                self.assertEqual(state, before)
            self.assertEqual(self._directory_state(root), before)

    def test_bad_stored_count_early(self) -> None:
        # The detected word carries a technically invalid stored count:
        # text, NULL, negative and fractional storage each fail closed
        # before detection completes, with zero review calls.
        for label, bad_value in (
            ("text", "canary-text-count"),
            ("null", None),
            ("negative", -5),
            ("fractional", 2.5),
        ):
            with self.subTest(count=label), \
                    tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / f"canary-{label}.sqlite"
                rows: list[tuple[str, object]] = [
                    r for r in HEALTHY_UNIGRAM if r[0] != "presenetliv"
                ]
                rows.append(("presenetliv", bad_value))
                # A NULL count can only be stored in a nullable
                # column; the other shapes use the default column and
                # are stored as typed (verified by the direct test).
                count_columns = (
                    {"count": "count INTEGER"} if bad_value is None else None
                )
                _build_db(path, unigram=rows, count_columns=count_columns)
                self._early_case(label, path, False)
                self._early_case(label + "-sse", path, True)

    def test_lock_contention_early(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            index = root / "locked.sqlite"
            _build_db(index)
            writer = sqlite3.connect(index)
            writer.execute("BEGIN EXCLUSIVE")
            try:
                harness = _EvidenceHarness(index)
                try:
                    status, payload = harness.request(
                        self.JSON_SOURCE, "application/json", False,
                        _replace_both_payload(),
                    )
                    self.assertEqual(status, 200)
                    self.assertEqual(payload, self.JSON_SOURCE)
                    self.assertEqual(len(_FakeUpstream.recorded), 0)
                finally:
                    harness.close()
            finally:
                writer.close()

    # -- late replacement-only failure: whole optional pass aborted --------

    def _late_case(
        self,
        stream: bool,
        usage: object,
    ) -> tuple[bytes, dict[str, object], dict[str, object]]:
        """Late failure request; observations are the actual usage
        callback record and the actual persisted trace (the HTTP handler
        consumes the engine details, so no post-hoc detail access)."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            canary = f"canary-late-{os.urandom(4).hex()}"
            index = self._late_index(root, canary)
            observed: list[dict[str, object]] = []
            harness = _EvidenceHarness(
                index, usage_observer=observed, trace_dir=root / "traces"
            )
            try:
                payload = _review_payload(
                    [
                        _prop("t0", replacement="tako"),
                        _prop("t1", replacement="tako\u017e"),
                    ],
                    usage=usage,
                )
                if stream:
                    status, body = harness.request(
                        self.SSE_SOURCE, "text/event-stream", True, payload
                    )
                else:
                    status, body = harness.request(
                        self.JSON_SOURCE, "application/json", False, payload
                    )
                self.assertEqual(status, 200)
                source = self.SSE_SOURCE if stream else self.JSON_SOURCE
                self.assertEqual(body, source)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                self.assertEqual(len(observed), 1)
                traces = harness.traces()
                self.assertEqual(len(traces), 1)
                return body, observed[0], traces[0]
            finally:
                harness.close()

    def _assert_late_trace_rollback(self, trace: dict[str, object]) -> None:
        self.assertEqual(
            trace["evidence_failure"],
            {"reason": REASON_INVALID_COUNT, "stage": "late"},
        )
        self.assertEqual(trace["repaired"], trace["original"])
        self.assertEqual(trace["replacements"], [])
        acceptance = trace["acceptance"]
        if not isinstance(acceptance, list):
            raise AssertionError("acceptance must be a list in the trace")
        for item in acceptance:
            if not isinstance(item, dict):
                raise AssertionError("acceptance entries must be objects")
            self.assertEqual(
                item,
                {"accepted": False, "reason": "evidence-abort",
                 "replacement": None},
            )
        decisions = trace["reviewer_decisions"]
        if not isinstance(decisions, list):
            raise AssertionError("reviewer_decisions must be a list in the trace")
        for decision in decisions:
            if not isinstance(decision, dict):
                raise AssertionError("reviewer decisions must be objects")
            self.assertEqual(decision["failure"], REASON_INVALID_COUNT)
            self.assertIsInstance(decision["proposal"], dict)

    def test_late_replacement_only_failure_json_known_usage(self) -> None:
        _body, record, trace = self._late_case(False, {
            "input_tokens": 11, "output_tokens": 5, "total_tokens": 16,
        })
        self.assertEqual(record, {
            "review_calls": 1,
            "reviewer_usage": {
                "input_tokens": 11,
                "output_tokens": 5,
                "total_tokens": 16,
            },
        })
        self._assert_late_trace_rollback(trace)

    def test_late_replacement_only_failure_sse_unknown_usage(self) -> None:
        _body, record, trace = self._late_case(True, _ABSENT)
        self.assertEqual(record, {
            "review_calls": 1,
            "reviewer_usage": "unknown",
        })
        self._assert_late_trace_rollback(trace)

    def test_late_failure_persisted_trace_disposition(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            trace_dir = root / "traces"
            index = self._late_index(root, "canary-late-trace")
            harness = _EvidenceHarness(index, trace_dir=trace_dir)
            try:
                status, payload = harness.request(
                    self.JSON_SOURCE, "application/json", False, self._late_payload()
                )
                self.assertEqual(status, 200)
                self.assertEqual(payload, self.JSON_SOURCE)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                traces = harness.traces()
                self.assertEqual(len(traces), 1)
                trace = traces[0]
                self.assertEqual(
                    trace["evidence_failure"],
                    {"reason": REASON_INVALID_COUNT, "stage": "late"},
                )
                self.assertEqual(trace["repaired"], trace["original"])
                self.assertEqual(trace["replacements"], [])
                acceptance = trace["acceptance"]
                if not isinstance(acceptance, list):
                    raise AssertionError("acceptance must be a list in the trace")
                accepted_flags: list[bool] = []
                for item in acceptance:
                    if not isinstance(item, dict):
                        raise AssertionError("acceptance entries must be objects")
                    accepted_flags.append(bool(item.get("accepted")))
                self.assertNotIn(True, accepted_flags)
                decisions = trace["reviewer_decisions"]
                if not isinstance(decisions, list):
                    raise AssertionError(
                        "reviewer_decisions must be a list in the trace"
                    )
                for decision in decisions:
                    if not isinstance(decision, dict):
                        raise AssertionError("reviewer decisions must be objects")
                    self.assertEqual(decision["failure"], REASON_INVALID_COUNT)
                    self.assertIsNotNone(decision["proposal"])
            finally:
                harness.close()

    # -- ordinary missing evidence stays an individual rejection -----------

    def test_ordinary_missing_replacement_evidence_individual_rejection(self) -> None:
        payload = _review_payload(
            [_prop("t0", replacement="tako"), _prop("t1", replacement="to")]
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _build_db(root / "healthy.sqlite")
            harness = _EvidenceHarness(root / "healthy.sqlite")
            try:
                status, out = harness.request(
                    self.JSON_SOURCE, "application/json", False, payload
                )
                self.assertEqual(status, 200)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                value = json.loads(out)
                # Only the second proposal is rejected; the valid first
                # edit survives.
                self.assertEqual(
                    value["output"][0]["content"][0]["text"],
                    "To je tako zapisano, to je presenetliv zapisano.",
                )
                status, out = harness.request(
                    self.SSE_SOURCE, "text/event-stream", True, payload
                )
                self.assertEqual(status, 200)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                self.assertIn(b"To je tako zapisano, to je presenetliv zapisano.", out)
            finally:
                harness.close()

    # -- recovery and no carryover on the same proxy -----------------------

    def test_same_proxy_recovers_healthy_next_request_no_carryover(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            index = self._late_index(root, "canary-late-carryover")
            observed: list[dict[str, object]] = []
            harness = _EvidenceHarness(index, usage_observer=observed)
            try:
                status, payload = harness.request(
                    self.JSON_SOURCE, "application/json", False, self._late_payload()
                )
                self.assertEqual(status, 200)
                self.assertEqual(payload, self.JSON_SOURCE)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                status, payload = harness.request(
                    self.JSON_SOURCE, "application/json", False,
                    self._healthy_payload(),
                )
                self.assertEqual(status, 200)
                self.assertEqual(len(_FakeUpstream.recorded), 1)
                value = json.loads(payload)
                self.assertEqual(
                    value["output"][0]["content"][0]["text"],
                    "To je tako zapisano, to je tako zapisano.",
                )
                self.assertEqual(len(observed), 2)
                self.assertEqual(observed[0], {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 11,
                        "output_tokens": 5,
                        "total_tokens": 16,
                    },
                })
                self.assertEqual(observed[1], {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 21,
                        "output_tokens": 7,
                        "total_tokens": 28,
                    },
                })
            finally:
                harness.close()

    # -- content-free canaries ---------------------------------------------

    def test_canaries_absent_from_outputs(self) -> None:
        canary = f"canary-absent-{os.urandom(4).hex()}"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            missing = root / f"{canary}.sqlite"
            observed: list[dict[str, object]] = []
            trace_dir = root / "traces"
            harness = _EvidenceHarness(
                missing, usage_observer=observed, trace_dir=trace_dir
            )
            try:
                status, payload = harness.request(
                    self.JSON_SOURCE, "application/json", False,
                    _replace_both_payload(),
                )
                self.assertEqual(status, 200)
                self.assertEqual(payload, self.JSON_SOURCE)
                self.assertFalse(missing.exists())
                for blob in (payload, json.dumps(observed, ensure_ascii=False).encode()):
                    self.assertNotIn(canary.encode(), blob)
                for trace in harness.traces():
                    self.assertNotIn(canary, json.dumps(trace, ensure_ascii=False))
            finally:
                harness.close()

    def test_invalid_count_value_absent_from_outputs(self) -> None:
        canary = f"canary-late-value-{os.urandom(4).hex()}"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            index = self._late_index(root, canary)
            observed: list[dict[str, object]] = []
            trace_dir = root / "traces"
            harness = _EvidenceHarness(
                index, usage_observer=observed, trace_dir=trace_dir
            )
            try:
                status, payload = harness.request(
                    self.JSON_SOURCE, "application/json", False, self._late_payload()
                )
                self.assertEqual(status, 200)
                self.assertEqual(payload, self.JSON_SOURCE)
                for blob in (payload, json.dumps(observed, ensure_ascii=False).encode()):
                    self.assertNotIn(canary.encode(), blob)
                for trace in harness.traces():
                    self.assertNotIn(canary, json.dumps(trace, ensure_ascii=False))
            finally:
                harness.close()

    # -- main semantics preserved; ineligible main never opens evidence ----

    def test_main_semantics_preserved_and_ineligible_never_opens(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            missing = root / "canary-absent-main.sqlite"
            harness = _EvidenceHarness(missing)
            opened: list[bool] = []

            class _SpiedRuntimeCorpus(RuntimeCorpus):
                def __init__(self, path: str | Path) -> None:
                    opened.append(True)
                    super().__init__(path)

            try:
                with mock.patch.object(proxy, "RuntimeCorpus", _SpiedRuntimeCorpus):
                    self._run_main_semantics_cases(harness, missing)
                # mode=ro never creates a file, so absence alone cannot
                # prove no open was attempted: the constructor itself is
                # observed and must never be reached for ineligible main.
                self.assertEqual(opened, [])
            finally:
                harness.close()

    def _run_main_semantics_cases(self, harness: _EvidenceHarness, missing: Path) -> None:
        with self.subTest(incomplete_main=True):
            source = _json_completed(TEXT, status="in_progress")
            status, payload = harness.request(
                source, "application/json", False, _replace_both_payload()
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload, source)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertFalse(missing.exists())
        with self.subTest(raw_503_main=True):
            status, payload = harness.request(
                b"upstream unavailable", "application/json", False,
                _replace_both_payload(),
                main_status=503,
            )
            self.assertEqual(status, 503)
            self.assertEqual(payload, b"upstream unavailable")
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertFalse(missing.exists())
        with self.subTest(malformed_main=True):
            status, _payload = harness.request(
                b'{"object": "response"', "application/json", False,
                _replace_both_payload(),
            )
            self.assertEqual(status, 502)
            self.assertEqual(len(_FakeUpstream.recorded), 0)
            self.assertFalse(missing.exists())


if __name__ == "__main__":
    unittest.main()
