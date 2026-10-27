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


class HeaderTimeoutError(ValueError):
    """Bounded main failure: the elapsed header budget expired."""


class HeaderSetupError(ValueError):
    """Bounded main failure: the owned transport was not ready for
    header acquisition (no captured owned socket object)."""


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
    connection: http.client.HTTPConnection,
    budget: object,
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
    state = {"expired": False}

    def _guard() -> None:
        remaining = deadline - time.monotonic()
        if remaining > 0:
            completed.wait(timeout=remaining)
        if not completed.is_set():
            # The absolute deadline passed while acquisition was still
            # in flight: interrupt only the captured owned socket
            # object so the owning thread's parser read unblocks.
            state["expired"] = True
            with contextlib.suppress(Exception):
                sock.shutdown(socket.SHUT_RDWR)

    guard = threading.Thread(target=_guard, name="concept-header-guard")
    guard.start()
    response: http.client.HTTPResponse | None = None
    error: BaseException | None = None
    try:
        try:
            response = connection.getresponse()
        except BaseException as exc:  # noqa: B036 - classified below
            error = exc
    finally:
        # Cancel the guard (no interrupt after completion) and actually
        # join the pure timer before any classification or transfer on
        # both success and failure: no late timer and no header work
        # outlives acquisition.  The join is blocking because the
        # guard's post-cancel work is bounded (the cancellation wakes
        # its event wait and no blocking primitive remains).
        completed.set()
        guard.join()
    expired = state["expired"] or time.monotonic() >= deadline
    if error is not None:
        if expired:
            # The deadline passed: this is the header timeout (its
            # interruption caused or accompanied the parser failure),
            # not a plain transport error.
            raise HeaderTimeoutError(
                "response header acquisition exceeded the elapsed "
                "header budget"
            ) from None
        raise error
    assert response is not None, "parser returned without a response"
    if expired:
        # Completion racing expiration: the elapsed budget has passed,
        # so the helper refuses to transfer and explicitly closes the
        # parsed response (its buffered reader must not survive the
        # acquisition, even if the connection is already closing).
        with contextlib.suppress(Exception):
            response.close()
        raise HeaderTimeoutError(
            "response header acquisition exceeded the elapsed "
            "header budget"
        )
    return response
