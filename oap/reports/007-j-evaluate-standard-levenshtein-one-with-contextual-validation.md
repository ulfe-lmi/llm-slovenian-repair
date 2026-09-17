# Work report 007-j — Evaluate standard Levenshtein-one candidates with contextual validation

```oap-report
{
  "id": "007-j",
  "result": "COMPLETE",
  "order_path": "oap/orders/007-j-evaluate-standard-levenshtein-one-with-contextual-validation.md",
  "order_sha256": "a7e72313424345bb86ffa92345348f063f5f95b756b9628574c91c5e4933a60f",
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
  "implementation_head": "373a9dd33ea9364061ed77fe9a3d76e2238f0a91",
  "publication_verified": false,
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "pr_url": "https://github.com/ulfe-lmi/llm-slovenian-repair/pull/8",
  "pr_state": "open",
  "branch": "oap/007-concept-verification",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "starting_remote_sha": "a4d3592e25a792dd3f8d65a729c54a08032a88e3",
  "no_merge": true,
  "checks": [
    {
      "command": "TMPDIR=native python3 -B -m unittest discover -s research/tests -v",
      "result": "PASSED",
      "details": "All 145 research tests passed, including 007-j distance, reuse, fallback, persistence, privacy, operation-analysis, and CI-portability coverage.",
      "sha": "5bf8e124ad2f7c1a25d718fad7128b80b3eda577",
      "publication_head_claim": false
    },
    {
      "command": "cached Ruff 0.16.6 check and format check on changed research scope",
      "result": "PASSED",
      "details": "Ruff and formatting checks passed for the 007-j implementation and tests.",
      "sha": "5bf8e124ad2f7c1a25d718fad7128b80b3eda577",
      "publication_head_claim": false
    },
    {
      "command": "changed-scope Python compile check",
      "result": "PASSED",
      "details": "The 007-j implementation and test sources compiled without writing bytecode artifacts.",
      "sha": "b203757afb330dedaab297fc868f3f8ecc8c6f9c",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B research/tools/publication_guard.py --root research; --staged-tree .",
      "result": "PASSED",
      "details": "The public research tree and staged non-report publication tree passed the privacy guard; no raw rows, targets, replacements, prompts, responses, credentials, or private paths were present.",
      "sha": "b203757afb330dedaab297fc868f3f8ecc8c6f9c",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B research/tools/rebuild_tables.py --check",
      "result": "PASSED",
      "details": "The deterministic summary table matched the registry after the additive 007-j record.",
      "sha": "b203757afb330dedaab297fc868f3f8ecc8c6f9c",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_governance.py --repo-root . --mode accepted-runtime --accepted-ref ee2d1b479719009ff1d07829478f241e3f395f7c",
      "result": "PASSED",
      "details": "Governance structure is valid; semantic and human authorization proofs remain false.",
      "sha": "5bf8e124ad2f7c1a25d718fad7128b80b3eda577",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_report_history.py --repo-root . --revision HEAD --require-manifest",
      "result": "PASSED",
      "details": "The existing report history and two frozen historical incidents remained valid before this report.",
      "sha": "b203757afb330dedaab297fc868f3f8ecc8c6f9c",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/acquisition_history.py --repo-root . --revision HEAD",
      "result": "PASSED",
      "details": "Cumulative acquisition history remained valid at 14 with no new source acquisition.",
      "sha": "b203757afb330dedaab297fc868f3f8ecc8c6f9c",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_whitespace.py for accepted OAP and application bases",
      "result": "PASSED",
      "details": "Both accepted-base checks passed with exactly the three pre-existing frozen blank-at-EOF incidents.",
      "sha": "b203757afb330dedaab297fc868f3f8ecc8c6f9c",
      "publication_head_claim": false
    },
    {
      "command": "git fsck --full --no-reflogs --no-progress",
      "result": "PASSED",
      "details": "Git object integrity passed; pre-existing dangling scratch objects were preserved.",
      "sha": "b203757afb330dedaab297fc868f3f8ecc8c6f9c",
      "publication_head_claim": false
    },
    {
      "command": "python3 -B oap/bin/check_transcript.py --repo-root . --index/--revision HEAD --expected-id 007-j",
      "result": "BLOCKED",
      "details": "Both transcript modes reached the shared Dropbox/rclone FUSE metadata stall and timed out at 20 seconds (exit 124); no transcript mutation was attempted.",
      "sha": "5bf8e124ad2f7c1a25d718fad7128b80b3eda577",
      "publication_head_claim": false
    },
    {
      "command": "TMPDIR=native python3 -B -m unittest discover -s oap/tests -v",
      "result": "BLOCKED",
      "details": "The local OAP suite entered uninterruptible Dropbox/rclone filesystem I/O after approximately ten minutes and was stopped; no assertion verdict is claimed. GitHub OAP bootstrap acceptance and OAP report history passed at the implementation head.",
      "sha": "b203757afb330dedaab297fc868f3f8ecc8c6f9c",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Research reproducibility check at PR #8 head 5bf8e12",
      "result": "PASSED",
      "details": "The remote research workflow passed after the 007-j test portability and public-config schema adaptations.",
      "sha": "5bf8e124ad2f7c1a25d718fad7128b80b3eda577",
      "publication_head_claim": false
    },
    {
      "command": "GitHub OAP bootstrap acceptance and OAP report history checks at PR #8 head 5bf8e12",
      "result": "PASSED",
      "details": "Both remote OAP checks passed.",
      "sha": "5bf8e124ad2f7c1a25d718fad7128b80b3eda577",
      "publication_head_claim": false
    },
    {
      "command": "GitHub Application baseline check at PR #8 head 5bf8e12",
      "result": "FAILED",
      "details": "Inherited baseline failure: mypy reported 11 ZipInfo/stat_result typing errors in scripts/verify_source_artifact.py; no application source changed in this round.",
      "sha": "5bf8e124ad2f7c1a25d718fad7128b80b3eda577",
      "publication_head_claim": false
    },
    {
      "command": "private completed-evidence and publication identity verification",
      "result": "PASSED",
      "details": "Native private status is COMPLETE with 1,035 observation records, 493 fresh dispatches, 542 reused observations, zero uncertain deliveries, 1,035 complete request trees, and aggregate artifacts verified.",
      "sha": "dc1a76e07765532e96a3238abbeae562c135337b",
      "publication_head_claim": false
    },
    {
      "command": "in-memory profile validation and bounded 007-j live driver",
      "result": "PASSED",
      "details": "The selected qwen-LSI-A100 profile and exact frozen Responses request identity were validated in memory; 493 fresh candidates completed once, with no probe, retry, resampling, service mutation, or uncertain delivery. Public artifacts were generated from completed private evidence.",
      "sha": "dc1a76e07765532e96a3238abbeae562c135337b",
      "publication_head_claim": false
    },
    {
      "command": "gh pr edit 8 --repo ulfe-lmi/llm-slovenian-repair --body ...",
      "result": "PASSED",
      "details": "PR metadata contains only the data-free 007-j scope and aggregate result; PR #8 is OPEN and UNMERGED.",
      "sha": "b203757afb330dedaab297fc868f3f8ecc8c6f9c",
      "publication_head_claim": false
    }
  ],
  "critical_action": "NONE",
  "pr_observed_at": "2026-09-13T04:28:37+02:00",
  "report_written_at": "2026-09-13T04:29:13+02:00",
  "implementation": "Implemented standard unit-cost Levenshtein distance over Python Unicode code points with identity, insertion, deletion, substitution, transposition-distance-two, complete-union, English-suppression, mechanical-gate, exact-reuse, fresh-call, immutable-persistence, eight-worker, fallback, operation-analysis, and per-view accounting boundaries. The live implementation was dc1a76e; the final non-report publication/test head is 5bf8e12.",
  "documentation": "Published data-free 007-j configuration, compressed result, report, registry entry, navigation row, and deterministic table row. Public artifacts are linked by hashes and contain aggregate metrics only. The final OAP report is this sole report-only change.",
  "criteria": "Frozen entering targets were 2,001 spelling and 920 preservation. The exact new unique population was 826 spelling plus 209 preservation, with 542 SUBSTITUTION, 172 INSERTION, and 321 DELETION candidates. The required transition matrix matched 007-j reconnaissance exactly. All 542 reuse records matched source row/coordinates, sentence, candidate, request body, prompt, deployment, parser, limits, and persisted response hashes. The fresh population made exactly 493 one-attempt calls and all 1,035 observations were durably aggregated.",
  "negative_paths": "Offline tests prove identity exclusion, two substitutions, substitution plus insertion, transposition distance two, whitespace/normalization rejection, English suppression before generation, cross-operation ambiguity fallback, exact-identity-only reuse, altered candidate/request/profile/parser fresh classification, KEEP/UNCERTAIN/failure fallback, supplied-candidate-only USE behavior, protected/outside integrity, worker partitioning, immutable persistence/resume, uncertain-delivery no-resample, and zero default network action. A mode-755 reused request parent and a CI portability/schema issue were corrected before the final live freeze. The earlier missing-credential attempt remains preserved as zero-dispatch failed evidence.",
  "boundary_fidelity": "Only the exact 007-j research implementation/tests and data-free public/OAP records changed. The 007-i research and OAP artifacts, frozen private source, model weights, quantization, vLLM/CUDA, shared GPU, service, gateway, network configuration, neighboring repositories, and existing agent profiles were not changed. No merge, auto-merge, release, deployment, or production integration occurred.",
  "setup": "Reconciled active 007-j, immutable order, branch, base, PR #8, remote head, staged work, prior 007-i hashes, and private roots before mutation. The documented prior zero-dispatch credential-boundary incident hashes were preserved: configuration 2411d31cb12fd4a247d63632658b30576ffa644f82b8d55c8ed6832d90d63982, candidate manifest acabcf1b33c38a949c80e81773b8ff3c355386daf768404791aaaed111f1df41, results 398a38eff253f3080d45f512a60b08191afa3240341d67caca1917e4138eb318, manifest 6f2d23d9950ea0da836f557e4779c79b7e06fb107fcf65650514df50009c3567, report 98aee169606dd75fd9069a88c7575f5b263545a9a008112d7f886e2202373c89, and run status 5d04c98fe543d564738e69a9b8707b74a2d856d756b9372bf84b8cda3612c876. A later zero-dispatch mode-boundary root was retained as private failed setup evidence; the final valid root is owner-controlled and directly beneath the required native runtime parent.",
  "privacy": "The public research guard passed on 145 files and on the staged non-report tree. The profile bearer was read as data and injected only into the child process; it was never printed, persisted, hashed, copied, logged, or placed in Git, PR metadata, public results, or this report. Public artifacts contain no raw text, targets, replacements, prompts, responses, credential values, endpoint values, profile paths, or private root paths.",
  "limits": "The live budget was exactly 493 fresh calls, at most eight in flight, one attempt per candidate, 300-second timeout, 2,000,000-byte response bound, zero validator retries, zero baseline resampling, and zero uncertain deliveries. Fresh latency statistics were n/sum/mean/median/p95/max 493/5283.875946435757/10.71780110838896/8.496985418023542/24.88524721498834/58.17827162001049 seconds; reasoning and output token distributions are recorded in the public result.",
  "human_gates": "D0 / NONE. CRITICAL has no admitted entries. The owner-authorized bounded experiment does not constitute human semantic acceptance, product readiness, deployment authorization, release authority, merge approval, or linguistic benefit certification. PR #8 remains OPEN and UNMERGED.",
  "scope": "Finished only the exact active 007-j order: standard Levenshtein-one candidate expansion with unchanged contextual validation and fallback, exact reuse, bounded fresh validation, aggregate comparison, data-free publication, and this immutable report. No next suffix or adjacent objective was assigned.",
  "result_summary": "COMPLETE for the ordered research round. Under the supplied-reference scorer, validated+fallback spelling improved from frozen 007-i BEST by TP +95, FP -18, FN -95, precision +0.03353680774631185, recall +0.06270627062706274, and F0.5 +0.04723140378449875; initial-u/v declined, preservation changed cases rose by 2 and edit units by 4, and protected/outside differences remained zero. This is a data-backed demonstrator result, not a semantic, product, merge, release, or deployment decision."
}
```

## Result

The 007-j demonstrator is COMPLETE. The standard Levenshtein-distance-one expansion produced the exact frozen population and completed 493 fresh contextual-validator calls alongside 542 exact 007-i observation reuses. All 1,035 observations and aggregate artifacts are durably present in the native private evidence root.

## Scientific result

For the primary validated+fallback spelling view, the result is TP/FP/FN 822/154/693, precision 0.8422131147540983, recall 0.5425742574257426, and F0.5 0.7584425170695701. Versus frozen 007-i BEST, the exact deltas are TP +95, FP -18, FN -95, precision +0.03353680774631185, recall +0.06270627062706274, and F0.5 +0.04723140378449875.

The initial-u/v view declined by TP -5, FP +2, FN +5, and F0.5 -0.05548094350201449. The spelling view without initial-u/v improved by TP +100, FP -20, FN -100, and F0.5 +0.05335040546308156. Preservation changed cases increased from 91 to 93 and edit units from 97 to 101; this is not a semantic-harm label. Protected and outside-span differences were zero in every view.

## Evidence and limitations

The complete data-free research records are published under `research/`. Fresh validator outcomes were USE/KEEP/UNCERTAIN/FAILURE 289/172/3/29; 29 protocol failures remain distinct from KEEP. The operation and new-or-changed candidate breakdown, fresh runtime distributions, four-view metrics, exact 007-i deltas, hashes, and limitations are in the public result and research report.

The local OAP unittest and transcript scans were blocked by the documented Dropbox/rclone FUSE metadata stall. Remote OAP checks and Research reproducibility passed. The Application baseline remains failed on inherited mypy errors in `scripts/verify_source_artifact.py`; unrelated baseline repair was outside this order.

## Deferred human adjudication

- Decision: NONE
