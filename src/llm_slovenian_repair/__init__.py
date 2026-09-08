"""Typed contract and bounded-policy seams for the future repair pipeline."""

from importlib import import_module
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

__version__ = "0.0.0"


if TYPE_CHECKING:
    from .contracts import (
        AcceptanceClass,
        ContextDenominatorState,
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
    from .source_manifest import (
        DEFAULT_MAX_MANIFEST_BYTES,
        DEFAULT_MAX_PAYLOAD_BYTES,
        DEFAULT_MAX_RECORDS,
        ManifestDenominatorKnowledge,
        ManifestVerificationError,
        QueryKind,
        RightsStatus,
        SourceManifest,
        SyntheticCorpus,
        SyntheticCountRecord,
        VerificationFailure,
        VerifiedSyntheticCorpus,
        verify_manifest_payload,
    )


_LAZY_EXPORTS = MappingProxyType(
    {
        **{
            name: ("contracts", name)
            for name in (
                "AcceptanceClass",
                "ContextDenominatorState",
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
            )
        },
        **{
            name: ("policy", name)
            for name in ("Policy", "PolicyConfig")
        },
        **{
            name: ("source_manifest", name)
            for name in (
                "DEFAULT_MAX_MANIFEST_BYTES",
                "DEFAULT_MAX_PAYLOAD_BYTES",
                "DEFAULT_MAX_RECORDS",
                "ManifestDenominatorKnowledge",
                "ManifestVerificationError",
                "QueryKind",
                "RightsStatus",
                "SourceManifest",
                "SyntheticCorpus",
                "SyntheticCountRecord",
                "VerificationFailure",
                "VerifiedSyntheticCorpus",
                "verify_manifest_payload",
            )
        },
    }
)


def __getattr__(name: str) -> Any:
    """Resolve documented runtime exports only when they are first accessed."""

    target = _LAZY_EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attribute_name = target
    value = getattr(import_module(f".{module_name}", __name__), attribute_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """List lazy exports without importing their backing modules."""

    return sorted(
        (set(globals()) - {"contracts", "policy", "source_manifest"}) | set(__all__)
    )

__all__ = [
    "__version__",
    "AcceptanceClass",
    "ContextDenominatorState",
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
    "DEFAULT_MAX_MANIFEST_BYTES",
    "DEFAULT_MAX_PAYLOAD_BYTES",
    "DEFAULT_MAX_RECORDS",
    "ManifestDenominatorKnowledge",
    "ManifestVerificationError",
    "QueryKind",
    "RightsStatus",
    "SourceManifest",
    "SyntheticCorpus",
    "SyntheticCountRecord",
    "VerifiedSyntheticCorpus",
    "VerificationFailure",
    "verify_manifest_payload",
]
