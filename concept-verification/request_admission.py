"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Admission.

Finite accepted-request admission for the runnable proxy (order
026-a): one active whole request handler plus a bounded number of
waiting owned requests, each under one absolute monotonic queue
deadline anchored at the accepted dispatch entry BEFORE admission
allocation/queue work; startup and waiting overhead are charged and
progress/phase transitions never reset the deadline.  The fixed
owned worker/monitor threads start synchronously in the owning
constructor before request traffic, so the accepting loop never
runs a request and keeps accepting and classifying new connections
while one handler is held.  Queue-full/expiry/closing entries are
rejected pre-main with one fixed content-free bounded 503 and
closed: no thread per rejected connection, no unbounded registry
growth, and no queued request reaches intake/forward/engine/
evidence/review after expiry or closure (order 026-a,
requirements 2-5).  This is an internal accepted-order FIFO, not a
tenant/kernel/network fairness claim; kernel backlog time before
accept is outside the measured clock.
"""

from __future__ import annotations

import contextlib
import json
import math
import socket
import sys
import threading
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

import config

__all__ = [
    "AdmissionPolicy",
    "CODE_QUEUE_CLOSED",
    "CODE_QUEUE_FULL",
    "CODE_QUEUE_TIMEOUT",
    "RequestAdmissionController",
    "current_admission_policy",
    "validate_admission_policy",
]

CODE_QUEUE_FULL = "REQUEST_QUEUE_FULL"
CODE_QUEUE_TIMEOUT = "REQUEST_QUEUE_TIMEOUT"
CODE_QUEUE_CLOSED = "REQUEST_QUEUE_CLOSED"

_ERROR_TYPE = "request_admission_error"
# Finite best-effort bound for emitting one fixed rejection packet:
# a client that does not read must not stall the listener
# indefinitely (order 026-a, requirement 4).
_REJECT_SEND_TIMEOUT = 1.0
# Bounded settle delay between retried join attempts: a join attempt
# interrupted by a cleanup fault is not a join, so the exact native
# join is retried; the delay only avoids hot-spinning while a
# transient fault persists (the owning loops always end on close,
# so the actual join is finite).
_SETTLE_RETRY_SECONDS = 0.001
# Finite lifecycle poll so elapsed expiry is noticed even without a
# wake event and idle loops never hot-spin; the actual claim
# re-checks the deadline, so the poll only bounds notice latency,
# never the deadline itself.
_MONITOR_POLL_SECONDS = 0.05
_MIN_WAIT_SECONDS = 0.001
_MONITOR_NAME = "concept-request-admission-monitor"
_WORKER_NAME = "concept-request-admission-handler"


def _reject_packet(code: str) -> bytes:
    body = json.dumps(
        {"error": {"type": _ERROR_TYPE, "code": code}}, separators=(",", ":")
    ).encode()
    return (
        b"HTTP/1.0 503 Service Unavailable\r\n"
        b"Content-Type: application/json\r\n"
        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
        b"Connection: close\r\n"
        b"\r\n" + body
    )


_REJECT_PACKETS: dict[str, bytes] = {
    CODE_QUEUE_FULL: _reject_packet(CODE_QUEUE_FULL),
    CODE_QUEUE_TIMEOUT: _reject_packet(CODE_QUEUE_TIMEOUT),
    CODE_QUEUE_CLOSED: _reject_packet(CODE_QUEUE_CLOSED),
}


@dataclass(frozen=True)
class AdmissionPolicy:
    """One immutable per-instance accepted-request admission policy.

    Resolved from the CURRENT config at each real ConceptProxy
    construction, before bind/thread/socket allocation (order
    026-a, requirement 1).  A running instance retains its policy
    for its whole life; later config defaults apply only to newly
    constructed instances - never a silent live resize.
    """

    max_queued: int
    wait_seconds: float


def validate_admission_policy(
    max_queued: object, wait_seconds: object
) -> AdmissionPolicy:
    """Validate the two independent finite admission limits.

    The waiting capacity is an exact positive int (bool or an int
    subclass is not an exact int value) and the queue wait is an
    exact int/float numeric (not bool, not a subclass), positive and
    representable under the native ``threading.TIMEOUT_MAX`` wait
    bound; no string/nonnumeric coercion, None, zero-disable,
    nonfinite value or out-of-range value is accepted, and an
    out-of-range int is rejected by integer comparison before any
    float conversion can overflow.  Validation reads no file,
    model, network or index and raises a plain ``ValueError``
    before any bind allocation (order 026-a, requirement 1).
    """
    if type(max_queued) is not int or max_queued <= 0:
        raise ValueError(
            "PROXY_MAX_QUEUED_REQUESTS must be an exact positive int"
        )
    if type(wait_seconds) not in (int, float):
        raise ValueError(
            "PROXY_QUEUE_WAIT_SECONDS must be an exact int or float "
            "duration"
        )
    if isinstance(wait_seconds, int):
        # The type-identity check above rejects bool and int
        # subclasses, so the isinstance narrowing is lossless: this
        # is an exact int.  Integer comparison first: a huge int
        # would overflow a float conversion before the range
        # rejection.
        if wait_seconds <= 0 or wait_seconds > int(threading.TIMEOUT_MAX):
            raise ValueError(
                "PROXY_QUEUE_WAIT_SECONDS must be a positive duration "
                "within the native wait bound"
            )
        return AdmissionPolicy(
            max_queued=max_queued, wait_seconds=float(wait_seconds)
        )
    if not isinstance(wait_seconds, float):
        # Unreachable at runtime: the type-identity check above
        # admits only exact int and exact float, and the int arm
        # handled the exact int.  The arm exists so the value stays
        # statically narrowed to a genuine float below without any
        # type-ignore or weakening.
        raise ValueError(
            "PROXY_QUEUE_WAIT_SECONDS must be an exact int or float "
            "duration"
        )
    if (
        not math.isfinite(wait_seconds)
        or wait_seconds <= 0
        or wait_seconds > threading.TIMEOUT_MAX
    ):
        raise ValueError(
            "PROXY_QUEUE_WAIT_SECONDS must be a finite positive "
            "duration within the native wait bound"
        )
    return AdmissionPolicy(max_queued=max_queued, wait_seconds=float(wait_seconds))


def current_admission_policy() -> AdmissionPolicy:
    """Resolve the CURRENT config admission defaults at call time.

    No import-time captured-default shortcut: every real
    ConceptProxy construction re-reads the CURRENT config values so
    a running instance keeps its validated policy while newly
    constructed instances see new defaults (order 026-a,
    requirement 1).
    """
    return validate_admission_policy(
        config.PROXY_MAX_QUEUED_REQUESTS,
        config.PROXY_QUEUE_WAIT_SECONDS,
    )


class _AdmissionServer(Protocol):
    """The owned server boundary the controller drives (structural).

    ConceptProxy satisfies this protocol through its existing
    BaseServer lifecycle methods; the handler run goes through the
    standard process_request boundary (finish plus shutdown of the
    exact accepted connection), so the existing outer HTTP error
    semantics - and the frozen test fixtures' process_request
    completion observation - are preserved unchanged.
    """

    def finish_request(
        self, request: socket.socket, client_address: tuple[str, int]
    ) -> None: ...

    def process_request(
        self, request: socket.socket, client_address: tuple[str, int]
    ) -> None: ...

    def shutdown_request(self, request: socket.socket) -> None: ...

    def handle_error(self, request: object, client_address: object) -> None: ...


class _QueueEntry:
    """One owned accepted connection and its anchored queue state.

    State transitions happen exactly once under the controller
    lock: waiting -> admitted -> (running) -> released, or waiting
    -> rejected.  Completed entries are removed from the registry
    on transition; nothing accumulates (order 026-a, requirement 2).
    """

    __slots__ = ("sock", "client_address", "deadline", "state", "code")

    def __init__(
        self,
        sock: socket.socket,
        client_address: tuple[str, int],
        deadline: float,
    ) -> None:
        self.sock = sock
        self.client_address = client_address
        self.deadline = deadline
        self.state = "waiting"  # waiting | admitted | running | rejected
        self.code: str | None = None


class RequestAdmissionController:
    """One owned accepted-request admission lifecycle.

    Exactly one whole handler is active at a time, executed by one
    fixed owned handler worker; up to the policy's waiting capacity
    is owned in accepted (FIFO) order under the one absolute
    monotonic deadline anchored at the accepted dispatch entry.  The
    one active/reserved slot plus at most the waiting capacity is an
    atomic invariant: an entry is reserved into the active slot in
    the same lock step that frees the handoff, so a claim/close race
    can never reserve a second in-flight entry.  An entry stays
    registered in an owned slot across every fallible step of the
    claim (the deadline clock read); only a non-fallible terminal
    transition releases it, so a lifecycle control at a claim can
    never orphan an accepted connection.  The fixed owned
    worker/monitor threads start synchronously before request
    traffic and commit to dispatch only after the owning constructor
    has fully completed (no work before initialization/dispatch
    commitment).  Normal shutdown/close stops admission,
    cancels/closes every waiting entry with the fixed closed code,
    releases every owned slot and actually joins the exact owned
    workers before the owning close returns; a nonordinary control
    losing either fixed worker is contained at that worker's owner
    boundary - the first owned-operation control is preserved,
    admission is stopped so no entry is ever assigned to a dead
    worker, every owned entry is canceled/closed, and the control is
    re-raised at the documented owning close: never a raw default
    thread traceback, never an accidental successful HTTP answer,
    never a replacement worker (order 026-a, requirements 4 and 5).
    """

    def __init__(
        self,
        server: _AdmissionServer,
        policy: AdmissionPolicy,
        *,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._server = server
        self._policy = policy
        self._clock = clock
        self._woken = threading.Condition(threading.Lock())
        self._waiting: deque[_QueueEntry] = deque()
        self._handoff: _QueueEntry | None = None
        self._active: _QueueEntry | None = None
        self._closed = False
        self._committed = False
        self._worker_control: BaseException | None = None
        self._monitor: threading.Thread | None = None
        self._worker: threading.Thread | None = None

    @property
    def policy(self) -> AdmissionPolicy:
        return self._policy

    def pending_count(self) -> int:
        """Live owned admission entries (waiting/handoff/active).

        Read-only introspection: completed entries are removed on
        state transition, so a growing count would indicate a leak
        (order 026-a, requirement 2).
        """
        with self._woken:
            return (
                len(self._waiting)
                + (1 if self._handoff is not None else 0)
                + (1 if self._active is not None else 0)
            )

    def start(self) -> None:
        """Synchronously own and start the fixed lifecycle threads.

        Both candidate threads are owned by exact reference BEFORE
        their fallible start, and the dispatch-readiness commit
        (flag plus notification under the owned condition) is part
        of the same ownership region: any control from a native
        start or from the readiness commit settles each reference
        that actually started (ident set - still alive or already
        ended) - stopped and actually joined - before the first
        control propagates; a never-started thread is never joined,
        and one cleanup failure neither skips a later owned
        resource nor replaces the first current-operation control
        (order 026-a, requirement 5).  The dispatch commit lands
        only after both threads are owned and started, so no
        lifecycle work runs before the owning constructor
        completes.
        """
        monitor = threading.Thread(
            target=self._monitor_loop, name=_MONITOR_NAME
        )
        worker = threading.Thread(target=self._worker_loop, name=_WORKER_NAME)
        self._monitor = monitor
        self._worker = worker
        try:
            monitor.start()
            worker.start()
            with self._woken:
                self._committed = True
                self._woken.notify_all()
        except BaseException as primary:
            self._settle_started((monitor, worker), primary)
            raise

    def _settle_join(self, thread: threading.Thread) -> BaseException | None:
        """Actually complete the native join of one started thread.

        A cleanup fault raised by a join attempt is recorded but is
        NOT a join: the exact native join must actually complete
        before the owning operation may propagate any control, so
        the join is retried until it completes (the owning lifecycle
        loops always end on close, so the actual join is finite).
        Returns the first cleanup fault observed, if any (order
        026-a, requirement 5).
        """
        first: BaseException | None = None
        while True:
            try:
                thread.join()
                return first
            except BaseException as cleanup_error:
                if first is None:
                    first = cleanup_error
                time.sleep(_SETTLE_RETRY_SECONDS)

    def _settle_started(
        self,
        threads: tuple[threading.Thread, ...],
        primary: BaseException | None,
    ) -> None:
        """Complete exact owned cleanup of actually-started threads.

        Every reference that actually started (ident set) is marked
        closed, woken and actually joined in order.  One cleanup
        failure neither skips a later owned resource nor replaces
        the first current-operation control: the FIRST cleanup
        error is recorded while the remaining owned resources are
        still settled, and the first control is re-raised only
        AFTER the complete cleanup.  A never-started thread is
        never joined.  With no pending primary, the first cleanup
        error (if any) becomes the raised control; unrelated
        ambient exception state is never consulted (order 026-a,
        requirement 5).
        """
        first_cleanup_error: BaseException | None = None
        for thread in threads:
            if thread.ident is None:
                continue
            try:
                with self._woken:
                    self._closed = True
                    self._woken.notify_all()
            except BaseException as cleanup_error:
                if first_cleanup_error is None:
                    first_cleanup_error = cleanup_error
            join_error = self._settle_join(thread)
            if join_error is not None and first_cleanup_error is None:
                first_cleanup_error = join_error
        if primary is None:
            if first_cleanup_error is not None:
                raise first_cleanup_error
            return
        if first_cleanup_error is None:
            raise primary
        raise primary from first_cleanup_error

    def dispatch(
        self, request: socket.socket, client_address: tuple[str, int]
    ) -> None:
        """Own one accepted connection at the accepted dispatch entry.

        The one absolute monotonic queue deadline anchors here,
        BEFORE admission allocation/queue work; kernel pre-accept
        time is outside it (order 026-a, requirement 3).  The
        accepting loop never runs a request: an unexpired entry is
        owned in accepted order and admitted by the monitor to the
        handler worker; a full or already-closing entry is
        rejected inline with one fixed bounded 503 and closed - no
        thread is created for a rejected connection.
        """
        try:
            deadline = self._clock() + self._policy.wait_seconds
            entry = _QueueEntry(request, client_address, deadline)
        except BaseException:
            # Deadline anchoring or entry allocation failed: close
            # the accepted socket (owned at the dispatch entry) and
            # propagate the exact control; nothing else was
            # allocated.
            with contextlib.suppress(Exception):
                request.close()
            raise
        with self._woken:
            if self._closed:
                code: str | None = CODE_QUEUE_CLOSED
            elif len(self._waiting) >= self._policy.max_queued:
                code = CODE_QUEUE_FULL
            else:
                self._waiting.append(entry)
                self._woken.notify_all()
                code = None
        if code is not None:
            self._reject(entry, code)

    def stop(self) -> None:
        """The documented owning admission close boundary.

        Stops admission, cancels/closes every waiting entry with
        the fixed closed code, releases every owned slot and
        actually joins the exact owned workers before returning;
        in-flight active work may take its existing bounded time
        (no hard-real-time or remote-cancel claim).  A nonordinary
        control preserved at a worker owner boundary is re-raised
        here, at the owning supervisor, after the exact cleanup
        (order 026-a, requirement 5).  A join failure on one exact
        owned worker neither skips the join of the other owned
        worker nor replaces the preserved lifecycle control: the
        first join error is recorded and the preserved control (if
        any) is re-raised after the complete join.  Idempotent: a
        second owning close after the workers are joined is a no-op
        join of the already-ended exact threads.
        """
        with self._woken:
            self._closed = True
            self._woken.notify_all()
        first_join_error: BaseException | None = None
        for thread in (self._monitor, self._worker):
            if thread is None or thread.ident is None:
                continue
            join_error = self._settle_join(thread)
            if join_error is not None and first_join_error is None:
                first_join_error = join_error
        with self._woken:
            control = self._worker_control
            self._worker_control = None
        if control is not None:
            if first_join_error is None:
                raise control
            raise control from first_join_error
        if first_join_error is not None:
            raise first_join_error

    def _reject(self, entry: _QueueEntry, code: str) -> None:
        """Emit one fixed bounded 503 where possible, then close.

        Bounded best-effort: a short socket timeout bounds the send
        so a client that does not read cannot stall the listener
        indefinitely; any emission failure closes the exact
        accepted connection.  Timeout restoration and close are
        independent cleanup steps so a restoration failure can never
        skip the close.  The fixed packet carries no caller
        headers/text/exceptions/queue values (order 026-a,
        requirement 4).
        """
        sock = entry.sock
        previous: float | None = None
        try:
            previous = sock.gettimeout()
            sock.settimeout(_REJECT_SEND_TIMEOUT)
            sock.sendall(_REJECT_PACKETS[code])
        except (OSError, ValueError):
            pass
        finally:
            if previous is not None:
                with contextlib.suppress(Exception):
                    sock.settimeout(previous)
            with contextlib.suppress(Exception):
                sock.close()

    def _fail_lifecycle(self) -> None:
        """One contained lifecycle failure at a worker owner boundary.

        A fixed lifecycle worker died on a nonordinary control:
        preserve the FIRST owned-operation control (never an
        ambient sys.exception and never a later control), stop
        admission so no entry is ever assigned to a dead worker,
        cancel/close every owned waiting entry - and a reserved
        handoff entry that never entered the handler - with the
        fixed closed code.  In-flight active work belongs to the
        surviving worker and keeps its existing bounded lifetime.
        No autoreplacement; the documented owning close re-raises
        the preserved control after the exact cleanup (order 026-a,
        requirement 5).
        """
        due: list[tuple[_QueueEntry, str]] = []
        with self._woken:
            if self._worker_control is None:
                self._worker_control = sys.exc_info()[1]
            self._closed = True
            for entry in self._waiting:
                entry.state = "rejected"
                entry.code = CODE_QUEUE_CLOSED
                due.append((entry, CODE_QUEUE_CLOSED))
            self._waiting.clear()
            if self._handoff is not None:
                entry = self._handoff
                self._handoff = None
                entry.state = "rejected"
                entry.code = CODE_QUEUE_CLOSED
                due.append((entry, CODE_QUEUE_CLOSED))
            self._woken.notify_all()
        for entry, code in due:
            self._reject(entry, code)

    def _monitor_loop(self) -> None:
        try:
            while True:
                due: list[tuple[_QueueEntry, str]] = []
                closing = False
                with self._woken:
                    while not self._committed and not self._closed:
                        self._woken.wait(_MONITOR_POLL_SECONDS)
                    if self._closed:
                        # Cancel/close every waiting entry exactly
                        # once before the owner return; clearing a
                        # deque is not socket cleanup.
                        for entry in self._waiting:
                            entry.state = "rejected"
                            entry.code = CODE_QUEUE_CLOSED
                            due.append((entry, CODE_QUEUE_CLOSED))
                        self._waiting.clear()
                        closing = True
                    else:
                        # Prune in accepted order: an expired entry
                        # is rejected and cannot block later
                        # eligible entries (order 026-a,
                        # requirement 2).
                        while (
                            self._waiting
                            and self._clock() >= self._waiting[0].deadline
                        ):
                            entry = self._waiting.popleft()
                            entry.state = "rejected"
                            entry.code = CODE_QUEUE_TIMEOUT
                            due.append((entry, CODE_QUEUE_TIMEOUT))
                        if (
                            self._waiting
                            and self._active is None
                            and self._handoff is None
                        ):
                            # FIFO claim; the deadline is inspected
                            # while the head entry is still
                            # registered in the queue, so a control
                            # at the claim clock read can never
                            # orphan the connection (order 026-a,
                            # requirement 5).  The actual claim
                            # re-checks the elapsed deadline so a
                            # late/racing wake-up loses to expiry
                            # and deadline equality is expired
                            # (order 026-a, requirement 3).
                            entry = self._waiting[0]
                            if self._clock() >= entry.deadline:
                                self._waiting.popleft()
                                entry.state = "rejected"
                                entry.code = CODE_QUEUE_TIMEOUT
                                due.append((entry, CODE_QUEUE_TIMEOUT))
                            else:
                                self._waiting.popleft()
                                entry.state = "admitted"
                                self._handoff = entry
                                self._woken.notify_all()
                        else:
                            if self._waiting:
                                timeout = max(
                                    _MIN_WAIT_SECONDS,
                                    min(
                                        _MONITOR_POLL_SECONDS,
                                        self._waiting[0].deadline
                                        - self._clock(),
                                    ),
                                )
                            else:
                                timeout = _MONITOR_POLL_SECONDS
                            self._woken.wait(timeout)
                for entry, code in due:
                    self._reject(entry, code)
                if closing:
                    return
        except BaseException:
            self._fail_lifecycle()
            return

    def _worker_loop(self) -> None:
        try:
            while True:
                entry: _QueueEntry | None = None
                reject: tuple[_QueueEntry, str] | None = None
                with self._woken:
                    while True:
                        if not self._committed and not self._closed:
                            self._woken.wait(_MONITOR_POLL_SECONDS)
                            continue
                        if self._handoff is not None:
                            entry = self._handoff
                            # The handoff registration stays the
                            # exact ownership across the fallible
                            # recheck below; it is cleared only in
                            # the non-fallible transition that
                            # follows, so a control at the claim
                            # clock read can never orphan the
                            # connection (order 026-a,
                            # requirement 5).  The actual claim for
                            # handler execution re-checks closing
                            # and the elapsed deadline atomically
                            # with the reservation: close or expiry
                            # wins over a late wake-up, and the
                            # active slot is set in the same lock
                            # step, so one active/reserved slot
                            # plus at most the waiting capacity is
                            # invariant (order 026-a, requirements
                            # 2 and 3).
                            if self._closed:
                                code: str | None = CODE_QUEUE_CLOSED
                            elif self._clock() >= entry.deadline:
                                code = CODE_QUEUE_TIMEOUT
                            else:
                                code = None
                            self._handoff = None
                            if code is None:
                                self._active = entry
                                entry.state = "running"
                            else:
                                entry.state = "rejected"
                                entry.code = code
                                reject = (entry, code)
                            break
                        if self._closed:
                            return
                        self._woken.wait(_MONITOR_POLL_SECONDS)
                if reject is not None:
                    self._reject(*reject)
                else:
                    assert entry is not None
                    self._run_handler(entry)
        except BaseException:
            self._fail_lifecycle()
            return

    def _run_handler(self, entry: _QueueEntry) -> None:
        # One whole handler run, serialized by this single worker.
        # The run goes through the standard process_request
        # boundary (finish plus shutdown of the exact accepted
        # connection), so the existing outer HTTP error semantics
        # - and the frozen test fixtures' process_request
        # completion observation - are preserved exactly; a
        # handler failure keeps the bounded silent handle_error,
        # and the owned connection shutdown is independent
        # finalization that runs on every outcome.  The existing
        # intake clock starts inside the handler, after successful
        # admission, unchanged.
        try:
            self._server.process_request(entry.sock, entry.client_address)
        except Exception:
            with contextlib.suppress(Exception):
                self._server.handle_error(entry.sock, entry.client_address)
        finally:
            with contextlib.suppress(Exception):
                self._server.shutdown_request(entry.sock)
            with self._woken:
                if self._active is entry:
                    self._active = None
                    self._woken.notify_all()
