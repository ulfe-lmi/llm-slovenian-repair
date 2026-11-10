"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Owned
elapsed deadline guard for upstream status/header acquisition.

Order 018-a: the standard-library ``getresponse`` parser is retained
unchanged and runs on the owning calling thread.  This module owns one
finite positive monotonic elapsed deadline anchored immediately before
acquisition (before the guard starts); slow status/header bytes and
legitimate interim 100 responses never reset it, so a
socket/inactivity timeout alone is insufficient and is not the phase
bound.  The owned guard is a pure timer: it owns only a bounded event
wait plus a shutdown of the exact captured owned socket object.  The
guard is cancelled (completion event) and actually joined before
classification or transfer on both success and failure, so no header
work outlives acquisition; the join is blocking because the guard's
post-cancel work is itself bounded (no blocking primitive remains
after the cancellation).  After the guard has terminated, the actual
elapsed state is classified: completion racing expiration loses to
expiration and a late response is explicitly closed and never used.
The guard never touches another owned connection.  The body deadline
(``capture_transport``) begins later and remains independent; overall
request deadlines are not implemented.
"""

from __future__ import annotations

import contextlib
import http.client
import math
import socket
import threading
import time
from collections.abc import Callable
from typing import Protocol

import request_lifecycle


class HeaderTimeoutError(ValueError):
    """Bounded main failure: the elapsed header budget expired."""


class HeaderSetupError(ValueError):
    """Bounded main failure: the owned transport was not ready for
    header acquisition (no captured owned socket object)."""


class _AcquisitionConnection(Protocol):
    """Structural owned-connection boundary used by acquisition.

    The owning ``HTTPConnection`` (or an https one) satisfies it: the
    exact owned socket object plus the stdlib response-parser entry.
    The acquisition never touches any other connection state, so this
    narrow boundary is the contract - and the fault-injection tests
    exercise exactly it.
    """

    sock: socket.socket | None

    def getresponse(self) -> http.client.HTTPResponse:
        ...


def _close_untransferred(response: http.client.HTTPResponse | None) -> None:
    """Explicitly close an untransferred parsed response, if any.

    Every successfully parsed response remains owned by the
    acquisition until ACTUAL transfer (order 030-a, requirement 5):
    when the response is not transferred it is closed here before
    any operation/guard/cleanup control propagates, because the
    caller's connection close cannot close a detached
    Connection-close response - its buffered reader pins the exact
    raw socket FD until the response itself is closed.
    """
    if response is not None:
        with contextlib.suppress(Exception):
            response.close()


def validate_header_budget(budget: object) -> float:
    """Return the finite positive header budget or reject the value.

    Rejects bool, nonnumeric, nonfinite and nonpositive values.  The
    constructor validates before any bind allocation and the guard
    validates again at helper use (order 018-a, requirement 2).
    """
    if (
        isinstance(budget, bool)
        or not isinstance(budget, (int, float))
        or not math.isfinite(budget)
        or budget <= 0
    ):
        raise ValueError(
            "header timeout must be a finite positive duration"
        )
    return float(budget)


def acquire_response(
    connection: _AcquisitionConnection,
    budget: object,
    *,
    cancelled: Callable[[], bool] | None = None,
) -> http.client.HTTPResponse:
    """Acquire the status/header response under one elapsed budget.

    The absolute deadline anchors before the guard starts and before
    ``getresponse`` acquisition; byte arrival never resets it and
    legitimate interim 100 responses (handled inside the stdlib parser)
    do not extend it.  ``getresponse`` runs on the owning calling
    thread; the owned guard timer waits for the deadline and, only if
    acquisition has not completed, interrupts the exact captured owned
    socket object - never another owned connection.  The guard is
    cancelled (completion event) and actually joined - on both success
    and failure, before classification or transfer - so no header work
    outlives acquisition.  The actual elapsed state is then checked: if
    the deadline has passed (or the guard fired), a
    ``HeaderTimeoutError`` is raised and a racing completion is
    explicitly closed and never used.  Other parser failures before
    the deadline propagate unchanged (existing transport-failure
    semantics).  The caller closes the owned response/connection on
    every path.

    Order 030-a: when ``cancelled`` (the current request's
    cancellation predicate, captured explicitly into the guard
    closure - no ContextVar assumption) is provided, an observed
    client cancellation interrupts the exact captured owned socket
    exactly like expiration and is classified as
    ``request_lifecycle.RequestCancelled`` (never a header timeout or
    transport error) after the guard is actually joined; a racing
    completion is explicitly closed and never transferred.  With
    ``cancelled`` absent the historical single-wait guard behavior is
    preserved exactly.
    """
    deadline_budget = validate_header_budget(budget)
    sock = getattr(connection, "sock", None)
    if sock is None:
        raise HeaderSetupError(
            "upstream transport has no owned socket for header acquisition"
        )
    # One absolute monotonic deadline anchored before guard startup and
    # before acquisition (order 018-a, requirement 2).
    deadline = time.monotonic() + deadline_budget
    completed = threading.Event()
    state = {"expired": False, "cancelled": False}
    # The owned guard's own nonordinary control (order 030-a,
    # requirement 5): preserved by the guard thread, handed to the
    # owning thread through the actual join, and never swallowed.
    guard_control: BaseException | None = None

    def _guard() -> None:
        nonlocal guard_control
        if cancelled is None:
            remaining = deadline - time.monotonic()
            if remaining > 0:
                completed.wait(timeout=remaining)
            if not completed.is_set():
                # The absolute deadline passed while acquisition was
                # still in flight: interrupt only the captured owned
                # socket object so the owning thread's parser read
                # unblocks.
                state["expired"] = True
                with contextlib.suppress(Exception):
                    sock.shutdown(socket.SHUT_RDWR)
            return
        # Cancellation-aware variant (order 030-a, requirement 4): the
        # anchored absolute deadline is never reset or extended; the
        # pure timer wait is only sliced at 50 ms so the explicitly
        # captured predicate can wake it.
        while True:
            if completed.is_set():
                return
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                state["expired"] = True
                with contextlib.suppress(Exception):
                    sock.shutdown(socket.SHUT_RDWR)
                return
            try:
                if cancelled():
                    state["cancelled"] = True
                    with contextlib.suppress(Exception):
                        sock.shutdown(socket.SHUT_RDWR)
                    return
            except BaseException as exc:
                if request_lifecycle.is_nonordinary_control(exc):
                    # The owned guard's own nonordinary control is
                    # preserved and transferred to the owning thread:
                    # the EXACT captured owned socket is interrupted
                    # first - storing the error and setting the event
                    # alone cannot wake a parser blocked inside the
                    # native socket read - then the timer stops (no
                    # interrupt after completion), the owning join is
                    # woken, and the control is never discarded
                    # (order 030-a, requirement 5).
                    with contextlib.suppress(Exception):
                        sock.shutdown(socket.SHUT_RDWR)
                    guard_control = exc
                    completed.set()
                    return
                # An ordinary predicate fault is a phase fault, not a
                # caller control: it must not kill the timer, and the
                # anchored deadline still bounds the phase.
            completed.wait(min(0.05, remaining))

    guard = threading.Thread(target=_guard, name="concept-header-guard")
    try:
        guard.start()
    except BaseException as exc:
        # Partial-startup ownership (order 030-a, requirement 5): a
        # guard that actually started before the startup fault is
        # cancelled and actually joined before the first control
        # propagates, so the exact owned guard can never later shut
        # down the captured socket; a never-started guard (ident is
        # None) is never joined.  A control from the cleanup join
        # itself never replaces the first (startup) control.
        if guard.ident is not None:
            completed.set()
            request_lifecycle.join_owned_thread(guard, exc)
        raise
    response: http.client.HTTPResponse | None = None
    error: BaseException | None = None
    try:
        response = connection.getresponse()
    except BaseException as exc:  # noqa: B036 - classified below
        error = exc
    # Cancel the guard (no interrupt after completion) and actually
    # join the pure timer before any classification or transfer on
    # both success and failure: no late timer and no header work
    # outlives acquisition.  The join is blocking because the guard's
    # post-cancel work is bounded (the cancellation wakes its event
    # wait and no blocking primitive remains).  A control raised by
    # the join itself is handled by the shared join rule (order
    # 030-a, requirement 5): the join is actually completed, a
    # pending first nonordinary control keeps its exact identity, and
    # otherwise the first nonordinary control from the join-fault
    # cleanup is preserved - and it is captured here so that the
    # phase-owned response cleanup below runs before ANY
    # operation/guard/cleanup control propagates: a join control
    # never skips the untransferred response close.
    completed.set()
    join_control: BaseException | None = None
    try:
        request_lifecycle.join_owned_thread(guard, error)
    except BaseException as exc:
        join_control = exc
    expired = state["expired"] or time.monotonic() >= deadline
    if error is not None and request_lifecycle.is_nonordinary_control(
        error
    ):
        # The current operation's own nonordinary caller control
        # keeps its EXACT first identity over any later deadline,
        # cancellation or cleanup (order 030-a, requirement 5):
        # it is never replaced by a timeout, a cancellation or a
        # transport failure, and no other fallible hook (such as
        # a further cancellation-predicate evaluation) runs
        # before this preservation.
        _close_untransferred(response)
        raise error
    if request_lifecycle.is_nonordinary_control(guard_control):
        # The owned guard's own control is transferred after the
        # guard was actually joined: it is never relabelled as a
        # header timeout or a transport failure (order 030-a,
        # requirement 5).
        _close_untransferred(response)
        raise guard_control
    if request_lifecycle.is_nonordinary_control(join_control):
        # A first nonordinary control from the join-fault cleanup is
        # preserved and propagated only after the join actually
        # completed (order 030-a, requirement 5).
        _close_untransferred(response)
        raise join_control
    # No nonordinary control is pending: the cancellation predicate
    # may now be evaluated for the observed-cancellation
    # classification (it never runs before the nonordinary
    # preservation above).
    observed_cancel = cancelled is not None and (
        state["cancelled"] or cancelled()
    )
    if error is not None:
        if observed_cancel:
            # Observed client cancellation: it is never relabeled as
            # a header timeout or transport error (order 030-a,
            # R3/R4); the interruption caused or accompanied the
            # parser failure.
            _close_untransferred(response)
            raise request_lifecycle.RequestCancelled() from None
        if expired:
            # The deadline passed: this is the header timeout (its
            # interruption caused or accompanied the parser failure),
            # not a plain transport error.
            _close_untransferred(response)
            raise HeaderTimeoutError(
                "response header acquisition exceeded the elapsed "
                "header budget"
            ) from None
        _close_untransferred(response)
        raise error
    assert response is not None, "parser returned without a response"
    if observed_cancel:
        # A racing completion loses to the observed cancellation
        # before transfer: the parsed response is explicitly closed
        # and never used (order 030-a, R3/R4).
        _close_untransferred(response)
        raise request_lifecycle.RequestCancelled() from None
    if expired:
        # Completion racing expiration: the elapsed budget has passed,
        # so the helper refuses to transfer and explicitly closes the
        # parsed response (its buffered reader must not survive the
        # acquisition, even if the connection is already closing).
        _close_untransferred(response)
        raise HeaderTimeoutError(
            "response header acquisition exceeded the elapsed "
            "header budget"
        )
    return response
