"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Proxy."""

from __future__ import annotations

import contextlib
import http.client
import json
import math
import os
import re
import socket
import sys
import tempfile
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Protocol, TypedDict, cast
from urllib.parse import urlparse

import analysis_policy
import capture_transport
import client_transport
import delivery_transport
import header_transport
import request_admission
import upstream_setup
from batch_review import (
    BOUND_REVIEW_REASONS,
    REASON_FAILED,
    REASON_PREP_INVALID,
    REASON_PROMPT_OVERSIZE,
    REASON_REQUEST_OVERSIZE,
    BatchProposal,
    BatchResult,
    BatchTarget,
    BatchUsage,
    build_prompt,
    prepare_targets,
)
from config import (
    CLIENT_DELIVERY_TIMEOUT_SECONDS,
    CLIENT_REQUEST_TIMEOUT_SECONDS,
    MAIN_BODY_MAX_BYTES,
    MAIN_HEADER_TIMEOUT_SECONDS,
    MAIN_SETUP_TIMEOUT_SECONDS,
    REVIEWER_HTTP_TIMEOUT_SECONDS,
    canonical_bytes,
)
from detector import Candidate, detect, tokenize
from evidence_budget import validate_default_evidence_policy
from pandoc_protection import (
    PandocSpec,
    PandocStartupError,
    check_pandoc,
    compose_protection,
    protect_with_pandoc,
    resolve_pandoc_spec,
)
from qwen_client import Proposal, ResponsesReviewer, responses_path
from repair import accept, apply_edits
from responses_contract import (
    RequestContractError,
    aligned_metadata_clean,
    validate_completed_envelope,
    validate_request,
)
from runtime_corpus import RuntimeCorpus, RuntimeCorpusError

# Native accepted-object class captured at import time.  BaseServer
# types the accepted request as the TCP/UDP union; this TCP
# HTTPServer accept boundary always yields the socket member, and
# the captured reference keeps that narrowing sound for the whole
# process even when a frozen native supervised-test child script
# legitimately reassigns the mutable socket.socket module attribute
# while the accept loop is running (order 026-a, requirements 2
# and 3).  It is not a new protocol behavior and adds no UDP
# support or claim.
_SOCKET_CLASS = socket.socket


class ProxyError(ValueError):
    pass


class Reviewer(Protocol):
    """Structural reviewer interface: the engine only calls ``review_batch``.

    The runtime RepairEngine never falls back to single-target calls; the
    historical single-target prompt/API stays in ``qwen_client`` and the
    frozen evaluator for research use only (order 014-a, requirement 1).
    """

    def review_batch(
        self, sentence: str, targets: tuple[BatchTarget, ...]
    ) -> BatchResult: ...


def _split_sse(raw: bytes) -> list[tuple[str, str]]:
    text = raw.decode("utf-8")
    result: list[tuple[str, str]] = []
    cursor = 0
    for match in re.finditer(r"\r\n\r\n|\n\n", text):
        result.append((text[cursor : match.start()], match.group(0)))
        cursor = match.end()
    if cursor < len(text):
        result.append((text[cursor:], ""))
    return result


def _strict_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            # Ambiguous duplicate keys never reach repair or rendering.
            raise ProxyError("upstream event contains duplicate keys")
        value[key] = item
    return value


def _strict_constant(_name: str) -> object:
    raise ProxyError("upstream event contains a nonfinite number")


def _strict_float(text: str) -> float:
    number = float(text)
    if not math.isfinite(number):
        raise ProxyError("upstream event contains a nonfinite number")
    return number


def _strict_json_object(raw: str) -> dict[str, object]:
    try:
        value = json.loads(
            raw,
            object_pairs_hook=_strict_pairs,
            parse_constant=_strict_constant,
            parse_float=_strict_float,
        )
    except ProxyError:
        raise
    except json.JSONDecodeError as exc:
        raise ProxyError("upstream event is not valid JSON") from exc
    if not isinstance(value, dict):
        raise ProxyError("upstream event is not an object")
    return value


def _event(block: str) -> dict[str, object] | None:
    data_lines = [line[5:] for line in block.splitlines() if line.startswith("data:")]
    if not data_lines or "".join(data_lines).strip() == "[DONE]":
        return None
    return _strict_json_object("\n".join(data_lines))


def _events(raw: bytes) -> list[tuple[str, dict[str, object]]]:
    result: list[tuple[str, dict[str, object]]] = []
    for block, _delimiter in _split_sse(raw):
        value = _event(block)
        if value is not None:
            result.append((block, value))
    return result


def _bounded_read(
    response: http.client.HTTPResponse,
    maximum: int,
    timeout: float,
    *,
    require_complete_sse: bool = False,
) -> bytes:
    """Read within byte/time limits, stopping at a complete SSE event.

    One finite positive monotonic body deadline is anchored at
    collection entry and governs declared Content-Length, close-delimited
    and chunked delivery (order 017-a): byte arrival never resets it and
    every blocking wait is bounded by the remaining time.  A wire chunk
    may end inside a UTF-8 code point: the live tail is carried until
    the body is known complete, where a truncated or invalid encoding is
    a bounded main failure.  Readiness spans two layers: header parsing
    (``getresponse``) may already have over-read body bytes into the
    buffered reader, which the collector drains first (never entering
    the stdlib chunk decoder or its connection-closing read paths), so a
    fully delimited terminal event already in the buffer terminates the
    read without EOF even while the HTTP/1.1 connection stays open.
    """
    try:
        return capture_transport.read_bounded_body(
            response,
            maximum,
            timeout,
            require_complete_sse=require_complete_sse,
            event=_event,
        )
    except capture_transport.CaptureError as exc:
        raise ProxyError(str(exc)) from exc


def _render_event(block: str, value: dict[str, object]) -> str:
    lines = block.splitlines()
    data_index = next((index for index, line in enumerate(lines) if line.startswith("data:")), None)
    if data_index is None:
        return block
    lines[data_index] = "data: " + json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    lines = [
        line
        for index, line in enumerate(lines)
        if index == data_index or not line.startswith("data:")
    ]
    return "\n".join(lines)


# Sentinel for a stream-event ownership position that is absent (distinct
# from a declared null, which is inconsistent and abstains).
_UNSET: object = object()


def transform_sse(raw: bytes, repair: Callable[[str], str]) -> tuple[bytes, bool]:
    """Repair one unambiguously identified assistant text answer only.

    Ownership is prefetched across the whole completed upstream SSE before
    any repair call: the delta layer (stream item ids and the positions the
    stream events themselves declare) and every terminal representation
    that carries the answer (``output_text.done`` events, ``content_part.done``
    output_text parts, message-typed ``output_item.done`` items, and the
    ``output_text`` part in the completed ``response.output``).  Several
    assistant text answers/items/content parts, a completed envelope that
    does not exactly confirm the single delta answer, stream-declared
    indices that contradict the completed list positions, a terminal copy
    that cannot be proved consistent (different text, role, status,
    identity, index, content cardinality/kinds, a duplicated terminal
    representation, or a missing/null/non-string id), or otherwise
    ambiguous target ownership bypass repair unchanged with zero review
    calls (order 014-a requirement 8; order 014-b requirements 2-4).

    The editable fields are collected as explicit event references during
    the preflight, and the renderer mutates only those: it never iterates
    the output_text nodes of a matching-id object after repair, never
    recurses into metadata, and never matches substrings or identical
    values (no ID coercion, no value-based recovery).  Every
    ``output_text.delta`` payload must be a string (an empty string is a
    valid no-op): a delta event whose payload is missing or non-string is
    a malformed answer event and abstains raw unchanged with zero calls.
    Initial ``added`` events are supported only as empty placeholders:
    their ownership (typed confirmed id) and, for message items, the
    assistant role are validated, their protected content is never
    rewritten, and any non-empty initial content - which cannot be proved
    safe - abstains raw unchanged with zero calls.  The confirming
    completed event must be an explicitly completed, error-free Responses
    object and the final message must carry exactly
    ``status == "completed"``; non-empty (or non-list) aligned
    annotations/logprobs on any answer-bearing representation make the
    whole stream ineligible before dispatch (order 015-a, requirements 4
    and 5).  When the review accepts no text edit the raw bytes are
    returned unchanged (order 014-a requirement 7).
    """
    blocks = _split_sse(raw)
    parsed: list[dict[str, object] | None] = [_event(block) for block, _ in blocks]
    streams: dict[str, list[str]] = {}
    # Positions declared by the stream events themselves: text delta/done
    # events and content-part added/done events carry ``item_id`` plus
    # ``output_index``/``content_index`` in the documented Responses
    # stream.  Those declared positions are authoritative for ownership;
    # optional indices on the final message/part are only an additional
    # consistency constraint, never a substitute.
    declared: dict[str, list[tuple[object, object]]] = {}
    # A delta/done event whose ``item_id`` is missing, non-string or empty
    # does not identify an answer, and an answer-shaped content part or
    # message item without a typed nonempty id is an unowned terminal copy.
    # Such a stream carries ambiguous ownership and abstains instead of
    # being coerced to an invented id.
    ownership_invalid = False
    # Every answer-related stream event (text delta/done, output-text
    # content-part added/done, message-typed output-item added/done) must
    # belong to the single confirmed answer; any other id abstains.
    answer_event_ids: set[str] = set()
    for value in parsed:
        if value is None:
            continue
        event_type = value.get("type")
        if event_type in (
            "response.output_text.delta",
            "response.output_text.done",
            "response.content_part.added",
            "response.content_part.done",
        ):
            stream_id = value.get("item_id")
            if type(stream_id) is not str or not stream_id:
                if event_type in ("response.output_text.delta", "response.output_text.done"):
                    ownership_invalid = True
                elif (
                    isinstance((stream_part := value.get("part")), dict)
                    and stream_part.get("type") == "output_text"
                ):
                    # An answer-shaped content part that cannot identify
                    # its owner is an unowned terminal copy.
                    ownership_invalid = True
                continue
            part = value.get("part")
            answer_part = (
                event_type.startswith("response.content_part.")
                and isinstance(part, dict)
                and part.get("type") == "output_text"
            )
            if event_type.startswith("response.output_text.") or answer_part:
                answer_event_ids.add(stream_id)
            if "output_index" in value or "content_index" in value:
                declared.setdefault(stream_id, []).append(
                    (value.get("output_index", _UNSET), value.get("content_index", _UNSET))
                )
        elif event_type in ("response.output_item.added", "response.output_item.done"):
            item_obj = value.get("item")
            if isinstance(item_obj, dict):
                obj_id = item_obj.get("id")
                if item_obj.get("type") == "message":
                    if type(obj_id) is not str or not obj_id:
                        # An answer-shaped message item without a typed id
                        # is an unowned terminal representation.
                        ownership_invalid = True
                        continue
                    answer_event_ids.add(obj_id)
                if type(obj_id) is str and obj_id and "output_index" in value:
                    declared.setdefault(obj_id, []).append((value["output_index"], _UNSET))
        if event_type == "response.output_text.delta":
            delta = value.get("delta")
            if type(delta) is not str:
                # A delta event whose payload is missing or non-string is a
                # malformed answer event: the stream carries ambiguous
                # content and abstains instead of being partially collected.
                ownership_invalid = True
                continue
            stream_id = value.get("item_id")
            if type(stream_id) is str and stream_id:
                streams.setdefault(stream_id, []).append(delta)
    if ownership_invalid:
        # Answer-related events with missing, non-string or empty ids (or
        # unowned answer-shaped terminal copies) carry ambiguous ownership:
        # bypass unchanged with zero review calls.
        return raw, False
    # Completed-envelope answer units: every output_text part of any message
    # item in any response.output, with list ownership positions.
    # Output messages are identified by ``id`` (delta/done events carry
    # ``item_id``); ``output_index``/``content_index`` are optional but must
    # be consistent when present.
    units: list[tuple[int, int, dict[str, object], int, dict[str, object]]] = []
    # The completed event that owns a confirming unit must itself be an
    # explicitly completed, error-free Responses object; a missing/null
    # status or a non-null error never confirms an answer (order 015-a,
    # requirements 4 and 5).
    completed_eligible: dict[int, bool] = {}
    for index, value in enumerate(parsed):
        if value is None or value.get("type") != "response.completed":
            continue
        response = value.get("response")
        if not isinstance(response, dict):
            completed_eligible[index] = False
            continue
        # The completed layer must match the shared JSON profile exactly
        # (order 015-a, requirements 4 and 5): the full envelope
        # validation - completed object, absent/null error, stateless
        # declarations, at most one bounded reasoning item preceding
        # exactly one completed assistant message with a typed nonempty
        # id and exactly one plain output_text part - decides both
        # eligibility and the single confirming unit.  Earlier stream
        # bookkeeping, terminal copy checks and rendering are unchanged.
        found = validate_completed_envelope(response)
        completed_eligible[index] = found is not None
        if found is None:
            continue
        _answer_text, part = found
        final_output = response.get("output")
        if not isinstance(final_output, list):
            continue
        for output_pos, item in enumerate(final_output):
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for content_pos, candidate in enumerate(content):
                # The validator returns a reference into this same
                # response; identity locates the exact unit.
                if candidate is part:
                    units.append((index, output_pos, item, content_pos, part))

    def ownership_consistent(
        output_pos: int, item: dict[str, object], content_pos: int, part: dict[str, object]
    ) -> bool:
        declared_output = item.get("output_index")
        output_ok = declared_output is None or (
            type(declared_output) is int and declared_output == output_pos
        )
        declared_content = part.get("content_index")
        content_ok = declared_content is None or (
            type(declared_content) is int and declared_content == content_pos
        )
        return output_ok and content_ok

    def stream_positions_consistent(
        item_id: str, output_pos: int, content_pos: int
    ) -> bool:
        # Every stream event for this item that declares an ownership
        # position must declare it as an integer matching the actual final
        # list position; a null or contradictory declaration abstains.
        for declared_output, declared_content in declared.get(item_id, ()):
            if declared_output is not _UNSET and (
                type(declared_output) is not int or declared_output != output_pos
            ):
                return False
            if declared_content is not _UNSET and (
                type(declared_content) is not int or declared_content != content_pos
            ):
                return False
        return True

    non_empty = [item_id for item_id, parts in streams.items() if "".join(parts)]
    unit_index: int
    unit_item: dict[str, object]
    unit_part: dict[str, object]
    confirmed_id: str
    original_text: str
    if non_empty:
        if len(non_empty) != 1:
            # Several assistant text answers: ambiguous ownership.
            return raw, False
        item_id = non_empty[0]
        if not answer_event_ids <= {item_id}:
            # An answer event for another id: ambiguous ownership.
            return raw, False
        joined = "".join(streams[item_id])
        # Exactly one confirming final assistant output_text with consistent
        # ownership is required before any repair call: the final message id
        # equals the stream item id, the text matches, and every position
        # declared by the stream events equals the actual final list
        # positions.  An unconfirmed completed answer (absent or several
        # units, wrong id, inconsistent indices, or mismatched text)
        # bypasses unchanged with zero calls.
        if len(units) != 1:
            return raw, False
        unit_index, output_pos, unit_item, content_pos, unit_part = units[0]
        message_id = unit_item.get("id")
        confirmed = (
            ownership_consistent(output_pos, unit_item, content_pos, unit_part)
            and stream_positions_consistent(item_id, output_pos, content_pos)
            and unit_item.get("role") == "assistant"
            and unit_item.get("status") == "completed"
            and type(message_id) is str
            and message_id == item_id
            and unit_part["text"] == joined
        )
        if not confirmed:
            return raw, False
        confirmed_id = item_id
        original_text = joined
    else:
        assistant_units = [
            unit for unit in units if unit[2].get("role") == "assistant"
        ]
        if len(assistant_units) != 1 or len(units) != 1:
            # No unambiguous single assistant answer (several answers,
            # several content parts, or non-answer content): bypass.
            return raw, False
        unit_index, output_pos, unit_item, content_pos, unit_part = assistant_units[0]
        message_id = unit_item.get("id")
        if (
            type(message_id) is not str
            or not message_id
            or unit_item.get("status") != "completed"
            or not ownership_consistent(output_pos, unit_item, content_pos, unit_part)
            or not stream_positions_consistent(message_id, output_pos, content_pos)
            or not answer_event_ids <= {message_id}
        ):
            # Absent or inconsistent ownership: bypass unchanged.
            return raw, False
        confirmed_id = message_id
        original_text = str(unit_part["text"])

    if not completed_eligible.get(unit_index, False):
        # The completed envelope confirming the single answer is not an
        # explicitly completed, error-free Responses object: bypass
        # unchanged with zero review calls.
        return raw, False
    if not aligned_metadata_clean(unit_part):
        # Non-empty (or non-list) aligned metadata on the final answer
        # part cannot be kept valid beside a changed answer: bypass
        # unchanged with zero review calls.
        return raw, False

    # Order 014-b requirement 2/3: before any reviewer side effect, every
    # answer-bearing terminal representation must be proved consistent with
    # the one final assistant answer (same exact typed id, same final
    # positions, expected part kind / item role / status / content
    # cardinality and kinds, and the exact original answer text).  Any copy
    # that cannot be proved consistent makes the whole SSE ineligible:
    # return the raw original with zero calls, never keep one edited
    # representation beside an incompatible original copy.  The validated
    # editable fields are collected here, as explicit event references, and
    # are the only ones the renderer below may mutate.
    final_content = unit_item["content"]
    if not isinstance(final_content, list):
        # Units are only collected from a list content above; this keeps the
        # preflight's typed boundary explicit.
        return raw, False
    final_kinds = [
        part.get("type") if isinstance(part, dict) else None for part in final_content
    ]
    # event index -> ("part" | "item" | "done", content position)
    editable: dict[int, tuple[str, int | None]] = {}
    delta_indices: set[int] = set()
    copy_counts = {"output_text.done": 0, "content_part.done": 0, "output_item.done": 0}
    for index, value in enumerate(parsed):
        if value is None or index == unit_index:
            continue
        event_type = value.get("type")
        stream_id = value.get("item_id")
        if event_type == "response.output_text.delta":
            if type(stream_id) is str and stream_id == confirmed_id:
                if not aligned_metadata_clean(value):
                    # A token/offset aligned list on a delta of the
                    # confirmed answer becomes stale beside a changed
                    # answer: the whole stream abstains.
                    return raw, False
                delta_indices.add(index)
        elif event_type == "response.content_part.added":
            part = value.get("part")
            if not (isinstance(part, dict) and part.get("type") == "output_text"):
                # Non-answer part: recognized bookkeeping, never touched.
                continue
            # An initial added part is a supported empty placeholder only:
            # its ownership is validated here, its protected content is
            # never rewritten, and non-empty initial content cannot be
            # proved safe, so it abstains raw unchanged with zero calls.
            if type(stream_id) is not str or stream_id != confirmed_id:
                return raw, False
            if "text" in part and part["text"] != "":
                return raw, False
            if not aligned_metadata_clean(part):
                return raw, False
        elif event_type == "response.output_item.added":
            item_obj = value.get("item")
            if not (isinstance(item_obj, dict) and item_obj.get("type") == "message"):
                # Non-message item: recognized non-answer bookkeeping.
                continue
            obj_id = item_obj.get("id")
            if type(obj_id) is not str or obj_id != confirmed_id:
                return raw, False
            # The initial representation of the answer item must agree on
            # identity and role and carry supported empty placeholders only.
            if item_obj.get("role") != "assistant":
                return raw, False
            content = item_obj.get("content")
            if content is not None:
                if not isinstance(content, list):
                    return raw, False
                for part in content:
                    if not isinstance(part, dict) or (
                        "text" in part and part["text"] != ""
                    ):
                        return raw, False
                    if not aligned_metadata_clean(part):
                        return raw, False
        elif event_type == "response.output_text.done":
            if type(stream_id) is not str or stream_id != confirmed_id:
                continue
            copy_counts["output_text.done"] += 1
            if value.get("text") != original_text:
                # A terminal done event must carry the exact original
                # answer text; a missing or different text cannot be
                # proved consistent.
                return raw, False
            if not aligned_metadata_clean(value):
                # Stale token/offset alignment on a terminal copy of the
                # confirmed answer makes the whole stream ineligible.
                return raw, False
            editable[index] = ("done", None)
        elif event_type == "response.content_part.done":
            part = value.get("part")
            if not (isinstance(part, dict) and part.get("type") == "output_text"):
                # Non-answer part: recognized bookkeeping, never touched.
                continue
            # A different valid id already failed the membership check
            # above; a missing or non-string id returned earlier.  Kept as
            # an explicit defense of the ownership rule.
            if type(stream_id) is not str or stream_id != confirmed_id:
                return raw, False
            copy_counts["content_part.done"] += 1
            if part.get("text") != original_text:
                return raw, False
            if not aligned_metadata_clean(part):
                return raw, False
            editable[index] = ("part", None)
        elif event_type == "response.output_item.done":
            item_obj = value.get("item")
            if not (isinstance(item_obj, dict) and item_obj.get("type") == "message"):
                # Non-message item (e.g. reasoning or tool bookkeeping):
                # recognized non-answer bookkeeping, never touched.
                continue
            obj_id = item_obj.get("id")
            if type(obj_id) is not str or obj_id != confirmed_id:
                return raw, False
            copy_counts["output_item.done"] += 1
            if item_obj.get("role") != "assistant":
                return raw, False
            if "status" in item_obj and item_obj.get("status") != "completed":
                return raw, False
            content = item_obj.get("content")
            if not isinstance(content, list) or len(content) != len(final_content):
                return raw, False
            for part_pos, part in enumerate(content):
                if not isinstance(part, dict) or part.get("type") != final_kinds[part_pos]:
                    return raw, False
            if content[content_pos].get("text") != original_text:
                return raw, False
            if not aligned_metadata_clean(content[content_pos]):
                return raw, False
            editable[index] = ("item", content_pos)
    if any(count > 1 for count in copy_counts.values()):
        # Duplicated terminal representations of the one answer are
        # ambiguous: bypass unchanged with zero calls.
        return raw, False

    new_text = repair(original_text)
    if new_text == original_text:
        # No accepted text edit: the raw bytes are returned unchanged.
        return raw, False

    # The validated final unit (a shared reference into the parsed events)
    # carries the repaired text; the render pass re-emits exactly the
    # collected editable references plus the confirmed delta events.
    unit_part["text"] = new_text
    output: list[str] = []
    delta_done = False
    for (block, delimiter), value, index in zip(blocks, parsed, range(len(blocks)), strict=True):
        if value is None:
            output.append(block + delimiter)
            continue
        re_render = index == unit_index
        kind = editable.get(index)
        if kind is not None:
            kind_name, copy_pos = kind
            if kind_name == "done":
                value["text"] = new_text
                re_render = True
            elif kind_name == "part":
                part = value.get("part")
                if isinstance(part, dict):
                    part["text"] = new_text
                    re_render = True
            else:
                item_obj = value.get("item")
                if isinstance(item_obj, dict) and type(copy_pos) is int:
                    content = item_obj.get("content")
                    if isinstance(content, list):
                        part = content[copy_pos]
                        if isinstance(part, dict):
                            part["text"] = new_text
                            re_render = True
        elif index in delta_indices:
            # The first non-empty delta of the confirmed answer carries the
            # full repaired text; every later delta is emptied so the answer
            # is not duplicated.  Only the explicitly validated confirmed id
            # is ever mutated; only genuine string payloads are touched and
            # empty text events stay untouched.
            delta = value.get("delta")
            if type(delta) is str and delta:
                value["delta"] = new_text if not delta_done else ""
                delta_done = True
                re_render = True
        if re_render:
            block = _render_event(block, value)
        output.append(block + delimiter)
    return "".join(output).encode("utf-8"), True


def _strict_json_body(raw: bytes) -> dict[str, object]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ProxyError("upstream JSON body is not valid UTF-8") from exc
    return _strict_json_object(text)


def transform_json(raw: bytes, repair: Callable[[str], str]) -> tuple[bytes, bool]:
    """Repair one completed JSON text answer with the same eligibility.

    Nonstreaming JSON is the primary supported path (order 015-a,
    requirement 4).  Malformed main JSON (invalid UTF-8, duplicate keys,
    nonfinite numbers, non-object) is a main error: it raises
    ``ProxyError`` and never reaches repair.  A well-formed envelope that
    is unsupported, or explicitly incomplete or error-bearing, passes
    through byte-identical with zero review calls, retaining its original
    status/finish/error semantics; no successful repair trace is recorded
    for it.  Only the exact validated answer part is mutated; unrelated
    values, IDs, usage and protected reasoning are preserved.
    """
    envelope = _strict_json_body(raw)
    found = validate_completed_envelope(envelope)
    if found is None:
        return raw, False
    original_text, part = found
    new_text = repair(original_text)
    if new_text == original_text:
        # No accepted text edit: the captured body is returned exactly.
        return raw, False
    part["text"] = new_text
    return (
        json.dumps(envelope, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        True,
    )


@dataclass(frozen=True)
class Forwarded:
    status: int
    body: bytes
    content_type: str


@dataclass(frozen=True)
class _PreparedCandidate:
    """A detector candidate with its validated neighbor context, in the
    deterministic original order used for batch target alignment."""

    candidate: Candidate
    left: str | None
    right: str | None
    left_bounds: tuple[int, int] | None
    right_bounds: tuple[int, int] | None


@dataclass
class RepairEngine:
    index: Path
    reviewer: Reviewer
    mode: str = "local-context"
    # Resolved qualified-Pandoc spec; None resolves lazily at repair time
    # (the proxy main path resolves and checks it at startup).
    pandoc: PandocSpec | None = None
    _details: list[dict[str, object]] | None = None
    # Actual reviewer usage for the in-flight request only; reset on every
    # request so no earlier usage is ever carried over (order 015-a,
    # requirement 7).
    _review_usage: BatchUsage | None = None

    def begin_request(self) -> None:
        self._details = []
        self._review_usage = None

    def take_details(self) -> list[dict[str, object]]:
        details = self._details or []
        self._details = None
        return details

    def _fail_closed_original(
        self, text: str, raw_started: float, reason: str | None, detail: str
    ) -> str:
        """Record a minimal trace and return the exact completed original.

        A global parse/mapping failure must short-circuit before Corpus
        access, detection and any reviewer call (order 013-a, requirement
        12).  No corpus is opened and no reviewer is invoked.
        """
        if self._details is not None:
            self._details.append(
                {
                    "original": text,
                    "repaired": text,
                    "candidates": [],
                    "corpus_summaries": [],
                    "reviewer_decisions": [],
                    "acceptance": [],
                    "replacements": [],
                    "timings": {
                        "raw_seconds": 0.0,
                        "detector_seconds": 0.0,
                        "reviewer_seconds": 0.0,
                        "repair_seconds": round(time.monotonic() - raw_started, 6),
                    },
                    "protected_difference_count": 0,
                    "review_batch": {
                        "calls": 0,
                        "targets": 0,
                        "outcome": "skipped",
                        "reason": None,
                        # No reviewer response exists on this path: usage
                        # is explicitly unknown, never reused from an
                        # earlier request.
                        "usage": "unknown",
                    },
                    "protection_failure": {
                        "reason": reason or "PANDOC_PROTECTION",
                        "detail": detail[:256],
                    },
                }
            )
        return text

    def _fail_closed_evidence(
        self, text: str, raw_started: float, reason: str, stage: str
    ) -> str:
        """Return the exact completed original after a technical evidence failure.

        An early failure (index open or detection) short-circuits before any
        reviewer call: zero edits and zero review calls are recorded.  A
        late failure is recorded on the normal detail by the caller (stage
        ``late``) with the actual review attempt and known/unknown usage
        preserved.  The fixed content-free label reflects no SQL, path,
        value, target or credential text, and an evidence failure is never
        reported as a Pandoc failure (order 016-a, requirement 4).
        """
        if self._details is not None:
            self._details.append(
                {
                    "original": text,
                    "repaired": text,
                    "candidates": [],
                    "corpus_summaries": [],
                    "reviewer_decisions": [],
                    "acceptance": [],
                    "replacements": [],
                    "timings": {
                        "raw_seconds": 0.0,
                        "detector_seconds": 0.0,
                        "reviewer_seconds": 0.0,
                        "repair_seconds": round(time.monotonic() - raw_started, 6),
                    },
                    "protected_difference_count": 0,
                    "review_batch": {
                        "calls": 0,
                        "targets": 0,
                        "outcome": "skipped",
                        "reason": None,
                        # No reviewer response exists on this path: usage
                        # is explicitly unknown, never reused from an
                        # earlier request.
                        "usage": "unknown",
                    },
                    "evidence_failure": {"reason": reason, "stage": stage},
                }
            )
        return text

    def _fail_closed_analysis(
        self, text: str, raw_started: float, reason: str
    ) -> str:
        """Record a minimal trace and return the exact completed original.

        An ineligible completed answer bypasses the OPTIONAL analysis
        pass BEFORE Pandoc, Corpus, detection and any reviewer call
        (order 025-a, requirement 3): zero analysis, evidence,
        protection and review work is performed, and nothing is
        truncated, split, sampled or partially repaired.  The fixed
        content-free ``analysis_bypass`` reason is separate from the
        protection and evidence failure labels, which this path never
        sets, and no client-visible diagnostic text or logging is
        added.
        """
        if self._details is not None:
            self._details.append(
                {
                    "original": text,
                    "repaired": text,
                    "candidates": [],
                    "corpus_summaries": [],
                    "reviewer_decisions": [],
                    "acceptance": [],
                    "replacements": [],
                    "timings": {
                        "raw_seconds": 0.0,
                        "detector_seconds": 0.0,
                        "reviewer_seconds": 0.0,
                        "repair_seconds": round(time.monotonic() - raw_started, 6),
                    },
                    "protected_difference_count": 0,
                    "review_batch": {
                        "calls": 0,
                        "targets": 0,
                        "outcome": "skipped",
                        "reason": None,
                        # No reviewer response exists on this path:
                        # usage is explicitly unknown, never reused
                        # from an earlier request.
                        "usage": "unknown",
                    },
                    "analysis_bypass": {"reason": reason},
                }
            )
        return text

    def repair(self, text: str) -> str:
        raw_started = time.monotonic()
        # Versioned finite analysis eligibility (order 025-a,
        # requirement 3): the ORIGINAL completed answer is checked on
        # its exact codepoint count first, then on its strict
        # original UTF-8 byte count (no NFC, stripping or other
        # transformation), BEFORE resolve/protect/map/residual/
        # tokenize/index/reviewer work.  Ineligibility - an invalid
        # policy, either size axis exceeded, or an unencodable
        # original - returns the exact completed original with a
        # fixed content-free analysis reason and zero optional work;
        # every admitted answer still runs the mandatory Pandoc
        # pipeline below unchanged.  Only the declared policy
        # (ValueError) and encoding (UnicodeEncodeError) conditions
        # are translated; caller control and MemoryError propagate
        # untouched.
        try:
            codepoint_limit, byte_limit = analysis_policy.current_limits()
        except ValueError:
            return self._fail_closed_analysis(
                text, raw_started, analysis_policy.ANALYSIS_POLICY_INVALID
            )
        reason = analysis_policy.classify_original(
            text, codepoint_limit, byte_limit
        )
        if reason is not None:
            return self._fail_closed_analysis(text, raw_started, reason)
        try:
            spec = self.pandoc if self.pandoc is not None else resolve_pandoc_spec()
            outcome = protect_with_pandoc(spec, text)
            if not outcome.ok:
                return self._fail_closed_original(
                    text, raw_started, outcome.reason, outcome.detail
                )
            intervals = compose_protection(text, outcome)
        except PandocStartupError as exc:
            return self._fail_closed_original(text, raw_started, exc.reason, exc.detail)
        except Exception as exc:  # noqa: BLE001 - fail closed before Corpus
            # Any unexpected mapping, composition or depth failure must be
            # translated to the fail-closed original, never escape to the
            # handler or widen around the upstream capture path.
            return self._fail_closed_original(
                text, raw_started, "PANDOC_UNEXPECTED", type(exc).__name__
            )
        # Technical evidence access opens only after complete-main
        # eligibility: an invalid or ineligible main response never opens
        # or creates the index (order 016-a, requirements 4 and 6).  The
        # adapter is strictly read-only over the existing index.
        try:
            corpus = RuntimeCorpus(self.index)
        except RuntimeCorpusError as exc:
            return self._fail_closed_evidence(text, raw_started, exc.reason, "early")
        try:
            try:
                detector_started = time.monotonic()
                candidates = detect(text, corpus, intervals, mode=self.mode, maximum=4)
            except RuntimeCorpusError as exc:
                # Detection queried the index: same early boundary - exact
                # completed original with zero edits and zero review calls.
                return self._fail_closed_evidence(
                    text, raw_started, exc.reason, "early"
                )
            detector_seconds = time.monotonic() - detector_started
            tokens = tokenize(text, intervals)
            prepared: list[_PreparedCandidate] = []
            selected_invalid = False
            for candidate in candidates:
                token_index = next(
                    (i for i, token in enumerate(tokens) if token.start == candidate.start),
                    None,
                )
                if token_index is None:
                    # A detected occurrence whose start matches no token is
                    # invalid/stale selection: the whole answer returns the
                    # completed original with zero calls, never a valid
                    # subset (order 014-a, requirement 2).
                    selected_invalid = True
                    break
                prepared.append(
                    _PreparedCandidate(
                        candidate,
                        left=tokens[token_index - 1].key if token_index else None,
                        right=tokens[token_index + 1].key
                        if token_index + 1 < len(tokens)
                        else None,
                        left_bounds=(
                            (tokens[token_index - 1].start, tokens[token_index - 1].end)
                            if token_index
                            else None
                        ),
                        right_bounds=(
                            (tokens[token_index + 1].start, tokens[token_index + 1].end)
                            if token_index + 1 < len(tokens)
                            else None
                        ),
                    )
                )
            # Bounded review budget: at most one fresh batch request per
            # completed answer (order 014-a, requirements 2-4 and 7).
            review_batch: dict[str, object] = {
                "calls": 0,
                "targets": len(candidates) if selected_invalid else len(prepared),
                "outcome": "skipped",
                "reason": REASON_PREP_INVALID if selected_invalid else None,
                # Request-local default: every path without a reviewer
                # response (Pandoc failure, no suspicion, unsupported
                # response, failed batch) reports explicit unknown usage,
                # never a zero and never an earlier request's usage.
                "usage": "unknown",
            }
            proposals: dict[str, BatchProposal] | None = None
            aligned: list[str] | None = None
            reviewer_seconds = 0.0
            if prepared and not selected_invalid:
                occurrences = tuple(
                    (item.candidate.start, item.candidate.end, item.candidate.text)
                    for item in prepared
                )
                protected = tuple((item.start, item.end) for item in intervals)
                targets = prepare_targets(text, occurrences, protected)
                if targets is None:
                    # Invalid/stale/protected/oversized batch preparation:
                    # completed original with zero calls.
                    review_batch["reason"] = REASON_PREP_INVALID
                elif build_prompt(targets) is None:
                    review_batch["targets"] = len(targets)
                    review_batch["reason"] = REASON_PROMPT_OVERSIZE
                else:
                    batch_started = time.monotonic()
                    try:
                        batch_result = self.reviewer.review_batch(text, targets)
                        proposals = batch_result.proposals
                        self._review_usage = batch_result.usage
                    except Exception as exc:
                        # Only the closed vocabulary of fixed labels is
                        # trusted; anything else maps to REVIEW_FAILED so
                        # untrusted exception content never reaches traces.
                        # (type guard first: an unhashable reason must not
                        # raise inside this fallback path.)
                        reason = getattr(exc, "reason", None)
                        if type(reason) is not str or reason not in BOUND_REVIEW_REASONS:
                            reason = REASON_FAILED
                        review_batch["targets"] = len(targets)
                        review_batch["outcome"] = "failed"
                        review_batch["reason"] = reason
                        review_batch["calls"] = (
                            0
                            if reason in (REASON_PROMPT_OVERSIZE, REASON_REQUEST_OVERSIZE)
                            else 1
                        )
                    else:
                        aligned = [target.id for target in targets]
                        review_batch["targets"] = len(targets)
                        review_batch["outcome"] = "ok"
                        review_batch["calls"] = 1
                        # Actual reviewer usage, separately from main
                        # usage; absence/invalidity stays unknown.
                        review_batch["usage"] = (
                            {
                                "input_tokens": self._review_usage.input_tokens,
                                "output_tokens": self._review_usage.output_tokens,
                                "total_tokens": self._review_usage.total_tokens,
                            }
                            if self._review_usage is not None
                            else "unknown"
                        )
                    finally:
                        reviewer_seconds = time.monotonic() - batch_started
            decisions: list[dict[str, object]] = []
            edits: list[tuple[int, int, str]] = []
            # Late technical evidence failure state: a known
            # RuntimeCorpusError during per-proposal acceptance aborts the
            # entire optional pass from the immutable original.
            late_aborted = False
            evidence_reason: str | None = None
            for index, item in enumerate(prepared):
                candidate = item.candidate
                review_started = time.monotonic()
                proposal_record: dict[str, object] | None = None
                acceptance: dict[str, object] = {
                    "accepted": False,
                    "reason": "reviewer-error",
                    "replacement": None,
                }
                failure: str | None = None
                if late_aborted:
                    # The optional pass already aborted: no earlier accepted
                    # edit survives and no further proposal is applied; the
                    # reviewer proposal is retained separately as untrusted
                    # data, never as an acceptance.
                    if aligned is not None and proposals is not None:
                        batch_proposal = proposals[aligned[index]]
                        proposal_record = {
                            "keep": batch_proposal.keep,
                            "replacement": batch_proposal.replacement,
                            "needs_wider_edit": batch_proposal.needs_wider_edit,
                        }
                    acceptance = {
                        "accepted": False,
                        "reason": "evidence-abort",
                        "replacement": None,
                    }
                    failure = evidence_reason
                elif aligned is not None and proposals is not None:
                    batch_proposal = proposals[aligned[index]]
                    try:
                        value = Proposal(
                            batch_proposal.keep,
                            batch_proposal.replacement,
                            batch_proposal.needs_wider_edit,
                        )
                        proposal_record = {
                            "keep": value.keep,
                            "replacement": value.replacement,
                            "needs_wider_edit": value.needs_wider_edit,
                        }
                        decision = accept(
                            text,
                            candidate,
                            value,
                            corpus,
                            intervals,
                            left=item.left,
                            right=item.right,
                            left_bounds=item.left_bounds,
                            right_bounds=item.right_bounds,
                        )
                        acceptance = {
                            "accepted": decision.accepted,
                            "reason": decision.reason,
                            "replacement": decision.replacement,
                        }
                    except RuntimeCorpusError as exc:
                        # A known technical evidence error escapes the
                        # per-proposal generic catch: it aborts the entire
                        # optional pass from the immutable original, with the
                        # actual review attempt and known/unknown usage
                        # preserved (order 016-a, requirement 4).
                        late_aborted = True
                        evidence_reason = exc.reason
                        acceptance = {
                            "accepted": False,
                            "reason": "evidence-abort",
                            "replacement": None,
                        }
                        failure = exc.reason
                    except Exception:
                        # Individual isolation: a failed acceptance never
                        # invalidates the other independent proposals.
                        failure = "reviewer-error"
                else:
                    # Whole-batch failure: byte-exact original, no edit.
                    failure = "reviewer-error"
                decisions.append(
                    {
                        "candidate": candidate.as_dict(),
                        "evidence": candidate.evidence,
                        "neighbors": {"left": item.left, "right": item.right},
                        "proposal": proposal_record,
                        "acceptance": acceptance,
                        "failure": failure,
                        "timing_seconds": round(time.monotonic() - review_started, 6),
                    }
                )
                if acceptance["accepted"] and isinstance(acceptance["replacement"], str):
                    edits.append((candidate.start, candidate.end, acceptance["replacement"]))
            if late_aborted:
                # Whole optional pass aborted from a technical evidence
                # failure: the immutable original is delivered and no
                # earlier accepted edit survives.  Every persisted decision
                # reflects that final disposition (not accepted); the
                # reviewer proposals are retained separately as untrusted
                # data, and the actual review call and known/unknown usage
                # stay recorded.
                edits = []
                for record in decisions:
                    record["acceptance"] = {
                        "accepted": False,
                        "reason": "evidence-abort",
                        "replacement": None,
                    }
                    record["failure"] = evidence_reason
            repaired = apply_edits(text, edits, intervals) if edits else text
            protected_changes = 0
            for interval in intervals:
                shift = sum(
                    len(replacement) - (end - start)
                    for start, end, replacement in edits
                    if end <= interval.start
                )
                start = interval.start + shift
                if (
                    repaired[start : start + interval.end - interval.start]
                    != text[interval.start : interval.end]
                ):
                    protected_changes += 1
        finally:
            corpus.close()
        if self._details is not None:
            detail: dict[str, object] = {
                    "original": text,
                    "repaired": repaired,
                    "candidates": [candidate.as_dict() for candidate in candidates],
                    "corpus_summaries": [candidate.evidence for candidate in candidates],
                    "reviewer_decisions": decisions,
                    "acceptance": [item["acceptance"] for item in decisions],
                    "replacements": [item[2] for item in edits],
                    "timings": {
                        "raw_seconds": 0.0,
                        "detector_seconds": round(detector_seconds, 6),
                        "reviewer_seconds": round(reviewer_seconds, 6),
                        "repair_seconds": round(time.monotonic() - raw_started, 6),
                    },
                    "protected_difference_count": protected_changes,
                    "review_batch": review_batch,
                }
            if late_aborted:
                # Recorded with the actual review attempt preserved (calls
                # and known/unknown usage); never a Pandoc failure and never
                # zeroed (order 016-a, requirement 4).
                detail["evidence_failure"] = {
                    "reason": evidence_reason,
                    "stage": "late",
                }
            self._details.append(detail)
        return repaired


class _Handler(BaseHTTPRequestHandler):
    server_version = "concept-verification/1"
    _intake: client_transport.IntakeGuard | None = None
    _delivery: delivery_transport.DeliveryGuard | None = None
    _emission_begun: bool = False

    def handle_one_request(self) -> None:
        # One anchored incoming-intake deadline BEFORE any
        # request-line/header/body read and before the guard starts
        # (order 020-a, requirement 1); OS accept-backlog waiting is
        # outside this scope.  The stdlib finite line/header-count
        # guards remain.
        owner = cast(ConceptProxy, self.server)
        self._intake = client_transport.IntakeGuard(
            self.connection, owner.client_timeout
        )
        try:
            super().handle_one_request()
        finally:
            # Release and actually join the owned intake guard on
            # every path: success, EOF, timeout, unsupported
            # method/path, framing rejection, parse failure,
            # exception or startup failure.  No intake worker
            # survives the request (order 020-a, requirement 2).
            if self._intake is not None:
                self._intake.release()
                self._intake = None

    def _deliver(self, emit: Callable[[], None]) -> None:
        """Emit one post-intake response under one delivery deadline.

        One absolute monotonic deadline anchors immediately before
        this emission's status/headers/body/flush and before the
        owned guard starts; response-ready work (upstream capture,
        optional repair) is outside the phase (order 021-a,
        requirement 2).  Byte progress, short writes and internal
        retries never reset it.  On expiry or a write/flush/
        early-disconnect failure the connection closes quietly: no
        body is logged, no second response/status/fallback is
        attempted on this socket, and a partially written body is
        never labelled completed (order 021-a, requirement 4).  The
        guard is cancelled and actually joined on every path before
        this handler returns to the next connection (order 021-a,
        requirement 3).
        """
        owner = cast(ConceptProxy, self.server)
        # No-retry ownership marker BEFORE any fallible delivery
        # setup (order 021-a, requirement 4): a delivery attempt
        # that fails before bytes - including a guard startup
        # failure - closes safely and never triggers another
        # response or a second delivery attempt on this socket.
        self._emission_begun = True
        try:
            guard = delivery_transport.DeliveryGuard(
                self.connection, owner.delivery_timeout
            )
        except Exception:
            # Guard startup failure (partial startup already
            # cancelled and actually joined inside the guard):
            # quiet close, no second response, no retry.
            self.close_connection = True
            return
        self._delivery = guard
        try:
            if guard.is_expired():
                # A successful guard startup that already consumed the
                # whole budget expires the anchored absolute clock
                # BEFORE emission can begin: the response must not be
                # started (late or racing completion loses to expiry,
                # order 021-a, requirement 2).  Close quietly without
                # any status/headers/body; the owned guard is still
                # cancelled and actually joined in the finally below.
                self.close_connection = True
                return
            emit()
            # The common explicit flush belongs inside the common
            # delivery lifecycle so every post-intake response -
            # normal emission, contract 400, protocol/generated 502 -
            # classifies its actual flush against the one delivery
            # clock (order 021-a, requirements 2 and 4).  On the
            # native unbuffered _SocketWriter this flush is a no-op
            # (the bytes were already sent by write), and later
            # stdlib unbuffered flushes are likewise no-ops; it is
            # the phase-ownership point, not a network barrier.
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError, ValueError):
            # write/flush failure or early client disconnect: quiet
            # close, no duplicate response, no body logging.
            self.close_connection = True
        finally:
            if guard.release():
                # The absolute deadline passed before the emission
                # completed (or a racing completion lost to it): the
                # partial (if any) body is never completed and no
                # second response is attempted on this socket.
                self.close_connection = True

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/responses":
            self.send_error(404)
            return
        owner = cast(ConceptProxy, self.server)
        # Strict unambiguous framing before any body read or
        # forwarding (order 020-a, requirement 3): repeated
        # Content-Length fields (even equal), comma lists, any
        # Transfer-Encoding and any unsupported Expect are fixed
        # content-free 400 rejections with connection close; a
        # missing length, a nondecimal value (including signed) or
        # an overlarge length keeps the existing bounded 413 size
        # policy.
        framing = client_transport.check_request_framing(self.headers)
        if isinstance(framing, client_transport.FramingRejection):
            if framing.status == 413:
                self.send_error(413)
            else:
                self._send_intake_error(400, framing.code)
            self.close_connection = True
            return
        _zero, length, _empty = framing
        # Read exactly the advertised length under the one anchored
        # intake deadline; the owned guard unblocks a waiting read by
        # shutting down only this accepted socket object (order
        # 020-a, requirements 2 and 4).
        body = self.rfile.read(length)
        # Release and actually join the intake guard BEFORE request
        # validation, forwarding or engine work (order 020-a,
        # requirement 5): the timer cannot fire later during
        # legitimate slow main/review work or interrupt another
        # connection.  A late or racing completion loses to the
        # expired clock and can never reach main.
        if self._intake is not None and self._intake.release():
            # Bounded best-effort 408 on an interrupted connection;
            # never blocks indefinitely, then closes with zero main,
            # analysis, evidence or review calls.
            self._send_intake_error(408, "REQUEST_INTAKE_TIMEOUT")
            self.close_connection = True
            return
        if len(body) != length:
            # EOF (or the guard's interruption) delivered fewer bytes
            # than advertised: a complete valid JSON prefix is NOT a
            # complete advertised body.  Fixed content-free 400 where
            # delivery is possible; always closes (order 020-a,
            # requirement 4).  Bytes beyond the one advertised
            # request can never become a second upstream request
            # (HTTP/1.0 close, no pipelining).
            self._send_intake_error(400, "REQUEST_BODY_INCOMPLETE")
            self.close_connection = True
            return
        request_id = self.headers.get("X-Concept-Request-ID", "")
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", request_id):
            request_id = uuid.uuid4().hex
        started = time.monotonic()
        try:
            try:
                contract = validate_request(body)
            except RequestContractError as exc:
                # Bounded content-free rejection before any upstream or
                # reviewer call: unsupported capabilities and invalid
                # requests never reach main generation (order 015-a,
                # requirement 2).  This post-intake emission runs
                # under the one delivery deadline (order 021-a,
                # requirement 4).  The fixed validated reason is
                # bound to an ordinary local before the callback:
                # the except-as variable is deleted at block end and
                # must not be closed over.
                reason = exc.reason
                self._deliver(
                    lambda: self._send_error_json(
                        400, "invalid_request", reason
                    )
                )
                return
            if hasattr(owner.engine, "begin_request"):
                owner.engine.begin_request()
            forwarded = owner.forward(body, dict(self.headers))
            raw_seconds = time.monotonic() - started
            repaired = forwarded.body
            if forwarded.status == 200:
                # The declared client mode must agree with the observed
                # upstream content type; a mismatch (including an unknown
                # type) is a bounded upstream protocol failure, never a
                # silent mode switch (order 015-a, requirement 6).
                media_type = forwarded.content_type.split(";", 1)[0].strip().lower()
                if contract.stream and media_type != "text/event-stream":
                    self._deliver(
                        lambda: self._send_error_json(
                            502,
                            "upstream_protocol_error",
                            "RESPONSE_MODE_MISMATCH",
                        )
                    )
                    return
                if not contract.stream and media_type != "application/json":
                    self._deliver(
                        lambda: self._send_error_json(
                            502,
                            "upstream_protocol_error",
                            "RESPONSE_MODE_MISMATCH",
                        )
                    )
                    return
                if contract.stream:
                    repaired, _ = transform_sse(forwarded.body, owner.engine.repair)
                else:
                    repaired, _ = transform_json(forwarded.body, owner.engine.repair)
                if hasattr(owner.engine, "take_details") and hasattr(owner, "write_traces"):
                    details = owner.engine.take_details()
                    owner.write_traces(
                        request_id,
                        details,
                        time.monotonic() - started,
                        raw_seconds,
                    )
                    owner.observe_usage(details)
            def _emit() -> None:
                # The delivery deadline is anchored inside _deliver
                # immediately before this emission and before the
                # owned guard starts (order 021-a, requirement 2);
                # the common explicit flush in _deliver keeps the
                # whole status/headers/body/flush phase inside the
                # one clock.
                content_type = (
                    forwarded.content_type or "application/octet-stream"
                )
                self.send_response(forwarded.status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(repaired)))
                self.end_headers()
                self.wfile.write(repaired)

            self._deliver(_emit)
        except BrokenPipeError:
            return
        except Exception:
            # Post-intake generated error (order 021-a, requirement
            # 4): only while no response emission has begun.  Once
            # emission began, a failed partial send is closed quietly
            # - never a second response/status/502/fallback on the
            # same socket.
            if not self._emission_begun:
                try:
                    self._deliver(lambda: self.send_error(502))
                except Exception:
                    self.close_connection = True

    def _send_intake_error(self, status: int, code: str) -> None:
        """Bounded best-effort fixed content-free intake error.

        A short socket timeout bounds the send so an error on an
        interrupted connection never blocks indefinitely; any failure
        is suppressed and the caller closes the connection (order
        020-a, requirement 4).  No raw exception, request, credential,
        header or text is emitted.
        """
        error_type = "request_timeout" if status == 408 else "invalid_request"
        payload = json.dumps(
            {"error": {"type": error_type, "code": code}},
            separators=(",", ":"),
        ).encode()
        sock = self.connection
        previous: float | None = None
        try:
            previous = sock.gettimeout()
            sock.settimeout(1.0)
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError, ValueError):
            return
        finally:
            with contextlib.suppress(Exception):
                if previous is not None:
                    sock.settimeout(previous)

    def _send_error_json(self, status: int, error_type: str, code: str) -> None:
        payload = json.dumps(
            {"error": {"type": error_type, "code": code}}, separators=(",", ":")
        ).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        try:
            self.wfile.write(payload)
        except BrokenPipeError:
            return

    def log_message(self, *_: object) -> None:
        return


class ConceptProxy(HTTPServer):
    def __init__(
        self,
        address: tuple[str, int],
        upstream: str,
        engine: RepairEngine,
        timeout: float = 30.0,
        trace_dir: Path | None = None,
        usage_observer: Callable[[dict[str, object]], None] | None = None,
        *,
        header_timeout: float = MAIN_HEADER_TIMEOUT_SECONDS,
        client_timeout: float = CLIENT_REQUEST_TIMEOUT_SECONDS,
        delivery_timeout: float = CLIENT_DELIVERY_TIMEOUT_SECONDS,
        setup_timeout: float = MAIN_SETUP_TIMEOUT_SECONDS,
    ):
        if address[0] != "127.0.0.1":
            raise ValueError("proxy must bind to loopback")
        parsed = urlparse(upstream)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("upstream must be an explicit HTTP URL")
        if parsed.port == 0:
            # Keep the full 16-bit port meaning: an explicit :0 is
            # rejected, never aliased to the scheme default (order
            # 022-a, requirement 4).
            raise ValueError("upstream port must be an explicit 1-65535")
        # Independent finite positive elapsed header budget (order
        # 018-a, requirement 2): separate from the socket/body capture
        # timeout; rejected before any bind allocation or traffic is
        # accepted, and validated again at guard use.
        self.header_timeout = header_transport.validate_header_budget(
            header_timeout
        )
        # Independent finite positive elapsed incoming-intake budget
        # (order 020-a, requirement 1): separate from the socket/body
        # capture timeout, the header budget and the fixed 15 s
        # reviewer budget; rejected before any bind allocation or
        # traffic is accepted, and validated again at guard use.
        self.client_timeout = client_transport.validate_client_budget(
            client_timeout
        )
        # Independent finite positive elapsed final-delivery budget
        # (order 021-a, requirement 1): bounds the final response
        # emission (status/headers/body/flush) after the response
        # bytes are ready; separate from the socket/body capture
        # timeout, the header budget, the intake budget and the fixed
        # 15 s reviewer budget; rejected before any bind allocation
        # or traffic is accepted, and validated again at guard use.
        self.delivery_timeout = delivery_transport.validate_delivery_budget(
            delivery_timeout
        )
        # Independent finite positive elapsed main-upstream setup
        # budget (order 022-a, requirement 1): bounds owned
        # transport startup, resolver, address attempts, connect,
        # TLS handshake and the entire request write before response
        # acquisition; separate from the socket/body capture timeout,
        # the header budget, the intake budget, the delivery budget
        # and the fixed 15 s reviewer budget; rejected before any
        # bind allocation or traffic is accepted, and validated
        # again at use.
        self.setup_timeout = upstream_setup.validate_setup_budget(
            setup_timeout
        )
        # Finite positive body budget (order 017-a, requirement
        # 2): nonfinite or nonpositive operator values are rejected
        # before any bind allocation or traffic is accepted.
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout)
            or timeout <= 0
        ):
            raise ValueError(
                "capture timeout must be a finite positive duration"
            )
        # Bounded evidence lookup policy (order 024-a, requirement
        # 2): the CURRENT config default policy must hold before any
        # bind allocation or traffic is accepted.  This pure
        # validation reads no index, file or connection, so a
        # startup-invalid policy fails here, before bind, while
        # at-use invalidity becomes the fixed RuntimeCorpus
        # budget-invalid label.
        validate_default_evidence_policy()
        # Versioned finite analysis-eligibility policy (order 025-a,
        # requirement 2): the CURRENT config default policy must hold
        # before any bind allocation or traffic is accepted.  This
        # pure validation reads no file, model, network or index, so
        # a startup-invalid policy fails here, before bind, with a
        # plain ValueError; a startup success is not a live
        # inference proof, and the mandatory normal-main Pandoc
        # startup/version/capability check remains the separate
        # startup contract.  At-use invalidity later becomes the
        # fixed content-free ANALYSIS_POLICY_INVALID bypass.
        analysis_policy.current_limits()
        # Finite accepted-request admission policy (order 026-a,
        # requirement 1): the CURRENT config admission defaults
        # must hold before any bind allocation or traffic is
        # accepted.  This pure validation reads no file, model,
        # network or index, so a startup-invalid policy fails
        # here, before bind, with a plain ValueError.  The
        # validated policy is immutable per instance: running
        # instances retain it while later config defaults apply
        # only to newly constructed instances.
        self._admission_policy = request_admission.current_admission_policy()
        super().__init__(address, _Handler)
        self.upstream = parsed
        self.engine = engine
        self.capture_timeout = timeout
        self.trace_dir = trace_dir
        # Bounded content-free operator observation of separated review
        # usage (order 015-a, requirement 7); None disables observation.
        self.usage_observer = usage_observer
        if trace_dir is not None and trace_dir.exists() and trace_dir.is_symlink():
            raise ValueError("trace directory must not be a symlink")
        if trace_dir is not None:
            trace_dir.mkdir(parents=True, exist_ok=True)
        # One owned accepted-request admission lifecycle (order
        # 026-a): the fixed owned worker/monitor threads start
        # synchronously here, before request traffic, and commit
        # to dispatch only after this constructor has fully
        # completed; partial-startup ownership is contained inside
        # the controller (started threads stopped and actually
        # joined, never-started threads never joined, first
        # current-operation control preserved).  A construction or
        # thread startup failure must not leave the bound listener
        # socket open: the exact first control is preserved and the
        # listener is closed as independent best-effort cleanup
        # (order 026-a, requirement 5).
        try:
            self._admission = request_admission.RequestAdmissionController(
                self, self._admission_policy
            )
            self._admission.start()
        except BaseException:
            with contextlib.suppress(Exception):
                super().server_close()
            raise

    def _handle_request_noblock(self) -> None:
        # The accepting loop (order 026-a, requirements 2 and 3):
        # accept, then one owned admission decision - admit in
        # accepted order, or one fixed bounded 503 and close -
        # with the one absolute queue deadline anchored inside
        # dispatch before admission allocation/queue work.  The
        # accepting loop never runs a request, so it keeps
        # accepting while one handler is held; the admitted entry
        # is later handled inline by the single owned handler
        # worker through the standard process_request boundary,
        # preserving the existing outer HTTP error semantics -
        # and the frozen test fixtures' process_request
        # completion observation - exactly.
        # The narrowing below uses the import-time captured class
        # (see _SOCKET_CLASS above) rather than the mutable module
        # attribute; the impossible non-socket member routes to the
        # existing content-free server error boundary.
        try:
            request, client_address = self.get_request()
        except OSError:
            return
        if not self.verify_request(request, client_address):
            return
        if not isinstance(request, _SOCKET_CLASS):
            self.handle_error(request, client_address)
            return
        try:
            self._admission.dispatch(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
            with contextlib.suppress(Exception):
                self.shutdown_request(request)
        except BaseException:
            with contextlib.suppress(Exception):
                self.shutdown_request(request)
            raise

    def shutdown(self) -> None:
        # Stop the accepting loop first, then the documented
        # owning admission close boundary (order 026-a,
        # requirement 5): stop admission, cancel/close every
        # waiting entry with the fixed closed code, release every
        # owned slot and actually join the exact owned workers
        # before returning; an owned nonordinary worker control is
        # re-raised here at the owning supervisor.  Must run from
        # a different thread than serve_forever (native
        # BaseServer contract).  The admission close may re-raise a
        # preserved owned control, so the listener close is an
        # independent finalization step that runs before the
        # control propagates; the native shutdown threading
        # semantics are unchanged.
        super().shutdown()
        try:
            self._admission.stop()
        except BaseException:
            with contextlib.suppress(Exception):
                super().server_close()
            raise

    def server_close(self) -> None:
        # The accepting-loop socket close boundary (order 026-a,
        # requirement 5): the documented owning admission close
        # runs BEFORE the listener socket is closed, so a close of
        # the accepting loop alone can never leave the fixed owned
        # workers running.  The admission close may re-raise a
        # preserved owned control, and the admission lifecycle may
        # not exist yet (the native constructor failure path
        # virtually invokes this method before _admission is
        # constructed), so the listener close is an independent
        # finalization step that runs in every case and any
        # preserved control is re-raised only after it.  Idempotent
        # after an owning shutdown close.
        control: BaseException | None = None
        admission: (
            request_admission.RequestAdmissionController | None
        ) = getattr(self, "_admission", None)
        if admission is not None:
            try:
                admission.stop()
            except BaseException as exc:
                control = exc
        super().server_close()
        if control is not None:
            raise control

    def handle_error(self, request: object, client_address: object) -> None:
        # Bounded content-free intake diagnostics (order 020-a,
        # requirement 4): handler failures are closed quietly; no
        # raw exception, request, credential, header or text reaches
        # the log.
        return

    def observe_usage(self, details: list[dict[str, object]]) -> None:
        """One bounded content-free request-local review usage record.

        ``review_calls`` counts attempted batch requests (zero versus one
        is recorded separately from whether usage is known);
        ``reviewer_usage`` is the actual reviewer usage object or the
        explicit string ``"unknown"`` (never zero, never carried over
        from an earlier request).  Observation failure must not change a
        safely completed answer or hide a main failure.

        The record is content-free: it carries counts and usage numbers
        only, never a caller-supplied identifier (the legacy opt-in trace
        files keep their own request id separately).
        """
        if self.usage_observer is None:
            return
        calls = 0
        usage: object = "unknown"
        for detail in details:
            review_batch = detail.get("review_batch")
            if not isinstance(review_batch, dict):
                continue
            attempted = review_batch.get("calls")
            if type(attempted) is int:
                calls += attempted
            record = review_batch.get("usage")
            if isinstance(record, dict):
                usage = {
                    "input_tokens": record.get("input_tokens"),
                    "output_tokens": record.get("output_tokens"),
                    "total_tokens": record.get("total_tokens"),
                }
        if calls == 0:
            usage = "unknown"
        record = {"review_calls": calls, "reviewer_usage": usage}
        # Best-effort observation: a failing operator probe must not
        # change the answer or hide a main failure.
        with contextlib.suppress(Exception):
            self.usage_observer(record)
            pass

    def write_traces(
        self,
        request_id: str,
        details: list[dict[str, object]],
        proxy_seconds: float,
        raw_seconds: float = 0.0,
    ) -> list[Path]:
        if self.trace_dir is None:
            return []
        paths: list[Path] = []
        for index, detail in enumerate(details):
            detail_timings = detail.get("timings")
            timings: dict[str, object] = {}
            if isinstance(detail_timings, dict):
                timings.update(detail_timings)
            value: dict[str, object] = {
                "request_id": request_id,
                "message_index": index,
                "original": detail["original"],
                "repaired": detail["repaired"],
                "candidates": detail["candidates"],
                "corpus_summaries": detail["corpus_summaries"],
                "reviewer_decisions": detail["reviewer_decisions"],
                "acceptance": detail["acceptance"],
                "replacements": detail["replacements"],
                "timings": {
                    **timings,
                    "raw_seconds": round(raw_seconds, 6),
                    "proxy_seconds": round(proxy_seconds, 6),
                },
                "protected_difference_count": detail["protected_difference_count"],
                "protocol": {"response_completed": True, "valid": True},
            }
            # Content-free technical evidence failure marker (fixed label
            # plus early/late stage); persisted whenever the optional pass
            # was aborted or short-circuited by a known evidence error.
            evidence_failure = detail.get("evidence_failure")
            if isinstance(evidence_failure, dict):
                value["evidence_failure"] = evidence_failure
            # Content-free analysis-eligibility bypass marker (fixed
            # reason only); persisted whenever the optional analysis
            # pass was skipped by the finite policy gate before any
            # analysis work (order 025-a, requirement 4).
            analysis_bypass = detail.get("analysis_bypass")
            if isinstance(analysis_bypass, dict):
                value["analysis_bypass"] = analysis_bypass
            # Optional trace serialization boundary (order 025-a,
            # requirement 4): the existing shared canonical serializer
            # (unchanged global config.canonical_bytes) is computed
            # BEFORE any tempfile allocation.  A detail whose completed
            # original the serializer cannot represent (an unpaired
            # surrogate) raises UnicodeEncodeError and that ONE
            # optional trace detail/file is skipped - no empty
            # temporary artifact, no raw-text persistence, no answer
            # transformation - so the in-memory analysis_bypass
            # reason, the zero-call shape, the usage observer and the
            # exact original delivery continue unchanged.  Only
            # UnicodeEncodeError is caught: MemoryError, caller
            # control and file I/O errors are not hidden, and no
            # ASCII fallback or re-rendering is added.
            try:
                payload = canonical_bytes(value)
            except UnicodeEncodeError:
                continue
            target = self.trace_dir / f"{request_id}-{index}.json"
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix=".trace-", suffix=".tmp", dir=self.trace_dir, delete=False
            ) as handle:
                temporary = Path(handle.name)
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, target)
            paths.append(target)
        return paths

    def forward(self, body: bytes, incoming: dict[str, str]) -> Forwarded:
        host = self.upstream.hostname
        if host is None:
            raise ProxyError("upstream hostname is missing")
        # Narrow forwarded header policy (order 015-a, requirement 3):
        # only content-type, accept and an explicitly caller-provided
        # Authorization reach the main upstream.  Hop-by-hop, internal
        # control and linkage headers (host, content-length, cookies,
        # session/request ids, proxy controls) are never forwarded, and
        # the reviewer's API key is never borrowed as a main credential.
        headers = {
            key: value
            for key, value in incoming.items()
            if key.lower() in {"content-type", "accept", "authorization"}
        }
        headers["Content-Length"] = str(len(body))
        # One absolute monotonic setup deadline anchored at entry to
        # the owned main forward setup, BEFORE any worker/guard/
        # process/IPC startup, resolver call, connect/TLS or request
        # emission (order 022-a, requirement 2): it covers owned
        # transport startup, resolver, bounded address attempts,
        # connect, the TLS handshake and the entire request write
        # through the last body byte handed to the local transport,
        # and never resets.  A successful setup releases its clock
        # before response-header acquisition; the existing header/
        # body, intake and delivery clocks stay independent.  Setup
        # failure is a main failure (the handler's existing fixed
        # content-free 502 path) with zero engine, corpus or reviewer
        # work.
        # The setup budget is re-validated at use, before the
        # arithmetic or any downstream work (order 022-a,
        # requirement 1): the constructor validates the configured
        # value before bind, and the setup path rejects a mutated or
        # otherwise invalid instance value now, never accepting it as
        # a duration.
        setup_budget = upstream_setup.validate_setup_budget(
            self.setup_timeout
        )
        deadline = time.monotonic() + setup_budget
        port = self.upstream.port
        if port is None:
            port = 443 if self.upstream.scheme == "https" else 80
        response: http.client.HTTPResponse | None = None
        connection: http.client.HTTPConnection | None = None
        try:
            connection = upstream_setup.open_upstream_connection(
                scheme=self.upstream.scheme,
                host=host,
                port=port,
                request_path=responses_path(self.upstream.path),
                body=body,
                headers=headers,
                deadline=deadline,
                capture_timeout=self.capture_timeout,
            )
            # One elapsed header budget anchored immediately before
            # acquisition (order 018-a, requirement 2): the stdlib
            # getresponse parser is retained unchanged; the owned guard
            # interrupts only this connection's owned socket on
            # expiration and joins before any body capture, so the 017
            # body deadline below begins later and stays independent.
            response = header_transport.acquire_response(
                connection, self.header_timeout
            )
            content_type = response.getheader("Content-Type", "")
            raw = _bounded_read(
                response,
                MAIN_BODY_MAX_BYTES,
                self.capture_timeout,
                require_complete_sse=response.status == 200
                and content_type.lower().startswith("text/event-stream"),
            )
            return Forwarded(response.status, raw, content_type)
        finally:
            # Close the response body (and any over-read buffer) and the
            # owned transport handle: no transport outlives the request.
            if response is not None:
                response.close()
            if connection is not None:
                connection.close()


def _stderr_usage_observer(record: dict[str, object]) -> None:
    """Bounded content-free stderr record for operator observation.

    Enabled with ``CONCEPT_USAGE_OBSERVER=stderr`` (order 015-a,
    requirement 7): no new HTTP route, metrics service or raw-text log;
    the record carries counts and usage numbers only.
    """
    usage = record.get("reviewer_usage")
    if isinstance(usage, dict):
        line = (
            "concept-review-usage "
            f"calls={record.get('review_calls')} "
            f"usage=input={usage.get('input_tokens')},"
            f"output={usage.get('output_tokens')},"
            f"total={usage.get('total_tokens')}"
        )
    else:
        line = f"concept-review-usage calls={record.get('review_calls')} usage=unknown"
    print(line, file=sys.stderr, flush=True)


class _IntakeKwargs(TypedDict, total=False):
    """Optional operator-forwarded budget keywords for the real
    validated constructor (orders 020-a, 021-a and 022-a,
    requirement 1)."""

    client_timeout: float
    delivery_timeout: float
    setup_timeout: float


def main() -> int:
    upstream = os.environ.get("CONCEPT_UPSTREAM_URL", "http://127.0.0.1:8001")
    index = os.environ.get("CONCEPT_INDEX")
    if not index:
        raise SystemExit("CONCEPT_INDEX is required")
    # Mandatory qualified-Pandoc startup check (order 013-a, requirements 2
    # and 12): executable presence, exact version and reader capability,
    # verified before the proxy accepts any traffic (before the HTTP bind).
    # There is no historical pulldown discovery or regex fallback path.
    try:
        pandoc_spec = resolve_pandoc_spec()
        check_pandoc(pandoc_spec)
    except PandocStartupError as exc:
        raise SystemExit(f"pandoc startup failure: {exc.reason}: {exc.detail}") from None
    # The batch reviewer is bounded by the ordered finite 15-second
    # cap, now the whole runtime exchange deadline: one monotonic
    # deadline anchored at review_batch entry covers process/IPC
    # startup and the owned child's actual resolver/connect/TLS/
    # upload/status/header/body/result work, a late success being a
    # failure (order 019-a).  The upstream capture timeout
    # (CONCEPT_TIMEOUT, socket/body axis) and the independent elapsed
    # response-header budget (CONCEPT_HEADER_TIMEOUT, order 018-a) are
    # separate axes and must not extend reviewer calls (order 014-a,
    # requirement 4).
    reviewer = ResponsesReviewer(
        os.environ.get("CONCEPT_REVIEWER_URL", "http://127.0.0.1:8001/v1"),
        os.environ.get("CONCEPT_REVIEWER_MODEL", "Qwen3.8-27B"),
        timeout=REVIEWER_HTTP_TIMEOUT_SECONDS,
        profile=os.environ.get("CONCEPT_REVIEWER_PROFILE"),
    )
    trace_value = os.environ.get("CONCEPT_TRACE_DIR")
    # Operator-observable separated review usage (order 015-a,
    # requirement 7): wired at the normal runnable entry point, enabled
    # without editing source; observation stays a bounded stderr record.
    usage_observer: Callable[[dict[str, object]], None] | None = None
    if os.environ.get("CONCEPT_USAGE_OBSERVER") == "stderr":
        usage_observer = _stderr_usage_observer
    # One elapsed incoming-intake budget (order 020-a, requirement
    # 1): independent of CONCEPT_TIMEOUT (socket/body capture),
    # CONCEPT_HEADER_TIMEOUT (response-header axis) and the fixed 15 s
    # reviewer exchange.  Forwarded only when the operator explicitly
    # configures CONCEPT_REQUEST_TIMEOUT; otherwise the real
    # constructor's named CLIENT_REQUEST_TIMEOUT_SECONDS default (30 s)
    # governs, keeping pre-020 constructor adapters compatible at
    # their defaults while the real constructor always validates and
    # sets the bounded 30 s default when unconfigured.
    intake_kwargs: _IntakeKwargs = {}
    if os.environ.get("CONCEPT_REQUEST_TIMEOUT") is not None:
        intake_kwargs["client_timeout"] = float(
            os.environ["CONCEPT_REQUEST_TIMEOUT"]
        )
    # One elapsed final-delivery budget (order 021-a, requirement
    # 1): independent of CONCEPT_TIMEOUT (socket/body capture),
    # CONCEPT_HEADER_TIMEOUT (response-header axis),
    # CONCEPT_REQUEST_TIMEOUT (incoming-intake axis) and the fixed 15 s
    # reviewer exchange.  Forwarded only when the operator explicitly
    # configures CONCEPT_DELIVERY_TIMEOUT; otherwise the real
    # constructor's named CLIENT_DELIVERY_TIMEOUT_SECONDS default
    # (30 s) governs, keeping pre-021 constructor adapters compatible
    # at their defaults while the real constructor always validates
    # and sets the bounded 30 s default when unconfigured.
    if os.environ.get("CONCEPT_DELIVERY_TIMEOUT") is not None:
        intake_kwargs["delivery_timeout"] = float(
            os.environ["CONCEPT_DELIVERY_TIMEOUT"]
        )
    # One elapsed main-upstream setup budget (order 022-a,
    # requirement 1): independent of CONCEPT_TIMEOUT (socket/body
    # capture), CONCEPT_HEADER_TIMEOUT (response-header axis),
    # CONCEPT_REQUEST_TIMEOUT (incoming-intake axis),
    # CONCEPT_DELIVERY_TIMEOUT (outgoing-delivery axis) and the fixed
    # 15 s reviewer exchange.  Forwarded only when the operator
    # explicitly configures CONCEPT_SETUP_TIMEOUT; otherwise the real
    # constructor's named MAIN_SETUP_TIMEOUT_SECONDS default (30 s)
    # governs, keeping pre-022 constructor adapters compatible at
    # their defaults while the real constructor always validates and
    # sets the bounded 30 s default when unconfigured.
    if os.environ.get("CONCEPT_SETUP_TIMEOUT") is not None:
        intake_kwargs["setup_timeout"] = float(
            os.environ["CONCEPT_SETUP_TIMEOUT"]
        )
    proxy = ConceptProxy(
        ("127.0.0.1", 18024),
        upstream,
        RepairEngine(Path(index), reviewer, pandoc=pandoc_spec),
        header_timeout=float(
            os.environ.get(
                "CONCEPT_HEADER_TIMEOUT", str(MAIN_HEADER_TIMEOUT_SECONDS)
            )
        ),
        timeout=float(os.environ.get("CONCEPT_TIMEOUT", "30")),
        trace_dir=Path(trace_value) if trace_value else None,
        usage_observer=usage_observer,
        **intake_kwargs,
    )
    proxy.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
