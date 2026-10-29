"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Actual-boundary tests for the finite runtime evidence budget (order
024-a, requirements 3-7).

Native real boundaries under test: real read-only SQLite (synthetic
owned databases), the real detector/acceptance/engine/proxy code, the
installed qualified Pandoc and, for the round-trip class, the real
ResponsesReviewer over owned loopback-0 HTTP.  Only the main upstream,
the review endpoint and (for the direct-engine class) the reviewer
object are synthetic fakes upstream of those boundaries; the corpus,
its queries and the engine/proxy paths are never faked.  No live
model, corpus, network or quality claim (order 024-a, requirement 7).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import socket
import sqlite3
import string
import sys
import tempfile
import unittest
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Protocol, cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
import proxy  # noqa: E402
import runtime_corpus  # noqa: E402
from batch_review import (  # noqa: E402
    BatchProposal,
    BatchResult,
    BatchTarget,
    BatchUsage,
)
from evidence_budget import (  # noqa: E402
    EvidenceBudgetState,
    EvidenceLimits,
    make_progress_handler,
    validate_default_evidence_policy,
)
from repair import accept as _real_accept  # noqa: E402
from runtime_corpus import (  # noqa: E402
    REASON_BUDGET_EXCEEDED,
    REASON_BUDGET_INVALID,
    REASON_CORRUPT,
    REASON_INCOMPATIBLE,
    REASON_INVALID_COUNT,
    REASON_LOCKED,
    REASON_UNAVAILABLE,
    RuntimeCorpus,
    RuntimeCorpusError,
)
from tests.test_responses_contract import (  # noqa: E402
    _Harness,
    _json_completed,
    _MainUpstream,
    _review_payload,
)
from tests.test_review_batch import (  # noqa: E402
    _contract_body,
    _FakeUpstream,
    _prop,
    _real_spec,
)

# One completed answer with zero detector candidates (every word is in
# the tiny lexicon with a local EXACT bigram): the under-budget
# no-suspicion baseline (order 024-a, requirement 5).
_HEALTHY = "To je tako zapisano, to je tako zapisano."

# The five schema-validation statements charge one start each; the
# accessed-table metadata rows are 5 (sqlite_master) + 2 + 2 + 2 + 4
# (PRAGMA table_info per accessed table) = 15 for the standard fixture.
_SCHEMA_STATEMENTS = 5
_SCHEMA_META_ROWS = 15

# Distinct synthetic absent words drive detector work at synthetic
# scale: token i costs 5 SQL starts (interior) or 2 (edge), so N
# tokens cost 5N-6 detection starts (order 024-a, E receipt).
_LATE_N = 13107   # 5 + 5N-6 + 2 accepted = exactly 65536 starts
_EARLY_N = 13108  # 5 + 5N-6 = 65539 > 65536 starts


def _absent_words(n: int) -> str:
    # Distinct all-letter tokens: the detector's WORD_RE matches letter
    # runs only, so each synthetic word must be one pure-letter token.
    # 3 letters over a-z give 17576 distinct words, enough for every
    # synthetic-scale case in this module.
    words = (
        "".join(combo)
        for combo in itertools.product(string.ascii_lowercase, repeat=3)
    )
    return " ".join(words for words in list(itertools.islice(words, n)))


def _index_state(root: Path, db: Path) -> tuple[str, list[str]]:
    """DB byte hash plus any journal/wal/shm sidecar names next to it."""
    names = sorted(
        p.name for p in root.iterdir() if p.name.startswith(db.name + "-")
    )
    return hashlib.sha256(db.read_bytes()).hexdigest(), names


def _fd_count() -> int:
    return len(list(Path("/proc/self/fd").iterdir()))


def _sub_mapping(detail: Mapping[str, object], key: str) -> dict[str, object]:
    value = detail[key]
    if not isinstance(value, dict):
        raise AssertionError(f"detail {key!r} is not a mapping")
    return cast("dict[str, object]", value)


def _envelope_text(payload: bytes) -> str:
    value = json.loads(payload)
    if not isinstance(value, dict):
        raise AssertionError("payload is not an object")
    output = value.get("output")
    if not isinstance(output, list) or not output or not isinstance(output[0], dict):
        raise AssertionError("payload has no output")
    content = output[0].get("content")
    if not isinstance(content, list) or not content or not isinstance(content[0], dict):
        raise AssertionError("payload has no content")
    text = content[0].get("text")
    if not isinstance(text, str):
        raise AssertionError("payload has no text")
    return text


def _evidence_db(root: Path, *, alt_rows: tuple[tuple[str, str, str, int], ...] = ()) -> Path:
    """One synthetic read-only evidence index (5 tables, tiny lexicon)."""
    db = root / "evidence.sqlite"
    connection = sqlite3.connect(db)
    connection.executescript(
        """
        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE unigram (word TEXT PRIMARY KEY, count INTEGER NOT NULL);
        CREATE TABLE bigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
        CREATE TABLE trigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
        CREATE TABLE middle (left_word TEXT, right_word TEXT, middle_word TEXT, count INTEGER,
            PRIMARY KEY(left_word,right_word,middle_word));
        INSERT INTO unigram VALUES
            ('to',100),('je',100),('tako',100),('zapisano',50),('repla',42);
        INSERT INTO bigram VALUES
            ('je tako',20),('tako zapisano',20),('repla aab',7);
        INSERT INTO trigram VALUES ('to je tako',20);
        """
    )
    if alt_rows:
        connection.executemany(
            "INSERT INTO middle VALUES (?,?,?,?)", alt_rows
        )
    connection.commit()
    connection.close()
    return db


def _alt_rows(n: int, left: str = "a", right: str = "b") -> tuple[tuple[str, str, str, int], ...]:
    return tuple((left, right, f"m{i:04d}", i) for i in range(n))


class _StubReviewer:
    """Synthetic reviewer standing in for the review worker (T7 only).

    It counts actual review_batch calls and proposes the same
    one-word replacement for every target; the engine, corpus and
    acceptance code around it are real.
    """

    def __init__(self, replacement: str = "repla", *, usage: bool = True) -> None:
        self.replacement = replacement
        self.usage_on = usage
        self.calls = 0

    def review_batch(
        self, sentence: str, targets: tuple[BatchTarget, ...]
    ) -> BatchResult:
        self.calls += 1
        proposals = {
            target.id: BatchProposal(target.id, False, self.replacement, False)
            for target in targets
        }
        usage = BatchUsage(10, 20, 30) if self.usage_on else None
        return BatchResult(proposals=proposals, usage=usage)


class UnderBudgetNativeTests(unittest.TestCase):
    """T1: native under-budget rows, order, counts, states, read-only."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _evidence_db(self.root, alt_rows=_alt_rows(11))
        self.before = _index_state(self.root, self.db)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_rows_order_counts_and_missing_states(self) -> None:
        corpus = RuntimeCorpus(self.db)
        self.assertEqual(corpus._budget.statements, _SCHEMA_STATEMENTS)
        self.assertEqual(corpus._budget.rows_total, _SCHEMA_META_ROWS)
        self.assertEqual(corpus.unigram("To").state, "EXACT")
        self.assertEqual(corpus.unigram("To").count, 100)
        self.assertEqual(corpus.unigram("nope").state, "UNAVAILABLE")
        self.assertEqual(corpus.ngram("Je tako", 2).state, "EXACT")
        self.assertEqual(corpus.ngram("Je tako", 2).count, 20)
        self.assertEqual(corpus.ngram("nope x", 2).state, "CENSORED")
        rows = corpus.alternatives("A", "B")
        self.assertEqual(len(rows), 11)
        self.assertEqual(rows[0], ("m0010", 10))  # count DESC
        self.assertEqual(rows[1], ("m0009", 9))
        self.assertEqual(rows[-1], ("m0000", 0))  # then middle_word ASC
        corpus.close()
        self.assertEqual(_index_state(self.root, self.db), self.before)

    def test_connection_is_read_only(self) -> None:
        corpus = RuntimeCorpus(self.db)
        with self.assertRaises(sqlite3.OperationalError):
            corpus.connection.execute("INSERT INTO meta VALUES ('k','v')")
        corpus.close()
        self.assertEqual(_index_state(self.root, self.db), self.before)

    def test_relative_path_keeps_semantics(self) -> None:
        previous = os.getcwd()
        try:
            os.chdir(self.root)
            corpus = RuntimeCorpus(self.db.name)
            self.assertEqual(corpus.unigram("to").count, 100)
            corpus.close()
        finally:
            os.chdir(previous)
        self.assertEqual(_index_state(self.root, self.db), self.before)

    def test_fresh_limits_per_instance_no_global_quota(self) -> None:
        first = RuntimeCorpus(self.db)
        first.unigram("to")
        first.alternatives("a", "b")
        second = RuntimeCorpus(self.db)
        # A concurrent fresh instance starts from full finite defaults.
        self.assertEqual(second._budget.statements, _SCHEMA_STATEMENTS)
        self.assertEqual(second._budget.rows_total, _SCHEMA_META_ROWS)
        self.assertFalse(second._budget.exhausted)
        self.assertEqual(len(second.alternatives("a", "b")), 11)
        second.close()
        first.close()


class InvalidPolicyBoundaryTests(unittest.TestCase):
    """T2: invalid policy fails before file at use and before bind at start."""

    FIELDS = (
        "max_statements",
        "max_rows_per_query",
        "max_rows_total",
        "progress_interval",
        "max_progress_callbacks",
    )
    CONFIG_FIELDS = (
        "RUNTIME_EVIDENCE_MAX_STATEMENTS",
        "RUNTIME_EVIDENCE_MAX_ROWS_PER_QUERY",
        "RUNTIME_EVIDENCE_MAX_ROWS_TOTAL",
        "RUNTIME_EVIDENCE_PROGRESS_INTERVAL",
        "RUNTIME_EVIDENCE_MAX_PROGRESS_CALLBACKS",
    )
    INVALID = (True, False, 1.5, float("inf"), float("nan"), "65536", 0, -1, 2**63)

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _evidence_db(self.root)
        self.before = _index_state(self.root, self.db)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_use_invalid_fields_rejected_before_any_file(self) -> None:
        for field in self.FIELDS:
            for value in self.INVALID:
                with self.subTest(field=field, value=value):
                    with self.assertRaises(RuntimeCorpusError) as caught:
                        if field == "max_statements":
                            RuntimeCorpus(self.db, max_statements=cast("int", value))
                        elif field == "max_rows_per_query":
                            RuntimeCorpus(
                                self.db, max_rows_per_query=cast("int", value)
                            )
                        elif field == "max_rows_total":
                            RuntimeCorpus(self.db, max_rows_total=cast("int", value))
                        elif field == "progress_interval":
                            RuntimeCorpus(self.db, progress_interval=cast("int", value))
                        else:
                            RuntimeCorpus(
                                self.db,
                                max_progress_callbacks=cast("int", value),
                            )
                    self.assertEqual(caught.exception.reason, REASON_BUDGET_INVALID)
        # A nonexistent path with an invalid limit must still be the
        # fixed budget-invalid label: validation precedes path access.
        with self.assertRaises(RuntimeCorpusError) as caught:
            RuntimeCorpus(self.root / "absent.sqlite", max_statements=cast("int", "x"))
        self.assertEqual(caught.exception.reason, REASON_BUDGET_INVALID)
        # The progress interval additionally rejects C-int overflow
        # even though it fits the 64-bit native-safe range.
        with self.assertRaises(RuntimeCorpusError) as caught:
            RuntimeCorpus(self.db, progress_interval=2**31)
        self.assertEqual(caught.exception.reason, REASON_BUDGET_INVALID)
        self.assertEqual(_index_state(self.root, self.db), self.before)

    def test_startup_invalid_policy_fails_before_bind_and_index(self) -> None:
        blocker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        blocker.bind(("127.0.0.1", 0))
        port = blocker.getsockname()[1]
        engine = proxy.RepairEngine(
            self.root / "absent.sqlite", _StubReviewer(), pandoc=_real_spec()
        )
        origins = {name: getattr(config, name) for name in self.CONFIG_FIELDS}
        try:
            for name in self.CONFIG_FIELDS:
                with self.subTest(field=name):
                    setattr(config, name, 0)
                    try:
                        raised: Exception | None = None
                        try:
                            proxy.ConceptProxy(
                                ("127.0.0.1", port), "http://127.0.0.1:1", engine
                            )
                        except Exception as exc:  # noqa: BLE001 - exact-type check
                            raised = exc
                        self.assertIsNotNone(raised)
                        # A plain policy ValueError: neither a
                        # RuntimeCorpusError (the index was never
                        # opened) nor an OSError (bind was never
                        # attempted) is acceptable here.
                        self.assertIs(type(raised), ValueError)
                    finally:
                        setattr(config, name, origins[name])
            # Differential control: with the valid policy the same
            # occupied port DOES reach bind and fails there.
            with self.assertRaises(OSError):
                proxy.ConceptProxy(
                    ("127.0.0.1", port), "http://127.0.0.1:1", engine
                )
        finally:
            for name, value in origins.items():
                setattr(config, name, value)
            blocker.close()

    def test_valid_overrides_and_defaults_unchanged(self) -> None:
        limits = validate_default_evidence_policy()
        self.assertEqual(
            limits,
            EvidenceLimits(65536, 4096, 262144, 1000, 10000),
        )
        self.assertEqual(limits.max_statements, config.RUNTIME_EVIDENCE_MAX_STATEMENTS)
        self.assertEqual(
            limits.max_rows_per_query, config.RUNTIME_EVIDENCE_MAX_ROWS_PER_QUERY
        )
        self.assertEqual(limits.max_rows_total, config.RUNTIME_EVIDENCE_MAX_ROWS_TOTAL)
        self.assertEqual(limits.progress_interval, config.RUNTIME_EVIDENCE_PROGRESS_INTERVAL)
        self.assertEqual(
            limits.max_progress_callbacks, config.RUNTIME_EVIDENCE_MAX_PROGRESS_CALLBACKS
        )
        corpus = RuntimeCorpus(self.db)
        self.assertEqual(corpus.unigram("to").count, 100)
        corpus.close()
        corpus = RuntimeCorpus(
            self.db,
            max_statements=100,
            max_rows_per_query=100,
            max_rows_total=1000,
            progress_interval=100,
            max_progress_callbacks=1000,
        )
        self.assertEqual(corpus.unigram("to").count, 100)
        corpus.close()
        server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            "http://127.0.0.1:1",
            proxy.RepairEngine(self.db, _StubReviewer(), pandoc=_real_spec()),
        )
        server.server_close()


class StatementBoundaryTests(unittest.TestCase):
    """T3: every SQL start charged before execute; no over-cap execution."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _evidence_db(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_schema_exhaustion_at_open_closes_connection(self) -> None:
        fd_before = _fd_count()
        with self.assertRaises(RuntimeCorpusError) as caught:
            RuntimeCorpus(self.db, max_statements=3)
        self.assertEqual(caught.exception.reason, REASON_BUDGET_EXCEEDED)
        self.assertLessEqual(_fd_count(), fd_before)
        # No partial state: a fresh default instance works fully.
        corpus = RuntimeCorpus(self.db)
        self.assertEqual(corpus.unigram("to").count, 100)
        corpus.close()

    def test_exact_schema_cap_denies_first_data_start(self) -> None:
        fd_before = _fd_count()
        corpus = RuntimeCorpus(self.db, max_statements=_SCHEMA_STATEMENTS)
        try:
            self.assertEqual(corpus._budget.statements, _SCHEMA_STATEMENTS)
            with self.assertRaises(RuntimeCorpusError) as caught:
                corpus.unigram("to")
            self.assertEqual(caught.exception.reason, REASON_BUDGET_EXCEEDED)
            # The denied start is charged to nothing and sticks.
            self.assertEqual(corpus._budget.statements, _SCHEMA_STATEMENTS)
            self.assertTrue(corpus._budget.exhausted)
            self.assertEqual(corpus._budget.rows_total, _SCHEMA_META_ROWS)
        finally:
            corpus.close()
        self.assertLessEqual(_fd_count(), fd_before)

    def test_cap_includes_data_and_denies_next_before_execute(self) -> None:
        corpus = RuntimeCorpus(self.db, max_statements=_SCHEMA_STATEMENTS + 1)
        try:
            self.assertEqual(corpus.unigram("to").count, 100)
            self.assertEqual(corpus._budget.statements, _SCHEMA_STATEMENTS + 1)
            with self.assertRaises(RuntimeCorpusError) as caught:
                corpus.unigram("je")
            self.assertEqual(caught.exception.reason, REASON_BUDGET_EXCEEDED)
            # No over-cap execution: the counter never passes the cap.
            self.assertEqual(corpus._budget.statements, _SCHEMA_STATEMENTS + 1)
        finally:
            corpus.close()


class RowQuotaTests(unittest.TestCase):
    """T4: per-query and cumulative row quotas, whole-discard overflow."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _evidence_db(self.root, alt_rows=_alt_rows(11))
        self.before = _index_state(self.root, self.db)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_metadata_rows_counted_after_schema(self) -> None:
        corpus = RuntimeCorpus(self.db)
        self.assertEqual(corpus._budget.rows_total, _SCHEMA_META_ROWS)
        corpus.close()

    def test_per_query_overflow_discards_whole_result(self) -> None:
        fd_before = _fd_count()
        corpus = RuntimeCorpus(self.db, max_rows_per_query=10)
        try:
            with self.assertRaises(RuntimeCorpusError) as caught:
                corpus.alternatives("a", "b")
            self.assertEqual(caught.exception.reason, REASON_BUDGET_EXCEEDED)
            # 11 rows actually fetched (allowed 10 + the one probe row
            # used solely to detect overflow) are all accounted, and
            # the whole result is discarded, never truncated.
            self.assertEqual(corpus._budget.rows_total, _SCHEMA_META_ROWS + 11)
            self.assertTrue(corpus._budget.exhausted)
            # Sticky exhaustion: the next start is denied before execute.
            with self.assertRaises(RuntimeCorpusError) as second:
                corpus.alternatives("a", "b")
            self.assertEqual(second.exception.reason, REASON_BUDGET_EXCEEDED)
        finally:
            corpus.close()
        self.assertLessEqual(_fd_count(), fd_before)
        self.assertEqual(_index_state(self.root, self.db), self.before)

    def test_exact_quota_eof_returns_all_rows(self) -> None:
        corpus = RuntimeCorpus(self.db, max_rows_per_query=11, max_rows_total=26)
        try:
            rows = corpus.alternatives("a", "b")
            self.assertEqual(len(rows), 11)
            self.assertFalse(corpus._budget.exhausted)
            self.assertEqual(corpus._budget.rows_total, 26)
        finally:
            corpus.close()

    def test_cumulative_quota_not_reset_per_query(self) -> None:
        corpus = RuntimeCorpus(self.db, max_rows_per_query=11, max_rows_total=26)
        try:
            self.assertEqual(len(corpus.alternatives("a", "b")), 11)
            self.assertEqual(corpus._budget.rows_total, 26)
            # Zero remaining total: allowed = min(11, 0) = 0, so even
            # this second identical result overflows on its probe row.
            with self.assertRaises(RuntimeCorpusError) as caught:
                corpus.alternatives("a", "b")
            self.assertEqual(caught.exception.reason, REASON_BUDGET_EXCEEDED)
            self.assertEqual(corpus._budget.rows_total, 27)
        finally:
            corpus.close()

    def test_empty_result_within_zero_remaining_quota(self) -> None:
        corpus = RuntimeCorpus(self.db, max_rows_per_query=11, max_rows_total=26)
        try:
            corpus.alternatives("a", "b")
            self.assertEqual(corpus.alternatives("z", "z"), [])
            self.assertFalse(corpus._budget.exhausted)
            self.assertEqual(corpus._budget.rows_total, 26)
        finally:
            corpus.close()


class NativeProgressInterruptTests(unittest.TestCase):
    """T5: real unindexed scan/sort interrupted by the native progress API."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = self._build_big_db(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def _build_big_db(root: Path) -> Path:
        db = root / "big.sqlite"
        connection = sqlite3.connect(db)
        connection.executescript(
            """
            CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE unigram (word TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE bigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE trigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE middle (left_word TEXT, right_word TEXT, middle_word TEXT, count INTEGER);
            INSERT INTO unigram VALUES ('to', 100);
            """
        )
        connection.executemany(
            "INSERT INTO middle VALUES ('l','r',?,?)",
            [(f"m{i:05d}", i) for i in range(20000)],
        )
        connection.commit()
        connection.close()
        return db

    def test_actual_scan_sort_interrupt_with_generous_other_caps(self) -> None:
        # The 20k-row middle table makes the fixed alternatives query
        # scan and sort without any index; the statement and row caps
        # stay at their generous defaults, so only the callback budget
        # (plus the native interval) can interrupt the work.
        corpus = RuntimeCorpus(
            self.db, progress_interval=30, max_progress_callbacks=1000
        )
        fd_before = _fd_count()
        try:
            with self.assertRaises(RuntimeCorpusError) as caught:
                corpus.alternatives("l", "r")
            self.assertEqual(caught.exception.reason, REASON_BUDGET_EXCEEDED)
            state = corpus._budget
            self.assertTrue(state.exhausted)
            # Exactly the one callback that crossed the budget: the
            # handler stops counting once its own flag is set.
            self.assertEqual(state.callbacks, 1001)
            # Statement and row caps were NOT the cause.
            self.assertEqual(state.statements, _SCHEMA_STATEMENTS + 1)
            self.assertEqual(state.rows_total, _SCHEMA_META_ROWS)
        finally:
            corpus.close()
        self.assertLessEqual(_fd_count(), fd_before)
        # A fresh instance with the default policy works on the same DB.
        fresh = RuntimeCorpus(self.db)
        try:
            self.assertEqual(fresh.unigram("to").count, 100)
        finally:
            fresh.close()


class OwnershipAndControlTests(unittest.TestCase):
    """T6: hook/SQL/lock/interrupt/caller-control cleanup at real boundaries."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _evidence_db(self.root, alt_rows=_alt_rows(500))
        self.before = _index_state(self.root, self.db)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_corrupt_header_preflight_label_unchanged(self) -> None:
        corrupt = self.root / "corrupt.sqlite"
        corrupt.write_bytes(b"this is not a sqlite database")
        fd_before = _fd_count()
        try:
            with self.assertRaises(RuntimeCorpusError) as caught:
                RuntimeCorpus(corrupt)
            self.assertEqual(caught.exception.reason, REASON_CORRUPT)
        finally:
            self.assertLessEqual(_fd_count(), fd_before)

    def test_malformed_image_sql_step_keeps_old_label(self) -> None:
        # A valid 100-byte header over a truncated body: the preflight
        # passes and the first real SQL step fails inside SQLite with
        # "database disk image is malformed".  The unchanged old label
        # table has no dedicated label for that class, so it keeps the
        # old UNAVAILABLE mapping (order 024-a: every other SQLite
        # error retains the old fixed labels and causes).
        truncated = self.root / "truncated.sqlite"
        truncated.write_bytes(self.db.read_bytes()[:100])
        fd_before = _fd_count()
        try:
            with self.assertRaises(RuntimeCorpusError) as caught:
                RuntimeCorpus(truncated)
            self.assertEqual(caught.exception.reason, REASON_UNAVAILABLE)
            self.assertEqual(caught.exception.detail, "DatabaseError")
        finally:
            self.assertLessEqual(_fd_count(), fd_before)
        corpus = RuntimeCorpus(self.db)
        self.assertEqual(corpus.unigram("to").count, 100)
        corpus.close()

    def test_locked_label_kept_and_next_instance_works(self) -> None:
        writer = sqlite3.connect(self.db)
        writer.isolation_level = None
        writer.execute("BEGIN EXCLUSIVE")
        try:
            error: RuntimeCorpusError | None = None
            corpus: RuntimeCorpus | None = None
            try:
                corpus = RuntimeCorpus(self.db)
                corpus.unigram("to")
            except RuntimeCorpusError as exc:
                error = exc
                if corpus is not None:
                    corpus.close()
            if error is None:
                self.fail("expected locked failure")
            self.assertEqual(error.reason, REASON_LOCKED)
        finally:
            writer.execute("ROLLBACK")
            writer.close()
        corpus = RuntimeCorpus(self.db)
        self.assertEqual(corpus.unigram("to").count, 100)
        corpus.close()
        self.assertEqual(_index_state(self.root, self.db), self.before)

    def test_incompatible_schema_label_unchanged(self) -> None:
        missing = self.root / "missing.sqlite"
        connection = sqlite3.connect(missing)
        connection.executescript(
            """
            CREATE TABLE unigram (word TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE bigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE trigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
            """
        )
        connection.commit()
        connection.close()
        with self.assertRaises(RuntimeCorpusError) as caught:
            RuntimeCorpus(missing)
        self.assertEqual(caught.exception.reason, REASON_INCOMPATIBLE)

    def test_invalid_count_label_unchanged(self) -> None:
        bad = self.root / "badcount.sqlite"
        connection = sqlite3.connect(bad)
        connection.executescript(
            """
            CREATE TABLE unigram (word TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE bigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE trigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
            CREATE TABLE middle (left_word TEXT, right_word TEXT, middle_word TEXT, count INTEGER);
            INSERT INTO unigram VALUES ('neg', -5);
            """
        )
        connection.commit()
        connection.close()
        corpus = RuntimeCorpus(bad)
        try:
            with self.assertRaises(RuntimeCorpusError) as caught:
                corpus.unigram("neg")
            self.assertEqual(caught.exception.reason, REASON_INVALID_COUNT)
        finally:
            corpus.close()

    def test_unavailable_label_for_absent_path(self) -> None:
        with self.assertRaises(RuntimeCorpusError) as caught:
            RuntimeCorpus(self.root / "absent.sqlite")
        self.assertEqual(caught.exception.reason, REASON_UNAVAILABLE)

    def test_caller_control_identity_at_data_boundary(self) -> None:
        # A rigged budget state whose first callback read raises
        # MemoryError: the product handler must return nonzero (never
        # raise into C), preserve the exact identity, and the adapter
        # must re-raise it after owned cleanup (probe
        # 024-native-callback-fault-and-range-observation.json).
        control = MemoryError("simulated-caller-control")
        fd_before = _fd_count()
        corpus = RuntimeCorpus(self.db, progress_interval=30)
        try:
            rigged = _RiggedState(corpus._budget.limits, control)
            corpus._budget = rigged
            corpus.connection.set_progress_handler(
                make_progress_handler(rigged), 30
            )
            try:
                corpus.alternatives("a", "b")  # 500-row scan fires a callback
                self.fail("expected the preserved control")
            except BaseException as exc:  # noqa: BLE001 - identity check
                self.assertIs(exc, control)
            self.assertTrue(rigged.exhausted)
            self.assertIsNone(rigged.pending_control)
        finally:
            corpus.close()
        self.assertLessEqual(_fd_count(), fd_before)
        self.assertEqual(_index_state(self.root, self.db), self.before)
        fresh = RuntimeCorpus(self.db)
        try:
            self.assertEqual(fresh.unigram("to").count, 100)
        finally:
            fresh.close()

    def test_caller_control_identity_at_constructor_boundary(self) -> None:
        # The rigged budget class is installed for the construction
        # itself: the first schema statement's callback raises
        # KeyboardInterrupt, the real product handler preserves it,
        # and the constructor re-raises the exact identity after
        # owned connection cleanup.
        control = KeyboardInterrupt()
        fd_before = _fd_count()

        def rigged_factory(limits: EvidenceLimits) -> _RiggedState:
            state = _RiggedState(limits, control)
            return state

        with mock.patch.object(
            runtime_corpus, "EvidenceBudgetState", rigged_factory
        ):
            try:
                with self.assertRaises(BaseException) as caught:
                    RuntimeCorpus(self.db, progress_interval=1)
                self.assertIs(caught.exception, control)
            finally:
                self.assertLessEqual(_fd_count(), fd_before)
        self.assertIs(
            # module attribute access is the strict-mypy attr-defined error
            # on a non-reexported name; getattr is intentional here.
            getattr(runtime_corpus, "EvidenceBudgetState"),  # noqa: B009
            EvidenceBudgetState,
        )
        corpus = RuntimeCorpus(self.db)
        try:
            self.assertEqual(corpus.unigram("to").count, 100)
        finally:
            corpus.close()


class _RiggedState(EvidenceBudgetState):
    """Test-only budget whose first callback read raises injected control."""

    def __init__(self, limits: EvidenceLimits, control: BaseException | None) -> None:
        super().__init__(limits)
        self._rigged_control = control
        self._rigged_armed = True
        self._raw_callbacks = 0

    @property
    def callbacks(self) -> int:
        if self._rigged_armed:
            self._rigged_armed = False
            control = self._rigged_control
            if control is not None:
                raise control
        return self._raw_callbacks

    @callbacks.setter
    def callbacks(self, value: int) -> None:
        self._raw_callbacks = value


class EngineEarlyLateTests(unittest.TestCase):
    """T7: real engine boundaries; early 0 calls, late 1 call, edit discarded."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _evidence_db(self.root)
        self.reviewer = _StubReviewer()
        self.engine = proxy.RepairEngine(self.db, self.reviewer, pandoc=_real_spec())

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _track_corpora(self) -> list[RuntimeCorpus]:
        captured: list[RuntimeCorpus] = []
        real_ctor = RuntimeCorpus

        def tracked(path: str | Path) -> RuntimeCorpus:
            corpus = real_ctor(path)
            captured.append(corpus)
            return corpus

        mock.patch.object(proxy, "RuntimeCorpus", tracked).start()
        self.addCleanup(mock.patch.stopall)
        return captured

    def test_early_exhaustion_exact_original_zero_calls(self) -> None:
        captured = self._track_corpora()
        text = _absent_words(_EARLY_N)  # N distinct absent letter-tokens
        self.engine.begin_request()
        repaired = self.engine.repair(text)
        self.assertEqual(repaired, text)
        self.assertEqual(self.reviewer.calls, 0)
        [detail] = self.engine.take_details()
        self.assertEqual(detail["repaired"], text)
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 0)
        self.assertEqual(review["usage"], "unknown")
        failure = _sub_mapping(detail, "evidence_failure")
        self.assertEqual(
            failure, {"reason": REASON_BUDGET_EXCEEDED, "stage": "early"}
        )
        [corpus] = captured
        self.assertTrue(corpus._budget.exhausted)
        self.assertEqual(
            corpus._budget.statements, config.RUNTIME_EVIDENCE_MAX_STATEMENTS
        )
        # No data row was ever returned: only the schema metadata rows.
        self.assertEqual(corpus._budget.rows_total, _SCHEMA_META_ROWS)

    def test_late_exhaustion_one_call_usage_retained_edit_discarded(self) -> None:
        captured = self._track_corpora()
        events, tracked = _tracked_accept_events(_real_accept)
        with mock.patch.object(proxy, "accept", tracked):
            text = _absent_words(_LATE_N)
            self.engine.begin_request()
            repaired = self.engine.repair(text)
        # The whole optional pass aborted: the exact original is
        # delivered and the earlier accepted edit disappears.
        self.assertEqual(repaired, text)
        self.assertEqual(self.reviewer.calls, 1)
        [detail] = self.engine.take_details()
        self.assertEqual(detail["repaired"], text)
        candidates = detail["candidates"]
        if not isinstance(candidates, list):
            self.fail("candidates is not a list")
        self.assertEqual(len(candidates), 4)
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 1)
        self.assertEqual(
            review["usage"],
            {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        )
        failure = _sub_mapping(detail, "evidence_failure")
        self.assertEqual(
            failure, {"reason": REASON_BUDGET_EXCEEDED, "stage": "late"}
        )
        decisions = detail["reviewer_decisions"]
        if not isinstance(decisions, list):
            self.fail("decisions is not a list")
        self.assertEqual(len(decisions), 4)
        for item in decisions:
            if not isinstance(item, dict):
                self.fail("decision is not a mapping")
            acceptance = _sub_mapping(item, "acceptance")
            self.assertFalse(acceptance["accepted"])
            self.assertEqual(acceptance["reason"], "evidence-abort")
        # R7/R10: the SAME late pass actually accepted a prior
        # proposal (call-through at acceptance, nothing faked) before
        # the subsequent budget failure aborted the whole pass.
        self.assertEqual(events, ["ACCEPTED", REASON_BUDGET_EXCEEDED])
        [corpus] = captured
        # Schema 5 + detection 65529 + exactly 2 accepted-starts = cap.
        self.assertEqual(
            corpus._budget.statements, config.RUNTIME_EVIDENCE_MAX_STATEMENTS
        )
        self.assertTrue(corpus._budget.exhausted)
        self.assertEqual(corpus._budget.rows_total, _SCHEMA_META_ROWS + 2)
        # Statement/row boundaries, not the progress budget, drove this.
        self.assertLess(
            corpus._budget.callbacks, config.RUNTIME_EVIDENCE_MAX_PROGRESS_CALLBACKS
        )

    def test_late_exhaustion_unknown_usage_stays_unknown(self) -> None:
        # R7/R10: the same late pass with a reviewer that reports no
        # usage: the original usage stays unknown, never an invented
        # zero, with the same actual accept-then-abort lifecycle.
        self.reviewer = _StubReviewer(usage=False)
        self.engine = proxy.RepairEngine(
            self.db, self.reviewer, pandoc=_real_spec()
        )
        captured = self._track_corpora()
        events, tracked = _tracked_accept_events(_real_accept)
        with mock.patch.object(proxy, "accept", tracked):
            text = _absent_words(_LATE_N)
            self.engine.begin_request()
            repaired = self.engine.repair(text)
        self.assertEqual(repaired, text)
        self.assertEqual(self.reviewer.calls, 1)
        [detail] = self.engine.take_details()
        self.assertEqual(detail["repaired"], text)
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 1)
        self.assertEqual(review["usage"], "unknown")
        failure = _sub_mapping(detail, "evidence_failure")
        self.assertEqual(
            failure, {"reason": REASON_BUDGET_EXCEEDED, "stage": "late"}
        )
        decisions = detail["reviewer_decisions"]
        if not isinstance(decisions, list):
            self.fail("decisions is not a list")
        for item in decisions:
            if not isinstance(item, dict):
                self.fail("decision is not a mapping")
            acceptance = _sub_mapping(item, "acceptance")
            self.assertFalse(acceptance["accepted"])
            self.assertEqual(acceptance["reason"], "evidence-abort")
        self.assertEqual(events, ["ACCEPTED", REASON_BUDGET_EXCEEDED])
        [corpus] = captured
        self.assertEqual(
            corpus._budget.statements, config.RUNTIME_EVIDENCE_MAX_STATEMENTS
        )
        self.assertTrue(corpus._budget.exhausted)

    def test_fresh_request_works_after_exhaustion(self) -> None:
        captured = self._track_corpora()
        self.engine.begin_request()
        self.assertEqual(self.engine.repair(_absent_words(_EARLY_N)), _absent_words(_EARLY_N))
        self.engine.begin_request()
        repaired = self.engine.repair(_HEALTHY)
        self.assertEqual(repaired, _HEALTHY)
        self.assertEqual(self.reviewer.calls, 0)
        self.assertEqual(len(captured), 2)
        # The second request gets a fresh budget that completes fully:
        # 8 tokens cost 34 starts and return 18 data rows on this lexicon.
        second = captured[1]
        self.assertFalse(second._budget.exhausted)
        self.assertEqual(second._budget.statements, _SCHEMA_STATEMENTS + 34)
        self.assertEqual(second._budget.rows_total, _SCHEMA_META_ROWS + 18)
        [detail] = self.engine.take_details()
        self.assertNotIn("evidence_failure", detail)

    def test_under_budget_positive_control_edit_applies(self) -> None:
        # Same corpus/text shape/proposal under budget: the leftmost
        # one-word replacement is genuinely accepted (the exact bigram
        # "repla aab" exists), proving the late case's discarded edit
        # was real.
        captured = self._track_corpora()
        text = _absent_words(10)
        self.engine.begin_request()
        repaired = self.engine.repair(text)
        self.assertEqual(repaired, "repla" + text[len("aaa"):])
        self.assertEqual(self.reviewer.calls, 1)
        [detail] = self.engine.take_details()
        self.assertNotIn("evidence_failure", detail)
        decisions = detail["reviewer_decisions"]
        if not isinstance(decisions, list):
            self.fail("decisions is not a list")
        accepted = [
            _sub_mapping(item, "acceptance")
            for item in decisions
            if isinstance(item, dict)
        ]
        self.assertEqual(
            sum(1 for a in accepted if a["accepted"]), 1
        )
        [corpus] = captured
        self.assertFalse(corpus._budget.exhausted)


class ProxyRoundTripTests(unittest.TestCase):
    """T8: full real proxy/Pandoc/RO-SQLite/review-worker HTTP round trip.

    Only the main upstream and the review endpoint are synthetic
    (owned loopback-0 servers); the proxy, engine, corpus, Pandoc and
    the real ResponsesReviewer protocol client are all actual code.
    The proxy handler consumes engine details after each repair, so
    the operator observation seam (usage_observer) is the primary
    evidence, with a bounded call-through recording patch for the
    detail-level stage/decision assertions.
    """

    def setUp(self) -> None:
        self.harness = _Harness(usage_observer=self._observe)
        self.records: list[dict[str, object]] = []
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _evidence_db(self.root)
        # Point the real engine at the synthetic-scale index.
        self.harness.engine.index = self.db

    def tearDown(self) -> None:
        self.harness.close()
        self.temp.cleanup()

    def _observe(self, record: dict[str, object]) -> None:
        self.records.append(record)

    def _post(
        self,
        answer: str,
        *,
        proposals: int = 4,
        usage: bool = True,
        record: bool = False,
    ) -> tuple[int, bytes]:
        props = [
            {
                "id": f"t{i}",
                "keep": False,
                "replacement": "repla",
                "needs_wider_edit": False,
            }
            for i in range(proposals)
        ]
        _MainUpstream.status = 200
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = _json_completed(answer=answer)
        if usage:
            _FakeUpstream.payload = _review_payload(
                props, usage={"input_tokens": 10, "output_tokens": 20, "total_tokens": 30}
            )
        else:
            _FakeUpstream.payload = _review_payload(props)
        self.captured_details: list[dict[str, object]] = []
        if record:
            real_take = self.harness.engine.take_details

            def recording_take() -> list[dict[str, object]]:
                details = real_take()
                self.captured_details = list(details)
                return details

            patcher = mock.patch.object(
                self.harness.engine, "take_details", recording_take
            )
            patcher.start()
            self.addCleanup(patcher.stop)
        return self.harness.post(_contract_body(False, input_text="hi"))

    def test_under_budget_control_exact_answer_zero_calls(self) -> None:
        status, payload = self._post(_HEALTHY, proposals=0)
        self.assertEqual(status, 200)
        self.assertEqual(_envelope_text(payload), _HEALTHY)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(
            self.records[-1], {"review_calls": 0, "reviewer_usage": "unknown"}
        )

    def test_early_exhaustion_exact_original_zero_calls(self) -> None:
        answer = _absent_words(_EARLY_N)
        status, payload = self._post(answer, record=True)
        self.assertEqual(status, 200)
        self.assertEqual(_envelope_text(payload), answer)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(
            self.records[-1], {"review_calls": 0, "reviewer_usage": "unknown"}
        )
        [detail] = self.captured_details
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 0)
        self.assertEqual(review["usage"], "unknown")
        failure = _sub_mapping(detail, "evidence_failure")
        self.assertEqual(
            failure, {"reason": REASON_BUDGET_EXCEEDED, "stage": "early"}
        )

    def test_late_exhaustion_exact_original_one_call_usage_retained(self) -> None:
        answer = _absent_words(_LATE_N)
        status, payload = self._post(answer, record=True)
        self.assertEqual(status, 200)
        self.assertEqual(_envelope_text(payload), answer)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertEqual(
            self.records[-1],
            {
                "review_calls": 1,
                "reviewer_usage": {
                    "input_tokens": 10,
                    "output_tokens": 20,
                    "total_tokens": 30,
                },
            },
        )
        [detail] = self.captured_details
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 1)
        failure = _sub_mapping(detail, "evidence_failure")
        self.assertEqual(
            failure, {"reason": REASON_BUDGET_EXCEEDED, "stage": "late"}
        )
        decisions = detail["reviewer_decisions"]
        if not isinstance(decisions, list):
            self.fail("decisions is not a list")
        for item in decisions:
            if not isinstance(item, dict):
                self.fail("decision is not a mapping")
            acceptance = _sub_mapping(item, "acceptance")
            self.assertFalse(acceptance["accepted"])
            self.assertEqual(acceptance["reason"], "evidence-abort")

    def test_late_exhaustion_unknown_usage_proxy_round_trip(self) -> None:
        # R7/R10 over the full proxy path: unknown usage stays
        # unknown in both the operator observation and the bounded
        # detail capture, never an invented zero.
        answer = _absent_words(_LATE_N)
        status, payload = self._post(answer, record=True, usage=False)
        self.assertEqual(status, 200)
        self.assertEqual(_envelope_text(payload), answer)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertEqual(
            self.records[-1], {"review_calls": 1, "reviewer_usage": "unknown"}
        )
        [detail] = self.captured_details
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 1)
        self.assertEqual(review["usage"], "unknown")
        failure = _sub_mapping(detail, "evidence_failure")
        self.assertEqual(
            failure, {"reason": REASON_BUDGET_EXCEEDED, "stage": "late"}
        )

    def test_malformed_main_is_main_error_not_fallback_success(self) -> None:
        _MainUpstream.status = 200
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = b'{"object":"response","broken":'
        _FakeUpstream.payload = _review_payload([_prop("t0")])
        status, payload = self.harness.post(_contract_body(False, input_text="hi"))
        self.assertEqual(status, 502)
        self.assertEqual(_FakeUpstream.recorded, [])
        # The engine never ran a repair on a malformed main.
        self.assertEqual(self.harness.engine.take_details(), [])

    def test_incomplete_main_bypasses_repair_with_zero_calls(self) -> None:
        source = _json_completed(answer=_HEALTHY, status="in_progress")
        _MainUpstream.status = 200
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = source
        _FakeUpstream.payload = _review_payload([_prop("t0")])
        status, payload = self.harness.post(_contract_body(False, input_text="hi"))
        # Raw unchanged main bytes, zero review calls: never a
        # repair/fallback success.
        self.assertEqual(status, 200)
        self.assertEqual(payload, source)
        self.assertEqual(_FakeUpstream.recorded, [])


class _AcceptanceLike(Protocol):
    """Structural view of a real accept decision (call-through only).

    ``accepted`` is a read-only member: the real decision is a frozen
    dataclass, so a settable-variable protocol member would not match
    it.
    """

    @property
    def accepted(self) -> bool: ...


def _tracked_accept_events(
    real: Callable[..., _AcceptanceLike],
) -> tuple[list[str], Callable[..., object]]:
    """Call-through observation of real accept decisions (R7/R10).

    Wraps the real repair.accept at the proxy module reference: every
    real decision is recorded as it happens and returned unchanged,
    and a real RuntimeCorpusError is recorded with its exact reason
    and re-raised unchanged. No acceptance, corpus or query is faked.
    """
    events: list[str] = []

    def tracked(*args: object, **kwargs: object) -> object:
        try:
            decision = real(*args, **kwargs)
        except RuntimeCorpusError as exc:
            events.append(exc.reason)
            raise
        events.append("ACCEPTED" if decision.accepted else "REJECTED")
        return decision

    return events, tracked


class _FaultCursor:
    """Test-only delegate over a real native cursor with at most one
    faulting fetch and at most one faulting close (each fires only
    after the real native call completes).  Every fault that actually
    fires is recorded in ``fault_events`` so a test can assert which
    boundary faulted and that no other fault fired."""

    fault_events: list[tuple[str, BaseException]] = []

    def __init__(
        self,
        real: sqlite3.Cursor,
        fetch_fault: BaseException | None,
        close_fault: BaseException | None,
    ) -> None:
        self._real = real
        self._fetch_fault = fetch_fault
        self._close_fault = close_fault
        self._fetch_armed = fetch_fault is not None
        self._close_armed = close_fault is not None

    def fetchmany(self, size: int) -> list[tuple[object, ...]]:
        rows = self._real.fetchmany(size)
        if self._fetch_armed:
            self._fetch_armed = False
            fault = self._fetch_fault
            if fault is not None:
                self.fault_events.append(("fetchmany", fault))
                raise fault
        return rows

    def close(self) -> None:
        self._real.close()
        if self._close_armed:
            self._close_armed = False
            fault = self._close_fault
            if fault is not None:
                self.fault_events.append(("close", fault))
                raise fault

    def __getattr__(self, name: str) -> object:
        return getattr(self._real, name)


class _FaultConnection(sqlite3.Connection):
    """Test-only real native connection with one injected fault.

    The fault fires at exactly one named boundary (hook install, the
    first execute AFTER the real native statement has executed, the
    first fetch AFTER the real native fetch, or the removal of an
    armed handler); every other call is the real native call.  The
    product calls ``connection.execute`` directly (it never goes
    through ``connection.cursor``), so the execute/fetch faults are
    installed on ``execute`` at that actual native boundary.
    """

    boundary: str = "none"
    injected: BaseException | None = RuntimeError("unfaulted")
    close_fault: BaseException | None = None
    removal_armed = False
    execute_armed = False
    fetch_armed = False
    cursor_armed = False
    executed_cursors: list[sqlite3.Cursor] = []

    def close(self) -> None:
        super().close()
        if self.close_fault is not None:
            fault = self.close_fault
            self.close_fault = None
            _FaultCursor.fault_events.append(("connection-close", fault))
            raise fault

    def set_progress_handler(
        self, callback: Callable[[], int | None] | None, n: int
    ) -> None:
        if self.boundary == "remove" and callback is None and self.removal_armed:
            self.removal_armed = False
            if self.injected is not None:
                raise self.injected
        if (
            self.boundary == "install"
            and callback is not None
            and self.injected is not None
        ):
            raise self.injected
        super().set_progress_handler(callback, n)

    def execute(self, sql: str, parameters: object = ()) -> sqlite3.Cursor:
        # Every real caller (the product's _execute and this test's
        # closed-connection probe) passes a parameter tuple or the
        # default; the cast documents that contract at the native call.
        params = cast("tuple[object, ...]", parameters)
        if self.boundary == "execute" and self.execute_armed:
            self.execute_armed = False
            # The real native statement runs to completion (its cursor
            # is allocated and retained for the unusability check); the
            # fault is injected only after that actual native work.
            real = super().execute(sql, params)
            self.executed_cursors.append(real)
            if self.injected is not None:
                raise self.injected
        if self.boundary == "fetch" and self.fetch_armed:
            self.fetch_armed = False
            real = super().execute(sql, params)
            # One targeted cast: _FaultCursor is a test-only delegate
            # over the real native cursor (all other attributes pass
            # through).
            return cast("sqlite3.Cursor", _FaultCursor(real, self.injected, None))
        if self.boundary == "cursor" and self.cursor_armed:
            self.cursor_armed = False
            real = super().execute(sql, params)
            self.executed_cursors.append(real)
            close_fault = self.close_fault
            self.close_fault = None
            # One targeted cast: _FaultCursor is a test-only delegate
            # over the real native cursor (all other attributes pass
            # through).
            return cast(
                "sqlite3.Cursor", _FaultCursor(real, self.injected, close_fault)
            )
        return super().execute(sql, params)


class NativeTeardownBoundaryTests(unittest.TestCase):
    """R6: real native connection/cursor fault boundaries.

    One focused case per boundary - hook install, SQL execute/prepare,
    fetch, callback removal, and the cursor-close boundary on the real
    data query - on the real read-only synthetic database, with the
    fault injected at the named native boundary.  The latter cases
    also cover the caller-control priority policy: an ordinary pending
    body exception must not swallow a later cleanup caller control, an
    in-flight caller control keeps its exact identity over a later
    cursor/connection close failure (ordinary or a distinct control),
    the first cleanup control wins over a later one, a clean normal
    close still propagates a new caller control, and an ALREADY
    HANDLED caller control in an outer frame (ambient exception
    context) never counts as the current operation's propagating
    error.  The product
    lifecycle under test is the caller-owned one: the real
    constructor and the context manager plus the documented close();
    arbitrary direct-method ownership sequences beyond that lifecycle
    are not claimed as product ownership. Every case verifies the
    product cleanup (connection closed) BEFORE this test's own
    cleanup runs, the exact injected or original exception identity,
    and a next healthy instance.
    """

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _evidence_db(self.root)
        self.before = _index_state(self.root, self.db)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _fault_connect(
        self,
        boundary: str,
        injected: BaseException | None,
        close_fault: BaseException | None = None,
    ) -> tuple[
        Callable[[str, bool, float], sqlite3.Connection],
        list[_FaultConnection],
    ]:
        _FaultConnection.boundary = boundary
        _FaultConnection.injected = injected
        _FaultConnection.close_fault = close_fault
        _FaultConnection.removal_armed = False
        _FaultConnection.execute_armed = boundary == "execute"
        _FaultConnection.fetch_armed = boundary == "fetch"
        _FaultConnection.cursor_armed = boundary == "cursor"
        _FaultConnection.executed_cursors = []
        _FaultCursor.fault_events = []
        original_connect = sqlite3.connect
        connections: list[_FaultConnection] = []

        def connect(
            database: str,
            uri: bool = False,
            timeout: float = 5.0,
        ) -> sqlite3.Connection:
            native = original_connect(
                database, uri=uri, timeout=timeout, factory=_FaultConnection
            )
            connections.append(native)
            return native

        return connect, connections

    def _assert_closed(self, native: sqlite3.Connection) -> None:
        # Product cleanup is observed BEFORE this test's own cleanup
        # (tearDown) runs.
        with self.assertRaises(sqlite3.ProgrammingError):
            native.execute("SELECT 1")

    def _next_healthy(self) -> None:
        corpus = RuntimeCorpus(self.db)
        try:
            self.assertEqual(corpus.unigram("to").count, 100)
            self.assertFalse(corpus._budget.exhausted)
        finally:
            corpus.close()
        self.assertEqual(_index_state(self.root, self.db), self.before)

    def test_hook_install_fault_preserves_identity_and_closes(self) -> None:
        injected = MemoryError("controlled-install")
        connect, connections = self._fault_connect("install", injected)
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(MemoryError) as caught:
            RuntimeCorpus(self.db)
        self.assertIs(caught.exception, injected)
        [native] = connections
        self._assert_closed(native)
        self._next_healthy()

    def test_sql_execute_fault_preserves_identity_and_closes(self) -> None:
        injected = KeyboardInterrupt("controlled-execute")
        connect, connections = self._fault_connect("execute", injected)
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(KeyboardInterrupt) as caught:
            RuntimeCorpus(self.db)
        self.assertIs(caught.exception, injected)
        [native] = connections
        self._assert_closed(native)
        # The real native statement had run: the exact cursor that was
        # allocated is unusable after the product cleanup.
        [real_cursor] = native.executed_cursors
        with self.assertRaises(sqlite3.ProgrammingError):
            real_cursor.fetchone()
        self._next_healthy()

    def test_fetch_fault_preserves_identity_and_closes(self) -> None:
        injected = MemoryError("controlled-fetch")
        connect, connections = self._fault_connect("fetch", injected)
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(MemoryError) as caught:
            RuntimeCorpus(self.db)
        self.assertIs(caught.exception, injected)
        [native] = connections
        self._assert_closed(native)
        self._next_healthy()

    def test_removal_memory_during_body_control_keeps_original_identity(self) -> None:
        # A MemoryError removing the handler while a distinct body
        # KeyboardInterrupt is propagating: the original body control
        # keeps its exact identity and the connection is still closed.
        removal = MemoryError("controlled-removal")
        body = KeyboardInterrupt("controlled-body")
        connect, connections = self._fault_connect("remove", removal)
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(KeyboardInterrupt) as caught, RuntimeCorpus(self.db) as corpus:
            self.assertEqual(corpus.unigram("to").count, 100)
            [conn] = connections
            conn.removal_armed = True
            raise body
        self.assertIs(caught.exception, body)
        [native] = connections
        self._assert_closed(native)
        self._next_healthy()

    def test_removal_keyboard_on_normal_close_closes_then_raises(self) -> None:
        # A KeyboardInterrupt removing the handler on a normal close
        # is still raised (normal-close exception semantics), but only
        # after the close attempt.
        injected = KeyboardInterrupt("controlled-removal")
        connect, connections = self._fault_connect("remove", injected)
        with mock.patch.object(sqlite3, "connect", connect):
            corpus = RuntimeCorpus(self.db)
            self.assertEqual(corpus.unigram("to").count, 100)
            [conn] = connections
            conn.removal_armed = True
            with self.assertRaises(KeyboardInterrupt) as caught:
                corpus.close()
        self.assertIs(caught.exception, injected)
        [native] = connections
        self._assert_closed(native)
        self._next_healthy()

    def test_ordinary_body_removal_keyboard_control_wins(self) -> None:
        # An ORDINARY body ValueError must not swallow a later cleanup
        # caller control: the removal KeyboardInterrupt propagates with
        # its exact identity after the close attempt.
        injected = KeyboardInterrupt("controlled-removal")
        body = ValueError("controlled-body")
        connect, connections = self._fault_connect("remove", injected)
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(KeyboardInterrupt) as caught, RuntimeCorpus(self.db) as corpus:
            self.assertEqual(corpus.unigram("to").count, 100)
            [conn] = connections
            conn.removal_armed = True
            raise body
        self.assertIs(caught.exception, injected)
        [native] = connections
        self._assert_closed(native)
        self._next_healthy()

    def test_ordinary_body_removal_memory_control_wins(self) -> None:
        # Same priority with a MemoryError cleanup control: although
        # MemoryError subclasses Exception, it is caller control here
        # and must propagate over the ordinary body ValueError.
        injected = MemoryError("controlled-removal")
        body = ValueError("controlled-body")
        connect, connections = self._fault_connect("remove", injected)
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(MemoryError) as caught, RuntimeCorpus(self.db) as corpus:
            self.assertEqual(corpus.unigram("to").count, 100)
            [conn] = connections
            conn.removal_armed = True
            raise body
        self.assertIs(caught.exception, injected)
        [native] = connections
        self._assert_closed(native)
        self._next_healthy()

    def test_cursor_fetch_control_preserved_over_close_secondary_control(
        self,
    ) -> None:
        # Real data-query cursor: the fetch raises the primary
        # KeyboardInterrupt after the real native fetch; the real close
        # REALLY CLOSES and then raises a distinct secondary
        # MemoryError. The primary control keeps its exact identity -
        # the data-method finally must not replace it - and the
        # context teardown still closes the connection.
        injected = KeyboardInterrupt("controlled-fetch")
        secondary = MemoryError("controlled-cursor-close")
        connect, connections = self._fault_connect(
            "cursor", injected, close_fault=secondary
        )
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(KeyboardInterrupt) as caught, RuntimeCorpus(self.db) as corpus:
            corpus.unigram("to")
        self.assertIs(caught.exception, injected)
        [native] = connections
        self._assert_closed(native)
        [real_cursor] = native.executed_cursors
        with self.assertRaises(sqlite3.ProgrammingError):
            real_cursor.fetchone()
        self._next_healthy()

    def test_cursor_fetch_control_preserved_over_close_ordinary_error(
        self,
    ) -> None:
        # Same data-query boundary with an ordinary secondary close
        # error: the primary fetch control still keeps its exact
        # identity over the ordinary close failure.
        injected = KeyboardInterrupt("controlled-fetch")
        secondary = ValueError("controlled-cursor-close")
        connect, connections = self._fault_connect(
            "cursor", injected, close_fault=secondary
        )
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(KeyboardInterrupt) as caught, RuntimeCorpus(self.db) as corpus:
            corpus.unigram("to")
        self.assertIs(caught.exception, injected)
        [native] = connections
        self._assert_closed(native)
        [real_cursor] = native.executed_cursors
        with self.assertRaises(sqlite3.ProgrammingError):
            real_cursor.fetchone()
        self._next_healthy()

    def test_first_cleanup_control_wins_over_later_close_control(self) -> None:
        # Removal raises a KeyboardInterrupt and the connection close
        # then raises a distinct MemoryError while an ordinary body
        # ValueError is pending: the FIRST cleanup caller control
        # (the removal one) propagates, the later one is not delivered.
        removal = KeyboardInterrupt("controlled-removal")
        conn_close = MemoryError("controlled-connection-close")
        body = ValueError("controlled-body")
        connect, connections = self._fault_connect(
            "remove", removal, close_fault=conn_close
        )
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(KeyboardInterrupt) as caught, RuntimeCorpus(self.db) as corpus:
            self.assertEqual(corpus.unigram("to").count, 100)
            [conn] = connections
            conn.removal_armed = True
            raise body
        self.assertIs(caught.exception, removal)
        [native] = connections
        self._assert_closed(native)
        self._next_healthy()

    def test_normal_close_propagates_connection_close_control(self) -> None:
        # A clean normal close() whose real connection close REALLY
        # CLOSES and then raises a MemoryError: with no pending caller
        # control, the new caller control propagates from close() with
        # its exact identity.
        close_control = MemoryError("controlled-connection-close")
        connect, connections = self._fault_connect(
            "none", RuntimeError("unused"), close_fault=close_control
        )
        with mock.patch.object(sqlite3, "connect", connect):
            corpus = RuntimeCorpus(self.db)
            self.assertEqual(corpus.unigram("to").count, 100)
            with self.assertRaises(MemoryError) as caught:
                corpus.close()
        self.assertIs(caught.exception, close_control)
        [native] = connections
        self._assert_closed(native)
        self._next_healthy()

    def test_ambient_handled_control_does_not_swallow_fresh_close_control(
        self,
    ) -> None:
        # The caller ALREADY HANDLES a KeyboardInterrupt in an outer
        # frame (ambient exception context); while that handler runs,
        # a fresh, otherwise healthy construction performs its real
        # native schema fetch with NO primary fetch fault, then the
        # first real native schema cursor REALLY CLOSES and raises a
        # NEW MemoryError at close.  The already-handled ancestor must
        # not be mistaken for the current operation's propagating
        # error: the fresh close control propagates with its exact
        # identity, exactly the intended close fault fired, and the
        # owned connection is still closed.
        ambient = KeyboardInterrupt("already-handled-ancestor")
        fresh = MemoryError("fresh-schema-close")
        connect, connections = self._fault_connect("cursor", None, fresh)
        with mock.patch.object(sqlite3, "connect", connect), \
                self.assertRaises(MemoryError) as caught:
            try:
                raise ambient
            except KeyboardInterrupt:
                with RuntimeCorpus(self.db) as corpus:
                    corpus.unigram("to")
        self.assertIs(caught.exception, fresh)
        self.assertEqual(_FaultCursor.fault_events, [("close", fresh)])
        [native] = connections
        self._assert_closed(native)
        self._next_healthy()


if __name__ == "__main__":
    unittest.main()
