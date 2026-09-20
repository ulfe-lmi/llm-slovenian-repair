# Research state — objective 007 (CURRENT, snapshot)

EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

This document is the single authoritative CURRENT research state for objective
007, published by the 007-o closure round (order 007-o, branch
`oap/007-concept-verification`, PR #8, AMEND_EXISTING_PR). It is a snapshot,
not history: it states what was investigated, what ran, what is trustworthy,
what failed or was superseded, what the strongest frozen method is, what is and
is not demonstrated, what remains worth testing, and what must not be tuned
further. Historical synthesis lives in `EXPERIMENT-HISTORY.md` (a 007-d-era
archival snapshot, superseded as current state) and in the immutable OAP
orders/reports. No claim in this document is an acceptance, merge, release,
deployment, or milestone claim.

Data-free and public-safe: no dataset rows, gold strings, prompts, response
bodies, credentials, or private native paths appear here. Private experiment
roots are cited by logical root name and SHA-256 of manifest files only. Every
quoted number is re-derived by `research/tests/test_research_state_consistency.py`
from the primary records named in section 1 (the embedded machine-readable
block at the end of this document must stay byte-consistent with those records).

## 1. Scope and exact reviewed Git identities

Snapshot date: 2026-09-17 (Europe/Ljubljana), at the 007-o reconciliation
point, before any 007-o mutation.

Reviewed Git identities:

- Remote `main` = `ee2d1b479719009ff1d07829478f241e3f395f7c` (equal to the
  runtime accepted reference at reconciliation).
- Branch `oap/007-concept-verification` head at review =
  `735c9830db95cbb02fc80446b6d28f62a56f10c9` ("Publish 007-n OAP report"),
  sole parent `b61f8e2e6b454a0969e5f2ac9009d4da87b8b215` (the 007-n
  implementation head). Report-only changed path verified.
- PR #8: OPEN, UNMERGED, base `main`, auto-merge disabled.
- Quarantined 007-n report (classified, never rewritten): publication commit
  `735c9830db95cbb02fc80446b6d28f62a56f10c9`; report Git blob
  `2b74413b54faf65de7659d3cf9957271d7721573`; report SHA-256
  `a0bf18f8b0e1218104f3fa4951be62758a3f4f5e88e7d776c4abe3d596b8372a`; 007-n
  order SHA-256 `0627cf26015dac47b17085e9f75b857f563379962a9590d5c8534e02e3f64f82`.
  Classification: INVALID_QUARANTINED by order 007-o's canonical
  `prior_report_recovery` block (forward-recovery protocol; precedent
  007-d/007-e). Root cause is formal, not scientific: the report's
  `checks[5].command` records an unfinalized angle-bracket placeholder token
  where the literal native temp parent directory must have been recorded, so
  machine validation rejects the whole report (REPORT_CHECK). The 007-n
  implementation (deterministic buffered terminal-SSE capture in the concept
  proxy and ZipInfo/stat_result typing repair) was independently accepted by
  strategy on 2026-09-17; the 007-n report's check claims are re-verified by
  this 007-o round and are NOT cited as accepted transcript evidence.

Primary records used to derive every number in this document (path, SHA-256):

- `research/registry/experiments.json` `b9abb66db55c06ce5920baa1a6c865f64b1f1b3472fcd1dda0dfb01a5a65f6ec` (24 entries)
- `research/registry/source-manifest.json` `932a69e1a831e13edf2d7697dba40924cbb6b8ddf34986fc08b5c7d9e4877aec`
- `research/registry/file-census.json` `408c9e5c512dcee21f32889ce1a25b6d1b77ab841cbb67b77566d51619ce19a8`; exact-entry ledger `research/registry/file-census.json.gz` `314e06f7a9f8f09201e45b23472d5f8b3c3256e0234af3ceb3b62d64e49100de`
- `research/registry/archive-catalog.json` `4ccc05547d69f52b1e95791a0bb3b3c81beebbf0db9876cb447511e215eaf49d`
- `research/results/strategic-official-summary.json` `59bc4c78f380762bf58c84f745a59b9ace1bc4b3154d28eb26c742c2474d949a` (official scorer summary; per-benchmark scorer-file SHAs inside)
- `research/results/007-h-unique-one-letter-unigram-substitution.json.gz` `49eb02c256de9bdb53be8fa6dc9b2535ae2fed0615869114b2ef1d47eba9dfa9`
- `research/results/007-i-contextual-validator.json.gz` `e981e3802ad0fc0db2a32262ba4dfada160ee880d3a86538bd241e8a57241fb5`
- `research/results/007-j-levenshtein-one-contextual-validator.json.gz` `f8643bcc01df7856218f3e66411c836469d9ecac91a1b6ffa6a9928044998c57`
- `research/results/007-m-rank-ambiguous-levenshtein-candidates.json.gz` `12a3913991c221566d5c0b3d0b16bca9e3e45a49af46c14f958e5526978bd134`
- `research/results/dassle.json.gz` `c45df127c3ddfa230faf35a5c9281359d0666d32df83d9b78ed117c67ef0d2f4`; `research/results/dassle-preservation.json.gz` `792df300426f0d321f3b7146275a8904ad45a5505e180517006550bcc2be836e`
- `research/results/study-evidence.json.gz` `a9c9827a2ac221f57dc1379612330d1147c1da3e7ec0219e9779c1718f5fa12c`
- `research/configs/007-m-rank-ambiguous-levenshtein-candidates.json` `41e1482a9ee100f5a3da6d31cd0646765271d874e2b7ef98593a50f5e7d2b5a0`
- Frozen data-free research reports: `research/reports/007-h-unique-one-letter-unigram-substitution.md` `86d41aa459883f8dbdee10c1286a8a317ead12275954873afaea2026c62f0252`; `research/reports/007-i-contextual-validator.md` `317bfc9e9721819da73bcbc0365ec63c3f5aab7f884f96400709a6f0e0a59af2`; `research/reports/007-j-levenshtein-one-contextual-validator.md` `9f0638684ee873f33d7be442b938d2c4d1fac693ea351d4fb2c05f160c661097`; `research/reports/007-m-rank-ambiguous-levenshtein-candidates.md` `89cb14a196e2f7ea1c66fdc429aa3cc375e8da1fd08066916bc9da31ecb9b634`
- `research/tables/experiment-summary.csv` `d7524c71d4c6c489ad235e872b5ba9b452876177bcfa465067034aef71e33a0d`
- OAP orders/reports 000-a through 007-n (immutable; the 007-o order carries
  the governance SHA block for the root law files).
- Governance: PLAN.md `d2aa1d98cc5177ac6093ab3aeb79903b192780910ef2d1712839b474fb5adbf0`; ARCHITECTURE.md `a16e0f87bdb21f6920aa63119cf5be148b6c8b68bf1337c44006d54b7261f7`; CRITICAL.md register = empty seed (zero entries, zero open gates).

Private root identities verified by SHA-256 of manifest/aggregate files only
(no content copied, no private path or text published):

- 007-m final root `007-m-rank-ambiguous-levenshtein-candidates-recovery.ec2962`: MANIFEST `3fb4aef33542e7fa3f357acb905b75f4d7e7551783f83a422b5d1ea6272c25f8`; CONFIGURATION `0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26`; LIVE-AGGREGATE `a30a2114563688adb18954237b97cfd4d6094a0e73566c2b29fd8f14c823ae7f`; HYBRID-AGGREGATE `cea2c167ad640fecb03408bdad98fb07c24dba2c9a4e014fe35bd512cd27c4be`; HYBRID-CASE-PROJECTIONS `3c779d96fd06237326902a5162c09f0588482491333d9f72be551eb9040f012c`; CASE-RESULTS-007J-REPLAY `8ff04afd4248ce4044a6f681121e29b9f11e44f99cb503b9d1492b2cdfb4ea08`; CASE-RESULTS-007M `0206a41f5f218c10aa5fc402968595e28915c971dc09597059dd4487879d4802`; FAILED-ROOT-LINKAGE `8cd98a661deed06880892e0839c7efb60c4a756aeb66ac7fc7bce98ab9790ecc`.
- 007-i root `007-i-contextual-validator.20260912`: CANDIDATE-MANIFEST `70544b1dec158f1e72cfaae8fb2547d9ba6ea22c3cd7934e0b7341bce8617854`.
- 007-j root `007-j-levenshtein-one-contextual-validator-recovery.54KmUx`: CANDIDATE-MANIFEST `acabcf1b33c38a949c80e81773b8ff3c355386daf768404791aaaed111f1df41`.

## 2. Executive scientific conclusion

The strongest current candidate is the frozen 007-m HYBRID method: the
full-campaign8 M2 targeted pipeline plus (007-h) deterministic unique
one-letter unigram substitution, (007-j) complete standard
Levenshtein-distance-one candidate generation, (007-m) a predeclared
lexicographic CPU top-1 ranking for ambiguous (C>1) targets, and the frozen
007-i/j contextual validator. On the frozen DASSLE same-sample population
(2,973 paired records; 1,515 spelling gold units), 007-m HYBRID reaches
TP/FP/FN 799/114/716 (precision 0.8751, recall 0.5274, F0.5 0.7732), a
conservative tradeoff against 007-j validated_fallback (822/154/693;
precision +0.0329, recall -0.0152, F0.5 +0.0147) with improved preservation
(78 vs 93 changed preservation cases; 83 vs 101 introduced edit units) and
zero new model calls in the final root (866 reused observations).

What this does NOT establish: no result here is held-out, confirmatory, or
target-distribution. Every 007-h/i/j/m number is same-sample exploratory,
reference-based (exact gold alignment or official ERRANT/GLEU scoring), and
produced on a non-target deployment regime (A100-FP8 `qwen3.8-27b`), while the
PLAN target deployment (strongly quantized Qwen3.8-27B on RTX 3090) was
unreachable at reconnaissance. No human semantic labels exist for the external
campaign; non-reference edits are overcorrection candidates and are NOT
labeled harmful. No product pipeline exists (detection/review/acceptance/
patching remain PLANNED), no ICA was launched, and no milestone, release, or
deployment authority is implied. The 007-m design is FROZEN FOR CONFIRMATION:
the researcher degrees of freedom on this one population are substantially
consumed (four successive same-sample mechanism changes), so the next research
step is structural (objective 008: prose/non-prose boundary qualification)
and then fresh untouched human-labelled target-distribution confirmation
(objective 009), with the two sequencing prohibitions in section 13.

## 3. Current frozen candidate method — exact 007-m identity

Method composition (pipeline seam, all experimental layer):

```text
original-coordinate protected spans (hand-written Markdown-sensitive protection logic)
  -> hyphen-view local-context detector with corpus evidence (OOV/lexical-absence oriented)
  -> original-target English eligibility/suppression
  -> candidate generation:
       (007-h) deterministic unique single-letter-substitution candidates attested
              in the exact unigram vocabulary (141,162 rows); English suppression
              precedes lookup; C>1 falls through in 007-h alone
       (007-j) complete standard unit-cost Levenshtein distance-one expansion
              (SUBSTITUTION/INSERTION/DELETION; transposition excluded) over the
              frozen vocabulary union
       (007-m) for C>1 targets: the predeclared lexicographic CPU top-1 is the only
              candidate the frozen validator sees; no runner-up is ever tried
  -> frozen contextual validator (one fresh bounded request per eligible target)
  -> conservative acceptance and exact original-coordinate patching
```

Frozen identity (private frozen configuration; public data-free projection at
`research/configs/007-m-rank-ambiguous-levenshtein-candidates.json`):

- Configuration SHA-256: `0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26`.
- Prompt SHA-256: `572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d`
  (owner-supplied frozen 007-i validator prompt, shared unchanged by 007-i/j/m).
- Ranking rule: predeclared lexicographic tuple, frozen before gold analysis —
  (1) trigram exactness flag, (2) trigram exact count, (3) exact bigram side
  count, (4) sum of exact bigram counts, (5) unigram exact count — over the
  frozen immediate left/right context; substitution is a hypothetical
  candidate insertion into that context only. Gold is structurally absent from
  ranking and score inputs and was used for post-ranking headroom analysis
  only. An exact top-score tie selects nothing (original retained, no
  validator call); evidence states EXACT/CENSORED/UNAVAILABLE are preserved —
  missing or censored evidence is never reported as zero.
- Validator protocol: strict binary-choice protocol (USE_CANDIDATE /
  KEEP_ORIGINAL / UNCERTAIN); extra text, malformed JSON, wrong
  model/effort, incomplete status, missing token accounting, timeout, or
  transport failure is a distinct conservative FAILURE. One terminal attempt
  per candidate; uncertain deliveries are never resampled.
- Limits: 300 s timeout; 2,000,000-byte response bound; no resampling;
  `new_call_budget` 0 in the final root; 8 workers, at most one in-flight call
  per worker, stable ordered position modulo worker count.
- Deployment class: A100-FP8, model `qwen3.8-27b`, Responses non-streaming
  (frozen 007-j profile SHA-256 `c79fd658db9c2006c0e542a12946962880e4ee3cec9dc57bc987b62d26c2dd60`;
  007-m profile SHA-256 `0c4aa4900733f37dc6da9b5fba4c5a772f83830b916938b8b89855917d1a1d4e`;
  endpoint identity private, omitted).
- Primary result definition: HYBRID projection — the preserved 007-j
  validated_fallback row per case with each C>1 target span replaced by the
  007-m decision outcome. The validated_only projection is a diagnostic that
  drops preserved 007-j fallback edits; it is not the primary result.
- Implementation heads: frozen implementation `537aa6a3ff03c60dd1b2c7f697c577940d52e88d`;
  recompute `f3fecab35c64ae202f6fed51d46e472b52270eb3`.

## 4. Full experiment ledger

Legend — evidence class: SYN = synthetic; BENCH = reference-backed benchmark;
LIVE = genuine target-model output; PRES = preservation input. Evidence role:
TUNE = tuning/development; SAME = same-sample exploratory; HELD = held-out;
CONF = confirmatory (ABSENT everywhere in this objective). Call accounting
distinguishes new / reused / zero-call projections. "Changed controls" are
control (correct) documents receiving at least one accepted edit; they are not
harm labels.

### 4.1 OAP rounds 007-a through 007-n (objective 007 rounds)

| Round | Result | Question | What it established | What failed / remained open |
| --- | --- | --- | --- | --- |
| 007-a (isolated end-to-end concept verification) | PARTIAL | Can the isolated completed-capture + detector + narrow-reviewer concept run offline and end to end? | Concept-verification prototype (proxy, buffered SSE capture, reviewer client, acceptance, patching, CLI) on branch; frozen dev/held-out detector evidence: dev 74 eligible / 6 known errors / 7 candidates (recall 1.00, candidate precision 0.714); held-out 145 eligible / 7 known / 10 candidates (recall 1.00, precision 0.700), frozen before held-out; 32-case frozen suite (7 labelled errors + 25 controls). | Workload capture 2/8 complete, 6 blocked (the RTX-3090 endpoint was TCP-closed at reconnaissance; the A100 was selected as the available target). Aggregate decision INCONCLUSIVE; human review sheet AWAITING_HUMAN_REVIEW. |
| 007-b (complete reviewer and Codex evaluation) | PARTIAL | Does the live narrow reviewer produce persisted, accepted local decisions end to end? | One allowed live reviewer sequence reached 10 selected candidates (10 bounded calls, A100) then hit a post-evaluation detector-only aggregation-key exception (instrument failure, not scientific); deterministic detector-only fallback: recall 1.00, precision 0.700. | Codex workload collection: 8/8 attempts exited 2 BEFORE proxy contact (unsupported builder flag; no model outputs). No populated human sheet. INCONCLUSIVE. |
| 007-c (preserve and publish the complete research trail) | PARTIAL | Can the private research trail be published data-free and reproducibly? | `research/` publication trail: registry, curated source closure, data-free reports/configs, compressed numeric projections, file census, source manifest. | Publication-guard/deployment-boundary corrections carried into later rounds; live boundaries unchanged. |
| 007-d (complete research publication and reproduction coverage) | PARTIAL | Is the published trail complete and executable offline? | Complete publication and offline reproduction coverage (replay, reproduce plan contract); the 007-d-era synthesis `EXPERIMENT-HISTORY.md`. | The 007-d report is machine-invalid and is quarantined as INVALID_QUARANTINED by order 007-e (forward recovery; precedent for the 007-n quarantine carried by this order). |
| 007-e (recover forward from an immutable invalid report) | COMPLETE | Can the protocol recover forward from the invalid 007-d report without rewriting it? | Canonical `prior_report_recovery` quarantine of the 007-d report (publication commit `88af5cefb76e5aaf727806ff589df93fa08f0861`); transcript coherence restored without touching any report byte. | None scientific; protocol-only. |
| 007-f (complete faithful research archive and CI-portable reproduction) | PARTIAL | Is the archive faithful and the reproduction CI-portable? | Executable archive correction: family-faithful historical drivers (no-English early variants, validator reuse, distinct retry wire/parser contracts, case rules, ten-run schedulers, worker/phase campaign routing, retry10 anchor, data-free DASSLE analyzer). Saved replay re-verified 16,375/16,375 M2 and M3 matches with zero model/network calls (archive reproduction evidence, not new science). | Residual environment/portability debt corrected in 007-k/007-l. |
| 007-g (close final GitHub portability and review surface) | PARTIAL | Is the branch remotely reviewable and portable? | Final GitHub portability and review-surface closure for the research trail. | Environment debt (fuse-mounted development environment) carried to 007-k. |
| 007-h (evaluate unique one-letter unigram substitution) | PARTIAL (round) / frozen valid result | Does deterministic unique one-letter unigram substitution change the frozen-campaign scores? | Frozen offline paired calculation (0 model calls) over the 2,973-pair population; score progression baseline 604/193/911 -> 704/345/811 (section 5); initial-u/v slice 28/11/47 -> 51/12/24; preservation 0/93/0 -> 0/234/0 (all non-reference); projected call savings 612. | Round result PARTIAL for environment/publication reasons; publication-only recovery ran with zero calls (incident recorded in the frozen report). Scientific metrics unchanged by the recovery. |
| 007-i (validate unique one-letter candidates contextually) | COMPLETE | Can one frozen contextual validator classify the 735 unique 007-h candidates without resampling? | 735 live validator calls (571 spelling + 164 preservation), 0 uncertain deliveries; validated_fallback 727/172/788 (section 5); reference-exact sensitivity 321/350 = 0.9171. | Post-live aggregation KeyError incident recovered with zero additional calls (request tree hash-identical before/after). Same-ID resume of the consumed order. |
| 007-j (evaluate standard Levenshtein-one with contextual validation) | COMPLETE | Does complete standard distance-one candidate generation improve coverage after the unchanged validator? | Candidate population 1,035 (826 spelling + 209 preservation); 542 observations reused byte-exact, 493 fresh calls; validated_fallback 822/154/693 (section 5); reference precision per operation class 0.926-0.939. | Initial-u/v slice regressed (42/7/33 vs 47/5/28); preservation changed cases +2, edit units +4. Documented prior zero-dispatch credential-boundary incident hashes preserved; same-ID resume. |
| 007-k (migrate development environment off fuse) | COMPLETE | Can the development environment run without the fuse mount? | Environment migration; deterministic baseline enabler. | None scientific. |
| 007-l (make environment ignore test hermetic) | COMPLETE | Is the environment-ignore test hermetic? | Hermetic environment handling for CI. | None scientific. |
| 007-m (rank ambiguous Levenshtein candidates) | COMPLETE | Does a predeclared CPU top-1 ranking of ambiguous (C>1) candidates improve the frozen method? | Frozen CPU ranking + one frozen validator call per C>1 target; 882 C>1 targets (651 spelling + 231 preservation), 4,372 candidate pairs; hybrid primary result 799/114/716 (section 5); headroom census (top-1 covers 60.54% of present gold). | Two failed instrument roots preserved (ffdf13: 188 calls; 090ea8: 678 calls); final zero-call root ec2962 adopted all 882 observations and recomputed the hybrid projections byte-for-byte. |
| 007-n (restore deterministic application baseline) | COMPLETE (implementation accepted; report quarantined) | Is the Application baseline deterministic and green? | Deterministic buffered terminal-SSE capture in the concept proxy and ZipInfo/stat_result typing repair; implementation independently accepted (diff review, focused concept suite 19/19, 25/25 consecutive iterations of the formerly flaky terminal-SSE test). | The 007-n REPORT is machine-invalid (unfinalized placeholder token in `checks[5].command`) and is classified INVALID_QUARANTINED by this order; its evidence claims are re-verified here. |

### 4.2 Registry roots (24 entries at the 007-o snapshot; 25 after the 008-b update; 27 after the 008-c update)

Population/denominator notes: the 32-case suite = 7 labelled errors + 25
controls; ten-run studies repeat the same 32 examples (320 instances measure
response variability, not 320 independent samples); the campaign runs 9 phases
(dassle 7,385; dassle-preservation 7,381; multigec-dev 50;
multigec-dev-preservation 50; multigec-test 49; multigec-train 10 [diagnostic
only]; slobench 1,232 [hidden references]; solar-canonical 109;
solar-canonical-preservation 109). Live deployment for all live roots:
A100 (campaign: A100-FP8) `qwen3.8-27b`.

| Root (kind, status) | Question / variable changed | Parent/baseline | Population and denominator | Evidence class / role | Call accounting (new/reused/zero-call) | Primary metrics (exact denominators) | Preservation | Supports / does NOT support / limitations / relationship / decision-relevance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 007-b-replacement (recovery, FAILED_BEFORE_PROXY_CONTACT) | Owner-authorized replacement of the failed 007-b instrument — did it reach the model boundary? | 007-b instrument | 32 controlled cases | LIVE / TUNE | 0 (failed before proxy contact) | No model outputs; held-out record: 10 controlled reviewer calls recorded historically (see timeout300), 4 valid structured decisions in the preserved record | n/a (no edits reached acceptance) | Supports: nothing scientific (instrument evidence). Does NOT support any reviewer conclusion. Limitation: failed before contact. Relationship: distinct historical execution, not a repaired original. Decision-relevance: none beyond the instrument history. |
| 007-b-timeout300 (recovery, COMPLETED_CONTROLLED_WITH_INVALID_TRACE_ASSOCIATION) | What evidence survived the controlled timeout-300 replacement? | 007-b instrument, 300 s ceiling | 32 controlled cases | LIVE / TUNE | 10 controlled calls (historical); workload 8 attempts / 2 completed | 10 valid reviewer decisions; 8 proposed replacements; 0 accepted edits; 0 exact-gold repairs; 7 missed known errors; 0 protected changes; median 21.44 s, p95 217.03 s | 0 protected changes | Supports: controlled-call timing and the instrument boundary. Does NOT support per-case semantic comparison (case/trace association invalid). Limitation: invalid trace association. Relationship: historical instrument evidence. Decision-relevance: none scientific. |
| nonthinking-mechanical (variant, COMPLETED) | Reasoning disabled, mechanical-only acceptance — what does the direct reviewer do at 32 cases? | Frozen direct reviewer, 32-case suite | 32 cases (7 errors + 25 controls) | LIVE / TUNE | 10 new calls | 4 applied edits; 2 exact-gold repairs; 1 changed control | 1 changed control | Supports: baseline direct-reviewer behavior at zero reasoning. Does NOT support a method choice alone. Limitation: 10 selected candidates of 32 cases. Relationship: parent of the low/high/xhigh comparisons. Decision-relevance: instrument calibration only. |
| low-thinking-mechanical (variant, COMPLETED) | Low reasoning, otherwise comparable. | Same parent | 32 cases | LIVE / TUNE | 10 new | 6 applied; 3 exact-gold; 1 changed control | 1 changed control | Supports: low-reasoning baseline used by all later variants. Does NOT support a quality claim. Limitation: same 10-candidate selection. Relationship: baseline for 007-h chain (campaign M2 behavior). Decision-relevance: baseline identity. |
| high-thinking-mechanical (variant, STOPPED) | High reasoning. | Same parent | 32 cases | LIVE / TUNE | 1 call, then stopped | Stopped run; do not substitute the completed xhigh result | n/a | Supports: nothing (negative operational record). Does NOT support any reasoning-level comparison. Limitation: stopped. Relationship: negative entry preserved, not hidden. Decision-relevance: none. |
| xhigh-thinking-mechanical (variant, COMPLETED) | xhigh reasoning. | Same parent | 32 cases | LIVE / TUNE | 10 new | 8 applied; 4 exact-gold; 1 changed control | 1 changed control | Supports: upper-bound reasoning behavior on the small suite. Does NOT support deployment of xhigh (cost/latency uncharacterized for product). Limitation: 32-case. Relationship: ablation point. Decision-relevance: none beyond ablation. |
| low-plus-validator (variant, COMPLETED) | Frozen low first-pass plus validation of already-sampled proposals. | low-thinking-mechanical | 32 cases | LIVE / TUNE | 6 new (10 first-pass reused) | 6 applied; 3 exact-gold | 0 changed controls observed in accepted set | Supports: validator-over-sampled-proposals pattern. Does NOT support fresh-observation validation (that is 007-i). Limitation: reused proposals. Relationship: precursor of 007-i protocol. Decision-relevance: design input only. |
| low-unigram-retry (variant, COMPLETED) | Unigram post-check + one contextual corrective retry. | low-thinking-mechanical | 32 cases | LIVE / TUNE | 2 new (10 first-pass reused) | 4 applied; 3 exact-gold; 0 changed controls | 0 changed controls | Supports: retry-limit pattern. Does NOT support a product retry policy. Limitation: 32-case. Relationship: precursor of retry ablation in campaign8. Decision-relevance: design input only. |
| low-word-only-retry (variant, COMPLETED_WITH_WHITESPACE_ONLY_CONTINUATION) | Context-free word-only retry. | low-thinking-mechanical | 32 cases | LIVE / TUNE | 2 new; continuation from saved response (not fresh resampling) | 4 applied; 3 exact-gold | whitespace-only continuation | Supports: saved-response continuation semantics. Does NOT support fresh resampling (never done). Limitation: stopped-then-continued distinction preserved. Relationship: protocol input. Decision-relevance: none. |
| full-hyphen-space-low (variant, COMPLETED) | ASCII hyphen becomes space in the detector view only. | low-thinking-mechanical | 32 cases; 9 candidates | LIVE / TUNE | 10 new | 5 applied; 3 exact-gold; 0 changed controls | 0 changed controls | Supports: hyphen-view detector behavior. Does NOT support production normalization (detector view only, no original mutation). Limitation: 32-case. Relationship: feeds the campaign detector design. Decision-relevance: design input. |
| full-hyphen-case-low (variant, COMPLETED) | First one-way initial-case preservation stage. | full-hyphen-space-low | 32 cases; 9 candidates | LIVE / TUNE | 11 new | 2 applied; 2 exact-gold; 0 observed applied case-adjustment events | 0 changed controls | Supports: one-way case stage. Does NOT support the symmetric rule (that is the ten-run study). Limitation: 32-case. Relationship: parent of the symmetric case rule. Decision-relevance: design input. |
| ten-run-initial-case-low (study, COMPLETED_WITH_STOPPED_TRIALS) | Symmetric initial-case rule over 10 trials. | full-hyphen-case-low | Same 32 examples x10 (320 instances) | LIVE / TUNE | 97 calls (87 first + 10 corrective); 8 trials complete, 2 stopped | Trial-by-trial metrics in the safe catalog; stopped trials retained separately | n/a | Supports: response-variability measurement of the symmetric rule. Does NOT support 320 independent samples. Limitation: 2 stopped trials. Relationship: feeds campaign case policy. Decision-relevance: design input. |
| ten-run-expression-retry-low (study, COMPLETED_WITH_STOPPED_TRIALS) | Context-free 1-4 word expression retry over 10 trials. | low-unigram-retry | Same 32 examples x10 | LIVE / TUNE | 103 calls (90 + 13); 9 complete, 1 stopped | Trial-by-trial metrics in the safe catalog | n/a | Supports: expression-retry behavior and its cost. Does NOT support a product retry policy. Limitation: 1 stopped trial. Relationship: design input. Decision-relevance: none. |
| ten-run-english-preserve-low (study, COMPLETED_ALL_TEN_TRIALS) | English-attestation suppression over 10 trials. | low-thinking-mechanical | Same 32 examples x10 | LIVE / TUNE | 95 calls (80 + 15); 10/10 complete | Deterministic policy suppression (not a model KEEP); campaign later: 83/1,905 candidates suppressed on SloBench | n/a | Supports: the deterministic English-suppression policy. Does NOT support linguistic benefit of suppression itself. Limitation: policy, not model behavior. Relationship: campaign M2/M3 component. Decision-relevance: design input. |
| large-evaluation-capped (campaign, INFERENCE_STARTED_NOT_COMPLETED) | Capped external campaign preparation. | Pre-campaign pipeline | Capped external set | LIVE / TUNE | Inference started, interrupted | Incomplete; not merely unexecuted | n/a | Supports: operational history of the capped attempt. Does NOT support any measurement. Limitation: incomplete. Relationship: superseded by uncapped then campaign8. Decision-relevance: none. |
| large-evaluation-uncapped (campaign, PAUSED_BY_HUMAN_RELEVANCE_CHANGE) | Owner-directed uncapped continuation after early results. | large-evaluation-capped | Uncapped external set | LIVE / TUNE | Paused by owner relevance change | No final aggregate (owner intervention, recorded, not researcher tuning) | n/a | Supports: the ownership of the relevance change. Does NOT support a method comparison. Limitation: paused. Relationship: superseded by campaign8. Decision-relevance: records one consumed human relevance change. |
| dassle-spelling-preparation (preparation, COMPLETE_LOCAL_EVIDENCE_WITH_RECORDED_INCIDENTS) | DASSLE spelling stage: error + preservation inputs through the frozen pipeline. | Frozen campaign pipeline | 1,487 spelling cases + 1,486 preservation cases; 11,892 method records | LIVE / TUNE (preparation) | 6,195 unique calls (later INHERITED by full-campaign8; not double-counted as fresh evidence) | Worker/recovery incidents preserved | 1,486 preservation inputs | Supports: the frozen 2,973-pair population that 007-h/i/j/m consume. Does NOT support a method conclusion. Limitation: preparation, with recorded incidents. Relationship: baseline for 007-h chain. Decision-relevance: population identity. |
| dassle-uv-audit (audit, COMPLETE_EXHAUSTIVE_MECHANICAL_AUDIT) | How many of the 8,623 gold units are u/v-related? | DASSLE gold (8,623 units) | 1,487 spelling rows | BENCH / SAME (mechanical audit, zero calls) | 0 new calls | 75 strict first-letter substitutions + 51 standalone-word + 54 noninitial = 180 u/v-related units, all in the supplied spelling category; 75/1,487 = 5.04%; incl. standalone 126/1,487 = 8.47% | n/a | Supports: the u/v slice size that motivated 007-h. Does NOT support any fix (audit only). Limitation: early-row ordering bias explained in the archive. Relationship: motivation record for 007-h. Decision-relevance: explains slice findings. |
| full-campaign8 (campaign, COMPLETED_LOCAL_CAMPAIGN_REMOTE_SCORING_PENDING) | Final nine-phase eight-worker A100 campaign: M0/M1/M2/M3 across reference-backed datasets. | Frozen pipeline (M0 original, M1 direct proofreading, M2 targeted, M3 targeted no-retry) | 16,375 cases; 65,500 method records; 9 phases (counts in section 4.2 note) | LIVE + BENCH + PRES / SAME | 39,184 distinct calls (31,916 new + 7,268 inherited); 1,419 verified checkpoints; 8 workers; 9 completed phases | Official scorer per dataset in section 5.1; custom end-to-end alignment in section 5.3; operational failures end-to-end: M1 2, M2 107, M3 103 (of 7,385 DASSLE) | Preservation: M1 2,489 introduced units (0/7,381 unchanged examples); M2 340 units (6,989/7,316); M3 252 units (7,076/7,320); retry ablation DASSLE +7 TP/+132 FP/581 calls, preservation +0 TP/+88 FP/395 calls | Supports: the complete same-sample reference-based picture (methods, cost, preservation, retry). Does NOT support: target-distribution benefit, human harm measurement, or transfer to the PLAN deployment (A100-FP8 regime only). Limitation: SloBench (1,232) and MultiGEC-test (49) have no distributed/hidden references — quality UNKNOWN (remote scoring access-blocked); deployment B excluded by owner override. Relationship: baseline consumed by 007-h chain. Decision-relevance: the current best same-sample evidence. |
| prijigrala-retry10 (variant, COMPLETE) | One-target retry-limit-ten contextual case. | Frozen pipeline, one sentence/target | 1 case | LIVE / TUNE (single case) | 4 calls (1 first + 3 corrective) | ACCEPTED an exact-unigram-attested proposal that did NOT match the known intended correction (HTTP 72.86 s) | n/a | Supports: dictionary-membership != contextual suitability. Does NOT support a retry policy (single case, not a benchmark). Limitation: one case. Relationship: motivates the validator's contextual strictness. Decision-relevance: design input. |
| 007-h-unique-one-letter-unigram-substitution (experiment, COMPLETE) | Sole mechanism: deterministic unique one-letter unigram substitution with frozen fallback. | Frozen campaign M2 baseline (baseline config `4c748b8e9711148c008d4157edef209a21531a2412745f230069215d3ddc5d29`, baseline results `3a75c4dac3d77db7c865d363197efc368898c53b8b092abbc14451052354700f`) | 2,973 paired records (1,487 spelling / 1,486 preservation); 1,515 spelling gold units (75 initial-u/v; 1,440 without) | BENCH / SAME | 0 model calls (offline paired calculation; projected call savings 612 vs baseline) | C buckets (spelling all): entering OOV 2,001 / English suppressed 7; C=0/C=1/C>1 = 1,011/571/419; unique accepted 571, applied 557, rolled back 14; score 604/193/911 -> 704/345/811 (section 5); initial-u/v 28/11/47 -> 51/12/24; lookup comparisons 31,084,860 | 0/93/0 -> 0/234/0; 197 changed cases / 234 introduced edits (all non-reference); protected/outside 0/0 | Supports: recall gain +100 TP and the u/v slice gain (+23 TP) at a precision and preservation cost. Does NOT support: overall superiority (F0.5 down 0.6421 -> 0.6164), any fresh-evidence claim. Limitation: same-sample, reference-based, offline projection. Relationship: parent of 007-i candidate set. Decision-relevance: consumed by the frozen 007-m method. |
| 007-i-contextual-validator (experiment, COMPLETE) | One frozen contextual validator over the 735 unique 007-h candidates, no resampling. | 007-h unique candidates; baseline M2 behavior | 735 candidates (571 spelling + 164 preservation); denominators as 007-h | LIVE + BENCH / SAME | 735 new validator calls; 0 uncertain deliveries; 0 resamples; net calls 2,419 vs baseline 2,210 (fallback view) | Spelling all: decisions USE/KEEP/UNCERTAIN/FAILURE 337/199/5/30; validated_fallback 727/172/788 (P 0.8087, R 0.4799, F0.5 0.7112); reference-exact sensitivity 321/350 = 0.9171; initial-u/v 47/5/28 (F0.5 0.8304) | Preservation FP 93 -> 97; changed cases 91/97 (fallback); protected/outside 0/0 | Supports: validation sharply cuts FP (+57 TP vs 007-h at -18... precisely: 007-h 704/345/811 -> 007-i 727/172/788). Does NOT support: held-out or target-distribution behavior. Limitation: same-sample; 46 protocol failures recorded. Relationship: parent protocol of 007-j/m. Decision-relevance: frozen validator in the 007-m method. |
| 007-j-levenshtein-one-contextual-validator (experiment, COMPLETE) | Sole variable: complete standard unit-cost Levenshtein distance-one candidate generation over the frozen 007-i vocabulary. | 007-i BEST (validated+fallback); 542 observations reused byte-exact | 1,035 candidates (826 spelling + 209 preservation); denominators as 007-h | LIVE + BENCH / SAME | 493 fresh calls + 542 reused; 0 uncertain deliveries; latency n=493 mean 10.71780110838896 s, p95 24.88524721498834 s, max 58.17827162001049 s | Spelling all validated_fallback 822/154/693 (P 0.8422, R 0.5426, F0.5 0.7584), delta vs 007-i +95/-18/-95; operations SUBSTITUTION 542 / INSERTION 172 / DELETION 321 (unique); reference precision per class 0.9260/0.9291/0.9392 | Preservation changed cases 91 -> 93, edit units 97 -> 101; protected/outside 0/0 | Supports: the strongest recall/F0.5 point before 007-m. Does NOT support: u/v slice (regressed 47/5/28 -> 42/7/33); fresh-evidence claim. Limitation: same-sample. Relationship: parent of 007-m. Decision-relevance: frozen base of the 007-m hybrid. |
| 007-m-rank-ambiguous-levenshtein-candidates (experiment, COMPLETE) | Sole variable: predeclared lexicographic CPU top-1 selection for C>1 targets; one frozen validator call per target; no runner-up. | 007-j validated_fallback; 1,035 C=1 observations copied byte-exact | 882 C>1 targets (651 spelling + 231 preservation); 4,372 candidate pairs; set size min 2 / median 3 / p90 9 / p95 14 / p99 29 / max 50 | LIVE + BENCH / SAME | 866 attempted + 16 uncertain-delivery (never resampled); 0 NEW calls in the final root (882 + 1,035 observations adopted/reused); inherited latency n=866 mean 16.193259791632915 s, p95 33.48273886600509 s, max 184.56243890197948 s; tokens input/output/reasoning 173,422/393,685/388,375 (inherited), 0 new | Hybrid: spelling all 799/114/716 (P 0.8751, R 0.5274, F0.5 0.7732) vs 007-j 822/154/693 (delta -23/-40/+23); initial-u/v 49/7/26 vs 42/7/33; without-initial-u/v 750/107/690 vs 780/147/660; decisions USE/KEEP/UNCERTAIN/FAILURE 270/509/16/87; accepted exact/non-reference 219/51; headroom top1 247/349/376/399/408 of 408 present (60.54%/85.54%/92.16%/97.79%/100%); oracle recall ceiling 0.5426 -> 0.8119 | Changed cases 93 -> 78; introduced edit units 101 -> 83; protected/outside/expected-output failures 0/0/0 | Supports: a conservative precision/F0.5/preservation tradeoff with zero fresh calls. Does NOT support: an unqualified win (recall -1.52 points); fresh-evidence or human-acceptance claims. Limitation: same-sample; selection of the experiment itself was same-sample-driven (though the tuple was frozen before gold analysis). Relationship: the frozen candidate method. Decision-relevance: FROZEN FOR CONFIRMATION (sections 12-14). |
| levenshtein-lookup-diagnostic (diagnostic, NOT_A_BENCHMARK) | Read-only lookup: does the vocabulary contain the unique distance-1 candidate for one supplied correction? | Frozen vocabulary (141,162 rows) | 1 lookup over 71,650 length-filtered keys | BENCH / SAME (diagnostic) | 0 calls (2.597 s lookup; unigram count 4,184) | Found the unique distance-1 candidate matching the supplied correction | n/a | Supports: feasibility of distance-1 lookup (motivated 007-j). Does NOT support any measurement (explicitly not a benchmark). Limitation: inline execution had no preserved standalone hash; later notes must not be misrepresented as the original frozen script. Relationship: motivation record. Decision-relevance: none. |

### 4.3 Corrective/recovery rounds that affect interpretation

- 007-b replacement and 007-b timeout300 (section 4.2 rows): historical
  instrument evidence only; invalid trace association means no per-case
  semantic comparison from the workload.
- 007-d report quarantine: the 007-d report is machine-invalid and
  INVALID_QUARANTINED by order 007-e (publication commit
  `88af5cefb76e5aaf727806ff589df93fa08f0861`); the quarantine remains
  preserved in the transcript at this round's head.
- 007-h publication recovery: the frozen scientific aggregation was valid;
  the publication projection failed afterward. Recovery exposed only the
  omitted `introduced_edits` field derived with the existing scorer from
  frozen source/output pairs; all other metrics are a deep copy of the frozen
  private aggregate; no linguistic metric or case changed; zero model/network
  calls. Incident identities: publication projection
  `cb382883f4b9e179e6149e49a7df7fdb1f494b91cd91670dd31942a6895fb01c`;
  invalid publication-render `fc4aebc9e179b3f82e5473da0619029a3d58717733128a5f2bbb32619c134650`
  (uncommitted attempt, excluded). Calculation/aggregation/implementation
  heads: `939ae8b1482f3b8b5cefba5b0e16d1fde580346d` /
  `5a1808b5227ef3b277ccd1a070b514840bdb310b` /
  `65ba55ef3ff84bda4202190e589d45721409287b`.
- 007-i aggregation recovery: deterministic KeyError on the derived
  `valid_response_count` field inside `make_views`; 735/735 observation and
  dispatch records already persisted; aggregation re-run with 0 additional
  model/network calls; request tree hash-identical before/after (2,940 files,
  4,651,774 bytes, manifest SHA-256
  `d46b47754e2ba158ea099bfe556a84164e534610233426819d9114a455aea945`);
  incident identity `598b707790e303811faef0ccf15898686225947d19fce44352bde05f75984f39`.
- 007-j same-ID resume: after the documented zero-dispatch credential-boundary
  incident (preserved hashes: configuration
  `2411d31cb12fd4a247d63632658b30576ffa644f82b8d55c8ed6832d90d63982`,
  candidate manifest `acabcf1b33c38a949c80e81773b8ff3c355386daf768404791aaaed111f1df41`,
  results `398a38eff253f3080d45f512a60b08191afa3240341d67caca1917e4138eb318`,
  manifest `6f2d23d9950ea0da836f557e4779c79b7e06fb107fcf65650514df50009c3567`,
  report `98aee169606dd75fd9069a88c7575f5b263545a9a008112d`), the round
  resumed on the same ID/branch/PR and reused the frozen 007-i observations
  byte-exact (542) with 493 fresh calls.
- 007-m failed instrument roots and final zero-call root:
  `007-m-rank-ambiguous-levenshtein-candidates-recovery.ffdf13` (implementation
  head `88ca4dfe19740aa21156457d42966661f67902ea`): 188 actual experiment
  calls; 8 request-only interruptions finalized as 8 uncertain observations;
  the harness rejected the canonical interrupted-finalization file set, so the
  root could not complete its own live resume; preserved unchanged as
  failed-instrument evidence.
  `007-m-rank-ambiguous-levenshtein-candidates-recovery.090ea8` (implementation
  head `92bee3a214aa50ef3921f54488545a57d9a95000`): 678 fresh calls (196
  observations reused from ffdf13); the fully observed root could not
  aggregate because the replay identity gate compared in-memory tuple-typed
  attribution fields against JSON-normalized persisted rows; preserved
  unchanged. Superseded census diagnostic root:
  `007-m-rank-ambiguous-levenshtein-candidates-recovery.e6ca66`; corrected
  census root `007-m-rank-ambiguous-levenshtein-candidates-recovery.97f59c`.
  Actual experiment calls across preserved roots: 188 + 678 = 866; cross-root
  reuse 196 (ffdf13 -> 090ea8) and 882 (090ea8 -> final) are distinct from
  actual calls. Final root
  `007-m-rank-ambiguous-levenshtein-candidates-recovery.ec2962`: adopted all
  882 C>1 and all 1,035 C=1 observations with ZERO new calls (budget 0; no
  resampling; all eight workers dispatched 0); hybrid recompute recomputed
  both case-result projections and matched them byte-for-byte before writing
  the hybrid aggregate (case_results_verified=true, new_calls=0).
- 007-n accepted implementation with quarantined report: the implementation
  (implementation head `b61f8e2e6b454a0969e5f2ac9009d4da87b8b215`) is
  accepted; the report (publication commit `735c9830db95cbb02fc80446b6d28f62a56f10c9`)
  is INVALID_QUARANTINED by this order's `prior_report_recovery` block. Its
  check claims (focused concept suite, development baseline, research suite,
  OAP suite, transcript, governance, report history, whitespace, Git
  integrity) are re-verified by this 007-o round; they are not cited as
  accepted transcript evidence.

No negative experiment is hidden: high-thinking-mechanical STOPPED,
large-evaluation-capped incomplete, large-evaluation-uncapped paused, 007-h
overall F0.5 loss, 007-i preservation FP rise, 007-j u/v regression, 007-m
recall loss, the retry ablation's adverse tradeoff, and the two 007-m failed
instrument roots are all recorded distinctly above.

## 5. Key metric progression

### 5.1 Official scorer (ERRANT + GLEU), from `research/results/strategic-official-summary.json`

Strategically extracted from the campaign's official `SCORES.json` files
(0 new model calls; metrics are NOT the custom alignment). Scorer-file
SHA-256s: multigec-train `d313140633ceffcb7ba4cb468aaffc59d84fc2c82e2cc24bb965266c8de74273`;
multigec-dev `479d3a79b1664cda5f546d419d30e819b0e506e9feba3ad6a4cf06d4fd19ba11`;
solar-canonical `b3f6ad1f621b9ac0f79138024652b8d3192c16ade22ccb615a34bb06e8d30fa8`;
dassle `e944ad5d5e34149ef7261fb2117ffc92bbc2e366b5a054a519dce809587906ad`.

M0 = original (no edits); M1 = direct Qwen proofreading; M2 = targeted full
method; M3 = targeted no-retry. ERRANT precision/recall/F0.5 with
tp/fp/fn; GLEU alongside.

| Dataset (examples) | Method | F0.5 | precision | recall | tp/fp/fn | GLEU |
| --- | --- | --- | --- | --- | --- | --- |
| multigec-train (10) | M0 | 0.0 | 1.0 | 0.0 | 0/0/792 | 29.7105 |
| multigec-train (10) | M1 | 0.4432 | 0.5021 | 0.3018 | 239/237/553 | 55.8223 |
| multigec-train (10) | M2 | 0.0957 | 0.4865 | 0.0227 | 18/19/774 | 31.4699 |
| multigec-train (10) | M3 | 0.0974 | 0.5455 | 0.0227 | 18/15/774 | 31.5333 |
| multigec-dev (50) | M0 | 0.0 | 1.0 | 0.0 | 0/0/3573 | 49.8263 |
| multigec-dev (50) | M1 | 0.4560 | 0.5337 | 0.2883 | 1030/900/2543 | 64.9078 |
| multigec-dev (50) | M2 | 0.0963 | 0.5127 | 0.0227 | 81/77/3492 | 50.9906 |
| multigec-dev (50) | M3 | 0.0967 | 0.5674 | 0.0224 | 80/61/3493 | 50.9331 |
| solar-canonical (109) | M0 | 0.0 | 1.0 | 0.0 | 0/0/7951 | 49.0726 |
| solar-canonical (109) | M1 | 0.4484 | 0.5312 | 0.2762 | 2196/1938/5755 | 64.1473 |
| solar-canonical (109) | M2 | 0.0849 | 0.4081 | 0.0204 | 162/235/7789 | 50.3534 |
| solar-canonical (109) | M3 | 0.0845 | 0.4527 | 0.0199 | 158/191/7793 | 50.3398 |
| dassle (7381) | M0 | 0.0 | 1.0 | 0.0 | 0/0/8578 | 67.9624 |
| dassle (7381) | M1 | 0.3883 | 0.438 | 0.2671 | 2291/2940/6287 | 74.7351 |
| dassle (7381) | M2 | 0.3003 | 0.618 | 0.0983 | 843/521/7735 | 71.4808 |
| dassle (7381) | M3 | 0.3103 | 0.6836 | 0.0975 | 836/387/7742 | 71.4226 |

Reading: direct proofreading (M1) scores best on reference-based F0.5 but is
highly invasive (e.g., DASSLE 2,940 FP); the targeted method (M2/M3) is far
more precise and far less invasive at a fraction of recall — the detector is
OOV/lexical-absence oriented, so grammatical/punctuation/multi-token
reference changes never reach review. Official DASSLE F0.5 is lower WITH
retry than without at M2-vs-M3 on the official scorer (0.3003 < 0.3103), and
the custom retry ablation is adverse (section 5.3).

### 5.2 Custom token-coordinate alignment — frozen DASSLE pairs (007-h chain)

Custom deterministic token-span alignment against supplied references (NOT
the official scorer). Population: 2,973 paired records; spelling gold units
1,515 (initial-u/v 75; without-initial-u/v 1,440); 1,486 preservation
reference inputs. View: `dassle-spelling/all`. Baseline = frozen campaign M2
behavior. 007-h = unrestricted unique one-letter unigram substitution with
frozen fallback. 007-i/007-j = validated_fallback (validator-accepted plus
frozen mechanical fallback). 007-m = HYBRID primary projection.

| Stage | TP | FP | FN | precision | recall | F0.5 |
| --- | --- | --- | --- | --- | --- | --- |
| baseline (frozen M2) | 604 | 193 | 911 | 0.7578419071518193 | 0.39867986798679866 | 0.6421433127790771 |
| 007-h unrestricted | 704 | 345 | 811 | 0.6711153479504289 | 0.4646864686468647 | 0.6163544037821747 |
| 007-i validated_fallback | 727 | 172 | 788 | 0.8086763070077865 | 0.47986798679867987 | 0.7112111132850714 |
| 007-j validated_fallback | 822 | 154 | 693 | 0.8422131147540983 | 0.5425742574257426 | 0.7584425170695701 |
| 007-m HYBRID | 799 | 114 | 716 | 0.8751369112814896 | 0.5273927392739274 | 0.7731759241339268 |

Exact 007-m-vs-007-j deltas: TP/FP/FN -23/-40/+23; precision
+0.0329237965273913; recall -0.015181518151815232; F0.5 +0.014733407064356663.
Slice deltas (007-m vs 007-j, TP/FP/FN): initial-u/v 49/7/26 vs 42/7/33
(+7 TP, FP flat); without-initial-u/v 750/107/690 vs 780/147/660 (-30 TP,
-40 FP).

Preservation/call/latency deltas (007-m HYBRID vs 007-j validated_fallback):

- Preservation changed cases: 78 vs 93 (delta -15); introduced edit units:
  83 vs 101 (delta -18); integrity: protected/outside-span/
  expected-output failures 0/0/0.
- Calls: 0 new calls in the final 007-m root (866 reused C>1 + 1,035 reused
  C=1 observations) vs 493 new validator calls in 007-j (542 reused).
- Latency (validator calls): 007-m inherited n=866, mean 16.193259791632915 s,
  p95 33.48273886600509 s, max 184.56243890197948 s vs 007-j fresh n=493,
  mean 10.71780110838896 s, p95 24.88524721498834 s, max 58.17827162001049 s
  (inherited cost is reported, not re-paid, in the final 007-m root).

### 5.3 Campaign-level custom alignment and retry ablation (full-campaign8, DASSLE)

End-to-end view of `research/results/dassle.json.gz` (7,385 cases; 8,623 gold
units):

| Method | TP | FP | FN | precision | recall | F0.5 | introduced edits | operational failures |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | 2212 | 2766 | 6411 | 0.44435516271595016 | 0.25652325176852603 | 0.3875941825827931 | 4981 | 2 |
| M2 | 834 | 525 | 7789 | 0.6136865342163356 | 0.09671807955467934 | 0.2966071555587168 | 1360 | 107 |
| M3 | 827 | 393 | 7796 | 0.6778688524590164 | 0.09590629711237389 | 0.3062282455750574 | 1221 | 103 |

Preservation (`research/results/dassle-preservation.json.gz`): introduced
edit units M1 2,489 (0/7,381 preservation examples unchanged), M2 340
(6,989/7,316), M3 252 (7,076/7,320). Retry ablation totals: DASSLE
tp_delta +7, fp_delta +132, 581 calls, 5 exact regressions; preservation
tp_delta +0, fp_delta +88, 395 calls, 83 exact regressions — the corrective
retry is an adverse tradeoff and M3 (no retry) is retained as the frozen
baseline behavior.

Non-reference edits in every view above are overcorrection candidates, never
human-labeled harmful edits; exact-gold alignment is reference agreement, not
linguistic correctness.

## 6. Evidence hierarchy

Explicitly separated layers (LR-014: software correctness, serving
compatibility, linguistic benefit, and deployment/release authority are
distinct evidence):

1. Merged state on `main` (ee2d1b4): bootstrap infrastructure and objectives
   000-002 only. Objectives 003-007 are NOT merged.
2. Unmerged application development (PR #8): objectives 003-006 product seams
   (typed contracts/policy, source manifests, unigram importer + cache), the
   concept-verification prototype, and all 007 research infrastructure.
3. Experimental/research implementation: the `research/` curated data-free
   trail plus private roots; exclusive of the product library
   (`src/llm_slovenian_repair/`).
4. Historical/replay evidence: saved campaign replay re-verified 16,375/16,375
   M2 and M3 matches with zero model/network calls (007-f archive
   reproduction; not new science).
5. Live model evidence: 007-b timeout300 (10 calls, invalid trace
   association), the mechanical/validator/retry small studies, full-campaign8
   (39,184 calls, A100-FP8), 007-i (735 calls), 007-j (493 fresh), 007-m
   (866 actual across the failed roots; zero in the final root).
6. Reference-based linguistic scoring: official scorer (ERRANT/GLEU,
   strategic-official-summary.json with scorer-file SHAs) and custom
   token-coordinate alignment (8,623 DASSLE gold units campaign-wide; 1,515
   spelling-category units in the frozen 007-h chain; denominators kept
   separate).
7. Human semantic evidence: ABSENT for the external campaign. Small-study
   case assessments were strategic-model judgments, never human ground truth;
   the 007-a review sheet remains AWAITING_HUMAN_REVIEW. No human harm labels
   exist; non-reference edits are not labeled harmful.
8. Operational evidence: CI, OAP checks (transcript, governance, report
   history with exactly two frozen historical incidents, whitespace),
   publication guard, file census (225,757-entry ledger), and this round's
   private-root identity verification.
9. Milestone/ICA evidence: ABSENT. No ICA launched; no milestone label
   assigned. Release/deployment authority: ABSENT.

## 7. Claims audit

Verified against primary records at the 007-o reconciliation point:

- PR #8 description (007-m round): scientific numbers VERIFIED against the
  007-m research report, config, and results projection; "same-sample
  exploratory" VERIFIED. The Application-baseline wording ("mypy stage fails
  only on the inherited 11 errors; local flake passes in isolation") was STALE
  relative to the then-current head; it is corrected by this round (007-n
  repaired the baseline; section 15 carries the truthful current status).
- STATUS.md: the blanket "linguistic evaluation NOT RUN" was STALE —
  reference-based benchmark linguistic evaluation HAS run (full-campaign8 and
  007-h/i/j/m on A100-FP8, same-sample exploratory); what has NOT run is the
  human-labelled target-distribution evaluation required by PLAN section 14.2.
  Corrected in this round with the layered wording; the 001-006 history
  paragraphs are preserved verbatim.
- `research/README.md`: VERIFIED consistent with the registry, file census,
  campaign numbers, and SloBench-pending status (no manufactured
  replication/GO); updated in this round with the START HERE pointer and the
  EXPERIMENT-HISTORY.md archival note.
- `research/EXPERIMENT-HISTORY.md`: VERIFIED for its 007-d-era scope (archive
  synthesis; u/v audit figures 180/75/51/54 and 5.04%/8.47% originate here);
  SUPERSEDED AS CURRENT STATE — it does not synthesize 007-h/i/j/m; it remains
  a historical snapshot, not moving status.
- Latest OAP reports (007-k, 007-l, 007-m) and latest research reports
  (007-h/i/j/m): VERIFIED — numbers cross-checked against
  registry/experiments.json, configs, results projections, and private-root
  manifest identities.
- The 007-n report: MACHINE-INVALID and quarantined (section 1); its check
  claims are re-verified by this round and are not cited as accepted
  transcript evidence.
- Owner observations of 2026-09-17: ALL CONFIRMED, with the correction that
  the closure round is 007-o (007-n was the in-flight baseline repair).

## 8. PLAN requirement/evidence matrix (strategic classification, re-verified)

Classifications: IAV = IMPLEMENTED AND VERIFIED; PARTIAL; ABSENT; UNPROVEN.
Flags: U = evidence exists only on the unmerged PR #8; F = fresh evidence
required; G = human gate (human decision, annotation, or deployment
authorization). Nothing in objectives 003-007 exists on `main` (ee2d1b4);
every product-level row is therefore U where anything exists at all.

### 8.1 Demonstrator (PLAN section 15.1, D01-D07)

| ID | PLAN task | Classification | Repository evidence | Limitations and gates |
| --- | --- | --- | --- | --- |
| D01 | Contracts and policy | PARTIAL (U) | Typed SpanSelection/EvidenceRecord/ReviewProposal/OriginalCoordinateEdit/RepairResult/PolicyConfig (objective 003) with tests; keep/replace separated | End-to-end demonstrator path absent |
| D02 | Bounded data import | PARTIAL (U) | 004 source manifests + 006 unigram importer (14 real GETs, verified archives, cache lifecycle) | Bigram/trigram import absent; product corpus index absent |
| D03 | Protection and mapping | ABSENT (product) | Product module absent; research curated code carries seams only (the hand-written Markdown-sensitive protection logic) | G (target-deployment decision for any live verification) |
| D04 | First CPU detector | ABSENT (product) | Research detector exists (experimental layer only) | Research evidence is not product evidence |
| D05 | Isolated reviewer | ABSENT (product) | Concept-verification prototype demonstrated the pattern (offline + 10 live bounded calls in 007-b) | Product reviewer client absent |
| D06 | Acceptance and patcher | ABSENT (product) | Research acceptance semantics studied (007-h/i/j/m; integrity 0/0) | Product patcher absent |
| D07 | CLI and first review | ABSENT (product) | Concept CLI exists only inside the prototype | Product CLI absent |

=> Demonstrator NOT complete; no ICA requested or launched.

### 8.2 Experimental MVP (PLAN section 15.2, M01-M07)

| ID | PLAN task | Classification | Repository evidence / status |
| --- | --- | --- | --- |
| M01 | Initial labelled set | ABSENT (F, G) | No human-labelled real target-configuration output set exists. PLAN: ~50-100 real outputs expanded to ~100-500 with human labels (genuine errors, acceptable alternatives, stylistic-only, non-local) + fully-correct controls + separate calibration/final split. DASSLE gold is benchmark reference text, not human-labelled real Qwen output. |
| M02 | Lemmas and morphology | ABSENT (F) | Research used unigram lookup only (141,162-row vocabulary); no Sloleks/CLASSLA import |
| M03 | Short phrases | PARTIAL (U, research-level) | 1-4 word / 80 code-point replacement bounds and expression retry studied (ten-run studies); product grouping / needs_wider_edit absent |
| M04 | Acceptance calibration | ABSENT (product; F, G) | 007-h/i/j/m produced a large same-sample calibration-like evidence base that is not product calibration and not on the target distribution |
| M05 | Limits and failures | PARTIAL (U, research-level) | 300 s / 2 MB / fail-closed / bounded-worker semantics demonstrated in research; product queue/cancel/size limits absent |
| M06 | Nonstreaming API path | ABSENT | No product nonstreaming path |
| M07 | Comparative report | PARTIAL (research-level) | M0-M3 comparison on four reference-backed datasets + custom alignment (section 5); product-level report absent |

### 8.3 Verified service (PLAN section 15.3, S01-S05)

S01 (wider negative tests), S02 (wider data support), S03 (production
connection), S04 (deployment and rollback), S05 (final documentation): all
ABSENT (service stage not started).

### 8.4 PLAN section 16 MVP criteria

| # | Criterion (PLAN section 16, abridged) | Status |
| --- | --- | --- |
| 1 | Complete main capture before review/delivery | UNPROVEN (concept prototype + research pipeline demonstrate capture; product pipeline absent) |
| 2 | No review call without suspicion | UNPROVEN (detector-gating demonstrated offline in concept verification; product absent) |
| 3 | Reviewer limited to the assigned span or keep | UNPROVEN (the frozen validator protocol demonstrates the contract in research; product absent) |
| 4 | Main history free of repair conversation | UNPROVEN (isolation tested in the concept prototype; product absent) |
| 5 | No changes outside validated spans | UNPROVEN at product level (research integrity: protected/outside 0/0 across 007-h/i/j/m; product absent) |
| 6 | Invalid proposal/failure preserves the completed answer | UNPROVEN (research fail-closed evidence exists; product absent) |
| 7 | Truncated frequencies are not complete statistics | IAV (U) — 006 importer EXACT/CENSORED/UNAVAILABLE semantics tested |
| 8 | Transparent benefit/harm/latency/cost report | UNPROVEN (research reports benefit (reference-based), latency, and call cost; human harm measurement absent) |

PLAN section 14.2 "quality measured on cases that did not serve
development": NOT MET — every current linguistic result is same-sample
(DASSLE/benchmark) or synthetic (concept suite). This is the central
unproven criterion.
Calibration goals (PLAN section 14.3: ~99% accepted-edit accuracy; at most
1 harmful change per 10,000 originally-correct words): NOT MEASURED — no
human harm labels exist; the documented 3/N 95%-upper-bound rule applies at
N = 0.

## 9. Deployment-validity matrix

| Dimension | PLAN target | Evaluated regime |
| --- | --- | --- |
| Intended deployment | Strongly quantized Qwen3.8-27B on RTX 3090 (PLAN v1.0 header: "Ciljna namestitev: obstoječi, močno kvantizirani Qwen3.8-27B na RTX 3090") | A100-FP8, model `qwen3.8-27b`, Responses non-streaming; FP8 observable in the model identity; serving framework vLLM 0.28.0 observed; hardware not mechanically verified, owner-declared (frozen 007-d archive record `research/EXPERIMENT-HISTORY.md`) |
| Reachability at reconnaissance | RTX-3090 endpoint TCP-closed at the 2026-09-09 reconnaissance (an internal address recorded in the private reconnaissance record; loopback vision proxy 502; the endpoint "must not be started/reconfigured") | A100 endpoint reachable; used for every live experiment |
| Second deployment | Deployment B EXCLUDED from full-campaign8 by owner override | — |
| Human target change | NO attributable human decision redefining the intended production target was found in orders, workorders, drafts, or continuity records | — |

Conclusion: the PLAN target (RTX 3090, strongly quantized) REMAINS the
authoritative intended deployment. The entire live evidence base comes from
a DIFFERENT regime (A100-FP8). The mismatch is recorded as an OPEN
EVIDENCE GAP, not a silent substitution: no live result transfers to the
intended deployment without replication. The gap has two resolutions, both
requiring an attributable human decision:
(a) restore/authorize access to the intended quantized deployment for a
    replication run; or
(b) explicitly accept the A100 regime as the research target (a
    product-intent change).

## 10. Open research questions vs completed questions

Completed within objective 007 (evidence: section 4):

1. Can the isolated concept run offline end to end? YES (007-a: prototype,
   frozen dev/held-out detector evidence, 32-case frozen suite).
2. Does the bounded live reviewer produce persisted, accepted local
   decisions? YES, with the recorded instrument boundary (007-b: 10 bounded
   calls on A100; post-evaluation aggregation defect documented).
3. What is the detector's error orientation? OOV/lexical-absence oriented;
   grammatical/punctuation/multi-token reference changes never reach review
   (campaign detector span recall 0.2542; explains the official-scorer
   recall ceiling, section 5.1).
4. How many DASSLE gold units are u/v-related? 180 (75 strict first-letter
   + 51 standalone-word + 54 non-initial); 75/1,487 = 5.04% and
   126/1,487 = 8.47% (mechanical audit, zero calls; 007-d-era archive
   record).
5. Is the corrective retry worth it? ADVERSE (section 5.3: DASSLE +7 TP /
   +132 FP at 581 calls; preservation +0 TP / +88 FP at 395 calls); M3
   no-retry retained as the frozen baseline behavior.
6. What is the same-sample relative behavior of the frozen chain? 604/193/
   911 -> 704/345/811 -> 727/172/788 -> 822/154/693 -> 799/114/716
   (section 5.2, exact denominators).
7. What headroom does C>1 ranking carry? Top-1 covers 247/408 = 60.54% of
   present gold, top-2 85.54%, top-3 92.16%, top-5 97.79%, top-10 100%;
   oracle recall ceiling 0.5426 -> 0.8119 (007-m census).
8. Can the campaign run operationally at scale? YES (9 phases, 8 workers,
   39,184 distinct calls, 1,419 verified checkpoints; 007-f saved replay
   re-verified 16,375/16,375 M2 and M3 matches with zero model/network
   calls).
9. Is the application baseline deterministic and green? YES at the 007-o
   head (007-n repair, implementation accepted; re-verified by this round
   — section 15).
10. Can the complete trail be published data-free and reproduced offline?
    YES (007-c/d/f: registry, file census, source manifest, archive
    catalog, offline reproduction).

Open (owned by a later objective or by a human decision):

- 008 (next research objective): structural-boundary question — does
  pulldown-cmark 0.13.4 provide sufficiently accurate, conservative and
  source-faithful structural segmentation of actual LLM-generated
  Markdown-like output to replace the Markdown-sensitive part of the
  current hand-written protection logic?
- 009 (reserved): fresh untouched human-labelled target-distribution
  linguistic confirmation of the complete effective pipeline (section 13).
- E2: the deployment-resolution decision (a) or (b) from section 9 — human
  gate, prerequisite of E1/E3; not an experiment.
- E3: bounded replication of the frozen method on the intended quantized
  deployment (only if (a) is chosen); replication evidence, not tuning.
- E4: SloBench hidden-reference scoring of the 1,232-row frozen outputs —
  remote scoring access-blocked; requires login authority; does not replace
  009.
- E5: morphology (Sloleks/CLASSLA import; lexical-vs-morphological error
  separation; M02) — may improve candidate quality, does not unblock the
  MVP judgment.
- E6: detector coverage for non-OOV error classes (grammar, punctuation,
  multi-token) — explains the recall ceiling; secondary.
- The 007-a human review sheet remains AWAITING_HUMAN_REVIEW (small scale;
  not a prerequisite of the 009 design).

## 11. Research-debt matrix (what is missing to decide the experimental-MVP linguistic judgment)

| Debt item | Blocks | Owner | Status |
| --- | --- | --- | --- |
| M01 human-labelled target set (~50-100 real outputs, expanded to ~100-500, + fully-correct controls, + separate calibration/final split) | M04 fresh calibration; PLAN section 14.2 judgment; harm-rate estimation | Human annotation + owner collection authorization | ABSENT |
| M04 acceptance calibration on fresh data | Product acceptance-rule selection; section-16 criteria 1-6 and 8 | Research (objective 009) | ABSENT (same-sample evidence base only) |
| PLAN section 14.3 human harm measurement (harmful changes per 10,000 originally-correct words; 3/N 95% upper bound) | The <=1/10,000 harm goal; transparent harm reporting | Human annotation | NOT MEASURED (N = 0) |
| E2 deployment decision (section 9, (a) or (b)) | E1/E3 target regime; every deployment-transfer claim | Human decision | OPEN |
| Product pipeline D03-D07 | Demonstrator completion; product-level section-16 criteria | Product development (separate rounds) | ABSENT |
| M05-M07 at product level (limits/failures, nonstreaming API path, product comparative report) | Verified-service stage (S01-S05) | Product development | ABSENT |
| ICA per S-ICA-01/02 | Milestone-judgment procedure | Strategy/human | NOT LAUNCHED |
| Milestone judgment (strict-mode enablement) | Any production use of the method | Human (owner) | OPEN |

## 12. Updated research sequencing (owner decision of 2026-09-17)

Owner decision (recorded in the 007-o order provenance, kind H):

1. The 007-m linguistic method design is FROZEN FOR CONFIRMATION. Its
   linguistic behaviour must not be tuned during 008 (section 14).
2. Objective 007 closes with this round (007-o): the research state is
   consolidated in this document; PR #8 remains open and unmerged
   (section 15).
3. Objective 008 is a NEW numeric objective on a NEW PR after the 007
   closure, and is the next research uncertainty: qualification of the
   prose/non-prose structural boundary.
   - Research question: does pulldown-cmark 0.13.4 provide sufficiently
     accurate, conservative and source-faithful structural segmentation of
     actual LLM-generated Markdown-like output to replace the
     Markdown-sensitive part of the current hand-written protection logic?
   - Candidate space supplied by the human-commissioned Deep Research
     report "Reliable Prose Segmentation in Mixed LLM Output" (pulldown-
     cmark 0.13.4 is the leading candidate). The candidate is a starting
     hypothesis, not an acceptance.
   - Method stance: falsification-first; no production integration; no
     model calls in the qualification design phase.
   - Prohibited inside 008: any production integration, any change to 007-m
     linguistic behaviour, and any use of 009 confirmation data.
   - This 007-o round carries a design summary of 008 ONLY; it does not
     execute 008 (no parser installation, no fixture creation, no wrapper,
     no challenger comparison).
4. Objective 009 (section 13) runs after 008 freezes the effective
   pipeline.

## 13. Objective 009 — reserved

Objective 009 is reserved for the fresh, untouched, human-labelled
target-distribution linguistic confirmation of the complete effective
pipeline (detector -> candidate generation -> ranking -> validator ->
acceptance -> patching, as frozen after 008). Design requirements (from the
007-o order's analysis baseline):

- Minimum fresh data: 100 real outputs from the intended target
  configuration (PLAN first-step size; expand toward 300-500 for harm-rate
  power) + fully-correct Slovenian control texts (including technical
  terms, rare expressions, proper names). Collection requires explicit
  rights and controlled storage; outputs are private.
- Human annotation REQUIRED, per detected span and per document: genuine
  erroneous target span / acceptable unchanged text / exact intended
  correction / alternative acceptable correction / unnecessary-but-harmless
  stylistic change / harmful or incorrect change / error requiring a wider
  edit; plus detector-miss labels on all genuine errors. Two-labeler
  disagreement recorded; ambiguous cases adjudicated by the owner or a
  named human. Qwen is never the final judge of its own changes.
- Target deployment per the E2 resolution (intended quantized deployment
  if restored; otherwise the A100 regime ONLY with an explicit owner
  designation).
- Frozen method identity exactly (config SHA-256, ranking tuple, prompt
  SHA-256, validator protocol, 300 s / 2,000,000-byte / no-resample limits
  as in section 3). NO tuning against the confirmation set, ever; the set
  is untouched until final scoring.
- Primary metrics (human-adjudicated): accepted-edit accuracy (fraction of
  accepted edits that genuinely fix an error and create none, with the
  count of assessed edits); harmful changes per 10,000 originally-correct
  words with 95% upper bound (3/N at zero events); coverage (fraction of
  genuine errors repaired, separately detector-detected vs finally
  repaired); stylistic-only change rate (separate metric); preservation
  (unchanged correct documents, introduced edit units on correct text).
- Operational metrics: review-call rate, mean/p95 latency, tokens per
  answer, failure/timeout rate.
- Required failure decomposition: every non-repaired genuine error is
  classified into detector miss / candidate-generation miss / ranking miss
  / validator rejection or failure / acceptance-policy rejection / patch
  failure, so a low end-to-end recall stays attributable.
- Stopping rules / falsification: stop and report (a) if accepted-edit
  accuracy falls materially below the ~99% goal with enough assessed edits
  to make the 95% upper bound decisive; (b) if any harmful change is
  established (each one reported; the 1/10,000 target needs ~30,000
  correct words at zero events, so small-N zero events are reported as
  upper bounds, not achievement); (c) if coverage is negligible relative
  to genuine error incidence; (d) if the operational failure rate makes
  the service path unreliable. A pass does not auto-accept the MVP; it
  enables the human milestone decision.

Two prohibitions (owner 2026-09-17, restated in the order):

1. 009 confirmation data must NOT be used during 008.
2. 007-m linguistic behaviour must NOT be tuned during 008.

## 14. Explicit boundary: no further tuning of the 007-m candidate before fresh evidence

Until fresh (009) evidence exists, NO further tuning on DASSLE or any
already-inspected benchmark of:

- the candidate rule (deterministic unique single-letter unigram
  substitution + complete standard Levenshtein distance-one expansion),
- the predeclared lexicographic ranking tuple (section 3),
- the validator prompt (frozen 007-i prompt, section 3),
- the acceptance/conservativeness thresholds,
- the validator protocol limits (300 s / 2,000,000 bytes / one terminal
  attempt / no resampling),
- the retry policy (no corrective retry in the frozen method).

Rationale: researcher degrees of freedom on this one population are
substantially consumed — four successive same-sample mechanism changes
(007-h -> 007-i -> 007-j -> 007-m), each selected on the same 2,973 paired
records. Any further same-sample variant (new ranking functions, prompt
edits, threshold sweeps, C>1 runner-ups, top-k>1 with resampling) carries
overfit risk: a same-sample improvement cannot be distinguished from noise
or adaptation to the inspected gold. No 007-p or later same-sample variant
is authorized. Any future mechanism change requires a new objective, fresh
data, and a new PR.

## 15. Explicit merge/release/deployment limitations

- PR #8 is the 007 closure container: objective 007 rounds 007-a..007-o
  plus the 003-006 product seams and the OAP governance artifacts. At the
  reconciliation point: OPEN, UNMERGED, MERGEABLE, UNSTABLE solely through
  the red OAP bootstrap acceptance check (the quarantined 007-n report;
  resolved by this round), 284 files, +66,792/-78, auto-merge disabled.
  This round's publication adds the 007-o order, this document, the
  README/STATUS corrections, and the consistency test.
- Development-merge conditions (all must hold; merge authority belongs to
  strategy/human, NOT to this round):
  1. 007-n lands green (Application baseline repaired — implemented in
     007-n; re-verified by this round),
  2. 007-o lands with the research-state document,
  3. all four required checks green at the final head (Application
     baseline, Research reproducibility, OAP bootstrap acceptance with
     007-n classified INVALID_QUARANTINED and the 007-d quarantine
     preserved, OAP report history),
  4. independent strategic review complete (S-MERGE-01).
- A development merge is NOT milestone acceptance and NOT deployment. No
  milestone label is assigned; no ICA is launched; no release or
  deployment activity occurs. The D2 boundaries (release, deployment,
  protected-resource changes) remain human-controlled.
- Fresh linguistic research (008/009) belongs to a NEW numeric objective
  and a NEW PR from merged main; historical evidence stays immutable on
  the branch history; this document links records by path + SHA, not by
  copying forward.
- Current Application-baseline status: GREEN at the 007-o head, inherited
  from the accepted 007-n repair and re-verified by this round through the
  real `scripts/verify_development_baseline.py` entry point (the 007-o
  report records the literal temp parent path used). Final-head CI is
  awaited and recorded at the report publication commit.

## 16. Post-merge acceptance update (objective 008, round 008-b)

This section is the additive post-merge acceptance update recorded by the
008-b corrective suffix (D0; classification rationale in the 008-b report).
It changes no scientific result and rewrites nothing in the 007 narrative
(sections 1-15): the only narrative byte changed outside the machine block
is the section 4.2 heading line, which now states both registry counts.

(a) PR #8 (the objective 007 closure container) was development-only merged
2026-09-17: merge commit `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9`, whose
second parent is the reviewed 007-o head
`4a029287f27e038d5c34c39b26ca836be7c6914b`; strategy receipt
`workorders/007-o-final-head-review-20260917.md`. The repository workflows
are pull_request-triggered, so the merge had no deployment side effect. The
machine block now tracks the current accepted main.

(b) The 007-o review point remains fully recorded in the 007 narrative
(sections 1-15), the unchanged quarantined 007-n identity fields, and the
committed 007-o order and report; this identity update is additive and
records the accepted post-merge state. It is not a rewrite of the 007
narrative.

(c) Rationale: the frozen 007-o snapshot test's live-ref and report-count
assertions are structurally unsatisfiable at any post-merge head
(demonstrated at 008-a; disclosed in the 008-a report as a dilemma
candidate; classified D0 by strategy). The only viable non-weakening remedy
is this additive identity update as a corrective suffix. No test logic
changed; every numeric re-derivation assertion remains binding.

(d) 008-a outcome GO (`research/prose-boundary/REPORT.md`;
`oap/reports/008-a-qualify-prose-boundary-parser.md`): 50 frozen fixtures x
3 profiles, 1,288 parser events, 0 coordinate violations, 0
protected-region exposures (under the documented D0 autolink rule), 0
missing prose bytes, 100 deterministically selected preserved outputs
(2,670 unique texts; 100 percent plain prose - recorded representativeness
limitation), 22 class-7 differential spans (18 number, 4 upper-identifier;
110 bytes), 0 safety-class false exposures, markdown-rs challenger
NOT_TRIGGERED.

(e) 008-a final-head CI was red on Research reproducibility and Application
baseline solely through the stale snapshot assertions (as predicted in the
008-a report before push); this round restores all four required checks to
green at its final head.

(f) Correction: `research/prose-boundary/REPORT.md`'s "4,910 input bytes"
is the pre-publication-rework fixture total; the committed post-rework suite
totals 4,907 bytes (F30 reworded 73 -> 70 bytes); no semantic change.

(g) Carried into 008-c: (i) the D0 autolink-destination rule (the config's
literal `candidate_rule` does not encode it; the 183 autolink-destination
bytes of F24/F48 are protected only by that documented D0 evaluator rule;
008-c must implement it in the runtime and amend the committed config rule
text); (ii) the D1 policy token-family matching note; (iii) the recorded
neutral tradeoffs (strikethrough/superscript/subscript exposed; image alt
text protected).

(h) Sequencing: 008-c (parser-first protection architecture; next order on
this branch/PR) freezes the effective pipeline; objective 009 remains
reserved for the fresh human-labelled linguistic confirmation; the 007-m
linguistic system stays frozen.

## 17. Parser-first protection and generated structural corpus (objective 008, round 008-c)

This section is the additive round-008-c record. It rewrites nothing in
sections 1-16 and changes no scientific result of the 007 narrative.

Human decision of 2026-09-17 (received after 008-b publication): the 008-a
GO is supporting evidence for `pulldown-cmark` 0.13.4, not final
independent validation of the prose boundary, because (1) the 50-fixture
adversarial suite was parser-informed during working-tree authoring before
its first committed freeze and (2) the 100 preserved real outputs were 100
percent plain prose and did not exercise the mixed-content problem. LLM
calls are authorized strictly for structural test-data generation (not
linguistic-method tuning; wholly separate from objective 009's future
confirmation set). Objective 008 must produce a much stronger acceptance
corpus: a deterministic mashup corpus with machine-known exact ground truth
plus a naturalistic whole-response corpus, with a mandatory development/
hidden split in which the hidden acceptance set is sealed by hash/manifest
before the implementation is frozen and is evaluated blindly in the next
round (008-d).

008-c change summary (research pipeline only; no 007-m linguistic change;
no 009 data touched): (a) the parser-first protection layer
(`research/curated/prose_boundary.py`; reworked
`research/curated/protected.py`) under the frozen structural policy v2:
parser-derived structural protection from the pinned pulldown-cmark 0.13.4
helper (frozen 008-a candidate identity) plus the narrow residual semantic
recognizer running only on candidate-prose spans in code-point coordinates;
the 008-a full-regex rule set is retained verbatim as the fail-closed
fallback (the layer never fails open); the public `Interval` /
`is_protected` / `protected_intervals` signatures are unchanged for all
consumers; strategy finding B (D0 autolink-destination rule absent from the
008-a config literal) is codified in `structural-policy-v2.json` with
`experiment-008a.json` byte-identical. (b) The authorized generation
program (frozen 76-family prompt library; single pinned Qwen endpoint
identity; budget per the frozen call allocation; actual call ledger
recorded, including all failures, retries and the recovery runs after the
components-stage transport crash and the naturalistic-stage partial
completion) produced the component pools and the 150 naturalistic
whole-response outputs (80 development / 70 hidden). (c) The deterministic
mashup builder composed 3,000 development documents (committed, with
machine-known ground-truth label maps derived purely from composition
provenance; the builder never invokes the parser or the protection layer)
and 2,000 hidden documents (private root only), sealed by
`corpus/manifests/hidden-manifest.json` (content-free) with the committed
hash-verified seal. (d) Dev-corpus evaluation (tuning evidence, NOT
acceptance): protected-bytes-exposed = 0, coordinate violations = 0, the
008-a 50-fixture baseline re-derived through the runtime path with zero
invariant violations, the 008-a 100-sample differential with no class-3
safety regression and the 22 class-7 spans still protected by the second
stage, and end-to-end invariants 1-7 on dev documents. (e) The hidden
acceptance evaluation, the naturalistic label adjudication per the frozen
annotation guide, and the final objective-008 disposition
(PASS/CONDITIONAL/FAIL) are deferred to round 008-d.

008-d corrective note (additive; no rewrite of the 008-c record above):
independent final-head review of the 008-c final head
4b6a90ab13c0c9a02e533a2673a084e26f841a5c found exactly one red required
check - the Application baseline full-pytest stage recorded TIMEOUT at the
frozen 300 s per-command cap (captured session '653 passed, 14 skipped,
89 subtests passed in 337.20s'; zero test failures; the 2026-09-17 pool
ran the near-identical suite in 134.92 s) - a runner-pool timing artifact
on the inherited application suite, not a 008-c test failure; OAP
bootstrap acceptance, OAP report history and Research reproducibility
were green at that head. Round 008-d is the bounded corrective: honest
bounded observation of the frozen stage under the unchanged cap, a
committed data-free timing decomposition, this ledger registration, and
the one stale suffix-reference correction; no gate, cap, driver,
workflow, or test change. Per the D1 recorded in the 008-c final-head
review, the blind hidden acceptance and the final objective-008
disposition are round 008-e (the 'round 008-d' deferral sentence in the
008-c record above carries that pre-renumbering label; the deferral
itself is unchanged).

008-e forward-recovery note (additive; no rewrite of the 008-c or 008-d
records above): the 008-d report is machine-invalid (REPORT_CHECK: three
checks[] command strings carry angle-bracket placeholder tokens; the same
defect class as the quarantined 007-n report) and is classified
INVALID_QUARANTINED by the 008-e order's forward-recovery linkage - no
byte of the 008-d report or order is altered; its evidence claims are
re-verified in the 008-e round. Transcript coherence is restored at the
008-e final head (the deterministic RECOVERY_LINKAGE_MISSING transcript
gate clears by the linkage). The 008-d final-head CI truth: three
required checks green - Research reproducibility (run 35381405131), OAP
report history (run 35381405199), and Application baseline via the
disclosed green identical-commit rerun of the zero-failure TIMEOUT class
(run 35381405077: attempt 1 red, session '653 passed, 14 skipped, 89
subtests passed in 328.50s', zero failures; attempt 2 green, all driver
stages PASSED) - and OAP bootstrap acceptance red and deterministic
(RECOVERY_LINKAGE_MISSING) until this linkage is committed. Per the 008-d
final-head review, the blind hidden acceptance and the final
objective-008 disposition are round 008-f (the 'round 008-e' label in the
008-d note above carries the pre-recovery numbering; the deferral itself
is unchanged).

## 18. Final objective-008 scientific conclusion (blind hidden acceptance, round 008-f)

This section is the additive final objective-008 conclusion recorded by
round 008-f (blind hidden acceptance of the frozen parser-first protection
layer). It rewrites nothing in the 008-c/008-d/008-e records above and
changes no scientific result recorded before this round.

The frozen implementation was evaluated EXACTLY as frozen at the 008-c
final head 4b6a90ab13c0c9a02e533a2673a084e26f841a5c against the sealed
hidden acceptance set (2,000 deterministic mashup documents with
machine-known ground truth plus 70 naturalistic whole-response outputs;
committed content-free manifest sha256
8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18), for the
first and only time as an acceptance instrument.

**Final objective-008 scientific conclusion: CONDITIONAL** (predeclared
decision state; the hidden set is downgraded to single-use evidential
status by this round per the 008-f order).

Field by field against the committed evidence
(research/prose-boundary/results/hidden-acceptance/):

- Safety: 458 of 311,358 labeled protected bytes exposed as candidate
  prose (0.147%; target 0) - a real, bounded, clearly understood defect.
  Attribution: 20 of 2,000 hidden documents, 19-24 B each, all labeled
  category structured (families structured-yaml 348 B + structured-xml
  110 B), all template T10-randomized. Mechanism: CommonMark does not
  recognize mid-document YAML blocks or HTML/XML fragments whose tags are
  not HTML block-start tags, so that content becomes paragraph text and is
  candidate prose under frozen structural policy v2; the residual layer
  partially compensates (number/path/shell fire inside) but block syntax
  stays exposed. Zero exposure on the dev set - the corner case was
  discovered only by the hidden set.
- Coordinates: 0 UTF-8 boundary violations, 0 byte/code-point conversion
  mismatches, 0 source slice mismatches, 0 patch-preservation violations
  (frozen patching.apply_edits(original, []) reproduces the exact original
  on every hidden document).
- Coverage: 97.851% of expected prose bytes exposed
  (1,256,837/1,284,435); 291/7,872 expected prose regions completely
  available; unnecessary suppression is actual loss by container type
  (S.Head 449, S.Item 2302, S.Para 13498, S.TableCell 327, unknown 11022) -
  no arbitrary threshold.
- Malformed-input behaviour: 0 violations over the 10 deterministic family
  rows (frozen malformed_class_map; the policy-decided-suppression
  distinction is preserved).
- End-to-end invariants 1-7: all PASS on 2,000/2,000 hidden-document
  replays through the actual frozen pipeline entry points (frozen
  deterministic stub boundary; zero network; zero new model calls; 20
  seeded adjacencies all edit_applied; synthetic zero-eligible ok).
- Determinism: 50-case re-run identical; fixed iteration order.
- Performance: median 44.5 / 67.6 / 254.2 ms/document at 1/10/50 KB
  (second deterministic re-run; first run 44.3 / 63.4 / 252.2 ms - timing
  axis only); parser + residual cost is cheap relative to one model
  inference (qualitative statement only).

Decision state application: NOT PASS (a material safety violation exists:
458 B above the 0 target); NOT FAIL (the exposure is bounded to 0.147% of
labeled protected bytes, confined to one corner-case class - mid-document
YAML-style blocks and HTML/XML fragments - with a fully understood
mechanism; the parser-first design is not materially discredited);
CONDITIONAL, with the defect named and bounded as above. Named smallest
corrective 008-g scope: extend protection for mid-document raw document
blocks (YAML-style blocks and HTML/XML fragments) via a policy-v2 residual
class or a structural pre-pass, and re-evaluate the full item-15 metrics
set plus e2e invariants 1-7 on a NEW independently generated and sealed
hidden set.

Round 008-f execution was BLOCKED before completing scope item 3: the
independent naturalistic adjudication of the 70 hidden whole-response
outputs stopped at case nat-comparison-table-hidden-04 (invalid
verbatim-quote tiling on two consecutive attempts under the predeclared
at-most-one-retry policy; fail-closed; no label fabricated). 17 of 70
pass-1 tilings are valid and preserved as raw observations in the private
root; 0 label files exist; no annotations manifest was written. Revised
interpretation (C-EVIDENCE-01): model-side tiling anomaly specific to that
case, not a driver defect (17/17 prior cases and 2/2 prequalification
pilots valid; 8/8 synthetic resolver self-tests correct and fail-closed).
The named 008-g scope therefore additionally covers adjudication
completion with a strategy-devised refined instrument. Hidden seal
identities before/after evaluation: 4091/4091 verified both times,
committed manifest sha256 unchanged, seal copy byte-identical;
out-of-manifest files 387 before (386 pre-seal generation receipts + the
seal copy) and 405 after (the same 387 + 18 annotations raw files, the
disclosed adjudication-process scope).

Classification: this conclusion is STRUCTURAL-SAFETY EVIDENCE ONLY. It
establishes no linguistic quality, no experimental-MVP acceptance, and no
release or deployment authority. Objective 009 (fresh human-labelled
linguistic confirmation of the complete frozen pipeline) remains the
separate reserved next objective; its future sample must not contain any
case generated or inspected for objective 008. No merge, no auto-merge, no
release, no deployment claim; PR #9 remains open and unmerged.

## 19. Final objective-008 verdict (bounded raw-block fix, completed
adjudication, new sealed v2 hidden set, round 008-g)

This section is the additive final objective-008 verdict recorded by
round 008-g (the corrective and final-verdict round of objective 008). It
rewrites nothing in section 18 or any earlier record and changes no
scientific result recorded before this round. The 008-f section 18 and the
008-f report remain immutable; this verdict supersedes the 008-f
CONDITIONAL as the current state of objective 008 additively, here and in
STATUS.md only.

The fixed implementation (the bounded mid-document raw-block fix: the
strict single-line machine-like yaml-toml-config trigger plus the new
xml-fragment residual class, structural policy v3 sha256
7ff6646e3c11d1241cb1c85bd96f08e3f0db08e73d4eb4a4e97fac0c17e1828f, with the
policy v2 -> v3 sha256 pair 996f4657.../7ff6646e... recorded in
experiment-008g.json) was evaluated EXACTLY as frozen at the dev-regression
gate (frozen protection identity census recorded in
experiment-008g.json) against the NEW sealed v2 hidden acceptance set
(2,000 deterministic mashup documents with machine-known ground truth by
construction, 340 components across all 76 families, zero exact-component
overlap with the dev and v1 pools asserted and disclosed; committed
content-free manifest sha256
cf37654a45b10c024525fc334f368d4b20956619e2568542544c855d93a85ec1), for the
first and only time as an acceptance instrument, with the completed 70-case
naturalistic hidden adjudication and the naturalistic consistency check.
Both seals were re-verified data-free before and after the evaluation phase
(v2 4076/4076, manifest sha256 unchanged; v1 4091/4091, manifest sha256
8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18 unchanged),
and strategy independently re-verified the v2 seal data-free before the
evaluation phase (receipt 008g-v2-seal-strategy-verification-20260919.md,
sha256 b24ed3f6693d19d180972d440f09d1c3c562d6e8e260d804ecac9f4a8d1488a5).

**Final objective-008 verdict: CONDITIONAL** (predeclared decision state;
structural-safety evidence only).

Field by field against the committed evidence
(research/prose-boundary/results/hidden-acceptance-v2/):

- Safety (v2 acceptance set): 51 of 384,363 labeled protected bytes
  exposed as candidate prose (0.0133%; target 0) - the one material
  defect. Attribution: 3 of 2,000 documents, all template T10-randomized:
  v2h-001054 (code-python, 35 B) - an adjacent structured-html closing tag
  opens an HTML block that absorbs the code fence plus 132 B of code; the
  blank line ends the block and the remaining code lines parse as
  paragraph, exposing the print-line syntax while identifier-like words
  and the number 99 stay covered; v2h-000262 and v2h-000218
  (structured-keyvalue, 8 B each) - the component embeds Markdown list
  items with quoted emphasis and the dialect parses list+strong/emphasis,
  exposing quote characters plus one word. The identical 51 B under the
  frozen 008-c implementation shows this is a pre-existing architecture
  gap newly surfaced by the fresh pool, not a fix regression.
- Coordinates: 0 UTF-8 boundary violations, 0 byte/code-point conversion
  mismatches, 0 source slice mismatches, 0 patch-preservation violations.
- Coverage: 97.843% of expected prose bytes exposed (1,153,924/1,179,365);
  494/8,382 expected prose regions completely available; unnecessary
  suppression is actual loss by container type (S.Emph 56, S.Head 240,
  S.Item 1788, S.Para 12802, S.TableCell 268, unknown 10287) - no
  arbitrary threshold.
- Malformed-input behaviour: 0 violations over the 10 deterministic family
  rows. Disclosed: the committed aggregate's policy_exposed row totals for
  the four policy-exposed families (58/84/34/16) carry a +7 B
  first-document double-count from the frozen 008-f harness
  merged_malformed aggregation; the true label values, independently
  recomputed from the sealed v2 labels, are 56/81/33/15; the violation
  counts are unaffected and the frozen harness byte was not changed.
- Policy-exposed census (challenge #4 number, stated explicitly): 1,174 B
  total over the v2 set remain policy-exposed by label role -
  machine-emails 989 B (inherited from the v2 policy; non-machine-like
  values abstain by the v3 strictness contract) plus the four
  policy-exposed malformed families 185 B (incomplete-display-dollar 56,
  malformed-nesting 81, unmatched-backtick 33, unmatched-dollar 15). The
  defect-class families (structured-yaml, structured-xml,
  structured-keyvalue) contribute 0 B policy-exposed, and the new v3
  yaml-nested-parser-split class materialized 0 B on the v2 set (28 B in
  the visible dev defect batch).
- End-to-end invariants 1-7: all PASS on 2,000/2,000 hidden-document
  replays through the actual frozen pipeline entry points (frozen
  deterministic stub boundary; zero network; zero new model calls; the
  embedded raw frozen-harness output is explicitly labelled as raw
  frozen-harness output over the v2 set, not a development-run result).
- Determinism: 50-case re-run identical; fixed iteration order.
- Performance: median 46.1 / 66.9 / 269.7 ms/document at 1/10/50 KB,
  peak RSS 69,088 KB (qualitative statement only).

Naturalistic hidden adjudication - COMPLETED (round 008-f scope item 3,
executed here under the strategy-devised refined instrument): 70/70
label files in the private root, 0 ADJUDICATION_FAILED, 113 HTTP calls
(1 preflight + 70 pass-1 + 42 pass-2; 0 retries; 0 failed calls), model
qwen3.8-27b (A100-FP8 007-lineage deployment record; profile sha256
510c3394d2ccad8a098660b8b5512d338de0a5b77352ec693d2286ee2223723c). Final
line-category totals: AMBIGUOUS 200, GENUINE_PROSE 326,
STRUCTURAL_PROTECT 399, MACHINE_SIGNIFICANT_RESIDUAL 0,
DELIMITER_WHITESPACE_NEUTRAL 0. Reconciliation: 39 disagreement_reconciled
(102 disagreement line spans), 3 identical, 28 single_pass. The committed
content-free annotations manifest covers the 18 v1 raw files and all 70
v2 label files (case IDs + sha256 + size only). Cross-instrument
agreement (sanity statistic only, not acceptance evidence): 17 comparable
cases (17 of 18 v1 raw files carry valid frozen tilings;
nat-comparison-table-hidden-04 is the known invalid tiling); strict line
agreement 334/447, ambiguous-tolerant 418/447. The order's predeclared
"3 valid v1 tiling cases" wording is flagged: the actual comparable count
is 17. Driver defect and recovery (disclosed): the first run (same sample
seed f3d72dd46013a779) completed passes 1-2 and then crashed in the
mechanical cross-instrument phase - unassigned quote-tiling glue code
points in the frozen v1 tilings left the line-vote plurality empty; its
at-least-118 HTTP calls are disclosed as driver-defect recovery overhead;
its on-disk labels and raws were censored data-free and removed before the
official re-run; the fix (glue excluded from the vote) lives in the new
v2 driver with self-tests 18/18.

Naturalistic consistency check (requirement 8): 5 material
contradictions against the predeclared materiality -
nat-glossary-entry-hidden-03 (max 69 B exposed), nat-json-config-hidden-01
(255 B), nat-math-answer-hidden-04 (53 B), nat-qa-answer-hidden-04 (66 B),
nat-table-equations-hidden-03 (125 B); attribution of the exposed ranges:
12 parser-dialect, 2 label-ambiguity, 1 residual-class-gap. By the
predeclared rule this caps the verdict at CONDITIONAL.

Dev regression gate (committed before any hidden evaluation): PASS - dev
corpus new safety exposure 0, dev defect batch defect-class safety 0,
prose over-suppression +0.0113 pp against the predeclared 1.0 pp bound;
actual losses reported by container regardless.

Labeled v1 diagnostic (disclosed; the spent v1 set, never acceptance):
458 B still exposed under the fixed implementation, unchanged from the
008-f number - the named scope shapes are fixed (dev batch 0), but the v1
defect population contains two sub-shapes outside the scope-4 strictness
contract: YAML '#' comment lines parsed as Markdown headings (348 B + 5 B)
and XML tag names containing non-ASCII (diacritic) letters (110 B; the
v3 xml-fragment trigger RE_XML_NAME is ASCII-only). Disclosed as the
remaining bounded scope, not as acceptance evidence.

Decision state application: NOT PASS (the v2 safety target is not met:
51 B above 0; and 5 material naturalistic contradictions exist); NOT FAIL
(every exposure is bounded and its mechanism fully understood; the named
defect class itself is fixed on the fresh pool with zero exposure in the
structured-yaml / structured-xml families; the parser-first design is not
materially discredited); CONDITIONAL, with the smallest corrective scope
named: (a) a builder-side T10 composition adjacency guard for the
code-python / structured-html boundary (35 B) and the
Markdown-emphasis-in-keyvalue composition (16 B), or a label-oracle
refinement; (b) the five named material naturalistic-consistency cases
(parser-dialect-dominated residual).

Judgment debt: D1-1 (fix mechanism for the mid-document raw-block
defect) is CARRIED FORWARD - it clears only on a final objective-008 PASS
verdict. D1-2 (adjudication instrument) is CLEARED - the adjudication
completed 70/70 with reconciliation statistics recorded in this record
and the report.

Classification: this verdict is STRUCTURAL-SAFETY EVIDENCE ONLY. It
establishes no linguistic quality, no experimental-MVP acceptance, and no
release or deployment authority. Objective 009 (fresh human-labelled
linguistic confirmation of the complete frozen pipeline) remains the
separate reserved next objective; its future sample must not contain any
case generated or inspected for objective 008 (every v1 and v2 component,
mashup, and naturalistic case). No merge, no auto-merge, no release, no
deployment claim; PR #9 remains open and unmerged.

## 20. Final objective-008 verdict (composition-contract fix, policy v4,
new sealed v3 hidden set, round 008-h)

This section is the additive final objective-008 verdict recorded by
round 008-h (the corrective and final-verdict round 2 of objective 008,
executing the 008-g named smallest corrective scope). It rewrites nothing
in section 19 or any earlier record and changes no scientific result
recorded before this round. The 008-g section 19 and the 008-g report
remain immutable; this verdict supersedes the 008-g CONDITIONAL as the
current state of objective 008 additively, here and in STATUS.md only.

The fixed implementation (the composition-contract fix: builder rule R1
(one blank line, template-owned NEUTRAL delimiter, recorded in the
document composition provenance) so a fenced or indented code component
is never composed on the line immediately after an HTML closing-tag line,
builder rule R2 (no structured-keyvalue component containing a
list-item-style line with quoted emphasis into the v3 pool; 0 exclusions
for this pool), and the single predeclared xml-fragment trigger decision
EXTEND (the trigger name pattern widened from ASCII letters to Unicode
letters, `(?!\d)\w[\w.:-]*`, with the shape guards unchanged; the
predeclared FALLBACK branch with R3 was available and NOT triggered),
plus structural policy v4 sha256
f564d9f87ef01a893d6cd6bb36f6cf99a0d353a4dde4e4c4c024942eb969e76f (additive
policy-exposed dialect-ambiguity classes with shape rules and measured
evidence; the v3 file byte-identical in-tree; the v3-to-v4 sha256 pair
7ff6646e.../f564d9f8... recorded in experiment-008h.json) was evaluated
EXACTLY as frozen at the dev-regression gate (frozen protection identity
census = the four-file census recorded in experiment-008h.json) against
the NEW sealed v3 hidden acceptance set (2,000 deterministic mashup
documents with machine-known ground truth by construction, 345 components
across all 76 families - densified 16 each for the four
dialect-interaction families structured-html, structured-keyvalue,
structured-xml, malformed-partial-html - zero exact-component overlap with
the dev, v1, and v2 pools asserted and disclosed with the bounded
zero-overlap recovery; committed content-free manifest sha256
ee503bd7c09f26a1b9c171319cc82f8ec692918d0d7d18f11d528a6f18c54f36), for
the first and only time as an acceptance instrument, with the naturalistic
consistency re-run against the existing 70 labels. All three seals were
re-verified data-free before and after the evaluation phase (v3 4076/4076,
manifest sha256 unchanged; v2 4076/4076, manifest sha256
cf37654a45b10c024525fc334f368d4b20956619e2568542544c855d93a85ec1
unchanged; v1 4091/4091, manifest sha256
8233bdcf683df8a97d62a375a6cf60d93b64aa6b7ecf22489ce9986333436a18
unchanged), and strategy independently re-verified the v3 seal data-free
BEFORE the evaluation phase (receipt strat-verify-tmp/
v3seal-result-pre-20260920-211915.json, sha256
46756a8ab18509a949dd5b1cf9cb611f166e5465b15c9a04692540c8208a360b, 3,623
B, cites the v3 manifest sha256) and all three seals AFTER the evaluation
phase (receipt strat-verify-tmp/v3seal-result-post-20260920-214519.json,
sha256 ecee7e285d073e69f6160ef63a2e3726c9c4db8ddbc26af9c3c5a855199f814a;
the receipt paths are in the supervision tree and not committed).

**Final objective-008 verdict: CONDITIONAL** (predeclared decision state;
structural-safety evidence only).

Field by field against the committed evidence
(research/prose-boundary/results/hidden-acceptance-v3/):

- Safety (v3 acceptance set; hard axis = construction-labeled protected
  bytes, zero tolerance): 364 of 232,816 construction-labeled protected
  bytes exposed as candidate prose (0.156 percent; target 0) - the one
  material defect. Attribution: 5 of 2,000 documents, three named bounded
  mechanism shapes: (1) 2 x 139 B (v3h-000713, v3h-001274; code-cpp) - an
  HTML OPENING-tag line (the last line of an adjacent structured-html
  component) opens a CommonMark type-6 HTML block that absorbs the code
  fence plus the first code lines to the internal blank line; the
  remaining code lines parse as paragraph and are exposed (machine tokens
  inside covered by residual classes); the released R1 predicate is
  closing-tag-scoped, so this complement shape is not covered and R1
  correctly did not fire (v3 R1 insertions 0); (2) 2 x 30 B (v3h-000625,
  v3h-001241; structured-xml) - a single-line multi-tag XML line in which
  one tag carries a non-ASCII (Slovenian) attribute name that the
  dialect's ASCII-only inline-HTML rule does not recognise; the frozen
  xml-fragment class abstains because the tag name is in the ASCII dialect
  vocabulary, so the tag bytes are exposed (18 + 10 + 2 B) while the
  interior machine tokens stay covered; (3) 1 x 26 B (v3h-001307;
  math-display-dollar) - an adjacent malformed-incomplete-display-dollar
  component makes the parser pair its unterminated `$$` opener with the
  complete component's opening `$$`; the TeX body parses as paragraph
  where the frozen classes cover numbers, identifier runs, and brace
  groups but not TeX command names or `=` (14 + 12 B). The exposure is
  BYTE-IDENTICAL under the 008-g implementation (the single 008-h curated
  change reverted, verified as the only curated delta): a pre-existing
  architecture gap newly surfaced by the fresh pool, not a fix regression.
  The oracle-refined protected census (950 B of 65,414, 24 documents) is
  a policy-coverage census with the disclosed circularity limitation (the
  label oracle is the implementation's own residual function); it does not
  gate the verdict. The raw frozen-harness record (298,230 protected
  bytes, 1,314 raw-exposed) reconciles exactly: 364 + 950.
- Coordinates: 0 UTF-8 boundary violations, 0 byte/code-point conversion
  mismatches, 0 source slice mismatches, 0 patch-preservation violations.
- Coverage: 96.811 percent of expected prose bytes exposed
  (1,264,413/1,306,063); 600/8,400 expected prose regions completely
  available; unnecessary suppression is actual loss by container type
  (S.Emph 49, S.Head 570, S.Item 2495, S.Para 14830, S.TableCell 256,
  unknown 23450) - no arbitrary threshold.
- Malformed-input behaviour: 0 violations over the 10 deterministic
  family rows; the policy-exposed row totals were independently
  recomputed from the sealed v3 labels (per-family
  first-contributing-document identity; the known frozen-harness
  first-document double-count carried as a defect): delta 0 satisfied for
  all families; raw rows and recomputed true values both committed; no
  frozen byte changed.
- End-to-end invariants 1-7: all PASS on 2,000/2,000 hidden-document
  replays through the actual frozen pipeline entry points (frozen
  deterministic stub boundary; zero network; zero new model calls; the
  embedded raw frozen-harness output is explicitly labelled as such).
- Determinism: 50-case re-run byte-identical; fixed sorted-doc_id
  iteration order.
- Performance: median 46.7 / 68.6 / 276.8 ms/document at 1/10/50 KB,
  peak RSS 72,732 KB (qualitative statement only).

Naturalistic consistency re-run (requirement 8; the fixed 70-label
population; no re-adjudication; no new naturalistic generation): 5
material cases (identical to the 008-g five), 15 exposed ranges, exposed
byte counts byte-identical to the committed 008-g aggregate (the EXTEND
trigger is monotonic - it only adds protection - and changed nothing on
this population). Per-range resolution (D1-4): 15/15
DOCUMENTED-DIALECT-LIMITATION with the v4 class references
(markdown-table-dialect-boundary x9, list-item-candidate-prose x2,
indented-code-lazy-continuation x1, residual-token-line-glue x3); 0
CLOSED-RESIDUAL (no shape falls in a named machine-significant category
with a viable bounded recognizer); 0 AMBIGUOUS; 0 UNRESOLVED - verdict
condition (vii) satisfied. Attribution (carried 008-g heuristic):
parser-dialect 12, label-ambiguity 2, residual-class-gap 1. The narrow
predeclared label-correction path was NOT triggered (label_corrections
empty: no frozen label factually wrong about the source text).

Dev regression gate (committed before any v3 generation): PASS - dev
corpus new safety exposure 0 (of 526,315 protected bytes), 008-g batch
safety 0, dev-edge protected-shape safety 0 (32 documents; order target
30, +2 disclosed end-of-input HTML-block-tail boundary variants), prose
over-suppression +0.021674 pp against the predeclared 1.0 pp bound
(+0.032983 pp vs the 008-c baseline); all four predeclared stop
conditions not fired; actual losses reported by container regardless.

Composition-contract fix record: R1 (closing-tag-scoped predicate per the
order) and R2 (hash-only matching predicate; excluded count 0 for this
pool) are in the committed builder (sha256
647ecf1ff3649f22867d124f70201135c267f3aa08328d900186371168fa5451) with
the composition provenance recording, the admission-rule recording, and
the no-parser-participation assertion retained; R3 is defined and
unit-tested but INACTIVE under the EXTEND decision. The visible dev
dialect-edge batch (defect-dev-008h/, 32 documents + 32 machine-known
labels) pins the ordered shapes with (protected) and without
(policy-exposed per v4) the R1 separator, the keyvalue shape, the
yaml-hash-comment-heading shape, the xml-diacritic-tag-name shape
(protected under EXTEND), the item-4 negative controls, and genuine prose
controls. The ordered closing-tag shape (the 35 B v2 shape) has zero v3
occurrences: the released R1 covers it by construction.

Label-source census (committed in the v3 manifest): construction-labeled
PROTECTED 232,816 B / 2,482 regions; oracle-refined PROTECTED 65,414 B /
1,462 regions; POLICY_EXPOSED 1,688 B / 331 regions (oracle-refined,
v4-class shapes).

Decision state application: NOT PASS (the v3 hard safety axis is not
met: 364 B above 0); NOT FAIL (every exposed byte is bounded and its
mechanism fully understood; the three shapes are composition/class-
boundary facts addressable at the builder/label-oracle level, not by a
further residual recognizer; the parser-first design detected all of it
on the fresh pool - the set's defect-detection purpose - and the dev
corpus plus the 008-g batch remain at zero exposure); CONDITIONAL, with
the smallest corrective suffix named (e.g. 008-i): (1) extend the R1
composition predicate from HTML closing-tag lines to all HTML
block-start lines (the 278 B absorption shape); (2) a bounded
class-boundary analysis of the 60 B xml-fragment non-ASCII-attribute
shape (trigger refinement or documented class) and of the 26 B
display-dollar pairing shape (a bounded malformed-family composition
guard or a documented class); (3) the T6 link-destination admission/label
refinement (the disclosed bounded pre-existing observation; not a v3
exposure). Structural-safety-only in every item; no residual-grammar
growth; objective 009 untouched.

Judgment debt: D1-3 (composition-contract fix mechanism) is CARRIED - the
fix is committed and the fresh pool validated it against the ordered
closing-tag shape (zero v3 occurrences), but the debt clears only on a
final objective-008 PASS. D1-4 (final-round acceptance-criteria design:
per-case resolution + label-source split) is CARRIED - the resolution
aggregate is committed and the split operated as designed, but the debt
clears only on a final PASS with the resolution aggregate committed. The
carried 008-g D1-1 (fix mechanism for the mid-document raw-block
defect) remains CARRIED - it clears only on a final objective-008 PASS
on a fresh set. On the (non-occurring) PASS branch, the objective-008
protection layer would be declared FROZEN at the 008-h census (frozen
protection identity = the four-file census in experiment-008h.json;
policy of record = v4 f564d9f8...) - that declaration is NOT made by
this round.

Classification: this verdict is STRUCTURAL-SAFETY EVIDENCE ONLY. It
establishes no linguistic quality, no experimental-MVP acceptance, and no
release or deployment authority. Objective 009 (fresh human-labelled
linguistic confirmation of the complete frozen pipeline on a new target
distribution) remains the separate reserved next objective; its future
sample must not contain any case generated or inspected for objective
008 (every v1, v2, and v3 component, mashup, naturalistic case, dev
document, dev batch, and dev-edge document). No merge, no auto-merge, no
release, no deployment claim; PR #9 remains open and unmerged.

## Machine-readable state block (research-state-machine-v1)

This fenced block is the machine-readable core of the numbers quoted above.
`research/tests/test_research_state_consistency.py` re-derives every value from
the primary records named in section 1 and asserts equality against this block;
it fails if any embedded number or identity is altered. CPU-only, offline, zero
model/network calls.

```json
{
  "schema": "research-state-machine-v1",
  "identities": {
    "main_sha": "7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9",
    "branch": "oap/007-concept-verification",
    "pr_number": 8,
    "reviewed_branch_head_sha": "7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9",
    "reviewed_branch_head_parent_sha": "4a029287f27e038d5c34c39b26ca836be7c6914b",
    "quarantined_007n": {
      "classification": "INVALID_QUARANTINED",
      "validation_error": "REPORT_CHECK",
      "publication_commit": "735c9830db95cbb02fc80446b6d28f62a56f10c9",
      "report_path": "oap/reports/007-n-restore-deterministic-application-baseline.md",
      "report_blob": "2b74413b54faf65de7659d3cf9957271d7721573",
      "report_sha256": "a0bf18f8b0e1218104f3fa4951be62758a3f4f5e88e7d776c4abe3d596b8372a",
      "order_path": "oap/orders/007-n-restore-deterministic-application-baseline.md",
      "order_sha256": "0627cf26015dac47b17085e9f75b857f563379962a9590d5c8534e02e3f64f82",
      "implementation_parent": "b61f8e2e6b454a0969e5f2ac9009d4da87b8b215"
    },
    "quarantined_008d": {
      "classification": "INVALID_QUARANTINED",
      "validation_error": "REPORT_CHECK",
      "publication_commit": "c0786f9898d3a97aefe9d063bcd43210c0d7d2f1",
      "report_path": "oap/reports/008-d-application-baseline-restoration.md",
      "report_blob": "13effeaae9ec50ae9779d5ab0caa3c568a88362b",
      "report_sha256": "6efbf90ee83e76997eb84985e3fe6f3498ba837a2998900094a0f4238c785a60",
      "order_path": "oap/orders/008-d-application-baseline-restoration.md",
      "order_sha256": "4e15638298f40b8871c2638371a2b5bfefa7d7df465d32eea6f1b907a9dfcbab",
      "implementation_parent": "3baa4f3318f76ba5fc44260829f3f593832695bf"
    },
    "frozen_007m_configuration_sha256": "0026a1a9d27652c36e2c5a960b10fafc1c9a93b0690d93b09089aa58884f5c26",
    "frozen_007m_prompt_sha256": "572cf2fb4864e66e38a500465e1089062d58aeed4721063fb0c1e466e424230d",
    "frozen_007m_final_root_manifest_sha256": "3fb4aef33542e7fa3f357acb905b75f4d7e7551783f83a422b5d1ea6272c25f8",
    "registry_entries": 32,
    "oap_reports_reviewed": 51,
    "frozen_report_history_incidents": 2
  },
  "official_scorer": {
    "note": "official scorer (ERRANT + GLEU), NOT the custom alignment",
    "benchmarks": {
      "multigec-train": {
        "source_sha256": "d313140633ceffcb7ba4cb468aaffc59d84fc2c82e2cc24bb965266c8de74273",
        "examples": 10,
        "methods": {
          "M0": {
            "tp": 0,
            "fp": 0,
            "fn": 792,
            "precision": 1.0,
            "recall": 0.0,
            "F0.5": 0.0,
            "GLEU": 29.7105
          },
          "M1": {
            "tp": 239,
            "fp": 237,
            "fn": 553,
            "precision": 0.5021,
            "recall": 0.3018,
            "F0.5": 0.4432,
            "GLEU": 55.8223
          },
          "M2": {
            "tp": 18,
            "fp": 19,
            "fn": 774,
            "precision": 0.4865,
            "recall": 0.0227,
            "F0.5": 0.0957,
            "GLEU": 31.4699
          },
          "M3": {
            "tp": 18,
            "fp": 15,
            "fn": 774,
            "precision": 0.5455,
            "recall": 0.0227,
            "F0.5": 0.0974,
            "GLEU": 31.5333
          }
        }
      },
      "multigec-dev": {
        "source_sha256": "479d3a79b1664cda5f546d419d30e819b0e506e9feba3ad6a4cf06d4fd19ba11",
        "examples": 50,
        "methods": {
          "M0": {
            "tp": 0,
            "fp": 0,
            "fn": 3573,
            "precision": 1.0,
            "recall": 0.0,
            "F0.5": 0.0,
            "GLEU": 49.8263
          },
          "M1": {
            "tp": 1030,
            "fp": 900,
            "fn": 2543,
            "precision": 0.5337,
            "recall": 0.2883,
            "F0.5": 0.456,
            "GLEU": 64.9078
          },
          "M2": {
            "tp": 81,
            "fp": 77,
            "fn": 3492,
            "precision": 0.5127,
            "recall": 0.0227,
            "F0.5": 0.0963,
            "GLEU": 50.9906
          },
          "M3": {
            "tp": 80,
            "fp": 61,
            "fn": 3493,
            "precision": 0.5674,
            "recall": 0.0224,
            "F0.5": 0.0967,
            "GLEU": 50.9331
          }
        }
      },
      "solar-canonical": {
        "source_sha256": "b3f6ad1f621b9ac0f79138024652b8d3192c16ade22ccb615a34bb06e8d30fa8",
        "examples": 109,
        "methods": {
          "M0": {
            "tp": 0,
            "fp": 0,
            "fn": 7951,
            "precision": 1.0,
            "recall": 0.0,
            "F0.5": 0.0,
            "GLEU": 49.0726
          },
          "M1": {
            "tp": 2196,
            "fp": 1938,
            "fn": 5755,
            "precision": 0.5312,
            "recall": 0.2762,
            "F0.5": 0.4484,
            "GLEU": 64.1473
          },
          "M2": {
            "tp": 162,
            "fp": 235,
            "fn": 7789,
            "precision": 0.4081,
            "recall": 0.0204,
            "F0.5": 0.0849,
            "GLEU": 50.3534
          },
          "M3": {
            "tp": 158,
            "fp": 191,
            "fn": 7793,
            "precision": 0.4527,
            "recall": 0.0199,
            "F0.5": 0.0845,
            "GLEU": 50.3398
          }
        }
      },
      "dassle": {
        "source_sha256": "e944ad5d5e34149ef7261fb2117ffc92bbc2e366b5a054a519dce809587906ad",
        "examples": 7381,
        "methods": {
          "M0": {
            "tp": 0,
            "fp": 0,
            "fn": 8578,
            "precision": 1.0,
            "recall": 0.0,
            "F0.5": 0.0,
            "GLEU": 67.9624
          },
          "M1": {
            "tp": 2291,
            "fp": 2940,
            "fn": 6287,
            "precision": 0.438,
            "recall": 0.2671,
            "F0.5": 0.3883,
            "GLEU": 74.7351
          },
          "M2": {
            "tp": 843,
            "fp": 521,
            "fn": 7735,
            "precision": 0.618,
            "recall": 0.0983,
            "F0.5": 0.3003,
            "GLEU": 71.4808
          },
          "M3": {
            "tp": 836,
            "fp": 387,
            "fn": 7742,
            "precision": 0.6836,
            "recall": 0.0975,
            "F0.5": 0.3103,
            "GLEU": 71.4226
          }
        }
      }
    }
  },
  "custom_alignment": {
    "view": "dassle-spelling",
    "population": {
      "paired_records": 2973,
      "spelling_cases": 1487,
      "preservation_reference_inputs": 1486
    },
    "gold_units": {
      "all": 1515,
      "initial_uv": 75,
      "without_initial_uv": 1440
    },
    "stages": {
      "baseline": {
        "tp": 604,
        "fp": 193,
        "fn": 911,
        "precision": 0.7578419071518193,
        "recall": 0.39867986798679866,
        "F0.5": 0.6421433127790771
      },
      "007h_unrestricted": {
        "tp": 704,
        "fp": 345,
        "fn": 811,
        "precision": 0.6711153479504289,
        "recall": 0.4646864686468647,
        "F0.5": 0.6163544037821747
      },
      "007i_validated_fallback": {
        "tp": 727,
        "fp": 172,
        "fn": 788,
        "precision": 0.8086763070077865,
        "recall": 0.47986798679867987,
        "F0.5": 0.7112111132850714
      },
      "007j_validated_fallback": {
        "tp": 822,
        "fp": 154,
        "fn": 693,
        "precision": 0.8422131147540983,
        "recall": 0.5425742574257426,
        "F0.5": 0.7584425170695701
      },
      "007m_hybrid": {
        "tp": 799,
        "fp": 114,
        "fn": 716,
        "precision": 0.8751369112814896,
        "recall": 0.5273927392739274,
        "F0.5": 0.7731759241339268
      }
    },
    "007m_vs_007j": {
      "tp_delta": -23,
      "fp_delta": -40,
      "fn_delta": 23,
      "precision_delta": 0.0329237965273913,
      "recall_delta": -0.015181518151815232,
      "F0.5_delta": 0.014733407064356663,
      "preservation_changed_cases": [
        78,
        93,
        -15
      ],
      "preservation_introduced_edit_units": [
        83,
        101,
        -18
      ]
    },
    "calls": {
      "007m_final_root_new_calls": 0,
      "007m_reused_c_gt_1_observations": 882,
      "007j_fresh_validator_calls": 493
    },
    "validator_latency_seconds": {
      "007m_inherited": {
        "n": 866,
        "mean": 16.193259791632915,
        "p95": 33.48273886600509,
        "max": 184.56243890197948
      },
      "007j_fresh": {
        "n": 493,
        "mean": 10.71780110838896,
        "p95": 24.88524721498834,
        "max": 58.17827162001049
      }
    }
  },
  "campaign": {
    "experiment_id": "full-campaign8",
    "cases": 16375,
    "method_records": 65500,
    "distinct_calls": 39184,
    "new_model_calls": 31916,
    "inherited_calls": 7268,
    "verified_checkpoints": 1419,
    "workers": 8,
    "completed_phases": 9,
    "deployment": "A100_FP8_ONLY",
    "custom_end_to_end_dassle": {
      "N": 7385,
      "gold_edits": 8623,
      "methods": {
        "M1": {
          "tp": 2212,
          "fp": 2766,
          "fn": 6411,
          "precision": 0.44435516271595016,
          "recall": 0.25652325176852603,
          "F0.5": 0.3875941825827931,
          "introduced_edits": 4981,
          "operational_failures": 2
        },
        "M2": {
          "tp": 834,
          "fp": 525,
          "fn": 7789,
          "precision": 0.6136865342163356,
          "recall": 0.09671807955467934,
          "F0.5": 0.2966071555587168,
          "introduced_edits": 1360,
          "operational_failures": 107
        },
        "M3": {
          "tp": 827,
          "fp": 393,
          "fn": 7796,
          "precision": 0.6778688524590164,
          "recall": 0.09590629711237389,
          "F0.5": 0.3062282455750574,
          "introduced_edits": 1221,
          "operational_failures": 103
        }
      }
    },
    "preservation_dassle": {
      "M1": {
        "introduced_edit_units": 2489,
        "unchanged_examples": 0,
        "N": 7381
      },
      "M2": {
        "introduced_edit_units": 340,
        "unchanged_examples": 6989,
        "N": 7316
      },
      "M3": {
        "introduced_edit_units": 252,
        "unchanged_examples": 7076,
        "N": 7320
      }
    },
    "retry_ablation": {
      "dassle": {
        "tp_delta": 7,
        "fp_delta": 132,
        "calls": 581
      },
      "dassle-preservation": {
        "tp_delta": 0,
        "fp_delta": 88,
        "calls": 395
      }
    }
  },
  "007m": {
    "roots": {
      "final": "007-m-rank-ambiguous-levenshtein-candidates-recovery.ec2962",
      "census": "007-m-rank-ambiguous-levenshtein-candidates-recovery.97f59c",
      "census_superseded_diagnostic": "007-m-rank-ambiguous-levenshtein-candidates-recovery.e6ca66",
      "failed_instrument": [
        "007-m-rank-ambiguous-levenshtein-candidates-recovery.ffdf13",
        "007-m-rank-ambiguous-levenshtein-candidates-recovery.090ea8"
      ]
    },
    "scheduled_total": 1917,
    "c1": 1035,
    "c_gt_1": 882,
    "c_gt_1_attempted": 866,
    "c_gt_1_uncertain": 16,
    "candidate_pairs": 4372,
    "unique_top": 882,
    "tied_top": 0,
    "reference_present": 408,
    "reference_absent": 474,
    "top_k_coverage_among_present": {
      "1": 247,
      "2": 349,
      "3": 376,
      "5": 399,
      "10": 408
    },
    "oracle": {
      "frozen_recall": 0.5425742574257426,
      "ceiling": 0.8118811881188119
    },
    "vocabulary_rows": 141162,
    "actual_experiment_calls": {
      "090ea8": 678,
      "ffdf13": 188,
      "total": 866,
      "final_root_new_calls": 0
    },
    "decisions": {
      "FAILURE": 87,
      "KEEP_ORIGINAL": 509,
      "UNCERTAIN": 16,
      "USE_CANDIDATE": 270
    },
    "accepted": {
      "exact_reference": 219,
      "non_reference": 51
    },
    "operational_failures": 87,
    "hybrid_composition": {
      "cases_with_c_gt_1_targets": 751,
      "winner_edits_applied": 270,
      "base_edits_removed": 158,
      "composition_conflict_rollbacks": 0,
      "new_calls": 0
    },
    "token_totals_inherited": {
      "input_tokens": 173422,
      "output_tokens": 393685,
      "reasoning_tokens": 388375
    }
  }
}
```
