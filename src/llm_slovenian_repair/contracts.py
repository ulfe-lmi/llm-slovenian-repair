"""Typed, side-effect-free contracts for the future repair pipeline.

These models describe data exchanged between future seams.  They deliberately
do not detect errors, call a reviewer, accept edits, or patch text.
"""

from __future__ import annotations

from enum import StrEnum
from math import isfinite
from typing import Annotated, Self

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    field_validator,
    model_validator,
)


class EvidenceState(StrEnum):
    """Whether a corpus measurement is exact, bounded, or unavailable."""

    EXACT = "EXACT"
    CENSORED = "CENSORED"
    UNAVAILABLE = "UNAVAILABLE"


class EvidenceCompleteness(StrEnum):
    """Completeness metadata for a measurement within its stated scope."""

    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


class RepairMode(StrEnum):
    """The finite policy modes reserved for later pipeline work."""

    DETECT_ONLY = "detect_only"
    SHADOW = "shadow"
    STRICT = "strict"
    EXPERIMENTAL = "experimental"


class AcceptanceClass(StrEnum):
    """Finite labels for the authority that accepted an edit proposal."""

    AUTO_REPAIR = "AUTO_REPAIR"
    SHADOW = "SHADOW"
    EXPERIMENTAL = "EXPERIMENTAL"


class RepairDisposition(StrEnum):
    """Finite result outcomes; only ``patched`` may change the text."""

    ORIGINAL = "original"
    SHADOW_ORIGINAL = "shadow-original"
    DEGRADED_ORIGINAL = "degraded-original"
    PATCHED = "patched"


class RepairReason(StrEnum):
    """Finite, non-sensitive reasons for a result disposition."""

    NO_ELIGIBLE_SUSPICION = "no-eligible-suspicion"
    SHADOW_REVIEW = "shadow-review"
    INSUFFICIENT_EVIDENCE = "insufficient-evidence"
    MAIN_CAPTURE_FAILED = "main-capture-failed"
    PATCH_ACCEPTED = "patch-accepted"


NonEmptyString = Annotated[StrictStr, Field(min_length=1)]
Identifier = Annotated[StrictStr, Field(min_length=1, max_length=64)]
NonNegativeInt = Annotated[StrictInt, Field(ge=0)]
PositiveInt = Annotated[StrictInt, Field(gt=0)]
FiniteNonNegativeFloat = Annotated[StrictFloat, Field(ge=0)]


CONTRACT_CONFIG = ConfigDict(
    extra="forbid",
    frozen=True,
    strict=True,
    validate_assignment=True,
    validate_default=True,
    allow_inf_nan=False,
)


def _validate_finite_float(value: float | None) -> float | None:
    if value is not None and not isfinite(value):
        raise ValueError("value must be finite")
    return value


def _validate_text(value: str | None) -> str | None:
    if value is None:
        return value
    if any(ord(character) < 32 or 0x7F <= ord(character) <= 0x9F for character in value):
        raise ValueError("text must not contain control characters")
    return value


class EvidenceRecord(BaseModel):
    """A scoped measurement whose uncertainty is explicit and fail-closed."""

    model_config = CONTRACT_CONFIG

    evidence_id: Identifier
    state: EvidenceState
    source: NonEmptyString
    version: NonEmptyString
    normalization: NonEmptyString
    annotation: NonEmptyString
    scope: NonEmptyString
    unit: NonEmptyString
    completeness: EvidenceCompleteness
    cutoff: NonEmptyString | None = None
    query_complete: StrictBool = False
    lower_bound: NonNegativeInt | None = None
    upper_bound: NonNegativeInt | None = None
    context_denominator: NonNegativeInt | None = None

    @model_validator(mode="after")
    def validate_measurement(self) -> Self:
        bounds = (self.lower_bound, self.upper_bound)
        if (
            self.lower_bound is not None
            and self.upper_bound is not None
            and self.lower_bound > self.upper_bound
        ):
            raise ValueError("lower_bound must not exceed upper_bound")

        if self.context_denominator is not None:
            known_bounds = [bound for bound in bounds if bound is not None]
            if any(bound > self.context_denominator for bound in known_bounds):
                raise ValueError("known numerator bounds exceed context_denominator")

        if self.state is EvidenceState.EXACT:
            if self.completeness is not EvidenceCompleteness.COMPLETE:
                raise ValueError("EXACT evidence must be COMPLETE")
            if self.lower_bound is None or self.upper_bound is None:
                raise ValueError("EXACT evidence requires equal lower and upper bounds")
            if self.lower_bound != self.upper_bound:
                raise ValueError("EXACT evidence requires equal lower and upper bounds")
            if self.lower_bound == 0 and not self.query_complete:
                raise ValueError("EXACT zero requires query_complete=True")
            if self.cutoff is None:
                raise ValueError("EXACT evidence requires cutoff metadata")
        elif self.state is EvidenceState.CENSORED:
            if self.completeness is not EvidenceCompleteness.PARTIAL:
                raise ValueError("CENSORED evidence must be PARTIAL")
            if self.cutoff is None:
                raise ValueError("CENSORED evidence requires cutoff metadata")
            if self.lower_bound is None and self.upper_bound is None:
                raise ValueError("CENSORED evidence requires at least one bound")
            if (
                self.lower_bound is not None
                and self.upper_bound is not None
                and self.lower_bound == self.upper_bound
            ):
                raise ValueError("CENSORED equal bounds would claim an exact count")
            if self.query_complete:
                raise ValueError("CENSORED evidence cannot claim a complete query")
        else:
            if self.completeness is not EvidenceCompleteness.UNKNOWN:
                raise ValueError("UNAVAILABLE evidence must have UNKNOWN completeness")
            if any(value is not None for value in (*bounds, self.cutoff, self.context_denominator)):
                raise ValueError("UNAVAILABLE evidence cannot carry counts or cutoff")
            if self.query_complete:
                raise ValueError("UNAVAILABLE evidence cannot claim query completeness")
        return self


class SpanSelection(BaseModel):
    """A CPU-selected, original-coordinate Unicode code-point span."""

    model_config = CONTRACT_CONFIG

    span_id: Identifier
    start: NonNegativeInt
    end: PositiveInt
    original: Annotated[NonEmptyString, Field(max_length=1024)]
    sentence: Annotated[NonEmptyString, Field(max_length=4096)]
    context_before: Annotated[StrictStr, Field(max_length=1024)] = ""
    context_after: Annotated[StrictStr, Field(max_length=1024)] = ""
    evidence_refs: tuple[Identifier, ...] = Field(min_length=1, max_length=16)

    @field_validator("sentence", "context_before", "context_after")
    @classmethod
    def reject_control_text(cls, value: str) -> str:
        return _validate_text(value) or ""

    @model_validator(mode="after")
    def validate_coordinates(self) -> Self:
        if self.end <= self.start:
            raise ValueError("end must be greater than start")
        if self.end - self.start != len(self.original):
            raise ValueError("end - start must equal len(original) in Unicode code points")
        if self.original not in self.sentence:
            raise ValueError("sentence must contain original")
        return self


SelectedSpan = SpanSelection


def _validate_non_overlapping(
    items: tuple[SpanSelection | OriginalCoordinateEdit, ...],
) -> None:
    seen_ids: set[str] = set()
    ordered = sorted(items, key=lambda item: (item.start, item.end))
    for item in ordered:
        if item.span_id in seen_ids:
            raise ValueError("span_id values must be unique")
        seen_ids.add(item.span_id)
    for previous, current in zip(ordered, ordered[1:], strict=False):
        if current.start < previous.end:
            raise ValueError("spans must not overlap")


class SelectionBatch(BaseModel):
    """Selections bound to one immutable original string."""

    model_config = CONTRACT_CONFIG | ConfigDict(populate_by_name=True)

    original_text: StrictStr
    spans: tuple[SpanSelection, ...] = Field(
        default_factory=tuple,
        validation_alias=AliasChoices("spans", "selections"),
        serialization_alias="spans",
        max_length=8,
    )

    @model_validator(mode="after")
    def validate_original_binding(self) -> Self:
        _validate_non_overlapping(self.spans)
        for span in self.spans:
            if span.end > len(self.original_text):
                raise ValueError("span is outside original_text")
            if self.original_text[span.start : span.end] != span.original:
                raise ValueError("span original does not match original_text slice")
        return self


class ReviewProposal(BaseModel):
    """One untrusted, narrow proposal from a future isolated reviewer."""

    model_config = CONTRACT_CONFIG

    span_id: Identifier
    keep: StrictBool
    replacement: StrictStr | None = None
    needs_wider_edit: StrictBool = False
    confidence: Annotated[StrictFloat, Field(ge=0, le=1)] | None = None

    _finite_confidence = field_validator("confidence")(_validate_finite_float)

    @field_validator("replacement")
    @classmethod
    def validate_replacement_text(cls, value: str | None) -> str | None:
        if value is not None:
            if not value.strip():
                raise ValueError("replacement must be nonblank")
            _validate_text(value)
        return value

    @model_validator(mode="after")
    def validate_relationship(self) -> Self:
        if self.needs_wider_edit:
            if not self.keep or self.replacement is not None:
                raise ValueError("wider edits must keep the target with null replacement")
        elif self.keep:
            if self.replacement is not None:
                raise ValueError("keep proposals require null replacement")
        elif self.replacement is None:
            raise ValueError("replace proposals require a replacement")
        return self


class ReviewProposalBatch(BaseModel):
    """A bounded proposal list with unique response-local IDs."""

    model_config = CONTRACT_CONFIG | ConfigDict(populate_by_name=True)

    proposals: tuple[ReviewProposal, ...] = Field(
        default_factory=tuple,
        validation_alias=AliasChoices("proposals", "reviews"),
        serialization_alias="proposals",
        max_length=8,
    )

    @model_validator(mode="after")
    def validate_unique_ids(self) -> Self:
        ids = [proposal.span_id for proposal in self.proposals]
        if len(ids) != len(set(ids)):
            raise ValueError("review span_id values must be unique")
        return self


class OriginalCoordinateEdit(BaseModel):
    """An accepted replacement anchored to an exact original-coordinate slice."""

    model_config = CONTRACT_CONFIG | ConfigDict(populate_by_name=True)

    span_id: Identifier
    start: NonNegativeInt
    end: PositiveInt
    original: Annotated[NonEmptyString, Field(max_length=1024)]
    replacement: Annotated[NonEmptyString, Field(max_length=2048)]
    acceptance_class: AcceptanceClass = Field(
        validation_alias=AliasChoices("acceptance_class", "acceptance"),
        serialization_alias="acceptance_class",
    )

    @field_validator("replacement")
    @classmethod
    def validate_edit_text(cls, value: str) -> str:
        if value == "":
            raise ValueError("replacement must be nonempty")
        _validate_text(value)
        return value

    @model_validator(mode="after")
    def validate_edit(self) -> Self:
        if self.end <= self.start:
            raise ValueError("end must be greater than start")
        if self.end - self.start != len(self.original):
            raise ValueError("end - start must equal len(original)")
        if self.original == self.replacement:
            raise ValueError("identity replacements are not edits")
        return self


class StageTimings(BaseModel):
    """Finite nonnegative timings recorded by a future request-local pipeline."""

    model_config = CONTRACT_CONFIG

    capture_seconds: FiniteNonNegativeFloat = 0.0
    analysis_seconds: FiniteNonNegativeFloat = 0.0
    review_seconds: FiniteNonNegativeFloat = 0.0
    patch_seconds: FiniteNonNegativeFloat = 0.0
    total_seconds: FiniteNonNegativeFloat = 0.0

    _finite_timings = field_validator(
        "capture_seconds",
        "analysis_seconds",
        "review_seconds",
        "patch_seconds",
        "total_seconds",
    )(_validate_finite_float)


class RepairResult(BaseModel):
    """The immutable-original result envelope for one future repair request."""

    model_config = CONTRACT_CONFIG | ConfigDict(populate_by_name=True)

    original_text: StrictStr
    final_text: StrictStr
    changed: StrictBool
    disposition: RepairDisposition
    reason: RepairReason
    selected_spans: tuple[SpanSelection, ...] = Field(
        default_factory=tuple,
        validation_alias=AliasChoices("selected_spans", "spans"),
        serialization_alias="selected_spans",
        max_length=8,
    )
    reviews: tuple[ReviewProposal, ...] = Field(default_factory=tuple, max_length=8)
    edits: tuple[OriginalCoordinateEdit, ...] = Field(default_factory=tuple, max_length=8)
    review_call_count: Annotated[StrictInt, Field(ge=0, le=1)] = Field(
        default=0,
        validation_alias=AliasChoices("review_call_count", "review_calls"),
        serialization_alias="review_call_count",
    )
    timings: StageTimings = Field(
        default_factory=StageTimings,
        validation_alias=AliasChoices("timings", "stage_timings"),
        serialization_alias="timings",
    )

    @model_validator(mode="after")
    def validate_result(self) -> Self:
        _validate_non_overlapping(self.selected_spans)
        _validate_non_overlapping(self.edits)
        for span in self.selected_spans:
            if span.end > len(self.original_text):
                raise ValueError("selected span is outside original_text")
            if self.original_text[span.start : span.end] != span.original:
                raise ValueError("selected span does not match original_text")
        for edit in self.edits:
            if edit.end > len(self.original_text):
                raise ValueError("edit is outside original_text")
            if self.original_text[edit.start : edit.end] != edit.original:
                raise ValueError("edit does not match original_text slice")
        if self.changed:
            if self.final_text == self.original_text:
                raise ValueError("changed results require different final_text")
            if not self.edits or self.disposition is not RepairDisposition.PATCHED:
                raise ValueError("changed results require edits and patched disposition")
        else:
            if self.final_text != self.original_text:
                raise ValueError("unchanged results require equal original and final text")
            if self.edits:
                raise ValueError("unchanged results cannot contain edits")
            if self.disposition is RepairDisposition.PATCHED:
                raise ValueError("patched disposition requires changed=True")
        return self


# Public aliases keep the vocabulary readable at both the span and result seams.
RepairSpan = SpanSelection
Edit = OriginalCoordinateEdit
PolicyMode = RepairMode


__all__ = [
    "AcceptanceClass",
    "Edit",
    "EvidenceCompleteness",
    "EvidenceRecord",
    "EvidenceState",
    "OriginalCoordinateEdit",
    "RepairDisposition",
    "RepairMode",
    "RepairReason",
    "RepairResult",
    "RepairSpan",
    "ReviewProposal",
    "ReviewProposalBatch",
    "SelectedSpan",
    "SelectionBatch",
    "SpanSelection",
    "StageTimings",
]
