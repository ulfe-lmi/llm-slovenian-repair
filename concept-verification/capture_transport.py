"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Bounded main-body capture with one elapsed body budget (order 017-a).

A single finite positive monotonic deadline is anchored at collection
entry and governs declared Content-Length, close-delimited and chunked
delivery.  Byte arrival never resets it: every blocking wait is a
``select`` bounded by the remaining time, and every read is a
non-blocking step whose cost is re-checked against the deadline.  Wire
chunk boundaries may split a UTF-8 code point, so a possibly-incomplete
trailing sequence is carried, never decoded as malformed, until the
body is known complete, where a truncated or otherwise invalid encoding
is a bounded main failure.  Raw bytes, Unicode and CRLF are preserved;
there is no ignore/replacement decoding, normalization, substring
recovery or answer regeneration.

The standard-library chunked decoder is deliberately not used for
framing: ``HTTPResponse.read1`` on a chunked body performs several
underlying blocking reads per logical read (chunk-size lines, CRLF
discards, trailer lines) that are not resumable across a timeout and
would let a slow peer outlive the body budget, and the stdlib closes
the connection file object on protocol completion, which would break
the caller's socket handling.  The framing is therefore decoded here
from wire bytes obtained through the bounded reads below.
"""

from __future__ import annotations

import io
import math
import re
import select
import socket
import ssl
import time
from collections.abc import Callable

_SSE_DELIMITERS = re.compile(r"\r\n\r\n|\n\n")
_HEX_DIGITS = re.compile(rb"[0-9a-fA-F]+")
_READ_STEP = 65536
# Finite content-free chunk-framing guards (order 017-a, requirement 2):
# they bound hostile framing so a slow peer cannot hold the stream open
# within every budget window.
_CHUNK_SIZE_LINE_MAX = 256
_TRAILER_LINE_MAX = 1024
_TRAILER_LINES_MAX = 100
# Bounded spin guard for the pathological readable-but-yields-nothing
# socket state; a real socket returns data or EOF.
_SPIN_LIMIT = 1000


class CaptureError(ValueError):
    """Bounded main-body capture failure with a content-free reason."""


def validate_budget(budget: object) -> None:
    """Reject nonnumeric, nonfinite, bool or nonpositive body budgets."""
    if (
        isinstance(budget, bool)
        or not isinstance(budget, (int, float))
        or not math.isfinite(budget)
        or budget <= 0
    ):
        raise CaptureError("capture budget must be a finite positive duration")


def utf8_split(raw: bytes) -> tuple[str, bytes]:
    """Split bytes into (strictly decodable prefix, live trailing tail).

    The tail is the possibly-incomplete UTF-8 sequence (0-3 bytes) that
    a wire chunk may have cut.  A buffer that stays invalid even with
    that tail ignored is a genuine encoding failure.
    """
    length = len(raw)
    for tail in range(0, min(3, length) + 1):
        cut = length - tail
        try:
            text = raw[:cut].decode("utf-8")
        except UnicodeDecodeError:
            continue
        tail_bytes = raw[cut:]
        if tail == 0:
            return text, b""
        lead = tail_bytes[0]
        if 0xC2 <= lead <= 0xF4:
            expected = 1 if lead < 0xE0 else 2 if lead < 0xF0 else 3
            if tail <= expected and all(
                0x80 <= byte <= 0xBF for byte in tail_bytes[1:]
            ):
                return text, tail_bytes
    raise CaptureError("upstream body is not valid UTF-8")


def utf8_require_complete(raw: bytes) -> str:
    """Strictly decode a body whose end is known; a live tail fails."""
    text, tail = utf8_split(raw)
    if tail:
        raise CaptureError("upstream body is not valid UTF-8")
    return text


def scan_complete_prefix(
    text: str, event: Callable[[str], dict[str, object] | None]
) -> bytes | None:
    """Return bytes through a delimited response.completed event, if any.

    Only fully delimited events are considered, so a marker split
    across wire chunks is never delivered prematurely.
    """
    cursor = 0
    for match in _SSE_DELIMITERS.finditer(text):
        block = text[cursor : match.start()]
        value = event(block)
        cursor = match.end()
        if value is not None and value.get("type") == "response.completed":
            return text[:cursor].encode("utf-8")
    return None


class _ChunkedFrames:
    """Bounded owned HTTP chunk-framing state machine (order 017-a).

    Feeds are raw wire bytes; ``feed`` returns the newly decoded chunk
    content.  Size-line/trailer lengths and counts are finite so a slow
    or hostile peer cannot hold the stream open within every budget
    window.
    """

    __slots__ = ("mode", "size_buf", "data_left", "crlf_state", "trailer_buf", "trailer_lines")

    def __init__(self) -> None:
        self.mode = "size"
        self.size_buf = bytearray()
        self.data_left = 0
        self.crlf_state = 0
        self.trailer_buf = bytearray()
        self.trailer_lines = 0

    def feed(self, chunk: bytes) -> bytes:
        if self.mode == "done":
            return b""
        out = bytearray()
        index = 0
        size = len(chunk)
        while index < size:
            byte = chunk[index]
            if self.mode == "size":
                self.size_buf.append(byte)
                if len(self.size_buf) > _CHUNK_SIZE_LINE_MAX:
                    raise CaptureError("upstream chunk framing is invalid")
                index += 1
                if byte == 0x0A:
                    self._begin_chunk()
            elif self.mode == "data":
                take = min(size - index, self.data_left)
                out.extend(chunk[index : index + take])
                index += take
                self.data_left -= take
                if self.data_left == 0:
                    self.mode = "crlf"
                    self.crlf_state = 0
            elif self.mode == "crlf":
                if self.crlf_state == 0:
                    if byte != 0x0D:
                        raise CaptureError("upstream chunk framing is invalid")
                    self.crlf_state = 1
                elif byte != 0x0A:
                    raise CaptureError("upstream chunk framing is invalid")
                else:
                    self.mode = "size"
                index += 1
            else:  # trailer
                self.trailer_buf.append(byte)
                if len(self.trailer_buf) > _TRAILER_LINE_MAX:
                    raise CaptureError("upstream chunk framing is invalid")
                index += 1
                if byte == 0x0A:
                    line = bytes(self.trailer_buf)
                    self.trailer_buf.clear()
                    if line in (b"\r\n", b"\n"):
                        self.mode = "done"
                    else:
                        self.trailer_lines += 1
                        if self.trailer_lines > _TRAILER_LINES_MAX:
                            raise CaptureError(
                                "upstream chunk framing is invalid"
                            )
        return bytes(out)

    def _begin_chunk(self) -> None:
        line = bytes(self.size_buf)
        self.size_buf.clear()
        if line.endswith(b"\r\n"):
            line = line[:-2]
        elif line.endswith(b"\n"):
            line = line[:-1]
        else:
            raise CaptureError("upstream chunk framing is invalid")
        head, _, _extension = line.partition(b";")
        if not _HEX_DIGITS.fullmatch(head):
            raise CaptureError("upstream chunk framing is invalid")
        self.data_left = int(head, 16)
        self.mode = "trailer" if self.data_left == 0 else "data"

    def require_complete(self) -> None:
        if self.mode != "done":
            raise CaptureError("upstream chunk framing is invalid")


def read_bounded_body(
    response: object,
    maximum: int,
    budget: float,
    *,
    require_complete_sse: bool = False,
    event: Callable[[str], dict[str, object] | None] | None = None,
) -> bytes:
    """Read one main response body under one elapsed budget and a bound.

    Declared Content-Length bodies must deliver exactly the declared
    bytes: early EOF is a failure and undelivered over-read bytes are
    ignored (the connection is request-scoped and closed by the caller).
    Close-delimited bodies run to EOF.  Chunked bodies are decoded by
    the bounded framing state machine and end at the terminating zero
    chunk; bytes after it (keep-alive) are not consumed.  For complete
    SSE, a delimited ``response.completed`` event terminates collection
    early even while the HTTP/1.1 connection stays open; bytes after the
    terminal marker are not consumed.  The budget is anchored at
    collection entry and every blocking wait is bounded by the remaining
    time; byte arrival never resets it.
    """
    validate_budget(budget)
    deadline = time.monotonic() + budget
    if maximum <= 0:
        raise CaptureError("upstream response exceeds capture bound")
    if require_complete_sse and event is None:
        raise CaptureError("upstream SSE event boundary is unavailable")
    fp = getattr(response, "fp", None)
    if not isinstance(fp, io.BufferedReader):
        raise CaptureError("upstream socket boundary is unavailable")
    raw_io = fp.raw
    raw_socket = getattr(raw_io, "_sock", None)
    if not isinstance(raw_socket, socket.socket):
        raise CaptureError("upstream socket boundary is unavailable")

    length = getattr(response, "length", None)
    if length is not None and length > maximum:
        raise CaptureError("upstream response exceeds capture bound")
    frames = _ChunkedFrames() if getattr(response, "chunked", False) else None

    chunks: list[bytes] = []
    total = 0
    spins = 0
    previous_timeout = raw_socket.gettimeout()

    def remaining() -> float:
        return deadline - time.monotonic()

    def check_deadline() -> None:
        if remaining() <= 0:
            raise CaptureError("upstream capture timeout")

    def accept(wire: bytes) -> bytes | None:
        """Fold one wire step into the body; return an early prefix."""
        nonlocal total
        if frames is not None:
            piece = frames.feed(wire)
        elif length is not None:
            piece = wire[: length - total] if total < length else b""
        else:
            piece = wire
        if piece:
            total += len(piece)
            if total > maximum:
                raise CaptureError("upstream response exceeds capture bound")
            chunks.append(piece)
            # Only unknown-length delivery may terminate at the terminal
            # marker (keep-alive without EOF): a declared Content-Length
            # body must deliver every advertised byte before completion
            # is validated (order 017-a, requirements 4 and 5).
            if require_complete_sse and length is None:
                text, _tail = utf8_split(b"".join(chunks))
                return scan_complete_prefix(text, event)  # type: ignore[arg-type]
        return None

    def try_read(limit: int) -> bytes | None:
        """One bounded readiness step; None means not ready yet.

        Step 1 drains over-read buffer bytes (raw wire bytes; a
        buffered hit never touches the wire, and the stdlib chunk
        decoder and its connection-closing read paths are never
        entered).  The non-consuming peek gates the read: with an
        empty buffer read1 would swallow a nonblocking EAGAIN as b"",
        indistinguishable from EOF, so a read happens only when
        buffered bytes are known to exist.  Step 2 is an optimistic
        non-blocking wire read: it also sees data buffered inside the
        TLS layer, which the OS select on the socket cannot.  A
        nonblocking TLS readiness error (SSLWantReadError) is
        not-ready, never EOF.  b"" is only returned by a read that
        reached the wire: clean EOF.
        """
        try:
            if fp.peek(1):
                return fp.read1(limit)
        except (BlockingIOError, InterruptedError, ssl.SSLWantReadError):
            pass
        try:
            return raw_socket.recv(_READ_STEP)
        except (BlockingIOError, InterruptedError, ssl.SSLWantReadError):
            return None

    try:
        while True:
            check_deadline()
            if length is not None and total >= length:
                break
            if frames is not None and frames.mode == "done":
                break
            if length is not None:
                limit = min(_READ_STEP, length - total)
            elif frames is None:
                limit = min(_READ_STEP, maximum - total + 1)
            else:
                limit = _READ_STEP
            raw_socket.settimeout(0.0)
            wire = try_read(limit)
            if wire is not None:
                if wire:
                    spins = 0
                    early = accept(wire)
                    if early is not None:
                        return early
                    continue
                # A read that reached the wire returned b"": clean EOF.
                if length is not None and total < length:
                    raise CaptureError(
                        "upstream body ended before declared length"
                    )
                if frames is not None:
                    frames.require_complete()
                if require_complete_sse:
                    text = utf8_require_complete(b"".join(chunks))
                    if scan_complete_prefix(text, event) is None:  # type: ignore[arg-type]
                        raise CaptureError("upstream SSE is incomplete")
                return b"".join(chunks)
            # Nothing buffered and nothing on the wire: wait under the
            # remaining budget (a slow peer that keeps dribbling bytes
            # cannot reset or outlive the anchored deadline).
            ready, _, _ = select.select(
                [raw_socket], [], [], max(remaining(), 0.0)
            )
            if not ready:
                raise CaptureError("upstream capture timeout")
            spins += 1
            if spins > _SPIN_LIMIT:
                raise CaptureError("upstream socket boundary is unavailable")
        # Body complete by framing (declared length reached or chunked
        # terminating zero chunk): the end is known, so the encoding is
        # strict and a complete SSE requires the terminal event.
        if require_complete_sse:
            text = utf8_require_complete(b"".join(chunks))
            if scan_complete_prefix(text, event) is None:  # type: ignore[arg-type]
                raise CaptureError("upstream SSE is incomplete")
        return b"".join(chunks)
    finally:
        raw_socket.settimeout(previous_timeout)
