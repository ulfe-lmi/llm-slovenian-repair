"""Typed contract and bounded-policy seams for the future repair pipeline."""

__version__ = "0.0.0"

from .contracts import (
    AcceptanceClass,
    Edit,
    EvidenceCompleteness,
    EvidenceRecord,
    EvidenceState,
    OriginalCoordinateEdit,
    RepairDisposition,
    RepairMode,
    RepairReason,
    RepairResult,
    RepairSpan,
    ReviewProposal,
    ReviewProposalBatch,
    SelectedSpan,
    SelectionBatch,
    SpanSelection,
    StageTimings,
)
from .policy import Policy, PolicyConfig

__all__ = [
    "__version__",
    "AcceptanceClass",
    "Edit",
    "EvidenceCompleteness",
    "EvidenceRecord",
    "EvidenceState",
    "OriginalCoordinateEdit",
    "Policy",
    "PolicyConfig",
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
