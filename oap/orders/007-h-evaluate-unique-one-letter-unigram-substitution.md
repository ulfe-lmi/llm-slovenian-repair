# Work order 007-h — Evaluate unique one-letter unigram substitution

Status: FINAL

```oap-metadata
{
  "id": "007-h",
  "title": "Evaluate unique one-letter unigram substitution",
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
  "local_work": "Clean local and remote PR #8 at strict-valid 007-g report commit dfeda1658c5c12f0bbb7de20d6e046d6eba10ea1. Preserve every prior order/report/research artifact and private result byte-for-byte. No experimental calculation for this new rule has run.",
  "prior_review": "007-g report is strict-remote-verified. Report-head Research, OAP bootstrap and OAP report history checks pass. Application same-head retry passes copied full pytest and Ruff, then fails only at the inherited 11-error verify_source_artifact.py mypy boundary. PR remains open/unmerged; branch protection remains disabled. Bounded reconnaissance proves 1,487 spelling records are exactly paired with saved M2 decisions and the 1,486 preservation records use the same archived schema, so a zero-resampling offline experiment is feasible.",
  "provenance": [
    {
      "kind": "H",
      "reference": "Owner directs exactly one bounded unique one-character Slovene-unigram substitution experiment before Qwen review, using DASSLE spelling and preservation, frozen fallback decisions, no new model calls, no tuning and STOP after reporting."
    },
    {
      "kind": "E",
      "reference": "Private DASSLE spelling baseline has 1,487/1,487 matching dataset/result IDs and input hashes, 2,008 detector candidates, 7 English suppressions, 2,001 eligible OOV targets, 2,001 saved first reviews, 209 saved retries and 40 M2 operational-failure cases."
    },
    {
      "kind": "E",
      "reference": "Frozen inputs: spelling 045825b7..., preservation d77d6942..., detector snapshots d401d583.../6e020b76..., baseline config 4c748b8e..., baseline results 3a75c4da..., u/v audit 6d6fb695..., unigram index f769235b... with 141,162 forms."
    },
    {
      "kind": "I",
      "reference": "Strategic bounded reconnaissance d4a29103096f23beff869612b2f62972732c1cb9bd35bbd5662f7e1bc2e1b854 establishes exact paths/schema, offline replay feasibility, scorer boundary, fixed experimental decisions and stop conditions without calculating outcomes."
    },
    {
      "kind": "A",
      "reference": "S-ORDER-03 permits the next suffix 007-h on the same objective/PR after strict-valid 007-g. The human experiment instruction supersedes further roadmap progression but does not authorize merge, production integration or live inference."
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
    "LR-002",
    "LR-003",
    "LR-007",
    "LR-008",
    "LR-012",
    "LR-013",
    "LR-014"
  ],
  "relevant_gates": [],
  "required_checks": [
    "Research reproducibility",
    "OAP bootstrap acceptance",
    "OAP report history",
    "Application baseline"
  ],
  "decision_class": "D0"
}
```

## Identity

Immediate experimental suffix after strict-valid 007-g, on the SAME objective-007
branch and PR #8. Exactly one new offline paired experiment. It does not amend a
prior experiment, resume the roadmap, integrate production code, merge or deploy.

## Provenance

The owner's current instruction fixes the complete scientific question, algorithm,
dataset views, fallback boundary, prohibited variations and stop condition. The
private reconnaissance below establishes that the saved baseline is sufficient;
no scientific outcome has been inspected and no threshold or tie rule remains to
choose.

Mandatory private source, read in full:

- `STRATEGIC_HOME/workorders/007-h-one-substitution-reconnaissance.md`
- SHA-256 `d4a29103096f23beff869612b2f62972732c1cb9bd35bbd5662f7e1bc2e1b854`

## Current verified state

Main is `ee2d1b479719009ff1d07829478f241e3f395f7c`. Local/remote PR #8
head is `dfeda1658c5c12f0bbb7de20d6e046d6eba10ea1`, the strict-valid
007-g report-only commit with implementation parent
`178c58275314a32a93a8b3ac0227c014afe67b81`. PR #8 is OPEN and
UNMERGED. Research/OAP/report-history checks are green. Application baseline is
red only at the inherited 11-error source-verifier mypy boundary after copied
full pytest/Ruff pass on the unchanged-head retry. CRITICAL is empty. Main branch
protection is disabled; do not change settings or merge.

## Governance

S-AUTH-01, S-PRODUCT-02/03/04, S-ORDER-01/03, S-EVIDENCE-01,
S-DIAGNOSE-01 and S-REVIEW-01 apply. This is an explicitly authorized isolated
concept experiment. Existing production acceptance evidence, OAP history,
privacy/source rights, protected-span behavior and no-merge boundary remain intact.
No D1/D2 decision or CRITICAL append is required.

## Goal and dependencies

Measure whether the exact unique one-code-point substitution lane repairs a useful
subset of detector-selected, English-unsuppressed Slovene OOV targets and reduces
projected Qwen calls without degrading reference-text preservation. Dependencies
are the frozen objective-007 research archive, exact DASSLE spelling/preservation
inputs, saved M2 decisions, existing scorer and frozen unigram index. No new data,
labels or model output is required.

## Scope

Create one deliberately experimental offline module/driver under `research/`,
focused tests, one new data-free config/report/machine-result record, and additive
navigation/registry/table entries. Create one unique private experiment root under:

`/home/ubuntu/.local/share/llm-slovenian-repair/research-runtime-20260911.YJemoq/`

Stage exact private named inputs/results there once, verify identities, freeze the
configuration, execute once, retain full private per-case evidence there, and
publish only safe aggregates/hashes. Update PR #8 body through GitHub metadata.

## Non-goals

No live Qwen/model/network request, response resampling, Codex/proxy/SSE/workload,
new dataset, full-DASSLE expansion unless already trivial from staged evidence,
generic Levenshtein distance, insertion/deletion/transposition, split/join,
normalization, frequency/context ranking, n-gram tie-break, u/v preference,
diacritic/suffix rule, morphology, lemma, BK-tree, SymSpell, learned ranker,
additional corpus, `--slovenize`, retry removal, second deployment, semantic
labeling, production integration, optimization, merge, release or deployment.

## Files and boundaries

Allowed repository paths: new one-substitution source/driver/test files; new
`research/configs/`, `research/reports/`, `research/results/` artifacts; additive
`research/README.md`, `research/EXPERIMENT-HISTORY.md`, registry/catalog/source
manifest and summary-table entries where current archive conventions require;
research CI only if needed; exact 007-h order/active/report paths. Existing
per-study config/report/result/source files remain byte-for-byte unchanged.

Private filled datasets, inputs, outputs, targets, replacements, Qwen responses,
reasoning and case-level source/reference text never enter Git, PR metadata or OAP
reports. Public machine evidence may contain aggregate counts and stable case/hash
identities only; it must pass the existing publication/privacy guard. Do not use
or leave `/tmp`; use the exact persistent native root above.

## Requirements

1. Before calculation, create a unique owned non-symlink private experiment root.
   Copy only the exact named DASSLE datasets, detector snapshots, saved M2 records,
   u/v audit and unigram index needed for this run. Verify every source SHA-256,
   size/regular-file status and copied byte identity. Preserve originals unchanged.
2. Verify 1,487 spelling and 1,486 preservation rows each have exactly one saved
   M2 record at the same index, matching ID and input SHA-256. Verify detector,
   English, decision, call, retry and failure fields are sufficient. Reproduce the
   exact frozen baseline outputs/metrics before enabling the new lane. Any mismatch
   stops the run with zero model calls and a truthful failure report.
3. Freeze `CONFIGURATION.json` before the first experimental record. Include all
   input hashes/counts, code/scorer/index identities, baseline configuration/result
   identities, exact rule text, Unicode/code-point semantics, English-first order,
   symmetric case rule, mechanical/exact-unigram gates, saved-fallback policy,
   failure/patch semantics, output schema, no-tuning statement and zero-live-call
   assertion. Do not mutate the freeze after execution begins.
4. Load the 141,162 exact unigram vocabulary from the verified read-only SQLite
   index once and bucket only by Python string length. Frequency/count is retained
   only as source evidence and is never used for candidate selection or ordering.
5. Apply the new stage only to an existing detector-selected target whose original
   candidate unigram state is exactly `UNAVAILABLE` and whose existing English
   policy did not suppress review. English-suppressed targets bypass the stage and
   preserve the original with zero review exactly as before.
6. Define candidates over `target.casefold()` and the complete exact-length bucket.
   A candidate qualifies only when the lookup form and candidate have identical
   Unicode code-point length, differ at exactly one position, both differing
   characters are alphabetic, and every other code point is identical. Explicitly
   reject identity, two differences, insertion, deletion, transposition,
   whitespace/multiword, split/join, hyphen/apostrophe insertion or removal, and
   manufactured Unicode normalization. Do not normalize either string.
7. Let C be the complete qualifying set. `|C|=0` falls through; `|C|>1` records
   ambiguity and falls through; only `|C|=1` is eligible. Never use unigram count,
   deterministic sort order, context, u/v or Qwen to break a tie.
8. For the unique candidate, apply the existing symmetric initial-case restoration
   to the original selected target, run the existing mechanical replacement gate,
   and independently confirm the resulting casefolded replacement remains one
   EXACT unigram. Only then produce an original-coordinate edit with source
   `MECHANICAL_ONE_SUBSTITUTION`. A gate failure falls through unchanged.
9. A mechanically accepted target must consume no first review, corrective retry,
   validator or confirmation. For every unresolved target, reuse the exact saved
   baseline first/retry decision and otherwise run the frozen pipeline unchanged:
   same detector, English policy, prompts logically represented by saved evidence,
   reasoning, unigram gate, one expression retry maximum, failure semantics and
   exact patching. Missing evidence is failure, never implicit KEEP or resampling.
10. Preserve document-level fail-closed semantics. If an unresolved saved fallback
    has an operational failure, apply the existing whole-result fallback exactly;
    do not retain a mechanical edit that the frozen combined-result failure rule
    would roll back. Separately record failures avoided when every previously
    failing target in a case is mechanically resolved.
11. Run exactly one paired calculation over all spelling and preservation records.
    Persist each case independently without overwrite and aggregate only after all
    records are present. Restart may skip hash-verified completed deterministic
    records but may not change configuration, recompute a different result,
    resample Qwen or create an alternate run identity.
12. Use the existing token-coordinate DASSLE scorer and first reproduce the frozen
    baseline metrics. Score new end-to-end output identically. Attribute each new
    edit as mechanical exact-reference, mechanical non-reference, fallback Qwen,
    or unchanged/unresolved. Non-reference is not automatically harmful.
13. Produce three spelling views using the existing u/v audit identities only:
    complete DASSLE spelling; all 75 identified initial-u/v cases after exact ID
    mapping; spelling with those cases removed. Do not discover or tune a new u/v
    category. Score corrected/reference preservation separately.
14. Report at least: stage-entering OOV targets; prior English suppressions; C=0,
    C=1 and C>1; unique candidates rejected by later mechanics/unigram; mechanical
    substitutions; exact-reference/non-reference mechanical edits; mechanical
    precision and spelling-gold recall with explicit denominators; fallback Qwen
    edits; unchanged/unresolved targets; end-to-end TP/FP/FN/precision/recall/F0.5;
    preservation changed cases/edits; baseline/projected first, retry and total
    calls; first/retry/total calls avoided specifically by mechanics; baseline/new
    operational failures and avoided/introduced counts; protected/outside-span
    differences; vocabulary-load and candidate-lookup runtime separately from
    reused model time. Actual experiment model/network calls must equal zero.
15. Validate baseline reference points, including spelling M2
    TP/FP/FN=`604/193/911`, precision `0.7578419071518193`, recall
    `0.39867986798679866`, first/retry/total calls=`2001/209/2210`, failures=40;
    preservation M2 first/retry/total=`920/92/1012`, failures=23 and 87 changed
    cases. If the same scorer/input does not reproduce these, stop before results.
16. Add focused offline tests proving same-length one difference; rejection of
    zero/two differences, insertion, deletion and transposition; unique acceptance;
    multiple-candidate fallback with no arbitrary selection; English suppression
    before mechanics; symmetric initial case; exact-unigram/mechanical recheck;
    mechanically accepted target skips all calls; unchanged frozen fallback;
    saved failure semantics; overlap/protected/outside-span integrity; deterministic
    persistence/resume and zero network/model boundary. Do not encode desired live
    Slovenian outputs.
17. Write a private full `REPORT.md`, `RESULTS.json`, per-case records, manifest and
    run status. Publish a concise data-free report, configuration and compressed
    machine result following archive conventions, plus additive navigation/registry
    entries. State all denominators, exact baseline identity, actual runtime and
    limitations. Preserve every earlier research artifact byte-for-byte.
18. Answer explicitly: resolvable fraction of entering OOV targets; accuracy and
    call savings; preservation effect; effect after removing u/v cases; and new
    end-to-end result after frozen fallback. Do not infer semantic harm for
    non-reference alternatives or generalize beyond DASSLE spelling.
19. Perform a strongest-reason-not-to-publish review: incomplete candidate set,
    accidental frequency/tie ranking, English-order violation, hidden model call,
    wrong baseline pairing, failure-semantics drift, data leakage, misclassified
    non-reference edit or prior-artifact mutation. Resolve material defects inside
    this single run without tuning/resampling; otherwise report PARTIAL/FAILED.
20. After the one experiment, publish the immutable 007-h report and STOP. Do not
    start another experiment, suffix, roadmap objective, production integration or
    follow-up rule without a new human instruction.

## Acceptance criteria

- Exact inputs and all 2,973 case/baseline pairings verify before calculation.
- Candidate semantics match the owner's code-point rule exhaustively and have no
  rank/tie heuristic.
- Mechanically accepted targets skip saved projected first/retry calls; unresolved
  targets reproduce the exact frozen fallback behavior; actual calls are zero.
- Complete spelling, u/v, spelling-minus-u/v and preservation metrics are produced
  with exact attribution/call/failure/runtime accounting.
- Protected and outside-approved-span differences are zero; prior archive bytes
  and private originals are unchanged; no raw data enters Git.
- Public config/report/machine evidence and private full evidence are hash-linked,
  navigable and reproducible. PR #8 remains open/unmerged.

## Verification

Use persistent native scratch only. Run focused one-substitution tests; complete
research tests; baseline replay equivalence; all 2,973 experimental cases; public
publication/privacy and private-overlap guards; Ruff/mypy over changed research
scope; full pytest; OAP unittest suite; native locked/offline baseline; transcript
index/revision; report history; exact accepted-base whitespace; accepted-runtime
governance; protected-source/prior-research diff; acquisition history; `git fsck
--full --no-reflogs`; exact implementation-head GitHub Research/OAP/report-history
checks and Application classification. Record PASSED/FAILED/PARTIAL separately.

## Local setup and constraints

Use existing locked dependencies and the verified read-only index. A simple
length-bucketed in-memory vocabulary is authorized; no persistent optimized index.
Copying named private files from the strategic sync workspace to the owned native
experiment root is allowed after hash verification. Do not acquire, redistribute,
package or commit DASSLE/Gigafida rows, archives, index bytes or model traces.
Bound CPU/memory and run sequentially; no GPU or HTTP client is needed.

## Documentation

Add one clearly labeled experimental report/config/result and minimal reproduction
instructions. Navigation may be updated additively, but existing experiment reports,
configs, results and interpretations remain unchanged. State that supplied-reference
metrics may penalize valid alternatives and that this experiment tests lexical
one-substitution restoration only.

## Git and report publication

SAME branch and PR #8. No merge. Commit/push code/tests/freeze/public results and
additive navigation before the OAP report. Preflight an external unpublished 007-h
draft. The final commit changes only
`oap/reports/007-h-evaluate-unique-one-letter-unigram-substitution.md`, has the
actual implementation/result head as sole parent, is pushed once and verified
remotely. Update PR body through GitHub metadata only. Send exact `OK` after durable
verification, then exit and stop.

## Decision classification

D0: exact owner-specified, reversible, offline experimental calculation over
already-authorized preserved evidence. There is no unresolved consequential choice,
live-service boundary, new annotation or release/deployment authority. The strongest
risk is false scientific confidence from reference-only scoring; explicit
attribution, no-tuning freeze, u/v ablation and conservative non-reference labels
contain it.

## Deferred human adjudication

- Decision: NONE
