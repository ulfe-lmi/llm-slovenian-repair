"""The pre-English historical pipeline families.

The preserved experiments did not share one evolving pipeline.  In particular,
the early retry and hyphen studies selected candidates without the later English
preservation policy.  These small drivers keep that boundary explicit while
sharing only the byte-safe detector, gate, and patch primitives.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from . import detector as raw_detector
from . import historical_detector as hyphen_detector
from .gating import UnigramIndex, check
from .patching import restore_initial_case
from .protected import protected_intervals
from .review import Proposal


class HistoricalVariantPipeline:
    """Detector/gate bridge for a named pre-English historical family."""

    def __init__(
        self,
        index: str | Path,
        *,
        maximum: int | None,
        threshold: int = 3,
        case_rule: str = "none",
        detector_view: str = "raw",
    ) -> None:
        if case_rule not in {"none", "one-way", "symmetric"}:
            raise ValueError("unknown historical case rule")
        if detector_view not in {"raw", "hyphen-space"}:
            raise ValueError("unknown historical detector view")
        self.maximum = maximum
        self.threshold = threshold
        self.case_rule = case_rule
        self.detector_view = detector_view
        self._detector = raw_detector if detector_view == "raw" else hyphen_detector
        self.unigrams = UnigramIndex(index)
        # Corpus is opened lazily by the real Corpus implementation below.  A
        # separate object is used so the detector retains its frozen n-gram
        # evidence path and the gate retains its separate unigram counter.
        from .corpus import Corpus

        self._corpus = Corpus(index)

    def detect(self, text: str) -> dict[str, Any]:
        intervals = protected_intervals(text)
        candidates = [
            candidate.as_dict()
            for candidate in self._detector.detect(
                text,
                self._corpus,
                intervals,
                mode="local-context",
                threshold=self.threshold,
                maximum=self.maximum,
            )
        ]
        # This is deliberately not English evidence.  It is a recorded
        # no-policy receipt so callers cannot silently substitute a later
        # English lookup or an implicit suppression.
        policies = [
            {
                "original_target": candidate["text"],
                "slovene_unigram": candidate["evidence"]["unigram"],
                "english_frequency": None,
                "english_classification": "NOT_APPLIED_HISTORICAL_POLICY",
                "review_suppressed": False,
                "reason": "historical-family-has-no-english-policy",
                "threshold": None,
            }
            for candidate in candidates
        ]
        return {
            "candidates": candidates,
            "english": policies,
            "eligible_words": len(self._detector.tokenize(text, intervals)),
            "protected_intervals": [interval.__dict__ for interval in intervals],
            "detector_mode": "local-context",
            "detector_view": self.detector_view,
            "threshold": self.threshold,
            "maximum": self.maximum,
            "historical_policy": "none",
        }

    def _adjust_case(self, target: str, proposal: Proposal) -> tuple[Proposal, dict[str, Any]]:
        if self.case_rule == "none":
            return proposal, {
                "eligible_original": False,
                "direction": None,
                "changed": False,
                "raw_replacement": proposal.replacement,
                "adjusted_replacement": proposal.replacement,
                "case_rule": "none",
            }
        if self.case_rule == "symmetric":
            adjusted, record = restore_initial_case(target, proposal)
            record["case_rule"] = "symmetric"
            return adjusted, record
        # The first hyphen-case experiment only introduced the title-case cap;
        # lowercase targets remained byte-for-byte as proposed.
        replacement = proposal.replacement
        eligible = len(target) >= 2 and target[0].isupper() and target[1].islower()
        changed = bool(eligible and not proposal.keep and not proposal.needs_wider_edit and replacement)
        adjusted_text = replacement
        if changed and isinstance(replacement, str):
            adjusted_text = replacement[0].upper() + replacement[1:]
        return Proposal(proposal.keep, adjusted_text, proposal.needs_wider_edit), {
            "eligible_original": eligible,
            "direction": "upper" if eligible else None,
            "changed": adjusted_text != replacement,
            "raw_replacement": replacement,
            "adjusted_replacement": adjusted_text,
            "case_rule": "one-way",
        }

    def gate(
        self,
        text: str,
        candidate: Mapping[str, Any],
        proposal: Proposal | Mapping[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        if not isinstance(proposal, Proposal):
            proposal = Proposal(
                bool(proposal["keep"]),
                proposal.get("replacement"),
                bool(proposal["needs_wider_edit"]),
            )
        adjusted, case = self._adjust_case(str(candidate["text"]), proposal)
        return adjusted.__dict__, case, check(text, dict(candidate), adjusted, self.unigrams.lookup)

    def close(self) -> None:
        self._corpus.close()
        self.unigrams.close()

    def __enter__(self) -> HistoricalVariantPipeline:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def build_historical_pipeline(
    index: str | Path,
    *,
    maximum: int | None,
    case_rule: str = "none",
    detector_view: str = "raw",
) -> HistoricalVariantPipeline:
    """Build an early-family pipeline with no English lookup side effect."""

    return HistoricalVariantPipeline(
        index,
        maximum=maximum,
        case_rule=case_rule,
        detector_view=detector_view,
    )
