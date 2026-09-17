# Work order 008-a — Qualify pulldown-cmark 0.13.4 as the structural prose boundary (falsification experiment)

Status: FINAL

Finalized by strategic reconciliation of 2026-09-17: verified independent
final-head review of 007-o at head 4a029287f27e038d5c34c39b26ca836be7c6914b
(private workorders/007-o-final-head-review-20260917.md), development-only
merge of PR #8 (merge commit 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9, second
parent the exact reviewed head), and post-merge main verification. The new PR
identity is not invented (CREATE_NEW_PR); it is created by the coding round.
All other content is finalized from the owner's 2026-09-17 research decision,
the owner-supplied Deep Research report, and independent candidate-precheck
evidence (private: workorders/008-a-candidate-precheck-20260917.md).

```oap-metadata
{
  "id": "008-a",
  "title": "Qualify pulldown-cmark 0.13.4 as the structural prose boundary",
  "objective": "008",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9",
  "branch": "oap/008-prose-boundary-qualification",
  "pr_mode": "CREATE_NEW_PR",
  "pr": null,
  "dependencies": ["007"],
  "local_work": "Preserve every merged 000-007 seam byte-for-byte, the merged research/ tree, all private experiment roots, and any unrelated local work.",
  "prior_review": "Strategic final-head review of 007-o (2026-09-17, private workorders/007-o-final-head-review-20260917.md): independently verified the report-only commit 4a029287f27e038d5c34c39b26ca836be7c6914b (sole parent f20bc5538de25cbafa455c7f89b2900381fe1057, changed path exactly oap/reports/007-o-consolidate-research-state.md), verify_report (remote) result verified, transcript valid with 007-n and 007-d both INVALID_QUARANTINED, consistency test 10/10 plus an independent tamper negative, all four required checks green at that head, whole-round diff in-scope with zero immutable-report mutations and zero model calls, and every RESEARCH-STATE.md machine-block number re-derived from the primary records. Development-only merge of PR #8 then executed at the exact reviewed SHA (merge commit 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9, second parent 4a029287f27e038d5c34c39b26ca836be7c6914b, PR state MERGED; all workflows are pull_request-triggered, so the merge carries no deployment side effect). Post-merge main verified: 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 carries the merged objective-007 research state and the 16 governance identities are byte-identical to the 007-o order block. Strategy precheck (2026-09-17, private workorders/008-a-candidate-precheck-20260917.md) independently verified the candidate identity: crates.io pulldown-cmark 0.13.4 (latest stable, not yanked, published 2026-05-20), registry cksum e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e, upstream pulldown-cmark/pulldown-cmark (main, tag v0.13.4), license MIT (crates.io version record, repository LICENSE file, crate Cargo.toml), MSRV 1.71.1, local rustc/cargo 1.75.0 present.",
  "provenance": [
    {"kind": "H", "reference": "Owner research decision 2026-09-17: protection research precedes linguistic confirmation; objective 008 researches, qualifies and, if justified, implements the prose/non-prose structural boundary before the effective pipeline is frozen and before objective 009 fresh human-labelled linguistic confirmation. Owner-supplied Deep Research report 'Reliable Prose Segmentation in Mixed LLM Output' (pulldown-cmark 0.13.4 leading candidate; markdown-rs 1.0.0 predefined challenger; Pandoc diagnostic only; tree-sitter-markdown rejected on maintainers' warning). Owner permits external CLI tools for this work. Full design parameters (fixture classes, coordinate invariant, dollar-math policy, challenger protocol, acceptance criteria, outcome states, report questions) are the owner's 2026-09-17 instruction, sections 5-23."},
    {"kind": "A", "reference": "PLAN.md v1.0 protection requirements (main capture precedes CPU detection; exact original spans; protected structures and boundaries); ARCHITECTURE.md v1.1 (protection layer, evidence layers section 16); S-PRODUCT-01/02/03, S-ORDER-01/02/03, S-EVIDENCE-01, S-DIAGNOSE-01; OAP communication profile sections 5-7."},
    {"kind": "E", "reference": "Merged objective-007 research state (research/RESEARCH-STATE.md): the protection layer is currently hand-written Markdown-sensitive regex logic; 007-m linguistic behaviour is frozen; no fresh linguistic confirmation exists; the structural boundary is the next research uncertainty. Post-merge main 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 (verified)."},
    {"kind": "I", "reference": "Strategy candidate precheck 2026-09-17 (private workorders/008-a-candidate-precheck-20260917.md): crates.io/sparse-index/GitHub identity, license evidence, MSRV, dependency set, tag v0.13.4, local toolchain 1.75.0; preserved real-output roots inventoried for the representative corpus (identity only, no content)."}
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
  "lr": ["LR-001", "LR-003", "LR-007", "LR-013", "LR-014"],
  "relevant_gates": [],
  "required_checks": ["Application baseline", "Research reproducibility", "OAP bootstrap acceptance", "OAP report history"],
  "decision_class": "D0"
}
```

## Identity

First round of new numeric objective 008, on a new branch
`oap/008-prose-boundary-qualification` and a new PR (CREATE_NEW_PR), based on the
post-merge main that contains the merged objective 007 research state. 008-a is a
bounded scientific/engineering **falsification experiment**, not production
integration:

> Does `pulldown-cmark` 0.13.4 provide sufficiently accurate, conservative and
> source-faithful structural segmentation of actual LLM-generated Markdown-like
> output to replace the Markdown-sensitive part of the current hand-written
> protection logic?

The round produces a durable, reproducible, data-safe record and an explicit
GO / CONDITIONAL GO / NO-GO decision for objective 008.

## Provenance

Owner-directed research sequencing (H) on the merged objective-007 closure (A/E),
with an independently prechecked candidate (I). The Deep Research report
narrows the candidate space but did not locally execute the Rust candidate on
our corpus; that missing empirical step is the primary purpose of 008-a.

## Current verified state

Verified by strategy 2026-09-17 from the remote:

- Remote `main` = `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9` (merge commit
  "Merge pull request #8 from ulfe-lmi/oap/007-concept-verification"; parents
  `ee2d1b479719009ff1d07829478f241e3f395f7c` and the exact reviewed 007-o head
  `4a029287f27e038d5c34c39b26ca836be7c6914b`). Equal to the runtime accepted
  reference at publication.
- PR #8: MERGED (mergedAt 2026-09-17T11:22:37Z, mergeSha
  `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9`). Objective 007 is closed; its
  research state is on main (`research/RESEARCH-STATE.md`, registry, reports,
  the 007-o order and report, both quarantines in the transcript).
- Branch `oap/007-concept-verification` remains at 4a02928 in history (not
  reused; 008 bases on main and uses its own new branch).
- No other open PR exists for objective 008; no 008 work has been started.
- 007-o final head review: complete (private
  `workorders/007-o-final-head-review-20260917.md`), including independent
  re-derivation of every RESEARCH-STATE.md machine-block number from primary
  records, the tamper negative, transcript/quarantine verification, and the
  development-only merge disposition with its strongest-argument record.

## Governance

S-PRODUCT-01/02/03, S-ORDER-01/02/03, S-EVIDENCE-01, S-DIAGNOSE-01,
S-DECIDE-01/02 govern. D0 research/engineering qualification inside architecture
and risk budget; no product mutation; no judgment debt expected (parser
selection flags, fixture layout, and command-line plumbing are reversible D0
details to be decided, tested, and recorded, not escalated).

## Goal and dependencies

Establish, with machine-checkable evidence, whether the parser's structural and
source-range contract holds for our use case, and classify what remains as a
bounded residual semantic problem. Depends on objective 007 (merged). Two
supervised increments with a strategy review gate between them: Increment 1
(core falsification) and Increment 2 (representative corpus and differential
evaluation), executed in separate reported increments of the same 008-a round
when the round is structured that way, or as one round with the predeclared
stop condition if Increment 1 fails.

## Scope

- Pin the exact candidate: `pulldown-cmark` version 0.13.4, crates.io registry
  checksum e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e,
  upstream pulldown-cmark/pulldown-cmark tag v0.13.4; record version, upstream
  identity, license evidence (MIT: crates.io version record, repository LICENSE,
  crate Cargo.toml), MSRV, and the exact installation mechanism in a machine-
  readable identity record.
- Begin with the existing upstream executable/event interface wherever
  practical (stock CLI on stdin). If the stock CLI cannot provide offset-level
  event/range output, build the smallest possible pinned measurement adapter
  (a throwaway Rust helper using `Parser::into_offset_iter()`, pinned to
  0.13.4) emitting stable JSONL lines such as kind/start_byte/end_byte/context.
  The adapter is explicitly a MEASUREMENT ADAPTER: it must be labeled as such in
  all artifacts, isolated from the application tree (research-only location),
  and must not be positioned as the future runtime interface.
- Increment 1 — core falsification, in order: (1) install/pin the candidate in
  a reproducible machine-local environment; (2) establish exact CLI/library
  identity (version string, checksum, tag); (3) run the difficult-case fixture
  suite; (4) verify event semantics; (5) verify exact source ranges; (6) verify
  UTF-8 behaviour; (7) inspect malformed-input recovery; (8) inspect math
  behaviour; (9) STOP for strategy review. If the fundamental source-range
  premise fails, stop the round and report NO-GO evidence; do not continue
  merely because work was planned.
- Build and freeze a project-authored, redistributable deterministic fixture
  suite covering at least these 38 classes: (1) plain Slovenian prose; (2)
  prose + inline code; (3) multi-backtick inline code; (4) prose + fenced
  Python; (5) tilde fences; (6) variable-length fences; (7) unfinished fenced
  code; (8) Markdown-looking material inside code; (9) mathematical-looking
  material inside code; (10) dollar-inline math; (11) dollar-display math;
  (12) paren-delimited TeX; (13) bracket-delimited TeX; (14) begin-end TeX
  environments (align); (15) malformed TeX; (16) paired dollar currency; (17)
  escaped dollar signs; (18) emphasis/strong containing prose; (19) heading
  containing prose; (20) list item containing prose; (21) blockquote containing
  prose; (22) Markdown link with prose label and URL destination; (23) image
  syntax; (24) autolink; (25) table containing both prose and inline code; (26)
  raw HTML; (27) bare JSON; (28) YAML/TOML/config-like material; (29) shell
  commands; (30) paths; (31) environment variables; (32) identifier-heavy
  tokens; (33) Slovenian c-caron/s-caron/z-caron (c/š/ž as UTF-8); (34) emoji;
  (35) decomposed Unicode combining sequences; (36) CRLF line endings; (37)
  malformed links; (38) mixed malformed Markdown/HTML/TeX. Expected structural
  safety semantics are frozen in the fixture file BEFORE any parser output is
  inspected; no parser-specific expectations may be added afterwards without a
  recorded strategy-approved rationale.
- Coordinate contract (hard invariant): for every parser range [start_byte,
  end_byte), original_utf8[start_byte:end_byte) must be the exact intended
  original source bytes; no range may bisect a UTF-8 code point; any mapping
  into Python character coordinates must be deterministic and exactly
  reversible for the span. Document: parser byte offsets vs Python code-point
  offsets, the conversion algorithm, its cost, invalid-boundary rejection, CRLF
  treatment, decomposed Unicode, and emoji/surrogate implications at external
  boundaries. A source-position failure is potentially disqualifying.
- Structural policy to test: candidate prose = parser Text leaves in paragraphs,
  headings, list items, blockquotes, table cells, link labels, and
  emphasis/strong content, provided they are not subsequently classified as
  machine-significant; structurally protected at minimum: inline code,
  fenced/indented code, recognized inline/display math, HTML, Markdown
  syntax/delimiters, link destination/title, metadata/front matter, and image
  structure by conservative default. Prose-bearing containers must expose their
  textual leaves (for example bold Slovenian prose keeps its words candidate
  while the Markdown punctuation stays protected); a link label may be prose
  while its URL destination is protected.
- Malformed input is a primary safety test: unfinished code fences, unmatched
  backticks, unmatched dollar signs, malformed links, incomplete HTML,
  malformed TeX, strange nesting, large spans, mixed constructs. Conservative
  false negatives (suppression) are generally preferable to false exposure of
  machine content, but each conservative behaviour is recorded as a tradeoff,
  not silently called correct.
- Dollar-math policy: test mathematical inline/display math, currency values,
  multiple currency values, escaped dollars, mixed prose, unmatched dollars,
  and actual dollar patterns observed in the representative corpus. Determine
  with evidence whether the parser math extension gives an acceptable
  safety/coverage tradeoff. Do not assume dollar-quotes mean math; do not
  invent a complicated rescue heuristic in this round; a material weakness is a
  valid challenger trigger.
- Increment 2 — only if Increment 1 is credible: (1) run the candidate over the
  authorized representative corpus; (2) compare its segmentation with the
  current hand-written protection implementation (differential A vs B); (3)
  classify every disagreement by consequence: parser correctly exposes
  over-protected prose / parser correctly protects previously exposed non-prose
  / parser falsely exposes machine-significant content / parser unnecessarily
  suppresses valid prose / source-coordinate mismatch / malformed-input safety
  difference / expected residual semantic category / unresolved needing
  inspection; (4) quantify residual categories; (5) trigger the challenger
  only on predefined material conditions; (6) reach an evidence-backed
  GO / CONDITIONAL GO / NO-GO conclusion.
- Representative real-output corpus (Increment 2): 50-200 representative real
  LLM outputs selected deterministically from already-preserved private
  research evidence (007-i/j/m roots and the preservation archive) WITHOUT new
  model generation and WITHOUT any future objective-009 confirmation examples.
  Retain privacy restrictions: raw text stays private; public reports carry
  counts/categories/hashes only; record source, population, and
  representativeness limitations. If the preserved outputs are overwhelmingly
  plain prose and cannot test the structural question, say so explicitly: keep
  the project-authored adversarial suite as the structural ground truth, use
  real outputs only for prevalence/disagreement observations, and record the
  limitation. Do not generate a new confirmation corpus without separate
  authorization.
- Differential evaluation: the success metric is NOT total protected
  characters. Report counts and data-free categories per consequence class;
  keep raw-text inspection private where required.
- Challenger protocol: `markdown-rs` 1.0.0 is the predefined primary challenger;
  trigger a bounded comparison ONLY if pulldown-cmark exhibits a material
  problem (incorrect or unusable source ranges; relevant GFM incompatibility;
  unsafe malformed-input handling; unacceptable math/currency behaviour;
  structural misclassification affecting actual Qwen output; or another failure
  markdown-rs plausibly addresses). Run the challenger on the exact failing
  fixtures, relevant representative cases, and enough controls to make the
  comparison meaningful. Pandoc may serve as an independent diagnostic oracle
  on disputed cases; it is not a runtime candidate. Do not revive
  tree-sitter-markdown absent materially new evidence contradicting the
  maintainers' warning.
- Predeclared acceptance criteria (frozen before the representative corpus
  runs): Hard - 100 percent exact source-range fidelity on the deterministic
  fixture suite; no range splits a UTF-8 sequence; structurally recognized code
  and math are never exposed as candidate prose; HTML/metadata protected per
  frozen policy; link destinations remain protected; prose-bearing Markdown
  containers still expose their textual leaves; malformed structural cases
  follow documented deterministic behaviour; no parse/re-render/
  reconstruction requirement; processing remains bounded and deterministic. A
  source-coordinate failure is an immediate NO-GO until explained and repaired
  upstream or through a trivial mapping layer. Safety - zero false exposures of
  protected machine content in the frozen adversarial suite for constructs the
  parser claims to recognize structurally. Coverage - avoid gross
  over-protection of ordinary prose in headings, lists, blockquotes, table
  cells, link labels, and emphasis/strong; report actual losses; set no
  arbitrary percentage. Residual - a GO requires that remaining
  machine-significant content exposed as ordinary Text falls into a bounded,
  comprehensible secondary-recognizer problem (paren/bracket TeX, selected TeX
  environments, bare JSON, YAML/TOML/config, shell, paths, environment
  variables, identifier-heavy tokens, dialect-missed URLs/autolinks), not
  evidence that the parser architecture is fundamentally unsuitable.
- Outcome states: GO (structural/source-range contract validated; residual
  gaps bounded and suitable for a second stage; strategy may then issue 008-b
  for the parser-first protection architecture); CONDITIONAL GO (core parser
  suitable, one or more bounded questions need a targeted follow-up, e.g.
  dollar-math policy or one GFM edge case; smallest corrective round); NO-GO
  (fundamental assumption fails: unreliable source spans, unsafe recovery on
  relevant constructs, unacceptable common-format failures, or the residual
  problem is not actually small; trigger the challenger path).
- Research artifacts (data-safe): frozen experiment configuration;
  candidate/upstream version identity; license identity; exact invocation
  recipe; fixture suite; expected fixture segmentation; deterministic
  evaluator; data-free aggregate result; differential comparison summary;
  representative-corpus selection receipt (counts/categories/hashes only);
  public research report; OAP order/report. No raw private LLM outputs in Git
  or public reports.
- The final research report must answer: (1) was the Deep Research
  recommendation empirically validated; (2) does pulldown-cmark give exact
  usable source ranges on our inputs; (3) which coordinate system will the
  application use; (4) which Markdown structures are solved structurally; (5)
  which constructs remain residual semantic cases; (6) what happens on
  malformed input; (7) what is the dollar-math decision; (8) how does it differ
  from current regex protection; (9) did any machine-significant content become
  falsely exposed; (10) how much valid prose was unnecessarily suppressed;
  (11) was the markdown-rs challenger triggered and why; (12) GO / CONDITIONAL
  GO / NO-GO; (13) exact recommendation for 008-b or the alternative next step.

## Non-goals

Frozen and out of scope: 007-m ranking; Levenshtein candidate semantics;
detector linguistic thresholds; corpus statistics; English suppression;
validator prompt; validator response parser; reasoning level; Qwen deployment;
retry policy; acceptance policy; linguistic benchmark scoring; any 007
historical result. No new scientific Qwen/model calls; no new data acquisition
beyond the deterministic selection from already-preserved outputs; no prompt
tuning; no production integration; no runtime wrapper/service (the measurement
adapter, if needed, is research-only and labeled); no Qwen/vLLM/CUDA/GPU/
service/network changes; no release or deployment; no merge of any PR from
this round; no rewriting of prior immutable orders/reports; no consumption of
any future objective-009 confirmation data; no claim that passing 008
establishes experimental-MVP linguistic acceptance. The existing regex
protection rules are classified later (008-b scope), not deleted here.

## Files and boundaries

Read/inspect: merged `research/` tree (RESEARCH-STATE.md, registry, reports),
the current protection implementation and its tests (to run the differential A
side), `PLAN.md` protection clauses, `ARCHITECTURE.md`, the private preserved
roots (identity/selection only, per privacy rules), crates.io/sparse-index/
GitHub records for the candidate (read-only network). Write: a new research-only
experiment subtree (frozen config, fixture suite, expected segmentation,
evaluator, selection receipt, aggregate results, report), the measurement
adapter (if required) in the same research-only location, the OAP order/active/
report paths, and the new PR. No application source changes.

## Requirements

1. Reconcile exact active 008-a, remote main (the post-merge head), no other
   open objective PR for objective 008, and all local work before mutation;
   create exactly one new PR for this objective.
2. Record the candidate identity (version, registry checksum, upstream
   repository and tag, license evidence, MSRV, dependency set, installation
   mechanism) in a machine-readable identity file committed with the round.
3. Freeze the fixture suite and its expected structural safety semantics
   (committed) BEFORE running the parser on them; no post-hoc parser-specific
   expectations without a recorded strategy-approved rationale.
4. Execute Increment 1 exactly in the predeclared order; at each failure,
   record the exact evidence; if the source-range premise fails, stop and
   report NO-GO evidence; otherwise present Increment 1 results for strategy
   review before Increment 2.
5. Verify the hard coordinate invariant on every fixture: byte-slice equality
   against the intended original bytes, no code-point bisection, and (where a
   Python mapping is demonstrated) deterministic exact reversibility; document
   CRLF and decomposed-Unicode behaviour.
6. If Increment 1 is credible, execute Increment 2 with the deterministic
   preserved-output selection (50-200 examples, receipt with
   counts/categories/hashes only, no raw text, no 009 examples, no new model
   calls) and the 8-class differential consequence report.
7. Trigger the challenger only per the predefined material conditions; record
   the trigger decision either way.
8. Apply the predeclared acceptance criteria and reach exactly one of GO /
   CONDITIONAL GO / NO-GO with the supporting evidence.
9. Run the Application baseline, Research reproducibility, OAP bootstrap
   acceptance, and OAP report history checks green at the final head; run the
   real `scripts/verify_development_baseline.py` entry point; no weakening,
   skipping, or redefinition of any check.
10. Publish one final report-only 008-a commit with the literal
    implementation head as sole parent and only the report path changed; verify
    remote head, report bytes, parent, and changed-path invariant; send response
    OK and stop. PR remains open and unmerged.

## Acceptance criteria

1. Candidate identity file present, exact (version 0.13.4, registry checksum,
   tag, MIT license evidence, MSRV, install mechanism).
2. Fixture suite committed before first parser execution; at least 38 classes;
   frozen expected semantics.
3. Hard coordinate invariant proven on all fixtures (byte-slice equality, no
   code-point bisection); CRLF and decomposed-Unicode documented.
4. Increment 1 results (event semantics, ranges, UTF-8, malformed recovery,
   math) recorded with data-free aggregates; strategy review gate passed
   before Increment 2.
5. Increment 2 (if executed): selection receipt, 8-class differential counts,
   residual category quantification, challenger trigger decision recorded.
6. Exactly one outcome state declared with evidence; the report answers all 13
   questions; no raw private text in any public artifact (publication guard
   passes).
7. All four required checks green at the final head; report-only commit
   invariant verified remotely; PR open/unmerged; no immutable prior
   order/report mutated.
8. Zero Qwen/model calls; zero new data acquisition; 009 data untouched; no
   linguistic tuning of the frozen 007-m system.

## Verification

Focused: the deterministic evaluator over the frozen fixture suite (positive:
exact expected segmentation semantics; negative: a deliberately corrupted
range/semantics fixture must be caught); the coordinate-invariant checker over
every emitted range; the differential evaluator's self-test on a controlled
synthetic pair. Broader: real `scripts/verify_development_baseline.py`
(including Application baseline); research test discovery; OAP suite;
transcript/governance/report-history/whitespace/protected-source diff/
`git fsck`; `verify_report` (local) on the 008-a report before push. Evidence
boundary: local commands at the literal implementation head plus the read-only
candidate-identity fetches; final-head GitHub checks awaited before the report;
no live model, no private data in public artifacts. Negative paths: corrupted-
range fixture failure; guard refusal of a planted private-path canary;
challenger trigger on a recorded material condition (if any); report-history
refusal if any prior report byte changed (must not occur).

## Local setup and constraints

CPU-only; machine-local Rust toolchain (rustc/cargo 1.75.0 present; MSRV
1.71.1 satisfied); pinned crate via registry checksum; no system-wide Rust
changes; no GPU/model/service access; no network beyond the read-only
candidate-identity fetches and normal GitHub publication; preserved private
roots read for deterministic selection and identity only; never print,
persist, or copy private text, prompts, responses, credentials, or private
paths into public artifacts; keep private absolute paths out of public
documents.

## Documentation

The research report and identity files must be readable by an independent
reviewer without access to private roots: every claim cites a committed record
(path plus SHA where material); the adapter (if any) is labeled a measurement
adapter, not a runtime interface; the report contains no production-readiness
or linguistic-quality claim and states explicitly that 009 remains reserved.

## Git and report publication

CREATE_NEW_PR on `oap/008-prose-boundary-qualification` from the post-merge
main. Commit non-report work (including the exact 008-a order and active bytes)
in one or more commits with truthful messages; wait for final-head CI; then one
report-only commit (SELF convention) with the literal implementation head as
sole parent and only `oap/reports/008-a-qualify-prose-boundary-parser.md`
changed; push; verify remote PR head, exact report bytes, parent, and
changed-path invariant; send exact response OK; stop. No merge, no auto-merge,
no subsequent push for this round.

## Decision classification

D0. Bounded research/engineering qualification; parser flags, fixture layout,
adapter shape, and command-line plumbing are reversible engineering details to
be decided, tested, and recorded in-round. No D2 boundary is crossed (no
protected resources, no deployment, no live linguistic claims).

## Deferred human adjudication
- Decision: NONE
