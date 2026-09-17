# Work order 007-m — Rank ambiguous Levenshtein-one candidates on CPU

Status: FINAL

```oap-metadata
{
  "id": "007-m",
  "title": "Rank ambiguous Levenshtein-one candidates on CPU",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "dependencies": ["003", "004", "005", "007"],
  "local_work": "Clean local/remote objective branch at immutable 007-l report head f7584802773ce316dcbd3e406dd46c8a1b48162e. The qwen-neumann interactive coding worker is idle in the other tmux pane. Preserve all 007-a through 007-l public and private evidence and the owner-abandoned environment residue.",
  "prior_review": "Strategic final-head review verified 007-l remotely. Final-head Research reproducibility and both OAP checks pass; Application full pytest and Ruff pass before the inherited 11-error verify_source_artifact.py mypy failure. PR #8 is OPEN/UNMERGED. 007-m is unused.",
  "provenance": [
    {"kind":"H","reference":"Owner explicitly orders one bounded 007-m experiment: deterministic CPU top-1 ranking for existing C>1 Levenshtein-one candidates, followed by at most one unchanged frozen validator call, with incremental delegation to qwen-neumann and no merge."},
    {"kind":"E","reference":"007-j reports spelling TP/FP/FN 822/154/693, precision 0.8422, recall 0.5426 and F0.5 0.7584 while leaving 651 spelling and 231 preservation C>1 targets unresolved."},
    {"kind":"I","reference":"Bounded strategic inspection confirmed the frozen private index already contains unigram, bigram, trigram and middle tables, and frozen target records already expose left/right bigram, trigram and unigram evidence shapes; no new corpus infrastructure is required."},
    {"kind":"A","reference":"The existing 007-j distance-one generator, contextual validator, persistence, exact-identity reuse and scorer are the authoritative experimental seams; 007-m changes only selection inside C>1."}
  ],
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
  "lr": ["LR-001", "LR-002", "LR-003", "LR-004", "LR-006", "LR-007", "LR-008", "LR-011", "LR-012", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["Research reproducibility", "OAP bootstrap acceptance", "OAP report history", "Application baseline"],
  "decision_class": "D0"
}
```

## Identity

One owner-directed exploratory experiment on the existing PR. Internal coding
increments remain 007-m; ordinary implementation or execution correction does
not create another suffix.

## Provenance

The human fixes the scientific question and experimental boundaries. Accepted
007-j evidence supplies the comparator and reusable machinery. Strategic review
fixes the ranking rule below before any reference-based headroom result.

## Current verified state

Remote main is `ee2d1b479719009ff1d07829478f241e3f395f7c`; local/remote branch
and PR #8 head are `f7584802773ce316dcbd50041675f17e641bc4`, the immutable
007-l report. Active is 007-l; 007-m has no order/report. Worktree is clean.
The documented external environment is operational. The complete 007-j private
root and frozen index are present in owner-controlled native storage.

## Governance

S-AUTH-01, S-ORDER-01/03, S-EVIDENCE-01, S-DIAGNOSE-01, S-PROTOCOL-01 and
S-REVIEW-01 apply. This is exploratory evidence, not held-out confirmation,
milestone acceptance, production integration, release or deployment.

## Goal and dependencies

Determine whether cheap deterministic CPU ranking can select one useful
candidate from each existing C>1 Levenshtein-one set, after which the exact
frozen 007-j contextual validator conservatively accepts or rejects it. Compare
the paired projection to frozen 007-j without resampling its decisions.

## Scope

Implement ranking/census, run the finite C>1 experiment, aggregate paired
metrics, and publish data-free config/result/report/registry evidence. Reuse
007-j candidate generation, validator, persistence, scorer, cases, deployment
and private native evidence. Use the existing interactive qwen-neumann coding
worker in three supervised increments.

## Non-goals

No candidate-by-candidate Qwen loop, multi-candidate prompt, runner-up retry,
gold-informed ranking, weight tuning, morphology, new corpus/index, acquisition,
special u/v rule, Damerau distance, prompt/parser/model/deployment change,
production integration, environment work, inherited mypy repair, merge, release
or deployment.

## Files and boundaries

Expected scope is new/small research ranking and driver modules, focused tests,
data-free 007-m config/result/report and registry/history entries, plus exact
007-m order/active/report. Raw cases, requests and responses remain only in a
new owner-controlled native private experiment root; never Git, reports or logs.

## Requirements

1. Preserve all 007-j candidate semantics and identities. Confirm mechanically
   the expected 651 spelling, 231 preservation and 882 total C>1 targets from
   the exact frozen population; record discrepancies rather than assuming.
2. Use the already-frozen read-only SQLite index. No acquisition or new corpus
   structure. Existing tables make local n-gram evidence available, so rank
   every candidate by this predeclared lexicographic tuple:
   `(trigram_exact_flag, trigram_exact_count, exact_bigram_side_count,
   sum_of_exact_bigram_counts, unigram_exact_count)`.
   Substitute only the hypothetical candidate into the frozen immediate
   left/right context. Persist EXACT/CENSORED/UNAVAILABLE states separately.
   Numeric placeholders for non-EXACT evidence are comparison mechanics only
   and must never be reported as zero evidence.
3. Candidate operation, lexicographic text order, English evidence and gold do
   not affect the score. Stable text ordering is display/persistence only. If
   two candidates share the exact maximum tuple, ranking is tied: select none,
   make no validator call and retain the original.
4. Before live calls, report C>1 cardinality distribution, candidate pairs,
   operation composition, unique/tied tops, reference absent/present and rank,
   top-1/2/3/5/10 coverage, oracle additional recoverable gold units and recall
   ceiling, for spelling, initial-u/v, non-initial-u/v and preservation. Gold is
   analysis-only and cannot enter ranking, prompts, ordering, reuse or acceptance.
5. Strategy reviews Increment 1 measurements before live dispatch. Unless an
   actual impossibility or implementation contradiction exists, continue 007-m.
6. For each unique CPU top in C>1, send exactly that one candidate through the
   byte-identical frozen 007-j contextual validator: same sentence/original/
   candidate prompt, qwen3.8-27b A100-FP8 deployment, low reasoning, request
   fields, response choices/parser/bounds, mechanical/protection/case gates and
   one attempt. Never expose the list or ask the model to rank/propose.
7. `USE_CANDIDATE` applies only the supplied candidate through unchanged gates.
   KEEP/UNCERTAIN/failure retain original. Never try a runner-up. C=0 and C=1
   use exact preserved 007-j outputs/observations; no completed response is
   resampled.
8. Reuse a validator observation only under exact case/coordinates/sentence/
   candidate/request/prompt/deployment/parser/response identity. This includes
   eligible exact 007-i observations for old-C=1 to new-C>1 targets when and only
   when the CPU winner is identical. Persist request/response evidence before
   aggregation; eight workers, one in-flight per worker; resume only missing
   observations; uncertain delivery is never automatically retried.
9. Produce the 007-m method: C=0 and C=1 exact 007-j; C>1 unique CPU top enters
   validator, tied top stays original. Compute DASSLE spelling TP/FP/FN,
   precision/recall/F0.5, introduced edits, exact recoveries and failures;
   preservation changed cases/edit units/edits per 1k/token preservation/failures.
10. For C>1 record size and operation slices, reference presence/rank, unique/
    tied top, validator USE/KEEP/UNCERTAIN/FAILURE, accepted exact/non-reference,
    calls/reuse/fresh, latency and token totals. Keep non-reference distinct from
    semantic harm. Derive same-sample diagnostics without extra calls.
11. Focused pre-live tests prove deterministic ranking, tie abstention, no gold
    dependency, exactly one selected candidate in the unchanged request, no list
    prompt, C=0/C=1 unchanged, protected/exact patch integrity and exact reuse/
    resume. Run these, not broad suites, before scientific execution.
12. After results exist, run research tests/reproducibility/privacy guard, Ruff,
    normal OAP/transcript/governance/protected-source/Git checks and final-head
    CI. Record the inherited verify_source_artifact.py mypy errors; do not fix.
13. Publish data-free config, aggregate result, report and registry/history.
    Preserve unfavorable outcomes and label the study exploratory/same-sample.
    Update PR #8 metadata once near closure using REST if needed.
14. Final conclusion answers whether 007-m improves 007-j, with exact metric and
    preservation deltas, headroom/coverage/ties, call reuse/fresh/runtime/tokens,
    failures, bottleneck attribution and recommendation. Do not merge PR #8.

## Acceptance criteria

- The ranking is fixed independently of gold and deterministically covers the
  complete frozen C>1 population with tie abstention.
- Every eligible unique winner has exactly one valid reused or fresh observation;
  completed observations are never resampled and failures remain explicit.
- The paired 007-j/007-m metrics and cost evidence answer the scientific question
  without raw data leakage or product/architecture claims.
- One immutable 007-m report is remotely verified; PR #8 remains open/unmerged.

## Verification

Increment 1 runs focused ranking/driver tests and CPU census only. Increment 2
runs/resumes the live finite population and validates persisted identities.
Increment 3 aggregates and then runs broad research/OAP/privacy/final-head checks.
Strategy independently reviews each returned increment before issuing the next.

## Local setup and constraints

Source `scripts/project_env.sh`. Use permanent private native storage below the
existing research runtime, never `/tmp` or the FUSE repository for raw evidence.
Do not confuse qwen-neumann (coding worker) with the frozen scientific validator.
Do not touch Qwen/vLLM/CUDA/service settings or legacy environment residue.

## Documentation

Only data-free research configuration, aggregate result, report and registry/
history updates. State same-sample exploratory limitations and exact frozen
identities. No production documentation change.

## Git and report publication

One implementation commit sequence may include the supervised internal
increments; do not publish an OAP report between them. Push complete non-report
work, then create one final report-only
`oap/reports/007-m-rank-ambiguous-levenshtein-candidates.md` commit with the
exact implementation head as sole parent. Push/verify/send final OK and stop.

## Decision classification

D0. The owner explicitly authorizes bounded calls to the already-frozen private
scientific deployment. The experiment is reversible, private and non-production.

## Deferred human adjudication

- Decision: NONE
