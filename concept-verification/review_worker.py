"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Owned
reviewer exchange worker (child-side entry).

Order 019-a, requirement 2: this is the exact repository-local
versioned worker executed by the parent through the running
interpreter (``sys.executable`` with ``-I -S -B``) - no shell, no
pickling, no arbitrary executable, no endpoint search, no model or
agent.  The child owns every potentially blocking phase of one
HTTP/HTTPS exchange (resolver, connect, TLS setup, request upload,
status/header and body reads).  It reads exactly one strict versioned
request frame from its private stdin pipe, performs at most one
attempt (no automatic retry), and writes exactly one strict versioned
response frame to its private stdout pipe.  Its socket timeout is the
parent-anchored remaining time passed through the private channel;
the authoritative total exchange deadline is enforced by the parent,
which terminates and reaps this child.  The child never logs: its
stderr is silenced and its stdout carries only the frame, so no raw
exception text, response bytes, header value or credential can leak.
Exit status: 0 after writing a well-formed frame (including a
transport-failure frame), nonzero only on a child-side contract
violation, which the parent rejects.
"""

from __future__ import annotations

import contextlib
import http.client
import os
import sys

# Isolated mode (-I) does not prepend the script directory; insert this
# worker's own repository-local directory - the exact trusted versioned
# path the parent selected, not a search - before importing the paired
# protocol module.
_WORKER_DIR = os.path.dirname(os.path.abspath(__file__))
if _WORKER_DIR not in sys.path:
    sys.path.insert(0, _WORKER_DIR)

from review_transport import (  # noqa: E402
    _FRAME_PREFIX,
    _PAYLOAD_MAX_BYTES,
    REQUEST_FRAME_MAX_BYTES,
    FrameIncomplete,
    FrameMalformed,
    decode_request_frame,
    encode_response_frame,
)


def _read_exact(fd: int, count: int) -> bytes:
    buffer = bytearray()
    while len(buffer) < count:
        chunk = os.read(fd, count - len(buffer))
        if not chunk:
            raise FrameIncomplete
        buffer.extend(chunk)
    return bytes(buffer)


def _write_all(fd: int, data: bytes) -> None:
    view = memoryview(data)
    offset = 0
    while offset < len(view):
        written = os.write(fd, view[offset:])
        if written <= 0:
            raise FrameIncomplete
        offset += written


def _stdin_carries_trailing_bytes() -> bool:
    """Wait for the request channel's actual EOF; a byte before EOF
    is a child-side contract violation.

    The parent closes its request writer directly after the complete
    frame, so the request channel always ends with EOF; unknown or
    delayed EOF never authorizes continuation.  The wait has no
    independent timeout: a stalled request channel is bounded by the
    parent's anchored deadline, which terminates and actually reaps
    this child on expiry (order 019-a, requirement 4).
    """
    return bool(os.read(0, 1))


def main() -> int:
    try:
        prefix = _read_exact(0, _FRAME_PREFIX.size)
        (frame_len,) = _FRAME_PREFIX.unpack(prefix)
        if frame_len == 0 or frame_len > REQUEST_FRAME_MAX_BYTES:
            return 3
        request = decode_request_frame(_read_exact(0, frame_len))
    except (OSError, FrameMalformed, FrameIncomplete):
        return 3
    if _stdin_carries_trailing_bytes():
        return 3
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if request.auth is not None:
        headers["Authorization"] = f"Bearer {request.auth}"
    connection_class = (
        http.client.HTTPSConnection
        if request.scheme == "https"
        else http.client.HTTPConnection
    )
    connection = connection_class(
        request.host, request.port, timeout=request.remaining_seconds
    )
    ok = False
    http_status = 0
    payload = b""
    try:
        connection.request("POST", request.path, body=request.body, headers=headers)
        result = connection.getresponse()
        # http.client mutates ``length`` to the remaining byte count as
        # read() consumes it; capture the declared value first.
        declared = result.length
        payload = result.read(_PAYLOAD_MAX_BYTES + 1)
        if (
            declared is not None
            and len(payload) < declared
            and len(payload) <= _PAYLOAD_MAX_BYTES
        ):
            # Incomplete declared delivery is a transport failure even
            # when the bytes already received parse as valid JSON and
            # regardless of how large the declaration is: a short
            # delivery can never become valid by declaring more.  A
            # payload that actually exceeds the cap keeps the existing
            # oversized-payload rejection path on the parent side.
            raise http.client.IncompleteRead(payload)
        ok = True
        http_status = result.status
    except (OSError, TimeoutError, http.client.IncompleteRead):
        ok = False
        http_status = 0
        payload = b""
    finally:
        with contextlib.suppress(Exception):
            connection.close()
    try:
        _write_all(1, encode_response_frame(ok=ok, http_status=http_status, payload=payload))
    except (OSError, FrameMalformed, FrameIncomplete):
        return 4
    return 0


if __name__ == "__main__":
    try:
        _devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(_devnull, 2)
        os.close(_devnull)
    except OSError:
        pass
    try:
        exit_code = main()
    except BaseException:
        exit_code = 3
    sys.exit(exit_code)
