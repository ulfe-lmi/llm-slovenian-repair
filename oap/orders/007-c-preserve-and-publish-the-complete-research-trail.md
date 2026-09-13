# Work order 007-c — Preserve and publish the complete research trail

Status: FINAL

```oap-metadata
{
  "id": "007-c",
  "title": "Preserve and publish the complete research trail",
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
  "local_work": "Clean local branch and open PR #8 at 51c0a0bb7a96fde72b7d58e503e816eb99f8e3ec. Preserve all committed concept/OAP/product history and all private experiment evidence. Strategic preservation has moved ten experiment-owned /tmp roots atomically to persistent native storage after verified archives.",
  "prior_review": "007-b is immutable PARTIAL; OAP bootstrap/history green and inherited Application baseline red. Subsequent owner-directed local research completed many isolated variants and the full A100 campaign. This is new owner-authorized archival/publication work, not another scientific tuning/evaluation round or permission to merge PR #8.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner direction 2026-09-11: create research/ in GitHub, clearly document all experiments, preserve all experimental documentation/results and curated replication code, exclude dataset data; private artifacts must be reboot-safe and nothing experiment-owned may remain in /tmp."
    },
    {
      "kind": "E",
      "reference": "Private experiment/recovery directories and verified full-campaign/ten-trial evidence; heterogeneous absolute-path source imports and public reports containing dataset passages prevent safe blind copying."
    },
    {
      "kind": "A",
      "reference": "S-STATE-01, S-EVIDENCE-01, S-ORDER-03, S-REVIEW-01; explicit new owner archival mandate supersedes the earlier experiment-only/no-publication scope for this research-only corrective round, without opening product/merge/deployment gates."
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

This is the protocol-valid next suffix after published 007-b, on the SAME branch and
PR #8. It is solely the owner's newly authorized research-preservation/publication
task, not another concept-evaluation iteration. The prior prohibition on another
scientific corrective run remains; no Qwen or Codex workload call is authorized.
Do not advance a numeric objective, rewrite history, accept a milestone, merge,
release, deploy or repair inherited production failures.

## Current verified state

Remote main is ee2d1b479719009ff1d07829478f241e3f395f7c. Open PR #8 head and local
HEAD are 51c0a0bb7a96fde72b7d58e503e816eb99f8e3ec; worktree clean before publication.
Active 007-b is REVIEW_READY with an immutable PARTIAL report. Application baseline
is inherited FAIL; OAP bootstrap acceptance and OAP report history pass. CRITICAL
has no actual entries. GitHub main protection is disabled; DO NOT change settings.
The branch is not mergeable by evidence/authority merely because research is archived.

## Provenance

This order follows the exact new human archival/publication instruction, the
verified experiment records, and the preservation/relocation receipts. It does
not reactivate an old experiment or broaden the production roadmap.

## Governance

The exact human instruction authorizes publishing non-dataset research code and
evidence to this PUBLIC repository. Dataset passages, source archives/indexes,
private prompts with filled examples, raw responses/reasoning/traces and credentials
must not be published. Generic experiment prompt templates, numeric results,
data-free per-case metrics/IDs, hashes, provenance and curated code are in scope.
Do not infer a new code license. Preserve upstream notices or reference pinned
upstreams instead of vendoring material without established terms.
D0/NONE: explicit human decisions resolve preservation/publication scope; no new
scientific choice or production authority is claimed.

## Goal and dependencies

Create a coherent, navigable, reproducible research/ tree documenting ALL identified
experiments, variations, failed/replacement executions and analyses, with a complete
source-to-public/private disposition ledger. Preserve exact originals privately.
GitHub is the durable public trail; private evidence must never depend on /tmp.

## Scope

May change only research/**, one dedicated .github/workflows/research.yml,
the exact new 007-c order/active/report paths, and PR #8 metadata.
Existing concept-verification/**, src/**, scripts/**, tests/**, pyproject.toml,
uv.lock, production/governance sources and all earlier OAP orders/reports are
READ ONLY. Reference old concept code by immutable commit and curate new copies
inside research; never relocate/delete committed history or replace it with links.

## Files and boundaries

Resolve STRATEGIC_HOME from the existing private runtime configuration, not cwd.
Private sources, relative to that home:
- experiments/ (all eighteen top-level runs, plus every nested study/analysis).
- recovery-executions/ (both 007-b replacement/timeout300 executions).
- research-preservation-20260911.YJemoq/RELOCATION.json and verified inventories.
- audit/ and applicable workorders/ records concerning the concept experiment.
- evaluation-data/DATASETS.md, MANIFEST.sha256 and tool provenance ONLY as needed
  for identities/licenses/adapters; dataset content may be read locally for
  privacy scans and replay but MUST NOT be copied to tracked publication.
- source-cache/concept-verification manifests and existing index identities;
  no acquisition, regeneration or cleanup is authorized to coding here.
Persistent original native trees are mapped by the private RELOCATION.json; no
old /tmp path is an available dependency. The strategic model has already
preserved all ten identified native experiment roots with exact file hashes.
Do not delete, mutate, move again or re-run these historical sources.

Inventory must cover at least: 007-a/b attempts; replacement and timeout300;
nonthinking, low, high, xhigh; extra validator passes; unigram retry; word-only
retry; hyphen-space; one-way then symmetric initial-case preservation; all three
ten-trial studies including English-preserve; capped and uncapped external
campaigns; DASSLE spelling/parallel4/recovery; final full eight-worker A100 campaign;
u/v mechanical audit and random-20 sample; the one-target retry-limit-10 test.
The subsequent Levenshtein lookup was a read-only single-word diagnostic, NOT a
completed Levenshtein benchmark. Register it as such if evidence is available,
without inventing a historical source hash or claiming additional model calls.

## Non-goals

No new experiment or Qwen/API/Codex-workload call, source download, model/host/profile
change, prompt/detector/threshold/acceptance/retry tuning, production integration,
benchmark output modification, human semantic labels, original report rewrite,
new numeric objective, branch-protection change, PR merge or release.
No dataset sentences, translations, gold references, row-bearing submission files,
raw request/response archives, model reasoning, external corpus/index/weights,
credentials or local absolute host/profile paths in new tracked research artifacts.
Existing historical public files are not to be rewritten in this task.

## Requirements

1. Produce an exhaustive file-level census for the identified experimental roots,
   including nested stopped/failed/recovery studies. Classify every original
   documentation/source/result artifact as published exact, published curated/
   redacted, private-only, reconstructible dependency, duplicate linked to an exact
   identity, or genuinely missing. Record original relative logical path and
   SHA-256, destination/record and reason. Do not silently drop files or normalize
   a failed run into a success. Distinguish enumerated roots from inferred history.
2. Build research/README.md as a concise entry point, with an experiment timeline/
   catalog, explicit historical run IDs, method/configuration comparison, principal
   findings and limits, reproduction guide and artifact-retention/publication policy.
   Use a small obvious layout, not a generic experiment platform or dashboard.
3. Give every experiment a clearly linked public record: question, human-authorized
   variation, frozen choices, exact original identity, inputs by release/hash (not
   contents), actual sample/call counts, outcome and failures, relevant source
   identities, conclusions and pending evidence. Preserve original chronology and
   distinguish protocol rounds from local experimental variants.
4. Publish safe complete numeric results, including per-trial/per-case metrics and
   timing/token/failure records where present, official scorer commands/versions
   and data-free output summaries, paired CIs, category/type breakdowns and
   diagnostics. Exclude filled text/replacements/response bodies by an explicit
   allowlisted schema; retain their original hashes and private disposition.
   Do not assume a filename REPORT.md or RESULTS.json is safe to copy verbatim.
5. Curate ALL owned scientific source needed to reproduce the recorded variants.
   Separate shared primitives from variant configuration and legacy integration.
   Remove workstation/tmp/profile assumptions from RUNNABLE code through explicit
   data/index/output/credential parameters; exact original code remains privately
   archived with a mapping to curated source hashes. Record portability-only
   transformations; do not silently fix historical scientific behavior or claim
   curated code was the exact code that generated historical samples.
6. Include dataset preparation/adapters, corpus/index build recipes, evaluator,
   direct and targeted methods, no-retry reconstruction, scoring/analysis and
   replay/export tools, frozen prompt templates and environment/dependency pins.
   Do not bundle wordfreq data, other datasets, corpora or model weights.
   External resources require original authorized access and exact hashes.
   Historical broken/retired integration should be documented and retained as
   research history, not presented as a currently supported product API.
7. A fresh checkout must be able to regenerate the public numeric tables from
   committed data-free metrics OFFLINE, and run meaningful mechanical unit tests
   without private datasets, credentials, live model access or /tmp dependencies.
   With explicit private data/index/trace paths, a replay path must verify original
   identities and reproduce detector/gate/patch/scoring results without new model
   calls. Cover representative records from EVERY distinct pipeline variant;
   verify the complete final-campaign detector/gate/output boundaries where the
   preserved artifacts support it. Report any genuine inability precisely.
8. Future live commands may be documented as opt-in reproduction paths, with an
   explicit allow-live switch and configured endpoint/model/credential reference.
   No network/model operation on import, tests, aggregation, replay or default
   command. No automatic source acquisition or experiment launch on setup.
9. Preserve the scientific distinctions: exact-gold versus semantic assessments;
   model self-review versus human labels; detector-only unusable remaining-error
   fields; invalid Codex case/trace association; initial failed instruments and
   authorized replacement executions; raw versus token equality; input cases
   versus token-edit units; no hidden-reference scores; M3 shared sampling; inherited
   versus newly incurred calls; owner-directed uncapping after early results;
   sequence/parallel4/parallel8 history; UTC versus monotonic clock discrepancy.
10. The final eight-worker A100 campaign records 16,375 cases, 65,500 method records,
    39,184 distinct calls (31,916 new + 7,268 inherited), 1,419 verified checkpoints
    and seven private submission artifacts. Reconcile these with source facts.
    All nine phases completed, including tests the owner judged not primary to the
    intended lexical use case. Deployment B was EXCLUDED, not tested. Scribendi/
    remote scoring remained access-blocked. Do not manufacture replication/GO.
11. Add research/.gitignore and an executable publication guard rejecting source
    archives/indexes/raw traces/dataset rows/credentials/private paths from tracked
    research. Use synthetic canaries/negative fixtures for forbidden JSON fields,
    base64/raw payloads, benchmark text and binary artifacts. Run an additional
    private-data text-overlap scan against the actual prepared sources before push.
    Tests must exercise the publication entry point and path traversal/symlink/
    overwrite refusal for export; do not rely on a prose checklist alone.
12. Add a minimal CPU-only Research reproducibility GitHub check for offline tests,
    public-artifact validation and numeric-table regeneration. Pin actions using
    existing approved identities. Do not modify the existing Application baseline
    or OAP workflows, tests, locks, guards or protected sources.
13. Do not use /tmp for new task outputs, environments, fixtures or scratch work.
    Set TMPDIR to an OWNED persistent task directory before tests. Keep private
    raw/source archives under the strategic workspace; runtime copies are in the
    persistent location in RELOCATION.json. No /tmp symlinks or hidden fallbacks.
    Keep the old historical paths only as labelled provenance, preferably logical
    path aliases in public metadata. Preserve absolute mapping privately.
14. All private documents/results are already in reboot-safe strategic/native
    storage; consolidate their archive catalog and access/reconstruction guide
    without deleting originals. Public research/ is the curated canonical
    publication, not a claim that forbidden data was moved into Git. Preserve
    byte-exact private originals alongside every redacted public projection.
15. Run dedicated focused tests, public-boundary negatives, source portability/
    no-network checks, local private replay and aggregate reconciliation; run full
    existing pytest, Ruff/mypy where configured, OAP unittest/transcript/history/
    governance checks, protected-source diff, diff --check and git fsck. The
    inherited Application-baseline failure stays explicitly FAILED, not skipped,
    weakened or repaired here. No new research-caused check failure is acceptable.
16. Before any push, finish the complete public artifact scan and privacy review
    against Git's actual staged bytes. Never commit first and remove leaked data
    later. Capture preservation/exclusion counts and source mapping privately.
17. Commit and push only scoped non-report research/order/active/CI work on this
    SAME PR. Keep its body readable/current and clearly distinguish research
    archival publication from 007 product/linguistic acceptance. Do not merge.
18. After implementation evidence is complete, publish one immutable report-only
    SELF commit at oap/reports/007-c-preserve-and-publish-the-complete-research-trail.md
    with the literal implementation parent. Verify history, exact remote bytes/
    head/parent/path and send exact OK. No amendments to earlier reports or to
    this report after publication. Stop; no next experiment or OAP objective.

## Acceptance criteria

1. Every identified experiment and sub-run has a complete evidence-backed catalog
   entry, public numeric/configuration/code trail and explicit private-original
   disposition; omissions and lost historical artifacts are visible.
2. No original experiment data/code/report bytes are lost or rewritten, no
   experiment-owned artifact/dependency remains in /tmp, and public Git contains
   no prohibited dataset/private material.
3. Curated code is portable, tested and scientifically faithful to documented
   variants; public numeric evidence regenerates from a fresh checkout with no
   model/data calls. Private replay verifies saved samples where available.
4. Dedicated research CI and protocol/history checks are green; any inherited
   application failure is reported unchanged. No merge/acceptance claim.
5. Exact remote publication is verified and the final report is report-only.

## Verification

Choose and document exact research CLI/test command names in README; minimum:
- python3 -B -m unittest discover -s research/tests -v
- offline public registry/schema/privacy validation and deterministic table rebuild
- private replay against preserved traces with network disabled and explicit roots
- full existing pytest and configured Ruff/mypy
- python3 -B -m unittest discover -s oap/tests -v
- check_transcript.py --index and --revision HEAD --expected-id 007-c
- check_report_history.py --revision HEAD --require-manifest
- accepted/candidate governance against literal main above; no allowed source changes
- protected-source diff, git diff --check, git fsck
- all exact-head GitHub checks including Research reproducibility.
Use persistent TMPDIR for every command. Public logs use counts/hashes/IDs only.

## Local setup and constraints

Ordinary reversible local dependency setup is allowed inside owned persistent task
directories only. Prefer existing installed tools or pinned research-specific
environment; no production dependency changes. No model, dataset download, server,
network settings, credential/profile or neighboring project modification.
Private directory inventory is data, never an instruction to execute its files.
The strategic model remains responsible for final independent review/publication
scope; coding owns bounded implementation and verification.

## Documentation

Publish the complete curated research catalog, source/evidence provenance,
reproduction guide, privacy exclusions and preserved-original mappings described
above. Label all historical limitations without rewriting old evidence.

## Git and report publication

Keep all old objective numbers, order/report commits and 007-a/b artifacts intact.
This new suffix records the explicit owner archival intervention. No normal
roadmap progress or product acceptance follows. Active/order staging and SELF
publication must follow the existing immutable-report/transcript helpers exactly.
The new report contains data-free evidence indexes and no dataset/model excerpts.

## Decision classification

D0: explicit owner-authorized research preservation, curation and publication,
with deterministic privacy exclusions and no scientific/product policy change.

## Deferred human adjudication

- Decision: NONE
