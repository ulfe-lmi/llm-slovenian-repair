"""Synthetic tests for the typed contract and bounded policy seams."""

from __future__ import annotations

import json
from typing import Any

import pytest
from pydantic import ValidationError

from llm_slovenian_repair import (
    AcceptanceClass,
    EvidenceCompleteness,
    EvidenceRecord,
    EvidenceState,
    OriginalCoordinateEdit,
    PolicyConfig,
    RepairDisposition,
    RepairMode,
    RepairReason,
    RepairResult,
    ReviewProposal,
    ReviewProposalBatch,
    SelectionBatch,
    SpanSelection,
)


def evidence(
    state: EvidenceState = EvidenceState.EXACT,
    *,
    lower: int | None = 4,
    upper: int | None = 4,
    complete: EvidenceCompleteness = EvidenceCompleteness.COMPLETE,
    cutoff: str | None = "synthetic-cutoff",
    query_complete: bool = False,
    denominator: int | None = 20,
) -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id="ev-1",
        state=state,
        source="synthetic-corpus",
        version="v1",
        normalization="NFC",
        annotation="surface-form",
        scope="synthetic sentences",
        unit="occurrences",
        completeness=complete,
        cutoff=cutoff,
        query_complete=query_complete,
        lower_bound=lower,
        upper_bound=upper,
        context_denominator=denominator,
    )


def span(span_id: str = "s-1", start: int = 6, original: str = "é") -> SpanSelection:
    return SpanSelection(
        span_id=span_id,
        start=start,
        end=start + len(original),
        original=original,
        sentence=f"To je {original} primer.",
        context_before="To je ",
        context_after=" primer.",
        evidence_refs=("ev-1",),
    )


def test_public_models_are_frozen_and_round_trip_without_normalizing_unicode() -> None:
    selected = span()
    batch = SelectionBatch(original_text="To je é primer.\r\nEmoji 🧪", spans=(selected,))
    assert batch.original_text[selected.start : selected.end] == "é"
    assert batch.model_validate_json(batch.model_dump_json()) == batch
    with pytest.raises(ValidationError):
        selected.span_id = "changed"


@pytest.mark.parametrize(
    ("bad_start", "bad_original"),
    [(1, "é"), (0, "x"), (0, "éé")],
)
def test_selection_rejects_stale_or_wrong_coordinate_slices(
    bad_start: int, bad_original: str
) -> None:
    selected = span(start=bad_start, original=bad_original)
    with pytest.raises(ValidationError):
        SelectionBatch(original_text="To je é primer.", spans=(selected,))


def test_selection_rejects_duplicate_overlap_and_out_of_bounds() -> None:
    first = span("first", 0, "To")
    second = span("second", 1, "o ")
    with pytest.raises(ValidationError):
        SelectionBatch(original_text="To je To", spans=(first, second))

    duplicate = span("first", 3, "je")
    with pytest.raises(ValidationError):
        SelectionBatch(original_text="To je To", spans=(first, duplicate))

    out_of_bounds = span("out", 20, "x")
    with pytest.raises(ValidationError):
        SelectionBatch(original_text="To je To", spans=(out_of_bounds,))


@pytest.mark.parametrize(
    "kwargs",
    [
        {"state": EvidenceState.EXACT, "lower": 0, "upper": 0, "query_complete": False},
        {"state": EvidenceState.EXACT, "lower": 1, "upper": 2},
        {
            "state": EvidenceState.CENSORED,
            "lower": None,
            "upper": None,
            "complete": EvidenceCompleteness.PARTIAL,
        },
        {
            "state": EvidenceState.CENSORED,
            "lower": 2,
            "upper": 2,
            "complete": EvidenceCompleteness.PARTIAL,
        },
        {
            "state": EvidenceState.UNAVAILABLE,
            "lower": None,
            "upper": None,
            "complete": EvidenceCompleteness.UNKNOWN,
            "cutoff": "should-not-be-counted",
        },
        {"state": EvidenceState.EXACT, "lower": 21, "upper": 21, "denominator": 20},
    ],
)
def test_evidence_rejects_incomplete_or_contradictory_states(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        evidence(**kwargs)  # type: ignore[arg-type]


def test_evidence_accepts_exact_censored_and_unavailable_without_fabricated_zero() -> None:
    assert evidence(query_complete=True, lower=0, upper=0).state is EvidenceState.EXACT
    censored = evidence(
        EvidenceState.CENSORED,
        lower=0,
        upper=4,
        complete=EvidenceCompleteness.PARTIAL,
        query_complete=False,
    )
    unavailable = evidence(
        EvidenceState.UNAVAILABLE,
        lower=None,
        upper=None,
        complete=EvidenceCompleteness.UNKNOWN,
        cutoff=None,
        denominator=None,
    )
    assert censored.upper_bound == 4
    assert unavailable.lower_bound is None and unavailable.context_denominator is None


def test_review_relationships_reject_invalid_proposals_at_validation_boundary() -> None:
    invalid: tuple[dict[str, Any], ...] = (
        {"span_id": "s", "keep": True, "replacement": "x"},
        {"span_id": "s", "keep": False},
        {"span_id": "s", "keep": False, "replacement": " "},
        {"span_id": "s", "keep": True, "needs_wider_edit": True, "replacement": "x"},
        {"span_id": "s", "keep": False, "needs_wider_edit": True},
        {"span_id": "s", "keep": True, "confidence": float("nan")},
    )
    for data in invalid:
        with pytest.raises(ValidationError):
            ReviewProposal(**data)

    with pytest.raises(ValidationError):
        ReviewProposalBatch(
            proposals=(
                ReviewProposal(span_id="s", keep=True),
                ReviewProposal(span_id="s", keep=True),
            )
        )


def test_review_relationships_accept_keep_replace_and_wider_edit() -> None:
    assert ReviewProposal(span_id="keep", keep=True).replacement is None
    replacement = ReviewProposal(span_id="replace", keep=False, replacement="druga")
    assert replacement.needs_wider_edit is False
    wider = ReviewProposal(span_id="wider", keep=True, needs_wider_edit=True)
    assert wider.replacement is None


def test_edits_and_results_reject_identity_bad_slice_and_inconsistent_flags() -> None:
    with pytest.raises(ValidationError):
        OriginalCoordinateEdit(
            span_id="s",
            start=0,
            end=2,
            original="To",
            replacement="To",
            acceptance_class=AcceptanceClass.AUTO_REPAIR,
        )
    edit = OriginalCoordinateEdit(
        span_id="s",
        start=0,
        end=2,
        original="To",
        replacement="To!",
        acceptance_class=AcceptanceClass.AUTO_REPAIR,
    )
    with pytest.raises(ValidationError):
        RepairResult(
            original_text="To",
            final_text="To!",
            changed=False,
            disposition=RepairDisposition.ORIGINAL,
            reason=RepairReason.PATCH_ACCEPTED,
            edits=(edit,),
        )
    bad_coordinate_edit = OriginalCoordinateEdit(
        span_id="bad",
        start=1,
        end=3,
        original="To",
        replacement="x",
        acceptance_class=AcceptanceClass.AUTO_REPAIR,
    )
    with pytest.raises(ValidationError):
        RepairResult(
            original_text="To",
            final_text="Tx",
            changed=True,
            disposition=RepairDisposition.PATCHED,
            reason=RepairReason.PATCH_ACCEPTED,
            edits=(bad_coordinate_edit,),
        )
    result = RepairResult(
        original_text="To",
        final_text="To!",
        changed=True,
        disposition=RepairDisposition.PATCHED,
        reason=RepairReason.PATCH_ACCEPTED,
        edits=(edit,),
    )
    assert result.changed is True


def test_result_validates_original_coordinates_and_outcomes() -> None:
    edit = OriginalCoordinateEdit(
        span_id="s",
        start=0,
        end=2,
        original="To",
        replacement="To!",
        acceptance_class=AcceptanceClass.AUTO_REPAIR,
    )
    patched = RepairResult(
        original_text="To",
        final_text="To!",
        changed=True,
        disposition=RepairDisposition.PATCHED,
        reason=RepairReason.PATCH_ACCEPTED,
        edits=(edit,),
        review_call_count=1,
    )
    assert patched.model_validate_json(json.dumps(patched.model_dump(mode="json"))) == patched


def test_policy_defaults_and_architectural_limits() -> None:
    policy = PolicyConfig()
    assert policy.schema_version == 1
    assert policy.mode is RepairMode.DETECT_ONLY
    assert policy.max_automatic_retries == 0
    assert policy.allow_evidence_insufficient_acceptance is False
    assert policy.persist_production_text is False

    invalid_overrides: tuple[tuple[str, Any], ...] = (
        ("max_review_requests", 2),
        ("max_generative_passes", 2),
        ("max_automatic_retries", 1),
        ("max_concurrent_reviews", 2),
        ("max_targets", 9),
        ("max_target_words", 7),
        ("max_replacement_words", 9),
        ("allow_evidence_insufficient_acceptance", True),
        ("persist_production_text", True),
    )
    for field, value in invalid_overrides:
        with pytest.raises(ValidationError):
            PolicyConfig(**{field: value})


@pytest.mark.parametrize(
    "override",
    [
        {"mode": RepairMode.EXPERIMENTAL},
        {"max_target_bytes": 1},
        {"max_analysis_code_points": 40_000},
        {"max_prompt_code_points": 1},
        {"max_review_duration_seconds": 1.0},
        {"max_queue_wait_seconds": float("inf")},
    ],
)
def test_policy_rejects_nonfinite_or_contradictory_bounds(override: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        PolicyConfig(**override)
