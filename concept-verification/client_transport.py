"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Owned
elapsed deadline guard for incoming client request intake.

Order 020-a: one finite positive monotonic incoming-intake deadline
anchored while handling the accepted connection, BEFORE any
request-line/header/body read and before the guard starts.  It covers
waiting for the first byte, the request line, all headers and the
exact advertised body; byte arrival, phase transitions and legitimate
short reads never reset it.  OS accept-backlog waiting (before the
connection is accepted and handled) is outside this scope.

The standard-library request-line/header parser is retained unchanged
and runs on the owning handler thread.  The owned guard is a pure
timer: it owns only a bounded event wait plus a shutdown of the exact
captured accepted socket object, so a waiting read unblocks.  The
guard is cancelled (completion event) and actually joined on every
path - success, EOF, timeout, unsupported method/path, framing
rejection, parse failure, exception or startup failure - so no intake
worker survives the request; startup is inside the clock and a
partial startup is contained (a guard that actually started before a
startup failure is cancelled and actually joined before the failure
propagates, and an unstarted thread is never joined).  The actual
elapsed state is classified after the join: completion racing
expiration loses to expiration and the request can never reach the
downstream work.  No hard-real-time OS scheduling guarantee is made;
the CPU inputs stay finite.

Strict request framing (order 020-a, requirement 3): a supported POST
requires one unambiguous finite decimal Content-Length within the
existing request byte cap; repeated fields (even equal values), comma
lists, any Transfer-Encoding and any unsupported Expect are ambiguous
framing rejected with a fixed content-free 400 before any body read or
forwarding.  A missing length keeps the existing bounded size policy
(413).  Very large numeric fields are rejected boundedly before
integer conversion.
"""

from __future__ import annotations

import contextlib
import math
import socket
import threading
import time
from email.message import Message

from config import API_MAX_REQUEST_BYTES

# Bounded before any integer conversion (order 020-a, requirement 3):
# leading zeros do not change the numeric value, so the significant
# decimal (leading zeros stripped on the derived numeric view, raw
# incoming bytes untouched) is the bounded conversion input; any
# decimal with more significant digits than the cap has (2,000,000 is
# seven digits) is rejected as overlarge before conversion.
_MAX_SIGNIFICANT_DIGITS = len(str(API_MAX_REQUEST_BYTES))


class IntakeTimeoutError(ValueError):
    """Bounded intake failure: the elapsed intake budget expired."""


class FramingRejection:
    """Fixed content-free intake framing rejection (400 or existing 413)."""

    def __init__(self, status: int, code: str) -> None:
        self.status = status
        self.code = code


def validate_client_budget(budget: object) -> float:
    """Return the finite positive intake budget or reject the value.

    Rejects bool, nonnumeric, zero, negative, NaN and infinite values,
    and also values the platform's finite threading wait cannot
    represent: the owned timer waits with one bounded
    ``threading.Event.wait`` call, so a numerically finite setting
    above ``threading.TIMEOUT_MAX`` (or a huge int that does not
    convert to float at all) must be rejected with the fixed
    ValueError before the timer starts, never allowed to silently
    disable the deadline (order 020-a, requirement 1).  The
    constructor validates before any bind allocation and the guard
    validates again at use.
    """
    if (
        isinstance(budget, bool)
        or not isinstance(budget, (int, float))
        or budget <= 0
    ):
        raise ValueError(
            "client timeout must be a finite positive duration"
        )
    if isinstance(budget, int):
        # A huge int may not convert to float at all; the float view
        # is the only one the platform wait can represent.
        try:
            value = float(budget)
        except OverflowError:
            raise ValueError(
                "client timeout must be a finite positive duration"
            ) from None
    else:
        value = budget
    if not math.isfinite(value) or value > threading.TIMEOUT_MAX:
        raise ValueError(
            "client timeout must be a finite positive duration"
        )
    return value


class IntakeGuard:
    """One owned elapsed-intake deadline over the exact accepted socket.

    The absolute monotonic deadline anchors in the constructor BEFORE
    the guard thread starts, so guard startup is inside the clock.
    Startup is owned: if the guard thread actually started before a
    startup failure, it is cancelled and actually joined before the
    failure propagates, whether it still runs or has already ended;
    an unstarted thread is never joined.
    ``release`` cancels and actually joins the pure timer on every
    path (idempotent), so no intake worker survives the request.  On
    expiration the guard shuts down only the captured accepted socket
    object so the handler's waiting read unblocks; it never touches
    another owned connection.  ``release`` returns whether the elapsed
    state is expired after the actual join (a late or racing
    completion loses to expiration).
    """

    def __init__(self, sock: socket.socket, budget: float) -> None:
        validated = validate_client_budget(budget)
        # One absolute monotonic deadline anchored before guard startup
        # (order 020-a, requirement 1); safe state is initialized first
        # so a failed startup has nothing live left behind.
        self._deadline = time.monotonic() + validated
        self._completed = threading.Event()
        self._state = {"expired": False}

        def _guard() -> None:
            remaining = self._deadline - time.monotonic()
            if remaining > 0:
                self._completed.wait(timeout=remaining)
            if not self._completed.is_set():
                # The absolute deadline passed while intake was still
                # in flight: interrupt only the captured accepted
                # socket object so the owning thread's waiting read
                # unblocks.
                self._state["expired"] = True
                with contextlib.suppress(Exception):
                    sock.shutdown(socket.SHUT_RDWR)

        guard = threading.Thread(
            target=_guard, name="concept-client-intake-guard"
        )
        try:
            guard.start()
        except BaseException:
            # Partial-startup ownership: a guard that actually started
            # before the startup failure (thread ident set, whether
            # still alive or already ended) is cancelled and actually
            # joined before the failure propagates; a never-started
            # thread (ident is None) is never joined (order 020-a,
            # requirement 2).
            if guard.ident is not None:
                self._completed.set()
                guard.join()
            raise
        self._guard = guard
        self._released = False

    def release(self) -> bool:
        """Cancel and actually join the guard; return the elapsed state.

        Idempotent: the intake handler releases the guard before
        downstream work and the owning handle_one_request releases it
        again on every remaining path; the second call is a no-op join
        of the already-terminated timer.  No intake worker survives.
        """
        if self._released:
            return self._state["expired"] or time.monotonic() >= self._deadline
        self._released = True
        # Cancel the guard (no interrupt after completion) and actually
        # join the pure timer before any classification or downstream
        # work on every path: the join is blocking because the guard's
        # post-cancel work is itself bounded (no blocking primitive
        # remains after the cancellation).
        self._completed.set()
        self._guard.join()
        return self._state["expired"] or time.monotonic() >= self._deadline


def check_request_framing(headers: Message) -> tuple[int, int, str] | FramingRejection:
    """Strict unambiguous-framing policy for the supported POST.

    Returns ``(0, length, "")`` on an accepted unambiguous finite
    decimal Content-Length, or a :class:`FramingRejection` before any
    body read or forwarding:

    - repeated Content-Length fields (even equal values), comma lists,
      any Transfer-Encoding and any unsupported Expect are ambiguous
      framing: fixed content-free 400 (order 020-a, requirement 3);
    - a missing length, a negative (nondecimal) value, an overlarge
      value or any nondecimal malformed length keeps the existing
      bounded size policy: 413;
    - ordinary header whitespace is parsed under the documented strict
      ASCII decimal policy (surrounding OWS stripped, digits only, no
      sign);
    - very large numeric fields are rejected boundedly before integer
      conversion: the derived numeric view strips leading zeros (raw
      bytes untouched) and any significant decimal longer than the
      cap's own digit count is overlarge by construction.
    """
    if headers.get("Transfer-Encoding") is not None:
        return FramingRejection(400, "REQUEST_FRAMING")
    if headers.get("Expect") is not None:
        return FramingRejection(400, "REQUEST_FRAMING")
    values = headers.get_all("Content-Length")
    if not values:
        # Missing length: existing bounded size policy.
        return FramingRejection(413, "REQUEST_LENGTH")
    if len(values) > 1:
        # Repeated fields are ambiguous framing even when equal.
        return FramingRejection(400, "REQUEST_FRAMING")
    raw = values[0].strip(" \t")
    if "," in raw:
        return FramingRejection(400, "REQUEST_FRAMING")
    if not raw or any(ch < "0" or ch > "9" for ch in raw):
        # Nondecimal malformed length (including a signed value):
        # existing bounded size policy.
        return FramingRejection(413, "REQUEST_LENGTH")
    # Bounded numeric view before integer conversion: leading zeros do
    # not change the value, so only the significant decimal (or "0")
    # is converted; the raw header bytes are preserved and never
    # normalized.
    significant = raw.lstrip("0")
    if len(significant) > _MAX_SIGNIFICANT_DIGITS:
        # More significant digits than the cap has: overlarge by
        # construction, still before integer conversion.
        return FramingRejection(413, "REQUEST_LENGTH")
    length = int(significant) if significant else 0
    if length > API_MAX_REQUEST_BYTES:
        return FramingRejection(413, "REQUEST_LENGTH")
    return (0, length, "")
