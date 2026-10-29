"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Finite analysis-eligibility boundary tests (order 025-a, T1-T8).

Real boundaries under test: the real versioned config defaults, the
real ConceptProxy constructor (before any bind allocation), the real
RepairEngine repair entry (before resolve/protect/map/residual/
tokenize/index/reviewer work), the real Pandoc subprocess, the real
read-only SQLite evidence adapter and, for the round-trip class, the
real ResponsesReviewer over owned loopback-0 HTTP.  Only the main
upstream, the review endpoint and (for the direct-engine classes) the
injected reviewer are synthetic fakes upstream of those boundaries;
negative no-work claims use transparent observers that delegate to
the actual code if invoked.  Missing qualified Pandoc is a failure,
never a skip.  No live model, corpus, network or quality claim
(order 025-a, requirements 5 and 8).
"""

from __future__ import annotations

import http.client
import json
import os
import socket
import sys
import tempfile
import threading
import unittest
from collections.abc import Mapping
from http.server import HTTPServer
from pathlib import Path
from typing import Protocol, cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import analysis_policy  # noqa: E402
import config  # noqa: E402
import proxy  # noqa: E402
from batch_review import BatchResult, BatchTarget  # noqa: E402
from pandoc_protection import (  # noqa: E402
    PandocSpec,
    ProtectionOutcome,
    protect_with_pandoc,
)
from qwen_client import ResponsesReviewer  # noqa: E402
from runtime_corpus import RuntimeCorpus  # noqa: E402
from tests.test_evidence_budget import (  # noqa: E402
    _HEALTHY,
    _absent_words,
    _evidence_db,
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
    _tc_delta,
    _tc_item_done,
    _tc_part_done,
    _tc_raw,
)

# One finite synthetic-scale useful-repair answer (39 code points /
# 39 UTF-8 bytes over the tiny owned lexicon): the first absent word
# "aaa" is the leftmost accepted one-word replacement "repla"
# (the exact bigram "repla aab" exists in the fixture).
_USEFUL = _absent_words(10)
_USEFUL_REPAIRED = "repla" + _USEFUL[len("aaa") :]

# Four-byte UTF-8 code point used for the byte axis.
_E4 = "\U0001F600"

# Nine invalid values per field (order 025-a, T1): bool, None, zero,
# negative, float, nonfinite float and string are all rejected.
_INVALID_VALUES = (
    True,
    False,
    None,
    0,
    -1,
    1.0,
    float("inf"),
    float("nan"),
    "32768",
)


def _require_qualified_pandoc() -> PandocSpec:
    # The installed pinned Pandoc via explicit CONCEPT_PANDOC; PATH
    # substitution is not allowed when the qualification is missing,
    # and a missing qualified Pandoc is a failure, never a skip.
    path = os.environ.get(config.PANDOC_ENV_VAR, "").strip()
    if not path or not os.path.isfile(path) or not os.access(path, os.X_OK):
        raise AssertionError(
            "qualified Pandoc via CONCEPT_PANDOC is required; a missing "
            "Pandoc is a failure, never a skip"
        )
    return PandocSpec(binary=path)


class _NoReview:
    """Reviewer that fails loudly if the gate ever reaches review."""

    def __init__(self) -> None:
        self.calls = 0

    def review_batch(
        self, sentence: str, targets: tuple[BatchTarget, ...]
    ) -> BatchResult:
        self.calls += 1
        raise AssertionError("reviewer must not be called")


class _ObservedEngine:
    """Real engine plus transparent call-through observers.

    The observers delegate to the actual protect/corpus code if
    invoked; a bypass must therefore leave every list empty.  The
    reviewer is the designed injection seam (A-SEAM-01) and fails if
    called.
    """

    def __init__(self, index: Path, pandoc: PandocSpec) -> None:
        self.reviewer = _NoReview()
        self.engine = proxy.RepairEngine(index, self.reviewer, pandoc=pandoc)
        self.protect_calls: list[int] = []
        self.corpus_attempts: list[int] = []
        real_protect = protect_with_pandoc
        real_ctor = RuntimeCorpus

        def observed_protect(spec: PandocSpec, text: str) -> ProtectionOutcome:
            self.protect_calls.append(1)
            return real_protect(spec, text)

        def observed_ctor(index: str | Path) -> RuntimeCorpus:
            self.corpus_attempts.append(1)
            return real_ctor(index)

        self._patches = (
            mock.patch.object(proxy, "protect_with_pandoc", observed_protect),
            mock.patch.object(proxy, "RuntimeCorpus", observed_ctor),
        )
        for patcher in self._patches:
            patcher.start()

    def cleanup(self) -> None:
        for patcher in self._patches:
            patcher.stop()

    def detail(self) -> dict[str, object]:
        details = self.engine.take_details()
        if len(details) != 1:
            raise AssertionError(f"expected exactly one detail, got {len(details)}")
        return details[0]


def _sub_mapping(detail: Mapping[str, object], key: str) -> dict[str, object]:
    value = detail[key]
    if not isinstance(value, dict):
        raise AssertionError(f"detail {key!r} is not a mapping")
    return cast("dict[str, object]", value)


class _Stopper(Protocol):
    def stop(self) -> None: ...


def _patch_limits(
    codepoints: object, utf8_bytes: object
) -> tuple[_Stopper, _Stopper]:
    started = (
        mock.patch.object(config, "RUNTIME_ANALYSIS_MAX_CODEPOINTS", codepoints),
        mock.patch.object(config, "RUNTIME_ANALYSIS_MAX_UTF8_BYTES", utf8_bytes),
    )
    for patcher in started:
        patcher.start()
    return started


def _stop_limits(started: tuple[_Stopper, ...]) -> None:
    for patcher in started:
        patcher.stop()


class PolicyValidationTests(unittest.TestCase):
    """T1: pure exact defaults, N/N+1 semantics and invalid values."""

    def test_versioned_defaults_are_finite_engineering_constants(self) -> None:
        codepoints = config.RUNTIME_ANALYSIS_MAX_CODEPOINTS
        utf8_bytes = config.RUNTIME_ANALYSIS_MAX_UTF8_BYTES
        # Exact positive ints, never bool/float/string/None.
        self.assertIs(type(codepoints), int)
        self.assertIs(type(utf8_bytes), int)
        self.assertEqual(codepoints, 32768)
        self.assertEqual(utf8_bytes, 131072)
        self.assertGreaterEqual(utf8_bytes, codepoints)
        self.assertEqual(analysis_policy.current_limits(), (codepoints, utf8_bytes))

    def test_exact_N_admits_N_plus_1_exceeds_on_both_axes(self) -> None:
        # Codepoint axis: exact default N admits, N+1 exceeds.
        self.assertIsNone(
            analysis_policy.classify_original("a" * 32768, 32768, 131072)
        )
        self.assertEqual(
            analysis_policy.classify_original("a" * 32769, 32768, 131072),
            analysis_policy.ANALYSIS_SIZE_EXCEEDED,
        )
        # Byte axis: 4-byte code points make the byte allowance the
        # independent binding axis; exact byte N admits, byte N+1
        # exceeds while the codepoint count still fits.
        self.assertIsNone(
            analysis_policy.classify_original(_E4 * 32768, 32768, 131072)
        )
        self.assertEqual(
            analysis_policy.classify_original(_E4 * 32768, 32768, 131071),
            analysis_policy.ANALYSIS_SIZE_EXCEEDED,
        )
        # Test-only valid limits: exact N on both axes admits.
        self.assertIsNone(analysis_policy.classify_original("ab\r\ncd", 6, 6))
        self.assertEqual(
            analysis_policy.classify_original("ab\r\ncd ", 6, 6),
            analysis_policy.ANALYSIS_SIZE_EXCEEDED,
        )

    def test_original_normalization_and_form_bytes_unmodified(self) -> None:
        # NFC "Tako \u017eivim" (10 code points, 11 bytes) versus the
        # exact canonical decomposition of the SAME text, "Tako
        # z\u030civim" (z + combining caron; 11 code points, 12
        # bytes).  The gate must measure the ORIGINAL bytes: with
        # test-only limits exactly at the NFC form, the NFC text
        # admits and the decomposed text exceeds, which a normalizing
        # measurement could not distinguish.
        nfc = "Tako \u017eivim"
        nfd = "Tako z\u030civim"
        self.assertEqual((len(nfc), len(nfc.encode("utf-8"))), (10, 11))
        self.assertEqual((len(nfd), len(nfd.encode("utf-8"))), (11, 12))
        self.assertIsNone(analysis_policy.classify_original(nfc, 10, 11))
        self.assertEqual(
            analysis_policy.classify_original(nfd, 10, 11),
            analysis_policy.ANALYSIS_SIZE_EXCEEDED,
        )
        # CRLF counts as two original bytes: no stripping before
        # measurement.  "ab \r\ncd" is 7 code points / 7 bytes.
        self.assertEqual(
            analysis_policy.classify_original("ab \r\ncd", 6, 6),
            analysis_policy.ANALYSIS_SIZE_EXCEEDED,
        )
        # Emoji keep their exact original byte width.
        self.assertEqual(len((_E4 * 2).encode("utf-8")), 8)

    def test_invalid_values_rejected_per_field_without_coercion(self) -> None:
        # Each invalid value is paired with a VALID counterpart on
        # the other axis (codepoint 1 for byte rows, 131072 for
        # codepoint rows) so the exact-type rejection stands alone:
        # with a large codepoint counterpart a wrong byte-type check
        # accepting bool True or float 1.0 would be masked by the
        # independent byte < codepoint ValueError, so the byte rows
        # must not rely on it (order 025-a, T1; the cross-field
        # constraint keeps its own test).
        for field, value, counterpart in tuple(
            ("codepoints", bad, 131072) for bad in _INVALID_VALUES
        ) + tuple(("utf8_bytes", bad, 1) for bad in _INVALID_VALUES):
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                if field == "codepoints":
                    analysis_policy.validate_limits(value, counterpart)
                else:
                    analysis_policy.validate_limits(counterpart, value)

    def test_cross_field_byte_below_codepoint_invalid(self) -> None:
        with self.assertRaises(ValueError):
            analysis_policy.validate_limits(100, 50)
        # The equal and larger byte allowance is valid.
        analysis_policy.validate_limits(100, 100)
        analysis_policy.validate_limits(100, 400)

    def test_current_defaults_refreshed_not_captured_once(self) -> None:
        # The pure validation re-reads the CURRENT config on every
        # real use: a patched valid pair is seen immediately, and
        # restoring the module attributes restores the defaults, with
        # no global usage state retained by the policy module.
        self.assertEqual(analysis_policy.current_limits(), (32768, 131072))
        started = _patch_limits(1234, 5678)
        try:
            self.assertEqual(analysis_policy.current_limits(), (1234, 5678))
        finally:
            _stop_limits(started)
        self.assertEqual(analysis_policy.current_limits(), (32768, 131072))

    def test_gate_catches_only_declared_conditions(self) -> None:
        # The declared policy condition (ValueError) is translated by
        # the engine; caller control and MemoryError raised inside the
        # classification are NOT swallowed.
        class _MemoryText(str):
            def encode(
                self,
                encoding: str | None = None,
                errors: str | None = None,
            ) -> bytes:
                raise MemoryError("injected")

        class _ControlText(str):
            def encode(
                self,
                encoding: str | None = None,
                errors: str | None = None,
            ) -> bytes:
                raise KeyboardInterrupt

        with self.assertRaises(MemoryError):
            analysis_policy.classify_original(_MemoryText("abc"), 100, 100)
        with self.assertRaises(KeyboardInterrupt):
            analysis_policy.classify_original(_ControlText("abc"), 100, 100)
        # The declared UnicodeEncodeError is translated to the fixed
        # content-free encoding-invalid reason.
        self.assertEqual(
            analysis_policy.classify_original("abc\ud800", 100, 100),
            analysis_policy.ANALYSIS_ENCODING_INVALID,
        )
        # The same propagation holds at the REAL engine entry with
        # precreated exact exception identity: the injected encoding
        # failures raise inside classify_original and must escape
        # RepairEngine.repair untouched, with zero optional work and
        # no misleading bypass detail recorded.  No spontaneous
        # native OOM or full HTTP control claim is made here.
        with tempfile.TemporaryDirectory(prefix="025a-policy-engine-") as root:
            reviewer = _NoReview()
            engine = proxy.RepairEngine(
                Path(root) / "absent.sqlite", reviewer, pandoc=None
            )
            memory_exc = MemoryError("engine-injected")
            control_exc = KeyboardInterrupt("engine-injected")

            class _MemoryEngineText(str):
                def encode(
                    self,
                    encoding: str | None = None,
                    errors: str | None = None,
                ) -> bytes:
                    raise memory_exc

            class _ControlEngineText(str):
                def encode(
                    self,
                    encoding: str | None = None,
                    errors: str | None = None,
                ) -> bytes:
                    raise control_exc

            engine.begin_request()
            with self.assertRaises(MemoryError) as memory_cm:
                engine.repair(_MemoryEngineText("abc"))
            self.assertIs(memory_cm.exception, memory_exc)
            engine.begin_request()
            with self.assertRaises(KeyboardInterrupt) as control_cm:
                engine.repair(_ControlEngineText("abc"))
            self.assertIs(control_cm.exception, control_exc)
            self.assertEqual(reviewer.calls, 0)
            self.assertEqual(engine.take_details(), [])


class StartupUseOrderingTests(unittest.TestCase):
    """T2: real constructor validation before bind; at-use gate order."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.reviewer = _NoReview()
        self.engine = proxy.RepairEngine(
            self.root / "absent.sqlite", self.reviewer, pandoc=None
        )
        # Occupied-port blocker for the bind differential.
        self.blocker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.blocker.bind(("127.0.0.1", 0))
        self.port = self.blocker.getsockname()[1]

    def tearDown(self) -> None:
        self.blocker.close()
        self.temp.cleanup()

    def test_startup_invalid_policy_fails_before_bind(self) -> None:
        for field, _name in (
            ("codepoints", "RUNTIME_ANALYSIS_MAX_CODEPOINTS"),
            ("utf8_bytes", "RUNTIME_ANALYSIS_MAX_UTF8_BYTES"),
        ):
            for value in _INVALID_VALUES:
                with self.subTest(field=field, value=value):
                    # Valid counterpart on the other axis (codepoint 1
                    # for byte rows, 131072 for codepoint rows) so the
                    # exact-type rejection stands alone at the real
                    # constructor, independent of the cross-field
                    # constraint (order 025-a, T2).
                    started = _patch_limits(
                        value if field == "codepoints" else 1,
                        value if field == "utf8_bytes" else 131072,
                    )
                    try:
                        raised: BaseException | None = None
                        try:
                            proxy.ConceptProxy(
                                ("127.0.0.1", self.port),
                                "http://127.0.0.1:1",
                                self.engine,
                            )
                        except BaseException as exc:  # noqa: BLE001 - exact type
                            raised = exc
                    finally:
                        _stop_limits(started)
                    self.assertIsNotNone(raised)
                    # A plain policy ValueError: neither an OSError
                    # (bind was never attempted) nor anything wider is
                    # acceptable.
                    self.assertIs(type(raised), ValueError)
        # Differential control: with the valid defaults the same
        # occupied port DOES reach bind and fails there, while a free
        # port binds successfully.
        with self.assertRaises(OSError):
            proxy.ConceptProxy(
                ("127.0.0.1", self.port),
                "http://127.0.0.1:1",
                self.engine,
            )
        server = proxy.ConceptProxy(
            ("127.0.0.1", 0), "http://127.0.0.1:1", self.engine
        )
        server.server_close()

    def test_at_use_invalid_policy_precedes_index_and_pandoc(self) -> None:
        observed = _ObservedEngine(
            self.root / "absent.sqlite",
            PandocSpec(binary=str(self.root / "absent-pandoc")),
        )
        try:
            started = _patch_limits(True, 131072)
            try:
                observed.engine.begin_request()
                repaired = observed.engine.repair("short answer")
            finally:
                _stop_limits(started)
            self.assertEqual(repaired, "short answer")
            detail = observed.detail()
            self.assertEqual(
                detail["analysis_bypass"],
                {"reason": analysis_policy.ANALYSIS_POLICY_INVALID},
            )
            self.assertNotIn("protection_failure", detail)
            self.assertNotIn("evidence_failure", detail)
            self.assertEqual(observed.protect_calls, [])
            self.assertEqual(observed.corpus_attempts, [])
            self.assertEqual(observed.reviewer.calls, 0)
        finally:
            observed.cleanup()
        # Ordering differential with valid policy: the missing Pandoc
        # preflight (PANDOC_NOT_FOUND) is reached BEFORE the index is
        # ever opened, so an invalid policy is the only label that can
        # precede both.
        observed2 = _ObservedEngine(
            self.root / "absent.sqlite",
            PandocSpec(binary=str(self.root / "absent-pandoc")),
        )
        try:
            observed2.engine.begin_request()
            repaired = observed2.engine.repair("short answer")
            self.assertEqual(repaired, "short answer")
            detail = observed2.detail()
            self.assertNotIn("analysis_bypass", detail)
            self.assertEqual(
                _sub_mapping(detail, "protection_failure")["reason"],
                "PANDOC_NOT_FOUND",
            )
            self.assertNotIn("evidence_failure", detail)
            self.assertEqual(observed2.protect_calls, [1])
            self.assertEqual(observed2.corpus_attempts, [])
        finally:
            observed2.cleanup()


class EngineDefaultBoundaryTests(unittest.TestCase):
    """T3: real engine exact default 32768/32769 boundaries and byte axis."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.pandoc = _require_qualified_pandoc()
        self.missing_index = self.root / "absent.sqlite"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_default_codepoint_boundary_N_admits_N_plus_1_bypasses(self) -> None:
        # N+1: the gate bypasses before ANY Pandoc, Corpus or reviewer
        # work; the exact original returns with the separate reason.
        observed = _ObservedEngine(self.missing_index, self.pandoc)
        try:
            text = "a" * 32769
            observed.engine.begin_request()
            repaired = observed.engine.repair(text)
            self.assertEqual(repaired, text)
            detail = observed.detail()
            self.assertEqual(
                detail["analysis_bypass"],
                {"reason": analysis_policy.ANALYSIS_SIZE_EXCEEDED},
            )
            self.assertNotIn("protection_failure", detail)
            self.assertNotIn("evidence_failure", detail)
            self.assertEqual(detail["candidates"], [])
            self.assertEqual(detail["replacements"], [])
            self.assertEqual(detail["reviewer_decisions"], [])
            self.assertEqual(detail["protected_difference_count"], 0)
            self.assertEqual(
                _sub_mapping(detail, "review_batch"),
                {
                    "calls": 0,
                    "targets": 0,
                    "outcome": "skipped",
                    "reason": None,
                    "usage": "unknown",
                },
            )
            self.assertEqual(observed.protect_calls, [])
            self.assertEqual(observed.corpus_attempts, [])
            self.assertEqual(observed.reviewer.calls, 0)
        finally:
            observed.cleanup()
        # Exact N: admitted through the mandatory real Pandoc pipeline
        # (no analysis_bypass label), then stops at the intentionally
        # missing index with the ORIGINAL evidence label retained.
        observed2 = _ObservedEngine(self.missing_index, self.pandoc)
        try:
            text = "a" * 32768
            observed2.engine.begin_request()
            repaired = observed2.engine.repair(text)
            self.assertEqual(repaired, text)
            detail = observed2.detail()
            self.assertNotIn("analysis_bypass", detail)
            self.assertNotIn("protection_failure", detail)
            self.assertEqual(
                _sub_mapping(detail, "evidence_failure"),
                {"reason": "RUNTIME_EVIDENCE_UNAVAILABLE", "stage": "early"},
            )
            self.assertEqual(observed2.protect_calls, [1])
            self.assertEqual(observed2.corpus_attempts, [1])
            self.assertEqual(observed2.reviewer.calls, 0)
        finally:
            observed2.cleanup()

    def test_byte_limit_crossing_while_codepoint_count_fits(self) -> None:
        # Explicit test-only valid policy values (labelled; NOT
        # default-throughput evidence): the codepoint axis fits while
        # the strict UTF-8 byte axis is crossed.
        observed = _ObservedEngine(self.missing_index, self.pandoc)
        try:
            started = _patch_limits(100, 148)
            try:
                # 37 four-byte code points: 37 code points (fits),
                # 148 bytes (exact N) -> admitted into the pipeline.
                admitted = _E4 * 37
                observed.engine.begin_request()
                repaired = observed.engine.repair(admitted)
                self.assertEqual(repaired, admitted)
                detail = observed.detail()
                self.assertNotIn("analysis_bypass", detail)
                self.assertEqual(
                    _sub_mapping(detail, "evidence_failure"),
                    {"reason": "RUNTIME_EVIDENCE_UNAVAILABLE", "stage": "early"},
                )
                self.assertEqual(observed.protect_calls, [1])
                # 38 four-byte code points: 38 code points (still
                # fits), 152 bytes (> 148) -> byte-axis bypass with
                # zero work.
                oversize = _E4 * 38
                observed.engine.begin_request()
                repaired = observed.engine.repair(oversize)
                self.assertEqual(repaired, oversize)
                detail = observed.detail()
                self.assertEqual(
                    detail["analysis_bypass"],
                    {"reason": analysis_policy.ANALYSIS_SIZE_EXCEEDED},
                )
                self.assertEqual(observed.protect_calls, [1])
                self.assertEqual(observed.corpus_attempts, [1])
                self.assertEqual(observed.reviewer.calls, 0)
            finally:
                _stop_limits(started)
        finally:
            observed.cleanup()

    def test_oversize_gate_zero_work_separate_reasons(self) -> None:
        # Every bypass kind returns the exact original with zero true
        # parser/mapper/index/reviewer work and its own separate
        # content-free reason; no performance or whole-process memory
        # claim is made from these no-work observers.
        observed = _ObservedEngine(self.missing_index, self.pandoc)
        try:
            cases = (
                ("a" * 32769, None, analysis_policy.ANALYSIS_SIZE_EXCEEDED),
                ("abc\ud800", None, analysis_policy.ANALYSIS_ENCODING_INVALID),
                ("short", True, analysis_policy.ANALYSIS_POLICY_INVALID),
            )
            for text, invalid_policy, reason in cases:
                with self.subTest(reason=reason):
                    started = (
                        _patch_limits(True, 131072)
                        if invalid_policy
                        else None
                    )
                    try:
                        observed.engine.begin_request()
                        repaired = observed.engine.repair(text)
                    finally:
                        if started is not None:
                            _stop_limits(started)
                    self.assertEqual(repaired, text)
                    detail = observed.detail()
                    self.assertEqual(
                        detail["analysis_bypass"], {"reason": reason}
                    )
                    self.assertNotIn("protection_failure", detail)
                    self.assertNotIn("evidence_failure", detail)
                    self.assertEqual(detail["replacements"], [])
                    self.assertEqual(detail["reviewer_decisions"], [])
                    self.assertEqual(
                        _sub_mapping(detail, "review_batch")["usage"],
                        "unknown",
                    )
                    self.assertEqual(observed.protect_calls, [])
                    self.assertEqual(observed.corpus_attempts, [])
                    self.assertEqual(observed.reviewer.calls, 0)
        finally:
            observed.cleanup()


class UsefulRepairTests(unittest.TestCase):
    """T4: real engine useful repair, real Pandoc/ROSQLite, deterministic
    upstream reviewer over owned loopback-0 HTTP."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.pandoc = _require_qualified_pandoc()
        self.db = _evidence_db(self.root)
        self.server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        self.thread = threading.Thread(
            target=self.server.serve_forever, daemon=True
        )
        self.thread.start()
        self.port = self.server.server_address[1]
        _FakeUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = b"{}"
        self.reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.port}/v1",
            "test-model",
            timeout=5.0,
            api_key="fake-key",
        )
        self.engine = proxy.RepairEngine(
            self.db, self.reviewer, pandoc=self.pandoc
        )

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(5)
        self.temp.cleanup()

    def _propose_useful(self, usage: bool) -> None:
        # t0 ("aaa") is the accepted replacement; the other three
        # explicit keeps reject nothing and change no slice.
        props = [
            _prop("t0", keep=False, replacement="repla"),
            _prop("t1", keep=True, replacement=None),
            _prop("t2", keep=True, replacement=None),
            _prop("t3", keep=True, replacement=None),
        ]
        _FakeUpstream.payload = (
            _review_payload(
                props, usage={"input_tokens": 10, "output_tokens": 20, "total_tokens": 30}
            )
            if usage
            else _review_payload(props)
        )

    def test_useful_repair_at_default_limits(self) -> None:
        self._propose_useful(True)
        _FakeUpstream.recorded = []
        self.engine.begin_request()
        repaired = self.engine.repair(_USEFUL)
        self.assertEqual(repaired, _USEFUL_REPAIRED)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        detail = self.engine.take_details()[0]
        self.assertNotIn("analysis_bypass", detail)
        self.assertEqual(detail["repaired"], _USEFUL_REPAIRED)
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 1)
        self.assertEqual(
            review["usage"],
            {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        )
        decisions = detail["reviewer_decisions"]
        if not isinstance(decisions, list):
            self.fail("reviewer_decisions is not a list")
        accepted = [
            _sub_mapping(item, "acceptance")
            for item in decisions
            if isinstance(item, dict)
        ]
        self.assertEqual(sum(1 for a in accepted if a["accepted"]), 1)

    def test_useful_repair_at_selected_test_only_limits_exactly_N(self) -> None:
        # Explicit test-only valid policy values (labelled, not
        # claimed as default-throughput evidence): the same 39
        # code point / 39 byte answer sits EXACTLY at both selected
        # limits, and exact N admits.
        self._propose_useful(True)
        _FakeUpstream.recorded = []
        started = _patch_limits(39, 39)
        try:
            self.engine.begin_request()
            repaired = self.engine.repair(_USEFUL)
            self.assertEqual(repaired, _USEFUL_REPAIRED)
            self.assertEqual(len(_FakeUpstream.recorded), 1)
            detail = self.engine.take_details()[0]
            self.assertNotIn("analysis_bypass", detail)
        finally:
            _stop_limits(started)

    def test_N_plus_1_exact_original_no_calls(self) -> None:
        # Explicit test-only valid policy values (labelled): one
        # code point below the answer length bypasses with the exact
        # original and zero review work.
        self._propose_useful(True)
        _FakeUpstream.recorded = []
        started = _patch_limits(38, 39)
        try:
            self.engine.begin_request()
            repaired = self.engine.repair(_USEFUL)
            self.assertEqual(repaired, _USEFUL)
            detail = self.engine.take_details()[0]
            self.assertEqual(
                detail["analysis_bypass"],
                {"reason": analysis_policy.ANALYSIS_SIZE_EXCEEDED},
            )
        finally:
            _stop_limits(started)
        self.assertEqual(_FakeUpstream.recorded, [])

    def test_under_budget_no_suspicion_zero_calls(self) -> None:
        # Zero detector candidates: the original returns unchanged
        # with zero review calls (LR-002), admitted through the gate.
        _FakeUpstream.recorded = []
        self.engine.begin_request()
        repaired = self.engine.repair(_HEALTHY)
        self.assertEqual(repaired, _HEALTHY)
        self.assertEqual(_FakeUpstream.recorded, [])
        detail = self.engine.take_details()[0]
        self.assertNotIn("analysis_bypass", detail)
        self.assertEqual(detail["candidates"], [])
        self.assertEqual(
            _sub_mapping(detail, "review_batch")["calls"], 0
        )

    def test_admitted_patch_preserves_original_form_and_slices(self) -> None:
        # An admitted answer with NFD diacritics, CRLF and an emoji in
        # untouched regions: only the accepted span changes; every
        # other original slice (normalization, formatting, unapproved
        # words) survives byte-for-byte (LR-007; A-SPAN-01 original
        # coordinates).
        text = _USEFUL + "\r\nz\u030civim \U0001F600"
        self._propose_useful(True)
        _FakeUpstream.recorded = []
        self.engine.begin_request()
        repaired = self.engine.repair(text)
        expected = "repla" + text[len("aaa") :]
        self.assertEqual(repaired, expected)
        # The NFD sequence stays decomposed (no NFC reserialization
        # to the composed zcaron) and the CRLF / emoji survive
        # byte-for-byte.
        self.assertIn("z\u030civim", repaired)
        self.assertNotIn("\u017eivim", repaired)
        self.assertIn("\r\n", repaired)
        self.assertIn("\U0001F600", repaired)
        self.assertEqual(
            repaired.encode("utf-8"), expected.encode("utf-8")
        )


class FreshRequestAfterBypassTests(unittest.TestCase):
    """T6: next healthy request after every bypass kind; no leakage."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.pandoc = _require_qualified_pandoc()
        self.db = _evidence_db(self.root)
        self.server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        self.thread = threading.Thread(
            target=self.server.serve_forever, daemon=True
        )
        self.thread.start()
        _FakeUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = _review_payload(
            [
                _prop("t0", keep=False, replacement="repla"),
                _prop("t1", keep=True, replacement=None),
                _prop("t2", keep=True, replacement=None),
                _prop("t3", keep=True, replacement=None),
            ],
            usage={"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        )
        self.reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.server.server_address[1]}/v1",
            "test-model",
            timeout=5.0,
            api_key="fake-key",
        )
        self.engine = proxy.RepairEngine(
            self.db, self.reviewer, pandoc=self.pandoc
        )

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(5)
        self.temp.cleanup()

    def _healthy(self) -> dict[str, object]:
        _FakeUpstream.recorded = []
        self.engine.begin_request()
        repaired = self.engine.repair(_HEALTHY)
        self.assertEqual(repaired, _HEALTHY)
        detail = self.engine.take_details()[0]
        self.assertNotIn("analysis_bypass", detail)
        self.assertNotIn("evidence_failure", detail)
        self.assertEqual(_sub_mapping(detail, "review_batch")["calls"], 0)
        self.assertEqual(_FakeUpstream.recorded, [])
        return detail

    def test_fresh_request_after_oversize_invalid_encoding_bypass(self) -> None:
        # Oversize bypass -> fresh healthy request works.
        self.engine.begin_request()
        self.assertEqual(self.engine.repair("a" * 32769), "a" * 32769)
        first = self.engine.take_details()[0]
        self.assertEqual(
            first["analysis_bypass"],
            {"reason": analysis_policy.ANALYSIS_SIZE_EXCEEDED},
        )
        healthy = self._healthy()
        # No leaked prior state in the fresh detail.
        self.assertEqual(healthy["original"], _HEALTHY)
        self.assertEqual(healthy["replacements"], [])
        # Invalid policy bypass -> scoped policy restoration -> works.
        started = _patch_limits(True, 131072)
        try:
            self.engine.begin_request()
            self.assertEqual(self.engine.repair("short"), "short")
            second = self.engine.take_details()[0]
            self.assertEqual(
                second["analysis_bypass"],
                {"reason": analysis_policy.ANALYSIS_POLICY_INVALID},
            )
        finally:
            _stop_limits(started)
        self._healthy()
        # Encoding bypass -> fresh healthy request works.
        self.engine.begin_request()
        self.assertEqual(self.engine.repair("abc\ud800"), "abc\ud800")
        third = self.engine.take_details()[0]
        self.assertEqual(
            third["analysis_bypass"],
            {"reason": analysis_policy.ANALYSIS_ENCODING_INVALID},
        )
        self._healthy()

    def test_usage_stays_request_local_across_bypass(self) -> None:
        # Known positive usage on a useful repair, then a bypass: the
        # bypass reports explicit unknown usage, never the earlier
        # request's known usage, and a later useful repair reports the
        # actual usage again.
        self.engine.begin_request()
        self.assertEqual(self.engine.repair(_USEFUL), _USEFUL_REPAIRED)
        useful = self.engine.take_details()[0]
        self.assertEqual(
            _sub_mapping(useful, "review_batch")["usage"],
            {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        )
        self.engine.begin_request()
        self.assertEqual(self.engine.repair("a" * 32769), "a" * 32769)
        bypass = self.engine.take_details()[0]
        self.assertEqual(
            _sub_mapping(bypass, "review_batch")["usage"], "unknown"
        )
        self.engine.begin_request()
        self.assertEqual(self.engine.repair(_USEFUL), _USEFUL_REPAIRED)
        again = self.engine.take_details()[0]
        self.assertEqual(
            _sub_mapping(again, "review_batch")["usage"],
            {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        )


class ProxyRoundTripTests(unittest.TestCase):
    """T7: real ConceptProxy HTTP round trips (completed JSON + delayed
    SSE), real Pandoc, real RO-SQLite corpus and real ResponsesReviewer
    owned worker; only the main and review endpoints are synthetic."""

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

    def _post_client_header(
        self, body: bytes
    ) -> tuple[int, str, bytes]:
        # A small own stdlib client to the REAL owned proxy: the
        # frozen harness post returns (status, body) only and drops
        # headers, so the client-visible Content-Type is observed
        # here on the actual wire (order 025-a, T7).
        client = http.client.HTTPConnection(
            "127.0.0.1", self.harness.proxy_server.server_port, timeout=20
        )
        try:
            client.request(
                "POST",
                "/v1/responses",
                body=body,
                headers={"Content-Length": str(len(body))},
            )
            response = client.getresponse()
            payload = response.read()
            content_type = response.getheader("Content-Type") or ""
            return response.status, content_type, payload
        finally:
            client.close()

    def _post(
        self, source: bytes, stream: bool
    ) -> tuple[int, bytes]:
        _MainUpstream.status = 200
        _MainUpstream.content_type = (
            "text/event-stream" if stream else "application/json"
        )
        _MainUpstream.source = source
        _FakeUpstream.recorded = []
        _FakeUpstream.payload = _review_payload(
            [
                _prop("t0", keep=False, replacement="repla"),
                _prop("t1", keep=True, replacement=None),
                _prop("t2", keep=True, replacement=None),
                _prop("t3", keep=True, replacement=None),
            ],
            usage={"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        )
        return self.harness.post(_contract_body(stream, input_text="hi"))

    def test_completed_json_oversize_bypass_exact_raw_bytes(self) -> None:
        answer = "a" * 32769
        source = _json_completed(answer=answer)
        status, payload = self._post(source, stream=False)
        # The EXACT captured raw main body is returned unchanged (not
        # only decoded-text equality); status and content type are
        # preserved and zero review work happens.
        self.assertEqual(status, 200)
        self.assertEqual(payload, source)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(
            self.records[-1],
            {"review_calls": 0, "reviewer_usage": "unknown"},
        )
        # Client-visible Content-Type on the actual wire (the frozen
        # harness post drops headers); same request envelope as the
        # harness post above.
        h_status, h_type, h_body = self._post_client_header(
            _contract_body(False, input_text="hi")
        )
        self.assertEqual(h_status, 200)
        self.assertEqual(h_type, "application/json")
        self.assertEqual(h_body, source)

    def test_delayed_sse_oversize_bypass_exact_raw_bytes(self) -> None:
        answer = "a" * 40000
        response = {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {
                            "type": "output_text",
                            "text": answer,
                            "content_index": 0,
                        }
                    ],
                }
            ],
        }
        completed = (
            '{"type":"response.completed","response":'
            + json.dumps(response, ensure_ascii=False)
            + "}"
        ).encode()
        raw = _tc_raw(
            _tc_delta("m", answer),
            _tc_part_done(text=answer),
            _tc_item_done(
                parts=[{"type": "output_text", "text": answer}]
            ),
            completed,
        )
        status, payload = self._post(raw, stream=True)
        self.assertEqual(status, 200)
        self.assertEqual(payload, raw)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(
            self.records[-1],
            {"review_calls": 0, "reviewer_usage": "unknown"},
        )
        # Client-visible Content-Type on the actual wire (the frozen
        # harness post drops headers); same streaming request
        # envelope as the harness post above.
        h_status, h_type, h_body = self._post_client_header(
            _contract_body(True, input_text="hi")
        )
        self.assertEqual(h_status, 200)
        self.assertEqual(h_type, "text/event-stream")
        self.assertEqual(h_body, raw)

    def test_admitted_useful_repair_and_fresh_following_request(self) -> None:
        status, payload = self._post(_json_completed(answer=_USEFUL), False)
        self.assertEqual(status, 200)
        envelope = json.loads(payload)
        output = cast("list[object]", envelope["output"])
        message = cast("dict[str, object]", output[0])
        content = cast("list[object]", message["content"])
        part = cast("dict[str, object]", content[0])
        self.assertEqual(part["text"], _USEFUL_REPAIRED)
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
        # Client-visible Content-Type on the actual wire for the
        # admitted useful-repair response (the frozen harness post
        # drops headers); the main upstream still serves the useful
        # answer at this point.
        h_status, h_type, h_body = self._post_client_header(
            _contract_body(False, input_text="hi")
        )
        self.assertEqual(h_status, 200)
        self.assertEqual(h_type, "application/json")
        h_envelope = json.loads(h_body)
        h_output = cast("list[object]", h_envelope["output"])
        h_message = cast("dict[str, object]", h_output[0])
        h_content = cast("list[object]", h_message["content"])
        h_part = cast("dict[str, object]", h_content[0])
        self.assertEqual(h_part["text"], _USEFUL_REPAIRED)
        # The following fresh request works after the admitted pass.
        status, payload = self._post(
            _json_completed(answer=_HEALTHY), False
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload, _json_completed(answer=_HEALTHY))
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(
            self.records[-1],
            {"review_calls": 0, "reviewer_usage": "unknown"},
        )

class EnvelopeSemanticsBeforeGateTests(unittest.TestCase):
    """T8: incomplete/error/unsupported main semantics precede the
    engine; the size gate never labels incomplete captured text a
    successful completed answer."""

    def setUp(self) -> None:
        self.harness = _Harness()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _evidence_db(self.root)
        self.harness.engine.index = self.db
        self.captured: list[dict[str, object]] = []

    def tearDown(self) -> None:
        self.harness.close()
        self.temp.cleanup()

    def _post_recording(
        self, source: bytes, stream: bool, content_type: str | None = None
    ) -> tuple[int, bytes]:
        real_take = self.harness.engine.take_details

        def recording_take() -> list[dict[str, object]]:
            details = real_take()
            self.captured = list(details)
            return details

        patcher = mock.patch.object(
            self.harness.engine, "take_details", recording_take
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.captured = []
        _MainUpstream.status = 200
        _MainUpstream.content_type = (
            content_type
            if content_type is not None
            else "text/event-stream" if stream else "application/json"
        )
        _MainUpstream.source = source
        _FakeUpstream.recorded = []
        _FakeUpstream.payload = _review_payload(
            [_prop("t0", keep=False, replacement="repla")]
        )
        return self.harness.post(_contract_body(stream, input_text="hi"))

    def test_oversize_incomplete_main_never_repair_success(self) -> None:
        # An over-limit answer inside an INCOMPLETE main envelope is
        # passed through byte-identical and the engine produces NO
        # detail at all - not even an analysis-bypass detail, because
        # the gate only ever sees a validated completed answer.
        source = _json_completed(
            answer="a" * 40000, status="in_progress"
        )
        status, payload = self._post_recording(source, False)
        self.assertEqual(status, 200)
        self.assertEqual(payload, source)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(self.captured, [])

    def test_oversize_completed_error_main_bypasses_without_repair(self) -> None:
        source = _json_completed(
            answer="a" * 40000, error={"code": "x", "message": "y"}
        )
        status, payload = self._post_recording(source, False)
        self.assertEqual(status, 200)
        self.assertEqual(payload, source)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(self.captured, [])

    def test_oversize_completed_json_gate_detail_present(self) -> None:
        # Contrast: the SAME over-limit length inside a validated
        # COMPLETED envelope reaches the gate and records exactly one
        # analysis-bypass detail with zero review work.
        source = _json_completed(answer="a" * 40000)
        status, payload = self._post_recording(source, False)
        self.assertEqual(status, 200)
        self.assertEqual(payload, source)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(len(self.captured), 1)
        self.assertEqual(
            self.captured[0]["analysis_bypass"],
            {"reason": analysis_policy.ANALYSIS_SIZE_EXCEEDED},
        )

    def test_malformed_json_main_stays_main_error(self) -> None:
        source = b'{"object":"response","broken":'
        status, payload = self._post_recording(source, False)
        self.assertEqual(status, 502)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(self.captured, [])

    def test_unsupported_content_type_stays_protocol_error(self) -> None:
        source = _json_completed(answer=_HEALTHY)
        status, _payload = self._post_recording(
            source, False, content_type="text/plain"
        )
        self.assertEqual(status, 502)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(self.captured, [])

    def test_hard_capture_cap_keeps_existing_failure_semantics(self) -> None:
        # A main body beyond the hard capture byte bound fails
        # bounded BEFORE the engine, with no review work; the gate
        # never sees it.
        source = b"x" * (config.MAIN_BODY_MAX_BYTES + 1)
        status, _payload = self._post_recording(source, False)
        self.assertEqual(status, 502)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(self.captured, [])

class TraceEncodingBypassTests(unittest.TestCase):
    """R3/R4 (order 025-a): safe-original delivery with optional
    controlled tracing.

    Real proxy, real trace writer, real owned trace directory and
    real stdlib client; only the main/review upstream endpoints are
    synthetic fakes.  The wire is valid ASCII JSON carrying an
    escaped unpaired surrogate (a lone \\ud800) - permitted synthetic
    data, not malformed wire UTF-8.  With tracing off the exact
    original is delivered; with the real owned trace directory
    enabled the SAME input delivers the exact original with zero
    review and the usage observer, while the ONE unencodable
    optional trace detail/file is skipped (no trace file and no
    empty temporary remain).  A valid ASCII size bypass with
    tracing on writes its normal canonical trace, and the following
    fresh request works.  No fake write_traces/canonical_bytes/
    engine/forward and no fabricated I/O error.
    """

    def _surrogate_completed(self, answer: str) -> bytes:
        value = {
            "object": "response",
            "id": "r",
            "status": "completed",
            "output": [
                {
                    "type": "message",
                    "id": "m",
                    "role": "assistant",
                    "status": "completed",
                    "output_index": 0,
                    "content": [
                        {"type": "output_text", "text": answer, "content_index": 0}
                    ],
                }
            ],
        }
        # ensure_ascii is the default: the unpaired surrogate stays a
        # valid ASCII escape on the wire.
        return json.dumps(value, separators=(",", ":")).encode("ascii")

    def _post(
        self, harness: _Harness, source: bytes
    ) -> tuple[int, bytes]:
        _MainUpstream.status = 200
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = source
        _FakeUpstream.recorded = []
        _FakeUpstream.payload = _review_payload(
            [_prop("t0", keep=True, replacement=None)],
            usage={"input_tokens": 1, "output_tokens": 1, "total_tokens": 2},
        )
        return harness.post(_contract_body(False, input_text="hi"))

    def setUp(self) -> None:
        self.harness = _Harness(usage_observer=self._observe)
        self.records: list[dict[str, object]] = []
        self.trace_temp = tempfile.TemporaryDirectory()
        self.trace_dir = Path(self.trace_temp.name)

    def tearDown(self) -> None:
        self.harness.close()
        self.trace_temp.cleanup()

    def _observe(self, record: dict[str, object]) -> None:
        self.records.append(record)

    def _trace_entries(self) -> list[Path]:
        return sorted(self.trace_dir.iterdir())

    def _harness_proxy_post_header(self, body: bytes) -> tuple[int, str, bytes]:
        client = http.client.HTTPConnection(
            "127.0.0.1", self.harness.proxy_server.server_port, timeout=20
        )
        try:
            client.request(
                "POST",
                "/v1/responses",
                body=body,
                headers={"Content-Length": str(len(body))},
            )
            response = client.getresponse()
            payload = response.read()
            content_type = response.getheader("Content-Type") or ""
            return response.status, content_type, payload
        finally:
            client.close()

    def test_encoding_bypass_trace_off_delivers_raw_original(self) -> None:
        # No trace directory is configured: the exact raw original is
        # delivered with zero review and the usage observer.
        source = self._surrogate_completed("abc\ud800def")
        self.assertTrue(all(b < 128 for b in source))
        self.assertIsNone(self.harness.proxy_server.trace_dir)
        status, payload = self._post(self.harness, source)
        self.assertEqual(status, 200)
        self.assertEqual(payload, source)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(
            self.records[-1],
            {"review_calls": 0, "reviewer_usage": "unknown"},
        )

    def test_encoding_bypass_trace_on_skips_unencodable_detail(self) -> None:
        # The real owned trace directory is assigned to the real
        # proxy before the request.
        self.harness.proxy_server.trace_dir = self.trace_dir
        source = self._surrogate_completed("abc\ud800def")
        status, payload = self._post(self.harness, source)
        self.assertEqual(status, 200)
        self.assertEqual(payload, source)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(
            self.records[-1],
            {"review_calls": 0, "reviewer_usage": "unknown"},
        )
        # The one unencodable optional detail is skipped before any
        # temporary allocation: no trace file, no empty temporary.
        self.assertEqual(self._trace_entries(), [])
        # Client-visible Content-Type on the actual wire for the same
        # bypass (the frozen harness post drops headers).
        h_status, h_type, h_body = self._harness_proxy_post_header(
            _contract_body(False, input_text="hi")
        )
        self.assertEqual(h_status, 200)
        self.assertEqual(h_type, "application/json")
        self.assertEqual(h_body, source)
        self.assertEqual(self._trace_entries(), [])

    def test_ascii_size_bypass_trace_on_writes_canonical_trace_and_fresh(self) -> None:
        self.harness.proxy_server.trace_dir = self.trace_dir
        answer = "a" * 32769
        source = _json_completed(answer=answer)
        status, payload = self._post(self.harness, source)
        self.assertEqual(status, 200)
        self.assertEqual(payload, source)
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(
            self.records[-1],
            {"review_calls": 0, "reviewer_usage": "unknown"},
        )
        # The valid ASCII bypass writes its normal canonical trace.
        entries = self._trace_entries()
        self.assertEqual(len(entries), 1)
        trace = json.loads(entries[0].read_text())
        self.assertEqual(
            trace["analysis_bypass"],
            {"reason": analysis_policy.ANALYSIS_SIZE_EXCEEDED},
        )
        self.assertNotIn("evidence_failure", trace)
        self.assertNotIn("protection_failure", trace)
        self.assertEqual(trace["replacements"], [])
        self.assertEqual(trace["candidates"], [])
        self.assertEqual(trace["reviewer_decisions"], [])
        self.assertEqual(trace["acceptance"], [])
        # The following fresh request works after the traced bypass.
        status, payload = self._post(
            self.harness, _json_completed(answer=_HEALTHY)
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload, _json_completed(answer=_HEALTHY))
        self.assertEqual(_FakeUpstream.recorded, [])
        self.assertEqual(
            self.records[-1],
            {"review_calls": 0, "reviewer_usage": "unknown"},
        )

if __name__ == "__main__":
    unittest.main()
