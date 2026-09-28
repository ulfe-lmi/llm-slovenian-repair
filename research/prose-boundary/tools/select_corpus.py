"""008-a Increment 2: deterministic representative-corpus selection.

Selects 100 real LLM output texts from the preserved private research roots
(007-i / 007-j / 007-m, directories cases/dassle-spelling and
cases/dassle-spelling-preservation), deduplicated by sha256 of the text bytes,
taking the first 100 in ascending sha256 order (config: fixed seedless
sampling).

Privacy (frozen rules): the private runtime parent is supplied at run time as
a CLI argument and never committed; raw text never leaves the private root and
never enters the receipt; the receipt carries counts/categories/hashes only.
No model calls are made.

Deterministic: identical inputs produce identical receipt bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG = HERE.parent / "config" / "experiment-008a.json"
DEFAULT_OUT = HERE.parent / "results" / "increment2" / "selection-receipt.json"

BENCHMARK_DIRS = ("cases/dassle-spelling", "cases/dassle-spelling-preservation")

# Data-free structural-prevalence markers (structure only; no content claims).
_MARKERS = {
    "fenced_code": re.compile(r"^\s*(```|~~~)", re.MULTILINE),
    "inline_code": re.compile(r"`[^`\n]+`"),
    "heading": re.compile(r"^\s{0,3}#{1,6}\s", re.MULTILINE),
    "list_marker": re.compile(r"^\s{0,3}(?:[-*+]|\d+[.)])\s", re.MULTILINE),
    "task_marker": re.compile(r"^\s{0,3}[-*+]\s+\[[ xX]\]\s", re.MULTILINE),
    "link_or_image": re.compile(r"!?\[[^\]\n]*\]\([^)\n]*\)"),
    "autolink": re.compile(r"<[a-zA-Z][a-zA-Z0-9+.-]*:[^>\s]+>"),
    "dollar_pair": re.compile(r"\$\S[\s\S]*?\$"),
    "table_pipe": re.compile(r"^\s*\|.*\|\s*$", re.MULTILINE),
    "html_tag": re.compile(r"</?[a-zA-Z][^>]*>"),
}


def structural_categories(text: str) -> list[str]:
    return [name for name, rx in _MARKERS.items() if rx.search(text)]


def load_population(runtime_root: Path) -> tuple[dict, dict]:
    """Return (population, source_counts). population: sha256 -> metadata."""
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    roots = config["increment2"]["corpus_selection"]["sources_logical_roots"]
    population: dict[str, dict] = {}
    source_counts: dict[str, dict] = {}
    for root_name in roots:
        root = runtime_root / root_name
        per_dir: dict[str, dict] = {}
        for rel in BENCHMARK_DIRS:
            dirpath = root / rel
            counts = {"case_files": 0, "inputs_read": 0, "skipped": []}
            per_dir[rel] = counts
            if not dirpath.is_dir():
                counts["error"] = "missing"
                continue
            for path in sorted(dirpath.glob("*.json")):
                counts["case_files"] += 1
                try:
                    doc = json.loads(path.read_text(encoding="utf-8"))
                    text = doc["dataset"]["input"]
                    if not isinstance(text, str) or not text:
                        raise ValueError("dataset.input not a non-empty string")
                except Exception as exc:  # fail closed, data-free record
                    counts["skipped"].append(
                        {"rel": str(path.relative_to(root)), "error": type(exc).__name__}
                    )
                    continue
                counts["inputs_read"] += 1
                sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
                if sha not in population:
                    population[sha] = {
                        "root": root_name,
                        "dir": rel,
                        "rel": str(path.relative_to(root)),
                        "chars": len(text),
                        "structural_categories": structural_categories(text),
                    }
        source_counts[root_name] = per_dir
    return population, source_counts


def select_sample(population: dict, sample_size: int) -> list[str]:
    return sorted(population.keys())[:sample_size]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runtime-root", required=True,
                    help="private research-runtime parent (never committed)")
    ap.add_argument("--sample-size", type=int, default=None)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    sel = config["increment2"]["corpus_selection"]
    sample_size = args.sample_size or sel["sample_size"]
    runtime_root = Path(args.runtime_root)
    if not runtime_root.is_dir():
        raise SystemExit(f"runtime root missing: {runtime_root}")

    population, source_counts = load_population(runtime_root)
    shas = select_sample(population, sample_size)
    if not shas:
        raise SystemExit("empty population")

    structural = sum(1 for s in shas if population[s]["structural_categories"])
    plain = len(shas) - structural
    category_totals: dict[str, int] = {}
    for s in shas:
        for c in population[s]["structural_categories"]:
            category_totals[c] = category_totals.get(c, 0) + 1

    pop_structural = sum(
        1 for meta in population.values() if meta["structural_categories"])
    pop_category_totals: dict[str, int] = {}
    for meta in population.values():
        for c in meta["structural_categories"]:
            pop_category_totals[c] = pop_category_totals.get(c, 0) + 1

    receipt = {
        "schema": "008a-selection-receipt/1",
        "order": "008-a",
        "increment": 2,
        "sources_logical": list(sel["sources_logical_roots"]),
        "benchmark_dirs": list(BENCHMARK_DIRS),
        "source_counts": source_counts,
        "population": {
            "total_input_records": sum(
                c["inputs_read"]
                for per_dir in source_counts.values()
                for c in per_dir.values()
            ),
            "unique_texts": len(population),
        },
        "sample": {
            "size": len(shas),
            "selection_rule": sel["sampling"],
            "sha256_ascending": shas,
        },
        "data_free_prevalence": {
            "note": "structure-only markers; no content claims. The sample is the "
                    "deterministic first-100 ascending-sha slice; population "
                    "prevalence characterizes the whole preserved corpus.",
            "sample": {
                "plain_prose_no_markers": plain,
                "with_any_structural_marker": structural,
                "marker_totals": dict(sorted(category_totals.items())),
            },
            "population": {
                "unique_texts": len(population),
                "with_any_structural_marker": pop_structural,
                "marker_totals": dict(sorted(pop_category_totals.items())),
            },
        },
        "representativeness_limitations": [
            "Corpus is the preserved 007 spelling-repair benchmark output "
            "(dassle-spelling and its preservation archive); it is dominated by "
            "plain Slovenian prose, so structural constructs are sparse.",
            "Per the order: the project-authored adversarial fixture suite is "
            "the structural ground truth; these real outputs are used for "
            "prevalence and disagreement observations only.",
            "No objective-009 confirmation examples were used; no new model "
            "calls were made; no new data was acquired.",
        ],
        "privacy": {
            "raw_text_in_receipt": False,
            "private_absolute_paths_in_receipt": False,
            "model_calls": 0,
            "fields_recorded": ["counts", "categories", "sha256", "relative case path"],
        },
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"population: {receipt['population']}")
    print(f"sample: {len(shas)} (plain {plain}, structural {structural})")
    print(f"sample markers: {receipt['data_free_prevalence']['sample']['marker_totals']}")
    print(f"population markers: {receipt['data_free_prevalence']['population']['marker_totals']}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
