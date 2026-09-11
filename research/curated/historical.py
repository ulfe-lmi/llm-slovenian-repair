"""Data-free historical variant contracts and safe reproduction plans.

This module is a curation boundary, not a new experiment runner.  It records
the settings that distinguished the preserved executions and can render an
opt-in plan without opening a network connection or loading private data.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import os
from pathlib import Path
import shlex
from typing import Any


@dataclass(frozen=True)
class VariantSpec:
    id: str
    parent: str | None
    question: str
    authorized_change: str
    detector: str
    reasoning: str
    maximum_targets: int | None
    corrective_retries: int
    prompt: str
    source_modules: tuple[str, ...]
    result_schema: str
    status: str


_COMMON_SOURCES = (
    "research/curated/historical_detector.py",
    "research/curated/historical_pipeline.py",
    "research/curated/historical_methods.py",
    "research/curated/historical_transport.py",
)


VARIANTS: tuple[VariantSpec, ...] = (
    VariantSpec("007-b-replacement", None, "Did the authorized replacement reach the model boundary?", "replacement execution only", "frozen", "unspecified", 4, 0, "generic targeted review; filled material omitted", ("recovery/driver",), "recovery", "FAILED_BEFORE_PROXY_CONTACT"),
    VariantSpec("007-b-timeout300", None, "What controlled evidence survived the timeout-300 replacement?", "timeout budget only", "frozen", "unspecified", 4, 0, "generic targeted review; filled material omitted", ("recovery/driver",), "recovery", "COMPLETED_CONTROLLED_WITH_INVALID_TRACE_ASSOCIATION"),
    VariantSpec("nonthinking-mechanical", None, "What did direct review do with reasoning disabled?", "reasoning disabled", "local-context", "none", 4, 0, "generic targeted review; filled material omitted", _COMMON_SOURCES, "small-study", "COMPLETED"),
    VariantSpec("low-thinking-mechanical", None, "What did direct review do with low reasoning?", "low reasoning", "local-context", "low", 4, 0, "generic targeted review; filled material omitted", _COMMON_SOURCES, "small-study", "COMPLETED"),
    VariantSpec("high-thinking-mechanical", None, "Could high-reasoning direct review complete?", "high reasoning", "local-context", "high", 4, 0, "generic targeted review; filled material omitted", _COMMON_SOURCES, "small-study", "STOPPED"),
    VariantSpec("xhigh-thinking-mechanical", None, "What did direct review do with xhigh reasoning?", "xhigh reasoning", "local-context", "xhigh", 4, 0, "generic targeted review; filled material omitted", _COMMON_SOURCES, "small-study", "COMPLETED"),
    VariantSpec("low-plus-validator", None, "How did the separately sampled validator classify first-pass proposals?", "independent validator pass over first-pass proposals", "local-context", "low", 4, 0, "actual validator prompt with complete sentence and selected replacement; filled material omitted", _COMMON_SOURCES + ("research/curated/validation.py",), "small-study", "COMPLETED"),
    VariantSpec("low-unigram-retry", None, "What changed after one unigram-uncertain corrective retry?", "contextual first-pass unigram gate followed by an expression-only corrective retry", "local-context", "low", 4, 1, "contextual retry program; the first target was selected from sentence context and the corrective prompt deliberately omitted that context", _COMMON_SOURCES + ("research/curated/retry.py",), "small-study-retry", "COMPLETED"),
    VariantSpec("low-word-only-retry", None, "How did strict word-only retry parsing behave after the stop?", "word-only retry and whitespace continuation", "local-context", "low", 4, 1, "generic word-only corrective retry; filled material omitted", _COMMON_SOURCES + ("research/curated/retry.py",), "small-study-retry", "STOPPED_WITH_WHITESPACE_CONTINUATION"),
    VariantSpec("full-hyphen-space-low", None, "What changed after the length-preserving hyphen lookup view?", "ASCII hyphen-to-space detector view", "hyphen-space", "low", 4, 1, "generic contextual review; filled material omitted", _COMMON_SOURCES + ("research/curated/historical_detector.py",), "small-study-retry", "COMPLETED"),
    VariantSpec("full-hyphen-case-low", None, "What changed with the first one-way initial-case rule?", "one-way initial-case restoration", "hyphen-space", "low", 4, 1, "generic contextual review; filled material omitted", _COMMON_SOURCES + ("research/curated/historical_detector.py",), "small-study-retry", "COMPLETED"),
    VariantSpec("ten-run-initial-case-low", None, "What persisted across ten symmetric initial-case trials?", "symmetric initial-case restoration", "hyphen-space", "low", 4, 1, "generic contextual review; filled material omitted", _COMMON_SOURCES + ("research/curated/historical_detector.py",), "trial-study", "COMPLETED_WITH_STOPPED_TRIALS"),
    VariantSpec("ten-run-expression-retry-low", None, "What persisted across ten context-free expression-retry trials?", "expression retry shape", "hyphen-space", "low", 4, 1, "generic contextual and expression retry; filled material omitted", _COMMON_SOURCES + ("research/curated/retry.py",), "trial-study", "COMPLETED_WITH_STOPPED_TRIALS"),
    VariantSpec("ten-run-english-preserve-low", None, "How did English attestation alter review eligibility?", "English-preservation pre-review", "hyphen-space", "low", 4, 1, "generic contextual review; filled material omitted", _COMMON_SOURCES + ("research/curated/english_preserve.py",), "trial-study", "COMPLETED_ALL_TEN_TRIALS"),
    VariantSpec("large-evaluation-capped", None, "What survived the started capped campaign?", "capped campaign preparation", "capped", "low", 4, 1, "generic campaign review; filled material omitted", ("research/curated/historical_campaign.py",), "campaign", "INFERENCE_STARTED_NOT_COMPLETED"),
    VariantSpec("large-evaluation-uncapped", None, "What evidence existed before the uncapped campaign was paused?", "uncapped campaign preparation", "uncapped", "low", None, 1, "generic campaign review; filled material omitted", ("research/curated/historical_campaign.py",), "campaign", "PAUSED_BY_HUMAN_RELEVANCE_CHANGE"),
    VariantSpec("dassle-spelling-preparation", None, "What did the spelling preparation preserve?", "spelling preparation and four-worker execution", "campaign", "low", None, 1, "generic campaign review; source sentences were sent as model input but filled records are excluded from public Git", ("research/curated/historical_campaign.py", "research/curated/historical_scoring.py"), "campaign", "COMPLETE_LOCAL_EVIDENCE_WITH_RECORDED_INCIDENTS"),
    VariantSpec("dassle-uv-audit", None, "How many frozen edit units matched the requested u/v categories?", "exhaustive and random-sample mechanical audit", "audit", "none", None, 0, "no model prompt; mechanical audit only", ("research/curated/historical_scoring.py",), "audit", "COMPLETE_EXHAUSTIVE_MECHANICAL_AUDIT"),
    VariantSpec("full-campaign8", None, "What did the nine-phase eight-worker campaign establish locally?", "final eight-worker campaign", "campaign", "low", None, 1, "generic campaign review with actual runner8 capture, checkpoint and scorer programs; filled material omitted", ("research/curated/historical_campaign.py", "research/curated/historical_campaign_storage.py", "research/curated/historical_campaign_checkpoint.py", "research/curated/historical_campaign_entrypoints.py", "research/curated/historical_scoring.py"), "campaign", "COMPLETED_LOCAL_CAMPAIGN_REMOTE_SCORING_PENDING"),
    VariantSpec("prijigrala-retry10", None, "What happened in the one-target retry-limit-ten case?", "retry limit ten for one target", "local-context", "low", 4, 10, "generic targeted retry; filled material omitted", ("research/curated/retry.py",), "single-case", "COMPLETE"),
)


def variant_map() -> dict[str, VariantSpec]:
    return {variant.id: variant for variant in VARIANTS}


def reproduction_contract(variant: VariantSpec) -> dict[str, Any]:
    """Return explicit resource/credential fields without resolving private paths."""
    return {
        "variant_id": variant.id,
        "mode": "offline_plan_only",
        "authorized_resources": {
            "input_root_env": "RESEARCH_INPUT_ROOT",
            "index_path_env": "RESEARCH_INDEX_PATH",
            "output_root_env": "RESEARCH_OUTPUT_ROOT",
            "endpoint_env": "RESEARCH_ENDPOINT",
            "credential_reference_env": "RESEARCH_CREDENTIAL_REF",
        },
        "inference_fields": {
            "sent": ["model", "reasoning", "input", "filled_dataset_text", "generic_prompt", "bounded_target_metadata"],
            "omitted": ["conversation_history", "gold_text", "private_response_body", "credentials"],
        },
        "resource_budget": {"workers": "explicit", "request_timeout_seconds": "explicit", "max_cases": "explicit", "max_retries": variant.corrective_retries},
        "default_network_calls": 0,
        "default_model_calls": 0,
        "requires_explicit_live_authorization": True,
    }


def reproduction_command(variant: VariantSpec, *, input_root: str = "$RESEARCH_INPUT_ROOT", index_path: str = "$RESEARCH_INDEX_PATH", output_root: str = "$RESEARCH_OUTPUT_ROOT") -> str:
    args = ["python3", "-B", "-m", "research.tools.reproduce", "--variant", variant.id, "--input-root", input_root, "--index", index_path, "--output-root", output_root, "--workers", "1", "--timeout-seconds", "60", "--max-cases", "0", "--credential-env", "RESEARCH_CREDENTIAL_REF"]
    return shlex.join(args)


def validate_live_authorization(*, allow_live: bool, endpoint: str | None, model: str | None, credential_env: str | None, input_root: str | None, index_path: str | None, output_root: str | None, workers: int, max_cases: int, timeout_seconds: int) -> None:
    """Validate the boundary; this function never performs a request."""
    if not allow_live:
        return
    values = (endpoint, model, credential_env, input_root, index_path, output_root)
    if not all(values):
        raise ValueError("live reproduction requires endpoint, model, credential reference, input/index/output roots")
    if workers < 1 or workers > 8 or max_cases < 1 or timeout_seconds < 1:
        raise ValueError("live reproduction budget is invalid")
    if not credential_env.isidentifier() or not os.environ.get(credential_env):
        raise ValueError("credential reference environment variable is absent")


def plan(variant_id: str) -> dict[str, Any]:
    try:
        variant = variant_map()[variant_id]
    except KeyError as exc:
        raise ValueError(f"unknown historical variant: {variant_id}") from exc
    return {"variant": asdict(variant), "contract": reproduction_contract(variant), "command": reproduction_command(variant)}
