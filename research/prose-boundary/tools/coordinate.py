"""008-a: coordinate contract helpers (byte <-> code point).

The hard invariant of order 008-a: for every parser range [start_byte,
end_byte), original_utf8[start_byte:end_byte) must be the exact intended
original source bytes; no range may bisect a UTF-8 code point; any mapping
into Python character coordinates must be deterministic and exactly
reversible for the span.
"""

from __future__ import annotations


def on_code_point_boundary(data: bytes, pos: int) -> bool:
    """True iff ``pos`` is a UTF-8 code point boundary in ``data``."""
    if pos < 0 or pos > len(data):
        return False
    if pos == 0 or pos == len(data):
        return True
    # A boundary is a position that does not fall in the middle of a UTF-8
    # sequence: the byte at pos must not be a continuation byte (10xxxxxx).
    return (data[pos] & 0xC0) != 0x80


def byte_to_cp(data: bytes, pos: int) -> int | None:
    """Deterministic byte -> code point mapping.

    Returns None when ``pos`` is not a code point boundary (a bisected
    position has no reversible image).  For valid boundaries this is the
    exact inverse of :func:`cp_to_byte`.
    """
    if not on_code_point_boundary(data, pos):
        return None
    return len(data[:pos].decode("utf-8"))


def cp_to_byte(text: str, cp: int) -> int:
    """Deterministic code point -> byte mapping (exact inverse of byte_to_cp)."""
    return len(text[:cp].encode("utf-8"))


def round_trip(text: str, pos: int) -> bool:
    """pos <-> cp(pos) <-> byte is exactly reversible iff pos is a boundary."""
    data = text.encode("utf-8")
    cp = byte_to_cp(data, pos)
    return cp is not None and cp_to_byte(text, cp) == pos


def check_range(data: bytes, start: int, end: int) -> list[str]:
    """Return a list of violation strings (empty = invariant holds)."""
    problems: list[str] = []
    if start < 0 or end > len(data) or start > end:
        problems.append(f"range out of bounds: {start}..{end} (len {len(data)})")
        return problems
    if not on_code_point_boundary(data, start):
        problems.append(f"start bisects a UTF-8 code point: {start}")
    if not on_code_point_boundary(data, end):
        problems.append(f"end bisects a UTF-8 code point: {end}")
    return problems


def as_byte_set(ranges: list[tuple[int, int]]) -> set[int]:
    out: set[int] = set()
    for s, e in ranges:
        out.update(range(s, e))
    return out


def merged(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge/normalize a list of half-open byte ranges."""
    if not ranges:
        return []
    ordered = sorted(ranges)
    out = [list(ordered[0])]
    for s, e in ordered[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [(s, e) for s, e in out]


def subtract(a: tuple[int, int], b: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """a minus union(b), in byte space."""
    out = [a]
    for bs, be in b:
        nxt = []
        for s, e in out:
            if be <= s or bs >= e:
                nxt.append((s, e))
                continue
            if bs > s:
                nxt.append((s, bs))
            if be < e:
                nxt.append((be, e))
        out = nxt
    return merged(out)
