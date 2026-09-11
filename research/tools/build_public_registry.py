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
    {"id": "low-unigram-retry", "root": "experiments/low-unigram-retry-20260909.Wb0TI7", "kind": "variant", "variation": "low-thinking unigram post-check and one corrective retry", "status": "COMPLETED", "question": "What changed when unigram-uncertain proposals received one word-only retry?"},
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
    ("experiments/large-evaluation-uncapped-20260910.faME3U/common.py", "research/curated/pipeline.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/pipeline_bridge.py", "research/curated/pipeline.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/detector_uncapped.py", "research/curated/detector.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/methods.py", "research/curated/methods.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/metrics.py", "research/curated/scoring.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/aggregate.py", "research/curated/aggregate.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/bootstrap_stats.py", "research/curated/scoring.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/adapters.py", "research/curated/adapters.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/official_score.py", "research/curated/official_score.py"),
    ("experiments/large-evaluation-uncapped-20260910.faME3U/transport.py", "research/curated/transport.py"),
    ("experiments/ten-run-english-preserve-low-20260909.AQnnRH/english_preserve.py", "research/curated/english_preserve.py"),
    ("experiments/ten-run-english-preserve-low-20260909.AQnnRH/expression_retry.py", "research/curated/review.py"),
    ("experiments/ten-run-english-preserve-low-20260909.AQnnRH/hyphen_detector.py", "research/curated/detector.py"),
    ("experiments/ten-run-english-preserve-low-20260909.AQnnRH/run_pipeline.py", "research/curated/pipeline.py"),
    ("experiments/low-word-only-retry-20260909.0Hk0P9/retry.py", "research/curated/gating.py"),
    ("experiments/low-word-only-retry-20260909.0Hk0P9/continue_whitespace.py", "research/curated/gating.py"),
)

SAFE_NUMERIC = {
    "applied_edits", "applied_retry_edits", "available_case_instances_including_partial", "available_eligible_word_instances_including_partial", "available_known_error_instances_including_partial", "cases", "changed_controls", "complete_trials", "completed_case_outputs", "completed_phases", "completed_trials", "corrective_calls", "distinct_calls", "eligible_words", "exact_gold_repairs", "failed", "first_calls", "fresh_reviewer_calls", "gold_edit_units", "inherited_calls", "method_records", "missed_gold_errors", "model_calls", "new_corrective_calls", "new_model_calls", "operational_failures", "preservation_cases", "proposed_edits", "proposed_first_edits", "qualified_calls", "reasoning_tokens", "record_count", "retry_calls", "scheduled_trials", "stopped_trials", "total_calls", "trials", "unchanged_controls", "verified_checkpoints", "workers", "submissions", "spelling_cases", "new_calls", "unique_model_calls",
}
SAFE_TEXT = {"status", "outcome", "mode", "deployment", "remote_scoring", "inference_coordinator_status"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json(path: Path) -> Any:
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


def source_manifest(repo: Path, home: Path, output: Path) -> dict[tuple[str, str], str]:
    destinations: dict[tuple[str, str], str] = {}
    rows = []
    for original, destination in SOURCE_MAP:
        source = repo / original if original.startswith("concept-verification/") else home / original
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
        rows.append({"original_logical_path": original, "original_sha256": original_hash, "curated_path": destination, "curated_sha256": sha256(target), "disposition": "published-curated/redacted", "transformations": ["removed historical absolute paths", "externalized input/index/output roots", "kept experimental semantics and variant boundaries"]})
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--strategic-home", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("research/registry"))
    parser.add_argument("--existing-census", type=Path, help="reuse a preserved exact census from an interrupted local preparation")
    args = parser.parse_args(argv)
    records = experiment_records(args.strategic_home)
    args.output.mkdir(parents=True, exist_ok=True)
    result_map = result_projections(args.strategic_home, records, args.repo_root / "research/results")
    source_map = source_manifest(args.repo_root, args.strategic_home, args.output)
    rows, class_counts = (
        census_from_existing(args.existing_census, source_map, result_map)
        if args.existing_census
        else census(args.strategic_home, records, source_map, result_map)
    )
    (args.output / "experiments.json").write_text(json.dumps({"schema_version": 2, "scope": "all enumerated experiment and recovery roots plus one non-benchmark diagnostic", "source_closure": "research/registry/source-manifest.json", "numeric_projections": "research/results/*.json.gz", "experiments": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output / "archive-catalog.json").write_text(json.dumps(archive_catalog(args.strategic_home), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    census_payload = {"schema_version": 2, "scope": "complete file-level census from exact owner manifests or verified native traversal", "entries": rows}
    with gzip.GzipFile(filename=str(args.output / "file-census.json.gz"), mode="wb", mtime=0) as handle:
        handle.write((json.dumps(census_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode())
    (args.output / "file-census.json").write_text(json.dumps({"schema_version": 2, "full_census": "file-census.json.gz", "entries": len(rows), "classifications": class_counts, "roots": len(records) - 1, "private_only_payloads": "All unprojected source/result/data/trace files remain private-only; exact hashes are in the compressed census."}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"experiments": len(records), "file_entries": len(rows), "classifications": class_counts, "numeric_projections": len(result_map), "model_calls": 0}, default=dict, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
