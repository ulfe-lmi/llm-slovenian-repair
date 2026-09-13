"""Data-free port of the preserved DASSLE u/v analyzer."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Any

from .historical_scoring import edit_key, edits, overlap, prf, tokens


def classify(source_tokens: list[str], replacement_tokens: list[str]) -> list[str]:
    """Classify literal token operations only; never infer linguistic meaning."""
    tags: list[str] = []
    if source_tokens != replacement_tokens and [x for x in source_tokens if x not in {",", "."}] == [x for x in replacement_tokens if x not in {",", "."}]:
        tags.append("comma_period_only")
    if len(source_tokens) == len(replacement_tokens) == 1 and source_tokens[0].isalpha() and replacement_tokens[0].isalpha():
        source, replacement = source_tokens[0].casefold(), replacement_tokens[0].casefold()
        if {source, replacement} == {"k", "h"}:
            tags.append("kh_standalone")
        if {source, replacement} == {"s", "z"}:
            tags.append("sz_standalone")
        if {source, replacement} == {"u", "v"}:
            tags.append("uv_standalone")
        if len(source) > 1 and len(source) == len(replacement):
            differences = [i for i, (left, right) in enumerate(zip(source, replacement, strict=True)) if left != right]
            if len(differences) == 1 and {source[differences[0]], replacement[differences[0]]} == {"u", "v"}:
                tags.append("uv_initial" if differences[0] == 0 else "uv_noninitial")
        if len(source) > 1 and len(replacement) > 1 and {source[0], replacement[0]} == {"u", "v"} and source[1:] != replacement[1:]:
            tags.append("opposed_initial_uv_with_other_changes_NOT_proven_mixup")
        if len(source) > 1 and source[0] == "v" and source[1:] == replacement:
            tags.append("leading_v_deleted_NOT_uv_substitution")
        if len(replacement) > 1 and replacement[0] == "v" and replacement[1:] == source:
            tags.append("leading_v_added_NOT_uv_substitution")
    return tags


def tagged(source: str, output: str | None) -> list[dict[str, Any]]:
    source_tokens = tokens(source)
    result: list[dict[str, Any]] = []
    for change in edits(source, output):
        source_values = [item[0] for item in source_tokens[change["source_token_start"] : change["source_token_end"]]]
        result.append({**change, "source_tokens": source_values, "tags": classify(source_values, change["replacement_tokens"])})
    return result


def evaluate(rows: Iterable[Mapping[str, Any]], excluded: Iterable[str] = ()) -> dict[str, dict[str, Any]]:
    excluded_set = set(excluded)
    output: dict[str, dict[str, Any]] = {}
    for method in ("M0", "M1", "M2", "M3"):
        counts = Counter()
        for row in rows:
            reference = row.get("reference")
            if not isinstance(reference, str):
                continue
            source = str(row["input"])
            gold = [item for item in tagged(source, reference) if not set(item["tags"]) & excluded_set]
            predicted = row.get("results", {}).get(method, {}) if isinstance(row.get("results"), Mapping) else {}
            output_text = predicted.get("output") if isinstance(predicted, Mapping) else None
            prediction = [item for item in tagged(source, output_text) if not set(item["tags"]) & excluded_set]
            gold_keys = {edit_key(item) for item in gold}
            prediction_keys = {edit_key(item) for item in prediction}
            candidates = row.get("candidates", [])
            counts.update(
                N=1,
                gold_edits=len(gold_keys),
                tp=len(gold_keys & prediction_keys),
                fp=len(prediction_keys - gold_keys),
                fn=len(gold_keys - prediction_keys),
                detector_covered=sum(any(overlap(candidate, item) for candidate in candidates if isinstance(candidate, Mapping)) for item in gold),
                model_operational_failures=bool(predicted.get("operational_failure")) if isinstance(predicted, Mapping) else False,
                changed_sentences=output_text != source,
            )
        output[method] = {**dict(counts), **prf(counts["tp"], counts["fp"], counts["fn"])}
    return output


def analyze(source_rows: list[Mapping[str, Any]], result_rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Analyze explicitly supplied rows; no filesystem, model, or network access."""
    by_id = {str(row.get("id", index)): row for index, row in enumerate(source_rows)}
    joined: list[dict[str, Any]] = []
    for index, result in enumerate(result_rows):
        source = by_id.get(str(result.get("id", index)), {})
        joined.append({**source, **result})
    views = evaluate(joined)
    tags = Counter(
        tag
        for row in joined
        for item in tagged(str(row["input"]), row.get("reference") if isinstance(row.get("reference"), str) else None)
        for tag in item["tags"]
    )
    return {
        "status": "ANALYZED_LITERAL_EDIT_UNITS",
        "rows_scanned": len(joined),
        "reference_rows": sum(isinstance(row.get("reference"), str) for row in joined),
        "views": views,
        "literal_pattern_units": dict(tags),
        "new_model_calls": 0,
        "network_calls": 0,
    }


def run_audit_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Execute the analyzer over caller-provided synthetic/saved rows."""
    source_rows = [{key: value for key, value in row.items() if key not in {"results", "candidates"}} for row in records]
    return analyze(source_rows, records)
