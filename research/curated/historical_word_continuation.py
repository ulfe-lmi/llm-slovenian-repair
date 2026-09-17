"""Copied whitespace-only continuation: reuse first response, call only pending request."""

from __future__ import annotations

import copy
from typing import Any

from .historical_transport import Client, _parse_word


def parse_word(response: dict[str, Any]):
    value = copy.deepcopy(response)
    for item in value.get("output", []):
        if isinstance(item, dict) and item.get("type") == "message" and item.get("role") == "assistant":
            for part in item.get("content", []):
                if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str):
                    part["text"] = part["text"].strip(" \t\r\n")
    return _parse_word(value)


def continue_saved(first_response: dict[str, Any], pending_item: dict[str, Any], client: Client, output_root: str) -> dict[str, Any]:
    """Preserve the strict-parser failure and make exactly one pending call."""
    first = parse_word(first_response)
    second = client.call(output_root, pending_item["request_body"], "word-only-retry")
    return {"initial_execution_status": "STOPPED_ON_OUTER_WHITESPACE", "first_response_reused": True,
            "first_proposal": first.__dict__, "pending_observation": second,
            "new_calls_in_continuation": 1, "model_calls": client.network_calls}
