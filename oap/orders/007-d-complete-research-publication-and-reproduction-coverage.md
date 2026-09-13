# Work order 007-d — Complete research publication and reproduction coverage

Status: FINAL

```oap-metadata
{
  "id": "007-d",
  "title": "Complete the research publication and reproduction coverage",
  "objective": "007",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "ee2d1b479719009ff1d07829478f241e3f395f7c",
  "branch": "oap/007-concept-verification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 8,
  "dependencies": [
    "001",
    "002",
    "003",
    "004",
    "005"
  ],
  "local_work": "Clean current local and remote PR #8 head 427aca4b86be984499ac44c0eec5e041d6535db2. Preserve all 007-c changes, published reports and private original experiment bytes.",
  "prior_review": "007-c remote report/parent/history verified; immutable result PARTIAL. Research/OAP CI pass, inherited Application baseline fails. Independent review found catalog/report/config/source/replay coverage incomplete, not a new scientific defect.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner 2026-09-11: publish all experiments, documentation/results and properly curated replication code under research/, excluding dataset data; no experiment artifacts may remain in /tmp."
    },
    {
      "kind": "I",
      "reference": "Strategic review of 427aca4b86be984499ac44c0eec5e041d6535db2: historical variant drivers/configs/generic prompts/narratives and safe detailed prior results missing; common frozen_choices generic; replay covers one case/schema only, not all claimed variants."
    },
    {
      "kind": "E",
      "reference": "007-c PARTIAL report and exact surviving private experiment/recovery/native artifact hashes; committed-byte scan found no known dataset passage matches. This correction addresses completeness, not tuning."
    },
    {
      "kind": "A",
      "reference": "S-ORDER-03/S-REVIEW-01 and communication sections 4/7: after a published PARTIAL report use the next suffix on the same PR. No rewriting c, no merge or normal roadmap."
    }
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
  "lr": [
    "LR-007",
    "LR-008",
    "LR-012",
    "LR-013",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "OAP bootstrap acceptance",
    "OAP report history",
    "Application baseline",
    "Research reproducibility"
  ],
  "decision_class": "D0"
}
```

## Identity

Next corrective suffix after immutable 007-c, SAME objective branch and PR #8.
ARCHIVAL PUBLICATION ONLY. This is not a new scientific iteration. No new Qwen,
Codex workload, benchmark or linguistic adjudication. Stop after publication.

## Current verified state

Main remains ee2d1b479719009ff1d07829478f241e3f395f7c.
Local/remote PR #8 head is 427aca4b86be984499ac44c0eec5e041d6535db2,
report 007-c with implementation parent 1b017a76ddb33c6a1d3af28233d6331067f88a9b.
Remote verify_report and historical report guard passed. Worktree is clean.
Research reproducibility, OAP bootstrap acceptance and OAP report history pass.
Inherited Application baseline fails; do not repair it. PR is OPEN/unmerged.
Main protection is disabled and unchanged. No merge is authorized.

## Provenance

The owner's all-experiment durable-publication mandate remains unfinished.
007-c did preserve originals, publish a useful catalog and latest pipeline core,
and strengthen the publication guard. It did not provide the complete historical
source/config/report trail or claimed algorithm replay coverage. Its PARTIAL
report is preserved, not amended. See the private strategic review and exact
published files; reports are claims to verify, not acceptance authority.

## Governance

The metadata lists unchanged accepted governance identities. Current CRITICAL
has zero actual entries; Decision class D0. No production or human gate crossing.
Explicit owner permission covers public OWNED research code and data-free results,
not dataset rows, filled prompts/responses, reasoning, private endpoints/credentials,
corpus/index/model bytes or a new code-license decision. Preserve upstream notices
and refer to pinned upstream tools rather than invent redistribution permission.

## Goal and dependencies

Finish the navigable, faithfully reproducible public research record for every
identified original attempt, recovery, variant, stopped trial, campaign and audit.
Retain all exact originals in reboot-safe private storage. Build on 007-c; do not
rebuild the archive from scratch or run another scientific experiment.

## Scope

Allowed: research/**, .github/workflows/research.yml, exact 007-d order/active/report,
PR #8 metadata. READ ONLY: existing concept-verification/**, product, existing tests,
scripts, pyproject.toml, uv.lock, governance, all earlier orders/reports, original
private experiments/recoveries/native archives and running service/profile state.
No merge, release, deployment, corpus acquisition, production/OAP infrastructure
changes, science tuning or new model calls. Do not change unrelated files.

## Non-goals

No new scientific evaluation, tuning, pipeline behavior, datasets, semantic labels,
model requests, production changes, merge, deployment or roadmap progression.
No deletion of originals or rewriting any previously published OAP report.

## Files and boundaries

Resolve STRATEGIC_HOME from runtime.env using its existing parser, never shell-source.
Read mandatory task-local review:
STRATEGIC_HOME/workorders/007-d-research-coverage-review.md.
Use prior 007-c order requirements 1–18 and private preservation README/RELOCATION.json
as evidence. Private roots are experiments/, recovery-executions/ and the ten
persistent native trees in that relocation map. Use existing inventories/manifests
and native copies, not another unbounded FUSE traversal of hundreds of thousands
of files. Inspect exact small source/config/report files; process raw inventories
mechanically. Do not print dataset text/credentials into OAP/public logs.

## Requirements

1. Preserve every existing commit/report and all private originals. Confirm no
   experiment-owned root remains in /tmp. All new scratch/env/test outputs must
   use an explicit owned persistent TMPDIR, with no /tmp fallback or alias.
   Keep relocation receipts; do not regenerate/modify old freezes.
2. Complete the catalog at experiment AND sub-run level: original 007-a/b failed
   executions, both replacements, all direct reasoning/mechanical variants,
   validator and contextual-unigram retry, word-only/whitespace continuation,
   hyphen/case changes, all three ten-trial studies with stopped-trial IDs, capped/
   uncapped campaign, spelling/4-worker/recovery stages, full 8-worker campaign,
   exhaustive u/v/random-sample analyses, retry10 and the read-only Levenshtein
   observation. Distinguish actual statuses from old RUNNING snapshots.
   Use stable child IDs and source/report/config/result hashes, not guessed
   generic status or conclusion. The inline Levenshtein source hash is unavailable.
3. For EACH study publish a readable data-free report/configuration projection
   with actual question, authorized change, exact relevant pipeline settings,
   generic prompts, inference fields explicitly sent/omitted, limits, data/index/
   English/source/environment identities, outputs, failures, denominators,
   limitations and conclusions. Link all from research/README.md. Remove passages/
   raw proposals/gold strings, but preserve numerical evidence and substantive
   experimental interpretation. Label strategic semantic assessment separately
   from human ground truth; create no new labels. Unknown historical facts stay
   UNKNOWN, not filled from the latest baseline.
4. Publish complete safe per-case/per-trial numeric evidence for the smaller
   studies and prior diagnostic/campaign phases, not only scalar top-level counts.
   Preserve first/retry/final distinctions, calls/tokens/latency/stopped outcomes,
   exact-gold vs prior semantic-assessment categories and case IDs. Project numeric
   final-campaign official/custom scores, confidence intervals, category/type data,
   retry ablation, preservation/detector/English/cost data and supplementary audits.
   Retain all original files privately; document field-level exclusions. Deterministic
   hashes/IDs replace content when needed. Never expose data-bearing dict keys.
5. Curate the ACTUAL owned source closure needed to reproduce the historical
   variants and campaign: loaders/adapters, inference capture/client/drivers,
   concurrency/checkpoint/resume/failure policy, variant prompts/gates, scoring/
   bootstrap/analysis tools. Latest-core fragments and documentation-only future
   live execution are insufficient. Simpler separate historical modules are fine.
   Prefer faithful copies with explicit resource/path injection over redesign.
   Extract embedded dataset fixtures into private inputs; generic prompts remain.
   No hidden absolute private imports, no dependency on strategic filesystem or
   /tmp, no network/import side effect, no live execution in this round.
6. Every original-to-curated source mapping must state exact file/function coverage
   and transformations. Do not claim all of common.py/bootstrap_stats.py/retry.py
   is preserved by unrelated/latest helper fragments. Public source missing a
   historical behavior must be completed or explicitly marked unavailable with
   a concrete source gap. Preserve old standalone scripts privately without edits.
7. Provide executable opt-in reproduction entry points/commands for historical
   variants and campaigns, with explicit authorized inputs, index, endpoint,
   credential ENV reference, persistent output directory and resource budget.
   Default/import/tests remain offline. No commands may trigger a model by
   accident. Pin research-specific dependencies from observed working environments,
   include upstream scorer/tool revisions and installation recipe; do not change
   production lock. Record inference differences without retuning.
8. Correct and extend offline saved-sample replay: handle both small-study
   original/decisions and campaign input/decisions/first/retry schemas. No missing
   English value may silently become zero. Use the correct frozen detector cap/
   uncapped setting and saved evidence; fail explicitly on unverifiable fields.
   Reproduce detector/English selections, gates, case rules, patches and M3 from
   first-stage samples, including KEEP/WIDER/parser/first/retry-only failures and
   full-example fail-closed semantics. Cover each distinct historical behavior
   with preserved records where available; report unavailable samples distinctly.
9. Replay complete final-campaign targeted records where source/sample evidence
   permits, using persistent native copies and verified index, zero model calls.
   Compare against originals without rewriting them; a mismatch is evidence to
   investigate at curation/replay boundary, never permission to change history or
   science. Also demonstrate baseline ten-study replay and representative earlier
   variants. Emit data-free per-record receipt/counts and honest gaps.
10. Fix documentation interpretation hazards: detector-only known_errors_remaining=0
    is unusable; timeout-300 workload association invalid; SloBench/MultiGEC-test
    have no references and apparent TP/FP/exact fields cannot be interpreted as
    correctness/harm; identity/token-identical DASSLE pairs are not repairs;
    official/custom denominator differences and post-hoc scope restrictions stay
    explicit. Owner marked essay test irrelevant to target regime, but all actual
    results remain documented. Do not infer harm from non-reference edits alone.
11. Document current benchmark conclusions quantitatively without new semantic
    labeling or invented GO: targeted recall limitations, preservation advantage,
    retry tradeoff, official-score comparisons, blocked remote scores and excluded
    Deployment B. Preserve clock accounting discrepancies and original-index
    byte-loss/logical-rebuild distinction. Safe selected observation summaries
    contain IDs/counts, not dataset examples.
12. Reconcile the file census using explicit original/private/current locations.
    A strategic mirror lacking native result files is not the native root. Do not
    claim all entries verified from a first100 check. Build a portable logical-root
    mapping format and documented hash verification. Reuse completed archive and
    8197-source/resource recheck receipts; avoid gratuitous re-archiving large data.
    Add a durable migration guide and private location pointer without public paths.
13. Preserve and extend publication safety: scan actual staged/committed bytes,
    compressed JSON and all new report/config/source artifacts before any push.
    Test raw/short-text/base64/credential/symlink/overwrite failures. Scan against
    actual prepared source/reference/controlled fixtures privately. Make narrow
    schema allowances for justified numeric/config/generic prompt artifacts;
    never generic allow-all or silently dropped scan coverage. Public output must
    remain dataset-free.
14. Add focused tests for faithful variant selection, actual saved-sample replay,
    no-reference metric masking, complete catalog/subrun/source links, deterministic
    report/table rebuild, explicit missing-resource failures, no network defaults,
    correct index/root relocation, resume no-resampling and safe publication.
    Existing strategic synthetic regressions stay green. No linguistic-success
    fixtures predicting Qwen answers.
15. Run focused research tests, source compile/import portability checks, replay,
    publication scan, deterministic regeneration, OAP tests/transcript/history/
    governance, protected diff, diff --check, fsck. Use persistent isolated pinned
    research env if needed for Ruff/mypy; do not report ordinary install work as
    permanently impossible without bounded investigation. Full application checks
    remain separately reported; do not repair their inherited failures.
16. Complete all independently executable acceptance before final report. Do not
    declare complete merely because CI is green or the originals have hashes.
    Record any genuine unavailable historical evidence and scope honestly. Commit/
    push implementation/order/active and update readable PR metadata FIRST.
17. Publish exactly one report-path-only SELF commit at:
    oap/reports/007-d-complete-research-publication-and-reproduction-coverage.md
    with actual implementation parent, verify remote bytes/head/history and send
    exact OK. Do not change the report after publication. Do not merge or resume
    experiments/roadmap afterward.

## Acceptance criteria

1. Public research is navigable by all actual experiments and child runs, with
   complete data-free report/config/metrics/source trail and private dispositions.
2. Reproduction code covers actual historical behaviors and campaign execution/
   analysis, uses explicit portable resources, and is independently replay-tested
   against available saved evidence; zero scientific/model reruns occurred.
3. No original bytes lost/changed, no experiment artifacts remain in /tmp, and
   actual public Git bytes pass privacy scans with no dataset/credential exposure.
4. Focused research and protocol checks pass; inherited Application failure and
   genuinely unavailable optional metric/history evidence stay explicit.
5. Exact same-PR remote/report publication verified; no merge/production claim.

## Verification

- python3 -B -m unittest discover -s research/tests -v
- pinned research-only Ruff/mypy and compile/import checks, no product lock edits
- all-variant and full-campaign offline replay with private data-free receipts
- deterministic report/config/metric/table rebuild and committed source mapping check
- staged publication guard plus actual private-source overlap scan
- full existing pytest/application baseline with inherited failures documented
- python3 -B -m unittest discover -s oap/tests -v
- check_transcript.py --index and --revision HEAD --expected-id 007-d
- check_report_history.py --revision HEAD --require-manifest
- accepted/candidate governance against exact accepted main, protected source diff
- git diff --check, git fsck, exact-head GitHub checks including Research reproducibility

## Local setup and constraints

Normal reversible local implementation/dependency installation is allowed only
inside persistent owned task directories. Use existing preserved environments
read-only; create a new pinned task environment if needed. No dataset/model/server
requests or resource/profile/service changes. Never expose credentials or private
paths in public artifacts. Finish D0 setup without involving owner as terminal relay.

## Documentation

Make research/README.md the scientific navigation, not only a hash catalog.
Provide reports/configs/trial summaries/method definitions/recipes/metric limits.
Private exact originals and relocation/backup receipts remain untouched and linked
by logical identity. Preserve prior narrative as redacted projection, not overwrite.

## Git and report publication

AMEND_EXISTING_PR #8 on oap/007-concept-verification only. Publish scoped new commits;
no rewrite, force push, history deletion, auto-merge, merge, new PR or numeric objective.
Old reports are immutable. Current CI evidence is SHA-specific; report cannot claim
future publication/CI. User authorized archive publication, not product acceptance.

## Decision classification

D0. Explicit owner instruction defines storage/publication/exclusion boundaries.
This round changes archival/reproduction implementation, not frozen scientific choices.

## Deferred human adjudication

- Decision: NONE
