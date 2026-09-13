# Work report 007-m — Rank ambiguous Levenshtein-one candidates on CPU

```oap-report
{
  "id": "007-m",
  "result": "COMPLETE",
  "order_path": "oap/orders/007-m-rank-ambiguous-levenshtein-candidates.md",
  "order_sha256": "d5b1807d79acf42538b5161e57a81698a80e086b17ad77bf9abb7aa8c046fc9a",
  "governance": {
    "AGENTS.md": "118be17b2e9e5b50d628c796b136ee1b8154ebf844af0007839f65848fd69f09",
    "ARCHITECTURE-for-agents.md": "e83545d648b32263110f532d9425c785abdcd96be5e37d0ce055f57cc2ec9491",
    "ARCHITECTURE.md": "a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7a7261f7",
    "OAP-COMMUNICATION-coding-agent.md": "6355623830eb5ef47523d04b1a6bf958685f4debd16b62f9f46c3f14de01020b",
    "PLAN.md": "d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0",
    "SECURITY.md": "0424b58bdaae1d4379364e3470b7cb4b2b729a20456d30e5c1ea59a3edbed7a6",
    "TESTING.md": "68a3307289f684910281b9d4947336f3a390924e229e7aafce7212b4a0fcc5d1",
    "oap/coding-instructions/AGENTS.md": "55bc5d72200cd3e25e1d8decd629d902ffb732c8808bae8ef36a6081b4416514",
    "oap/governance/DISTILLATION-MAP.md": "a03d4be8d70101dc2d038bc5e8bd98e18fcaf3806539651b37d0e85f2558c2d7",
    "oap/governance/WORKSPACE-LAYOUT.json": "cba4ae2226038a44d74bff2eb727bc79e930b34f8f657b1e14c411a4ca09d254",
    "oap/prompts/coding-round.md": "fa94f21c065209d284978f7f731b95600cbab87949d0c8ae2c226a0923552611",
    "oap/prompts/ica-start.md": "2311778a8c2f8cbfa24bbc9be1eed30d14289f3d82c2b5e8da70d806b12d70f4",
    "oap/prompts/strategic-start.md": "40ccb00e48c9b1b6ae93d5e5a334322b8a249d655341e47a123e5321b65b6e9b",
    "oap/strategic-instructions/AGENTS.md": "ac05494856ac8c85c31b77225ac96abe9596f0d0ae50d96e338da7370669fa5c",
    "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md": "6ba11ddcde24ed3d8777f305951d706d3fc4a1869470be9669a9853d3ce15cbf",
    "oap/strategic-instructions/strategic_model_init_material.md": "813edbc94f0a991abda046a544beb22510a83c9b45dc5282f046dd71a324465d"
  },
  "publication_commit": "SELF",
  "implementation_head": "1a67adf80a679489288c39998cc41974f0c21d8e",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "f7584802773ce316dcbd3e406dd46c8a1b48162e",
  "no_merge": true,
  "checks": [
    {
      "command": "TMPDIR=native python3 -B -m unittest discover -s research/tests -v",
      "result": "PASSED",
      "details": "All 222 research tests passed, including the ten new 007-m FinalPublicationTests covering the final zero-call root verification gate (hermetic synthetic root, tamper/hash, recompute-status, decision, headline-slice and wrong-root negatives, data-free self-hashed public projection, public write immutability, and the publication Git lineage guard).",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "TMPDIR=native python3 -B -m unittest research.tests.test_levenshtein_rank -v",
      "result": "PASSED",
      "details": "The focused 007-m module passed 77/77, including deterministic ranking, tie abstention, no-gold-dependency, exact reuse/resume, failed-root adoption, replay-gate normalization, and final-publication gate coverage.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "ruff 0.16.6 check and format check on the changed 007-m research scope",
      "result": "PASSED",
      "details": "Ruff check passed on all three changed Python files and on the frozen head. ruff format --check shows pre-existing format drift in the two scientific 007-m modules that is identical at the frozen head f3fecab; reformatting frozen scientific code was out of scope, and CI runs ruff check only on src/scripts/tests, which does not include research.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.rebuild_tables --check",
      "result": "PASSED",
      "details": "The deterministic numeric table matched the registry after the additive 007-m record.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.publication_guard --root research",
      "result": "PASSED",
      "details": "The public research tree passed the privacy guard on 151 files: no raw text, targets, replacements, prompts, responses, credentials, endpoint values, profile paths, or private root paths.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref 2832fa1e51bdf3641aabbd81feab8ddb64a876da",
      "result": "PASSED",
      "details": "Governance structure is valid; semantic and human authorization proofs remain false.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "41 reports with exactly the two frozen historical incidents. One transient 30-second FUSE git subprocess timeout was retried once and passed; no report mutation was attempted.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_transcript.py --repo-root . --revision HEAD --expected-id 007-m",
      "result": "PASSED",
      "details": "active=latest=007-m with the exact order present; no 007-m report existed before this publication.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "python3 oap/bin/check_whitespace.py --base 2832fa1e51bdf3641aabbd81feab8ddb64a876da / --base 82ea1e6f4173934fa47bb34ee6a6f78338d3603a --revision HEAD",
      "result": "PASSED",
      "details": "Both accepted-base checks passed with exactly the three pre-existing frozen blank-at-EOF incidents.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "git diff --exit-code 82ea1e6f4173934fa47bb34ee6a6f78338d3603a -- PLAN.md ARCHITECTURE.md CRITICAL.md AGENTS.md ARCHITECTURE-for-agents.md OAP-COMMUNICATION-coding-agent.md SECURITY.md TESTING.md oap/bootstrap-sources.lock.json oap/governance oap/coding-instructions oap/strategic-instructions docs/bootstrap",
      "result": "PASSED",
      "details": "No protected source changed against the application accepted base.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs",
      "result": "PASSED",
      "details": "Git object integrity passed; pre-existing dangling scratch objects were preserved.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "RUNNER_TEMP=native TMPDIR=native python3 -B -m unittest discover -s oap/tests -v",
      "result": "PASSED",
      "details": "129/129 passed in an isolated native run. An earlier local run recorded one environmental copytree error caused by a concurrent mypy cache write into the copied tree; the gitignored cache was removed and the full suite re-ran clean.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "python3 scripts/verify_development_baseline.py --temp-parent native --command-timeout 900 (local observation; mypy stage run directly)",
      "result": "FAILED",
      "details": "Inherited failure only: the mypy stage (mypy src tests/contract) fails with exactly the 11 inherited errors in scripts/verify_source_artifact.py and no new errors; the order forbids repairing that debt in 007-m. Local full pytest showed one environmental flake (concept-verification proxy terminal-event test, local 2-second HTTP timeout) that passes 3/3 in isolation and touches no 007-m code. The remote Application baseline at the implementation head is the arbiter.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B -m research.tools.run_levenshtein_rank --repo-root . --scratch native-final-root-ec2962 --source-root native-007j-source-root --expected-implementation-head 537aa6a3ff03c60dd1b2c7f697c577940d52e88d --publish-final",
      "result": "PASSED",
      "details": "Independent end-to-end re-verification of the final zero-call root against all strategy-accepted SHA-256s (configuration, live/hybrid aggregates, hybrid projections, case results, failed-root linkage, census artifacts, request tree, worker results, C=1 records), the corrected census root, the 007-j source root identity, and the publication Git lineage guard. Private manifest/report and public config/result re-emitted byte-identically; new_calls=0, resampled=false.",
      "sha": "f3fecab35c64ae202f6fed51d46e472b52270eb3",
      "publication_head_claim": false
    },
    {
      "command": "gh api -X PATCH repos/ulfe-lmi/llm-slovenian-repair/pulls/8 (single metadata update)",
      "result": "PASSED",
      "details": "PR #8 body was updated exactly once near closure with the data-free 007-m result and status; no merge, release, deployment, or linguistic-success claim. PR #8 is OPEN and UNMERGED.",
      "sha": "1a67adf80a679489288c39998cc41974f0c21d8e",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-14T01:07:41+02:00",
  "report_written_at": "2026-09-14T01:11:13+02:00",
  "implementation": "Increment 3 added only aggregation/publication machinery: the final zero-call root verification gate (EXPECTED_FINAL_* frozen facts, verify_final_root_state, publication Git lineage guard, deterministic private manifest/report, data-free public projection and immutable public write), the additive data-free 007-m registry/README/table records, and ten hermetic FinalPublicationTests. No ranking, method, prompt, corpus, detector, or model-call change; the frozen implementation head is 537aa6a3ff03c60dd1b2c7f697c577940d52e88d and the recompute head is f3fecab35c64ae202f6fed51d46e472b52270eb3.",
  "documentation": "Published the data-free 007-m configuration, compressed aggregate result, research report, registry entry, navigation row, and deterministic table row. Public artifacts contain aggregate metrics, hashes, transition and operation counts only. The failed instrument roots (ffdf13, 090ea8) and the final successful zero-call recompute (ec2962) are reported distinctly. This OAP report is the sole report-only change.",
  "criteria": "The exact frozen C>1 population was 882 targets (651 spelling + 231 preservation) with 4,372 candidate pairs; operation pairs SUBSTITUTION 2801, DELETION 845, INSERTION 726; 882/882 unique tops, 0 ties; reference present 408 / absent 474. Complete C>1 validation: 882 = 866 attempted + 16 uncertain-delivery (never resampled); USE/KEEP/UNCERTAIN/FAILURE 270/509/16/87; accepted exact/non-reference 219/51; attribution 247/635. The final root ec2962 adopted all 882 C>1 observations and 1,035 C=1 observations with zero new calls and byte-for-byte verified case-result projections. Every strategy-reviewed headline, slice, call, failure, latency, and token fact was re-verified against the private roots and the strategy-accepted SHA-256s before publication.",
  "negative_paths": "The new publication gate rejects tampered artifacts, hash drift, RECOMPUTE-STATUS drift (new_calls=1, case_results_verified=False), decision drift, headline-slice drift, wrong root names, non-descendant publication heads, wrong branches, and shared-science-code drift, proven by hermetic synthetic-root tests. Public projection tests prove data-free bytes (guard-validated, self-hashed, no raw-language tokens or private path markers) and immutable public writes. Uncertain deliveries are never resampled; tied tops select nothing; no runner-up is ever tried; no new model call was dispatched in the final root.",
  "boundary_fidelity": "Only the 007-m research implementation/tests and data-free public/OAP records changed. The frozen 007-j/007-i private roots, model weights, quantization, vLLM/CUDA, shared GPU, services, gateway, network configuration, neighboring repositories, and existing agent profiles were not changed. No merge, auto-merge, release, deployment, or production integration occurred; PR #8 remains OPEN and UNMERGED.",
  "setup": "Reconciled active 007-m, immutable order (sha256 d5b1807d79acf42538b5161e57a81698a80e086b17ad77bf9abb7aa8c046fc9a), branch, base ee2d1b479719009ff1d07829478f241e3f395f7c, PR #8, and the pushed clean head f3fecab35c64ae202f6fed51d46e472b52270eb3 before mutation. Private durable roots (final ec2962, census 97f59c, superseded census e6ca66, failed instrument roots ffdf13 and 090ea8) remain under the owner-controlled native runtime; the completed 007-j source root 54KmUx was verified read-only.",
  "privacy": "The publication guard passed on 151 research files; the public config, result, and report contain no raw datasets, sentences, model responses, request trees, credentials, endpoint values, profile paths, or private layout beyond the existing redacted conventions. The profile bearer and raw evidence stay in private roots only.",
  "limits": "The final root made zero new calls (budget 0; all eight workers dispatched 0) and resampled nothing. The actual experiment calls were 866 across the preserved roots (188 in ffdf13, 678 in 090ea8); cross-root reuse was 196 (ffdf13 to 090ea8) plus 882 (090ea8 to final) and is reported distinctly from actual calls. Inherited latency n=866: sum 14023.362979554106, mean 16.193259791632915, median 11.124804617022164, p95 33.48273886600509, max 184.56243890197948 seconds; inherited tokens input/output/reasoning 173422/393685/388375; new-call tokens 0.",
  "human_gates": "D0 / NONE. CRITICAL has no admitted entries. The owner-authorized bounded experiment does not constitute human semantic acceptance, product readiness, deployment authorization, release authority, merge approval, or linguistic benefit certification. PR #8 remains OPEN and UNMERGED.",
  "scope": "Finished only Increment 3 of the exact active 007-m order: aggregation verification, data-free publication, registry/history updates, broad verification, PR metadata update, and this immutable report. No next suffix or adjacent objective was assigned or started.",
  "result_summary": "COMPLETE for the ordered research round. The primary 007-m HYBRID projection (007-j validated_fallback per case with each C>1 target replaced by the 007-m decision outcome) is a conservative tradeoff versus 007-j, not an unqualified win: spelling TP/FP/FN 799/114/716 vs 822/154/693 (delta -23/-40/+23), precision 0.8751369112814896 vs 0.8422131147540983 (+0.0329237965273913), recall 0.5273927392739274 vs 0.5425742574257426 (-0.015181518151815232, i.e. 1.5181518151815232 recall points lost), F0.5 0.7731759241339268 vs 0.7584425170695701 (+0.014733407064356663). Preservation improved (changed cases 78 vs 93; introduced edit units 83 vs 101) with protected/outside-span/expected-output failures 0/0/0. Initial-u/v improved 49/7/26 vs 42/7/33 (+7 TP, no FP delta); without-initial-u/v lost 750/107/690 vs 780/147/660 (-30 TP while removing 40 FP). Oracle recall ceilings are high (spelling 0.5425742574257426 to 0.8118811881188119) but top-1 covers only 60.54% of present gold candidates, so both ranking position and validator rejection/failure limit recall. The validated-only projection (778/96/737) is a diagnostic, not the primary result. This is same-sample exploratory evidence, not held-out confirmation, human linguistic acceptance, or production readiness; the design is recommended to be frozen and tested against fresh evidence rather than further tuned."
}
```

## Result

The 007-m experiment is COMPLETE. The frozen CPU top-1 ranking selected exactly one candidate for each of the 882 ambiguous (C>1) distance-one targets (0 tied tops), and the final zero-call root verified every preserved observation and the hybrid recompute byte-for-byte. The complete data-free research records are published under `research/`; the immutable final OAP report is this report-only commit.

## Scientific result

Does 007-m improve upon 007-j? **A conservative tradeoff, not an unqualified win.** The primary HYBRID projection improves precision, F0.5, and preservation while losing 23 TP (1.5181518151815232 recall points):

- **Spelling all:** TP/FP/FN 799/114/716 vs 822/154/693; precision 0.8751369112814896 vs 0.8422131147540983; recall 0.5273927392739274 vs 0.5425742574257426; F0.5 0.7731759241339268 vs 0.7584425170695701.
- **initial-u/v:** 49/7/26 vs 42/7/33 (+7 TP, no FP delta; F0.5 0.8193979933110368 vs 0.7749077490774908).
- **without-initial-u/v:** 750/107/690 vs 780/147/660 (−30 TP while removing 40 FP; F0.5 0.7703368940016433 vs 0.7575757575757577).
- **Preservation:** changed cases 78 vs 93; introduced edit units 83 vs 101; protected/outside-span/expected-output failures 0/0/0.
- **Diagnostic (not primary):** validated-only 778/96/737 versus 007-j validated-only 802/136/713.

**Headroom and ties:** 882 C>1 targets (651 spelling + 231 preservation), 4,372 candidate pairs, operation pairs SUBSTITUTION 2801 / DELETION 845 / INSERTION 726, 882 unique tops, 0 ties, set size 2/3/9/14/29/50 (min/median/p90/p95/p99/max). Reference present 408 / absent 474; among present, top-1 covers 247 (60.54%), top-2 349 (85.54%), top-3 376 (92.16%), top-5 399 (97.79%), top-10 408 (100%). Oracle recall ceilings: spelling 0.5425742574257426 → 0.8118811881188119; initial-u/v 0.56 → 0.8933333333333333; non-initial-u/v 0.5416666666666666 → 0.8076388888888889. Ranking headroom is high, but top-1 covers only 60.54% of gold candidates when present; both ranking position and validator rejection/failure limit recall.

**Validator decisions and failures (complete C>1 882 = 866 attempted + 16 uncertain-delivery, never resampled):** USE_CANDIDATE 270, KEEP_ORIGINAL 509, UNCERTAIN 16, FAILURE 87; accepted exact-reference/non-reference 219/51; candidate attribution exact-reference/non-reference 247/635 (by decision USE 219/51, KEEP 13/496, UNCERTAIN 2/14, FAILURE 13/74).

**Calls, latency, tokens (actual calls vs cross-root reuse reported distinctly):** actual experiment calls 188 (ffdf13, head 88ca4dfe19740aa21156457d42966661f67902ea) + 678 (090ea8, head 92bee3a214aa50ef3921f54488545a57d9a95000) = 866; cross-root reuse 196 (ffdf13 → 090ea8) and 882 (090ea8 → final); the final root ec2962 made **0 new calls** (all eight workers dispatched 0, case-result projections verified byte-for-byte). Inherited latency n=866: mean 16.193259791632915 s, median 11.124804617022164 s, p95 33.48273886600509 s, max 184.56243890197948 s, sum 14023.362979554106 s; inherited tokens input/output/reasoning 173422/393685/388375; new-call tokens 0/0/0.

**Interpretation:** CPU top-1 plus the frozen validator improves precision, F0.5, and preservation but loses 23 TP / 1.52 recall points overall. The initial-u/v slice improves; the non-initial-u/v slice loses 30 TP while removing 40 FP (same-sample exploratory evidence only). This is not held-out confirmation, human linguistic acceptance, or production readiness. Recommendation: freeze the design and test fresh evidence rather than further tuning DASSLE.

## Evidence and limitations

The failed instrument roots are reported distinctly: ffdf13 (188 actual calls, 8 request-only interruptions finalized as uncertain observations; its harness revision rejected the canonical interrupted-finalization file set) and 090ea8 (678 fresh calls, 196 reused from ffdf13; fully observed but blocked by a tuple/JSON replay-identity bug). Both are preserved unchanged as failed-instrument evidence. The final root ec2962 adopted all 882 C>1 observations and all 1,035 C=1 observations with zero new calls.

Public artifacts are data-free and hash-linked; raw cases, requests, and responses remain only in owner-controlled private roots (final ec2962, census 97f59c, superseded census e6ca66, source 54KmUx). Same-sample exploratory projection on the frozen 007-j population; gold is post-ranking headroom analysis only and cannot affect selection. The Application baseline mypy stage still fails only on the 11 inherited errors in `scripts/verify_source_artifact.py` (out of 007-m scope); a local concept-proxy pytest flake is environmental and passes in isolation. Remote final-head CI state at `1a67adf` is recorded in strategy review, not in this pre-push report.

## Deferred human adjudication

- Decision: NONE
