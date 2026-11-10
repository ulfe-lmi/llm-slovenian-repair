"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Request-owned cancellation tests (order 030-a).

Real boundaries under test: the real native disconnect-only poll
watcher (POLLRDHUP|POLLHUP|POLLERR|POLLNVAL, POLLIN excluded, proved
behind an 8192-byte unread ignored tail), the real explicit native
capability validation before bind, and the real proxy lifecycle:
real TCP client -> real admission/Handler -> real main setup/header/
body -> real RepairEngine/Pandoc/read-only SQLite corpus -> real
ResponsesReviewer child exchange -> real parser/acceptance/composition
-> real delivery.  Only the main upstream and the review endpoint are
synthetic loopback-0 servers; observer hooks delegate to the actual
code, never substitute fake detect/candidate/corpus/protect/accept/
compose/apply.  Finite owned children/loopback0 only; no live model,
corpus, network or quality claim (order 030-a, requirements 8 and 12).
"""

from __future__ import annotations

import contextlib
import http.client
import json
import os
import select
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import ClassVar, cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import capture_transport  # noqa: E402
import header_transport  # noqa: E402
import pandoc_protection  # noqa: E402
import proxy  # noqa: E402
import request_lifecycle  # noqa: E402
import review_transport  # noqa: E402
import upstream_setup  # noqa: E402
from batch_review import BatchResult, BatchTarget  # noqa: E402
from qwen_client import ResponsesReviewer  # noqa: E402
from runtime_corpus import RuntimeCorpus  # noqa: E402
from tests.test_responses_contract import _json_completed  # noqa: E402
from tests.test_review_batch import (  # noqa: E402
    TEXT,
    _build_corpus,
    _contract_body,
    _envelope,
    _prop,
    _real_spec,
    _sse_completed,
    _sse_delta,
    _valid_inner,
)

_TAIL = 8192


class _PollCallCounts:
    """Real delegated poll call counts (order 030-a, R8 no-spin proof)."""

    __slots__ = ("poll", "register", "unregister")

    def __init__(self) -> None:
        self.poll = 0
        self.register = 0
        self.unregister = 0


def _counting_poll(counts: _PollCallCounts) -> Callable[[], object]:
    """A transparent poll factory that counts REAL native calls.

    Every returned object delegates register/unregister/poll to the
    real ``select.poll`` (no fake poll results); the counts observe
    the actual register/poll/unregister behavior of the watcher, so
    a bounded number of calls over several 50 ms slices proves there
    is no data-readiness busy-spin (an unchanged flag alone cannot).
    """
    real_poll = select.poll

    class _CountingPoll:
        def __init__(self) -> None:
            self._inner = real_poll()

        def register(self, fd: int, eventmask: int) -> None:
            counts.register += 1
            self._inner.register(fd, eventmask)

        def unregister(self, fd: int) -> None:
            counts.unregister += 1
            self._inner.unregister(fd)

        def poll(self, timeout: int | None = None) -> list[tuple[int, int]]:
            counts.poll += 1
            return self._inner.poll(timeout)

    return _CountingPoll


class _LifecycleNativeTests(unittest.TestCase):
    """Small direct lifecycle/native-socket controls (order 030-a, R8).

    These run BEFORE any proxy integration: positive, FIN/RST,
    unread-tail/no-spin, release/join and context isolation over the
    exact native watcher and capability validation.
    """

    def _pair(self) -> tuple[socket.socket, socket.socket]:
        local, peer = socket.socketpair()
        return local, peer

    def test_live_peer_with_unread_tail_is_not_cancelled(self) -> None:
        local, peer = self._pair()
        scope = request_lifecycle.CancellationScope(local)
        try:
            peer.send(b" " * (_TAIL + 8))
            scope.start()
            self.assertFalse(scope.cancelled())
            # One full bounded slice with data readiness (POLLIN
            # excluded) must not cancel and must not spin on data.
            deadline = time.monotonic() + 0.16
            while time.monotonic() < deadline and not scope.cancelled():
                time.sleep(0.01)
            self.assertFalse(scope.cancelled())
            # The tail bytes were never read or drained by the watcher.
            peek = local.recv(_TAIL + 8, socket.MSG_PEEK)
            self.assertEqual(len(peek), _TAIL + 8)
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()

    def test_fin_behind_unread_tail_cancels_without_reading(self) -> None:
        local, peer = self._pair()
        scope = request_lifecycle.CancellationScope(local)
        try:
            peer.send(b" " * _TAIL)
            scope.start()
            peer.close()
            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline and not scope.cancelled():
                time.sleep(0.005)
            self.assertTrue(scope.cancelled())
            # The unread tail remains in the receive buffer: the
            # watcher never read, parsed or drained it.
            peek = local.recv(_TAIL, socket.MSG_PEEK)
            self.assertEqual(len(peek), _TAIL)
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()

    def test_rst_cancels(self) -> None:
        # Real TCP loopback0: the proved RST path (SO_LINGER 0 close).
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        try:
            client = socket.create_connection(
                ("127.0.0.1", listener.getsockname()[1])
            )
            server_sock, _addr = listener.accept()
            scope = request_lifecycle.CancellationScope(server_sock)
            try:
                client.send(b" " * 8)
                scope.start()
                # SO_LINGER (linger_on=1, l_onltime=0): RST on close.
                client.setsockopt(
                    socket.SOL_SOCKET,
                    socket.SO_LINGER,
                    struct.pack("ii", 1, 0),
                )
                client.close()
                deadline = time.monotonic() + 2.0
                while time.monotonic() < deadline and not scope.cancelled():
                    time.sleep(0.005)
                self.assertTrue(scope.cancelled())
            finally:
                scope.finish()
                with contextlib.suppress(OSError):
                    server_sock.close()
                    client.close()
        finally:
            listener.close()

    def test_already_closed_client_is_caught_by_synchronous_first_check(
        self,
    ) -> None:
        local, peer = self._pair()
        peer.close()
        scope = request_lifecycle.CancellationScope(local)
        try:
            scope.start()
            self.assertTrue(scope.cancelled())
            scope.raise_if_cancelled()
        except request_lifecycle.RequestCancelled:
            pass
        else:
            self.fail("synchronous first check missed a closed client")
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()

    def test_finish_joins_watcher_and_releases_socket(self) -> None:
        local, peer = self._pair()
        scope = request_lifecycle.CancellationScope(local)
        try:
            scope.start()
            started = time.monotonic()
            scope.finish()
            self.assertLessEqual(time.monotonic() - started, 1.0)
            scope.finish()  # idempotent
            self.assertIsNone(scope._sock)
            self.assertIsNone(scope._watcher)
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()

    def test_double_start_is_rejected(self) -> None:
        local, peer = self._pair()
        scope = request_lifecycle.CancellationScope(local)
        try:
            scope.start()
            with self.assertRaises(ValueError):
                scope.start()
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()

    def test_context_isolation_and_noop_outside_request(self) -> None:
        self.assertIsNone(request_lifecycle.active_cancellation_check())
        local, peer = self._pair()
        scope = request_lifecycle.CancellationScope(local)
        seen: dict[str, object] = {}

        def other_thread() -> None:
            seen["check"] = request_lifecycle.active_cancellation_check()

        try:
            scope.start()
            thread = threading.Thread(target=other_thread)
            thread.start()
            thread.join(5)
            # The per-thread slot is a no-op outside the owning
            # request thread: guard threads and foreign threads never
            # see this scope.
            self.assertIsNone(seen.get("check"))
            self.assertEqual(
                request_lifecycle.active_cancellation_check(),
                scope.cancelled,
            )
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        self.assertIsNone(request_lifecycle.active_cancellation_check())

    def test_capability_validation_positive_native(self) -> None:
        # The actual selected native runtime must validate.
        request_lifecycle.validate_native_poll_capability()

    def test_live_peer_unread_tail_keeps_real_poll_calls_bounded(self) -> None:
        # R8 proof fidelity (order 030-a, requirement 2): under
        # unread data readiness the REAL delegated poll/register/
        # unregister calls must stay bounded over several full 50 ms
        # slices - a data-readiness busy-spin that ignores POLLIN
        # would issue one poll per loop iteration, and the count
        # measures that directly (no fake poll results).
        counts = _PollCallCounts()
        local, peer = self._pair()
        scope = request_lifecycle.CancellationScope(local)
        try:
            peer.send(b" " * _TAIL)
            with mock.patch.object(
                # The watcher and first check call select.poll()
                # through the shared module object: patching the
                # select module itself is the exact delegated
                # boundary (no fake poll results).
                select,
                "poll",
                _counting_poll(counts),
            ):
                scope.start()
                deadline = time.monotonic() + 0.21
                while time.monotonic() < deadline and not scope.cancelled():
                    time.sleep(0.01)
                # Join the watcher INSIDE the counting window so the
                # final bounded slice's unregister is counted too.
                scope.finish()
            self.assertFalse(scope.cancelled())
            # 0.21 s covers at least four full 50 ms watcher slices
            # plus the one synchronous first check: a bounded count
            # (one poll per slice, never per data-ready event) proves
            # no data-readiness spin.
            self.assertGreaterEqual(counts.poll, 4)
            self.assertLessEqual(counts.poll, 20)
            self.assertEqual(counts.register, counts.poll)
            self.assertEqual(counts.unregister, counts.poll)
            # The unread tail was never read or drained.
            peek = local.recv(_TAIL, socket.MSG_PEEK)
            self.assertEqual(len(peek), _TAIL)
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()

    def test_capability_validation_rejects_missing_rdhup(self) -> None:
        from unittest import mock

        with (
            mock.patch.object(request_lifecycle, "_POLLRDHUP", 0),
            self.assertRaises(request_lifecycle.NativePollCapabilityError),
        ):
            request_lifecycle.validate_native_poll_capability()

    def test_capability_validation_rejects_missing_poll_interface(self) -> None:
        # Pure R1: the required poll interface must exist; a missing
        # (non-callable) select.poll refuses to start before bind.
        with (
            mock.patch.object(select, "poll", None),
            self.assertRaises(request_lifecycle.NativePollCapabilityError),
        ):
            request_lifecycle.validate_native_poll_capability()

    def test_capability_validation_rejects_zero_mask(self) -> None:
        # Pure R1: a zero composed event mask refuses to start.
        with (
            mock.patch.object(request_lifecycle, "_DISCONNECT_MASK", 0),
            self.assertRaises(request_lifecycle.NativePollCapabilityError),
        ):
            request_lifecycle.validate_native_poll_capability()

    def test_capability_validation_rejects_data_readiness_mask(self) -> None:
        # Pure R1: data readiness (POLLIN) must stay excluded from
        # the disconnect-only mask.
        with mock.patch.object(
            request_lifecycle, "_DISCONNECT_MASK", select.POLLIN
        ), self.assertRaises(request_lifecycle.NativePollCapabilityError):
            request_lifecycle.validate_native_poll_capability()


class _GuardSurvivor:
    """No guard thread may survive a classified acquisition."""

    @staticmethod
    def assert_none() -> None:
        survivors = [
            thread
            for thread in threading.enumerate()
            if thread.name
            in ("concept-header-guard", "concept-setup-guard")
        ]
        assert not survivors, f"guard survivors: {survivors}"


class _FaultyConnection:
    """Exact owned socket plus a fault-injected getresponse (R5).

    The classification/ownership boundary under test is the real
    acquire_response with its real deadline guard and socketpair
    cleanup; only the parser call is deliberately fault-injected to
    raise the exact given instance (Root six-case receipt).
    """

    def __init__(
        self,
        sock: socket.socket,
        control: BaseException | None,
        sleep_seconds: float = 0.0,
    ) -> None:
        self.sock: socket.socket | None = sock
        self._control = control
        self._sleep = sleep_seconds

    def getresponse(self) -> http.client.HTTPResponse:
        if self._sleep:
            time.sleep(self._sleep)
        if self._control is not None:
            raise self._control
        raise AssertionError("no control configured")


class _HeaderFirstControlTests(unittest.TestCase):
    """Existing R5 first-caller-control regressions on the header hook
    (order 030-a, requirement 5; Root six-case fault-injection
    receipt 030a-root-initial-header-first-control-six-cases)."""

    def _run(
        self,
        control: BaseException | None,
        *,
        budget: float,
        sleep: float = 0.0,
        scope: request_lifecycle.CancellationScope | None = None,
        force_cancel: bool = False,
    ) -> BaseException:
        local, peer = socket.socketpair()
        connection = _FaultyConnection(local, control, sleep)
        try:
            if scope is None:
                cancelled = None
            else:
                scope.start()
                if force_cancel:
                    scope._cancelled.set()
                cancelled = scope.cancelled
            try:
                header_transport.acquire_response(
                    connection, budget, cancelled=cancelled
                )
            except BaseException as raised:
                return raised
        finally:
            if scope is not None:
                scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        raise AssertionError("acquisition returned without a response")

    def test_caller_control_before_deadline_preserves_identity(self) -> None:
        for control in (MemoryError(), KeyboardInterrupt(), SystemExit()):
            with self.subTest(control=type(control).__name__):
                raised = self._run(control, budget=5.0)
                self.assertIs(raised, control)
                _GuardSurvivor.assert_none()

    def test_caller_control_after_deadline_preserves_identity(self) -> None:
        for control in (MemoryError(), KeyboardInterrupt(), SystemExit()):
            with self.subTest(control=type(control).__name__):
                # R5: the first nonordinary caller control of the
                # current operation survives the later deadline.
                raised = self._run(control, budget=0.05, sleep=0.3)
                self.assertIs(raised, control)
                _GuardSurvivor.assert_none()

    def test_ordinary_error_after_deadline_stays_header_timeout(self) -> None:
        raised = self._run(OSError("ordinary"), budget=0.05, sleep=0.3)
        self.assertIsInstance(raised, header_transport.HeaderTimeoutError)
        _GuardSurvivor.assert_none()

    def test_ordinary_error_with_cancel_becomes_request_cancelled(self) -> None:
        local_scope, _peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local_scope)
        raised = self._run(
            OSError("ordinary"),
            budget=5.0,
            scope=scope,
            force_cancel=True,
        )
        self.assertIsInstance(raised, request_lifecycle.RequestCancelled)
        _GuardSurvivor.assert_none()
        with contextlib.suppress(OSError):
            local_scope.close()

    def test_caller_control_with_cancel_keeps_exact_identity(self) -> None:
        control = MemoryError()
        local_scope, _peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local_scope)
        raised = self._run(
            control,
            budget=5.0,
            scope=scope,
            force_cancel=True,
        )
        # Cancellation never replaces the current operation's own
        # nonordinary caller control.
        self.assertIs(raised, control)
        _GuardSurvivor.assert_none()
        with contextlib.suppress(OSError):
            local_scope.close()

    def test_racing_completion_with_cancel_closed_and_cancelled(self) -> None:
        local, peer = socket.socketpair()

        class _CompletingConnection:
            def __init__(self) -> None:
                self.sock: socket.socket | None = local
                # A REAL (unparsed) stdlib response object: the racing
                # completion path is the real one, only the parser
                # input is bypassed.
                self.response = http.client.HTTPResponse(local)

            def getresponse(self) -> http.client.HTTPResponse:
                return self.response

        connection = _CompletingConnection()
        scope = request_lifecycle.CancellationScope(local)
        scope.start()
        scope._cancelled.set()
        try:
            with self.assertRaises(request_lifecycle.RequestCancelled):
                header_transport.acquire_response(
                    connection,
                    5.0,
                    cancelled=scope.cancelled,
                )
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        # The racing completion was explicitly closed and never
        # transferred (a real close empties the buffered reader).
        self.assertIsNone(connection.response.fp)
        _GuardSurvivor.assert_none()

    def test_caller_control_not_replaced_by_faulty_predicate(self) -> None:
        # R5 (Root ten-case receipt, case 1): getresponse raises the
        # FIRST MemoryError; the provided predicate returns False on
        # the guard thread but raises a DIFFERENT MemoryError when
        # evaluated on the caller thread after the join.  No other
        # fallible cancellation hook may run before the known
        # current-operation nonordinary control is preserved: the
        # first error keeps its exact identity.
        local, peer = socket.socketpair()
        first = MemoryError()
        second = MemoryError()
        connection = _FaultyConnection(local, first, sleep_seconds=0.1)
        main_ident = threading.get_ident()

        def predicate() -> bool:
            if threading.get_ident() == main_ident:
                raise second
            return False

        scope = request_lifecycle.CancellationScope(local)
        scope.start()
        try:
            with self.assertRaises(MemoryError) as caught:
                header_transport.acquire_response(
                    connection, 5.0, cancelled=predicate
                )
            self.assertIs(caught.exception, first)
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        _GuardSurvivor.assert_none()

    def test_caller_control_survives_faulty_guard_join(self) -> None:
        # R5 (Root cleanup matrix, header-join case): getresponse
        # raises the FIRST MemoryError; the transparent guard.join
        # raises a DIFFERENT MemoryError ONCE, BEFORE the real native
        # join, then joins normally on retry.  Preserving the first
        # control is not completing cleanup: the join must actually
        # complete (the exact owned guard really reaped) before the
        # owning phase returns, and the first control keeps its exact
        # identity.
        local, peer = socket.socketpair()
        first = MemoryError()
        second = MemoryError()
        connection = _FaultyConnection(local, first)
        real_join = threading.Thread.join
        interrupted = False
        reaped: list[threading.Thread] = []

        def faulty_join(
            self: threading.Thread, timeout: float | None = None
        ) -> None:
            nonlocal interrupted
            if not interrupted:
                interrupted = True
                raise second
            real_join(self, timeout)
            reaped.append(self)

        try:
            with (
                mock.patch.object(threading.Thread, "join", faulty_join),
                self.assertRaises(MemoryError) as caught,
            ):
                header_transport.acquire_response(connection, 5.0)
            self.assertIs(caught.exception, first)
            # The actual owned join was completed (reaped), not just
            # the control preserved: the real native join ran.
            self.assertEqual(len(reaped), 1)
            self.assertFalse(reaped[0].is_alive())
        finally:
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        _GuardSurvivor.assert_none()

    def test_guard_predicate_nonordinary_control_transferred(self) -> None:
        # R5 (Root native-header receipt): a blocking real
        # getresponse plus a supplied cancellation predicate that
        # raises the EXACT MemoryError on the owned guard thread.
        # The owned guard's own nonordinary control is preserved and
        # transferred to the owning thread through the actual join:
        # the exact instance propagates - never relabelled as a
        # header timeout or a transport failure - and no guard
        # survives.
        local, peer = socket.socketpair()
        memory = MemoryError()
        raised = False

        def predicate() -> bool:
            nonlocal raised
            if not raised:
                raised = True
                raise memory
            return False

        # getresponse blocks (sleeps) so the guard's sliced wait
        # evaluates the predicate before any parser completion.
        connection = _FaultyConnection(local, None, sleep_seconds=0.3)
        try:
            with self.assertRaises(MemoryError) as caught:
                header_transport.acquire_response(
                    connection, 5.0, cancelled=predicate
                )
            self.assertIs(caught.exception, memory)
        finally:
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        _GuardSurvivor.assert_none()

    def test_ordinary_first_control_keeps_cleanup_memory_error(self) -> None:
        # R5 (Root cleanup matrix, ordinary-first join case):
        # getresponse raises the FIRST ordinary OSError; the
        # transparent guard.join raises a DIFFERENT MemoryError
        # ONCE, BEFORE the real native join, then joins normally on
        # retry.  An ordinary first control has no authority to
        # discard a subsequent first nonordinary cleanup control:
        # the join actually completes (the exact owned guard really
        # reaped) and the MemoryError propagates.
        local, peer = socket.socketpair()
        ordinary = OSError("ordinary")
        cleanup = MemoryError()
        connection = _FaultyConnection(local, ordinary)
        real_join = threading.Thread.join
        interrupted = False
        reaped: list[threading.Thread] = []

        def faulty_join(
            self: threading.Thread, timeout: float | None = None
        ) -> None:
            nonlocal interrupted
            if not interrupted:
                interrupted = True
                raise cleanup
            real_join(self, timeout)
            reaped.append(self)

        try:
            with (
                mock.patch.object(threading.Thread, "join", faulty_join),
                self.assertRaises(MemoryError) as caught,
            ):
                header_transport.acquire_response(connection, 5.0)
            self.assertIs(caught.exception, cleanup)
            self.assertEqual(len(reaped), 1)
            self.assertFalse(reaped[0].is_alive())
        finally:
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        _GuardSurvivor.assert_none()

    def test_faulty_guard_start_stops_joins_and_preserves_control(self) -> None:
        # R5 (Root ten-case receipt, case 3): the transparent guard
        # Thread.start calls the REAL start (the thread actually
        # launches) and then raises the exact MemoryError.  The
        # guard startup sits outside the cleanup scope of the old
        # code and left the actual owned guard alive (able to later
        # shut down the captured socket): exact ownership must be
        # established before fallible startup and the actually
        # started guard actually cancelled/joined, with the first
        # control preserved.
        local, peer = socket.socketpair()
        memory = MemoryError()
        real_start = threading.Thread.start
        started: list[threading.Thread] = []

        def faulty_start(self: threading.Thread) -> None:
            real_start(self)
            started.append(self)
            raise memory

        connection = _FaultyConnection(
            local, AssertionError("unreachable")
        )
        try:
            with (
                mock.patch.object(threading.Thread, "start", faulty_start),
                self.assertRaises(MemoryError) as caught,
            ):
                header_transport.acquire_response(connection, 5.0)
            self.assertIs(caught.exception, memory)
            self.assertEqual(len(started), 1)
            # The actually launched guard was actually stopped and
            # joined: no live guard survives to interrupt the socket.
            self.assertFalse(started[0].is_alive())
        finally:
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        _GuardSurvivor.assert_none()


class _ScopeOwnershipTests(unittest.TestCase):
    """R5 ownership regressions on the new scope (Root five-case
    receipt 030a-root-initial-lifecycle-five-ownership-cases)."""

    def test_partial_start_failure_stops_joins_and_preserves_control(
        self,
    ) -> None:
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        started: list[threading.Thread] = []
        memory = MemoryError()
        real_start = threading.Thread.start

        def faulty_start(self: threading.Thread) -> None:
            real_start(self)
            started.append(self)
            raise memory

        try:
            with (
                mock.patch.object(threading.Thread, "start", faulty_start),
                self.assertRaises(MemoryError) as caught,
            ):
                scope.start()
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        self.assertIs(caught.exception, memory)
        self.assertEqual(len(started), 1)
        # The actually launched watcher is owned and was actually
        # stopped/joined: no live watcher survives the partial start.
        self.assertFalse(started[0].is_alive())
        self.assertFalse(scope.cancelled())

    def test_partial_start_cleanup_join_preserves_first_control(self) -> None:
        # R5 (Root cleanup matrix, partial-scope case): the
        # transparent CancellationScope.start Thread.start actually
        # starts then raises the FIRST MemoryError; the cleanup join
        # raises a SECOND MemoryError ONCE, BEFORE the real native
        # join, then joins normally on retry.  Preserving the first
        # control is not completing cleanup: the actually launched
        # watcher must be really stopped/joined before the owning
        # phase returns, and the first control keeps its exact
        # identity.
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        first = MemoryError()
        second = MemoryError()
        real_start = threading.Thread.start
        real_join = threading.Thread.join
        started: list[threading.Thread] = []
        join_faulted = False
        reaped: list[threading.Thread] = []

        def faulty_start(self: threading.Thread) -> None:
            real_start(self)
            started.append(self)
            raise first

        def faulty_join(
            self: threading.Thread, timeout: float | None = None
        ) -> None:
            nonlocal join_faulted
            if not join_faulted:
                join_faulted = True
                raise second
            real_join(self, timeout)
            reaped.append(self)

        try:
            with (
                mock.patch.object(threading.Thread, "start", faulty_start),
                mock.patch.object(threading.Thread, "join", faulty_join),
                self.assertRaises(MemoryError) as caught,
            ):
                scope.start()
            self.assertIs(caught.exception, first)
            self.assertEqual(len(started), 1)
            # The actually launched watcher was really stopped/joined
            # (the real native join ran), not just left alive.
            self.assertEqual(len(reaped), 1)
            self.assertFalse(started[0].is_alive())
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        self.assertTrue(scope._finished)

    def test_interrupted_join_retains_ownership_and_retry_completes(
        self,
    ) -> None:
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        try:
            scope.start()
            watcher = scope._watcher
            self.assertIsNotNone(watcher)
            assert watcher is not None
            memory = MemoryError()
            interrupted = False
            real_join = threading.Thread.join

            def faulty_join(
                self: threading.Thread, timeout: float | None = None
            ) -> None:
                nonlocal interrupted
                if self is watcher and not interrupted:
                    interrupted = True
                    raise memory
                real_join(self, timeout)

            with (
                mock.patch.object(threading.Thread, "join", faulty_join),
                self.assertRaises(MemoryError) as caught,
            ):
                scope.finish()
            self.assertIs(caught.exception, memory)
            # Ownership is retained, not abandoned or falsely
            # completed: the exact owned watcher and socket remain
            # reachable and the scope is retryable.
            self.assertFalse(scope._finished)
            self.assertIs(scope._watcher, watcher)
            self.assertIsNotNone(scope._sock)
            # The retry completes the exact owned cleanup.
            scope.finish()
            self.assertTrue(scope._finished)
            self.assertIsNone(scope._watcher)
            self.assertIsNone(scope._sock)
            self.assertFalse(watcher.is_alive())
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()

    def test_finish_owned_scope_retries_join_and_transfers_cleanup_control(
        self,
    ) -> None:
        # R5 (shared rule on the owned-scope finish hook): the
        # transparent Thread.join raises a DIFFERENT MemoryError
        # ONCE, BEFORE the real native join, then joins normally on
        # retry.  finish_owned_scope must actually complete the
        # exact owned watcher join (ownership released, not falsely
        # completed) before transferring the first nonordinary
        # cleanup control.
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        try:
            scope.start()
            watcher = scope._watcher
            self.assertIsNotNone(watcher)
            assert watcher is not None
            cleanup = MemoryError()
            interrupted = False
            real_join = threading.Thread.join

            def faulty_join(
                self: threading.Thread, timeout: float | None = None
            ) -> None:
                nonlocal interrupted
                if self is watcher and not interrupted:
                    interrupted = True
                    raise cleanup
                real_join(self, timeout)

            with (
                mock.patch.object(threading.Thread, "join", faulty_join),
                self.assertRaises(MemoryError) as caught,
            ):
                request_lifecycle.finish_owned_scope(scope, None)
            self.assertIs(caught.exception, cleanup)
            # The exact owned watcher was actually joined (cleanup
            # completed before propagation) and the socket released.
            self.assertFalse(watcher.is_alive())
            self.assertTrue(scope._finished)
            self.assertIsNone(scope._sock)
            self.assertIsNone(scope._watcher)
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()


class _HeaderNativeOwnershipTests(unittest.TestCase):
    """R4/R5 actual native parser/resource boundaries (order 030-a).

    Real ``HTTPConnection``/``HTTPResponse`` over owned socketpairs
    with the external owned peer synthetic: a held native parser
    proves the owned guard wake, and a real parsed Connection-close
    response proves the owned-until-transfer response/FD cleanup.
    """

    def test_native_held_parser_guard_fault_wakes_owner(self) -> None:
        # R5 (Root native-header wake receipt): a REAL
        # HTTPConnection.request/getresponse over an owned socketpair
        # with the peer HOLDING the response; the provided
        # cancellation predicate raises the EXACT MemoryError on the
        # actual header guard.  Storing the guard control and setting
        # the event alone cannot wake a parser blocked inside the
        # native socket read: the owned guard must interrupt the
        # exact captured owned socket before exiting, so the owning
        # phase is actually unblocked and bounded, and the exact
        # MemoryError propagates (never a header timeout).
        local, peer = socket.socketpair()
        memory = MemoryError()
        raised = False

        def predicate() -> bool:
            nonlocal raised
            if not raised:
                raised = True
                raise memory
            return False

        connection = http.client.HTTPConnection("synthetic.invalid", 0)
        connection.sock = local
        try:
            connection.request("GET", "/")
            started = time.monotonic()
            with self.assertRaises(MemoryError) as caught:
                header_transport.acquire_response(
                    connection, 0.05, cancelled=predicate
                )
            self.assertIs(caught.exception, memory)
            # The owned interruption unblocked the native parser
            # promptly: bounded, never the unbounded block observed
            # without the wake (Root: .25s+ still blocked).
            self.assertLessEqual(time.monotonic() - started, 2.0)
        finally:
            with contextlib.suppress(Exception):
                connection.close()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        _GuardSurvivor.assert_none()

    def test_native_parsed_response_closed_before_join_control(self) -> None:
        # R5 (Root native parsed-response receipt): a REAL HTTP/1.0
        # 200 Content-Length:2 Connection:close response over an
        # owned socketpair; the REAL getresponse parses it fully and
        # is observed transparently.  The transparent guard.join
        # raises the EXACT MemoryError ONCE, BEFORE the real native
        # join, then joins normally on retry.  A successfully parsed
        # response remains owned until ACTUAL transfer, including
        # when cleanup raises: the join control must not skip the
        # response close, and the parent connection.close (as
        # forward would) cannot close this detached
        # Connection-close response - so after the raise and the
        # parent connection.close, the real response fp and the
        # exact raw socket FD must be closed.
        local, peer = socket.socketpair()
        memory = MemoryError()
        peer.sendall(
            b"HTTP/1.0 200 OK\r\n"
            b"Content-Length: 2\r\n"
            b"Connection: close\r\n"
            b"\r\n"
            b"ok"
        )
        connection = http.client.HTTPConnection("synthetic.invalid", 0)
        connection.sock = local
        fd = local.fileno()
        observed: list[http.client.HTTPResponse] = []
        real_getresponse = connection.getresponse

        def observing_getresponse() -> http.client.HTTPResponse:
            response = real_getresponse()
            observed.append(response)
            return response

        real_join = threading.Thread.join
        interrupted = False
        reaped: list[threading.Thread] = []

        def faulty_join(
            self: threading.Thread, timeout: float | None = None
        ) -> None:
            nonlocal interrupted
            if not interrupted:
                interrupted = True
                raise memory
            real_join(self, timeout)
            reaped.append(self)

        try:
            connection.request("GET", "/")
            with (
                mock.patch.object(
                    connection, "getresponse", observing_getresponse
                ),
                mock.patch.object(threading.Thread, "join", faulty_join),
                self.assertRaises(MemoryError) as caught,
            ):
                header_transport.acquire_response(connection, 5.0)
            self.assertIs(caught.exception, memory)
            self.assertEqual(len(reaped), 1)
            self.assertFalse(reaped[0].is_alive())
            self.assertEqual(len(observed), 1)
            response = observed[0]
            # The untransferred parsed response was explicitly closed
            # BEFORE the join control propagated (real fp gone, not
            # only a fake flag or an identity assertion).
            self.assertTrue(response.will_close)
            self.assertIsNone(response.fp)
            # The parent connection.close (as forward would) then
            # leaves nothing owned open: the exact raw socket FD is
            # actually closed (a detached Connection-close response
            # cannot be closed by the connection close alone).
            connection.close()
            self.assertIsNone(response.fp)
            with self.assertRaises(OSError):
                os.fstat(fd)
        finally:
            if observed:
                with contextlib.suppress(Exception):
                    observed[0].close()
            with contextlib.suppress(Exception):
                connection.close()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        _GuardSurvivor.assert_none()


class _BodyHookTests(unittest.TestCase):
    """R4 actual native body-capture controls (order 030-a).

    Real ``HTTPResponse``/native socketpair/real BufferedReader/real
    select with the external owned peer synthetic: a delayed body
    under a healthy (always-false) predicate, a delayed cancellation
    during a quiet wait, and the unchanged anchored deadline.
    """

    def _primed(self) -> tuple[socket.socket, socket.socket, http.client.HTTPResponse]:
        local, peer = socket.socketpair()
        peer.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\n")
        response = http.client.HTTPResponse(local)
        response.begin()
        return local, peer, response

    def test_healthy_false_predicate_delayed_body_completes(self) -> None:
        # R4 (Root native body two-control proof): the peer sends
        # headers then DELAYS the 2-byte body .12s; the anchored
        # budget is .5s.  A CONNECTED healthy request whose predicate
        # can never cancel must complete the body under the anchored
        # deadline: the 50 ms wake slice is never the deadline (no
        # premature CaptureError at 50 ms).
        local, peer, response = self._primed()

        def deliver() -> None:
            time.sleep(0.12)
            peer.sendall(b"ok")

        thread = threading.Thread(target=deliver)
        try:
            thread.start()
            started = time.monotonic()
            body = capture_transport.read_bounded_body(
                response, 10, 0.5, cancelled=lambda: False
            )
            elapsed = time.monotonic() - started
            self.assertEqual(body, b"ok")
            self.assertLessEqual(elapsed, 0.45)
        finally:
            thread.join(2)
            with contextlib.suppress(OSError):
                local.close()
                peer.close()

    def test_delayed_cancel_during_quiet_wait_is_request_cancelled(self) -> None:
        # R4: the same quiet wait with the cancellation observed
        # midway: it must become RequestCancelled promptly at the
        # next wake slice - never a premature CaptureError, and
        # never a wait out of the anchored budget.
        local, peer, response = self._primed()
        state = {"cancelled": False}

        def flip() -> None:
            time.sleep(0.12)
            state["cancelled"] = True

        thread = threading.Thread(target=flip)
        try:
            thread.start()
            started = time.monotonic()
            with self.assertRaises(request_lifecycle.RequestCancelled):
                capture_transport.read_bounded_body(
                    response,
                    10,
                    5.0,
                    cancelled=lambda: state["cancelled"],
                )
            # Observed at the next 50 ms wake slice after the flip:
            # well under the anchored budget.
            self.assertLessEqual(time.monotonic() - started, 1.0)
        finally:
            thread.join(2)
            with contextlib.suppress(OSError):
                local.close()
                peer.close()

    def test_false_predicate_full_deadline_expiry_unchanged(self) -> None:
        # R4: with a predicate that never cancels, the SAME anchored
        # deadline still bounds the phase: a body that never arrives
        # times out at the full budget (not at the first 50 ms wake
        # slice, and not later).
        local, peer, response = self._primed()
        try:
            started = time.monotonic()
            with self.assertRaises(capture_transport.CaptureError):
                capture_transport.read_bounded_body(
                    response, 10, 0.5, cancelled=lambda: False
                )
            elapsed = time.monotonic() - started
            self.assertGreaterEqual(elapsed, 0.45)
            self.assertLessEqual(elapsed, 1.5)
        finally:
            with contextlib.suppress(OSError):
                local.close()
                peer.close()


class _SetupBetweenPhaseTests(unittest.TestCase):
    """Actual setup between-phase ownership controls (order 030-a).

    Real ``open_upstream_connection``/``SetupGuard`` against an owned
    loopback-0 TCP listener with a transparent ``_connect_phase``
    observer that delegates to the REAL connect: the positive control
    returns a real connection whose emitted request the peer actually
    observes, and the cancel case (direct cancellation Event set only
    AFTER the actual successful connect) is observed BETWEEN phases,
    so the already-owned connected socket must be actually closed on
    the cancel path with 0 emitted HTTP bytes (Root sixth review).
    """

    @contextlib.contextmanager
    def _listener(self) -> Iterator[socket.socket]:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        try:
            yield listener
        finally:
            with contextlib.suppress(OSError):
                listener.close()

    def _observing_connect(
        self, after: Callable[[socket.socket], None]
    ) -> Callable[..., socket.socket]:
        """A transparent ``_connect_phase`` delegate with a hook."""
        real_connect = upstream_setup._connect_phase

        def observer(
            addresses: list[tuple[int, str]],
            port: int,
            deadline: float,
            capture_timeout: float,
            guard: upstream_setup.SetupGuard,
            cancelled: Callable[[], bool] | None = None,
        ) -> socket.socket:
            sock = real_connect(
                addresses,
                port,
                deadline,
                capture_timeout,
                guard,
                cancelled,
            )
            after(sock)
            return sock

        return observer

    def test_between_phase_cancel_closes_actual_connected_socket(self) -> None:
        with self._listener() as listener:
            port = listener.getsockname()[1]
            local, peer = socket.socketpair()
            scope = request_lifecycle.CancellationScope(local)
            captured_fd: int | None = None

            def cancel_after_connect(sock: socket.socket) -> None:
                nonlocal captured_fd
                # Direct cancellation only AFTER the actual
                # successful connect: the phase boundary right after
                # connect must own the already-connected socket.
                captured_fd = sock.fileno()
                scope._cancelled.set()

            try:
                scope.start()
                with mock.patch.object(
                    upstream_setup,
                    "_connect_phase",
                    self._observing_connect(cancel_after_connect),
                ), self.assertRaises(
                    request_lifecycle.RequestCancelled
                ):
                    upstream_setup.open_upstream_connection(
                        scheme="http",
                        host="127.0.0.1",
                        port=port,
                        request_path="/",
                        body=b"",
                        headers={"Host": "127.0.0.1"},
                        deadline=time.monotonic() + 5.0,
                        capture_timeout=5.0,
                        cancelled=scope.cancelled,
                    )
            finally:
                scope.finish()
                with contextlib.suppress(OSError):
                    local.close()
                    peer.close()
            # The exact owned connected socket FD is actually closed
            # on the cancel path (checked immediately: no other fd has
            # been opened in between, so the number cannot be reused).
            self.assertIsNotNone(captured_fd)
            assert captured_fd is not None
            with self.assertRaises(OSError):
                os.fstat(captured_fd)
            # 0 emitted HTTP bytes: the accepted connection ends
            # immediately with EOF (a left-open socket would block
            # until this timeout and fail instead of hanging).
            listener.settimeout(2.0)
            accepted, _ = listener.accept()
            try:
                accepted.settimeout(2.0)
                try:
                    data = accepted.recv(4096)
                except TimeoutError:
                    self.fail(
                        "the actual connected socket was left open "
                        "on between-phase cancel (no EOF)"
                    )
                self.assertEqual(data, b"")
            finally:
                with contextlib.suppress(OSError):
                    accepted.close()
        _GuardSurvivor.assert_none()

    def test_between_phase_positive_control_returns_real_connection(self) -> None:
        with self._listener() as listener:
            port = listener.getsockname()[1]
            local, peer = socket.socketpair()
            scope = request_lifecycle.CancellationScope(local)
            seen: list[socket.socket] = []

            def observe(sock: socket.socket) -> None:
                seen.append(sock)

            connection: http.client.HTTPConnection | None = None
            try:
                scope.start()
                with mock.patch.object(
                    upstream_setup,
                    "_connect_phase",
                    self._observing_connect(observe),
                ):
                    connection = upstream_setup.open_upstream_connection(
                        scheme="http",
                        host="127.0.0.1",
                        port=port,
                        request_path="/",
                        body=b"",
                        headers={"Host": "127.0.0.1"},
                        deadline=time.monotonic() + 5.0,
                        capture_timeout=5.0,
                        cancelled=scope.cancelled,
                    )
                # The healthy request was never cancelled and the
                # observer saw exactly the one real connect.
                self.assertFalse(scope.cancelled())
                self.assertEqual(len(seen), 1)
                self.assertIsNotNone(connection.sock)
                # The peer actually observes the real emitted request
                # (the positive control of the cancel case's
                # 0-HTTP-byte proof).
                listener.settimeout(2.0)
                accepted, _ = listener.accept()
                try:
                    accepted.settimeout(2.0)
                    data = b""
                    while b"\r\n\r\n" not in data:
                        chunk = accepted.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                finally:
                    with contextlib.suppress(OSError):
                        accepted.close()
                self.assertTrue(data.startswith(b"POST / HTTP/1.1"))
                self.assertIn(b"Host: 127.0.0.1", data)
                self.assertIn(b"Content-Length: 0", data)
            finally:
                if connection is not None:
                    with contextlib.suppress(Exception):
                        connection.close()
                scope.finish()
                with contextlib.suppress(OSError):
                    local.close()
                    peer.close()
        _GuardSurvivor.assert_none()


class _SetupUploadHandoffTests(unittest.TestCase):
    """Actual setup AFTER-upload handoff controls (order 030-a).

    Real loopback-0 TCP / ``open_upstream_connection`` / real
    ``HTTPConnection.request`` upload / real ``SetupGuard`` with
    transparent ``SetupGuard`` constructor and request observers
    that delegate the REAL work and only synchronize the sticky
    uploaded Event (visible to BOTH parent and guard) after the
    successful upload: the healthy control transfers a usable open
    owned connection with the guard joined, a cancellation
    observed before the handoff wins over the completed upload
    (closed, dedicated exception), and the guard's own first
    nonordinary control is transferred with the exact identity plus
    an actually closed FD and zero live guards (Root eighth review).
    """

    def _peer(
        self, listener: socket.socket
    ) -> tuple[threading.Thread, dict[str, object]]:
        """Accept one connection and record the observed upload."""
        observed: dict[str, object] = {"data": b"", "error": None}
        state: dict[str, socket.socket | None] = {"peer": None}

        def server() -> None:
            try:
                # Finite accept: even a pre-connect fault cannot
                # strand this thread - closing the listener alone
                # does not guarantee a blocked native accept wakes.
                listener.settimeout(5.0)
                peer, _ = listener.accept()
                state["peer"] = peer
                peer.settimeout(2.0)
                observed["data"] = peer.recv(4096)
            except BaseException as exc:
                observed["error"] = exc
            finally:
                owned_peer = state["peer"]
                if owned_peer is not None:
                    with contextlib.suppress(OSError):
                        owned_peer.close()

        thread = threading.Thread(target=server, name="concept-upload-peer")
        thread.start()
        return thread, observed

    def _listener(self) -> socket.socket:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        return listener

    def test_healthy_upload_returns_open_usable_connection(self) -> None:
        listener = self._listener()
        port = listener.getsockname()[1]
        peer_thread, observed = self._peer(listener)
        connection: http.client.HTTPConnection | None = None
        try:
            connection = upstream_setup.open_upstream_connection(
                scheme="http",
                host="127.0.0.1",
                port=port,
                request_path="/",
                body=b"",
                headers={"Host": "127.0.0.1"},
                deadline=time.monotonic() + 5.0,
                capture_timeout=5.0,
            )
            # The healthy same actual upload transfers a usable
            # OPEN owned connection (no observer, no cancellation),
            # and the guard is actually joined.
            sock = connection.sock
            assert sock is not None
            fd = sock.fileno()
            self.assertGreaterEqual(fd, 0)
            os.fstat(fd)
        finally:
            if connection is not None:
                with contextlib.suppress(Exception):
                    connection.close()
            peer_thread.join(3)
            with contextlib.suppress(OSError):
                listener.close()
        # The owned peer thread actually completed (finite, truthful
        # cleanup - no daemon-and-abandon).
        self.assertFalse(peer_thread.is_alive())
        self.assertIsNone(observed["error"])
        self.assertTrue(
            cast("bytes", observed["data"]).startswith(b"POST / HTTP/1.1")
        )
        _GuardSurvivor.assert_none()

    def test_observed_cancel_before_handoff_closes_and_raises(self) -> None:
        listener = self._listener()
        port = listener.getsockname()[1]
        peer_thread, observed = self._peer(listener)
        uploaded = threading.Event()
        guards: list[upstream_setup.SetupGuard] = []
        captured: dict[str, int] = {}
        real_guard = upstream_setup.SetupGuard
        real_request = http.client.HTTPConnection.request

        def guard_observer(
            deadline: float,
        ) -> upstream_setup.SetupGuard:
            # Transparent: the real constructor call shape is
            # deadline-only (the product adopts the predicate on the
            # real guard after construction).
            guard = real_guard(deadline)
            guards.append(guard)
            return guard

        def predicate() -> bool:
            # The sticky uploaded Event is visible to BOTH the
            # parent and the native guard (Root eighth review).
            return uploaded.is_set()

        def request_observer(
            self: http.client.HTTPConnection,
            method: str,
            url: str,
            body: bytes | None,
            headers: dict[str, str],
            encode_chunked: bool = False,
        ) -> None:
            # Delegate the REAL upload, then synchronize to the
            # native guard's OWN observation before returning.
            real_request(
                self,
                method,
                url,
                body=body,
                headers=headers,
                encode_chunked=encode_chunked,
            )
            sock = self.sock
            assert sock is not None
            captured["fd"] = sock.fileno()
            uploaded.set()
            limit = time.monotonic() + 2.0
            while time.monotonic() < limit:
                if guards and guards[0].is_cancelled():
                    break
                time.sleep(0.001)

        try:
            with (
                mock.patch.object(
                    upstream_setup, "SetupGuard", guard_observer
                ),
                mock.patch.object(
                    http.client.HTTPConnection, "request", request_observer
                ),
                self.assertRaises(request_lifecycle.RequestCancelled),
            ):
                upstream_setup.open_upstream_connection(
                    scheme="http",
                    host="127.0.0.1",
                    port=port,
                    request_path="/",
                    body=b"",
                    headers={"Host": "127.0.0.1"},
                    deadline=time.monotonic() + 5.0,
                    capture_timeout=5.0,
                    cancelled=predicate,
                )
        finally:
            peer_thread.join(3)
            with contextlib.suppress(OSError):
                listener.close()
        # The owned peer thread actually completed (finite, truthful
        # cleanup - no daemon-and-abandon).
        self.assertFalse(peer_thread.is_alive())
        # The native guard ACTUALLY observed the cancellation
        # before the handoff, and the exact connected FD is
        # actually closed on the cancel path (checked immediately:
        # no other fd opened in between, so no reuse).
        self.assertEqual(len(guards), 1)
        self.assertTrue(guards[0].is_cancelled())
        self.assertIn("fd", captured)
        with self.assertRaises(OSError):
            os.fstat(captured["fd"])
        # The real upload DID complete (the peer saw it); the
        # cancellation still won BEFORE the handoff.
        self.assertIsNone(observed["error"])
        self.assertTrue(
            cast("bytes", observed["data"]).startswith(b"POST / HTTP/1.1")
        )
        _GuardSurvivor.assert_none()

    def test_late_guard_control_identity_and_fd_close(self) -> None:
        listener = self._listener()
        port = listener.getsockname()[1]
        peer_thread, observed = self._peer(listener)
        uploaded = threading.Event()
        guards: list[upstream_setup.SetupGuard] = []
        captured: dict[str, int] = {}
        memory = MemoryError()
        real_guard = upstream_setup.SetupGuard
        real_request = http.client.HTTPConnection.request

        def guard_observer(
            deadline: float,
        ) -> upstream_setup.SetupGuard:
            # Transparent: the real constructor call shape is
            # deadline-only (the product adopts the predicate on the
            # real guard after construction).
            guard = real_guard(deadline)
            guards.append(guard)
            return guard

        def predicate() -> bool:
            # The unique first control is raised by the native
            # guard thread only, after the actual upload: the
            # owning thread's own checks stay healthy.
            if uploaded.is_set() and (
                threading.current_thread().name == "concept-setup-guard"
            ):
                raise memory
            return False

        def request_observer(
            self: http.client.HTTPConnection,
            method: str,
            url: str,
            body: bytes | None,
            headers: dict[str, str],
            encode_chunked: bool = False,
        ) -> None:
            # Delegate the REAL upload, then synchronize to the
            # guard's OWN capture of the first control.
            real_request(
                self,
                method,
                url,
                body=body,
                headers=headers,
                encode_chunked=encode_chunked,
            )
            sock = self.sock
            assert sock is not None
            captured["fd"] = sock.fileno()
            uploaded.set()
            limit = time.monotonic() + 2.0
            while time.monotonic() < limit:
                if guards and guards[0].captured_control() is memory:
                    break
                time.sleep(0.001)

        try:
            with (
                mock.patch.object(
                    upstream_setup, "SetupGuard", guard_observer
                ),
                mock.patch.object(
                    http.client.HTTPConnection, "request", request_observer
                ),
                self.assertRaises(MemoryError) as caught,
            ):
                upstream_setup.open_upstream_connection(
                    scheme="http",
                    host="127.0.0.1",
                    port=port,
                    request_path="/",
                    body=b"",
                    headers={"Host": "127.0.0.1"},
                    deadline=time.monotonic() + 5.0,
                    capture_timeout=5.0,
                    cancelled=predicate,
                )
        finally:
            peer_thread.join(3)
            with contextlib.suppress(OSError):
                listener.close()
        # The owned peer thread actually completed (finite, truthful
        # cleanup - no daemon-and-abandon).
        self.assertFalse(peer_thread.is_alive())
        # The guard recorded the control and was actually joined,
        # and the EXACT first MemoryError escaped with its
        # identity...
        self.assertEqual(len(guards), 1)
        self.assertIs(guards[0].captured_control(), memory)
        self.assertIs(caught.exception, memory)
        # ...and the untransferred owned connection is actually
        # closed on this late guard-control path too.
        self.assertIn("fd", captured)
        with self.assertRaises(OSError):
            os.fstat(captured["fd"])
        self.assertIsNone(observed["error"])
        self.assertTrue(
            cast("bytes", observed["data"]).startswith(b"POST / HTTP/1.1")
        )
        _GuardSurvivor.assert_none()


class _RecordingPopen(subprocess.Popen[bytes]):
    """Transparent Popen that records the exact owned instance (R8).

    The real construction is untouched: the runner's ``__new__`` +
    ``__init__`` pair still performs the REAL child creation, and
    only the instance identity is recorded for the reaping proof
    (frozen 023-a owned-subclass pattern mirror; no global
    class-slot mutation, no fake child).
    """

    created: ClassVar[list[subprocess.Popen[bytes]]] = []

    def __new__(
        cls: type[_RecordingPopen], *args: object, **kwargs: object
    ) -> _RecordingPopen:
        instance = super().__new__(cls)
        _RecordingPopen.created.append(instance)
        return instance


class _PandocRunnerCancellationTests(unittest.TestCase):
    """Actual owned Pandoc runner cancellation control (order 030-a).

    The real ``_run_bounded`` owned runner over the qualified real
    Pandoc binary (strict ``CONCEPT_PANDOC``, no PATH discovery or
    fallback), with an active request scope on the owner thread: the
    context-local accessor path (the runner-only boundary; no public
    parameter) is observed at the phase entry BEFORE the owned
    launch, where a pre-entry cancellation starts ZERO children,
    and at the loop top AFTER the actual child start, where a
    cancellation set from a transparent observer after real Popen
    returns must kill and ACTUALLY reap the exact owned child
    (Root seventh review).
    """

    @staticmethod
    def _binary() -> str:
        configured = os.environ.get("CONCEPT_PANDOC", "").strip()
        if not configured:
            raise AssertionError(
                "CONCEPT_PANDOC must name the qualified installed "
                "Pandoc binary; no PATH discovery or fallback"
            )
        return configured

    @staticmethod
    def _fds() -> set[int]:
        return {int(name) for name in os.listdir("/proc/self/fd")}

    @staticmethod
    def _child_pids() -> set[int]:
        """The pids of the live/zombie children of THIS test process."""
        my_pid = os.getpid()
        pids: set[int] = set()
        for entry in os.listdir("/proc"):
            if not entry.isdigit():
                continue
            try:
                stat = Path(f"/proc/{entry}/stat").read_text()
            except OSError:
                continue
            fields = stat.rsplit(")", 1)[1].split()
            if int(fields[1]) == my_pid:
                pids.add(int(entry))
        return pids

    def test_after_start_cancel_reaps_actual_owned_child(self) -> None:
        binary = self._binary()
        self.assertTrue(os.path.isfile(binary))
        self.assertTrue(os.access(binary, os.X_OK))
        spec = pandoc_protection.PandocSpec(binary=binary)
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        _RecordingPopen.created.clear()
        before = self._fds()
        children_before = self._child_pids()
        real_accessor = request_lifecycle.active_cancellation_check
        observations = 0

        def observing_accessor() -> Callable[[], bool] | None:
            # Transparent: delegate to the REAL accessor; the
            # cancellation is set from this observer only AFTER the
            # pre-launch phase-entry observation - i.e. after real
            # Popen has returned and the exact child exists.
            nonlocal observations
            observations += 1
            check = real_accessor()
            assert check is not None
            if observations >= 2:
                scope._cancelled.set()
            return check

        try:
            scope.start()
            with (
                mock.patch.object(subprocess, "Popen", _RecordingPopen),
                mock.patch.object(
                    request_lifecycle,
                    "active_cancellation_check",
                    observing_accessor,
                ),
                self.assertRaises(request_lifecycle.RequestCancelled),
            ):
                pandoc_protection._run_bounded(
                    spec, pandoc_protection._pandoc_argv(spec), b""
                )
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        # The ACTUAL child was created (the cancel landed AFTER the
        # real start) and then signalled and ACTUALLY reaped by the
        # owned cleanup before the exception propagated: the real
        # wait set the returncode, the exact /proc entry is gone
        # (no live child, no zombie), and this process owns no
        # child at all afterwards.
        self.assertEqual(observations, 2)
        self.assertEqual(len(_RecordingPopen.created), 1)
        process = _RecordingPopen.created[0]
        self.assertIsNotNone(process.pid)
        self.assertIsNotNone(process.returncode)
        self.assertFalse(Path(f"/proc/{process.pid}/stat").exists())
        self.assertEqual(self._child_pids(), children_before)
        # No owned resource survives: no watcher thread and no new
        # file descriptor (the child's pipes are closed by the owned
        # cleanup).
        watchers = [
            thread
            for thread in threading.enumerate()
            if thread.name == "concept-cancellation-watch"
        ]
        self.assertEqual(watchers, [])
        self.assertEqual(self._fds() - before, set())

    def test_pre_entry_cancel_starts_zero_children(self) -> None:
        binary = self._binary()
        self.assertTrue(os.path.isfile(binary))
        self.assertTrue(os.access(binary, os.X_OK))
        spec = pandoc_protection.PandocSpec(binary=binary)
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        _RecordingPopen.created.clear()
        before = self._fds()
        children_before = self._child_pids()
        try:
            scope.start()
            # PRE-entry cancellation: the phase-entry check must
            # fire BEFORE the owned launch - no child is started,
            # allocated or orphaned (Root seventh review).
            scope._cancelled.set()
            with (
                mock.patch.object(subprocess, "Popen", _RecordingPopen),
                self.assertRaises(request_lifecycle.RequestCancelled),
            ):
                pandoc_protection._run_bounded(
                    spec, pandoc_protection._pandoc_argv(spec), b""
                )
        finally:
            scope.finish()
            with contextlib.suppress(OSError):
                local.close()
                peer.close()
        # ZERO children: no Popen instance was even allocated, and
        # this process owns no child at the OS level.
        self.assertEqual(_RecordingPopen.created, [])
        self.assertEqual(self._child_pids(), children_before)
        self.assertEqual(self._fds() - before, set())


if __name__ == "__main__":
    unittest.main()

# ------------------------------------------------------------------
# Order 030-a, requirement 8: full Proxy integration over real TCP.
#
# Real accepted client -> real admission/Handler -> real main setup /
# header / body capture -> real RepairEngine (Pandoc, read-only
# SQLite corpus, detection, acceptance, composition, rendering) ->
# real owned ResponsesReviewer child exchange -> real delivery.
# Only the main upstream and the review endpoint are synthetic
# loopback-0 raw-socket servers; the observer hooks delegate the
# actual work and never substitute fake detect/candidate/corpus/
# protect/accept/compose/apply.  Finite owned children/loopback0
# only (requirements 8 and 12).


class _RawLoopbackServer:
    """One finite owned raw-socket server on loopback port 0.

    The owned (non-daemon) server thread handles client connections
    in order by calling the test-provided handler for each client.
    Every accept iteration is a bounded native wait (closing the
    listener FD from another thread does not itself prove the native
    accept wakes), and ``close`` actually joins the thread - no
    daemon-and-abandon.
    """

    def __init__(
        self, name: str, handler: Callable[[socket.socket], None]
    ) -> None:
        self._name = name
        self._handler = handler
        self._listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listener.bind(("127.0.0.1", 0))
        self._listener.listen(16)
        self.port = self._listener.getsockname()[1]
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._clients: list[socket.socket] = []

    def start(self) -> None:
        self._thread = threading.Thread(
            target=self._run, name=self._name, daemon=False
        )
        self._thread.start()

    def _run(self) -> None:
        # Bounded native accept wake/stop: each accept is a bounded
        # wait, the stop flag is rechecked between real accepts, and
        # a closed listener (OSError) ends the loop.  A blocked
        # native accept therefore always terminates on close.
        self._listener.settimeout(0.25)
        while not self._stop.is_set():
            try:
                client, _ = self._listener.accept()
            except TimeoutError:
                continue
            except OSError:
                break
            self._clients.append(client)
            try:
                self._handler(client)
            except OSError:
                pass
            finally:
                with contextlib.suppress(OSError):
                    client.close()

    def close(self) -> bool:
        """Stop, close and actually join the owned server.

        Returns True when the thread actually completed.  Callers
        must attempt close on EVERY owned server before asserting, so
        one failed cleanup cannot strand the remaining owned
        servers/threads (the single aggregate assertion happens in
        the test teardown).
        """
        self._stop.set()
        with contextlib.suppress(OSError):
            self._listener.close()
        for client in list(self._clients):
            with contextlib.suppress(OSError):
                client.close()
        thread = self._thread
        if thread is not None:
            thread.join(5.0)
        return thread is None or not thread.is_alive()


def _read_http_request(sock: socket.socket) -> tuple[str, dict[str, str], bytes]:
    """Read one bounded raw HTTP/1.1 request (synthetic loopback)."""
    sock.settimeout(10.0)
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = sock.recv(65536)
        if not chunk:
            raise OSError("client closed before the request was complete")
        data += chunk
    head, _, body = data.partition(b"\r\n\r\n")
    lines = head.decode("iso-8859-1").split("\r\n")
    headers: dict[str, str] = {}
    for line in lines[1:]:
        name, _, value = line.partition(":")
        headers[name.strip().lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    while len(body) < length:
        chunk = sock.recv(65536)
        if not chunk:
            break
        body += chunk
    return lines[0], headers, body


def _send_http_response(sock: socket.socket, payload: bytes, content_type: str) -> None:
    head = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: " + content_type.encode() + b"\r\n"
        b"Content-Length: " + str(len(payload)).encode() + b"\r\n"
        b"\r\n"
    )
    sock.sendall(head + payload)


def _read_http_response(sock: socket.socket) -> tuple[int, dict[str, str], bytes]:
    sock.settimeout(20.0)
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = sock.recv(65536)
        if not chunk:
            raise OSError("proxy closed before the response headers")
        data += chunk
    head, _, body = data.partition(b"\r\n\r\n")
    lines = head.decode("iso-8859-1").split("\r\n")
    status = int(lines[0].split(" ", 2)[1])
    headers: dict[str, str] = {}
    for line in lines[1:]:
        name, _, value = line.partition(":")
        headers[name.strip().lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    while len(body) < length:
        chunk = sock.recv(65536)
        if not chunk:
            break
        body += chunk
    return status, headers, body


def _post_to_proxy(
    sock: socket.socket, body: bytes, close: bool = False
) -> None:
    head = (
        b"POST /v1/responses HTTP/1.1\r\n"
        b"Host: 127.0.0.1\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
    )
    if close:
        # One-shot direct-drive fixture: the native handle loop must
        # cover exactly this one request (root fifteenth review).
        head += b"Connection: close\r\n"
    head += b"\r\n"
    sock.sendall(head + body)


def _drain_client(sock: socket.socket, limit: float = 10.0) -> bytes:
    """After the client write-half close (FIN), read everything the
    proxy sends on that connection.  Bounded: the quiet-abort
    expectation is zero bytes followed by the proxy-side close (EOF);
    any captured bytes prove a spurious emission on a closed client."""
    sock.settimeout(0.25)
    data = b""
    deadline = time.monotonic() + limit
    while True:
        try:
            chunk = sock.recv(65536)
        except TimeoutError:
            if time.monotonic() >= deadline:
                break
            continue
        except OSError:
            break
        if not chunk:
            break
        data += chunk
        if time.monotonic() >= deadline:
            break
    return data


def _hold_until_close(sock: socket.socket, release: threading.Event) -> bool:
    """Hold one synthetic upstream connection until the proxy closes
    it.  True when the peer (the proxy) closed it first, False when
    the test released the hold first (teardown)."""
    sock.settimeout(0.25)
    while not release.is_set():
        try:
            chunk = sock.recv(1)
        except TimeoutError:
            continue
        except OSError:
            return True
        if not chunk:
            return True
    return False


def _main_complete_handler(
    requests: list[dict[str, object]],
    payload: bytes,
    content_type: str,
    released: threading.Event,
    request_event: threading.Event,
    closed: threading.Event,
) -> Callable[[socket.socket], None]:
    """Synthetic main upstream: complete response, then hold until
    the proxy closes the request-scoped connection."""

    def handle(client: socket.socket) -> None:
        line, headers, body = _read_http_request(client)
        requests.append({"line": line, "headers": headers, "body": body})
        request_event.set()
        _send_http_response(client, payload, content_type)
        if _hold_until_close(client, released):
            closed.set()

    return handle


def _main_hold_before_headers_handler(
    requests: list[dict[str, object]],
    released: threading.Event,
    request_event: threading.Event,
    closed: threading.Event,
) -> Callable[[socket.socket], None]:
    """Synthetic main upstream: accept and read the request, then
    hold before sending any response bytes (main held before
    headers)."""

    def handle(client: socket.socket) -> None:
        line, headers, body = _read_http_request(client)
        requests.append({"line": line, "headers": headers, "body": body})
        request_event.set()
        if _hold_until_close(client, released):
            closed.set()

    return handle


def _main_hold_mid_body_handler(
    requests: list[dict[str, object]],
    released: threading.Event,
    request_event: threading.Event,
    partial_event: threading.Event,
    closed: threading.Event,
) -> Callable[[socket.socket], None]:
    """Synthetic main upstream: declared length, partial body, then
    hold (completion withheld; main held during body)."""

    def handle(client: socket.socket) -> None:
        line, headers, body = _read_http_request(client)
        requests.append({"line": line, "headers": headers, "body": body})
        request_event.set()
        declared = 1_000_000
        head = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: application/json\r\n"
            b"Content-Length: " + str(declared).encode() + b"\r\n"
            b"\r\n"
        )
        client.sendall(head + b"{" * 512)
        partial_event.set()
        if _hold_until_close(client, released):
            closed.set()

    return handle


def _review_respond_handler(
    requests: list[dict[str, object]],
    payload: bytes,
    released: threading.Event,
    request_event: threading.Event,
    closed: threading.Event,
) -> Callable[[socket.socket], None]:
    """Synthetic review endpoint: one scripted batch envelope."""

    def handle(client: socket.socket) -> None:
        line, headers, body = _read_http_request(client)
        requests.append({"line": line, "headers": headers, "body": body})
        request_event.set()
        _send_http_response(client, payload, "application/json")
        if _hold_until_close(client, released):
            closed.set()

    return handle


def _review_hold_handler(
    requests: list[dict[str, object]],
    released: threading.Event,
    request_event: threading.Event,
    closed: threading.Event,
) -> Callable[[socket.socket], None]:
    """Synthetic review endpoint: accept and read the exchange
    request, then hold (no response ever)."""

    def handle(client: socket.socket) -> None:
        line, headers, body = _read_http_request(client)
        requests.append({"line": line, "headers": headers, "body": body})
        request_event.set()
        if _hold_until_close(client, released):
            closed.set()

    return handle


def _review_payload_replace_all() -> bytes:
    envelope = _envelope(_valid_inner([_prop("t0"), _prop("t1")]))
    envelope["usage"] = {
        "input_tokens": 11,
        "output_tokens": 17,
        "total_tokens": 28,
    }
    return json.dumps(envelope, ensure_ascii=False, separators=(",", ":")).encode()


def _usage_observer(
    records: list[dict[str, object]], event: threading.Event
) -> Callable[[dict[str, object]], None]:
    def observe(record: dict[str, object]) -> None:
        records.append(record)
        event.set()

    return observe


_REQUEST_SCOPED_THREAD_NAMES = (
    "concept-cancellation-watch",
    "concept-client-intake-guard",
    "concept-setup-guard",
    "concept-header-guard",
    "concept-client-delivery-guard",
)


def _request_scoped_survivors() -> list[threading.Thread]:
    return [
        thread
        for thread in threading.enumerate()
        if thread.is_alive() and thread.name in _REQUEST_SCOPED_THREAD_NAMES
    ]


def _wait_no_request_scoped_survivors(limit: float = 10.0) -> list[threading.Thread]:
    """Bounded wait for the handler-side owned cleanup (scope finish,
    guard release) that completes right after the client-visible
    response/quiet close."""
    deadline = time.monotonic() + limit
    while True:
        survivors = _request_scoped_survivors()
        if not survivors or time.monotonic() >= deadline:
            return survivors
        time.sleep(0.05)


def _owned_child_pids() -> set[int]:
    """The pids of the live/zombie children of THIS test process."""
    my_pid = os.getpid()
    pids: set[int] = set()
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            stat = Path(f"/proc/{entry}/stat").read_text()
        except OSError:
            continue
        fields = stat.rsplit(")", 1)[1].split()
        if int(fields[1]) == my_pid:
            pids.add(int(entry))
    return pids


def _wait_no_new_children(before: set[int], limit: float = 10.0) -> set[int]:
    """Bounded wait until no NEW owned child PIDs beyond ``before``
    remain; returns the surviving new PIDs (expected empty).

    Attribution is at the request boundary (order 030-a,
    requirements 5 and 8): a request is only held responsible for
    descendants it spawned itself, so pre-existing process-tree
    entries (whose lifetime belongs to their own owner and is
    tracked there) are excluded, while every child this request
    spawned must be actually reaped before the request is complete."""
    deadline = time.monotonic() + limit
    while True:
        survivors = _owned_child_pids() - before
        if not survivors or time.monotonic() >= deadline:
            return survivors
        time.sleep(0.05)


class _ReviewExchangePreDispatchTests(unittest.TestCase):
    """Actual ``run_review_exchange`` pre-dispatch boundary (order
    030-a, existing R4/R7/R8; root final review).

    The REAL transport entry - real codec, real owned native
    review_worker child, real IPC, the child's real
    resolver/connect/upload and the parent's real governed waits and
    reap - runs against one synthetic owned loopback-0 review
    endpoint (the only external substitute).  An observed
    cancellation that already exists at the post-pure-frame /
    pre-marker / pre-launch point must propagate the contained
    RequestCancelled with ZERO child, the attempted-dispatch marker
    FALSE and ZERO HTTP POST - both when it predates the exchange
    entry and when it lands after the REAL ``encode_request_frame``
    returns a valid frame but before the marker/launch.  The healthy
    control proves the actual child/HTTP/reap path and the attempted
    marker.  The stimuli are manual phase-cancellation Event sets,
    not native client RST/FIN claims; the actual FIN/RST watcher
    proofs live in :class:`_ProxyIntegrationTests` and in Root's
    native RST proofs.
    """

    def setUp(self) -> None:
        self.requests: list[dict[str, object]] = []
        self.released = threading.Event()
        self.request_event = threading.Event()
        self.closed = threading.Event()
        self.server = _RawLoopbackServer(
            "review-endpoint",
            _review_respond_handler(
                self.requests,
                b"{}",
                self.released,
                self.request_event,
                self.closed,
            ),
        )
        self.server.start()

    def tearDown(self) -> None:
        # Bounded honest teardown: release any held client, then
        # actually stop/close/join the owned endpoint.
        self.released.set()
        self.assertTrue(self.server.close(), "review endpoint not joined")

    @staticmethod
    def _worker_path() -> Path:
        return Path(__file__).resolve().parents[1] / "review_worker.py"

    @staticmethod
    def _fds() -> set[int]:
        return {int(name) for name in os.listdir("/proc/self/fd")}

    def _call_exchange(self, port: int) -> tuple[int, bytes]:
        return review_transport.run_review_exchange(
            scheme="http",
            host="127.0.0.1",
            port=port,
            path="/v1/responses",
            body=b'{"model":"test-model"}',
            auth="fake-key",
            deadline=time.monotonic() + 20.0,
            worker_path=self._worker_path(),
        )

    def test_healthy_actual_child_post_200_reaped(self) -> None:
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        _RecordingPopen.created.clear()
        before_fds = self._fds()
        children_before = _owned_child_pids()
        try:
            scope.start()
            with mock.patch.object(subprocess, "Popen", _RecordingPopen):
                status, payload = self._call_exchange(self.server.port)
            # The real owned worker child performed the real HTTP
            # exchange against the owned endpoint: one POST, one 200
            # with the scripted payload.
            self.assertEqual(status, 200)
            self.assertEqual(payload, b"{}")
            self.assertEqual(len(self.requests), 1)
            self.assertTrue(str(self.requests[0]["line"]).startswith("POST /v1"))
            # The exact owned child was recorded with its real pid and
            # was ACTUALLY reaped by the owned cleanup before return:
            # the kernel itself reports the wait as already done and
            # the /proc entry is gone.
            self.assertEqual(len(_RecordingPopen.created), 1)
            process = _RecordingPopen.created[0]
            pid = process.pid
            self.assertIsInstance(pid, int)
            self.assertIsNotNone(pid)
            self.assertGreater(pid, 0)
            self.assertEqual(process.returncode, 0)
            with self.assertRaises(ChildProcessError):
                os.waitpid(pid, os.WNOHANG)
            self.assertFalse(Path(f"/proc/{pid}/stat").exists())
            # The real worker closed its real TCP connection (the
            # owned endpoint observed the close), and this exchange
            # counts as one attempted dispatch for the accounting
            # boundary.
            self.assertTrue(self.closed.wait(10.0))
            self.assertTrue(scope.review_dispatch_attempted())
            self.assertFalse(scope.cancelled())
        finally:
            scope.finish()
            peer.close()
            local.close()
        # Nothing survives the actual exchange: no child (live or
        # zombie) and no new file descriptor.
        self.assertEqual(_wait_no_new_children(children_before, 10.0), set())
        self.assertEqual(self._fds() - before_fds, set())
        watchers = [
            thread
            for thread in threading.enumerate()
            if thread.name == "concept-cancellation-watch"
        ]
        self.assertEqual(watchers, [])

    def test_cancel_before_exchange_entry_starts_zero(self) -> None:
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        _RecordingPopen.created.clear()
        before_fds = self._fds()
        children_before = _owned_child_pids()
        try:
            scope.start()
            # Deterministic phase-cancellation stimulus at the SAME
            # scope state the watcher would set - before the actual
            # exchange entry (manual; not a native RST claim).
            scope._cancelled.set()
            with (
                mock.patch.object(subprocess, "Popen", _RecordingPopen),
                self.assertRaises(request_lifecycle.RequestCancelled),
            ):
                self._call_exchange(self.server.port)
            # Already-observed pre-dispatch cancellation: the
            # dedicated exception propagated BEFORE the marker and the
            # owned launch - no child, no attempted-dispatch count,
            # no POST can exist for an already-canceled request.
            self.assertEqual(_RecordingPopen.created, [])
            self.assertFalse(scope.review_dispatch_attempted())
            self.assertEqual(len(self.requests), 0)
            self.assertFalse(self.request_event.is_set())
        finally:
            scope.finish()
            peer.close()
            local.close()
        self.assertEqual(_wait_no_new_children(children_before, 10.0), set())
        self.assertEqual(self._fds() - before_fds, set())

    def test_cancel_after_real_frame_before_marker_starts_zero(self) -> None:
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        _RecordingPopen.created.clear()
        before_fds = self._fds()
        children_before = _owned_child_pids()
        real_frame = review_transport.encode_request_frame

        def cancel_after_real_frame(
            *,
            scheme: str,
            host: str,
            port: int | None,
            path: str,
            auth: str | None,
            remaining_seconds: float,
            body: bytes,
        ) -> bytes:
            # Transparent: the REAL codec runs to a valid frame; only
            # THEN is the phase-cancellation stimulus set - after the
            # pure frame bounds, before marker/launch (same scope
            # state the watcher would set; manual, not native RST).
            frame = real_frame(
                scheme=scheme,
                host=host,
                port=port,
                path=path,
                auth=auth,
                remaining_seconds=remaining_seconds,
                body=body,
            )
            scope._cancelled.set()
            return frame

        try:
            scope.start()
            with (
                mock.patch.object(subprocess, "Popen", _RecordingPopen),
                mock.patch.object(
                    review_transport,
                    "encode_request_frame",
                    cancel_after_real_frame,
                ),
                self.assertRaises(request_lifecycle.RequestCancelled),
            ):
                self._call_exchange(self.server.port)
            self.assertEqual(_RecordingPopen.created, [])
            self.assertFalse(scope.review_dispatch_attempted())
            self.assertEqual(len(self.requests), 0)
            self.assertFalse(self.request_event.is_set())
        finally:
            scope.finish()
            peer.close()
            local.close()
        self.assertEqual(_wait_no_new_children(children_before, 10.0), set())
        self.assertEqual(self._fds() - before_fds, set())


class _ProxyIntegrationTests(unittest.TestCase):
    """Real TCP client -> real admission/Handler/main capture/Engine/
    Pandoc/ROCorpus/029 selector/ResponsesReviewer child exchange/
    parser/accept/compose/render positives and cancellations (order
    030-a, requirement 8).  Only the main upstream and the review
    endpoint are synthetic loopback-0 servers; observer hooks
    delegate the actual work.  Cancellation clients write-half-close
    (FIN) or RST after the fully valid ingress - the single-threaded
    client owns its socket end-to-end, so the transport event is
    delivered without a concurrent reader deferring it.  Finite
    owned children/loopback0 only (requirements 8 and 12)."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)
        self.servers: list[_RawLoopbackServer] = []
        self.threads: list[threading.Thread] = []
        self.proxy_server: proxy.ConceptProxy | None = None

    def tearDown(self) -> None:
        proxy_server = self.proxy_server
        if proxy_server is not None:
            proxy_server.shutdown()
            proxy_server.server_close()
        survivors = [server for server in self.servers if not server.close()]
        for thread in self.threads:
            thread.join(5.0)
        self.assertFalse(
            survivors, f"owned loopback servers still alive: {survivors}"
        )
        self.temp.cleanup()

    def _new_reviewer(self, port: int) -> ResponsesReviewer:
        return ResponsesReviewer(
            f"http://127.0.0.1:{port}/v1",
            "test-model",
            timeout=8.0,
            api_key="fake-key",
        )

    def _start_proxy(
        self,
        main_port: int,
        engine: proxy.RepairEngine,
        records: list[dict[str, object]],
        observed: threading.Event,
    ) -> proxy.ConceptProxy:
        proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{main_port}",
            engine,
            usage_observer=_usage_observer(records, observed),
        )
        self.proxy_server = proxy_server
        thread = threading.Thread(
            target=proxy_server.serve_forever, name="proxy-serve", daemon=False
        )
        thread.start()
        self.threads.append(thread)
        return proxy_server

    def test_normal_json_word_positive_full_pipeline(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._start_proxy(main.port, engine, records, observed)

        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client, _contract_body(False))
            status, headers, body = _read_http_response(client)
        finally:
            client.close()
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("content-type"), "application/json")
        envelope = json.loads(body.decode("utf-8"))
        output = cast("list[dict[str, object]]", envelope["output"])
        message = output[0]
        content = cast("list[dict[str, object]]", message["content"])
        self.assertEqual(
            cast("str", content[0]["text"]),
            "To je tako zapisano, to je tako zapisano.",
        )
        self.assertEqual(len(main_requests), 1)
        self.assertEqual(len(review_requests), 1)
        self.assertTrue(review_event.is_set())
        self.assertEqual(
            records,
            [
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 11,
                        "output_tokens": 17,
                        "total_tokens": 28,
                    },
                }
            ],
        )
        # The handler consumed the request details on delivery (one
        # operator observation observed above, no trace dir here):
        # nothing text-bearing may remain for the next request.
        self.assertEqual(engine.take_details(), [])
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_normal_sse_phrase_positive_full_pipeline(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        sse_payload = _sse_delta("m", TEXT) + _sse_completed()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                sse_payload,
                "text/event-stream",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._start_proxy(main.port, engine, records, observed)

        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client, _contract_body(True))
            status, headers, body = _read_http_response(client)
        finally:
            client.close()
        self.assertEqual(status, 200)
        self.assertTrue(
            headers.get("content-type", "").startswith("text/event-stream")
        )
        self.assertIn(b"To je tako zapisano, to je tako zapisano.", body)
        self.assertNotIn(b"presenetliv", body)
        self.assertEqual(len(main_requests), 1)
        self.assertEqual(len(review_requests), 1)
        self.assertEqual(
            records,
            [
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 11,
                        "output_tokens": 17,
                        "total_tokens": 28,
                    },
                }
            ],
        )
        self.assertEqual(engine.take_details(), [])
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_fin_before_headers_cancels_before_downstream_review(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_hold_before_headers_handler(
                main_requests, main_released, main_event, main_closed
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_hold_handler(
                review_requests, review_released, review_event, review_closed
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._start_proxy(main.port, engine, records, observed)

        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client, _contract_body(False))
            # The owned setup write completed: the synthetic main saw
            # the whole request before the client write-half-closes.
            self.assertTrue(main_event.wait(15.0))
            time.sleep(0.3)
            # FIN (write-half close); the read direction stays open
            # so the drain proves the quiet close.
            client.shutdown(socket.SHUT_WR)
            self.assertTrue(observed.wait(20.0))
            received = _drain_client(client, 10.0)
        finally:
            client.close()
        self.assertEqual(received, b"")
        self.assertEqual(
            records, [{"review_calls": 0, "reviewer_usage": "unknown"}]
        )
        self.assertEqual(len(main_requests), 1)
        self.assertEqual(len(review_requests), 0)
        # The owned upstream connection was actually closed on abort.
        self.assertTrue(main_closed.wait(10.0))
        self.assertEqual(engine.take_details(), [])
        self.assertIsNone(engine._review_usage)
        self.assertIsNone(engine._scope)
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_rst_before_headers_cancels_before_downstream_review(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_hold_before_headers_handler(
                main_requests, main_released, main_event, main_closed
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_hold_handler(
                review_requests, review_released, review_event, review_closed
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._start_proxy(main.port, engine, records, observed)

        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client, _contract_body(False))
            self.assertTrue(main_event.wait(15.0))
            time.sleep(0.3)
            # RST: the hard transport error is also cancellation; the
            # client refuses all further data, so quiet close is
            # asserted through the observation and owned state.
            client.setsockopt(
                socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0)
            )
            client.close()
            self.assertTrue(observed.wait(20.0))
        finally:
            client.close()
        self.assertEqual(
            records, [{"review_calls": 0, "reviewer_usage": "unknown"}]
        )
        self.assertEqual(len(main_requests), 1)
        self.assertEqual(len(review_requests), 0)
        self.assertTrue(main_closed.wait(10.0))
        self.assertEqual(engine.take_details(), [])
        self.assertIsNone(engine._scope)
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_fin_during_body_cancels_owned_capture(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        partial_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_hold_mid_body_handler(
                main_requests,
                main_released,
                main_event,
                partial_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_hold_handler(
                review_requests, review_released, review_event, review_closed
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._start_proxy(main.port, engine, records, observed)

        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client, _contract_body(False))
            self.assertTrue(main_event.wait(15.0))
            self.assertTrue(partial_event.wait(15.0))
            # The proxy is now inside the owned body capture.
            time.sleep(0.5)
            client.shutdown(socket.SHUT_WR)  # FIN
            self.assertTrue(observed.wait(20.0))
            received = _drain_client(client, 10.0)
        finally:
            client.close()
        self.assertEqual(received, b"")
        self.assertEqual(
            records, [{"review_calls": 0, "reviewer_usage": "unknown"}]
        )
        self.assertEqual(len(main_requests), 1)
        self.assertEqual(len(review_requests), 0)
        self.assertTrue(main_closed.wait(10.0))
        self.assertEqual(engine.take_details(), [])
        self.assertIsNone(engine._scope)
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_review_already_started_cancelled_one_attempt_reaped(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_hold_handler(
                review_requests, review_released, review_event, review_closed
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._start_proxy(main.port, engine, records, observed)

        child_pids_before = _owned_child_pids()
        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client, _contract_body(False))
            # The ACTUAL owned reviewer child connected to the
            # synthetic review endpoint and sent its exchange request.
            self.assertTrue(review_event.wait(20.0))
            time.sleep(0.2)
            client.shutdown(socket.SHUT_WR)  # FIN
            self.assertTrue(observed.wait(20.0))
            received = _drain_client(client, 10.0)
        finally:
            client.close()
        self.assertEqual(received, b"")
        # One counted actual attempt; no validated usage; no retry.
        self.assertEqual(
            records, [{"review_calls": 1, "reviewer_usage": "unknown"}]
        )
        self.assertEqual(len(review_requests), 1)
        self.assertEqual(
            _wait_no_new_children(child_pids_before, 10.0), set()
        )
        self.assertEqual(engine.take_details(), [])
        self.assertIsNone(engine._review_usage)
        self.assertIsNone(engine._scope)
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_queued_cancelled_request_never_starts_main(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._start_proxy(main.port, engine, records, observed)

        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        _post_to_proxy(client, _contract_body(False))
        # The fully valid ingress is complete and the single-threaded
        # client closes (FIN) before any future main work: the bounded
        # synchronous first check must catch it before forward.
        client.close()
        self.assertTrue(observed.wait(20.0))
        self.assertEqual(
            records, [{"review_calls": 0, "reviewer_usage": "unknown"}]
        )
        self.assertEqual(len(main_requests), 0)
        self.assertEqual(len(review_requests), 0)
        self.assertEqual(engine.take_details(), [])
        self.assertIsNone(engine._scope)
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_same_proxy_recovery_after_cancelled_request(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        released = threading.Event()
        review_released = threading.Event()
        first_request = threading.Event()
        review_event = threading.Event()
        first_closed = threading.Event()
        review_closed = threading.Event()
        state = {"hold_first": True}

        def main_handler(client: socket.socket) -> None:
            line, headers, body = _read_http_request(client)
            main_requests.append({"line": line, "headers": headers, "body": body})
            if state["hold_first"]:
                # Request 1: main held before headers; the client
                # write-half-closes and the request must be canceled.
                state["hold_first"] = False
                first_request.set()
                if _hold_until_close(client, released):
                    first_closed.set()
            else:
                # Request 2: healthy complete response on the SAME
                # proxy instance (recovery).
                _send_http_response(
                    client, _json_completed(TEXT), "application/json"
                )
                _hold_until_close(client, released)

        main = _RawLoopbackServer("main-upstream", main_handler)
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._start_proxy(main.port, engine, records, observed)

        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client, _contract_body(False))
            self.assertTrue(first_request.wait(15.0))
            time.sleep(0.3)
            client.shutdown(socket.SHUT_WR)  # FIN
            self.assertTrue(observed.wait(20.0))
            received = _drain_client(client, 10.0)
        finally:
            client.close()
        self.assertEqual(received, b"")
        self.assertEqual(len(records), 1)
        self.assertEqual(
            records[0], {"review_calls": 0, "reviewer_usage": "unknown"}
        )
        self.assertEqual(len(review_requests), 0)
        self.assertTrue(first_closed.wait(10.0))

        # The same proxy instance now serves a healthy request to
        # completion: no foreign-request/resource effect.
        client2 = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client2, _contract_body(False))
            status, _headers, body2 = _read_http_response(client2)
        finally:
            client2.close()
        deadline = time.monotonic() + 20.0
        while len(records) < 2:
            self.assertTrue(
                time.monotonic() < deadline, "second observation never fired"
            )
            time.sleep(0.05)
        self.assertEqual(status, 200)
        envelope = json.loads(body2.decode("utf-8"))
        output = cast("list[dict[str, object]]", envelope["output"])
        message = output[0]
        content = cast("list[dict[str, object]]", message["content"])
        self.assertEqual(
            cast("str", content[0]["text"]),
            "To je tako zapisano, to je tako zapisano.",
        )
        self.assertEqual(len(records), 2)
        self.assertEqual(
            records[1],
            {
                "review_calls": 1,
                "reviewer_usage": {
                    "input_tokens": 11,
                    "output_tokens": 17,
                    "total_tokens": 28,
                },
            },
        )
        self.assertEqual(len(main_requests), 2)
        self.assertEqual(len(review_requests), 1)
        self.assertEqual(_wait_no_request_scoped_survivors(), [])


class _ProxyAccountingTests(unittest.TestCase):
    """Request-local abort accounting (order 030-a, requirement 7)
    driven at the real engine boundary: real engine, real scope,
    real corpus and the real owned reviewer exchange.  DIRECT-ENGINE
    evidence, labeled separately from the actual Handler/TCP
    evidence in _ProxyIntegrationTests: the operator-record
    aggregation is the ACTUAL ConceptProxy.observe_usage boundary
    (drained details -> one content-free record -> the operator
    usage observer), exactly as the Handler applies it on abort.
    The cancellation state is the exact scope state the owned
    watcher sets on an observed disconnect."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)
        self.servers: list[_RawLoopbackServer] = []
        self.threads: list[threading.Thread] = []
        self.proxy_server: proxy.ConceptProxy | None = None

    def tearDown(self) -> None:
        proxy_server = self.proxy_server
        if proxy_server is not None:
            proxy_server.shutdown()
            proxy_server.server_close()
        survivors = [server for server in self.servers if not server.close()]
        for thread in self.threads:
            thread.join(5.0)
        self.assertFalse(
            survivors, f"owned loopback servers still alive: {survivors}"
        )
        self.temp.cleanup()

    def _proxy_for_observation(
        self,
        engine: proxy.RepairEngine,
        port: int,
        records: list[dict[str, object]],
        observed: threading.Event,
    ) -> proxy.ConceptProxy:
        # No traffic flows through this proxy instance; it provides
        # the ACTUAL operator-record aggregation boundary.
        proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{port}",
            engine,
            usage_observer=_usage_observer(records, observed),
        )
        self.proxy_server = proxy_server
        # Fully owned instance: the accepted serve_forever loop runs
        # in one owned (non-daemon) thread actually joined in
        # teardown (no traffic flows; it provides the ACTUAL
        # operator-record aggregation boundary).
        thread = threading.Thread(
            target=proxy_server.serve_forever,
            name="proxy-serve-accounting",
            daemon=False,
        )
        thread.start()
        self.threads.append(thread)
        return proxy_server

    def test_pre_dispatch_cancel_zero_calls_unknown_usage(self) -> None:
        review_requests: list[dict[str, object]] = []
        review_released = threading.Event()
        review_event = threading.Event()
        review_closed = threading.Event()
        review = _RawLoopbackServer(
            "review-upstream",
            _review_hold_handler(
                review_requests, review_released, review_event, review_closed
            ),
        )
        review.start()
        self.servers.append(review)
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        scope.start()
        try:
            # Deterministic pre-dispatch cancellation: the same scope
            # state the watcher would set, set before any engine work.
            scope._cancelled.set()
            reviewer = ResponsesReviewer(
                f"http://127.0.0.1:{review.port}/v1",
                "test-model",
                timeout=8.0,
                api_key="fake-key",
            )
            engine = proxy.RepairEngine(
                self.db, reviewer, pandoc=_real_spec()
            )
            records: list[dict[str, object]] = []
            observed = threading.Event()
            proxy_server = self._proxy_for_observation(
                engine, review.port, records, observed
            )
            engine.begin_request(scope)
            child_pids_before = _owned_child_pids()
            with self.assertRaises(request_lifecycle.RequestCancelled):
                engine.repair(TEXT)
            # No new model call / optional phase after cancellation:
            # no child existed or was left, no dispatch was attempted.
            self.assertFalse(scope.review_dispatch_attempted())
            self.assertEqual(len(review_requests), 0)
            self.assertEqual(
                _wait_no_new_children(child_pids_before, 10.0), set()
            )
            engine.abort_request(proxy_server.observe_usage)
            self.assertTrue(observed.is_set())
            self.assertEqual(len(records), 1)
            self.assertEqual(
                records[0], {"review_calls": 0, "reviewer_usage": "unknown"}
            )
            self.assertEqual(engine.take_details(), [])
            self.assertIsNone(engine._review_usage)
            self.assertIsNone(engine._scope)
        finally:
            scope.finish()
            peer.close()
            local.close()

    def test_known_usage_preserved_through_later_cpu_cancellation(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        scope.start()
        try:
            inner = ResponsesReviewer(
                f"http://127.0.0.1:{review.port}/v1",
                "test-model",
                timeout=8.0,
                api_key="fake-key",
            )

            class _PostCompletionCancelReviewer:
                """Transparent: delegate to the REAL owned exchange,
                then cancel after the actual attempt completed with
                validated usage - a later CPU cancellation."""

                def __init__(
                    self,
                    inner: ResponsesReviewer,
                    cancelled_scope: request_lifecycle.CancellationScope,
                ) -> None:
                    self._inner = inner
                    self._scope = cancelled_scope

                def review_batch(
                    self, sentence: str, targets: tuple[BatchTarget, ...]
                ) -> BatchResult:
                    result = self._inner.review_batch(sentence, targets)
                    self._scope._cancelled.set()
                    return result

            engine = proxy.RepairEngine(
                self.db,
                _PostCompletionCancelReviewer(inner, scope),
                pandoc=_real_spec(),
            )
            records: list[dict[str, object]] = []
            observed = threading.Event()
            proxy_server = self._proxy_for_observation(
                engine, review.port, records, observed
            )
            engine.begin_request(scope)
            child_pids_before = _owned_child_pids()
            with self.assertRaises(request_lifecycle.RequestCancelled):
                engine.repair(TEXT)
            self.assertTrue(scope.review_dispatch_attempted())
            self.assertEqual(len(review_requests), 1)
            engine.abort_request(proxy_server.observe_usage)
            self.assertTrue(observed.is_set())
            self.assertEqual(len(records), 1)
            # The completed known result remains known through the
            # later CPU cancellation (one content-free observation,
            # no carryover, no re-observed usage).
            self.assertEqual(
                records[0],
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 11,
                        "output_tokens": 17,
                        "total_tokens": 28,
                    },
                },
            )
            self.assertEqual(engine.take_details(), [])
            self.assertIsNone(engine._review_usage)
            self.assertIsNone(engine._scope)
            self.assertEqual(
                _wait_no_new_children(child_pids_before, 10.0), set()
            )
        finally:
            scope.finish()
            peer.close()
            local.close()


class _CorpusNativeCancellationTests(unittest.TestCase):
    """Native SQLite cooperative cancellation inside the REAL
    read-only corpus (order 030-a, requirements 4 and 8): the
    composed native progress handler maps an observed cancellation
    interrupt to RequestCancelled - never a quota or transport
    failure - while the base budget handler state stays untouched.
    The constructor captures the current active request's check on
    the owner thread (effective during its schema SQL); the owner
    may additionally adopt it explicitly for work begun without an
    active scope, the same closure capture the proxy applies."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_cancelled_before_construction_maps_native_interrupt(self) -> None:
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        scope.start()
        try:
            # Deterministic: the same scope state the owned watcher
            # sets on an observed disconnect, set before the real
            # construction SQL runs under the composed native
            # progress handler.
            scope._cancelled.set()
            with self.assertRaises(request_lifecycle.RequestCancelled):
                RuntimeCorpus(self.db, progress_interval=1)
        finally:
            scope.finish()
            peer.close()
            local.close()

    def test_cancelled_query_maps_native_interrupt(self) -> None:
        local, peer = socket.socketpair()
        scope = request_lifecycle.CancellationScope(local)
        scope.start()
        try:
            # The real construction completes UNcancelled; the
            # per-request scope check is adopted and set BEFORE the
            # first data query (the exact proxy adoption order).
            corpus = RuntimeCorpus(self.db, progress_interval=1)
            corpus.adopt_cancelled(scope.cancelled)
            scope._cancelled.set()
            try:
                with self.assertRaises(request_lifecycle.RequestCancelled):
                    corpus.unigram("tako")
            finally:
                corpus.close()
        finally:
            scope.finish()
            peer.close()
            local.close()

    def test_uncancelled_adopted_corpus_unaffected_control(self) -> None:
        # Healthy control: the same adopted-check path with no
        # observed cancellation leaves the native corpus behavior
        # exactly as before (no new failure class, no drift).
        corpus = RuntimeCorpus(self.db, progress_interval=1)
        corpus.adopt_cancelled(None)
        try:
            evidence = corpus.unigram("tako")
            self.assertEqual(evidence.count, 100)
            self.assertEqual(corpus.alternatives("je", "zapisano"), [("tako", 20)])
        finally:
            corpus.close()


class _CleanupFaultScope(request_lifecycle.CancellationScope):
    """Transparent scope for the finisher authority regressions
    (order 030-a, requirement 5): the real constructor, start,
    cancellation checks and finish all actually run; only the
    first ``finish()`` attempt's fault is injected - one distinct
    current cleanup MemoryError raised before the actual owned
    watcher join.  Every later attempt performs the actual finish
    (the real native join completes and the scope finishes)."""

    inject_cleanup_fault: ClassVar[bool] = True

    def finish(self) -> None:
        if type(self).inject_cleanup_fault:
            type(self).inject_cleanup_fault = False
            raise MemoryError("cleanup-fault")
        super().finish()


class _PostConstructionCancelCorpus(RuntimeCorpus):
    """Transparent corpus for the late handoff regression (order
    030-a, requirements 4 and 5): the real constructor runs
    unchanged (real schema SQL, budgets and controls); only the
    handoff after construction is injected - the exact scope state
    the owned watcher sets on an observed disconnect."""

    cancel_after_construction: ClassVar[Callable[[], None] | None] = None

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
        super().__init__(
            path,
            max_statements=max_statements,
            max_rows_per_query=max_rows_per_query,
            max_rows_total=max_rows_total,
            progress_interval=progress_interval,
            max_progress_callbacks=max_progress_callbacks,
        )
        hook = type(self).cancel_after_construction
        if hook is not None:
            hook()


class _ControlPriorityCorpus(RuntimeCorpus):
    """Transparent corpus for the control priority matrix (order
    030-a, requirement 5): the real constructor, adoption and close
    all run unchanged; only the injected handoff/cleanup controls
    are substituted.  ``close_completed`` records that the real
    close ran before the injected close fault."""

    adopt_fault: ClassVar[BaseException | None] = None
    close_fault: ClassVar[BaseException | None] = None
    close_completed: ClassVar[bool] = False
    # Phase-cancellation stimulus for the cancel-pending rows
    # (deterministic stand-in for a native peer disconnect observed
    # by the owned watcher; the actual FIN/RST watcher proofs live in
    # _ProxyIntegrationTests and Root's native RST proofs).  The
    # event is set AFTER the real adoption, inside the corpus-owned
    # region: a pre-entry cancel stops at the pre-corpus boundary
    # and could never prove the owned finally (root fifteenth
    # review).
    cancel_in_adopt: ClassVar[bool] = False
    cancel_scope: ClassVar[request_lifecycle.CancellationScope | None] = None

    def adopt_cancelled(self, cancelled: Callable[[], bool] | None) -> None:
        super().adopt_cancelled(cancelled)
        if type(self).cancel_in_adopt:
            scope = type(self).cancel_scope
            if scope is not None:
                scope._cancelled.set()
        fault = type(self).adopt_fault
        if fault is not None:
            raise fault

    def close(self) -> None:
        super().close()
        type(self).close_completed = True
        fault = type(self).close_fault
        if fault is not None:
            raise fault


def _swap_attr(owner: object, name: str, value: object) -> object:
    """One transparent monkeypatch seam (order 030-a, requirement
    8): replace ``owner.name`` with ``value`` and return the exact
    previous value for restore.  The seam is deliberately
    parameterized because the repo ruff config rejects constant-name
    getattr/setattr while mypy rejects direct module-attribute and
    instance-method assignment on imported/product names; no real
    work is substituted (every observer delegates to the product).
    """
    saved = getattr(owner, name)
    setattr(owner, name, value)
    return saved


class _ProxyLateHandoffRegressionTests(unittest.TestCase):
    """Bounded actual-boundary regressions for the late-handoff
    accounting/ownership/control failures of order 030-a
    requirements 5, 6 and 7 (root twelfth-fourteenth reviews):
    cancellation after the real repair fully returns emits ONE
    authoritative 0/1 known/unknown record with the text-bearing
    details drained and discarded; cancellation after the first
    operator observation before delivery is never re-observed
    (exactly one record per request); cancellation after the real
    corpus constructor closes the read-only handle on every path;
    the Handler finisher receives only this operation's explicitly
    tracked control (an unrelated already-handled ambient error is
    never borrowed, the first own MemoryError is never caught into
    a generated 502, and a later nonordinary cleanup control is
    never suppressed by an ambient or ordinary error); and the
    corpus-owned region keeps the exact first control identity for
    the entire region while a later nonordinary cleanup control
    propagates over an ordinary pending.  All actual product work
    runs through transparent delegation; only the external main/
    review endpoints are synthetic (requirement 8).  Local fixture
    contract (root fifteenth review): the direct-handler rows drive
    the real Handler exactly once through the transparent native
    finish_request boundary with the POST already available (the
    stdlib constructor would otherwise run setup/handle/finish with
    no request bytes and close its streams before the handler could
    be driven); the deliberate scope-event injections are
    phase-cancellation stimuli - deterministic stand-ins for a
    native peer disconnect observed by the owned watcher - and are
    not native peer-RST evidence, which the actual FIN/RST
    integration rows and Root's native RST proofs establish
    separately."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _build_corpus(self.root)
        self.servers: list[_RawLoopbackServer] = []
        self.threads: list[threading.Thread] = []
        self.proxy_server: proxy.ConceptProxy | None = None
        self._serving = False
        self._handler_conn: socket.socket | None = None

    def tearDown(self) -> None:
        proxy_server = self.proxy_server
        if proxy_server is not None:
            if self._serving:
                proxy_server.shutdown()
            # The accepting-loop close boundary: the owned admission
            # lifecycle stops and actually joins before the listener
            # socket closes (correct for served and never-served
            # owners alike).
            proxy_server.server_close()
        handler_conn = self._handler_conn
        if handler_conn is not None:
            with contextlib.suppress(OSError):
                handler_conn.close()
        survivors = [server for server in self.servers if not server.close()]
        for thread in self.threads:
            thread.join(5.0)
        alive = [thread for thread in self.threads if thread.is_alive()]
        self.assertFalse(
            survivors, f"owned loopback servers still alive: {survivors}"
        )
        self.assertFalse(
            alive, f"owned serve threads did not actually join: {alive}"
        )
        self.temp.cleanup()

    def _new_reviewer(self, port: int) -> ResponsesReviewer:
        return ResponsesReviewer(
            f"http://127.0.0.1:{port}/v1",
            "test-model",
            timeout=8.0,
            api_key="fake-key",
        )

    def _start_proxy(
        self,
        main_port: int,
        engine: proxy.RepairEngine,
        observer: Callable[[dict[str, object]], None],
    ) -> proxy.ConceptProxy:
        proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{main_port}",
            engine,
            usage_observer=observer,
        )
        self.proxy_server = proxy_server
        self._serving = True
        thread = threading.Thread(
            target=proxy_server.serve_forever,
            name="proxy-serve-late",
            daemon=False,
        )
        thread.start()
        self.threads.append(thread)
        return proxy_server

    def _capture_begin(
        self, engine: proxy.RepairEngine
    ) -> list[request_lifecycle.CancellationScope]:
        captured: list[request_lifecycle.CancellationScope] = []
        real_begin = engine.begin_request

        def _begin_capture(
            scope: request_lifecycle.CancellationScope | None = None,
        ) -> None:
            real_begin(scope)
            if scope is not None:
                captured.append(scope)

        # Typed one-request observer seam: the exact product boundary
        # is replaced with a transparent delegate (requirement 8).
        _swap_attr(engine, "begin_request", _begin_capture)
        return captured

    def _open_fds_for(self, path: Path) -> set[int]:
        target = path.resolve()
        fds: set[int] = set()
        for entry in os.listdir("/proc/self/fd"):
            if not entry.isdigit():
                continue
            try:
                if Path(f"/proc/self/fd/{entry}").resolve() == target:
                    fds.add(int(entry))
            except OSError:
                continue
        return fds

    def _accept_direct(
        self,
        proxy_server: proxy.ConceptProxy,
        client: socket.socket,
    ) -> tuple[socket.socket, tuple[str, int]]:
        # The one-shot request is fully available BEFORE the real
        # Handler is constructed: the stdlib request-handler
        # constructor runs setup/handle/finish immediately, so a
        # constructor with no request bytes would close its streams
        # before the handler could ever be driven (root fifteenth
        # review, native constructor-premise proof).  The POST uses
        # Connection: close so the native handle loop covers exactly
        # this one request; the test then drives the transparent
        # native finish_request boundary exactly once (real stdlib
        # setup/handle/finish and Scope cleanup), on this thread
        # without a serve loop (never-served owner).
        _post_to_proxy(client, _contract_body(False), close=True)
        conn, addr = proxy_server.socket.accept()
        self._handler_conn = conn
        return conn, addr

    def _direct_proxy(
        self,
        main_port: int,
        engine: proxy.RepairEngine,
        observer: Callable[[dict[str, object]], None],
    ) -> proxy.ConceptProxy:
        proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{main_port}",
            engine,
            usage_observer=observer,
        )
        self.proxy_server = proxy_server
        return proxy_server

    def test_cancel_after_repair_return_emits_one_authoritative_record(
        self,
    ) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        captured = self._capture_begin(engine)
        cancelled_once = False
        real_repair = engine.repair

        def _repair_then_cancel(text: str) -> str:
            # The handoff: the ACTUAL repair fully returned and the
            # details are already populated.  Phase-cancellation
            # stimulus (deterministic stand-in for a native peer
            # disconnect observed by the owned watcher before the
            # Handler takes the details; the actual FIN/RST watcher
            # proofs live in _ProxyIntegrationTests and Root's
            # native RST proofs).
            nonlocal cancelled_once
            answer = real_repair(text)
            if not cancelled_once and captured:
                cancelled_once = True
                captured[-1]._cancelled.set()
            return answer

        # Typed one-request observer seam: the exact product repair
        # boundary is replaced with a transparent delegate.
        _swap_attr(engine, "repair", _repair_then_cancel)
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._start_proxy(
            main.port, engine, _usage_observer(records, observed)
        )
        child_pids_before = _owned_child_pids()
        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client, _contract_body(False))
            self.assertTrue(observed.wait(20.0))
            received = _drain_client(client, 10.0)
        finally:
            client.close()
        # Quiet close: the cancellation won before delivery.
        self.assertEqual(received, b"")
        # Exactly ONE authoritative content-free record derived from
        # the engine's own state: the actual one attempt and the
        # completed known usage preserved; the text-bearing details
        # were drained and discarded, never re-aggregated.
        self.assertEqual(
            records,
            [
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 11,
                        "output_tokens": 17,
                        "total_tokens": 28,
                    },
                }
            ],
        )
        self.assertEqual(len(review_requests), 1)
        self.assertEqual(engine.take_details(), [])
        self.assertIsNone(engine._review_usage)
        self.assertIsNone(engine._scope)
        self.assertEqual(_wait_no_new_children(child_pids_before, 10.0), set())
        self.assertEqual(_wait_no_request_scoped_survivors(), [])
        # Same-proxy recovery: the next request is healthy.
        client2 = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client2, _contract_body(False))
            status, _headers, body = _read_http_response(client2)
        finally:
            client2.close()
        self.assertEqual(status, 200)
        envelope = json.loads(body.decode("utf-8"))
        output = cast("list[dict[str, object]]", envelope["output"])
        message = output[0]
        content = cast("list[dict[str, object]]", message["content"])
        self.assertEqual(
            cast("str", content[0]["text"]),
            "To je tako zapisano, to je tako zapisano.",
        )
        self.assertEqual(len(records), 2)
        self.assertEqual(records[1], records[0])
        self.assertEqual(len(main_requests), 2)
        self.assertEqual(len(review_requests), 2)

    def test_cancel_after_observation_before_delivery_observes_exactly_once(
        self,
    ) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        captured = self._capture_begin(engine)
        records: list[dict[str, object]] = []
        observed = threading.Event()

        def _observing_cancel_observer(record: dict[str, object]) -> None:
            # The ACTUAL operator callback: after appending its real
            # first record, the phase-cancellation stimulus fires -
            # a deterministic stand-in for a native peer disconnect
            # observed by the owned watcher after the first
            # observation, before delivery (the actual FIN/RST
            # watcher proofs live in _ProxyIntegrationTests and
            # Root's native RST proofs).
            records.append(record)
            observed.set()
            if captured:
                captured[-1]._cancelled.set()

        proxy_server = self._start_proxy(
            main.port, engine, _observing_cancel_observer
        )
        child_pids_before = _owned_child_pids()
        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        try:
            _post_to_proxy(client, _contract_body(False))
            self.assertTrue(observed.wait(20.0))
            received = _drain_client(client, 10.0)
        finally:
            client.close()
        # Quiet close: the cancellation won before delivery.
        self.assertEqual(received, b"")
        # Exactly ONE operator record for this POST: the abort must
        # never re-observe the already-emitted record.
        self.assertEqual(len(records), 1)
        self.assertEqual(
            records[0],
            {
                "review_calls": 1,
                "reviewer_usage": {
                    "input_tokens": 11,
                    "output_tokens": 17,
                    "total_tokens": 28,
                },
            },
        )
        self.assertEqual(len(main_requests), 1)
        self.assertEqual(len(review_requests), 1)
        self.assertEqual(engine.take_details(), [])
        self.assertIsNone(engine._review_usage)
        self.assertIsNone(engine._scope)
        self.assertEqual(_wait_no_new_children(child_pids_before, 10.0), set())
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_cancel_after_corpus_constructor_closes_readonly_handle(
        self,
    ) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        # The owned review endpoint supplies the valid scripted
        # response from the start: the first request must still
        # prove zero review POSTs (the cancel wins before dispatch),
        # and the healthy same-proxy recovery can actually repair
        # (root fifteenth review).
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        captured = self._capture_begin(engine)
        cancelled_once = False

        def _cancel_once() -> None:
            # The handoff: the ACTUAL constructor returned.  Phase-
            # cancellation stimulus (deterministic stand-in for a
            # native peer disconnect observed by the owned watcher
            # before the engine's corpus-owned work; the actual
            # FIN/RST watcher proofs live in _ProxyIntegrationTests
            # and Root's native RST proofs).
            nonlocal cancelled_once
            if not cancelled_once and captured:
                cancelled_once = True
                captured[-1]._cancelled.set()

        _PostConstructionCancelCorpus.cancel_after_construction = _cancel_once
        saved_corpus = cast(
            "type[RuntimeCorpus]",
            _swap_attr(proxy, "RuntimeCorpus", _PostConstructionCancelCorpus),
        )
        records: list[dict[str, object]] = []
        observed = threading.Event()
        try:
            proxy_server = self._start_proxy(
                main.port, engine, _usage_observer(records, observed)
            )
            # Control: nothing read-only is open before the request.
            self.assertEqual(self._open_fds_for(self.db), set())
            child_pids_before = _owned_child_pids()
            client = socket.create_connection(
                ("127.0.0.1", proxy_server.server_port), timeout=20
            )
            try:
                _post_to_proxy(client, _contract_body(False))
                self.assertTrue(observed.wait(20.0))
                received = _drain_client(client, 10.0)
            finally:
                client.close()
            self.assertEqual(received, b"")
            # One correct 0/unknown record; the review never started.
            self.assertEqual(
                records, [{"review_calls": 0, "reviewer_usage": "unknown"}]
            )
            self.assertEqual(len(review_requests), 0)
            self.assertEqual(len(main_requests), 1)
            # No read-only SQLite FD remains open after the abort.
            self.assertEqual(self._open_fds_for(self.db), set())
            self.assertEqual(engine.take_details(), [])
            self.assertIsNone(engine._review_usage)
            self.assertIsNone(engine._scope)
            self.assertEqual(
                _wait_no_new_children(child_pids_before, 10.0), set()
            )
            self.assertEqual(_wait_no_request_scoped_survivors(), [])
            # Same-proxy recovery: the healthy next request reopens
            # and closes the corpus normally.
            client2 = socket.create_connection(
                ("127.0.0.1", proxy_server.server_port), timeout=20
            )
            try:
                _post_to_proxy(client2, _contract_body(False))
                status, _headers, body = _read_http_response(client2)
            finally:
                client2.close()
            self.assertEqual(status, 200)
            envelope = json.loads(body.decode("utf-8"))
            output = cast("list[dict[str, object]]", envelope["output"])
            message = output[0]
            content = cast("list[dict[str, object]]", message["content"])
            self.assertEqual(
                cast("str", content[0]["text"]),
                "To je tako zapisano, to je tako zapisano.",
            )
            self.assertEqual(len(records), 2)
            self.assertEqual(
                records[1],
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 11,
                        "output_tokens": 17,
                        "total_tokens": 28,
                    },
                },
            )
            self.assertEqual(self._open_fds_for(self.db), set())
        finally:
            _swap_attr(proxy, "RuntimeCorpus", saved_corpus)
            _PostConstructionCancelCorpus.cancel_after_construction = None

    def test_ambient_handled_error_keeps_cleanup_control_authority(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        captured = self._capture_begin(engine)
        records: list[dict[str, object]] = []
        observed = threading.Event()
        _CleanupFaultScope.inject_cleanup_fault = True
        saved_scope_cls = cast(
            "type[request_lifecycle.CancellationScope]",
            _swap_attr(
                request_lifecycle, "CancellationScope", _CleanupFaultScope
            ),
        )
        client: socket.socket | None = None
        try:
            proxy_server = self._direct_proxy(
                main.port, engine, _usage_observer(records, observed)
            )
            client = socket.create_connection(
                ("127.0.0.1", proxy_server.server_port), timeout=20
            )
            conn, addr = self._accept_direct(proxy_server, client)
            child_pids_before = _owned_child_pids()
            try:
                with self.assertRaises(MemoryError) as cm:
                    # The ACTUAL Handler is driven exactly once
                    # (transparent native finish_request) under an
                    # unrelated already-HANDLED ambient MemoryError
                    # (no current-operation error of its own); the
                    # ambient context must never borrow authority.
                    try:
                        raise MemoryError("ambient-handled")
                    except MemoryError:
                        proxy_server.finish_request(conn, addr)
                # The 200 useful repair was actually delivered
                # before the cleanup phase; the client is preserved
                # until this read, then closed in the owned finally.
                status, _headers, body = _read_http_response(client)
            finally:
                if client is not None:
                    client.close()
        finally:
            _swap_attr(request_lifecycle, "CancellationScope", saved_scope_cls)
            _CleanupFaultScope.inject_cleanup_fault = False
        # The distinct CURRENT cleanup control propagates: it is not
        # suppressed by the ambient handled error.
        self.assertEqual(str(cm.exception), "cleanup-fault")
        envelope = json.loads(body.decode("utf-8"))
        output = cast("list[dict[str, object]]", envelope["output"])
        message = output[0]
        content = cast("list[dict[str, object]]", message["content"])
        self.assertEqual(
            cast("str", content[0]["text"]),
            "To je tako zapisano, to je tako zapisano.",
        )
        self.assertEqual(status, 200)
        self.assertEqual(
            records,
            [
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 11,
                        "output_tokens": 17,
                        "total_tokens": 28,
                    },
                }
            ],
        )
        scope = captured[-1]
        self.assertTrue(scope._finished)
        self.assertIsNone(scope._watcher)
        self.assertEqual(_wait_no_new_children(child_pids_before, 10.0), set())
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_ambient_handled_error_alone_is_harmless(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        captured = self._capture_begin(engine)
        records: list[dict[str, object]] = []
        observed = threading.Event()
        proxy_server = self._direct_proxy(
            main.port, engine, _usage_observer(records, observed)
        )
        client = socket.create_connection(
            ("127.0.0.1", proxy_server.server_port), timeout=20
        )
        conn, addr = self._accept_direct(proxy_server, client)
        child_pids_before = _owned_child_pids()
        try:
            # Control premise: the ambient context alone must not
            # surface as an error or alter the operation; the
            # ACTUAL Handler is driven exactly once (transparent
            # native finish_request) under it.
            try:
                raise MemoryError("ambient-handled")
            except MemoryError:
                proxy_server.finish_request(conn, addr)
            # The client is preserved until this read, then closed in
            # the owned finally.
            status, _headers, body = _read_http_response(client)
        finally:
            client.close()
        self.assertEqual(status, 200)
        envelope = json.loads(body.decode("utf-8"))
        output = cast("list[dict[str, object]]", envelope["output"])
        message = output[0]
        content = cast("list[dict[str, object]]", message["content"])
        self.assertEqual(
            cast("str", content[0]["text"]),
            "To je tako zapisano, to je tako zapisano.",
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(len(main_requests), 1)
        self.assertEqual(len(review_requests), 1)
        scope = captured[-1]
        self.assertTrue(scope._finished)
        self.assertIsNone(scope._watcher)
        self.assertEqual(_wait_no_new_children(child_pids_before, 10.0), set())
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_handler_first_memoryerror_preserved_over_later_cleanup(self) -> None:
        main_requests: list[dict[str, object]] = []
        review_requests: list[dict[str, object]] = []
        main_released = threading.Event()
        review_released = threading.Event()
        main_event = threading.Event()
        review_event = threading.Event()
        main_closed = threading.Event()
        review_closed = threading.Event()
        main = _RawLoopbackServer(
            "main-upstream",
            _main_complete_handler(
                main_requests,
                _json_completed(TEXT),
                "application/json",
                main_released,
                main_event,
                main_closed,
            ),
        )
        review = _RawLoopbackServer(
            "review-upstream",
            _review_respond_handler(
                review_requests,
                _review_payload_replace_all(),
                review_released,
                review_event,
                review_closed,
            ),
        )
        main.start()
        review.start()
        self.servers.extend((main, review))
        engine = proxy.RepairEngine(
            self.db, self._new_reviewer(review.port), pandoc=_real_spec()
        )
        captured = self._capture_begin(engine)
        first_mem = MemoryError("own-first-memory")
        real_repair = engine.repair

        def _repair_then_memory(text: str) -> str:
            # The actual native forward/repair fully completes, then
            # the FIRST own control of the operation is raised.
            real_repair(text)
            raise first_mem

        # Typed one-request observer seam: the exact product repair
        # boundary is replaced with a transparent delegate.
        _swap_attr(engine, "repair", _repair_then_memory)
        records: list[dict[str, object]] = []
        observed = threading.Event()
        _CleanupFaultScope.inject_cleanup_fault = True
        saved_scope_cls = cast(
            "type[request_lifecycle.CancellationScope]",
            _swap_attr(
                request_lifecycle, "CancellationScope", _CleanupFaultScope
            ),
        )
        client: socket.socket | None = None
        try:
            proxy_server = self._direct_proxy(
                main.port, engine, _usage_observer(records, observed)
            )
            client = socket.create_connection(
                ("127.0.0.1", proxy_server.server_port), timeout=20
            )
            conn, addr = self._accept_direct(proxy_server, client)
            child_pids_before = _owned_child_pids()
            try:
                with self.assertRaises(MemoryError) as cm:
                    # The ACTUAL Handler is driven exactly once
                    # (transparent native finish_request) under an
                    # unrelated already-HANDLED ambient MemoryError;
                    # the EXACT first own control of the operation
                    # must keep its identity.
                    try:
                        raise MemoryError("ambient-handled")
                    except MemoryError:
                        proxy_server.finish_request(conn, addr)
                # Quiet close: nothing was delivered (the first own
                # control escaped before delivery); the client is
                # preserved until this drain.
                self.assertEqual(_drain_client(client, 10.0), b"")
            finally:
                if client is not None:
                    client.close()
        finally:
            _swap_attr(request_lifecycle, "CancellationScope", saved_scope_cls)
            _CleanupFaultScope.inject_cleanup_fault = False
        # The EXACT first own MemoryError keeps its identity after
        # complete cleanup; the later cleanup MemoryError is
        # suppressed; no generated 502 (quiet close, no bytes).
        self.assertIs(cm.exception, first_mem)
        self.assertEqual(records, [])
        scope = captured[-1]
        self.assertTrue(scope._finished)
        self.assertIsNone(scope._watcher)
        self.assertEqual(len(main_requests), 1)
        self.assertEqual(len(review_requests), 1)
        self.assertEqual(_wait_no_new_children(child_pids_before, 10.0), set())
        self.assertEqual(_wait_no_request_scoped_survivors(), [])

    def test_corpus_owned_region_control_priority_matrix(self) -> None:
        # (row, injected adopt fault, cancel at the adopt handoff,
        # close fault, expected escape): the corpus-owned region
        # keeps the exact first NONORDINARY control identity;
        # otherwise a later NONORDINARY cleanup control propagates;
        # an ordinary pending (or cancellation) is never replaced by
        # an ordinary cleanup fault and never acquires authority over
        # a later nonordinary control.  The cancel-pending rows
        # inject the phase-cancellation stimulus after the real
        # adoption (inside the corpus-owned region), exactly as the
        # other adopt-handoff rows do; the real pre-entry zero-child
        # coverage stays in _ProxyIntegrationTests.
        rows: list[
            tuple[str, BaseException | None, bool, BaseException | None, str]
        ] = [
            (
                "first-kI-later-close-memory",
                KeyboardInterrupt(),
                False,
                MemoryError("late-close-memory"),
                "first",
            ),
            (
                "first-memory-later-close-kI",
                MemoryError("own-first-memory"),
                False,
                KeyboardInterrupt(),
                "first",
            ),
            (
                "ordinary-pending-later-close-memory",
                ValueError("ordinary-pending"),
                False,
                MemoryError("late-close-memory"),
                "close",
            ),
            (
                "ordinary-pending-later-close-kI",
                ValueError("ordinary-pending"),
                False,
                KeyboardInterrupt(),
                "close",
            ),
            (
                "cancel-pending-later-close-memory",
                None,
                True,
                MemoryError("late-close-memory"),
                "close",
            ),
            (
                "cancel-pending-later-close-kI",
                None,
                True,
                KeyboardInterrupt(),
                "close",
            ),
            (
                "cancel-pending-later-close-ordinary",
                None,
                True,
                OSError("ordinary-close-fault"),
                "cancel",
            ),
        ]
        for name, adopt_fault, cancel_in_adopt, close_fault, expected in rows:
            with self.subTest(row=name):
                local, peer = socket.socketpair()
                scope = request_lifecycle.CancellationScope(local)
                scope.start()
                _ControlPriorityCorpus.adopt_fault = adopt_fault
                _ControlPriorityCorpus.close_fault = close_fault
                _ControlPriorityCorpus.close_completed = False
                _ControlPriorityCorpus.cancel_in_adopt = cancel_in_adopt
                _ControlPriorityCorpus.cancel_scope = scope
                saved_corpus = cast(
                    "type[RuntimeCorpus]",
                    _swap_attr(
                        proxy, "RuntimeCorpus", _ControlPriorityCorpus
                    ),
                )
                engine = proxy.RepairEngine(
                    self.db, self._new_reviewer(1), pandoc=_real_spec()
                )
                child_pids_before = _owned_child_pids()
                try:
                    engine.begin_request(scope)
                    with self.assertRaises(BaseException) as cm:
                        engine.repair(TEXT)
                finally:
                    _swap_attr(proxy, "RuntimeCorpus", saved_corpus)
                    _ControlPriorityCorpus.adopt_fault = None
                    _ControlPriorityCorpus.close_fault = None
                    _ControlPriorityCorpus.cancel_in_adopt = False
                    _ControlPriorityCorpus.cancel_scope = None
                    scope.finish()
                    peer.close()
                    local.close()
                # The ACTUAL close always completed before the
                # injected close fault (real cleanup, real identity).
                self.assertTrue(_ControlPriorityCorpus.close_completed)
                if expected == "first":
                    self.assertIs(cm.exception, adopt_fault)
                elif expected == "close":
                    self.assertIs(cm.exception, close_fault)
                else:
                    self.assertIsInstance(
                        cm.exception, request_lifecycle.RequestCancelled
                    )
                self.assertEqual(
                    _wait_no_new_children(child_pids_before, 10.0), set()
                )
