"""Structural lint for the 009-a preregistration (order scope item 6).

Data-free, CPU-only, offline: asserts that the committed
``research/target-distribution/PROTOCOL-009.md`` carries every pre-registered
element marker and that ``research/target-distribution/DEPLOYMENT-IDENTITY-009.md``
carries the E2 decision-package markers.

Positive: all markers present at the tested head (the committed bytes).
Negative (tamper): the marker checker fails when ANY marker is removed -
exercised in-memory against a whitespace-normalized copy, so the committed
bytes are never touched.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = REPO_ROOT / "research" / "target-distribution" / "PROTOCOL-009.md"
DEPLOYMENT = REPO_ROOT / "research" / "target-distribution" / "DEPLOYMENT-IDENTITY-009.md"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def missing_markers(text: str, markers) -> list:
    flat = normalize(text)
    return [m for m in markers if normalize(m) not in flat]


# --------------------------------------------------------------------------- #
# Pre-registered element markers, PROTOCOL-009.md                             #
# --------------------------------------------------------------------------- #

TARGET_HARD_GATE = "TARGET DEPLOYMENT HARD GATE"
COLLECTION_PROCEDURE = "COLLECTION PROCEDURE"
DOMAIN_MIX = "DOMAIN MIX"
STAGE_SIZES = "STAGE SIZES AND EXPANSION CRITERIA"
CONTROLS_QUOTA = "CONTROLS QUOTA"
ADJUDICATION_PROCEDURE = "ADJUDICATION PROCEDURE"
SPLIT_RULE = "SPLIT RULE"
UNCERTAINTY_RULES = "UNCERTAINTY RULES"
STOPPING_RULES_HEADER = "STOPPING RULES (pre-registered, all four)"
FAILURE_DECOMPOSITION = "FAILURE DECOMPOSITION"
NO_TUNING_AFTER_UNBLINDING = "NO-TUNING-AFTER-UNBLINDING RULE"
CALIBRATION_TARGETS_NOT_RELEASE = (
    "EVALUATION/CALIBRATION TARGETS, NOT AUTOMATIC RELEASE AUTHORIZATION"
)

TAXONOMY_LABELS = [
    "ACTUAL_ERROR",
    "ACCEPTABLE_UNCHANGED",
    "FULLY_CORRECT_DOCUMENT",
    "NEEDS_WIDER_EDIT",
    "CORRECTS_ERROR",
    "ACCEPTABLE_ALTERNATIVE",
    "HARMLESS_STYLISTIC",
    "HARMFUL_CHANGE",
    "NO_CHANGE",
    "PROTECTION_FAILURE",
    "DETECTOR_MISS",
    "CANDIDATE_GENERATION_MISS",
    "RANKING_MISS",
    "VALIDATOR_REJECTION_OR_FAILURE",
    "ACCEPTANCE_POLICY_REJECTION",
    "PATCH_FAILURE",
]

COMPARATORS = [
    "ORIGINAL",
    "DETECTOR_ONLY",
    "DIRECT_QWEN_PROOFREADING",
    "FROZEN_RESTRICTED_METHOD",
    "CORPUS_ONLY",
]

METRIC_FAMILIES = [
    "Accepted-repair correctness = CORRECTS_ERROR edits / all assessed accepted edits",
    "Harmful interventions per 10,000 originally-correct words = 10000 x",
    "detector coverage = genuine errors flagged / all genuine errors",
    "final-repair coverage = genuine errors finally repaired as CORRECTS_ERROR / all genuine errors",
    "Stylistic-only rate = (ACCEPTABLE_ALTERNATIVE + HARMLESS_STYLISTIC) assessed edits / all assessed accepted edits",
    "Preservation: unchanged-correct-document rate over FULLY_CORRECT controls",
    "Operational cost: review-call rate",
]

STOPPING_RULES = [
    "STOP AND REPORT if accepted-repair correctness falls materially below the approximately 99 percent goal",
    "one-sided 95 percent lower bound of the harmful rate exceeds 1 per 10,000 originally-correct words",
    "coverage limitation with the measured benefit/harm statement",
    "more than 5 percent of attempts as distinct conservative failures",
]

FAILURE_STAGE_ORDER = (
    "PROTECTION_LAYER -> DETECTOR -> CANDIDATE_GENERATION -> RANKING -> "
    "VALIDATOR -> ACCEPTANCE_POLICY -> PATCH"
)

PROTOCOL_MARKERS = [
    TARGET_HARD_GATE,
    COLLECTION_PROCEDURE,
    DOMAIN_MIX,
    STAGE_SIZES,
    CONTROLS_QUOTA,
    ADJUDICATION_PROCEDURE,
    SPLIT_RULE,
    UNCERTAINTY_RULES,
    STOPPING_RULES_HEADER,
    FAILURE_DECOMPOSITION,
    NO_TUNING_AFTER_UNBLINDING,
    CALIBRATION_TARGETS_NOT_RELEASE,
    FAILURE_STAGE_ORDER,
    *TAXONOMY_LABELS,
    *COMPARATORS,
    *METRIC_FAMILIES,
    *STOPPING_RULES,
]

# --------------------------------------------------------------------------- #
# E2 decision-package markers, DEPLOYMENT-IDENTITY-009.md                     #
# --------------------------------------------------------------------------- #

DEPLOYMENT_MARKERS = [
    "E2 ALTERNATIVES",
    "E2(a)",
    "E2(b)",
    "E2(c)",
    "3090 UNAVAILABILITY RECORD",
    "TCP-CLOSED at the 2026-09-09 reconnaissance",
    "MUST-NOT-BE-STARTED/RECONFIGURED",
    "B EXCLUSION",
    "EXCLUDED_BY_HUMAN_OVERRIDE",
    "no probes, no calls, ever",
]


class ProtocolElementsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol_text = PROTOCOL.read_text(encoding="utf-8")
        cls.deployment_text = DEPLOYMENT.read_text(encoding="utf-8")

    # ---- positive: all markers present at the tested head ---------------- #

    def test_protocol_element_markers_present(self):
        missing = missing_markers(self.protocol_text, PROTOCOL_MARKERS)
        self.assertEqual(missing, [], "missing protocol markers: %r" % missing)

    def test_deployment_identity_markers_present(self):
        missing = missing_markers(self.deployment_text, DEPLOYMENT_MARKERS)
        self.assertEqual(missing, [], "missing deployment markers: %r" % missing)

    # ---- negative (tamper): the checker fails when a marker is removed ---- #

    def _tamper(self, text, markers, marker):
        flat = normalize(text)
        needle = normalize(marker)
        tampered = flat.replace(needle, "")
        self.assertNotEqual(tampered, flat, "marker not found to tamper: %r" % marker)
        missing = missing_markers(tampered, markers)
        self.assertTrue(any(m == marker or normalize(m) in (needle,) for m in missing),
                        "removing %r was not detected; missing=%r" % (marker, missing))

    def test_protocol_tamper_negative_all_markers(self):
        for marker in PROTOCOL_MARKERS:
            with self.subTest(marker=marker[:60]):
                self._tamper(self.protocol_text, PROTOCOL_MARKERS, marker)

    def test_deployment_tamper_negative_all_markers(self):
        for marker in DEPLOYMENT_MARKERS:
            with self.subTest(marker=marker[:60]):
                self._tamper(self.deployment_text, DEPLOYMENT_MARKERS, marker)


if __name__ == "__main__":
    unittest.main()
