"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Owned final-response delivery budget for the accepted client socket
(order 021-a).

One finite positive monotonic delivery deadline anchors immediately
before the final response emission (status line, headers, body and the
actual flush) and BEFORE the owned guard starts, so guard startup is
inside the clock.  Response-ready work - upstream capture and optional
repair - is outside the phase.  Byte progress, short writes, phase
transitions and internal retries never reset the deadline; a per-write
idle socket timeout alone is insufficient.  On expiration the pure
timer guard shuts down only the EXACT captured accepted socket object
so the owning handler's blocking write unblocks; it never touches a
numeric FD, another connection or a reused/later socket.  The guard is
cancelled and actually joined on every path - success, timeout,
disconnect, write/flush error, exception or startup failure, including
a thread that started and already ended before start raises - so no
delivery worker survives the response and nothing is ever armed during
the next connection.  A late or racing completion loses to expiration.

Local kernel acceptance is not proof the peer received or read the
bytes; no delivery acknowledgment is implied and no hard-real-time OS
scheduling guarantee is made.
"""

from __future__ import annotations

import contextlib
import math
import socket
import threading
import time


def validate_delivery_budget(budget: object) -> float:
    """Return the finite positive delivery budget or reject the value.

    Rejects bool, nonnumeric, zero, negative, NaN and infinite values,
    and also values the platform's finite threading wait cannot
    represent: the owned timer waits with one bounded
    ``threading.Event.wait`` call, so a numerically finite setting
    above ``threading.TIMEOUT_MAX`` (or a huge int that does not
    convert to float at all) must be rejected with the fixed
    ValueError before the timer starts, never allowed to silently
    disable the deadline (order 021-a, requirement 1).  The
    constructor validates before any bind allocation and the guard
    validates again at use.
    """
    if (
        isinstance(budget, bool)
        or not isinstance(budget, (int, float))
        or budget <= 0
    ):
        raise ValueError(
            "delivery timeout must be a finite positive duration"
        )
    if isinstance(budget, int):
        # A huge int may not convert to float at all; the float view
        # is the only one the platform wait can represent.
        try:
            value = float(budget)
        except OverflowError:
            raise ValueError(
                "delivery timeout must be a finite positive duration"
            ) from None
    else:
        value = budget
    if not math.isfinite(value) or value > threading.TIMEOUT_MAX:
        raise ValueError(
            "delivery timeout must be a finite positive duration"
        )
    return value


class DeliveryGuard:
    """One owned elapsed-delivery deadline over the exact accepted socket.

    The absolute monotonic deadline anchors in the constructor BEFORE
    the guard thread starts, so guard startup is inside the clock.
    Startup is owned: if the guard thread actually started before a
    startup failure, it is cancelled and actually joined before the
    failure propagates, whether it still runs or has already ended;
    an unstarted thread is never joined.  ``release`` cancels and
    actually joins the pure timer on every path (idempotent), so no
    delivery worker survives the response.  On expiration the guard
    shuts down only the captured accepted socket object so the
    handler's blocked write unblocks; it never touches another owned
    connection.  ``release`` returns whether the elapsed state is
    expired after the actual join (a late or racing completion loses
    to expiration).
    """

    def __init__(self, sock: socket.socket, budget: float) -> None:
        validated = validate_delivery_budget(budget)
        # One absolute monotonic deadline anchored before guard
        # startup (order 021-a, requirement 2); safe state is
        # initialized first so a failed startup has nothing live left
        # behind.
        self._deadline = time.monotonic() + validated
        self._completed = threading.Event()
        self._state = {"expired": False}

        def _guard() -> None:
            remaining = self._deadline - time.monotonic()
            if remaining > 0:
                self._completed.wait(timeout=remaining)
            if not self._completed.is_set():
                # The absolute deadline passed while emission was
                # still in flight: interrupt only the captured
                # accepted socket object so the owning thread's
                # blocked write unblocks.
                self._state["expired"] = True
                with contextlib.suppress(Exception):
                    sock.shutdown(socket.SHUT_RDWR)

        guard = threading.Thread(
            target=_guard, name="concept-client-delivery-guard"
        )
        try:
            guard.start()
        except BaseException:
            # Partial-startup ownership: a guard that actually started
            # before the startup failure (thread ident set, whether
            # still alive or already ended) is cancelled and actually
            # joined before the failure propagates; a never-started
            # thread (ident is None) is never joined (order 021-a,
            # requirement 3).
            if guard.ident is not None:
                self._completed.set()
                guard.join()
            raise
        self._guard = guard
        self._released = False

    def is_expired(self) -> bool:
        """Whether the anchored absolute deadline already passed.

        A synchronous observation against the anchored monotonic
        deadline: it makes no assumption that the owned timer thread
        has been scheduled to run, so the owning handler can detect a
        successful-but-already-spent startup before it begins any
        response emission (order 021-a, requirement 2: late or racing
        completion loses to expiry)."""
        return self._state["expired"] or time.monotonic() >= self._deadline

    def release(self) -> bool:
        """Cancel and actually join the guard; return the elapsed state.

        Idempotent: the owning handler releases the guard on every
        emission path; a second call is a no-op join of the
        already-terminated timer.  No delivery worker survives.
        """
        if self._released:
            return self._state["expired"] or time.monotonic() >= self._deadline
        self._released = True
        # Cancel the guard (no interrupt after completion) and actually
        # join the pure timer before any classification, cleanup or
        # next connection on every path: the join is blocking because
        # the guard's post-cancel work is itself bounded (no blocking
        # primitive remains after the cancellation).
        self._completed.set()
        self._guard.join()
        return self._state["expired"] or time.monotonic() >= self._deadline
