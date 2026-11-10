"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.
Request-owned cancellation scope for the runnable proxy (order 030-a).

One request-local scope starts AFTER fully captured VALID ingress and
BEFORE any owned main work, and covers main setup/header/body, the
optional engine pass and final delivery of exactly one admitted
request.  The scope owns exactly one cancellation event and exactly
one watcher over the EXACT accepted socket object: a pure bounded
``select.poll`` watcher on the disconnect-only mask
``POLLRDHUP | POLLHUP | POLLERR | POLLNVAL`` (value 8248 on the
selected native Linux runtime) with POLLIN deliberately excluded.
The proved native primitive (receipt
NEXT-root-native-disconnect-only-poll-mask-proof) detects the peer FIN
even behind 8192 unread ignored tail bytes, and a still-open peer with
the same extra bytes yields no event in a full bounded slice - so no
tail bytes are ever read, parsed, drained or forwarded, no new tail
quota exists, and no data-readiness busy-spin is possible.

The contained MVP transport policy (documented, not silently
assumed): EOF after a complete VALID request means cancellation, as
do RST and hard transport errors.  Native TCP cannot distinguish a
fully closed peer from a legitimate complete-request write-half-close
(SHUT_WR), so a complete valid SHUT_WR is intentionally UNSUPPORTED:
clients keep both directions open until the response.  Incomplete-body
SHUT_WR keeps the existing bounded 400, and trailing-open-data keeps
the existing first-request-only semantics (both are intake behavior,
unchanged).

The watcher never touches a numeric FD directly: every poll iteration
re-reads the current file descriptor of the captured socket object and
acts only on an event whose descriptor matches it; the owning handler
always stops and actually joins the watcher before the accepted
socket is released or the next request starts, so a reused foreign
numeric FD can never be observed.  ``POLLNVAL`` (descriptor no longer
valid, e.g. closed under the watcher) stops the watcher without
setting the event: it is never acted on as a cancellation.

Explicit pure native capability validation runs before the proxy
binds (order 030-a, requirement 1): a pure selected-native
prerequisite check verifies the required poll interface, the
disconnect constants and the composed disconnect-only mask, and
refuses to start explicitly on any weaker or missing detector -
there is no silent fallback, no runtime self-probe and no discovery.
The ACTUAL native disconnect behavior (FIN/RST behind unread tail,
no data-readiness spin) is proved by the ordered owned
socket/TCP tests, not by startup IO.

Phase cooperation is explicit: transports and owned runners receive
the scope's ``cancelled`` predicate as an ordinary argument captured
into their exact closures (guard threads never assume a ContextVar
propagation).  The owner-thread phase-entry boundaries whose frozen
caller cannot forward an argument instead consult
:func:`active_cancellation_check`, a per-thread slot holding the
CURRENT request's scope: the owned final-forward transport waits,
the Pandoc owned runner, the read-only RuntimeCorpus constructor and
the owned reviewer exchange (whose frozen caller ``qwen_client``
cannot forward an argument).  Under the owning admission
serialization exactly one whole request runs at a time on one handler
thread, the slot is set when the scope starts and cleared when it
finishes on that same thread, and any access outside an active
request (startup, direct core tests, other threads) is a no-op that
returns ``None``.  No global cross-request state and no caller
bypass or header exist: cancellation is observed only from the exact
accepted socket of the one active request.

``RequestCancelled`` is the dedicated contained exception: it carries
one fixed content-free message and never any request, header, body,
text or credential content.  It is raised only at phase boundaries or
bounded owned waits, never replaces a propagating nonordinary caller
control (KeyboardInterrupt/SystemExit/MemoryError), and is caught
inside the owning handler before any optional-original or 502
fallback and before the admission worker boundary.
"""

from __future__ import annotations

import contextlib
import select
import socket
import threading
from collections.abc import Callable
from typing import TypeGuard

# The disconnect-only mask (order 030-a, requirement 2): RDHUP plus
# HUP/ERR plus NVAL.  POLLIN is deliberately excluded so data
# readiness is never read as cancellation.  POLLRDHUP is 8192 on the
# selected native Linux runtime, making the mask 8248; the constant is
# taken from the platform, and its absence is a capability failure at
# validation (no silent weaker detector).
_POLLRDHUP = getattr(select, "POLLRDHUP", 0)
_DISCONNECT_MASK = (
    _POLLRDHUP | select.POLLHUP | select.POLLERR | select.POLLNVAL
)
# Bits that indicate an observed peer disconnect.  POLLNVAL is handled
# separately: it invalidates the watched descriptor and stops the
# watcher without setting the cancellation event.
_CANCEL_BITS = _POLLRDHUP | select.POLLHUP | select.POLLERR
# Bounded watcher wake slice: bounds cancellation notice latency and,
# because the slice is the only blocking wait, is also the worst-case
# join latency of :meth:`CancellationScope.finish`.
_WATCH_SLICE_SECONDS = 0.05


class RequestCancelled(Exception):
    """Contained request-owned client cancellation.

    One fixed content-free message; no request, header, body, text or
    credential content is ever carried (order 030-a, requirement 7).
    """

    def __init__(self) -> None:
        super().__init__("client request was cancelled")


class NativePollCapabilityError(ValueError):
    """The selected native disconnect-poll capability is unavailable.

    Raised before any bind allocation; the proxy refuses to start
    instead of falling back to a weaker detector.
    """

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def is_nonordinary_control(
    exc: BaseException | None,
) -> TypeGuard[BaseException]:
    """Whether ``exc`` is the current operation's nonordinary caller
    control that must keep its exact first identity (order 030-a,
    requirement 5): any nonordinary BaseException (KeyboardInterrupt,
    SystemExit, ...) plus MemoryError, which subclasses Exception
    explicitly.  The guard type narrows the pending control to a
    non-None BaseException for the exact-identity raise sites."""
    if exc is None:
        return False
    if not isinstance(exc, Exception):
        return True
    return isinstance(exc, MemoryError)


def join_owned_thread(
    thread: threading.Thread, first: BaseException | None
) -> None:
    """Actually join an owned thread to completion (order 030-a,
    requirement 5).

    Preserving a control is not completing cleanup: the join is
    retried until it ACTUALLY completes, so an interrupted first join
    (a control raised before the real native join) never leaves the
    owned thread alive or falsely completed.  Shared control rule:
    a pending first control keeps its exact identity when it is
    nonordinary; an ordinary first control cannot acquire authority
    to discard a subsequent first nonordinary control from the
    join-fault cleanup, which is preserved and re-raised only after
    the join has actually completed.
    """
    cleanup_control: BaseException | None = None
    while True:
        try:
            thread.join()
            break
        except BaseException as exc:
            if cleanup_control is None and is_nonordinary_control(exc):
                cleanup_control = exc
    if not is_nonordinary_control(first) and cleanup_control is not None:
        raise cleanup_control


def finish_owned_scope(
    scope: CancellationScope, first: BaseException | None
) -> None:
    """Actually finish an owned scope before the owning request
    returns (order 030-a, requirement 5).

    Retries :meth:`CancellationScope.finish` until the exact owned
    watcher join actually completes (ownership is retained and
    retryable across an interrupted join), then applies the shared
    control rule to any first nonordinary control captured from the
    cleanup while a pending first control - when nonordinary - keeps
    its exact identity.
    """
    cleanup_control: BaseException | None = None
    while True:
        try:
            scope.finish()
            break
        except BaseException as exc:
            if cleanup_control is None and is_nonordinary_control(exc):
                cleanup_control = exc
    if not is_nonordinary_control(first) and cleanup_control is not None:
        raise cleanup_control


# Per-thread current-scope holder (see module docstring): the
# owner-thread consumers whose frozen caller cannot receive the
# check as an argument consult this slot - the owned final-forward
# transport waits, the Pandoc owned runner, the read-only
# RuntimeCorpus constructor and the owned reviewer exchange.  Set
# and cleared on the one handler thread under the owning admission
# serialization; guard threads still receive the explicit captured
# predicate (no ContextVar propagation); reads outside an active
# request are a no-op.
class _ScopeSlot:
    """Fully typed per-thread holder of the current request scope."""

    __slots__ = ("_stores",)

    def __init__(self) -> None:
        self._stores: dict[int, CancellationScope | None] = {}

    def set(self, scope: CancellationScope) -> None:
        self._stores[threading.get_ident()] = scope

    def clear(self, scope: CancellationScope) -> None:
        if self._stores.get(threading.get_ident()) is scope:
            self._stores[threading.get_ident()] = None

    def get(self) -> CancellationScope | None:
        return self._stores.get(threading.get_ident())


_current_slot = _ScopeSlot()


def active_scope() -> CancellationScope | None:
    """The CURRENT request's scope, or ``None`` outside an active
    request (startup, direct core tests, another thread)."""
    return _current_slot.get()


def active_cancellation_check() -> Callable[[], bool] | None:
    """The CURRENT request's cancellation check, or a no-op ``None``.

    Outside an active request (startup, direct core tests, another
    thread) this is a no-op and returns ``None`` (order 030-a,
    requirement 1).
    """
    scope = _current_slot.get()
    return scope.cancelled if scope is not None else None


def _bounded_poll_flags(sock: socket.socket, slice_seconds: float) -> int:
    """One bounded poll on the exact socket object; 0 when unusable.

    The current file descriptor of the captured object is registered
    and an event is returned only when its descriptor matches it; a
    closed or invalidated descriptor yields 0 without acting on any
    foreign numeric FD.
    """
    fd = sock.fileno()
    if fd < 0:
        return 0
    poller = select.poll()
    try:
        poller.register(fd, _DISCONNECT_MASK)
        try:
            events = poller.poll(int(slice_seconds * 1000))
        finally:
            with contextlib.suppress(OSError):
                poller.unregister(fd)
    except OSError:
        return 0
    for event_fd, flags in events:
        if event_fd == fd:
            return flags
    return 0


def validate_native_poll_capability(
) -> None:
    """Explicit pure native capability validation (order 030-a, R1/R2).

    A PURE selected-native prerequisite check that runs before any
    bind allocation (order 030-a, requirement 1): it verifies the
    required poll interface, the disconnect constants and the
    composed disconnect-only mask, and refuses to start explicitly on
    any weaker or missing detector.  There is no runtime socket/IO
    self-probe, no fallback and no discovery: the ACTUAL native
    disconnect behavior (FIN/RST behind an unread tail, no
    data-readiness spin) is proved by the ordered owned socket/TCP
    tests, not by startup IO.

    Raises :class:`NativePollCapabilityError` on a missing POLLRDHUP,
    a missing or zero event mask, a missing poll interface or a mask
    that admits data readiness.
    """
    if _POLLRDHUP == 0:
        raise NativePollCapabilityError(
            "native disconnect poll: POLLRDHUP unavailable"
        )
    if _CANCEL_BITS == 0 or _DISCONNECT_MASK == 0:
        raise NativePollCapabilityError(
            "native disconnect poll: event mask unavailable"
        )
    if not callable(getattr(select, "poll", None)):
        raise NativePollCapabilityError(
            "native disconnect poll: poll interface unavailable"
        )
    if _DISCONNECT_MASK & select.POLLIN:
        # Data readiness is never cancellation: the mask must stay
        # disconnect-only (order 030-a, requirement 2).
        raise NativePollCapabilityError(
            "native disconnect poll: data readiness must be excluded"
        )


class CancellationScope:
    """One request-local cancellation scope over one exact socket.

    ``start`` performs one bounded synchronous first check (catching
    an already-disconnected queued client before any future main work)
    and then starts the one bounded poll watcher; ``finish`` stops and
    actually joins the watcher and drops the socket reference so no
    canceled-request resource or text is retained idle.  ``start`` /
    ``finish`` are idempotency-guarded in that order (a second start
    is an error; a second finish is a no-op).
    """

    def __init__(self, sock: socket.socket) -> None:
        self._sock: socket.socket | None = sock
        self._cancelled = threading.Event()
        self._stop = threading.Event()
        self._watcher: threading.Thread | None = None
        self._started = False
        self._finished = False
        # Request-local attempted-dispatch marker (order 030-a, R7):
        # set by the parent side of the owned reviewer exchange AFTER
        # the pure frame/request bounds and BEFORE the actual owned
        # launch, so an interrupted exchange is distinguished from a
        # pre-dispatch cancellation.
        self._review_dispatch_attempted = False

    def cancelled(self) -> bool:
        """Whether a disconnect was observed for this request."""
        return self._cancelled.is_set()

    def mark_review_dispatch_attempted(self) -> None:
        """Record one attempted owned reviewer dispatch (no-op-safe)."""
        self._review_dispatch_attempted = True

    def review_dispatch_attempted(self) -> bool:
        """Whether the owned reviewer dispatch was actually attempted."""
        return self._review_dispatch_attempted

    def raise_if_cancelled(self) -> None:
        """Raise the dedicated contained exception at a phase boundary."""
        if self._cancelled.is_set():
            raise RequestCancelled

    def start(self) -> None:
        """Synchronous first check plus the one bounded watcher start."""
        if self._started:
            raise ValueError("cancellation scope already started")
        self._started = True
        sock = self._sock
        if sock is None or sock.fileno() < 0:
            # The exact accepted socket is already unusable: cancel
            # immediately so no owned main work can start.
            self._cancelled.set()
        else:
            flags = _bounded_poll_flags(sock, 0.0)
            if flags & _CANCEL_BITS or flags & select.POLLNVAL:
                self._cancelled.set()
            else:
                # Ownership is established BEFORE the fallible start:
                # a transparent start that actually launches the thread
                # and then faults still leaves the exact owned watcher
                # reachable by finish for a real stop/join; the exact
                # first caller control is preserved and a control from
                # the cleanup join itself never replaces it (order
                # 030-a, requirement 5).
                watcher = threading.Thread(
                    target=self._watch, name="concept-cancellation-watch"
                )
                self._watcher = watcher
                try:
                    watcher.start()
                except BaseException as exc:
                    if watcher.ident is not None:
                        self._stop.set()
                        join_owned_thread(watcher, exc)
                    raise
        _current_slot.set(self)

    def _watch(self) -> None:
        # The stdlib select.poll object needs no explicit close; it is
        # released with the watcher frame.  Every iteration re-reads
        # the current descriptor of the exact captured socket object
        # and acts only on a matching event (no foreign numeric FD).
        poller = select.poll()
        while not self._stop.is_set():
            sock = self._sock
            if sock is None:
                break
            fd = sock.fileno()
            if fd < 0:
                break
            try:
                poller.register(fd, _DISCONNECT_MASK)
                try:
                    events = poller.poll(int(_WATCH_SLICE_SECONDS * 1000))
                finally:
                    with contextlib.suppress(OSError):
                        poller.unregister(fd)
            except OSError:
                # The exact descriptor closed/invalidated under the
                # check: stop watching; never act on a foreign FD.
                break
            for event_fd, flags in events:
                if event_fd != fd:
                    continue
                if flags & select.POLLNVAL:
                    return
                if flags & _CANCEL_BITS:
                    self._cancelled.set()
                    return

    def finish(self) -> None:
        """Stop and actually join the watcher; release the socket.

        Bounded: the watcher's only blocking wait is one poll slice, so
        the join completes within one slice.  Idempotent.  The
        watcher reference, the socket reference and the finished flag
        are cleared only AFTER a successful join: an interrupted join
        (exact first caller control preserved and re-raised) leaves
        the ownership intact and retryable, never falsely completed.
        """
        if self._finished:
            return
        _current_slot.clear(self)
        self._stop.set()
        watcher = self._watcher
        if watcher is not None and watcher.ident is not None:
            watcher.join()
        self._watcher = None
        self._sock = None
        self._finished = True
