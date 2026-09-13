"""Data-free historical variant contracts and safe reproduction plans.

This module is a curation boundary, not a new experiment runner.  It records
the settings that distinguished the preserved executions and can render an
opt-in plan without opening a network connection or loading private data.
"""

from __future__ import annotations

import os
import shlex
from dataclasses import asdict, dataclass
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
    historical_model_calls: int | None = None
    historical_network_calls: int | None = None


_RAW_SOURCES = (
    "research/curated/detector.py",
    "research/curated/historical_variants.py",
    "research/curated/historical_methods.py",
    "research/curated/historical_transport.py",
)
_HYPHEN_SOURCES = (
    "research/curated/historical_detector.py",
    "research/curated/historical_pipeline.py",
    "research/curated/historical_methods.py",
    "research/curated/historical_transport.py",
)
_CAMPAIGN_SOURCES = (
    "research/curated/historical_campaign.py",
    "research/curated/historical_campaign_storage.py",
    "research/curated/historical_campaign_checkpoint.py",
    "research/curated/historical_campaign_entrypoints.py",
    "research/curated/historical_pipeline.py",
    "research/curated/historical_methods.py",
    "research/curated/historical_scoring.py",
)
_MODEL_WIRE_KEYS = ("model", "stream", "store", "input", "include_reasoning", "reasoning")


VARIANTS: tuple[VariantSpec, ...] = (
    VariantSpec("007-b-replacement", None, "Did the authorized replacement reach the model boundary?", "replacement execution only", "frozen", "unspecified", 4, 0, "no fresh reproduction request; historical held-out Qwen contact is recorded separately", ("research/curated/historical.py",), "recovery", "FAILED_BEFORE_PROXY_CONTACT", 10, 10),
    VariantSpec("007-b-timeout300", None, "What controlled evidence survived the timeout-300 replacement?", "timeout budget only", "frozen", "unspecified", 4, 0, "no fresh reproduction request; historical held-out Qwen contact is recorded separately", ("research/curated/historical.py",), "recovery", "COMPLETED_CONTROLLED_WITH_INVALID_TRACE_ASSOCIATION", 10, 10),
    VariantSpec("nonthinking-mechanical", None, "What did direct review do with reasoning disabled?", "reasoning disabled", "raw", "none", 4, 0, "direct reviewer request with mechanical-only acceptance; filled material omitted", _RAW_SOURCES, "small-study", "COMPLETED"),
    VariantSpec("low-thinking-mechanical", None, "What did direct review do with low reasoning?", "low reasoning", "raw", "low", 4, 0, "direct reviewer request with mechanical-only acceptance; filled material omitted", _RAW_SOURCES, "small-study", "COMPLETED"),
    VariantSpec("high-thinking-mechanical", None, "Could high-reasoning direct review complete?", "high reasoning", "raw", "high", 4, 0, "direct reviewer request with mechanical-only acceptance; filled material omitted", _RAW_SOURCES, "small-study", "STOPPED", 1, 1),
    VariantSpec("xhigh-thinking-mechanical", None, "What did direct review do with xhigh reasoning?", "xhigh reasoning", "raw", "xhigh", 4, 0, "direct reviewer request with mechanical-only acceptance; filled material omitted", _RAW_SOURCES, "small-study", "COMPLETED"),
    VariantSpec("low-plus-validator", None, "How did the separately sampled validator classify first-pass proposals?", "independent validator pass over first-pass proposals", "raw", "low", 4, 0, "validator-only request over caller-supplied frozen first-stage proposal; filled material omitted", ("research/curated/historical_validator.py", "research/curated/validation.py"), "small-study", "COMPLETED"),
    VariantSpec("low-unigram-retry", None, "What changed after one unigram-uncertain corrective retry?", "contextual first-pass unigram gate followed by one contextual JSON corrective retry", "raw", "low", 4, 1, "contextual retry sends the original sentence, selected target, raw rejected replacement, and missing-word evidence; filled material omitted", _RAW_SOURCES + ("research/curated/retry.py",), "small-study-retry", "COMPLETED"),
    VariantSpec("low-word-only-retry", None, "How did strict word-only retry parsing behave after the stop?", "word-only retry and whitespace continuation", "raw", "low", 4, 1, "word-only retry sends the raw rejected word; saved whitespace continuation reuses the first response", _RAW_SOURCES + ("research/curated/retry.py", "research/curated/historical_word_continuation.py"), "small-study-retry", "STOPPED_WITH_WHITESPACE_CONTINUATION", 2, 2),
    VariantSpec("full-hyphen-space-low", None, "What changed after the length-preserving hyphen lookup view?", "ASCII hyphen-to-space detector view", "hyphen-space", "low", 4, 1, "hyphen-space detector view with the early no-English policy and word-only retry; filled material omitted", _HYPHEN_SOURCES + ("research/curated/retry.py", "research/curated/historical_variants.py"), "small-study-retry", "COMPLETED"),
    VariantSpec("full-hyphen-case-low", None, "What changed with the first one-way initial-case rule?", "one-way initial-case restoration", "hyphen-space", "low", 4, 1, "hyphen-space detector view with one-way initial-case adjustment and word-only retry; filled material omitted", _HYPHEN_SOURCES + ("research/curated/retry.py", "research/curated/historical_variants.py"), "small-study-retry", "COMPLETED"),
    VariantSpec("ten-run-initial-case-low", None, "What persisted across ten symmetric initial-case trials?", "symmetric initial-case restoration", "hyphen-space", "low", 4, 1, "ten scheduled symmetric-case trials with early word-only retry; filled material omitted", _HYPHEN_SOURCES + ("research/curated/retry.py", "research/curated/historical_variants.py", "research/curated/historical_ten_run.py"), "trial-study", "COMPLETED_WITH_STOPPED_TRIALS"),
    VariantSpec("ten-run-expression-retry-low", None, "What persisted across ten context-free expression-retry trials?", "expression retry shape", "hyphen-space", "low", 4, 1, "ten scheduled no-English trials with context-free expression retry; filled material omitted", _HYPHEN_SOURCES + ("research/curated/retry.py", "research/curated/historical_variants.py", "research/curated/historical_ten_run.py"), "trial-study", "COMPLETED_WITH_STOPPED_TRIALS"),
    VariantSpec("ten-run-english-preserve-low", None, "How did English attestation alter review eligibility?", "English-preservation pre-review", "hyphen-space", "low", 4, 1, "ten scheduled trials with numeric English evidence on original absent targets only; filled material omitted", _HYPHEN_SOURCES + ("research/curated/english_preserve.py", "research/curated/retry.py", "research/curated/historical_ten_run.py"), "trial-study", "COMPLETED_ALL_TEN_TRIALS"),
    VariantSpec("large-evaluation-capped", None, "What survived the started capped campaign?", "capped campaign preparation", "capped", "low", 4, 1, "campaign worker request; filled material omitted", _CAMPAIGN_SOURCES, "campaign", "INFERENCE_STARTED_NOT_COMPLETED"),
    VariantSpec("large-evaluation-uncapped", None, "What evidence existed before the uncapped campaign was paused?", "uncapped campaign preparation", "uncapped", "low", None, 1, "campaign worker request; filled material omitted", _CAMPAIGN_SOURCES, "campaign", "PAUSED_BY_HUMAN_RELEVANCE_CHANGE"),
    VariantSpec("dassle-spelling-preparation", None, "What did the spelling preparation preserve?", "spelling preparation and four-worker execution", "campaign", "low", None, 1, "campaign worker request; source sentences were sent as model input but filled records are excluded from public Git", _CAMPAIGN_SOURCES, "campaign", "COMPLETE_LOCAL_EVIDENCE_WITH_RECORDED_INCIDENTS"),
    VariantSpec("dassle-uv-audit", None, "How many frozen edit units matched the requested u/v categories?", "exhaustive and random-sample mechanical audit", "audit", "none", None, 0, "no model request; literal source/result classification only", ("research/curated/historical_dassle.py", "research/curated/historical_scoring.py"), "audit", "COMPLETE_EXHAUSTIVE_MECHANICAL_AUDIT"),
    VariantSpec("full-campaign8", None, "What did the nine-phase eight-worker campaign establish locally?", "final eight-worker campaign", "campaign", "low", None, 1, "campaign worker request with actual runner8 capture, checkpoint and scorer programs; filled material omitted", _CAMPAIGN_SOURCES, "campaign", "COMPLETED_LOCAL_CAMPAIGN_REMOTE_SCORING_PENDING"),
    VariantSpec("prijigrala-retry10", None, "What happened in the one-target retry-limit-ten case?", "retry limit ten for one target", "hyphen-space", "low", 1, 10, "latest English-preserve pipeline; one selected target; every context-free retry repeats the raw first rejected replacement; filled material omitted", _HYPHEN_SOURCES + ("research/curated/english_preserve.py", "research/curated/historical_retry10.py", "research/curated/retry.py"), "single-case", "COMPLETE"),
    VariantSpec("levenshtein-lookup-diagnostic", None, "Can one deterministic lookup illuminate a single diagnostic case?", "single read-only lookup; inline source unavailable", "unavailable", "none", None, 0, "no model request; unavailable inline Levenshtein source remains explicit", ("research/curated/historical_scoring.py",), "diagnostic", "NOT_A_BENCHMARK"),
)


def variant_map() -> dict[str, VariantSpec]:
    return {variant.id: variant for variant in VARIANTS}


def reproduction_contract(variant: VariantSpec) -> dict[str, Any]:
    """Return explicit resource/credential fields without resolving private paths."""
    contract: dict[str, Any] = {
        "variant_id": variant.id,
        "mode": "offline_plan_only",
        "authorized_resources": {
            "input_root_env": "RESEARCH_INPUT_ROOT",
            "index_path_env": "RESEARCH_INDEX_PATH",
            "output_root_env": "RESEARCH_OUTPUT_ROOT",
            "endpoint_env": "RESEARCH_ENDPOINT",
            "credential_reference_env": "RESEARCH_CREDENTIAL_REF",
        },
        "resource_budget": {"workers": "explicit", "request_timeout_seconds": "explicit", "max_cases": "explicit", "max_retries": variant.corrective_retries},
        "default_network_calls": 0,
        "default_model_calls": 0,
        "requires_explicit_live_authorization": True,
    }
    if variant.historical_model_calls is not None or variant.historical_network_calls is not None:
        contract["historical_execution"] = {
            "model_calls": variant.historical_model_calls,
            "network_calls": variant.historical_network_calls,
            "separate_from_reproduction_policy": True,
        }
    if variant.id in {"007-b-replacement", "007-b-timeout300", "dassle-uv-audit", "levenshtein-lookup-diagnostic"}:
        contract["request"] = {
            "mode": variant.prompt,
            "model_calls": 0,
            "content": [] if variant.id.startswith("007-b-") else ["caller-supplied literal source/result records"],
        }
    elif variant.id == "low-plus-validator":
        contract["request"] = {
            "wire_keys": list(_MODEL_WIRE_KEYS),
            "content": ["caller-supplied frozen first-stage proposal", "original sentence", "selected target", "resulting sentence"],
            "mode": "validator calls only; first-stage calls are reused",
        }
    else:
        contract["inference_fields"] = {
            "sent": list(_MODEL_WIRE_KEYS),
            "content_sent": ["completed source sentence", "selected target", "variant-specific retry fields when applicable"],
            "omitted": ["conversation_history", "gold_text", "private_response_body", "credentials"],
            "public_redactions": ["source sentences", "filled prompts", "replacements", "raw responses", "reasoning traces"],
        }
        contract["request"] = {
            "wire_keys": list(_MODEL_WIRE_KEYS),
            "content": ["completed source sentence", "selected target"],
            "mode": variant.prompt,
        }
    return contract


def reproduction_command(variant: VariantSpec, *, input_root: str = "$RESEARCH_INPUT_ROOT", index_path: str = "$RESEARCH_INDEX_PATH", output_root: str = "$RESEARCH_OUTPUT_ROOT") -> str:
    args = ["python3", "-B", "-m", "research.tools.reproduce", "--variant", variant.id, "--input-root", input_root, "--index", index_path, "--output-root", output_root, "--endpoint", "$RESEARCH_ENDPOINT", "--model", "$RESEARCH_MODEL", "--workers", "1", "--timeout-seconds", "60", "--max-cases", "0", "--credential-env", "RESEARCH_CREDENTIAL_REF", "--retry-limit", str(variant.corrective_retries)]
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
    if not isinstance(credential_env, str) or not credential_env.isidentifier() or not os.environ.get(credential_env):
        raise ValueError("credential reference environment variable is absent")


def plan(variant_id: str) -> dict[str, Any]:
    try:
        variant = variant_map()[variant_id]
    except KeyError as exc:
        raise ValueError(f"unknown historical variant: {variant_id}") from exc
    return {"variant": asdict(variant), "contract": reproduction_contract(variant), "command": reproduction_command(variant)}
