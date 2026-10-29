"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Analysis policy."""

from __future__ import annotations

import config

# Fixed content-free analysis-bypass reason vocabulary (order 025-a,
# requirement 4).  A bypass is neither a Pandoc/protection error nor
# an evidence failure: the completed original is safely captured and
# the OPTIONAL analysis pass (detection, evidence lookup, review) is
# simply not run.  The labels never carry answer, path, value, target
# or credential text.
ANALYSIS_SIZE_EXCEEDED = "ANALYSIS_SIZE_EXCEEDED"
ANALYSIS_POLICY_INVALID = "ANALYSIS_POLICY_INVALID"
ANALYSIS_ENCODING_INVALID = "ANALYSIS_ENCODING_INVALID"


def validate_limits(codepoints: object, utf8_bytes: object) -> None:
    """Pure validation of one explicit policy pair.

    Raises plain ValueError; no file, model, network or index work.
    The byte allowance must be at least the codepoint allowance
    (order 025-a, requirement 1).
    """
    # Exact positive int only: bool, float (including nonfinite),
    # string, None, zero and negative values are rejected with plain
    # ValueError and no coercion (order 025-a, requirement 1).
    if type(codepoints) is not int or codepoints <= 0:
        raise ValueError(
            "RUNTIME_ANALYSIS_MAX_CODEPOINTS must be an exact positive int"
        )
    if type(utf8_bytes) is not int or utf8_bytes <= 0:
        raise ValueError(
            "RUNTIME_ANALYSIS_MAX_UTF8_BYTES must be an exact positive int"
        )
    if utf8_bytes < codepoints:
        raise ValueError(
            "RUNTIME_ANALYSIS_MAX_UTF8_BYTES must be at least "
            "RUNTIME_ANALYSIS_MAX_CODEPOINTS"
        )


def current_limits() -> tuple[int, int]:
    """Pure validation of the CURRENT config default policy.

    Reads the config attributes at call time - never an import-time
    copy and no global usage state - and touches no file, model,
    network or index, so the real proxy constructor can require the
    startup policy to hold before any bind allocation (order 025-a,
    requirement 2).
    """
    codepoints = config.RUNTIME_ANALYSIS_MAX_CODEPOINTS
    utf8_bytes = config.RUNTIME_ANALYSIS_MAX_UTF8_BYTES
    validate_limits(codepoints, utf8_bytes)
    return codepoints, utf8_bytes


def classify_original(text: str, codepoints: int, utf8_bytes: int) -> str | None:
    """Classify one ORIGINAL completed answer against explicit limits.

    The exact original codepoint count is checked first, before any
    encoding; otherwise the strict original UTF-8 byte count is
    measured with no NFC, stripping or other transformation
    (order 025-a, requirement 3; A-SPAN-01 original coordinates).
    Exact limit values admit on both axes; exceeding either axis
    never truncates, splits, samples or partially repairs.  Returns
    ``None`` when the answer is admitted, otherwise one fixed
    content-free bypass reason.  Only the declared encoding
    condition (UnicodeEncodeError) is translated; caller control and
    MemoryError propagate untouched (order 025-a, requirement 3).
    """
    if len(text) > codepoints:
        return ANALYSIS_SIZE_EXCEEDED
    try:
        byte_count = len(text.encode("utf-8"))
    except UnicodeEncodeError:
        return ANALYSIS_ENCODING_INVALID
    if byte_count > utf8_bytes:
        return ANALYSIS_SIZE_EXCEEDED
    return None
