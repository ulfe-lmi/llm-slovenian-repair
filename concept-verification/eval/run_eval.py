"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Eval runner."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import canonical_bytes, load_json, sha256_file  # noqa: E402
from corpus import Corpus  # noqa: E402
from detector import Candidate, candidate_summary, detect, tokenize  # noqa: E402
from eval.common import (  # noqa: E402
    aggregate_candidates,
    dataset_identity,
    file_sha256,
    load_cases,
)
from protected import Interval, is_protected, protected_intervals  # noqa: E402
from qwen_client import Proposal, ResponsesReviewer, ReviewerError, prompt  # noqa: E402
from repair import Acceptance, accept, apply_edits  # noqa: E402


def _run_detector(
    cases: list[dict[str, Any]], corpus: Corpus, mode: str, threshold: int
) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]]]:
    by_id: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        text = str(case["text"])
        candidates = detect(
            text,
            corpus,
            protected_intervals(text),
            mode=mode,
            threshold=threshold,
        )
        by_id[str(case["id"])] = candidate_summary(candidates)
    return aggregate_candidates(cases, by_id), by_id


def _candidate(value: dict[str, Any]) -> Candidate:
    evidence = value.get("evidence")
    if not isinstance(evidence, dict):
        raise ValueError("candidate evidence is not an object")
    return Candidate(
        int(value["start"]),
        int(value["end"]),
        str(value["text"]),
        float(value["score"]),
        evidence,
    )


def _proposal_dict(proposal: Proposal | None) -> dict[str, Any] | None:
    if proposal is None:
        return None
    return {
        "keep": proposal.keep,
        "replacement": proposal.replacement,
        "needs_wider_edit": proposal.needs_wider_edit,
    }


def _acceptance_dict(decision: Acceptance) -> dict[str, Any]:
    return {
        "accepted": decision.accepted,
        "reason": decision.reason,
        "replacement": decision.replacement,
    }


def _protected_diff_count(
    original: str, repaired: str, edits: list[tuple[int, int, str]], intervals: list[Interval]
) -> int:
    differences = 0
    for interval in intervals:
        if interval.end > len(original):
            continue
        shift = sum(
            len(replacement) - (end - start)
            for start, end, replacement in edits
            if end <= interval.start
        )
        start = interval.start + shift
        if (
            repaired[start : start + interval.end - interval.start]
            != original[interval.start : interval.end]
        ):
            differences += 1
    return differences


def _assert_patch_invariants(
    original: str,
    repaired: str,
    edits: list[tuple[int, int, str]],
    intervals: list[Interval],
) -> None:
    ordered = sorted(edits)
    cursor = 0
    expected: list[str] = []
    for start, end, replacement in ordered:
        if start < cursor:
            raise AssertionError("evaluation edits overlap")
        expected.append(original[cursor:start])
        expected.append(replacement)
        cursor = end
    expected.append(original[cursor:])
    if "".join(expected) != repaired:
        raise AssertionError("patch changed an outside-edit slice")
    if _protected_diff_count(original, repaired, ordered, intervals):
        raise AssertionError("patch changed protected content")
    for interval in intervals:
        if any(start < interval.end and end > interval.start for start, end, _ in ordered):
            raise AssertionError("accepted edit intersects protected content")
        if not is_protected(interval.start, interval.end, intervals):
            raise AssertionError("protected interval was not recognized")


def _token_neighbors(
    text: str, candidate: Candidate, intervals: list[Interval]
) -> tuple[str | None, str | None]:
    tokens = tokenize(text, intervals)
    index = next((i for i, token in enumerate(tokens) if token.start == candidate.start), None)
    if index is None:
        return None, None
    left = tokens[index - 1].key if index else None
    right = tokens[index + 1].key if index + 1 < len(tokens) else None
    return left, right


def _reviewer_correct(
    case: dict[str, Any], candidate: Candidate, proposal: Proposal | None
) -> bool:
    if candidate.start != int(case["start"]) or candidate.end != int(case["end"]):
        return False
    if proposal is None:
        return False
    if not bool(case["known_error"]):
        return proposal.keep and proposal.replacement is None and not proposal.needs_wider_edit
    return (
        not proposal.keep
        and proposal.replacement == case.get("gold")
        and not proposal.needs_wider_edit
    )


def _base_ablation(cases: list[dict[str, Any]]) -> dict[str, Any]:
    known = sum(bool(case["known_error"]) for case in cases)
    return {
        "cases": len(cases),
        "known_errors": known,
        "known_errors_remaining": known,
        "candidates": 0,
        "candidate_recall": 0.0,
        "candidate_precision": 0.0,
        "changed": 0,
        "accepted_edits": 0,
        "exact_gold_correct_repairs": 0,
        "harmful_edits": 0,
        "missed_known_errors": known,
        "end_to_end_recovery": 0.0,
        "protected_changes": 0,
    }


def _controlled_metrics(
    cases: list[dict[str, Any]],
    candidate_map: dict[str, list[dict[str, Any]]],
    case_records: list[dict[str, Any]],
) -> dict[str, Any]:
    selected_candidates = [item for values in candidate_map.values() for item in values]
    known = sum(bool(case["known_error"]) for case in cases)
    candidate_hits = sum(
        any(
            item["start"] == case["start"] and item["end"] == case["end"]
            for item in candidate_map.get(str(case["id"]), [])
        )
        for case in cases
        if case["known_error"]
    )
    labelled_reviewer = 0
    reviewer_correct = 0
    proposed = 0
    accepted = 0
    correct = 0
    harmful = 0
    missed = 0
    protected_changes = 0
    changed = 0
    unlabelled_accepted = 0
    for case, record in zip(cases, case_records, strict=True):
        decisions = record["decisions"]
        if not isinstance(decisions, list):
            raise ValueError("case decisions are not a list")
        for value in decisions:
            if not isinstance(value, dict):
                raise ValueError("case decision is not an object")
            candidate_value = value.get("candidate")
            if not isinstance(candidate_value, dict):
                raise ValueError("decision candidate is not an object")
            candidate = _candidate(candidate_value)
            proposal_value = value.get("proposal")
            proposal: Proposal | None = None
            if isinstance(proposal_value, dict):
                replacement = proposal_value.get("replacement")
                if replacement is not None and not isinstance(replacement, str):
                    raise ValueError("proposal replacement is not a string")
                proposal = Proposal(
                    bool(proposal_value.get("keep")),
                    replacement,
                    bool(proposal_value.get("needs_wider_edit")),
                )
            is_labelled_target = candidate.start == int(case["start"]) and candidate.end == int(
                case["end"]
            )
            if is_labelled_target:
                labelled_reviewer += 1
                reviewer_correct += _reviewer_correct(case, candidate, proposal)
            if (
                proposal is not None
                and not proposal.keep
                and proposal.replacement
                and not proposal.needs_wider_edit
            ):
                proposed += 1
            acceptance = value.get("acceptance")
            if not isinstance(acceptance, dict) or not acceptance.get("accepted"):
                continue
            accepted += 1
            if is_labelled_target and bool(case["known_error"]):
                if acceptance.get("replacement") == case.get("gold"):
                    correct += 1
                else:
                    harmful += 1
            elif not bool(case["known_error"]):
                harmful += 1
            else:
                unlabelled_accepted += 1
        changed += int(record["changed"])
        protected_changes += int(record["protected_difference_count"])
        if bool(case["known_error"]) and not bool(record["exact_gold_repair"]):
            missed += 1
    reviewer_accuracy: float | str = (
        reviewer_correct / labelled_reviewer if labelled_reviewer else "NO_LABELLED_CANDIDATE"
    )
    recovery = correct / known if known else 0.0
    harmful_fraction: float | str = harmful / accepted if accepted else "NO_ACCEPTED_EDITS"
    return {
        "cases": len(cases),
        "known_errors": known,
        "known_errors_remaining": missed,
        "candidates": len(selected_candidates),
        "candidate_recall": candidate_hits / known if known else 0.0,
        "candidate_precision": candidate_hits / len(selected_candidates)
        if selected_candidates
        else 0.0,
        "reviewer_calls": sum(int(record["reviewer_calls"]) for record in case_records),
        "reviewer_labelled_candidates": labelled_reviewer,
        "reviewer_correct": reviewer_correct,
        "reviewer_accuracy": reviewer_accuracy,
        "proposed_replacements": proposed,
        "accepted_edits": accepted,
        "exact_gold_correct_repairs": correct,
        "harmful_edits": harmful,
        "harmful_fraction_accepted": harmful_fraction,
        "missed_known_errors": missed,
        "end_to_end_recovery": recovery,
        "changed_cases": changed,
        "protected_changes": protected_changes,
        "unlabelled_accepted_edits": unlabelled_accepted,
    }


def _evaluate(
    cases: list[dict[str, Any]],
    corpus: Corpus,
    candidate_map: dict[str, list[dict[str, Any]]],
    reviewer: ResponsesReviewer | None,
    prompt_variant: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for case in cases:
        text = str(case["text"])
        intervals = protected_intervals(text)
        decisions: list[dict[str, Any]] = []
        edits: list[tuple[int, int, str]] = []
        reviewer_calls = 0
        for raw_candidate in candidate_map.get(str(case["id"]), []):
            candidate = _candidate(raw_candidate)
            left, right = _token_neighbors(text, candidate, intervals)
            proposal: Proposal | None = None
            acceptance = Acceptance(False, "reviewer-not-configured", None)
            failure: str | None = None
            started = time.monotonic()
            if reviewer is not None:
                reviewer_calls += 1
                try:
                    proposal = reviewer.review(text, candidate.text, prompt_variant)
                    acceptance = accept(
                        text,
                        candidate,
                        proposal,
                        corpus,
                        intervals,
                        left=left,
                        right=right,
                    )
                except ReviewerError:
                    failure = "reviewer-error"
                    acceptance = Acceptance(False, failure, None)
                except (ValueError, TypeError):
                    failure = "reviewer-invalid"
                    acceptance = Acceptance(False, failure, None)
            decisions.append(
                {
                    "candidate": candidate.as_dict(),
                    "neighbors": {"left": left, "right": right},
                    "evidence": candidate.evidence,
                    "proposal": _proposal_dict(proposal),
                    "acceptance": _acceptance_dict(acceptance),
                    "failure": failure,
                    "reviewer_timing_seconds": round(time.monotonic() - started, 6)
                    if reviewer is not None
                    else 0.0,
                }
            )
            if acceptance.accepted and acceptance.replacement is not None:
                edits.append((candidate.start, candidate.end, acceptance.replacement))
        repaired = apply_edits(text, edits, intervals)
        _assert_patch_invariants(text, repaired, edits, intervals)
        gold = case.get("gold")
        exact_gold = (
            bool(case["known_error"])
            and isinstance(gold, str)
            and repaired == text[: int(case["start"])] + gold + text[int(case["end"]) :]
        )
        records.append(
            {
                "id": case["id"],
                "original": text,
                "repaired": repaired,
                "changed": int(repaired != text),
                "decisions": decisions,
                "reviewer_calls": reviewer_calls,
                "protected_difference_count": _protected_diff_count(
                    text, repaired, edits, intervals
                ),
                "exact_gold_repair": exact_gold,
                "apply_edits_calls": 1,
            }
        )
    return records, _controlled_metrics(cases, candidate_map, records)


def _ablation(
    cases: list[dict[str, Any]],
    summary: dict[str, Any],
    records: list[dict[str, Any]],
    candidate_map: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    result = dict(summary)
    result["candidate_map"] = candidate_map
    result["case_count"] = len(cases)
    result["records_with_text"] = sum(bool(record.get("original")) for record in records)
    return result


def _validate_frozen(
    config_path: Path, heldout_path: Path, index: Path, frozen: dict[str, Any]
) -> None:
    if frozen.get("config_sha256") != sha256_file(config_path):
        raise SystemExit("frozen identity mismatch; held-out tuning is refused")
    if frozen.get("heldout") != dataset_identity(heldout_path):
        raise SystemExit("frozen identity mismatch; held-out tuning is refused")
    if frozen.get("version") != "concept-v1-frozen":
        raise SystemExit("unsupported frozen experiment")
    if frozen.get("mode") != "local-context" or int(frozen.get("threshold", -1)) != 3:
        raise SystemExit("frozen detector selection mismatch")
    if frozen.get("prompt_variant") != "frozen-v1":
        raise SystemExit("frozen prompt selection mismatch")
    if index.exists() and frozen.get("index_sha256") != file_sha256(index):
        raise SystemExit("frozen index identity mismatch")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE"
    )
    parser.add_argument("--phase", choices=("dev", "heldout"))
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument(
        "--index", type=Path, default=Path("concept-verification/eval/results/index.sqlite")
    )
    parser.add_argument("--results", type=Path)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--frozen", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--reviewer-url")
    parser.add_argument("--reviewer-model")
    parser.add_argument("--reviewer-profile", type=Path)
    parser.add_argument("--reviewer-timeout", type=float, default=30.0)
    args = parser.parse_args(argv)
    config = load_json(args.config)
    dev_path = args.config.parent / "cases/dev.jsonl"
    heldout_path = args.config.parent / "cases/heldout.jsonl"
    if args.freeze:
        if args.output is None:
            raise SystemExit("--freeze requires --output")
        frozen = {
            "version": "concept-v1-frozen",
            "config_sha256": sha256_file(args.config),
            "dev": dataset_identity(dev_path),
            "heldout": dataset_identity(heldout_path),
            "index_sha256": file_sha256(args.index) if args.index.exists() else None,
            "mode": config["selected_mode"],
            "threshold": config["selected_threshold"],
            "prompt_variant": config["selected_prompt_variant"],
            "prompt_template_sha256": hashlib.sha256(
                prompt("{{sentence}}", "{{target}}", str(config["selected_prompt_variant"])).encode(
                    "utf-8"
                )
            ).hexdigest(),
            "threshold_settings": config["threshold_settings"],
            "prompt_variants": config["prompt_variants"],
            "decision_thresholds": config["decision"],
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(canonical_bytes(frozen))
        print(
            json.dumps(
                {"frozen": str(args.output), "sha256": file_sha256(args.output)}, sort_keys=True
            )
        )
        return 0
    if args.phase is None or args.results is None:
        raise SystemExit("--phase and --results are required unless --freeze is used")
    cases = load_cases(dev_path if args.phase == "dev" else heldout_path)
    if args.phase == "heldout":
        if args.frozen is None or not args.frozen.exists():
            raise SystemExit("held-out execution requires frozen-experiment.json")
        _validate_frozen(args.config, heldout_path, args.index, load_json(args.frozen))
        # The selected local-context run is frozen; unigram-only is a same-threshold
        # ablation and does not participate in selection or reviewer calls.
        settings = [("local-context", 3), ("unigram-only", 3)]
        prompt_variant = "frozen-v1"
    else:
        settings = [
            (str(mode), int(threshold))
            for mode in config["detector_modes"]
            for threshold in config["threshold_settings"]
        ]
        if len(settings) > 8:
            raise SystemExit("development tuning exceeds four thresholds per mode")
        prompt_variant = str(config["selected_prompt_variant"])
    if not args.index.exists():
        raise SystemExit("verified external SQLite index is required")
    reviewer_args = (args.reviewer_url, args.reviewer_model, args.reviewer_profile)
    if any(value is not None for value in reviewer_args) and not all(
        value is not None for value in reviewer_args
    ):
        raise SystemExit("reviewer URL, model, and profile must be supplied together")
    reviewer = (
        ResponsesReviewer(
            str(args.reviewer_url),
            str(args.reviewer_model),
            timeout=args.reviewer_timeout,
            profile=args.reviewer_profile,
        )
        if all(value is not None for value in reviewer_args)
        else None
    )
    summaries: list[dict[str, Any]] = []
    selected: dict[str, list[dict[str, Any]]] = {}
    unigram_candidates: dict[str, list[dict[str, Any]]] = {}
    local_candidates: dict[str, list[dict[str, Any]]] = {}
    with Corpus(args.index) as corpus:
        for mode, threshold in settings:
            summary, candidates = _run_detector(cases, corpus, mode, threshold)
            summary.update({"mode": mode, "threshold": threshold})
            summaries.append(summary)
            if mode == "unigram-only" and threshold == 3:
                unigram_candidates = candidates
            if mode == "local-context" and threshold == 3:
                local_candidates = candidates
            if mode == config["selected_mode"] and threshold == config["selected_threshold"]:
                selected = candidates
        records, full_metrics = _evaluate(cases, corpus, selected, reviewer, prompt_variant)
    raw = _base_ablation(cases)
    detector_summary = next(
        summary
        for summary in summaries
        if summary["mode"] == "local-context" and summary["threshold"] == 3
    )
    detector_only = dict(detector_summary)
    detector_known_remaining = detector_only["known_errors"] - sum(
        1
        for case in cases
        if case["known_error"]
        and any(
            item["start"] == case["start"] and item["end"] == case["end"]
            for item in selected.get(str(case["id"]), [])
        )
    )
    detector_only.update(
        {
            "known_errors_remaining": detector_known_remaining,
            "accepted_edits": 0,
            "exact_gold_correct_repairs": 0,
            "harmful_edits": 0,
            "missed_known_errors": detector_known_remaining,
            "end_to_end_recovery": 0.0,
            "protected_changes": 0,
        }
    )
    reviewer_without_application = dict(full_metrics)
    reviewer_without_application.update(
        {
            "accepted_edits": 0,
            "exact_gold_correct_repairs": 0,
            "harmful_edits": 0,
            "changed_cases": 0,
            "known_errors_remaining": full_metrics["known_errors"],
            "missed_known_errors": full_metrics["known_errors"],
            "end_to_end_recovery": 0.0,
            "protected_changes": 0,
        }
    )
    result = {
        "phase": args.phase,
        "config_sha256": sha256_file(args.config),
        "dataset": dataset_identity(dev_path if args.phase == "dev" else heldout_path),
        "index_sha256": file_sha256(args.index),
        "decision_thresholds": config["decision"],
        "eligible_words": sum(
            len(tokenize(str(case["text"]), protected_intervals(str(case["text"]))))
            for case in cases
        ),
        "settings_evaluated": summaries,
        "selected_candidates": selected,
        "cases": records,
        "controlled_metrics": full_metrics,
        "ablations": {
            "raw": _ablation(cases, raw, [], {}),
            "detector_only": _ablation(cases, detector_only, [], selected),
            "reviewer_without_application": _ablation(
                cases, reviewer_without_application, records, selected
            ),
            "full_conservative_pipeline": _ablation(cases, full_metrics, records, selected),
            "unigram_only": {
                **next(
                    summary
                    for summary in summaries
                    if summary["mode"] == "unigram-only" and summary["threshold"] == 3
                ),
                "candidate_map": unigram_candidates,
            },
            "local_context": {**detector_summary, "candidate_map": local_candidates},
        },
        "reviewer": {
            "configured": reviewer is not None,
            "calls": full_metrics["reviewer_calls"],
            "max_per_response": 4,
            "retry": False,
            "status": "MEASURED" if reviewer is not None else "NOT RUN",
        },
        "ablation_status": {
            "raw": "MEASURED",
            "detector_only": "MEASURED",
            "reviewer_without_application": "MEASURED" if reviewer is not None else "NOT RUN",
            "full_conservative_pipeline": "MEASURED" if reviewer is not None else "NOT RUN",
            "unigram_only": "MEASURED",
            "local_context": "MEASURED",
        },
    }
    output = args.results / f"{args.phase}.json"
    args.results.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_bytes(result))
    print(
        json.dumps(
            {"phase": args.phase, "output": str(output), "sha256": file_sha256(output)},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
