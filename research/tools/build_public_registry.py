#!/usr/bin/env python3
"""Build evidence-derived public research metadata without copying payloads."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
import re
from typing import Any, Iterable, Iterator


ROOT_SPECS: tuple[dict[str, Any], ...] = (
    {"id": "007-b-replacement", "root": "recovery-executions/007-b-human-replacement-20260909.MnH1Qb", "kind": "recovery", "variation": "human-authorized replacement execution", "status": "FAILED_BEFORE_PROXY_CONTACT", "question": "Did the owner-authorized replacement reach the model boundary?"},
    {"id": "007-b-timeout300", "root": "recovery-executions/007-b-human-timeout300-20260909.NWGrtX", "kind": "recovery", "variation": "human-authorized timeout-300 replacement execution", "status": "COMPLETED_CONTROLLED_WITH_INVALID_TRACE_ASSOCIATION", "question": "What evidence survived the controlled timeout-300 replacement and where is its case/trace association invalid?"},
    {"id": "nonthinking-mechanical", "root": "experiments/nonthinking-mechanical-20260909.5m8LKG", "kind": "variant", "variation": "direct review with reasoning disabled and mechanical-only acceptance", "status": "COMPLETED", "question": "What did the frozen direct reviewer do when reasoning was disabled?"},
    {"id": "low-thinking-mechanical", "root": "experiments/low-thinking-mechanical-20260909.Ih2OFD", "kind": "variant", "variation": "direct review with low reasoning and mechanical-only acceptance", "status": "COMPLETED", "question": "What did the frozen direct reviewer do with low reasoning?"},
    {"id": "high-thinking-mechanical", "root": "experiments/high-thinking-mechanical-20260909.50kTrN", "kind": "variant", "variation": "direct review with high reasoning", "status": "STOPPED", "question": "Could the high-reasoning direct run complete under the preserved execution boundary?"},
    {"id": "xhigh-thinking-mechanical", "root": "experiments/xhigh-thinking-mechanical-20260909.ZsPBb5", "kind": "variant", "variation": "direct review with xhigh reasoning and mechanical-only acceptance", "status": "COMPLETED", "question": "What did the frozen direct reviewer do with xhigh reasoning?"},
    {"id": "low-plus-validator", "root": "experiments/low-plus-validator-20260909.eKAYe6", "kind": "variant", "variation": "low-thinking review plus a frozen validator pass", "status": "COMPLETED", "question": "How did the separately sampled validator classify frozen first-pass proposals?"},
    {"id": "low-unigram-retry", "root": "experiments/low-unigram-retry-20260909.Wb0TI7", "kind": "variant", "variation": "low-thinking unigram post-check and one contextual JSON corrective retry", "status": "COMPLETED", "question": "What changed when unigram-uncertain proposals received one contextual corrective retry?"},
    {"id": "low-word-only-retry", "root": "experiments/low-word-only-retry-20260909.0Hk0P9", "kind": "variant", "variation": "low-thinking word-only corrective retry with continuation", "status": "STOPPED_WITH_WHITESPACE_CONTINUATION", "question": "How did strict word-only retry parsing behave at the first stopped execution?"},
    {"id": "full-hyphen-space-low", "root": "experiments/full-hyphen-space-low-20260909.12wKze", "kind": "variant", "variation": "full low-thinking pipeline with ASCII hyphen-to-space detector view", "status": "COMPLETED", "question": "What was measured after introducing the length-preserving hyphen lookup view?"},
    {"id": "full-hyphen-case-low", "root": "experiments/full-hyphen-case-low-20260909.IFYupt", "kind": "variant", "variation": "full low-thinking pipeline with one-way initial-case preservation", "status": "COMPLETED", "question": "What was measured with the first one-way initial-case preservation rule?"},
    {"id": "ten-run-initial-case-low", "root": "experiments/ten-run-initial-case-low-20260909.87bzTW", "kind": "study", "variation": "ten-trial symmetric initial-case preservation", "status": "COMPLETED_WITH_STOPPED_TRIALS", "question": "What persisted across ten scheduled trials of the symmetric case rule?"},
    {"id": "ten-run-expression-retry-low", "root": "experiments/ten-run-expression-retry-low-20260909.xJhqYm", "kind": "study", "variation": "ten-trial context-free expression retry", "status": "COMPLETED_WITH_STOPPED_TRIALS", "question": "What persisted across ten scheduled trials of the expression retry?"},
    {"id": "ten-run-english-preserve-low", "root": "experiments/ten-run-english-preserve-low-20260909.AQnnRH", "kind": "study", "variation": "ten-trial English-preservation pre-review", "status": "COMPLETED_ALL_TEN_TRIALS", "question": "How did original Slovene-unigram absence plus English attestation change review eligibility?"},
    {"id": "large-evaluation-capped", "root": "experiments/large-evaluation-20260909.ZowPyK", "kind": "campaign", "variation": "capped external evaluation preparation", "status": "INFERENCE_STARTED_NOT_COMPLETED", "question": "What evidence survived the started capped external campaign before completion?"},
    {"id": "large-evaluation-uncapped", "root": "experiments/large-evaluation-uncapped-20260910.faME3U", "kind": "campaign", "variation": "owner-directed uncapped external campaign", "status": "PAUSED_BY_HUMAN_RELEVANCE_CHANGE", "question": "What evidence was available before the owner redirected the uncapped campaign?"},
    {"id": "dassle-spelling-preparation", "root": "experiments/dassle-spelling-preparation-20260910.whOa6K", "kind": "preparation", "variation": "DASSLE spelling preparation, detector evidence, and controlled execution", "status": "COMPLETE_LOCAL_EVIDENCE_WITH_RECORDED_INCIDENTS", "question": "What did the DASSLE spelling preparation and controlled execution preserve, including worker incidents?"},
    {"id": "dassle-uv-audit", "root": "experiments/dassle-uv-audit-20260911.BGeMLs", "kind": "audit", "variation": "DASSLE exhaustive u/v mechanical audit and random-20 sample", "status": "COMPLETE_EXHAUSTIVE_MECHANICAL_AUDIT", "question": "How many frozen DASSLE edit units matched the requested u/v categories and sensitivities?"},
    {"id": "full-campaign8", "root": "experiments/full-campaign8-20260911.XLAbaa", "kind": "campaign", "variation": "final full eight-worker A100 campaign", "status": "COMPLETED_LOCAL_CAMPAIGN_REMOTE_SCORING_PENDING", "question": "What did the complete nine-phase eight-worker campaign establish locally, and what remained access-blocked?"},
    {"id": "prijigrala-retry10", "root": "experiments/prijigrala-retry10-20260911.3E6HOg", "kind": "variant", "variation": "one-target contextual review with retry limit ten", "status": "COMPLETE", "question": "What happened in the one-target retry-limit-ten contextual case?"},
)

SOURCE_MAP: tuple[tuple[str, str], ...] = (
    ("concept-verification/config.py", "research/curated/config.py"),
    ("concept-verification/corpus.py", "research/curated/corpus.py"),
    ("concept-verification/protected.py", "research/curated/protected.py"),
    ("concept-verification/detector.py", "research/curated/detector.py"),
    ("concept-verification/qwen_client.py", "research/curated/review.py"),
    ("concept-verification/repair.py", "research/curated/patching.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/common.py", "research/curated/historical_common.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/pipeline_bridge.py", "research/curated/historical_pipeline.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/detector_uncapped.py", "research/curated/historical_detector.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/methods.py", "research/curated/historical_methods.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/metrics.py", "research/curated/historical_scoring.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/aggregate.py", "research/curated/historical_aggregate.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/bootstrap_stats.py", "research/curated/historical_bootstrap.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/adapters.py", "research/curated/historical_adapters.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/official_score.py", "research/curated/historical_official_score.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/transport.py", "research/curated/historical_transport.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/campaign.py", "research/curated/historical_campaign.py"),
    ("experiments/ten-run-english-preserve-low-20260909.AQnnRH/english_preserve.py", "research/curated/english_preserve.py"),
    ("experiments/ten-run-english-preserve-low-20260909.AQnnRH/expression_retry.py", "research/curated/retry.py"),
    ("experiments/ten-run-english-preserve-low-20260909.AQnnRH/hyphen_detector.py", "research/curated/historical_detector.py"),
    ("experiments/ten-run-english-preserve-low-20260909.AQnnRH/run_pipeline.py", "research/curated/historical_ten_run.py"),
    ("experiments/low-word-only-retry-20260909.0Hk0P9/retry.py", "research/curated/retry.py"),
    ("experiments/low-word-only-retry-20260909.0Hk0P9/continue_whitespace.py", "research/curated/historical_word_continuation.py"),
    ("experiments/low-unigram-retry-20260909.Wb0TI7/retry.py", "research/curated/retry.py"),
    ("llm-slovenian-repair-campaign8.ewruv3/runner8.py", "research/curated/historical_campaign.py"),
    ("llm-slovenian-repair-campaign8.ewruv3/storage8.py", "research/curated/historical_campaign_storage.py"),
    ("llm-slovenian-repair-campaign8.ewruv3/checkpoint8.py", "research/curated/historical_campaign_checkpoint.py"),
    ("llm-slovenian-repair-campaign8.ewruv3/prepare8.py", "research/curated/historical_campaign_entrypoints.py"),
    ("llm-slovenian-repair-campaign8.ewruv3/launch8.py", "research/curated/historical_campaign_entrypoints.py"),
)

FUNCTION_COVERAGE: dict[str, dict[str, list[str]]] = {
    "experiments/large-evaluation-uncapped-20260910.faME3U/common.py": {"copied": ["digest", "sha", "read", "encoded", "utc", "immutable_bytes", "save", "pointer", "jsonlines", "snapshot", "verify", "result_path"], "unavailable": []},
    "experiments/large-evaluation-uncapped-20260910.faME3U/pipeline_bridge.py": {"copied": ["Pipeline", "first_body", "retry_body", "patch", "parse_first", "parse_retry"], "unavailable": []},
    "experiments/large-evaluation-uncapped-20260910.faME3U/detector_uncapped.py": {"copied": ["Token", "Candidate", "tokenize", "_evidence", "detect", "candidate_summary"], "unavailable": []},
    "experiments/large-evaluation-uncapped-20260910.faME3U/methods.py": {"copied": ["identity", "direct", "targeted", "no_retry"], "unavailable": []},
    "experiments/large-evaluation-uncapped-20260910.faME3U/metrics.py": {"copied": ["tokens", "edits", "edit_key", "overlap", "prf", "distribution", "row_metrics", "summarize"], "unavailable": []},
    "experiments/large-evaluation-uncapped-20260910.faME3U/aggregate.py": {"copied": ["phase"], "unavailable": []},
    "experiments/large-evaluation-uncapped-20260910.faME3U/bootstrap_stats.py": {"copied": ["paired", "SEED", "REPLICATES"], "unavailable": []},
    "experiments/large-evaluation-uncapped-20260910.faME3U/adapters.py": {"copied": ["md_parse", "md_render", "multigec", "canonical_solar", "dassle", "slobench", "preservation", "build"], "unavailable": []},
    "experiments/large-evaluation-uncapped-20260910.faME3U/official_score.py": {"copied": ["tokenize", "command", "score_pairs"], "unavailable": ["main: caller-specific benchmark loop is represented by score_pairs"]},
    "experiments/large-evaluation-uncapped-20260910.faME3U/transport.py": {"copied": ["text_body", "parse_text", "Client", "Client.call", "_HttpTransport", "request capture and bounded parsing"], "unavailable": []},
    "experiments/large-evaluation-uncapped-20260910.faME3U/campaign.py": {"copied": ["inherited_records", "stored", "one", "run"], "unavailable": ["native scorer subprocess dispatch: score drivers are intentionally caller-selected"]},
    "experiments/ten-run-english-preserve-low-20260909.AQnnRH/english_preserve.py": {"copied": ["EnglishResourceError", "resource_identity", "load_frozen", "classify"], "unavailable": []},
    "experiments/ten-run-english-preserve-low-20260909.AQnnRH/expression_retry.py": {"copied": ["INSTRUCTION", "body_for", "parse_reply"], "unavailable": []},
    "experiments/ten-run-english-preserve-low-20260909.AQnnRH/hyphen_detector.py": {"copied": ["Token", "Candidate", "tokenize", "detect"], "unavailable": []},
    "experiments/ten-run-english-preserve-low-20260909.AQnnRH/run_pipeline.py": {"copied": ["PipelineStop", "prepare", "preserve_initial_case", "process_case", "run"], "unavailable": []},
    "experiments/low-word-only-retry-20260909.0Hk0P9/retry.py": {"copied": ["Unigrams equivalent via UnigramIndex", "check", "body_for equivalent word_only_retry_body", "outcome", "parse_word equivalent parse_word_only"], "unavailable": ["run: caller supplies explicit saved state and Client"]},
    "experiments/low-word-only-retry-20260909.0Hk0P9/continue_whitespace.py": {"copied": ["parse_word", "continue_saved"], "unavailable": ["finish: caller invokes continue_saved with saved response and pending item"]},
    "experiments/low-unigram-retry-20260909.Wb0TI7/retry.py": {"copied": ["INSTRUCTION", "Unigrams equivalent via UnigramIndex", "check", "body_for equivalent contextual_retry_body", "outcome", "parse_reply equivalent parse_contextual"], "unavailable": ["run: caller supplies explicit saved state and Client"]},
    "llm-slovenian-repair-campaign8.ewruv3/runner8.py": {"copied": ["partition", "process_identity", "run_assigned", "worker status/failure accounting"], "unavailable": ["execute: protected live coordinator is represented by historical_campaign.run and explicit entrypoint"]},
    "llm-slovenian-repair-campaign8.ewruv3/storage8.py": {"copied": ["Storage.source_bytes", "Storage.source_read", "Storage.source_sha", "Storage.source_tree"], "unavailable": []},
    "llm-slovenian-repair-campaign8.ewruv3/checkpoint8.py": {"copied": ["checkpoint_completed_cases"], "unavailable": []},
    "llm-slovenian-repair-campaign8.ewruv3/prepare8.py": {"copied": ["verify", "prepare"], "unavailable": []},
    "llm-slovenian-repair-campaign8.ewruv3/launch8.py": {"copied": ["launch_plan"], "unavailable": ["Popen: live detached launch remains deliberate caller boundary"]},
}

SAFE_NUMERIC = {
    "applied_edits", "applied_retry_edits", "available_case_instances_including_partial", "available_eligible_word_instances_including_partial", "available_known_error_instances_including_partial", "cases", "changed_controls", "complete_trials", "completed_case_outputs", "completed_phases", "completed_trials", "corrective_calls", "distinct_calls", "eligible_words", "exact_gold_repairs", "failed", "first_calls", "fresh_reviewer_calls", "gold_edit_units", "inherited_calls", "method_records", "missed_gold_errors", "model_calls", "new_corrective_calls", "new_model_calls", "operational_failures", "preservation_cases", "proposed_edits", "proposed_first_edits", "qualified_calls", "reasoning_tokens", "record_count", "retry_calls", "scheduled_trials", "stopped_trials", "total_calls", "trials", "unchanged_controls", "verified_checkpoints", "workers", "submissions", "spelling_cases", "new_calls", "unique_model_calls",
}
SAFE_TEXT = {"status", "outcome", "mode", "deployment", "remote_scoring", "inference_coordinator_status"}

GENERIC_PROMPT = "Ali se ti zdi uporaba besede oziroma besedne zveze X najboljša naravna izbira v tem slovenskem stavku? Če ne, s čim bi jo nadomestil?"
REPORT_NOTES = {
    "007-b-timeout300": "The timeout-300 association is not valid for case-level interpretation; preserve the controlled receipt without assigning it to a case.",
    "large-evaluation-capped": "A RUNNING snapshot means inference started, not that the campaign completed.",
    "large-evaluation-uncapped": "The human relevance change paused this campaign; no later phase is inferred.",
    "dassle-spelling-preparation": "Four-worker and recovery incidents remain operational evidence, not a quality label.",
    "dassle-uv-audit": "The exhaustive and random-sample views are mechanical; u/v membership is not a semantic judgment.",
    "full-campaign8": "Official and custom denominators remain separate. SloBench and MultiGEC-test have no references for correctness/harm interpretation; remote scoring and Deployment B remain blocked/excluded.",
    "prijigrala-retry10": "Clock accounting and logical reconstruction are retained as observations; the one-target result is not a general retry claim.",
    "levenshtein-lookup-diagnostic": "This is one read-only observation, not a benchmark.",
}


def _safe_child_hash(root: Path, *names: str) -> str | None:
    for name in names:
        path = root / name
        if path.is_file():
            return sha256(path)
    return None


def _child_runs(home: Path, spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Enumerate stable child IDs from existing small manifests, never snapshots alone."""
    root = home / spec["root"]
    if not root.is_dir():
        return []
    children: list[dict[str, Any]] = []
    runs = root / "runs"
    if runs.is_dir():
        for run in sorted(runs.iterdir(), key=lambda path: path.name):
            if not run.is_dir() or not re.fullmatch(r"[0-9]{2}", run.name):
                continue
            timing: dict[str, Any] = {}
            timing_path = run / "TRIAL-TIMING.json"
            if timing_path.is_file():
                try:
                    value = _json(timing_path)
                    if isinstance(value, dict):
                        timing = {key: child for key, child in value.items() if key in SAFE_NUMERIC or key in SAFE_TEXT and isinstance(child, str)}
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    timing = {}
            status = timing.get("status", "COMPLETED" if (run / "RESULTS.json").is_file() else "STOPPED")
            child = {
                "id": f"{spec['id']}/{run.name}",
                "kind": "trial",
                "status": status,
                "source_hash": _safe_child_hash(run, "FROZEN-RUN.json", "RUN-STARTED.json"),
                "result_hash": _safe_child_hash(run, "RESULTS.json", "STOPPED.json"),
                "metrics": timing,
                "public_report": f"research/reports/{spec['id']}.md#trial-{run.name}",
                "public_configuration": f"research/configs/{spec['id']}.json",
            }
            stopped = run / "STOPPED.json"
            if stopped.is_file():
                try:
                    value = _json(stopped)
                    if isinstance(value, dict) and isinstance(value.get("reason"), str):
                        child["stopped_reason"] = value["reason"]
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    pass
            children.append(child)
    if spec["id"] == "full-campaign8":
        final = root / "FINAL-VERIFICATION.json"
        if final.is_file():
            try:
                value = _json(final)
                for phase, item in sorted(value.get("phases", {}).items()):
                    completion = item.get("completion", {})
                    children.append({
                        "id": f"{spec['id']}/{phase}",
                        "kind": "phase",
                        "status": "COMPLETED" if completion.get("completed") else "UNKNOWN",
                        "source_hash": _safe_child_hash(root, "CONFIGURATION.json", "FINAL-VERIFICATION.json"),
                        "result_hash": _safe_child_hash(root, f"analysis/{phase}.json", f"phase-complete/{phase}.json"),
                        "metrics": {key: item.get(key) for key in ("examples", "method_records", "unique_call_records") if isinstance(item.get(key), (int, float))} | {"new_model_calls": completion.get("new_model_calls", 0)},
                        "public_report": f"research/reports/{spec['id']}.md#phase-{phase}",
                        "public_configuration": f"research/configs/{spec['id']}.json",
                    })
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                pass
    if spec["id"] == "dassle-uv-audit":
        for child_id, names in (("exhaustive-u-v", ("RESULTS.json", "REPORT.md")), ("random-20", ("INCLUSIVE-SENSITIVITY.json", "REPORT.md"))):
            children.append({
                "id": f"{spec['id']}/{child_id}",
                "kind": "audit-view",
                "status": "COMPLETE",
                "source_hash": _safe_child_hash(root, *names),
                "result_hash": _safe_child_hash(root, "RESULTS.json", "INCLUSIVE-SENSITIVITY.json"),
                "metrics": {"model_calls": 0},
                "public_report": f"research/reports/{spec['id']}.md#{child_id}",
                "public_configuration": f"research/configs/{spec['id']}.json",
            })
    if spec["id"] in {"large-evaluation-capped", "large-evaluation-uncapped"}:
        phase_dir = root / "phase-complete"
        if phase_dir.is_dir():
            for phase_file in sorted(phase_dir.glob("*.json")):
                children.append({
                    "id": f"{spec['id']}/{phase_file.stem}",
                    "kind": "phase",
                    "status": "RECORDED",
                    "source_hash": _safe_child_hash(root, "CONFIGURATION.json"),
                    "result_hash": sha256(phase_file),
                    "metrics": {"model_calls": 0},
                    "public_report": f"research/reports/{spec['id']}.md#phase-{phase_file.stem}",
                    "public_configuration": f"research/configs/{spec['id']}.json",
                })
    if spec["id"] == "dassle-spelling-preparation":
        for child_id, names in (("preparation", ("PREPARATION-VERIFIED.json", "DATASET-PREPARATION.json")), ("parallel4", ("parallel4-20260910.YOsnuz", "RUN-STATUS.json")), ("recovery", ("CONTINUITY.md", "RUN-STATUS.json")), ("final-scoring", ("SCORER-ROUNDTRIP-VERIFIED.json", "RUN-STATUS.json"))):
            children.append({
                "id": f"{spec['id']}/{child_id}",
                "kind": "stage",
                "status": "RECORDED",
                "source_hash": _safe_child_hash(root, *names),
                "result_hash": _safe_child_hash(root, "RUN-STATUS.json", "OFFLINE-VERIFICATION.json"),
                "metrics": {},
                "public_report": f"research/reports/{spec['id']}.md#{child_id}",
                "public_configuration": f"research/configs/{spec['id']}.json",
            })
    if spec["kind"] == "recovery":
        heldout = root / "heldout"
        children.append({
            "id": f"{spec['id']}/heldout",
            "kind": "recovery-stage",
            "status": "RECORDED" if heldout.is_dir() else "MISSING",
            "source_hash": _safe_child_hash(root, "AUTHORIZATION.md", "RESULT.md"),
            "result_hash": _safe_child_hash(root, "RESULT.md", "CONTROLLED-RESULT.md"),
            "metrics": {},
            "public_report": f"research/reports/{spec['id']}.md#heldout",
            "public_configuration": f"research/configs/{spec['id']}.json",
        })
    return children


def _public_links(experiment_id: str) -> dict[str, str]:
    return {
        "public_report": f"research/reports/{experiment_id}.md",
        "public_configuration": f"research/configs/{experiment_id}.json",
        "public_metrics": "research/results/study-evidence.json.gz",
        "source_manifest": "research/registry/source-manifest.json",
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json(path: Path) -> Any:
    if path.name.endswith(".gz"):
        with gzip.open(path, "rb") as handle:
            return json.loads(handle.read())
    return json.loads(path.read_text(encoding="utf-8"))


def _scalar_metrics(root: Path) -> dict[str, Any]:
    values: dict[str, Any] = {}
    candidates = ("RESULTS.json", "RUN-STATUS.json", "BATCH-SUMMARY.json", "STATISTICS.json", "VERIFICATION.json", "CONFIGURATION.json", "FINAL-VERIFICATION.json")
    for name in candidates:
        path = root / name
        if not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        try:
            value = _json(path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(value, dict):
            continue
        for key, child in value.items():
            if key in SAFE_NUMERIC and isinstance(child, (int, float, bool)) and key not in values:
                values[key] = child
            elif key in SAFE_TEXT and isinstance(child, str) and "\n" not in child and len(child) < 120 and key not in values:
                values[key] = child
        calls = value.get("calls")
        if isinstance(calls, list) and "model_calls" not in values:
            values["model_calls"] = len(calls)
            values["total_calls"] = len(calls)
            staged_review = sum(
                call.get("kind") == "reviewer" or call.get("stage") == "reviewer"
                for call in calls
                if isinstance(call, dict)
            )
            staged_retry = sum(
                call.get("kind") == "expression-retry" or call.get("stage") == "expression-retry"
                for call in calls
                if isinstance(call, dict)
            )
            values["review_calls"] = value.get("qualified_calls", staged_review)
            values["retry_calls"] = value.get("corrective_calls", value.get("new_corrective_calls", staged_retry))
        if "new_validator_calls" in value and "model_calls" not in values:
            values["model_calls"] = value["new_validator_calls"]
            values["validator_calls"] = value["new_validator_calls"]
        if "first_pass_calls_reused" in value:
            values["reused_calls"] = value["first_pass_calls_reused"]
        if "unique_model_calls" in value and "model_calls" not in values:
            values["model_calls"] = value["unique_model_calls"]
        summary = value.get("summary")
        if isinstance(summary, dict):
            controlled = summary.get("controlled")
            if isinstance(controlled, dict) and isinstance(controlled.get("cases"), int):
                values["cases"] = controlled["cases"]
            workload = summary.get("real_workload")
            if isinstance(workload, dict) and isinstance(workload.get("eligible_words"), int):
                values["eligible_words"] = workload["eligible_words"]
        if isinstance(value.get("trials"), list):
            trial_keys = sorted({key for trial in value["trials"] if isinstance(trial, dict) for key in trial if key in SAFE_NUMERIC})
            values["trial_metrics"] = [
                {key: trial.get(key) for key in trial_keys if isinstance(trial.get(key), (int, float, bool))}
                for trial in value["trials"] if isinstance(trial, dict)
            ]
    return values


def _campaign_metrics(root: Path, values: dict[str, Any]) -> dict[str, Any]:
    if root.name.startswith("full-campaign8-"):
        run = _json(root / "RUN-STATUS.json")
        final = _json(root / "FINAL-VERIFICATION.json")
        phases = []
        new_calls = 0
        method_records = 0
        for phase, item in sorted(final["phases"].items()):
            completion = item["completion"]
            row = {"phase": phase, "examples": item["examples"], "method_records": item["method_records"], "new_model_calls": completion["new_model_calls"], "unique_call_records": item["unique_call_records"]}
            phases.append(row)
            new_calls += completion["new_model_calls"]
            method_records += item["method_records"]
        values.update({"cases": run["cases"], "method_records": method_records, "distinct_calls": final["unique_call_records"], "model_calls": final["unique_call_records"], "new_model_calls": new_calls, "inherited_calls": final["unique_call_records"] - new_calls, "verified_checkpoints": final["raw_backups"]["archives"], "workers": run["LLM_workers"], "completed_phases": len(run["completed_phases"]), "phase_metrics": phases})
    return values


def experiment_records(home: Path) -> list[dict[str, Any]]:
    records = []
    for spec in ROOT_SPECS:
        root = home / spec["root"]
        metrics = _campaign_metrics(root, _scalar_metrics(root)) if root.is_dir() else {}
        record = {
            **spec,
            "experiment_id": spec["id"],
            "logical_root": spec["root"],
            "evidence_status": "enumerated-root" if root.is_dir() else "genuinely-missing",
            **_public_links(spec["id"]),
            "child_runs": _child_runs(home, spec),
            "frozen_choices": {
                "source": "preserved original source identity; curated copies are portability-only projections",
                "model_calls_during_curation": 0,
                "dataset_contents_published": False,
            },
            "metrics": metrics,
            "evidence_files": [],
            "conclusion": "Recorded historical outcome only; not a product, linguistic, replication, milestone, merge, or release claim.",
            "pending_evidence": ["human semantic labels where applicable", "official remote scoring where access was blocked", "independent reproduction when private data or service access is unavailable"],
        }
        if spec["id"] == "large-evaluation-capped":
            run_status = root / "RUN-STATUS.json"
            if run_status.is_file():
                try:
                    run_value = _json(run_status)
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    run_value = {}
                if isinstance(run_value, dict) and run_value.get("status") == "RUNNING":
                    record["status"] = "INFERENCE_STARTED_NOT_COMPLETED"
        if root.is_dir():
            for path in sorted(path for path in root.iterdir() if path.is_file()):
                disposition = "private-only; data-free metrics are projected separately"
                record["evidence_files"].append({"logical_path": f"{spec['root']}/{path.name}", "sha256": sha256(path), "size": path.stat().st_size, "disposition": disposition})
        records.append(record)
    records.append({
        "experiment_id": "levenshtein-lookup-diagnostic",
        "logical_root": "read-only diagnostic referenced by preserved research records",
        "kind": "diagnostic",
        "variation": "single-word lookup inspection after retry-limit-ten case",
        "status": "NOT_A_BENCHMARK",
        "question": "Can one deterministic lookup illuminate a single diagnostic case?",
        "frozen_choices": {"new_model_calls": 0, "standalone_source_hash": "not available"},
            "metrics": {"model_calls": 0},
            "evidence_files": [{"logical_path": "research-preservation-20260911.YJemoq/SUPPLEMENTAL-OBSERVATIONS.md", "disposition": "private-only"}],
            **_public_links("levenshtein-lookup-diagnostic"),
            "child_runs": [],
            "conclusion": "One observation only; no multi-example Levenshtein benchmark or generalized quality result.",
        "pending_evidence": ["none; this record is explicitly not a completed benchmark"],
    })
    return records


def _manifest_entries(root: Path) -> Iterator[tuple[str, str, int | None]]:
    candidates = (root / "NATIVE-MANIFEST.sha256", root / "MANIFEST.sha256", root / "MANIFEST.preparation.sha256")
    manifest = next((path for path in candidates if path.is_file()), None)
    if manifest is not None:
        for line in manifest.read_text(encoding="utf-8").splitlines():
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if match:
                yield match.group(2), match.group(1), None
        return
    for current, directories, names in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in directories:
            if (current_path / name).is_symlink():
                raise ValueError(f"symlink in private source: {current_path / name}")
        for name in sorted(names):
            path = current_path / name
            if path.is_symlink() or not path.is_file():
                raise ValueError(f"unsafe private source entry: {path}")
            yield path.relative_to(root).as_posix(), sha256(path), path.stat().st_size


def _logical(relative: str) -> tuple[str, str]:
    parts = []
    for part in Path(relative).parts:
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.+\-]{0,100}", part):
            parts.append(part)
        else:
            parts.append("<redacted-path-component>")
    safe = "/".join(parts)
    return safe, "safe-logical-path" if safe == relative else "path-component-redacted"


def census(home: Path, records: list[dict[str, Any]], curated_sources: dict[tuple[str, str], str], curated_results: dict[tuple[str, str], str]) -> tuple[list[dict[str, Any]], Counter[str]]:
    rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    seen: dict[str, str] = {}
    for record in records:
        logical_root = record.get("logical_root", "")
        root = home / logical_root
        if not root.is_dir():
            continue
        for relative, file_hash, size in _manifest_entries(root):
            safe_relative, path_status = _logical(relative)
            key = (logical_root, relative)
            classification = "private-only"
            destination = "private archive only"
            reason = "byte-exact original retained in private native archive; payload is excluded from public Git"
            if key in curated_sources:
                classification = "published-curated/redacted"
                destination = curated_sources[key]
                reason = "actual source seam curated with explicit path/resource portability transformation"
            elif key in curated_results:
                classification = "published-curated/redacted"
                destination = curated_results[key]
                reason = "data-free numeric projection; original result remains private"
            elif file_hash in seen:
                classification = "duplicate-linked"
                destination = "exact identity linked to " + seen[file_hash]
                reason = "duplicate byte identity; primary private disposition is retained"
            row = {"root": logical_root, "relative_path": safe_relative, "original_path_status": path_status, "sha256": file_hash, "size": size, "classification": classification, "destination_or_record": destination, "reason": reason}
            rows.append(row)
            counts[classification] += 1
            seen.setdefault(file_hash, logical_root + "/" + relative)
    return rows, counts


def census_from_existing(path: Path, curated_sources: dict[tuple[str, str], str], curated_results: dict[tuple[str, str], str]) -> tuple[list[dict[str, Any]], Counter[str]]:
    """Reclassify an already verified interrupted census without rereading payloads."""
    document = _json(path)
    rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for old in document.get("entries", []):
        root, relative = old["root"], old["relative_path"]
        key = (root, relative)
        classification = "private-only"
        destination = "private archive only"
        reason = "byte-exact original retained in private native archive; payload is excluded from public Git"
        if key in curated_sources:
            classification = "published-curated/redacted"
            destination = curated_sources[key]
            reason = "actual source seam curated with explicit path/resource portability transformation"
        elif key in curated_results:
            classification = "published-curated/redacted"
            destination = curated_results[key]
            reason = "data-free numeric projection; original result remains private"
        elif old.get("classification") == "duplicate-linked":
            classification = "duplicate-linked"
            destination = old.get("destination_or_record", "exact identity linked to a private primary")
            reason = "duplicate byte identity; primary private disposition is retained"
        row = {**old, "classification": classification, "destination_or_record": destination, "reason": reason}
        rows.append(row)
        counts[classification] += 1
    return rows, counts


def _safe_projection(value: Any, key: str = "") -> Any:
    denied = {"input", "output", "reference", "text", "original_target", "target", "candidate", "english_suppressions", "result_identities"}
    if isinstance(value, dict):
        result = {}
        for name, child in value.items():
            if name.casefold() in denied and not isinstance(child, (int, float, bool)):
                continue
            if isinstance(child, list) and any(isinstance(item, str) for item in child):
                continue
            if isinstance(child, str) and name not in {"id", "category", "problem_type", "benchmark", "metric_authority", "official_metric_note", "unit"}:
                continue
            result[name] = _safe_projection(child, name)
        return result
    if isinstance(value, list):
        return [_safe_projection(child, key) for child in value]
    return value


def result_projections(home: Path, records: list[dict[str, Any]], output: Path) -> dict[tuple[str, str], str]:
    source_root = home / "experiments/full-campaign8-20260911.XLAbaa/analysis"
    destination_map: dict[tuple[str, str], str] = {}
    output.mkdir(parents=True, exist_ok=True)
    for source in sorted(source_root.glob("*.json")):
        data = _json(source)
        projection = _safe_projection({key: value for key, value in data.items() if key not in {"english_suppressions", "result_identities"}})
        destination = output / (source.stem + ".json.gz")
        encoded = (json.dumps({"schema_version": 1, "benchmark": source.stem, "source_analysis_sha256": sha256(source), "data_free": True, "projection": projection}, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
        with gzip.GzipFile(filename=str(destination), mode="wb", mtime=0) as handle:
            handle.write(encoded)
        destination_map[("experiments/full-campaign8-20260911.XLAbaa", "analysis/" + source.name)] = "research/results/" + destination.name
    return destination_map


def source_manifest(repo: Path, home: Path, output: Path, native_root: Path | None = None) -> dict[tuple[str, str], str]:
    destinations: dict[tuple[str, str], str] = {}
    rows = []
    for original, destination in SOURCE_MAP:
        if original.startswith("concept-verification/"):
            source = repo / original
        elif original.startswith("llm-slovenian-repair-campaign8.ewruv3/"):
            source = (native_root / original if native_root is not None else Path("/__native-root-not-supplied__") / original)
        else:
            source = home / original
        target = repo / destination
        if not source.is_file() or not target.is_file():
            rows.append({"original_logical_path": original, "original_status": "genuinely-missing", "destination": destination})
            continue
        logical_root, relative = original.split("/", 1) if original.startswith("experiments/") or original.startswith("recovery-executions/") else ("repository", original)
        if logical_root == "repository":
            original_hash = sha256(source)
        else:
            original_hash = sha256(source)
            destinations[(original.rsplit("/", 1)[0], original.rsplit("/", 1)[1])] = destination
        rows.append({"original_logical_path": original, "original_sha256": original_hash, "curated_path": destination, "curated_sha256": sha256(target), "disposition": "published-curated/redacted", "function_coverage": FUNCTION_COVERAGE.get(original, {"copied": ["file-level executable source"], "unavailable": []}), "transformations": ["removed historical absolute paths", "externalized input/index/output roots", "kept experimental semantics and variant boundaries"]})
    (output / "source-manifest.json").write_text(json.dumps({"schema_version": 1, "scope": "actual source closure named by final campaign configuration and review", "entries": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return destinations


def archive_catalog(home: Path) -> dict[str, Any]:
    relocation_path = home / "research-preservation-20260911.YJemoq/RELOCATION.json"
    relocation = _json(relocation_path)
    archives = []
    preservation = home / "research-preservation-20260911.YJemoq"
    for item in relocation.get("roots", []):
        verified = {}
        for path in preservation.glob("*.verified.json"):
            value = _json(path)
            if value.get("archive") == item.get("archive"):
                verified = value
                break
        archives.append({"archive": item.get("archive"), "archive_sha256": item.get("archive_sha256"), "entries": verified.get("entries"), "uncompressed_file_bytes": verified.get("uncompressed_file_bytes"), "every_file_byte_hash_verified": verified.get("every_file_byte_hash_verified", False), "source_status": "private reboot-safe native archive; source bytes retained"})
    return {"schema_version": 1, "archives": archives, "tmp_status": relocation.get("status"), "source_byte_deletions": relocation.get("source_byte_deletions")}


_PUBLIC_DENIED = {"input", "output", "reference", "text", "replacement", "candidate", "request", "response", "result_identities", "english_suppressions"}


def _public_numeric(value: Any, key: str = "") -> Any:
    if isinstance(value, bool) or value is None or isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        if key.casefold() in _PUBLIC_DENIED or key.casefold().endswith(("_text", "_path")):
            return None
        if len(value) > 80 or "\n" in value or "/" in value:
            return None
        return value
    if isinstance(value, list):
        return [child for child in (_public_numeric(item, key) for item in value) if child is not None]
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for name, child in value.items():
            if str(name).casefold() in _PUBLIC_DENIED:
                continue
            projected = _public_numeric(child, str(name))
            if projected is not None:
                result[str(name)] = projected
        return result
    return None


def _study_evidence(home: Path, record: dict[str, Any]) -> dict[str, Any]:
    root = home / record.get("logical_root", "")
    evidence: dict[str, Any] = {
        "experiment_id": record["experiment_id"],
        "status": record["status"],
        "top_level_metrics": _public_numeric(record.get("metrics", {})),
        "trial_metrics": [],
        "case_metrics": [],
        "phase_metrics": [],
        "field_exclusions": ["sentences", "gold strings", "filled prompts", "response bodies", "private result identities"],
    }
    metrics = record.get("metrics", {})
    for index, trial in enumerate(metrics.get("trial_metrics", []), start=1):
        evidence["trial_metrics"].append({"trial_id": f"{index:02d}", **(_public_numeric(trial) or {})})
    statistics = root / "STATISTICS.json"
    if statistics.is_file() and statistics.stat().st_size <= 2_000_000:
        try:
            value = _json(statistics)
            per_case = value.get("per_case", {}) if isinstance(value, dict) else {}
            if isinstance(per_case, dict):
                for case_id, row in sorted(per_case.items()):
                    projected = _public_numeric(row)
                    if isinstance(projected, dict):
                        projected["case_id"] = str(case_id)
                        evidence["case_metrics"].append(projected)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            evidence["case_metrics_status"] = "UNAVAILABLE_PARSE_ERROR"
    if record["experiment_id"] == "full-campaign8" and (root / "analysis").is_dir():
        for path in sorted((root / "analysis").glob("*.json")):
            try:
                value = _json(path)
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                continue
            if not isinstance(value, dict):
                continue
            phase = {"phase": path.stem, "expected_examples": value.get("expected_examples"), "complete": value.get("complete")}
            for key in ("row_metrics", "retry_ablation_totals", "paired_bootstrap", "available_examples"):
                if key in value:
                    phase[key] = _public_numeric(value[key], key)
            evidence["phase_metrics"].append(phase)
    return evidence


def write_publications(records: list[dict[str, Any]], repo: Path) -> None:
    from research.curated.historical import variant_map
    from research.curated.historical_pipeline import reviewer_prompt
    from research.curated.historical_transport import CONTEXTUAL_RETRY_PROMPT, EXPRESSION_RETRY_PROMPT, WORD_RETRY_PROMPT
    historical_variants = variant_map()
    configs = repo / "research/configs"
    reports = repo / "research/reports"
    configs.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    for record in records:
        experiment_id = record["experiment_id"]
        spec = next((item for item in ROOT_SPECS if item["id"] == experiment_id), None)
        variant = {}
        historical = historical_variants.get(experiment_id)
        if historical is not None:
            variant = {
                "authorized_change": historical.authorized_change,
                "detector_view": "historical frozen view; see curated source seam",
                "reasoning_effort": historical.reasoning,
                "maximum_targets": historical.maximum_targets if historical.maximum_targets is not None else "UNCAPPED",
                "corrective_retries": historical.corrective_retries,
            }
        config = {
            "schema_version": 2,
            "experiment_id": experiment_id,
            "question": record.get("question"),
            "authorized_change": variant.get("authorized_change", record.get("variation")),
            "historical_status": record.get("status"),
            "logical_root": record.get("logical_root"),
            "generic_prompt": reviewer_prompt("{sentence}", "{target}"),
            "retry_prompt": WORD_RETRY_PROMPT if experiment_id == "low-word-only-retry" else CONTEXTUAL_RETRY_PROMPT if experiment_id == "low-unigram-retry" else EXPRESSION_RETRY_PROMPT,
            "inference_fields": {
                "sent": ["model", "stream", "store", "input", "filled_dataset_text", "include_reasoning", "reasoning"],
                "omitted": ["conversation_history", "gold_text", "private_response_body", "credential_value"],
            },
            "limits": {
                "request_count": "preserved per record",
                "target_count": variant.get("maximum_targets", "UNKNOWN"),
                "corrective_retry_count": variant.get("corrective_retries", "UNKNOWN"),
                "workers": "preserved per record",
                "timeout": "preserved per record",
            },
            "resource_identity": {
                "data": "private preserved identity; rows excluded",
                "index": "private verified identity; path excluded",
                "english": "private preserved attestation identity; values excluded unless numeric projection",
                "source": "research/registry/source-manifest.json",
                "environment": "private preserved environment identity; no import/network side effect",
            },
            "result_destination": "research/results/study-evidence.json.gz",
            "reproduction": {
                "entrypoint": "python3 -B -m research.tools.reproduce",
                "credential_reference": "RESEARCH_CREDENTIAL_REF",
                "requires_explicit_live_authorization": True,
                "default_network_calls": 0,
                "default_model_calls": 0,
            },
            "source_modules": list(historical.source_modules) if historical is not None else ["research/curated/historical.py"],
        }
        (configs / f"{experiment_id}.json").write_text(json.dumps(config, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        metrics = record.get("metrics", {})
        lines = [f"# {experiment_id}", "", "Data-free projection of one preserved historical record. This is an archival result, not a new experiment, semantic ground truth, product claim, or release decision.", "", "## Identity and question", "", f"- Question: {record.get('question', 'UNKNOWN')}", f"- Authorized change: {record.get('variation', 'UNKNOWN')}", f"- Status: `{record.get('status', 'UNKNOWN')}`; an old `RUNNING` marker is not completion.", f"- Private logical root: `{record.get('logical_root', 'UNKNOWN')}`; native path and payloads are not published.", "", "## Configuration projection", "", f"- Generic prompt: `{GENERIC_PROMPT}`", "- Sent fields: model, preserved reasoning setting, generic prompt, bounded target metadata.", "- Omitted fields: conversation history, filled dataset text, gold strings, private response bodies, credentials.", "- Detector/gate/retry limits: preserved from the source record; `UNKNOWN` is retained where the source did not expose a value.", "- Resource identities: data, index, English attestation, source, and environment are referenced by identity only; no private path is a runtime dependency.", "", "## Numeric evidence", "", "The complete data-free numeric projection is linked from [study-evidence](../results/study-evidence.json.gz). Per-case/trial fields retain counts, calls, timing/status where available. Text, proposals, references, filled prompts, response bodies, and private result identities are excluded.", "", "| Metric | Value |", "| --- | ---: |"]
        for key, value in sorted(metrics.items()):
            if key == "trial_metrics" or isinstance(value, (dict, list)):
                continue
            if isinstance(value, (int, float, bool, str)):
                lines.append(f"| `{key}` | `{value}` |")
        lines += ["", "## Child runs and phases", "", "| Child ID | Status | Source hash | Result hash |", "| --- | --- | --- | --- |"]
        for child in record.get("child_runs", []):
            lines.append(f"| `{child.get('id')}` | `{child.get('status')}` | `{child.get('source_hash') or 'UNAVAILABLE'}` | `{child.get('result_hash') or 'UNAVAILABLE'}` |")
        if not record.get("child_runs"):
            lines.append("| none enumerated | `NOT_APPLICABLE` | `UNAVAILABLE` | `UNAVAILABLE` |")
        lines += ["", "## Interpretation and limitations", "", REPORT_NOTES.get(experiment_id, "The preserved numerical result is reported without adding a semantic label."), "", "Strategic semantic assessments, where present, are not human ground truth. Exact-gold matches, custom alignment, official scores, preservation, detector-only counts, retry effects, and remote access status remain separate. Non-reference edits are not called harmful. Missing historical source/evidence is marked unavailable rather than filled from the latest baseline.", "", "## Reproduction and source links", "", f"- [Configuration](../configs/{experiment_id}.json)", "- [Experiment catalog](../registry/experiments.json)", "- [Source manifest](../registry/source-manifest.json)", "- [Archive and relocation catalog](../registry/archive-catalog.json)", "- [Curated source closure](../curated/)", "", "Offline replay is the only default. Live execution requires explicit caller-owned input/index/result roots, endpoint/model, credential reference, and bounded resource budget; this round made zero model calls.", ""]
        (reports / f"{experiment_id}.md").write_text("\n".join(lines), encoding="utf-8")


def write_numeric_evidence(records: list[dict[str, Any]], home: Path, repo: Path) -> None:
    destination = repo / "research/results/study-evidence.json.gz"
    payload = {
        "schema_version": 2,
        "kind": "data-free-historical-numeric-evidence",
        "model_calls_during_curation": 0,
        "field_exclusions": ["sentences", "gold strings", "filled prompts", "response bodies", "private result identities"],
        "studies": [_study_evidence(home, record) for record in records],
    }
    encoded = (json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    with gzip.GzipFile(filename=str(destination), mode="wb", mtime=0) as handle:
        handle.write(encoded)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--strategic-home", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("research/registry"))
    parser.add_argument("--existing-census", type=Path, help="reuse a preserved exact census from an interrupted local preparation")
    parser.add_argument("--native-root", type=Path, default=Path(os.environ["RESEARCH_NATIVE_ROOT"]) if os.environ.get("RESEARCH_NATIVE_ROOT") else None)
    args = parser.parse_args(argv)
    records = experiment_records(args.strategic_home)
    args.output.mkdir(parents=True, exist_ok=True)
    write_publications(records, args.repo_root)
    write_numeric_evidence(records, args.strategic_home, args.repo_root)
    result_map = result_projections(args.strategic_home, records, args.repo_root / "research/results")
    source_map = source_manifest(args.repo_root, args.strategic_home, args.output, args.native_root)
    rows, class_counts = (
        census_from_existing(args.existing_census, source_map, result_map)
        if args.existing_census
        else census(args.strategic_home, records, source_map, result_map)
    )
    (args.output / "experiments.json").write_text(json.dumps({"schema_version": 3, "scope": "all enumerated experiment and recovery roots plus stable child runs/phases and one non-benchmark diagnostic", "source_closure": "research/registry/source-manifest.json", "numeric_projections": "research/results/*.json.gz", "publication_projections": "research/reports/*.md and research/configs/*.json", "experiments": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "archive-catalog.json").write_text(json.dumps(archive_catalog(args.strategic_home), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    census_payload = {"schema_version": 2, "scope": "complete file-level census from exact owner manifests or verified native traversal", "entries": rows}
    with gzip.GzipFile(filename=str(args.output / "file-census.json.gz"), mode="wb", mtime=0) as handle:
        handle.write((json.dumps(census_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode())
    (args.output / "file-census.json").write_text(json.dumps({"schema_version": 2, "full_census": "file-census.json.gz", "entries": len(rows), "classifications": class_counts, "roots": len(records) - 1, "private_only_payloads": "All unprojected source/result/data/trace files remain private-only; exact hashes are in the compressed census."}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"experiments": len(records), "child_runs": sum(len(record.get("child_runs", [])) for record in records), "file_entries": len(rows), "classifications": class_counts, "numeric_projections": len(result_map) + 1, "model_calls": 0}, default=dict, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
