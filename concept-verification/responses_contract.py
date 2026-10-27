"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Request contract.

Pure, bounded validation of the explicit text Responses request contract
(order 015-a, requirement 2) and of completed main envelopes (requirement
4).  The module is content-free: every rejection carries a fixed label and
never echoes field names or values.  It performs no transport, no corpus
access and no mutation.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass

from config import (
    API_MAX_INPUT_CODEPOINTS,
    API_MAX_MESSAGE_PARTS,
    API_MAX_MESSAGES,
    API_MAX_METADATA_KEY_CODEPOINTS,
    API_MAX_METADATA_KEYS,
    API_MAX_METADATA_VALUE_CODEPOINTS,
    API_MAX_MODEL_CODEPOINTS,
    API_MAX_OUTPUT_TOKENS,
    API_MAX_STOP_SEQUENCE_CODEPOINTS,
    API_MAX_STOP_SEQUENCES,
    API_MAX_TOP_K,
)

# Closed-set rejection labels (requirement 2).  They are the only values
# that may appear in the bounded 400 body; untrusted request content is
# never stringified into them.
REQUEST_INVALID_JSON = "REQUEST_INVALID_JSON"
REQUEST_DUPLICATE_KEY = "REQUEST_DUPLICATE_KEY"
REQUEST_INVALID_NUMBER = "REQUEST_INVALID_NUMBER"
REQUEST_SCHEMA = "REQUEST_SCHEMA"
REQUEST_STORE_REQUIRED = "REQUEST_STORE_REQUIRED"
REQUEST_UNSUPPORTED = "REQUEST_UNSUPPORTED"

#: Client roles accepted in a client-managed text message sequence.
REQUEST_ROLES = frozenset({"user", "assistant", "system", "developer"})

#: Supported ordinary generation fields (exact types, finite values).
_OPTIONAL_FIELDS = frozenset(
    {"temperature", "top_p", "top_k", "max_output_tokens", "stop", "metadata"}
)


class RequestContractError(ValueError):
    """Bounded rejection of a proxy request; ``reason`` is a fixed label."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class RequestContract:
    """The validated declared mode of one supported request."""

    model: str
    stream: bool


def _strict_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            # Duplicate keys are rejected, never collapsed last-wins.
            raise RequestContractError(REQUEST_DUPLICATE_KEY)
        value[key] = item
    return value


def _strict_constant(_name: str) -> object:
    # NaN/Infinity are nonfinite numbers: rejected, not accepted.
    raise RequestContractError(REQUEST_INVALID_NUMBER)


def _strict_float(text: str) -> float:
    # A numeric literal that overflows to infinity (e.g. 1e999) is a
    # nonfinite number too: rejected, not silently accepted as inf.
    number = float(text)
    if not math.isfinite(number):
        raise RequestContractError(REQUEST_INVALID_NUMBER)
    return number


def _valid_stop(value: object) -> bool:
    if type(value) is str:
        return 1 <= len(value) <= API_MAX_STOP_SEQUENCE_CODEPOINTS
    return (
        isinstance(value, list)
        and 1 <= len(value) <= API_MAX_STOP_SEQUENCES
        and all(
            type(item) is str and 1 <= len(item) <= API_MAX_STOP_SEQUENCE_CODEPOINTS
            for item in value
        )
    )


def _valid_metadata(value: object) -> bool:
    if not isinstance(value, dict) or len(value) > API_MAX_METADATA_KEYS:
        return False
    for key, item in value.items():
        if (
            type(key) is not str
            or not (1 <= len(key) <= API_MAX_METADATA_KEY_CODEPOINTS)
            or type(item) is not str
            or len(item) > API_MAX_METADATA_VALUE_CODEPOINTS
        ):
            return False
    return True


def _valid_optional_field(key: str, value: object) -> bool:
    if key in ("temperature", "top_p"):
        # Exact type guard first: bool is not a number here, and an int is
        # finite by construction - never convert an arbitrary big int to
        # float (that conversion itself may overflow).
        if type(value) is bool:
            return False
        if type(value) is int:
            finite = True
        elif type(value) is float:
            finite = math.isfinite(value)
        else:
            return False
        if not finite:
            return False
        if key == "temperature":
            return 0 <= value <= 2
        return 0 < value <= 1
    if key == "top_k":
        return type(value) is int and 0 <= value <= API_MAX_TOP_K
    if key == "max_output_tokens":
        return type(value) is int and 1 <= value <= API_MAX_OUTPUT_TOKENS
    if key == "stop":
        return _valid_stop(value)
    if key == "metadata":
        return _valid_metadata(value)
    return False


def _valid_message(message: object) -> bool:
    if not isinstance(message, dict) or set(message) != {"role", "content"}:
        return False
    if type(message["role"]) is not str or message["role"] not in REQUEST_ROLES:
        return False
    content = message["content"]
    if type(content) is str:
        return 1 <= len(content) <= API_MAX_INPUT_CODEPOINTS
    if not isinstance(content, list) or not (1 <= len(content) <= API_MAX_MESSAGE_PARTS):
        return False
    for part in content:
        if (
            not isinstance(part, dict)
            or set(part) != {"type", "text"}
            or part["type"] != "input_text"
            or type(part["text"]) is not str
            or not (1 <= len(part["text"]) <= API_MAX_INPUT_CODEPOINTS)
        ):
            return False
    return True


def _valid_input(value: object) -> bool:
    if type(value) is str:
        return 1 <= len(value) <= API_MAX_INPUT_CODEPOINTS
    return (
        isinstance(value, list)
        and 1 <= len(value) <= API_MAX_MESSAGES
        and all(_valid_message(message) for message in value)
    )


def validate_request(body: bytes) -> RequestContract:
    """Validate one explicit text Responses request before forwarding.

    Accepts a strict JSON object with a nonempty bounded ``model``, text
    input as a string or a client-managed text-only message sequence, an
    explicit ``store: false`` and a boolean ``stream`` flag (absent means
    false), plus the allowlisted ordinary generation fields with exact
    types and finite values.  Any other key is an unsupported capability
    and is rejected regardless of its value (an empty capability list is
    not a supported shape).  Invalid UTF-8/JSON, duplicate keys,
    nonfinite numbers and type mismatches are rejected with the closed
    label set, before any upstream or reviewer call.
    """
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RequestContractError(REQUEST_INVALID_JSON) from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_strict_pairs,
            parse_constant=_strict_constant,
            parse_float=_strict_float,
        )
    except RequestContractError:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise RequestContractError(REQUEST_INVALID_JSON) from exc
    if not isinstance(value, dict):
        raise RequestContractError(REQUEST_INVALID_JSON)
    model = value.get("model")
    if type(model) is not str or not model or len(model) > API_MAX_MODEL_CODEPOINTS:
        raise RequestContractError(REQUEST_SCHEMA)
    if not _valid_input(value.get("input")):
        raise RequestContractError(REQUEST_SCHEMA)
    if "store" not in value:
        # store:false is required explicitly, never assumed.
        raise RequestContractError(REQUEST_STORE_REQUIRED)
    if value["store"] is not False:
        # Server storage is a capability this contract does not support.
        raise RequestContractError(REQUEST_UNSUPPORTED)
    stream = value.get("stream", False)
    if type(stream) is not bool:
        raise RequestContractError(REQUEST_SCHEMA)
    for key, item in value.items():
        if key in ("model", "input", "store", "stream"):
            continue
        if key not in _OPTIONAL_FIELDS or not _valid_optional_field(key, item):
            raise RequestContractError(
                REQUEST_SCHEMA if key in _OPTIONAL_FIELDS else REQUEST_UNSUPPORTED
            )
    return RequestContract(model=model, stream=stream)


def aligned_metadata_clean(value: dict[str, object]) -> bool:
    """Recognized aligned metadata beside an editable answer.

    ``annotations``/``logprobs`` must be absent or an empty list: a
    non-empty (or non-list) aligned list is stale data a changed answer
    can never retain, and a non-list shape is not a recognized aligned
    field (order 015-a, requirement 5).  Only the explicitly named
    answer-shaped representations are checked; metadata echoes are never
    scanned.
    """
    for key in ("annotations", "logprobs"):
        if key in value:
            item = value[key]
            if not isinstance(item, list) or item:
                return False
    return True


def stateless_declarations_clean(response: dict[str, object]) -> bool:
    """Pinned completed/stateless/foreground declaration policy.

    A completed envelope that explicitly declares stored generation
    (``store: true``), background generation (``background: true``),
    response linkage (a non-null ``previous_response_id`` or
    ``conversation``) or incompleteness details (a non-null
    ``incomplete_details``) contradicts the supported stateless
    foreground text profile and must abstain raw unchanged with zero
    review calls (order 015-a, requirements 2, 4 and 5; ARCH13).  The
    typed unset policy is: absent or null values are unset; present
    ``store``/``background`` accept only the exact boolean ``false``;
    nothing is coerced and protected metadata echoes are never scanned.
    """
    for key in ("store", "background"):
        if response.get(key) is not None and response[key] is not False:
            return False
    for key in ("previous_response_id", "conversation", "incomplete_details"):
        if response.get(key) is not None:
            return False
    return True


def _usage_int(value: object) -> int | None:
    # bool is not an int here.
    return value if type(value) is int and value >= 0 else None


def strict_reviewer_usage(value: object) -> tuple[int, int, int] | None:
    """Actual reviewer usage, or ``None`` when absent/invalid (unknown).

    Pinned policy (order 015-a, requirement 7): the three common token
    count keys must each be a nonnegative int (bool is not an int here);
    the documented detailed shape carries additional breakdown fields
    (``input_tokens_details``/``output_tokens_details``) which are
    tolerated as opaque extras and never parsed.  Missing, unavailable or
    invalid counts stay explicitly unknown, never zero.
    """
    if not isinstance(value, dict):
        return None
    tokens: list[int] = []
    for key in ("input_tokens", "output_tokens", "total_tokens"):
        item = _usage_int(value.get(key))
        if item is None:
            return None
        tokens.append(item)
    return (tokens[0], tokens[1], tokens[2])


def validate_completed_envelope(envelope: object) -> tuple[str, dict[str, object]] | None:
    """Return ``(answer_text, answer_part)`` for one unambiguous answer.

    A supported main envelope is a documented Responses object
    (``object == "response"``) with exactly ``status == "completed"``, an
    absent/null ``error`` and no explicit stored/background/linkage/
    incompleteness declarations, at most one recognized noneditable
    reasoning item preceding exactly one assistant message with an exact
    typed nonempty id, exactly ``status == "completed"``, and exactly one
    plain nonempty ``output_text`` part carrying no non-empty aligned
    metadata.  Missing/null status is pinned as not repairable;
    contradictory or incomplete markers, unknown output variants,
    tools/refusals, extra answer parts and malformed identity never
    permit repair.  The
    returned part is the single editable reference.  ``None`` means the
    envelope must pass through unchanged with zero calls (its original
    status/finish/error semantics are retained by the caller).
    """
    if not isinstance(envelope, dict):
        return None
    if envelope.get("object") != "response":
        return None
    if envelope.get("status") != "completed":
        return None
    if "error" in envelope and envelope["error"] is not None:
        return None
    if not stateless_declarations_clean(envelope):
        return None
    output = envelope.get("output")
    if not isinstance(output, list):
        return None
    seen_reasoning = False
    message: dict[str, object] | None = None
    for item in output:
        if not isinstance(item, dict):
            return None
        item_type = item.get("type")
        if item_type == "reasoning":
            # Bounded recognized noneditable bookkeeping: its summary and
            # content are never parsed into edits; an explicit
            # incomplete/in_progress (or any non-completed) marker is
            # contradictory and abstains.
            if seen_reasoning or message is not None:
                return None
            status = item.get("status")
            if status is not None and status != "completed":
                return None
            seen_reasoning = True
        elif item_type == "message":
            if message is not None:
                return None
            message = item
        else:
            return None
    if message is None:
        return None
    if message.get("role") != "assistant":
        return None
    if message.get("status") != "completed":
        return None
    message_id = message.get("id")
    if type(message_id) is not str or not message_id:
        return None
    content = message.get("content")
    if not isinstance(content, list) or len(content) != 1:
        return None
    part = content[0]
    if (
        not isinstance(part, dict)
        or part.get("type") != "output_text"
        or type(part.get("text")) is not str
        or not part["text"]
    ):
        return None
    if not aligned_metadata_clean(part):
        return None
    # Main-generation usage is accounting, not completion: absent, null,
    # partial or invalid counts stay exactly as reported (observed as
    # unknown) and never suppress an otherwise valid completed answer
    # (order 015-a, requirement 7).
    return str(part["text"]), part
