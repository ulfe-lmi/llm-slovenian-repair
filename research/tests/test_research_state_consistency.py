"""Consistency test for research/RESEARCH-STATE.md (objective 007, round 007-o).

Re-derives every value in the embedded machine-readable block
(schema ``research-state-machine-v1``) from the primary records named in
section 1 of the document:

- reviewed Git identities (quarantined 007-n report bytes, 007-o order
  metadata at HEAD, remote main, committed frozen 007-m config);
- ``research/results/strategic-official-summary.json`` (official scorer);
- ``research/results/007-j-levenshtein-one-contextual-validator.json.gz``
  (baseline / 007-h / 007-j custom alignment, fresh-validator accounting);
- ``research/results/007-i-contextual-validator.json.gz`` (007-i stage);
- ``research/results/007-m-rank-ambiguous-levenshtein-candidates.json.gz``
  (007-m hybrid, census, lineage, preservation, latency);
- ``research/registry/experiments.json`` (24 registry entries, full-campaign8
  metrics);
- ``research/results/dassle.json.gz`` and
  ``research/results/dassle-preservation.json.gz`` (campaign custom
  end-to-end, preservation, retry ablation);
- ``oap/REPORT-HISTORY-INCIDENTS.json`` (frozen incident count).

CPU-only, offline, zero model/network calls (git subprocess reads only).
The test FAILS if any embedded number or identity in RESEARCH-STATE.md is
altered, and PASSES at the 007-o implementation head and report head.
"""

import gzip
import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = REPO_ROOT / "research" / "RESEARCH-STATE.md"
SCHEMA = "research-state-machine-v1"
REPORT_007O = "007-o-consolidate-research-state.md"
ORDER_007O = "oap/orders/007-o-consolidate-research-state.md"


def git(*args, binary=False):
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True,
        check=True,
    )
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def git_ok(*args):
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True,
    )
    return proc.returncode


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_gz_json(path: Path):
    with gzip.open(path, "rb") as handle:
        return json.load(handle)


def extract_machine_block(text: str) -> dict:
    blocks = re.findall(r"```json\n(.*?)\n```", text, flags=re.S)
    matching = [
        json.loads(body) for body in blocks if '"schema"' in body
    ]
    matching = [b for b in matching if b.get("schema") == SCHEMA]
    assert len(matching) == 1, (
        "expected exactly one %s block in RESEARCH-STATE.md, found %d"
        % (SCHEMA, len(matching))
    )
    return matching[0]


class ResearchStateConsistencyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = STATE_PATH.read_text(encoding="utf-8")
        cls.block = extract_machine_block(cls.text)
        # The Application-baseline driver runs the suite in a file-copy
        # pytest workspace that excludes .git; the git-identity assertions
        # need the real repository history and skip there. All numeric
        # re-derivation assertions still run in that workspace.
        cls.git_history_available = (REPO_ROOT / ".git").exists()

    # ------------------------------------------------------------------ #
    # 1. identities                                                       #
    # ------------------------------------------------------------------ #
    def test_quarantined_007n_git_identity(self):
        if not self.git_history_available:
            self.skipTest(
                "git history unavailable in this test workspace "
                "(file copy without .git); runs in a real checkout"
            )
        q = self.block["identities"]["quarantined_007n"]
        pub = q["publication_commit"]
        git("cat-file", "-e", pub)  # publication commit exists
        self.assertEqual(git("rev-parse", pub + "^"), q["implementation_parent"])
        self.assertEqual(
            git("rev-parse", "%s:%s" % (pub, q["report_path"])), q["report_blob"]
        )
        report_bytes = git("cat-file", "blob", q["report_blob"], binary=True)
        self.assertEqual(sha256_bytes(report_bytes), q["report_sha256"])
        order_bytes = git(
            "cat-file", "blob", git("rev-parse", "%s:%s" % (pub, q["order_path"])),
            binary=True,
        )
        self.assertEqual(sha256_bytes(order_bytes), q["order_sha256"])
        self.assertEqual(q["classification"], "INVALID_QUARANTINED")
        self.assertEqual(q["validation_error"], "REPORT_CHECK")

    def test_main_is_ancestor_of_reviewed_head(self):
        if not self.git_history_available:
            self.skipTest(
                "git history unavailable in this test workspace "
                "(file copy without .git); runs in a real checkout"
            )
        ident = self.block["identities"]
        main_sha = ident["main_sha"]
        head = ident["reviewed_branch_head_sha"]
        git("cat-file", "-e", main_sha + "^{commit}")
        self.assertEqual(
            git_ok("merge-base", "--is-ancestor", main_sha, head), 0
        )
        if git_ok("rev-parse", "--verify", "--quiet", "refs/remotes/origin/main") == 0:
            self.assertEqual(
                git("rev-parse", "refs/remotes/origin/main"), main_sha
            )

    def test_branch_and_pr_match_committed_007o_order(self):
        if not self.git_history_available:
            self.skipTest(
                "git history unavailable in this test workspace "
                "(file copy without .git); runs in a real checkout"
            )
        ident = self.block["identities"]
        order_text = git("show", "HEAD:" + ORDER_007O)
        match = re.search(
            r"```oap-metadata\n(.*?)\n```", order_text, flags=re.S
        )
        assert match, "committed 007-o order missing oap-metadata block"
        meta = json.loads(match.group(1))
        self.assertEqual(ident["branch"], meta["branch"])
        self.assertEqual(ident["pr_number"], meta["pr"])
        self.assertEqual(meta["id"], "007-o")
        # the order's recovery linkage must agree with the embedded identity
        rec = meta["prior_report_recovery"]
        q = ident["quarantined_007n"]
        for key in (
            "publication_commit",
            "report_path",
            "report_blob",
            "report_sha256",
            "order_path",
            "order_sha256",
            "implementation_parent",
        ):
            self.assertEqual(rec[key], q[key])
        self.assertEqual(rec["prior_id"], "007-n")
        self.assertEqual(rec["corrective_id"], "007-o")
        self.assertEqual(rec["classification"], "INVALID_QUARANTINED")

    def test_frozen_007m_sha_fields_match_committed_config(self):
        ident = self.block["identities"]
        cfg = load_json(
            REPO_ROOT / "research" / "configs"
            / "007-m-rank-ambiguous-levenshtein-candidates.json"
        )
        self.assertEqual(
            ident["frozen_007m_configuration_sha256"],
            cfg["private_evidence"]["configuration_sha256"],
        )
        self.assertEqual(
            ident["frozen_007m_prompt_sha256"], cfg["prompt"]["sha256"]
        )
        self.assertEqual(
            ident["frozen_007m_final_root_manifest_sha256"],
            cfg["private_evidence"]["manifest_sha256"],
        )

    def test_registry_and_report_counts(self):
        ident = self.block["identities"]
        registry = load_json(REPO_ROOT / "research" / "registry" / "experiments.json")
        self.assertEqual(ident["registry_entries"], len(registry["experiments"]))
        report_files = sorted(p.name for p in (REPO_ROOT / "oap" / "reports").glob("*.md"))
        counted = [n for n in report_files if n != REPORT_007O]
        self.assertEqual(ident["oap_reports_reviewed"], len(counted))
        incidents = load_json(REPO_ROOT / "oap" / "REPORT-HISTORY-INCIDENTS.json")
        self.assertEqual(
            ident["frozen_report_history_incidents"], len(incidents["incidents"])
        )

    # ------------------------------------------------------------------ #
    # 2. official scorer                                                   #
    # ------------------------------------------------------------------ #
    def test_official_scorer(self):
        summary = load_json(
            REPO_ROOT / "research" / "results" / "strategic-official-summary.json"
        )
        expected_benchmarks = {}
        for name, bench in summary["benchmarks"].items():
            methods = {}
            for meth, data in bench["methods"].items():
                errant = data["ERRANT"]
                methods[meth] = {
                    "tp": errant["tp"],
                    "fp": errant["fp"],
                    "fn": errant["fn"],
                    "precision": errant["precision"],
                    "recall": errant["recall"],
                    "F0.5": errant["F0.5"],
                    "GLEU": data["GLEU"],
                }
            expected_benchmarks[name] = {
                "source_sha256": bench["source_sha256"],
                "examples": bench["examples"],
                "methods": methods,
            }
        self.assertEqual(self.block["official_scorer"]["benchmarks"], expected_benchmarks)

    # ------------------------------------------------------------------ #
    # 3. custom alignment (007-h chain)                                    #
    # ------------------------------------------------------------------ #
    def _custom_sources(self):
        r = REPO_ROOT / "research" / "results"
        j = load_gz_json(r / "007-j-levenshtein-one-contextual-validator.json.gz")
        i = load_gz_json(r / "007-i-contextual-validator.json.gz")
        m = load_gz_json(r / "007-m-rank-ambiguous-levenshtein-candidates.json.gz")
        return j, i, m

    def test_custom_alignment_stages_and_gold(self):
        j, i, m = self._custom_sources()
        dvj = j["metrics"]["views"]["dassle-spelling"]
        dvi = i["metrics"]["views"]["dassle-spelling"]
        dvm = m["views"]["dassle-spelling"]

        def pick(view):
            return {
                "tp": view["tp"],
                "fp": view["fp"],
                "fn": view["fn"],
                "precision": view["precision"],
                "recall": view["recall"],
                "F0.5": view["F0.5"],
            }

        ca = self.block["custom_alignment"]
        self.assertEqual(ca["view"], "dassle-spelling")
        self.assertEqual(ca["gold_units"], {
            "all": dvj["all"]["baseline"]["gold_edits"],
            "initial_uv": dvj["initial_uv"]["baseline"]["gold_edits"],
            "without_initial_uv": dvj["without_initial_uv"]["baseline"]["gold_edits"],
        })
        self.assertEqual(ca["stages"], {
            "baseline": pick(dvj["all"]["baseline"]),
            "007h_unrestricted": pick(dvj["all"]["unrestricted_007h"]),
            "007i_validated_fallback": pick(dvi["all"]["validated_fallback"]),
            "007j_validated_fallback": pick(dvj["all"]["validated_fallback"]),
            "007m_hybrid": pick(dvm["all"]),
        })

    def test_custom_alignment_deltas_preservation_calls_latency(self):
        j, i, m = self._custom_sources()
        ca = self.block["custom_alignment"]
        a, b = ca["stages"]["007m_hybrid"], ca["stages"]["007j_validated_fallback"]
        delta = ca["007m_vs_007j"]
        self.assertEqual(delta["tp_delta"], a["tp"] - b["tp"])
        self.assertEqual(delta["fp_delta"], a["fp"] - b["fp"])
        self.assertEqual(delta["fn_delta"], a["fn"] - b["fn"])
        self.assertEqual(delta["precision_delta"], a["precision"] - b["precision"])
        self.assertEqual(delta["recall_delta"], a["recall"] - b["recall"])
        self.assertEqual(delta["F0.5_delta"], a["F0.5"] - b["F0.5"])

        pm = m["preservation"]["007m_hybrid"]
        pj = m["preservation"]["007j_validated_fallback"]
        self.assertEqual(
            delta["preservation_changed_cases"],
            [pm["hybrid_cases"], pj["validated_fallback_cases"],
             pm["hybrid_cases"] - pj["validated_fallback_cases"]],
        )
        self.assertEqual(
            delta["preservation_introduced_edit_units"],
            [pm["hybrid_edit_units"], pj["validated_fallback_edit_units"],
             pm["hybrid_edit_units"] - pj["validated_fallback_edit_units"]],
        )

        calls = ca["calls"]
        self.assertEqual(calls["007m_final_root_new_calls"], m["population"]["c_gt_1_new_calls"])
        self.assertEqual(calls["007m_reused_c_gt_1_observations"], m["observations"]["c_gt_1_reused"])
        self.assertEqual(
            calls["007j_fresh_validator_calls"],
            j["metrics"]["fresh_validator"]["dispatched_attempts"],
        )

        lat_m = m["c_gt_1_outcomes"]["latency_seconds"]
        lat_j = j["metrics"]["fresh_validator"]["latency_seconds"]
        self.assertEqual(ca["validator_latency_seconds"], {
            "007m_inherited": {
                "n": lat_m["n"], "mean": lat_m["mean"],
                "p95": lat_m["p95"], "max": lat_m["max"],
            },
            "007j_fresh": {
                "n": lat_j["n"], "mean": lat_j["mean"],
                "p95": lat_j["p95"], "max": lat_j["max"],
            },
        })

    # ------------------------------------------------------------------ #
    # 4. campaign (full-campaign8)                                         #
    # ------------------------------------------------------------------ #
    def test_campaign(self):
        registry = load_json(REPO_ROOT / "research" / "registry" / "experiments.json")
        fc = [
            e for e in registry["experiments"]
            if (e.get("id") or e.get("experiment_id")) == "full-campaign8"
        ]
        self.assertEqual(len(fc), 1)
        cm = fc[0]["metrics"]
        r = REPO_ROOT / "research" / "results"
        das = load_gz_json(r / "dassle.json.gz")["projection"]
        pre = load_gz_json(r / "dassle-preservation.json.gz")["projection"]

        camp = self.block["campaign"]
        self.assertEqual(camp["experiment_id"], "full-campaign8")
        for key in (
            "cases", "method_records", "distinct_calls", "new_model_calls",
            "inherited_calls", "verified_checkpoints", "workers",
            "completed_phases", "deployment",
        ):
            self.assertEqual(camp[key], cm[key])

        expected_e2e = {}
        for meth in ("M1", "M2", "M3"):
            e = das["methods"][meth]["end_to_end"]
            expected_e2e[meth] = {
                "tp": e["tp"], "fp": e["fp"], "fn": e["fn"],
                "precision": e["precision"], "recall": e["recall"],
                "F0.5": e["F0.5"], "introduced_edits": e["introduced_edits"],
                "operational_failures": e["operational_failures"],
            }
        e2e = camp["custom_end_to_end_dassle"]
        self.assertEqual(e2e["methods"], expected_e2e)
        self.assertEqual(e2e["N"], das["methods"]["M1"]["end_to_end"]["N"])
        self.assertEqual(e2e["gold_edits"], das["methods"]["M1"]["end_to_end"]["gold_edits"])

        expected_pv = {}
        for meth in ("M1", "M2", "M3"):
            c = pre["methods"][meth]["conditional_no_operational_failure"]
            expected_pv[meth] = {
                "introduced_edit_units": c["introduced_edits"],
                "unchanged_examples": c["unchanged_examples"],
                "N": c["N"],
            }
        self.assertEqual(camp["preservation_dassle"], expected_pv)

        self.assertEqual(camp["retry_ablation"], {
            "dassle": {
                "tp_delta": das["retry_ablation_totals"]["tp_delta"],
                "fp_delta": das["retry_ablation_totals"]["fp_delta"],
                "calls": das["retry_ablation_totals"]["calls"],
            },
            "dassle-preservation": {
                "tp_delta": pre["retry_ablation_totals"]["tp_delta"],
                "fp_delta": pre["retry_ablation_totals"]["fp_delta"],
                "calls": pre["retry_ablation_totals"]["calls"],
            },
        })

    # ------------------------------------------------------------------ #
    # 5. 007-m frozen experiment                                           #
    # ------------------------------------------------------------------ #
    def test_007m(self):
        m = self._custom_sources()[2]
        o7m = self.block["007m"]
        lin = m["lineage"]
        obs = m["observations"]
        pop = m["population"]
        slices = m["census"]["slices"]
        sp = slices["spelling-all"]
        prs = slices["preservation-all"]

        self.assertEqual(o7m["roots"], {
            "final": lin["final_root"],
            "census": lin["census_root"],
            "census_superseded_diagnostic": lin["census_superseded_diagnostic_root"],
            "failed_instrument": [r["root"] for r in lin["failed_instrument_roots"]],
        })
        self.assertEqual(o7m["scheduled_total"], pop["scheduled_total"])
        self.assertEqual(o7m["c1"], pop["c1"])
        self.assertEqual(o7m["c_gt_1"], pop["c_gt_1"])
        self.assertEqual(o7m["c_gt_1_attempted"], obs["c_gt_1_reused_attempted"])
        self.assertEqual(o7m["c_gt_1_uncertain"], obs["c_gt_1_reused_uncertain"])
        self.assertEqual(
            o7m["candidate_pairs"],
            sp["total_candidate_pairs"] + prs["total_candidate_pairs"],
        )
        self.assertEqual(o7m["unique_top"], sp["unique_top"] + prs["unique_top"])
        self.assertEqual(o7m["tied_top"], sp["tied_top"] + prs["tied_top"])
        self.assertEqual(o7m["reference_present"], sp["reference_present"])
        self.assertEqual(
            o7m["reference_absent"],
            sp["reference_absent"] + prs["reference_absent"],
        )
        self.assertEqual(o7m["top_k_coverage_among_present"], {
            k: sp["top_k_coverage"][k]["certain"]["count"] for k in ("1", "2", "3", "5", "10")
        })
        self.assertEqual(o7m["oracle"], {
            "frozen_recall": sp["baseline"]["frozen_recall"],
            "ceiling": sp["baseline"]["ceiling"],
        })
        self.assertEqual(o7m["vocabulary_rows"], m["census"]["runtime"]["vocabulary_rows"])
        self.assertEqual(o7m["actual_experiment_calls"], {
            **lin["actual_experiment_calls"],
            "final_root_new_calls": lin["final_root_new_calls"],
        })
        self.assertEqual(o7m["decisions"], m["c_gt_1_outcomes"]["decisions"])
        self.assertEqual(o7m["accepted"], {
            "exact_reference": m["c_gt_1_outcomes"]["accepted_exact_reference"],
            "non_reference": m["c_gt_1_outcomes"]["accepted_non_reference"],
        })
        self.assertEqual(o7m["operational_failures"], obs["operational_failures"])
        self.assertEqual(o7m["hybrid_composition"], {
            "cases_with_c_gt_1_targets": m["hybrid_composition"]["cases_with_c_gt_1_targets"],
            "winner_edits_applied": m["hybrid_composition"]["winner_edits_applied"],
            "base_edits_removed": m["hybrid_composition"]["base_edits_removed"],
            "composition_conflict_rollbacks": m["hybrid_composition"]["rollbacks"],
            "new_calls": m["hybrid_composition"]["new_calls"],
        })
        self.assertEqual(
            o7m["token_totals_inherited"], m["c_gt_1_outcomes"]["token_totals"]
        )


if __name__ == "__main__":
    unittest.main()
