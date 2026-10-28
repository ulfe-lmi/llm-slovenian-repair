"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Owned elapsed deadline for the main-upstream setup phase (order
022-a).

One finite positive monotonic setup deadline is anchored by the
owner (``ConceptProxy.forward``) at entry to the owned main forward
setup, BEFORE any worker/guard/process/IPC startup, resolver call,
connect/TLS or request emission.  It covers the entire setup phase:
owned transport startup, address resolution (one owned ordinary
stdlib child for named hosts; an IP-literal host needs no child),
bounded address attempts, TCP connection, the TLS handshake and the
entire request write through the last body byte handed to the local
transport.  Byte progress, short writes, address attempts and phase
transitions never reset it: a per-operation socket timeout alone is
insufficient, so every blocking operation is additionally capped by
the remaining deadline and a pure timer guard - which can interrupt
only the exact socket object it currently holds - covers phases
composed of many short blocking operations (TLS handshake, request
write).  A late or racing setup completion loses to expiration.

The resolver runs in the owned child because no parent socket exists
yet for a timer to interrupt: a timer cannot interrupt
``getaddrinfo`` merely by closing a socket that does not exist, and
timing out a Future/daemon thread does not cancel it.  The parent
contains the noninterruptible resolution by terminating and actually
reaping the exact child on expiration.  The child speaks a private
strict versioned bounded frame protocol over private pipes with an
empty environment, an argv array and no shell; no body, request,
credential or secret data ever transits argv, env, tempfiles or
logs.  The parent's pipe descriptors are nonblocking and every
partial write/read and readiness race is governed by the remaining
deadline, so a stalled or shrunken pipe cannot block past the bound.

A successful setup releases its clock (the guard is cancelled and
actually joined) BEFORE actual response-header acquisition; the
existing header/body, intake and delivery clocks then run as before
on their own independent axes.  Setup failure is a main failure
(the handler's existing fixed content-free 502 path) with zero
engine, corpus or reviewer work and no fabricated completion.
Local write completion is not peer receipt or model-execution
acknowledgment; cleanup and OS scheduling can add elapsed time past
the deadline before the bounded return, and no hard-real-time
scheduling guarantee is made.
"""

from __future__ import annotations

import contextlib
import errno
import fcntl
import http.client
import ipaddress
import math
import os
import select
import socket
import ssl
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import cast

UPSTREAM_SETUP_VERSION = 1

# Fixed content-free diagnostic labels (closed set; no exception
# text, host, address, header value or credential is ever carried).
REASON_DEADLINE = "SETUP_DEADLINE"
REASON_TRANSPORT = "SETUP_TRANSPORT"

_FIXED_MESSAGES = {
    REASON_DEADLINE: "main upstream setup deadline expired",
    REASON_TRANSPORT: "main upstream setup transport failed",
}

# Finite IPC caps (order 022-a, requirement 4).  The resolver frame
# carries one bounded host and returns one bounded unique address
# list; no body, credential or request data ever transits this
# channel.
_MAGIC = b"USTX"
_KIND_REQUEST = 1
_KIND_RESPONSE = 2
_STATUS_OK = 0
_STATUS_FAILED = 1
_FAMILY_INET = 1
_FAMILY_INET6 = 2
_HOST_MAX_BYTES = 255
_ADDRESS_MAX_BYTES = 64
_ADDRESS_COUNT_MAX = 16
_FRAME_PREFIX = struct.Struct(">Q")
_REQUEST_HEADER = struct.Struct(">4sBBHH")  # magic, version, kind, host_len, port
_RESPONSE_HEADER = struct.Struct(">4sBBBH")  # magic, version, kind, status, count
_REQUEST_FIXED_BYTES = _REQUEST_HEADER.size
_RESPONSE_FIXED_BYTES = _RESPONSE_HEADER.size
REQUEST_FRAME_MAX_BYTES = _REQUEST_FIXED_BYTES + _HOST_MAX_BYTES
RESPONSE_FRAME_MAX_BYTES = _RESPONSE_FIXED_BYTES + _ADDRESS_COUNT_MAX * (
    2 + _ADDRESS_MAX_BYTES
)

# Bounded cleanup slices for terminating and reaping the exact owned
# child; finite and honestly accounted, not a deadline extension.
_CLEANUP_SLICE_SECONDS = 0.5
_CLEANUP_POLL_SECONDS = 0.05

# The wire family bytes are stable protocol constants; native
# AF_* values are platform-dependent and are introduced at exactly
# one boundary (after decode, before connect), never inside the
# codec.
_WIRE_TO_NATIVE_FAMILY = {}

_WORKER_PATH = Path(__file__).resolve().with_name("upstream_worker.py")
_WIRE_TO_NATIVE_FAMILY = {
    _FAMILY_INET: socket.AF_INET,
    _FAMILY_INET6: socket.AF_INET6,
}


class UpstreamSetupError(ValueError):
    """Owned main-upstream setup failure; ``reason`` is a fixed label."""

    def __init__(self, message: str, reason: str) -> None:
        super().__init__(message)
        self.reason = reason


class DeadlineExceeded(Exception):
    """The anchored absolute setup deadline passed before a phase
    finished."""


class FrameMalformed(Exception):
    """A private pipe frame violated the strict versioned contract."""


class FrameIncomplete(Exception):
    """The pipe ended before a complete frame arrived."""


class ProcessFailure(Exception):
    """The owned resolver child exited nonzero, could not start, or
    its reply violated the contract."""


def validate_setup_budget(budget: object) -> float:
    """Return the finite positive setup budget or reject the value.

    Rejects bool, nonnumeric, zero, negative, NaN and infinite
    values, and also values the platform's finite threading wait
    cannot represent: the owned guard waits with one bounded
    ``threading.Event.wait`` call, so a numerically finite setting
    above ``threading.TIMEOUT_MAX`` (or a huge int that does not
    convert to float at all) must be rejected with the fixed
    ValueError before the guard starts, never allowed to silently
    disable the deadline (order 022-a, requirement 1).  The
    constructor validates before any bind allocation and the setup
    path validates again at use.
    """
    if (
        isinstance(budget, bool)
        or not isinstance(budget, (int, float))
        or budget <= 0
    ):
        raise ValueError("setup timeout must be a finite positive duration")
    if isinstance(budget, int):
        # A huge int may not convert to float at all; the float view
        # is the only one the platform wait can represent.
        try:
            value = float(budget)
        except OverflowError:
            raise ValueError(
                "setup timeout must be a finite positive duration"
            ) from None
    else:
        value = budget
    if not math.isfinite(value) or value > threading.TIMEOUT_MAX:
        raise ValueError("setup timeout must be a finite positive duration")
    return value


def _fixed_message(reason: str) -> str:
    return _FIXED_MESSAGES[reason]


class SetupGuard:
    """One owned elapsed-setup deadline over the exact current socket.

    The absolute monotonic deadline is anchored by the owner at
    entry to the setup (before this guard starts and before any
    worker or process startup), so guard startup is inside the
    clock.  The guard is a pure timer: it owns only a bounded event
    wait plus a shutdown of the exact socket object last bound with
    :meth:`adopt`, so a blocked connect, handshake or write
    unblocks; it never touches a numeric FD, another connection or a
    later socket.  Startup is owned: a guard thread that actually
    started before a startup failure is cancelled and actually
    joined (whether still running or already ended); a never-started
    thread is never joined.  :meth:`release` cancels and actually
    joins the guard on every path (idempotent) and returns whether
    the elapsed state is expired after the actual join (a late or
    racing completion loses to expiration).
    """

    def __init__(self, deadline: float) -> None:
        if not math.isfinite(deadline):
            raise ValueError("setup deadline is not finite")
        self._deadline = deadline
        self._completed = threading.Event()
        self._lock = threading.Lock()
        self._current: socket.socket | None = None
        self._state = {"expired": False}

        def _guard() -> None:
            remaining = self._deadline - time.monotonic()
            if remaining > 0:
                self._completed.wait(
                    timeout=min(remaining, threading.TIMEOUT_MAX)
                )
            if not self._completed.is_set():
                self._state["expired"] = True
                with self._lock:
                    sock = self._current
                if sock is not None:
                    with contextlib.suppress(Exception):
                        sock.shutdown(socket.SHUT_RDWR)

        guard = threading.Thread(target=_guard, name="concept-setup-guard")
        try:
            guard.start()
        except BaseException:
            # Partial-startup ownership: a guard that actually
            # started before the startup failure (thread ident set,
            # whether still alive or already ended) is cancelled and
            # actually joined before the failure propagates; a
            # never-started thread (ident is None) is never joined
            # (order 022-a, requirement 3).
            if guard.ident is not None:
                self._completed.set()
                guard.join()
            raise
        self._guard = guard
        self._released = False

    def adopt(self, sock: socket.socket) -> bool:
        """Bind the guard's interrupt to one exact socket object.

        Called immediately before each potentially blocking phase,
        with the exact socket object that phase will block on.  The
        TLS wrap returns a NEW socket object and detaches the
        pre-wrap one, so the wrapped object must be adopted before
        the handshake; the guard never keeps an interrupt target
        that no longer owns the file descriptor.  Returns False and
        keeps the previous target when the guard has already
        expired: an already-fired guard must not be bypassed by
        adopting a new socket (order 022-a, requirement 3).
        """
        if self._state["expired"] or time.monotonic() >= self._deadline:
            return False
        with self._lock:
            self._current = sock
        return True

    def is_expired(self) -> bool:
        """Synchronous observation against the anchored deadline.

        Makes no assumption that the owned timer thread has been
        scheduled to run, so the owner can detect a
        successful-but-already-spent phase before it continues.
        """
        return self._state["expired"] or time.monotonic() >= self._deadline

    def release(self) -> bool:
        """Cancel and actually join the guard; return the elapsed
        state.

        Idempotent: the owner releases the guard on every setup
        path; a second call is a no-op join of the already-terminated
        timer.  No setup worker survives the forward.
        """
        if self._released:
            return self._state["expired"] or time.monotonic() >= self._deadline
        self._released = True
        # Cancel the guard (no interrupt after completion) and
        # actually join the pure timer before any classification,
        # cleanup or return on every path: the join is blocking
        # because the guard's post-cancel work is itself bounded
        # (no blocking primitive remains after the cancellation).
        self._completed.set()
        self._guard.join()
        return self._state["expired"] or time.monotonic() >= self._deadline


def _decode_host(data: bytes) -> str:
    if not data or len(data) > _HOST_MAX_BYTES:
        raise FrameMalformed("resolver host exceeds bound")
    if b"\x00" in data:
        raise FrameMalformed("resolver host contains NUL")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        raise FrameMalformed("resolver host is not UTF-8") from None


def encode_request_frame(*, host: str, port: int) -> bytes:
    """Encode one strict versioned resolver request frame (wire-ready).

    ``port`` keeps the full 16-bit meaning: the concrete numeric
    upstream port (the scheme default resolved by the owner); a bool
    or out-of-range port is rejected before encoding.
    """
    if (
        not isinstance(port, int)
        or isinstance(port, bool)
        or not 1 <= port <= 0xFFFF
    ):
        raise FrameMalformed("resolver port is out of range")
    host_bytes = host.encode("utf-8")
    if not host_bytes or len(host_bytes) > _HOST_MAX_BYTES:
        raise FrameMalformed("resolver host exceeds bound")
    frame = (
        _REQUEST_HEADER.pack(
            _MAGIC, UPSTREAM_SETUP_VERSION, _KIND_REQUEST,
            len(host_bytes), port,
        )
        + host_bytes
    )
    assert len(frame) <= REQUEST_FRAME_MAX_BYTES
    return _FRAME_PREFIX.pack(len(frame)) + frame


def decode_request_frame(frame: bytes) -> tuple[str, int]:
    """Strictly decode one request frame; reject any deviation."""
    if len(frame) > REQUEST_FRAME_MAX_BYTES:
        raise FrameMalformed("resolver request frame exceeds bound")
    if len(frame) < _REQUEST_FIXED_BYTES:
        raise FrameMalformed("resolver request frame is truncated")
    magic, version, kind, host_len, port = _REQUEST_HEADER.unpack_from(
        frame, 0
    )
    if (
        magic != _MAGIC
        or version != UPSTREAM_SETUP_VERSION
        or kind != _KIND_REQUEST
    ):
        raise FrameMalformed("resolver request frame identity is invalid")
    if len(frame) != _REQUEST_FIXED_BYTES + host_len:
        raise FrameMalformed("resolver request frame length is inconsistent")
    if not 1 <= port <= 0xFFFF:
        raise FrameMalformed("resolver port is out of range")
    return _decode_host(frame[_REQUEST_FIXED_BYTES:]), port


def _family_of_address_text(address: str) -> int | None:
    """The protocol family an address text actually denotes, or None."""
    try:
        value = ipaddress.ip_address(address)
    except ValueError:
        return None
    return _FAMILY_INET if value.version == 4 else _FAMILY_INET6


def encode_response_frame(*, addresses: list[tuple[int, str]]) -> bytes:
    """Encode one strict versioned resolver response frame (wire-ready)."""
    if len(addresses) > _ADDRESS_COUNT_MAX:
        raise FrameMalformed("resolver address count exceeds bound")
    seen: set[tuple[int, bytes]] = set()
    payload = bytearray()
    for family, address in addresses:
        if family not in (_FAMILY_INET, _FAMILY_INET6):
            raise FrameMalformed("resolver address family is unknown")
        address_bytes = address.encode("utf-8")
        if not address_bytes or len(address_bytes) > _ADDRESS_MAX_BYTES:
            raise FrameMalformed("resolver address exceeds bound")
        key = (family, address_bytes)
        if key in seen:
            raise FrameMalformed("resolver address list is not unique")
        seen.add(key)
        payload.append(family)
        payload.append(len(address_bytes))
        payload.extend(address_bytes)
    header = _RESPONSE_HEADER.pack(
        _MAGIC, UPSTREAM_SETUP_VERSION, _KIND_RESPONSE,
        _STATUS_OK, len(addresses),
    )
    frame = header + bytes(payload)
    assert len(frame) <= RESPONSE_FRAME_MAX_BYTES
    return _FRAME_PREFIX.pack(len(frame)) + frame


def encode_failure_frame() -> bytes:
    """Encode one well-formed resolver failure frame (no data)."""
    header = _RESPONSE_HEADER.pack(
        _MAGIC, UPSTREAM_SETUP_VERSION, _KIND_RESPONSE,
        _STATUS_FAILED, 0,
    )
    return _FRAME_PREFIX.pack(len(header)) + header


def decode_response_frame(frame: bytes) -> list[tuple[int, str]]:
    """Strictly decode one response frame; reject any deviation.

    Returns the validated unique ``(family, address-text)`` list;
    the empty list is a well-formed failure (no usable address) and
    is classified by the caller.  The family byte must agree with
    the address text's actual numeric form (wrong-kind
    rejection), every entry must be a valid IP literal within the
    bounds, and no entry may be repeated.
    """
    if len(frame) > RESPONSE_FRAME_MAX_BYTES:
        raise FrameMalformed("resolver response frame exceeds bound")
    if len(frame) < _RESPONSE_FIXED_BYTES:
        raise FrameMalformed("resolver response frame is truncated")
    magic, version, kind, status, count = _RESPONSE_HEADER.unpack_from(
        frame, 0
    )
    if (
        magic != _MAGIC
        or version != UPSTREAM_SETUP_VERSION
        or kind != _KIND_RESPONSE
    ):
        raise FrameMalformed("resolver response frame identity is invalid")
    if status not in (_STATUS_OK, _STATUS_FAILED):
        raise FrameMalformed("resolver response frame status is unknown")
    if status == _STATUS_FAILED:
        if count != 0 or len(frame) != _RESPONSE_FIXED_BYTES:
            raise FrameMalformed("resolver failure frame carries data")
        return []
    if count == 0 or count > _ADDRESS_COUNT_MAX:
        raise FrameMalformed("resolver address count exceeds bound")
    offset = _RESPONSE_FIXED_BYTES
    seen: set[tuple[int, bytes]] = set()
    addresses: list[tuple[int, str]] = []
    for _ in range(count):
        if offset + 2 > len(frame):
            raise FrameMalformed("resolver response frame is truncated")
        family = frame[offset]
        address_len = frame[offset + 1]
        offset += 2
        if address_len == 0 or address_len > _ADDRESS_MAX_BYTES:
            raise FrameMalformed("resolver address exceeds bound")
        if offset + address_len > len(frame):
            raise FrameMalformed("resolver response frame is truncated")
        address_bytes = frame[offset : offset + address_len]
        offset += address_len
        if family not in (_FAMILY_INET, _FAMILY_INET6):
            raise FrameMalformed("resolver address family is unknown")
        try:
            address = address_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise FrameMalformed("resolver address is not UTF-8") from None
        actual = _family_of_address_text(address)
        if actual is None:
            raise FrameMalformed("resolver address is not an IP literal")
        if actual != family:
            raise FrameMalformed("resolver address family disagrees")
        key = (family, address_bytes)
        if key in seen:
            raise FrameMalformed("resolver address list is not unique")
        seen.add(key)
        addresses.append((family, address))
    if offset != len(frame):
        raise FrameMalformed("resolver response frame carries extra data")
    return addresses


def _make_pipe_nonblocking(fd: int) -> None:
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


def _select_governed(
    readable_fd: int | None, writeable_fd: int | None, deadline: float
) -> None:
    """Wait for one governed readiness slice before a pipe operation."""
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise DeadlineExceeded
        readable, writeable, _ = select.select(
            [readable_fd] if readable_fd is not None else [],
            [writeable_fd] if writeable_fd is not None else [],
            [],
            min(remaining, 0.05),
        )
        if readable or writeable:
            return


def _read_exact_governed(fd: int, count: int, deadline: float) -> bytes:
    """Read exactly ``count`` bytes from a nonblocking fd under the
    deadline; partial reads and readiness races stay governed."""
    buffer = bytearray()
    while len(buffer) < count:
        _select_governed(fd, None, deadline)
        try:
            chunk = os.read(fd, count - len(buffer))
        except BlockingIOError:
            continue
        if not chunk:
            raise FrameIncomplete
        buffer.extend(chunk)
    return bytes(buffer)


def _read_frame_governed(fd: int, max_bytes: int, deadline: float) -> bytes:
    prefix = _read_exact_governed(fd, _FRAME_PREFIX.size, deadline)
    (frame_len,) = _FRAME_PREFIX.unpack(prefix)
    if frame_len == 0 or frame_len > max_bytes:
        raise FrameMalformed("resolver frame length exceeds bound")
    return _read_exact_governed(fd, frame_len, deadline)


def _write_all_governed(fd: int, data: bytes, deadline: float) -> None:
    """Write all bytes to a nonblocking fd under the deadline; partial
    writes on a stalled or shrunken pipe stay governed, never a
    deadline-unsafe blocking write."""
    view = memoryview(data)
    offset = 0
    while offset < len(view):
        _select_governed(None, fd, deadline)
        try:
            written = os.write(fd, view[offset:])
        except BlockingIOError:
            continue
        if written <= 0:
            raise FrameIncomplete
        offset += written


def _wait_exit_governed(proc: subprocess.Popen[bytes], deadline: float) -> int:
    while True:
        code = proc.poll()
        if code is not None:
            return code
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise DeadlineExceeded
        try:
            return proc.wait(timeout=min(remaining, 0.05))
        except subprocess.TimeoutExpired:
            continue


def _terminate_and_reap(proc: subprocess.Popen[bytes]) -> None:
    """Terminate, kill if needed, and actually wait/reap the exact
    child before return.  A pre-allocated instance whose constructor
    never created a child has no pid and is a no-op: waitpid on an
    unset pid could touch other owned children, so the never-created
    state is distinguished by the unset pid, never by a process
    scan; an already-ended created child is reaped by the first
    poll without a signal.  Bounded polls cover the ordinary paths;
    if the child still cannot be reaped after SIGKILL, the final
    wait blocks until the kernel reaps it - an OS scheduling delay
    is honestly waited out, never converted into a live-child escape
    (order 022-a, requirement 3)."""
    if getattr(proc, "pid", None) is None:
        return
    if proc.poll() is None:
        with contextlib.suppress(OSError):
            proc.terminate()
        for _ in range(int(_CLEANUP_SLICE_SECONDS / _CLEANUP_POLL_SECONDS)):
            if proc.poll() is not None:
                return
            time.sleep(_CLEANUP_POLL_SECONDS)
    if proc.poll() is None:
        with contextlib.suppress(OSError):
            proc.kill()
    proc.wait()


def _resolver_argv() -> list[str]:
    """The exact owned argv for the repository-local resolver child:
    the running interpreter in isolated mode, no shell, no site, no
    bytecache, one trusted versioned script path."""
    return [sys.executable, "-I", "-S", "-B", str(_WORKER_PATH)]


def _resolve_literal(host: str) -> list[tuple[int, str]] | None:
    """An IP-literal host needs no child: the parse is local and
    nonblocking, so there is nothing to interrupt."""
    try:
        value = ipaddress.ip_address(host)
    except ValueError:
        return None
    if value.version == 4:
        return [(socket.AF_INET, host)]
    return [(socket.AF_INET6, host)]


def resolve_addresses(
    host: str, port: int, deadline: float
) -> list[tuple[int, str]]:
    """Resolve the upstream host to a bounded unique address list.

    An IP-literal host is returned directly (no child).  A named
    host is resolved by one owned ordinary stdlib child over the
    private strict frame channel; the parent's anchored
    ``deadline`` governs spawn, IPC and the child's actual
    ``getaddrinfo``, and a late or racing frame loses to expiration.
    On every path the exact child is terminated if still alive and
    actually wait/reaped, and every owned descriptor is closed,
    before return (order 022-a, requirement 3).
    """
    if not math.isfinite(deadline) or deadline - time.monotonic() <= 0:
        raise UpstreamSetupError(
            _fixed_message(REASON_DEADLINE), REASON_DEADLINE
        )
    literal = _resolve_literal(host)
    if literal is not None:
        return literal
    frame = encode_request_frame(host=host, port=port)
    request_read = -1
    request_write = -1
    response_read = -1
    response_write = -1
    allocated: list[int] = []
    try:
        request_read, request_write = os.pipe()
        allocated.extend((request_read, request_write))
        response_read, response_write = os.pipe()
        allocated.extend((response_read, response_write))
        _make_pipe_nonblocking(request_write)
        _make_pipe_nonblocking(response_read)
    except BaseException as exc:
        # Owned cleanup over the allocation/startup stage itself:
        # every already-created descriptor is closed on ordinary
        # errors AND on caller interruption (a second-allocation
        # KeyboardInterrupt must not leak the first pipe); ordinary
        # failures keep the fixed content-free transport failure,
        # and nonordinary interruption is re-raised, never mapped
        # into an ordinary failure (order 022-a, requirement 3).
        for fd in allocated:
            with contextlib.suppress(OSError):
                os.close(fd)
        if isinstance(exc, OSError):
            raise UpstreamSetupError(
                _fixed_message(REASON_TRANSPORT), REASON_TRANSPORT
            ) from exc
        raise
    proc: subprocess.Popen[bytes] | None = None
    open_fds: list[int] = [
        request_read, request_write, response_read, response_write
    ]
    result: list[tuple[int, str]] | None = None
    internal_error: BaseException | None = None
    try:
        # Pre-allocated owned process: the parent owns the exact
        # process object BEFORE the fallible start can create any
        # child, so a caller interruption inside the constructor
        # after actual child creation still leaves the owning
        # instance (and its pid) reachable by the finally below for
        # terminate, kill escalation and an actual wait/reap instead
        # of an orphaned child.  The pre-allocation itself sits
        # inside the owned cleanup scope, so its failure leaves no
        # child and the pipe descriptors are still closed (order
        # 022-a, requirement 3).
        proc = subprocess.Popen.__new__(subprocess.Popen)
        try:
            # Minimal explicit environment: the resolver child needs
            # nothing from the parent (no TLS trust reference, no
            # locale, no secret); an argv array, no shell.  The real
            # unmodified Popen construction runs on the pre-allocated
            # owned instance.
            subprocess.Popen.__init__(
                proc,
                _resolver_argv(),
                stdin=request_read,
                stdout=response_write,
                stderr=subprocess.DEVNULL,
                env={},
                close_fds=True,
            )
        except OSError as exc:
            raise ProcessFailure("owned resolver child could not start") from exc
        # The child now owns its copies of the pipe ends; the parent
        # drops the two ends it does not use immediately.
        os.close(request_read)
        os.close(response_write)
        open_fds.remove(request_read)
        open_fds.remove(response_write)
        _write_all_governed(request_write, frame, deadline)
        os.close(request_write)
        open_fds.remove(request_write)
        reply = _read_frame_governed(response_read, RESPONSE_FRAME_MAX_BYTES, deadline)
        # Strict single-frame check: exactly one frame, then the pipe
        # ends; any extra byte is a malformed reply.
        _select_governed(response_read, None, deadline)
        try:
            extra = os.read(response_read, 1)
        except BlockingIOError:
            extra = b""
        if extra:
            raise FrameMalformed("resolver reply carries extra data")
        code = _wait_exit_governed(proc, deadline)
        if code != 0:
            raise ProcessFailure("owned resolver child exited nonzero")
        decoded = decode_response_frame(reply)
        # Expiry is checked after completion: a racing or late valid
        # frame loses to the deadline and is never used.
        if time.monotonic() >= deadline:
            raise DeadlineExceeded
        if not decoded:
            raise ProcessFailure("owned resolver child returned no usable address")
        # The single wire-to-native family boundary: the codec keeps
        # stable protocol constants; connect needs native AF_*.
        result = [
            (_WIRE_TO_NATIVE_FAMILY[family], address)
            for family, address in decoded
        ]
    except (
        DeadlineExceeded,
        FrameMalformed,
        FrameIncomplete,
        ProcessFailure,
        OSError,
    ) as exc:
        internal_error = exc
    finally:
        if proc is not None:
            _terminate_and_reap(proc)
        for fd in open_fds:
            with contextlib.suppress(OSError):
                os.close(fd)
    if internal_error is not None:
        reason = (
            REASON_DEADLINE
            if isinstance(internal_error, DeadlineExceeded)
            else REASON_TRANSPORT
        )
        raise UpstreamSetupError(_fixed_message(reason), reason) from internal_error
    assert result is not None
    return result


def _require_deadline(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise DeadlineExceeded


def _connect_phase(
    addresses: list[tuple[int, str]],
    port: int,
    deadline: float,
    capture_timeout: float,
    guard: SetupGuard,
) -> socket.socket:
    """Bounded address attempts: each validated address is connected
    to at most once (no retry, no reset); every attempt is capped by
    the remaining deadline in addition to the guard."""
    last: OSError | None = None
    chosen: socket.socket | None = None
    for family, address in addresses:
        if deadline - time.monotonic() <= 0:
            raise DeadlineExceeded
        sock = socket.socket(family, socket.SOCK_STREAM)
        try:
            if not guard.adopt(sock):
                raise DeadlineExceeded
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise DeadlineExceeded
            sock.settimeout(min(capture_timeout, remaining))
            sock.connect((address, port))
            chosen = sock
            break
        except BaseException as exc:  # noqa: B036 - re-raised below
            # The exact owned socket is closed on EVERY failure kind
            # (including caller interruption) before classification;
            # only a nonexpired transport error tries the next
            # validated address (bounded attempts, no reset).
            with contextlib.suppress(OSError):
                sock.close()
            if (
                not isinstance(exc, OSError)
                or guard.is_expired()
                or deadline - time.monotonic() <= 0
            ):
                raise
            last = exc
            continue
    if chosen is not None:
        # Preserve the original connected-socket transport
        # profile: the frozen stdlib forward path
        # (HTTPConnection.connect) enables TCP_NODELAY after
        # the real connect, ignoring only ENOPROTOOPT and
        # propagating any other option error.  A real option
        # failure fails this connection (the exact socket is
        # closed), it does not replay the address attempt.
        try:
            chosen.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_NODELAY, 1
            )
        except OSError as exc:
            if exc.errno != errno.ENOPROTOOPT:
                with contextlib.suppress(OSError):
                    chosen.close()
                raise
        except BaseException:
            with contextlib.suppress(OSError):
                chosen.close()
            raise
        return chosen
    if last is not None:
        raise last
    raise UpstreamSetupError(
        _fixed_message(REASON_TRANSPORT), REASON_TRANSPORT
    )


def _tls_phase(
    connection: http.client.HTTPSConnection,
    sock: socket.socket,
    host: str,
    deadline: float,
    capture_timeout: float,
    guard: SetupGuard,
) -> socket.socket:
    """Actual TLS handshake under the remaining setup deadline.

    The ORIGINAL stdlib transport profile is preserved: the context
    used is the very one the owning ``HTTPSConnection`` constructed
    (``http.client._create_https_context`` at construction: platform
    default trust plus hostname check, honoring the explicit
    SSL_CERT_FILE/SSL_CERT_DIR trust references, the stdlib HTTP/1.1
    ALPN advertisement and the post-handshake-auth default) - no
    manually weakened or substituted profile, and verification is
    never disabled.  The handshake runs on the wrapped socket
    (``do_handshake_on_connect=False`` then an explicit
    ``do_handshake``) because ``wrap_socket`` returns a NEW socket
    object and detaches the pre-wrap one: the guard must adopt the
    exact object the handshake will block on.
    """
    if deadline - time.monotonic() <= 0:
        raise DeadlineExceeded
    # The exact context object the original stdlib connect() would
    # have used for this connection (set at construction; private
    # stdlib attribute, narrow typed access).
    context = cast(
        "ssl.SSLContext",
        getattr(connection, "_context"),  # noqa: B009
    )
    wrapped = context.wrap_socket(
        sock, server_hostname=host, do_handshake_on_connect=False
    )
    try:
        # The wrap is a fallible boundary that detaches the raw
        # socket: the deadline may have passed (and the guard fired)
        # while it ran.  Reject an expired phase BEFORE any new
        # blocking TLS work; the guard refuses to re-adopt after
        # expiration, so a fired guard cannot be bypassed by
        # adopting the wrapped socket (order 022-a, requirement 3).
        if not guard.adopt(wrapped):
            raise DeadlineExceeded
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise DeadlineExceeded
        wrapped.settimeout(min(capture_timeout, remaining))
        wrapped.do_handshake()
    except BaseException:
        with contextlib.suppress(Exception):
            wrapped.close()
        raise
    return wrapped


def _request_phase(
    connection: http.client.HTTPConnection,
    request_path: str,
    body: bytes,
    headers: dict[str, str],
    deadline: float,
    capture_timeout: float,
    guard: SetupGuard,
    sock: socket.socket,
) -> http.client.HTTPConnection:
    """Hand the prepared connection to the stdlib request emitter.

    The connection is pre-connected (``connection.sock`` set to the
    exact owned socket), so ``request`` performs only the request
    write - no resolver, no connect: headers and the entire body,
    through the last body byte handed to the local transport - under
    the remaining setup deadline.  Local write completion is not
    peer receipt.
    """
    try:
        connection.sock = sock
        if not guard.adopt(sock):
            raise DeadlineExceeded
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise DeadlineExceeded
        sock.settimeout(min(capture_timeout, remaining))
        connection.request("POST", request_path, body=body, headers=headers)
    except BaseException:
        # The exact owned connection (and its socket) is closed on
        # EVERY failure kind before the failure propagates; no
        # partially emitted request is ever replayed.
        with contextlib.suppress(Exception):
            connection.close()
        raise
    # Restore the owner's capture timeout for the frozen
    # header/body acquisition path before the setup clock is
    # released.
    sock.settimeout(capture_timeout)
    return connection


def open_upstream_connection(
    *,
    scheme: str,
    host: str,
    port: int,
    request_path: str,
    body: bytes,
    headers: dict[str, str],
    deadline: float,
    capture_timeout: float,
) -> http.client.HTTPConnection:
    """Prepare and emit the main upstream request under one deadline.

    ``deadline`` is the owner-anchored absolute ``time.monotonic()``
    deadline covering this entire phase (order 022-a, requirement
    2): guard startup, address resolution (owned child for named
    hosts), bounded address attempts, TCP connection, TLS handshake
    and the entire request write through the last body byte handed
    to the local transport.  No progress, short write, address
    attempt or phase change resets it; every blocking operation is
    additionally capped by the remaining deadline, and the pure
    timer guard interrupts only the exact current transport socket
    object.  A late or racing completion loses to expiration.  On
    success the guard is released (cancelled and actually joined)
    and the socket timeout restored to the owner's capture
    timeout BEFORE the returned connection is handed to response
    acquisition.  On every failure path the guard is released, the
    exact owned socket or connection is closed, and any owned child
    has already been terminated and actually reaped (order 022-a,
    requirement 3); the failure is a bounded
    :class:`UpstreamSetupError` (a main failure for the handler).
    """
    if scheme not in ("http", "https"):
        raise UpstreamSetupError(
            _fixed_message(REASON_TRANSPORT), REASON_TRANSPORT
        )
    if not math.isfinite(deadline) or deadline - time.monotonic() <= 0:
        raise UpstreamSetupError(
            _fixed_message(REASON_DEADLINE), REASON_DEADLINE
        )
    guard = SetupGuard(deadline)
    sock: socket.socket | None = None
    connection: http.client.HTTPConnection | None = None
    internal_error: Exception | None = None
    base_error: BaseException | None = None
    try:
        try:
            addresses = resolve_addresses(host, port, deadline)
            _require_deadline(deadline)
            sock = _connect_phase(
                addresses, port, deadline, capture_timeout, guard
            )
            _require_deadline(deadline)
            if scheme == "https":
                # The real stdlib connection object is created BEFORE
                # the handshake so the TLS phase reuses its exact
                # original context (trust/SNI/ALPN profile).
                connection = http.client.HTTPSConnection(
                    host, port, timeout=capture_timeout
                )
                sock = _tls_phase(
                    connection, sock, host, deadline, capture_timeout, guard
                )
            _require_deadline(deadline)
            if connection is None:
                connection = http.client.HTTPConnection(
                    host, port, timeout=capture_timeout
                )
            connection = _request_phase(
                connection, request_path, body, headers,
                deadline, capture_timeout, guard, sock,
            )
            # The request write completed: release the setup clock
            # BEFORE response acquisition.  A racing completion loses
            # to expiration.
            if guard.release():
                raise DeadlineExceeded
        except Exception as exc:  # noqa: B036 - re-raised below
            # Ordinary setup failures become the bounded main
            # failure below.
            internal_error = exc
        except BaseException as exc:  # noqa: B036 - re-raised below
            # Caller interruption (KeyboardInterrupt/SystemExit/
            # GeneratorExit), wherever it lands - inside a phase OR
            # BETWEEN phases - is remembered for propagation AFTER
            # the unconditional owned cleanup below; it is never
            # converted into an ordinary failure or a content-free
            # 502 that keeps serving.  Phase-local catches already
            # closed the phase's own objects; the finally's closes
            # are idempotent for them and cover the between-phase
            # connected socket no phase catch owns.
            base_error = exc
    finally:
        # Unconditional owned cleanup on EVERY non-successful
        # transfer (ordinary failure or caller interruption) before
        # the failure propagates or the function returns: release
        # and actually join the guard, close the exact owned
        # connection or socket.  No setup worker or open transport
        # survives the forward (order 022-a, requirement 3).
        guard.release()
        if internal_error is not None or base_error is not None:
            if connection is not None:
                with contextlib.suppress(Exception):
                    connection.close()
            elif sock is not None:
                with contextlib.suppress(OSError):
                    sock.close()
    if base_error is not None:
        raise base_error
    if internal_error is not None:
        reason = (
            REASON_DEADLINE
            if isinstance(internal_error, DeadlineExceeded)
            or time.monotonic() >= deadline
            else REASON_TRANSPORT
        )
        raise UpstreamSetupError(_fixed_message(reason), reason) from internal_error
    assert connection is not None
    return connection


def worker_main() -> int:
    """Child-side entry (``upstream_worker.py``): resolve one host.

    Reads exactly one strict versioned request frame from the
    private stdin pipe, performs at most one resolution attempt (no
    automatic retry) and writes exactly one strict versioned
    response frame to the private stdout pipe.  The child never
    logs: its stderr is silenced and its stdout carries only the
    frame, so no raw exception text, host or address can leak.
    Exit status: 0 after writing a well-formed frame (including a
    failure frame), nonzero only on a child-side contract
    violation, which the parent rejects.
    """
    try:
        prefix = _read_exact(0, _FRAME_PREFIX.size)
        (frame_len,) = _FRAME_PREFIX.unpack(prefix)
        if frame_len == 0 or frame_len > REQUEST_FRAME_MAX_BYTES:
            return 3
        host, port = decode_request_frame(_read_exact(0, frame_len))
    except (OSError, FrameMalformed, FrameIncomplete):
        return 3
    if _stdin_carries_trailing_bytes():
        return 3
    try:
        entries = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
        unique: list[tuple[int, str]] = []
        seen: set[tuple[int, str]] = set()
        for family, entry_type, _proto, _canon, sockaddr in entries:
            if entry_type != socket.SOCK_STREAM:
                continue
            if not isinstance(sockaddr, tuple):
                continue
            if not isinstance(sockaddr[0], str):
                continue
            if family == socket.AF_INET:
                pair: tuple[int, str] = (_FAMILY_INET, sockaddr[0])
            elif family == socket.AF_INET6:
                pair = (_FAMILY_INET6, sockaddr[0])
            else:
                continue
            if pair in seen:
                continue
            seen.add(pair)
            unique.append(pair)
            if len(unique) == _ADDRESS_COUNT_MAX:
                break
        if not unique:
            return _write_frame(encode_failure_frame())
        return _write_frame(encode_response_frame(addresses=unique))
    except (OSError, FrameMalformed):
        # A resolution failure is a well-formed protocol answer, not
        # a contract violation: report it and exit 0.
        return _write_frame(encode_failure_frame())


def _read_exact(fd: int, count: int) -> bytes:
    buffer = bytearray()
    while len(buffer) < count:
        chunk = os.read(fd, count - len(buffer))
        if not chunk:
            raise FrameIncomplete
        buffer.extend(chunk)
    return bytes(buffer)


def _stdin_carries_trailing_bytes() -> bool:
    """Wait for the request channel's actual EOF; a byte before
    EOF is a child-side contract violation.

    The parent closes its request writer directly after the complete
    frame, so the request channel always ends with EOF; unknown or
    delayed EOF never authorizes continuation.  The wait has no
    independent timeout: a stalled request channel is bounded by the
    parent's anchored deadline, which terminates and actually
    reaps this child on expiry (order 022-a, requirement 4).
    """
    return bool(os.read(0, 1))


def _write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    offset = 0
    while offset < len(view):
        written = os.write(fd, view[offset:])
        if written <= 0:
            raise FrameIncomplete
        offset += written


def _write_frame(frame: bytes) -> int:
    try:
        _write_all(1, frame)
    except (OSError, FrameMalformed, FrameIncomplete):
        return 3
    return 0
