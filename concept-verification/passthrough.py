"""HTTP relay helpers; repair eligibility never decides API admission."""

from __future__ import annotations

import re
from http.client import HTTPMessage
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit

MAX_REQUEST_BYTES = 256 * 2**20
HOP_HEADERS = frozenset(
    {
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "proxy-connection",
        "te",
        "trailer",
        "transfer-encoding",
        "upgrade",
    }
)


def hop_headers(headers: HTTPMessage) -> set[str]:
    return set(HOP_HEADERS) | {
        name.strip().lower()
        for value in headers.get_all("Connection", [])
        for name in value.split(",")
    }


def request_path(base: str, incoming: str) -> str:
    """Keep the caller's path/query, with an optional upstream mount prefix."""
    parsed = urlsplit(incoming)
    if parsed.scheme or parsed.netloc or not incoming.startswith("/"):
        raise ValueError("origin-form request target required")
    prefix = base.rstrip("/")
    if prefix.endswith("/v1"):
        prefix = prefix[:-3]
    return prefix + incoming


def read_request(handler: BaseHTTPRequestHandler) -> bytes:
    """Capture bounded client input, decoding only this hop's HTTP framing."""
    lengths = handler.headers.get_all("Content-Length", [])
    transfers = handler.headers.get_all("Transfer-Encoding", [])
    if len(lengths) > 1 or len(transfers) > 1 or (lengths and transfers):
        raise ValueError("ambiguous request framing")

    def exact(size: int) -> bytes:
        value = handler.rfile.read(size)
        if len(value) != size:
            raise ValueError("incomplete request body")
        return value

    if transfers:
        if transfers[0].strip().lower() != "chunked":
            raise ValueError("unsupported transfer encoding")
        chunks: list[bytes] = []
        total = 0
        while True:
            line = handler.rfile.readline(257)
            if not line.endswith(b"\r\n") or len(line) > 256:
                raise ValueError("invalid chunk framing")
            size_text = line[:-2].split(b";", 1)[0]
            if not re.fullmatch(rb"[0-9a-fA-F]+", size_text):
                raise ValueError("invalid chunk framing")
            size = int(size_text, 16)
            total += size
            if total > MAX_REQUEST_BYTES:
                raise OverflowError("request too large")
            if size == 0:
                for _ in range(100):
                    trailer = handler.rfile.readline(1025)
                    if trailer == b"\r\n":
                        return b"".join(chunks)
                    if len(trailer) > 1024 or not trailer.endswith(b"\r\n"):
                        break
                raise ValueError("invalid chunk trailers")
            chunks.append(exact(size))
            if exact(2) != b"\r\n":
                raise ValueError("invalid chunk framing")
    if not lengths:
        return b""
    if not re.fullmatch(r"[0-9]+", lengths[0]) or len(lengths[0]) > 20:
        raise ValueError("invalid content length")
    size = int(lengths[0])
    if size > MAX_REQUEST_BYTES:
        raise OverflowError("request too large")
    return exact(size)
