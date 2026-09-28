# Work order 008-c — Parser-first protection layer and generated structural corpus

Status: FINAL

Finalized by strategic review of 008-b (final head
49e4e70f1a8c304b4ad5ce27055a39e9e6e17288, all four required checks green at
that head, independently verified) and the explicit human research decision of
2026-09-17 received after 008-b publication: the 008-a GO is supporting
evidence for `pulldown-cmark` 0.13.4, not final independent validation of the
prose boundary, because (1) the 50-fixture adversarial suite was
parser-informed during working-tree authoring before its first committed
freeze, and (2) the 100 preserved real outputs were 100 percent plain prose
and did not exercise the mixed-content problem. The human authorizes LLM
calls strictly for structural test-data generation (not linguistic-method
tuning, and wholly separate from the future objective-009 confirmation set).
This is the third round of objective 008 on PR #9. It implements the
owner-prescribed parser-first structural protection architecture in the
research pipeline, builds the authorized generated mixed-content evaluation
program (frozen component-generation prompt library, deterministic mashup
corpus with machine-known ground truth, naturalistic whole-response corpus,
mandatory development/hidden split with a sealed hidden acceptance set), and
freezes the implementation before any hidden-set evaluation. The hidden
acceptance itself is the next round (008-d). No linguistic-method tuning of
any kind occurs in this round; the frozen 007-m linguistic system is
untouched.

```oap-metadata
{
  "id": "008-c",
  "title": "Parser-first protection layer and generated structural corpus",
  "objective": "008",
  "status": "FINAL",
  "phase": "DEMONSTRATOR",
  "repository": "ulfe-lmi/llm-slovenian-repair",
  "default_branch": "main",
  "base_sha": "49e4e70f1a8c304b4ad5ce27055a39e9e6e17288",
  "branch": "oap/008-prose-boundary-qualification",
  "pr_mode": "AMEND_EXISTING_PR",
  "pr": 9,
  "dependencies": ["008"],
  "local_work": "Preserve byte-for-byte: every merged 000-007 seam on main, the entire research/ tree at the 008-b final head (including the frozen 008-a baseline under research/prose-boundary/: config/experiment-008a.json, fixtures/, results/increment1/, results/increment2/, REPORT.md, adapter/ source, identity/), the 008-b research-state files as the additive-update base, all private experiment roots, the existing research test suite byte-for-byte (this round adds exactly one new focused test file and changes no existing test file), and any unrelated local work (including untracked .research-test-scratch/).",
  "prior_review": "Strategy independent final-head review of 008-b (2026-09-17, private workorders/008-b-final-head-review-20260917.md): report-only commit 49e4e70 (sole parent 8300573, sole changed path oap/reports/008-b-post-merge-research-state-identities.md); verify_report remote=verified (report history valid, 2 frozen incidents, report_count 46); transcript valid (active=latest=008-b); round diff 8dbb79a..49e4e70 = exactly 6 files (order, active, report, RESEARCH-STATE.md, registry, CSV) with zero test changes, zero src/ changes, zero 008-a baseline changes; RESEARCH-STATE re-derived line-for-line (5 block fields, section 16 statements (a)-(h), single 4.2 heading); registry 25 entries with the 008-a entry's 9/9 evidence sha256+size pairs re-verified against committed blobs; rebuild_tables --check PASS; all four required CI checks independently confirmed green at 49e4e70 (Application baseline run 35249363947, OAP acceptance+history run 35249363933, Research reproducibility run 35249363954); implementation-head red checks failed solely on the designed pre-report count assertion (613 passed, 1 failed); zero model calls and zero parser runs in the round; response OK received; PR #9 open/unmerged, main still 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9.",
  "provenance": [
    {"kind": "H", "reference": "Human research decision 2026-09-17 (received after 008-b publication): (1) 008-a GO is useful supporting evidence for pulldown-cmark 0.13.4 but NOT sufficient final independent validation of the prose boundary, due to pre-freeze parser-informed fixture authoring and a structurally unrepresentative (100 percent plain prose) preserved real-output sample; (2) LLM calls are authorized specifically for generating structural test material - test-data generation, not linguistic-method tuning, wholly separate from objective 009's future confirmation set; (3) objective 008 must produce a much stronger acceptance corpus: a deterministic mashup corpus with machine-known exact ground truth (thousands of documents from hundreds of independently generated components across dozens of prompt families, Slovenian mixed content) plus a naturalistic whole-response LLM corpus (100-300 examples) with independently derived labels; (4) mandatory development/hidden split - the hidden acceptance set's case contents and labels must remain unavailable to the implementation agent until the implementation is frozen, sealed by hash/manifest before implementation finalization, preferably generated independently, controlled by strategy or an independent evaluation process; (5) 008-c implements the parser-first architecture and residual semantic layer, builds/freezes the corpus, adds development tests, and freezes the implementation; 008-d performs blind hidden acceptance, naturalistic evaluation, end-to-end preservation tests, and the final objective-008 disposition (PASS/CONDITIONAL/FAIL); (6) do not restart parser selection absent falsifying evidence; markdown-rs remains challenger-only under the predefined trigger; (7) do not ask the human to choose seeds, filenames, schemas, subprocess details, or prompt numbering."},
    {"kind": "A", "reference": "research/prose-boundary/config/experiment-008a.json (frozen structural policy, PROSE/NON_PROSE container sets, P2 profile, coordinate contract, differential consequence classes 1-8, challenger protocol); research/prose-boundary/identity/candidate-identity.json (pinned pulldown-cmark 0.13.4, registry checksum e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e, tag v0.13.4, MIT, adapter binary sha256 5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf); research/curated/protected.py (current protection contract: Interval, is_protected, protected_intervals and every consumer); research/curated/pipeline.py, detector.py, patching.py (end-to-end invariants 1-7 boundaries); research/curated/transport.py and concept-verification/qwen_client.py (authorized private-endpoint generation mechanism, env-credential based); PLAN protection clauses (main capture precedes detection; protected boundaries; exact original spans; every unapproved slice preserved); S-PRODUCT-01/02/03, S-ORDER-01/02/03, S-EVIDENCE-01 (fakes outside the tested boundary), S-DIAGNOSE-01, S-DECIDE-01/02; CRITICAL.md register rules section 1 (five-condition D1 admission)."},
    {"kind": "E", "reference": "008-a final head 8dbb79a20f129d4c07c6b94827cacad74683ba6b (GO; 50 fixtures x 3 profiles, 1,288 events, 0 coordinate violations, 0 exposures under the documented D0 autolink rule, 0 missing prose bytes; 100-sample differential: 22 class-7 spans, 0 safety-class; challenger NOT_TRIGGERED; both methodological limitations now explicitly recognized per the human decision); 008-b final head 49e4e70f1a8c304b4ad5ce27055a39e9e6e17288 (identities corrected: main_sha=reviewed_branch_head_sha=7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9, parent 4a029287f27e038d5c34c39b26ca836be7c6914b, registry 25 entries, oap_reports_reviewed=45; all four checks green); strategy finding B (config literal candidate_rule omits the D0 autolink-destination rule; resolved in this round by a new v2 config, experiment-008a.json untouched)."},
    {"kind": "I", "reference": "Strategy independent final-head reviews of 008-a (private workorders/008-a-final-head-review-20260917.md: full scientific re-derivation, findings A and B) and 008-b (private workorders/008-b-final-head-review-20260917.md: identity chain, report-only invariants, all-four-green verification, zero model calls)."}
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

Third round of objective 008, amending the objective-008 branch
`oap/008-prose-boundary-qualification` and PR #9. 008-a (frozen head
8dbb79a20f129d4c07c6b94827cacad74683ba6b) qualified `pulldown-cmark` 0.13.4
with outcome GO; 008-b (final head 49e4e70f1a8c304b4ad5ce27055a39e9e6e17288)
restored the post-merge research-state identities and registered 008-a in the
ledger. The human decision of 2026-09-17 reclassifies the 008-a GO: it
remains valid as the historical round result and as supporting evidence for
the candidate parser, but independent mixed-format acceptance is now required
before the protection layer is trusted. This round therefore does two things
in one bounded objective-008 suffix:

1. implements, in the research pipeline only, the owner-prescribed
   parser-first architecture:

   raw immutable UTF-8 response -> pulldown-cmark structural parse with
   original-source ranges -> parser-derived candidate Text regions -> narrow
   residual semantic protection layer -> final eligible prose spans -> frozen
   007-m linguistic pipeline;

2. builds and freezes the authorized generated structural evaluation program:
   a frozen component-generation prompt library, LLM-generated component
   pools (Slovenian prose, code, structured data, math/TeX, Markdown
   structures, machine-significant fragments, malformed fragments), a
   deterministic mashup builder that composes thousands of final documents
   with machine-known exact ground-truth interval maps, a naturalistic
   whole-response corpus, and the mandatory development/hidden split with a
   hash-sealed hidden acceptance set.

The implementation is frozen at this round's final head. The hidden
acceptance evaluation, naturalistic label adjudication, end-to-end
preservation verification on the hidden set, and the final objective-008
scientific conclusion (PASS/CONDITIONAL/FAIL) are the next round (008-d).
This is bounded D0 engineering plus explicitly authorized bounded test-data
generation. It is not production integration, not a linguistic experiment,
and not a change to the frozen 007-m linguistic system.

## Provenance

- H: Human research decision 2026-09-17 (full text summarized in the
  metadata provenance): 008-a evidence standing and its two recognized
  limitations; authorization of LLM calls for structural test-data
  generation only; the two-layer corpus requirement (deterministic mashups
  with machine-known ground truth + naturalistic whole-response outputs);
  the mandatory dev/hidden split with sealed hidden acceptance; the 008-c
  vs 008-d responsibility split; the final decision states PASS/CONDITIONAL/
  FAIL; 009 remains separate and untouched; documentation must stay
  truthful (PR #8 merged; generated structural corpus tests structural
  safety, not repair quality); the owner is not to be asked routine
  reversible engineering details.
- A: 008-a frozen config and candidate identity (pinned parser, policy,
  coordinate contract, consequence classes, challenger protocol); the
  current protection contract and its consumers in `research/curated/`; the
  end-to-end pipeline seams (`pipeline.py`, `detector.py`, `patching.py`)
  for the seven end-to-end invariants; the authorized private-endpoint
  generation mechanism (`concept-verification/qwen_client.py` env-credential
  pattern, same deployment class as the 007 research); PLAN protection
  clauses; CRITICAL.md register rules (five-condition D1 admission).
- E: 008-a final head (GO; both limitations now explicitly recognized) and
  008-b final head (identities corrected; all four checks green), both
  independently reviewed by strategy (private receipts); strategy finding B
  (D0 autolink rule absent from the 008-a config literal rule text).
- I: Strategy independent final-head reviews of 008-a and 008-b (private
  workorders/008-a-final-head-review-20260917.md,
  workorders/008-b-final-head-review-20260917.md).

## Current verified state

Verified by strategy at publication (this session, from remote and primary
records):

- main remains `7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9` (development-only
  merge of PR #8); objective 007 closed.
- PR #9 OPEN / UNMERGED / MERGEABLE, auto-merge disabled, head
  49e4e70f1a8c304b4ad5ce27055a39e9e6e17288 (the 008-b final head); all four
  required checks green at that head, independently confirmed via GitHub.
- 008-a GO stands as the historical round result; its two methodological
  limitations (parser-informed pre-freeze fixture authoring; 100 percent
  plain-prose preserved real-output sample) are now explicitly recognized by
  the human decision; the 008-a REPORT.md and all 008-a artifacts remain
  immutable and byte-identical.
- 008-b complete: machine block main_sha = reviewed_branch_head_sha =
  7d2cc9ee..., reviewed_branch_head_parent_sha = 4a02928..., registry 25
  entries, oap_reports_reviewed = 45.
- `STATUS.md` is materially stale in one place: its objective-007 paragraph
  still says "PR #8, open and unmerged". Corrected in this round (scope item
  11).
- The 007 research used the private research endpoint through the existing
  env-credential mechanism (`concept-verification/qwen_client.py`;
  deployment class A100-FP8 Qwen per the 007-m config lineage). Live
  endpoint availability is NOT asserted here: it is established by the
  bounded single-call preflight in requirement 3, and the observed
  model/profile identity is recorded in this round's generation identity
  receipt. If the preflight fails, generation is BLOCKED and reported -
  never faked with local text.

## Governance

S-PRODUCT-01/02/03 (protection boundaries; exact original code-point spans;
every unapproved slice preserved; no second large GPU model; shared GPU and
endpoint protected; no raw private text in public artifacts), S-ORDER-01/
02/03, S-EVIDENCE-01 (distinct evidence states; fakes placed outside the
tested boundary; truthful per-head check recording), S-DIAGNOSE-01,
S-DECIDE-01/02. D0 overall: bounded, reversible engineering inside the
experimental research pipeline plus explicitly human-authorized bounded
test-data generation. One recorded D1 provisional judgment (the hidden-set
seal mechanism in this single-workspace environment) is assessed in the
Decision classification section against the five CRIT admission conditions;
admission is not triggered (condition 1: the human decision of 2026-09-17
resolves the substantive issue; the remaining choice is reversible
engineering mechanics), so no CRIT entry is created.

## Goal and dependencies

Implement the parser-first structural protection architecture with a narrow
residual semantic layer, and produce the authorized generated mixed-content
evaluation program (component library, deterministic mashups with
machine-known ground truth, naturalistic whole-response corpus, sealed
hidden acceptance set) so that 008-d can perform a blind, independent
structural acceptance of the frozen implementation and issue the final
objective-008 conclusion. Passing the dev corpus in 008-c is tuning evidence
only; it is never presented as acceptance.

Dependencies (all satisfied and verified): 008-a (GO evidence, pinned
candidate, frozen baseline, committed adapter source), 008-b (consistent
state, ledger registration, green checks). No other dependencies.

## Scope

Exactly:

1. `research/curated/prose_boundary.py` (NEW): pinned-helper invocation,
   JSONL protocol parsing, byte<->code-point coordinate mapping with
   fail-closed invalid-boundary rejection, structural policy v2 evaluation,
   the fail-closed legacy fallback, and the residual semantic recognizers
   (scope item 2) applied only to parser-approved candidate-prose spans.
2. Residual semantic recognizer design (frozen in scope item 10): a narrow
   content-level recognizer operating ONLY on candidate-prose text, for the
   residual classes: `\(...\)`, `\[...\]`, selected TeX environments
   (equation/align/aligned and similar), bare JSON/YAML/TOML/XML/INI/
   config-like text, shell/terminal commands and flags, POSIX/Windows paths,
   environment variables, identifiers, machine-significant numbers with
   short units, and bare URLs missed by the parser dialect. It must NOT
   reparse Markdown structure, code, parser-recognized math, HTML, or
   metadata, and must not contain Markdown-delimiter regexes (it is not a
   second Markdown parser).
3. `research/curated/protected.py` (REWORKED): Markdown-syntax rules become
   parser-derived intervals; surviving semantic rules run only on
   candidate-prose spans in code-point coordinates with unchanged semantics;
   public signatures `Interval`, `is_protected`, `protected_intervals`
   unchanged for all consumers; the legacy full-regex path retained,
   clearly marked, used only as the documented fail-closed fallback.
4. `research/prose-boundary/config/structural-policy-v2.json` (NEW): the
   complete corrected policy (scope item 9). `research/prose-boundary/config/
   experiment-008a.json` is NEVER edited (byte-identical; registry-cited SHA
   must still match).
5. Generation program, committed under `research/prose-boundary/config/
   generation/` (frozen prompt library + generation identity + call
   accounting) and `research/prose-boundary/tools/generation_driver.py`
   (NEW, bounded driver with receipts):
   - `prompt-families.json`: the frozen component-generation prompt library
     (scope item 11): 76 prompt families across the seven component
     categories, each with exact prompt text, category, per-family sample
     count, generation parameters (model/profile, temperature, max tokens),
     and the deterministic sampling plan.
   - `generation-identity.json`: generator identity (endpoint class,
     model/profile as recorded, call budget vs actual calls, batch plan,
     retry policy, parameter set), committed data-free (counts/hashes/
     identities only; no raw outputs).
6. `research/prose-boundary/tools/prose_boundary_builder.py` (NEW): the
   deterministic mashup builder - composes final documents from the frozen
   component pools using a documented seeded PRNG, layout templates, and
   multi-layer interaction patterns (scope item 12); emits, for every
   document, a machine-readable ground-truth interval map (byte ranges +
   code-point ranges + component provenance IDs + expected category per
   region) derived purely from composition provenance. No parser output may
   participate in label construction (enforced structurally: the builder
   never invokes the parser or the protection layer).
7. Dev corpus, committed: `research/prose-boundary/corpus/components-dev/`
   (JSONL component pools), `corpus/documents-dev/` (3,000 assembled
   documents), `corpus/labels-dev/` (ground-truth interval maps),
   `corpus/naturalistic-dev/` (naturalistic responses used for development
   observation), `corpus/manifests/corpus-census.json` (counts, category
   distributions, byte totals, per-file sha256).
8. Hidden acceptance set, sealed: generated independently (separate seed
   streams and separate prompt instances of the same frozen families),
   written ONLY to the private research runtime root under
   `008c-hidden/` (components, 2,000 assembled documents, label maps,
   naturalistic hidden responses); committed as
   `research/prose-boundary/corpus/manifests/hidden-manifest.json`
   (case IDs, per-file sha256 and sizes for every hidden case file and label
   file, component provenance IDs, seed identities, generator identity,
   census - NO content). The manifest is committed and hash-verified BEFORE
   the implementation is frozen (scope item 13). The private-root seal copy
   is hash-identical to the committed manifest.
9. Focused tests: one new file
   `research/tests/test_parser_first_protection.py` (coordinate mapping,
   protocol tamper, policy v2, residual recognizers per class, fail-closed
   fallback, determinism, end-to-end invariants 1-7 on dev documents,
   single-assertion planted negatives). Existing test files remain
   byte-identical.
10. Differential regression + dev-corpus evaluation, committed data-free
    aggregates under `research/prose-boundary/results/increment3/`:
    (a) the 008-a 50-fixture baseline re-derived through the new runtime
    path (zero coordinate violations, zero protected-region exposures under
    policy v2, zero missing prose bytes); (b) dev-corpus safety/coverage/
    coordinate metrics per scope item 14; (c) differential of new protection
    vs legacy protection on the 008-a 100-sample receipt corpus (same
    consequence classes 1-8; the 22 class-7 spans remain protected by the
    second stage; no class-3 safety regressions); (d) end-to-end invariants
    1-7 results; (e) performance measurement (scope item 15). Dev-corpus
    failures are tuning findings: they may be fixed within this round and
    re-measured; they are NEVER acceptance evidence.
11. Prompt library content (frozen before any generation call): 76 families -
    16 Slovenian prose topic families (science, history, everyday advice,
    computing, cooking, travel, education, engineering, neutral medicine
    explanation, sports, literature, administration, statistics,
    mathematics, electronics, programming explanation; 25 fragments each,
    400 total, varying sentence/paragraph length, register, punctuation,
    Unicode incl. č/š/ž, quotations, parentheticals); 7 code families
    (Python, C, C++, JavaScript, shell/Bash, SQL, and one further common
    language; ~22 fragments each, 154 total, incl. Slovenian comments,
    Markdown-looking string literals, backticks, dollar signs, braces,
    URLs, paths, Slovenian-resembling identifiers, non-ASCII); 8 structured-
    data/config families (JSON, YAML, TOML, XML, HTML, INI-like, env-var
    blocks, key/value snippets; 15 each, 120 total); 12 math/TeX families
    (inline `$...$`, display `$$...$$`, `\(...\)`, `\[...\]`, equation,
    align, aligned, matrices, fractions, summations, probability,
    `\text{...}` with Slovenian prose-like words; 12-13 each, 150 total);
    13 Markdown-structure families (headings, emphasis, strong,
    strikethrough, lists, nested lists, blockquotes, tables, links, images,
    autolinks, task lists, inline code, fenced/tilde/variable-length fences,
    raw HTML; ~15 each, 200 total); 10 machine-significant families (POSIX
    paths, Windows paths, shell commands, command-line flags, environment
    variables, filenames, URLs, email addresses, identifiers, version
    strings, numbers with units; 15 each, 150 total); 10 malformed families
    (unclosed fence, unmatched backtick, unmatched `$`, incomplete `$$`,
    incomplete `\(`/`\[`, unclosed TeX environment, broken link, partial
    HTML, truncated JSON, malformed nesting; 6 each, 60 total). Total 1,234
    components across 76 families. The prose is varied topical text, not
    specially optimized to interact with the parser.
12. Mashup composition: 5,000 final documents total (3,000 dev / 2,000
    hidden), 2-10 components each, 200-4,000 bytes each, seeded PRNG
    (documented seed per set), layout templates including at least: PROSE +
    INLINE_CODE + PROSE; PROSE + DISPLAY_MATH + PROSE; PROSE + FENCED_CODE +
    PROSE; HEADING(PROSE) + PROSE + TABLE(PROSE,CODE); LIST(PROSE,
    INLINE_CODE, PROSE); PROSE + LINK(PROSE_LABEL, URL) + PROSE; PROSE +
    JSON + PROSE + LATEX; BLOCKQUOTE(PROSE + INLINE_CODE) + FENCED_CODE;
    PROSE + MALFORMED_STRUCTURE + PROSE; plus randomized compositions.
    Guaranteed minimum counts per corpus (census-verified) for multi-layer
    interactions: Markdown-looking syntax inside code; TeX delimiters inside
    code; backticks inside strings; currency dollars adjacent to real math;
    Slovenian comments in code; Slovenian strings inside JSON; Markdown
    inside JSON strings; `\text{slovensko}` in math; URLs inside code; paths
    in Markdown tables; code in lists; links in blockquotes; inline code
    adjacent to punctuation; emoji and č/š/ž; decomposed Unicode; CRLF;
    adjacent protected regions; protected region at document start/end.
13. Naturalistic corpus: 150 whole-response Slovenian LLM outputs from 15
    scenario families x 10 (explain an algorithm in Slovenian with Python
    code; Slovenian explanation + Markdown table + equations;
    troubleshooting with shell commands and paths; explain a JSON
    configuration in Slovenian; Markdown documentation with links, lists,
    fenced code; Slovenian math answer with inline and display LaTeX;
    comparison table with code fragments; intentionally incomplete/malformed
    Markdown; five further mixed-documentation scenarios chosen by strategy
    from the owner's examples list and recorded in the prompt library).
    Split 80 dev / 70 hidden (hidden responses generated with separate
    scenario instances, written only to the private root, hash-sealed in the
    hidden manifest). Labels for the naturalistic set are NOT built in this
    round: 008-d adjudicates them independently from the frozen annotation
    guide (scope item 16). This round records only the raw responses (hash
    manifest) and the frozen annotation guide.
14. `research/prose-boundary/config/structural-policy-v2.json` content
    (frozen by strategy, D0, before implementation):
    1. Profile P2 (ENABLE_TABLES | ENABLE_STRIKETHROUGH | ENABLE_TASKLISTS
       | ENABLE_MATH | ENABLE_YAML_STYLE_METADATA_BLOCKS), identical to the
       008-a P2 profile.
    2. Candidate prose: a parser Text event is candidate prose iff its
       open-tag ancestor set intersects PROSE_CONTAINERS and does not
       intersect NON_PROSE_CONTAINERS, with the two 008-a implementation
       rules carried unchanged into the runtime: D1 token-family matching
       (a family entry matches its own token or any level-suffixed token)
       and the D0 autolink-destination rule (the only S.Link whose original
       source slice starts with byte `<` is an autolink; its inner Text
       leaf is the destination and is PROTECTED). PROSE_CONTAINERS and
       NON_PROSE_CONTAINERS are exactly the 008-a sets.
    3. Strikethrough/superscript/subscript content REMAINS EXPOSED (open
       008-a policy item resolved: these wrap prose, not machine content).
    4. Images (including alt text) REMAIN PROTECTED (open 008-a policy item
       resolved: conservative default; revisit only with future evidence).
    5. Residual recognizers run only over candidate-prose spans, code-point
       coordinates, per scope item 2.
    6. Coordinate contract: byte<->code-point mapping
       (`cp = len(bytes[:s].decode('utf-8'))`; inverse
       `byte = len(text[:cp].encode('utf-8'))`); any bounds or UTF-8
       boundary failure is rejected fail-closed (legacy fallback), never
       repaired by guessing; `original_utf8[start:end)` must be the exact
       intended source bytes; no range bisects a code point.
    7. Fail-closed fallback: helper unavailable / non-zero exit / timeout /
       malformed or truncated protocol -> legacy full-regex protection with
       the fallback reason recorded; never fail open.
    8. Determinism: identical input bytes -> identical protected-interval
       bytes.
15. Dev-corpus metrics reported in `results/increment3/` (tuning evidence,
    clearly labeled as such): safety - protected bytes exposed as prose
    (target 0), protected regions with any overlap into candidate prose
    (0), machine-significant component exposure rate (0 for structurally
    known material), malformed-structure unsafe exposure rate (per frozen
    policy: policy-decided suppression is not a violation; exposure of
    policy-protected machine content is); coverage - expected prose bytes
    exposed (target 100 percent of construction-labeled prose), expected
    prose regions completely available, unnecessary suppression by
    container type (actual losses reported, no arbitrary threshold);
    coordinates - UTF-8 boundary violations (0), byte/code-point conversion
    mismatches (0), source slice mismatches (0); residual-recognizer
    performance broken down by class (TeX; JSON/config; shell; paths;
    identifiers; numbers/units; URLs; other); malformed-input deterministic
    behaviour table; performance - parser + residual latency on
    representative documents at ~1KB, ~10KB, ~50KB (ms/document, peak RSS;
    qualitative statement only that this is cheap relative to model
    inference - no inference latency is measured in this round).
16. `research/prose-boundary/config/annotation-guide.json` (NEW, frozen):
    the naturalistic-label annotation guide for 008-d - the category
    vocabulary (genuine prose; structural protect; machine-significant
    residual; delimiter/whitespace neutral; ambiguous), the decision
    procedure written without reference to any implementation, the
    ambiguity labelling rule (explicit AMBIGUOUS label, no forced
    certainty), and the reconciliation rule for independent review.
17. Documentation corrections: `STATUS.md` objective-007 paragraph corrected
    (PR #8 development-only merged 2026-09-17, merge commit 7d2cc9ee...;
    objective 007 closed) plus a short new objective-008 paragraph (008-a
    supporting GO with its two recorded limitations; 008-b identities;
    008-c parser-first implementation and generated structural corpus in
    progress; the generated corpus tests structural safety, not Slovenian
    repair quality). `research/RESEARCH-STATE.md` additive note (scope item
    18). No 007 narrative rewrite.
18. `research/RESEARCH-STATE.md`: machine block additive update (registry_
    entries 25 -> 27, oap_reports_reviewed 45 -> 46; main_sha,
    reviewed_branch_head_sha, reviewed_branch_head_parent_sha,
    quarantined_007n, frozen_007m_* fields UNCHANGED - if live origin/main
    has moved from 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 at
    implementation time, STOP and report BLOCKED); plus one additive
    section recording: the human decision of 2026-09-17 (008-a
    reclassification; generated corpus program; dev/hidden split; 008-d
    hidden acceptance); the 008-c change summary (parser-first layer,
    residual recognizer, corpus census, sealed hidden manifest identity,
    dev-corpus tuning results with the explicit label that they are not
    acceptance).
19. `research/registry/experiments.json`: add the exact 008-b entry and the
    008-c entry (scope item 20); replace the scope string exactly with:
    `all enumerated experiment and recovery roots plus stable child runs/phases, non-benchmark diagnostics, the 008-a parser-qualification study, the 008-b post-merge state repair, and the 008-c parser-first protection implementation and generated structural corpus (committed data-free subtree)`.
20. `research/tables/experiment-summary.csv` regenerated by
    `research.tools.rebuild_tables` (byte-identical to tool output, verified
    with `--check`).
21. `research/prose-boundary/REPORT-008C.md` (NEW; the 008-a REPORT.md is
    never edited) and the OAP report
    `oap/reports/008-c-parser-first-protection.md` (report-only final
    commit).

### Interface decision (D0, decided by strategy)

A single pinned subprocess helper per document: the 008-a measurement
adapter source (`research/prose-boundary/adapter/`, committed, pinned by
Cargo.lock and registry checksum e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e,
008-a-recorded binary sha256 5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf),
reused or rebuilt at the machine-local private research runtime root (same
convention as 008-a; presence verified by sha256, rebuild from committed
source if absent). Invoked as `<helper> P2 < document` emitting the
deterministic JSONL event protocol. The stock CLI remains a diagnostic
cross-check only (008-a precedent). No service, no process pool, no
Rust-in-Python binding. Label transition recorded in REPORT-008C.md: the
008-a README's "MEASUREMENT ADAPTER" label described round 008-a; in 008-c
the identical pinned source and protocol are adopted as the research
pipeline's structural helper (only the new module docstring label changes;
the 008-a README is immutable history).

### Generation-model policy (D0, decided by strategy)

All generation calls use the existing authorized private research endpoint
(env-credential mechanism per the 007 lineage; deployment class A100-FP8
Qwen as recorded in the 007-m config lineage), so that at least the
naturalistic corpus - and in fact the whole generation program - comes from
the intended Qwen family, whose formatting habits are operationally
relevant, with a single pinned generator identity for auditability.
Diversity comes from the 76 frozen prompt families and the recorded
parameter set, not from unrecorded model switching. If the coding agent
finds a second authorized generator trivially available, it MAY use it for
part of the component pool with separately recorded identity (permitted, not
required); the default is the single pinned Qwen endpoint. Hard call budget:
400 generation calls total (component batches <= 250; naturalistic <= 150;
retry policy: at most one retry per failed call, all failures and retries
recorded in generation-identity.json). Actual call counts, model/profile
identity, prompts, parameters, seeds and batch plan are committed in the
generation identity receipt. Generated corpus content is structural test
data: it is NOT objective-009 data, may never be represented as fresh 009
confirmation evidence, and is not linguistic-method tuning data.

### Dev/hidden split and hidden-seal mechanics (recorded D1 judgment)

The hidden acceptance set is generated independently (separate seed streams,
separate prompt instances), written only to the private research runtime
root under `008c-hidden/`, and sealed before the implementation is frozen:
`corpus/manifests/hidden-manifest.json` (committed) carries case IDs,
per-file sha256 and sizes for every hidden case file and label file,
component provenance IDs, seed identities, generator identity and census -
no content. The 008-d round reads the private root, verifies every file
against the committed manifest hashes, and evaluates the frozen
implementation; any mismatch voids the acceptance and is a
corrective-sequencing event. Order-mandated procedure inside 008-c: the
generation driver writes hidden components/cases/labels directly to the
private root and never prints hidden case contents or label contents into
the model's context (driver contract test: hidden files are created with
no echoed content in stdout logs; the driver's stdout carries counts and
hashes only); after the hidden manifest commit, the coding agent's
development tooling may reference hidden-set files only through their
manifest hashes (no content reads), and the development evaluation tool
reads only the dev corpus. Residual risk recorded honestly: in this
single-workspace environment the implementation agent's user account can in
principle read the private root; the mitigations are (a) procedural
prohibitions in this order and in the 008-d order, (b) frozen hashes
verified by strategy at both the 008-c and 008-d final-head reviews, (c)
008-d being a separate round in which the implementation is frozen (no
implementation changes permitted) and whose evaluation is independently
verified by strategy, and (d) the naturalistic labels being derived in
008-d without consulting the implementation under test. This mechanism is a
recorded D1 provisional judgment (Decision classification section); the
five CRIT admission conditions are not all met because condition 1 fails:
the human decision of 2026-09-17 resolves the substantive issue (seal the
hidden set, freeze by hash, keep it unavailable to the implementation
agent, strategy-controlled), leaving only reversible engineering mechanics
for this environment.

## Non-goals

Frozen and out of scope: all 007-m linguistic behaviour (detector
thresholds, candidate generation, ranking, validator prompt/parser,
reasoning level, Qwen deployment configuration, retry, acceptance,
benchmark scoring); any linguistic-method tuning of any kind; any
re-scoring or reinterpretation of 007 historical metrics as if the new
protection existed historically; objective 009 in any form (no 009 data
touched, no 008-generated sample may later serve as 009 confirmation
evidence); the hidden-set evaluation itself (008-d); production
integration, release, deployment; merge or auto-merge of PR #9;
Qwen/vLLM/CUDA/GPU configuration changes (the generation calls use the
existing endpoint only, within the recorded budget); new data acquisition
beyond the authorized generation program; modifying the frozen 008-a
baseline files; modifying `oap/orders`, prior reports,
`oap/REPORT-HISTORY-INCIDENTS.json`, or any immutable record; changes under
`src/` (application), `oap/bin/`, or existing research test files;
restarting parser selection (pulldown-cmark 0.13.4 remains the selected
structural parser unless new evidence falsifies it; markdown-rs is
challenger-only under the predefined 008-a trigger conditions); building
the residual layer into a general Markdown parser (scope item 2
prohibitions); any claim that passing the dev corpus is acceptance,
experimental-MVP linguistic acceptance, or release readiness.

## Files and boundaries

Read/inspect: `research/prose-boundary/` (008-a baseline, read-only),
`research/curated/` (protection + all consumers), `research/tests/`
(existing tests, read-only), `concept-verification/qwen_client.py`
(generation endpoint mechanism), PLAN protection clauses, ARCHITECTURE,
008-a REPORT.md, 008-b OAP report, the private research runtime root
(helper location convention; new `008c-hidden/` subtree).

Write (exactly): `research/curated/prose_boundary.py` (new),
`research/curated/protected.py` (rework), `research/prose-boundary/config/
structural-policy-v2.json` (new), `research/prose-boundary/config/
generation/prompt-families.json` (new), `research/prose-boundary/config/
generation/generation-identity.json` (new, updated after execution),
`research/prose-boundary/config/annotation-guide.json` (new),
`research/prose-boundary/tools/generation_driver.py` (new),
`research/prose-boundary/tools/prose_boundary_builder.py` (new),
`research/prose-boundary/tools/differential_regression.py` (new),
`research/prose-boundary/tools/end_to_end_invariants.py` (new),
`research/prose-boundary/corpus/` (dev components, dev documents, dev
labels, naturalistic-dev, manifests - all committed),
`research/prose-boundary/results/increment3/` (new committed data-free
aggregates), `research/prose-boundary/REPORT-008C.md` (new),
`research/tests/test_parser_first_protection.py` (new, the single new test
file), `STATUS.md` (the one objective-007 paragraph correction plus the new
objective-008 paragraph), `research/RESEARCH-STATE.md` (additive per scope
item 18), `research/registry/experiments.json` (per scope item 19),
`research/tables/experiment-summary.csv` (regenerated),
`oap/orders/008-c-parser-first-protection.md` + `oap/active` (publication),
`oap/reports/008-c-parser-first-protection.md` (report-only final commit).
Private root: `008c-hidden/` (hidden set content - never committed).

No other path is modified.

## Requirements

1. Reconcile active 008-c, branch head == 49e4e70f1a8c304b4ad5ce27055a39e9e6e17288,
   PR #9 open/unmerged with all four checks green at that head, and the
   local work; no other concurrent mutations.
2. Create and freeze `config/generation/prompt-families.json` (scope item
   11) and `config/structural-policy-v2.json` (scope item 14) BEFORE any
   generation call or implementation code depends on them; both are frozen
   by commit and may not be changed later in the round without a strategy
   report (post-freeze changes require a recorded rationale; the default is
   that they do not change).
3. Execute the authorized generation with `tools/generation_driver.py`
   within the hard budget (400 calls; component batches <= 250;
   naturalistic <= 150; at most one retry per failed call, all recorded).
   BEFORE any bulk generation, the driver performs one bounded preflight
   call to verify endpoint availability and records the observed
   model/profile identity in `generation-identity.json`; on preflight
   failure, STOP the generation increment and report BLOCKED (no local
   fabrication of generated content, ever):
   component pools (1,234 components across 76 families; dev + hidden
   draws from separate seed streams and separate prompt instances) and the
   150 naturalistic responses (80 dev / 70 hidden instances). Hidden
   outputs go only to the private root `008c-hidden/`; dev outputs go to
   `corpus/` staging. The driver never echoes hidden content into model
   context (counts/hashes on stdout only). Record the complete generation
   identity (model/profile, parameters, seeds, batch plan, actual call
   count, failures, retries) in `generation-identity.json`. No generation
   call is a linguistic-method tuning call; no generated content is 009
   data.
4. Build `tools/prose_boundary_builder.py` and produce: 3,000 dev documents
   + label maps (committed under `corpus/documents-dev/` and
   `corpus/labels-dev/`); 2,000 hidden documents + label maps (private
   root only). Ground truth is derived purely from composition provenance
   (scope item 12 layout templates + interaction coverage guarantees; the
   builder never invokes the parser or protection layer; label invariants:
   no overlapping contradictory labels, complete mapping where required,
   exact byte + code-point ranges, deterministic reproduction from
   component IDs + seed).
5. Seal the hidden set: commit `corpus/manifests/hidden-manifest.json`
   (hashes/sizes/IDs/provenance/seeds only) and verify that the private
   root content matches the manifest exactly (driver-level self-check with
   the check logged to the report evidence). The seal commit happens BEFORE
   any dev-corpus tuning iteration (requirement 8) and before the
   implementation freeze (requirement 11). After the seal commit, no tool
   in the round reads hidden file content (manifest hashes only).
6. Implement `research/curated/prose_boundary.py` and the reworked
   `research/curated/protected.py` exactly per scope items 1-3 and policy
   v2 (scope item 14); residual recognizers per scope item 2 (narrow,
   content-level, candidate-prose-only, no Markdown-delimiter regexes, no
   reparsing of code/math/HTML/metadata); fail-closed legacy fallback;
   `Interval`/`is_protected`/`protected_intervals` signatures compatible
   with all existing consumers (verified by running the full research test
   suite); classify EVERY current protection rule in REPORT-008C.md into
   exactly one of: (1) Markdown syntax replaced by the parser; (2) semantic
   second-stage survivor; (3) redundant/obsolete; (4) purpose unclear (each
   with the rule's regex and disposition). No rule silently deleted.
7. Add the single new focused test file
   `research/tests/test_parser_first_protection.py` covering: coordinate
   mapping (exact round-trip; mid-sequence rejection; CRLF; decomposed
   Unicode; emoji/surrogate-pair boundaries); protocol parsing (tamper
   negative -> fallback, not crash); policy v2 (autolink destination
   protected; image incl. alt protected; strike/sup/sub exposed;
   math/HTML/code/metadata protected; link label exposed); residual
   recognizers per class (positive + negative per class: TeX, JSON/config,
   shell, paths, env vars, identifiers, numbers/units, URLs); fail-closed
   fallback (missing helper; corrupted stream; non-zero exit) with
   byte-identical legacy output and recorded reason; determinism;
   end-to-end invariants 1-7 (below) on dev documents with a scripted
   reviewer fake placed at the HTTP boundary (outside the protection
   boundary under test, per S-EVIDENCE-01); planted negatives (a
   deliberately broken coordinate mapping must be caught; a
   fail-open path must be impossible by construction and asserted).
8. Development evaluation (tuning evidence, labeled as such): run
   `tools/differential_regression.py` over (a) the 008-a 50-fixture x P2
   baseline through the new runtime path, (b) the full dev corpus
   (3,000 documents) with the scope item 15 metric set, (c) the 008-a
   100-sample receipt corpus differential vs legacy (consequence classes
   1-8; the 22 class-7 spans must remain protected by the second stage; no
   class-3 safety regressions). Fix genuine defects found on the dev corpus
   (allowed - this is the development set), re-run until the dev safety
   targets are met (protected-bytes-exposed = 0; coordinate violations = 0)
   or a genuine design limitation is documented. Every dev-corpus iteration
   is recorded in `results/increment3/` (final committed state only).
9. Run `tools/end_to_end_invariants.py` proving, on dev documents with
   seeded prose errors and a scripted reviewer at the HTTP boundary:
   (1) candidate detector input cannot include protected source ranges;
   (2) local n-gram/context windows do not bridge across protected spans;
   (3) reviewer targets cannot originate inside protected spans; (4)
   accepted repair patches cannot overlap protected spans; (5) every
   protected original substring remains byte/code-point identical after the
   complete repair path; (6) prose immediately adjacent to protected
   content remains repairable; (7) zero eligible prose yields zero
   linguistic-review work. Committed results in `results/increment3/`.
10. Performance measurement (scope item 15): parser + residual latency on
    representative documents at ~1KB, ~10KB, ~50KB (ms/document median,
    peak RSS), committed data-free.
11. Freeze: the implementation is frozen at the final head. Before the
    report-only commit: re-verify that the private-root hidden content
    still matches `hidden-manifest.json` exactly (hash re-check logged);
    verify `experiment-008a.json`, `fixtures/`, `results/increment1|2/`,
    008-a `REPORT.md`, `adapter/`, `identity/` are byte-identical to base
    (git diff empty); verify the full research suite passes unchanged
    plus the new focused test file; run the four required checks green at
    the implementation head.
12. Keep the research-state snapshot consistent with the tree at the final
    head (data update, not a test change) per scope item 18, including the
    additive section recording the human decision and the 008-c change
    summary (dev-corpus results explicitly labeled tuning evidence, not
    acceptance).
13. Registry (exactly):
    (a) add the 008-b entry, byte-for-byte this JSON (inserted in
    chronological position after the 008-a entry):

    ```json
    {
      "experiment_id": "008-b-post-merge-research-state-identities",
      "logical_root": "none (documentation/state corrective suffix; no private root)",
      "kind": "audit",
      "variation": "post-merge research-state identity correction and 008-a ledger registration",
      "status": "COMPLETE",
      "question": "Which machine-readable research-state identities became stale after the development-only merge of PR #8 (main 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9), and how were they corrected additively without weakening any gate?",
      "frozen_choices": {
        "new_model_calls": 0,
        "new_science": 0,
        "gate_or_test_changes": 0,
        "machine_block_fields_updated": 5,
        "registry_entries_added": 1
      },
      "metrics": {
        "model_calls": 0,
        "block_fields_updated": 5,
        "registry_entries_added": 1,
        "immutable_reports_mutated": 0,
        "test_files_changed": 0
      },
      "evidence_files": [
        {
          "disposition": "state projection at 008-b final head 49e4e70f1a8c304b4ad5ce27055a39e9e6e17288",
          "logical_path": "research/RESEARCH-STATE.md",
          "sha256": "aafa2f094cb00f17bd9e00eb7e60ad9f55d981d231049a9bb6a5679ed48e3b9e",
          "size": 89149
        },
        {
          "disposition": "ledger projection at 008-b final head 49e4e70f1a8c304b4ad5ce27055a39e9e6e17288",
          "logical_path": "research/registry/experiments.json",
          "sha256": "edba7e470cb5d36295294602da077ec5d40ac01f24b892fc94fdc35f8373434c",
          "size": 225355
        },
        {
          "disposition": "immutable OAP report at 008-b final head 49e4e70f1a8c304b4ad5ce27055a39e9e6e17288",
          "logical_path": "oap/reports/008-b-post-merge-research-state-identities.md",
          "sha256": "458a3e6dcb1aba1a5573ff56810e3763caf8ef57d918beece6be04c595451ed7",
          "size": 35491
        }
      ],
      "evidence_status": "public-data-free",
      "public_report": "research/RESEARCH-STATE.md#16",
      "public_configuration": "none (documentation/state round; no experiment configuration)",
      "public_metrics": "none (state correction; no experiment metrics)",
      "source_manifest": "none (no private source)",
      "child_runs": [],
      "conclusion": "Post-merge identity correction: machine block main_sha and reviewed_branch_head_sha set to merged main 7d2cc9ee37c1fc8c2a3eba238f89bc9bb242f9d9 (parent 4a029287f27e038d5c34c39b26ca836be7c6914b), reviewed_branch_head_parent_sha set accordingly, 008-a registered (registry 25 entries), oap_reports_reviewed=45; all four required checks green at the 008-b final head with test logic byte-unchanged; no scientific content, no model calls, no gate changes.",
      "pending_evidence": []
    }
    ```

    (b) add the 008-c entry following the 008-a entry schema with:
    experiment_id `008-c-parser-first-protection`; kind `study`; status set
    from the actual committed outcome (expected `COMPLETE`); question
    "Does the parser-first structural protection layer with its narrow
    residual semantic recognizer reproduce the 008-a qualification
    invariants through the runtime path, preserve the legacy protection as
    a fail-closed fallback, hold the seven end-to-end invariants on dev
    documents, and support a sealed independent hidden acceptance corpus
    without any dev-corpus safety regression?"; frozen_choices recording
    new_model_calls = the actual authorized generation call count (test
    data generation only, per the human decision of 2026-09-17), the P2
    profile, the pinned helper identity (crate checksum + binary sha256),
    the v2 config sha256 (committed file), the frozen prompt-library sha256,
    the mashup seeds, and the hidden-manifest sha256; metrics filled from
    the actual committed increment-3 aggregates (generation calls,
    components, dev documents, hidden documents, dev safety targets,
    dev coverage losses by container, coordinate violations 0,
    end-to-end invariants 7/7, helper invocations, helper wall-time
    median, performance ms/document at 1KB/10KB/50KB); evidence_files
    citing the committed v2 config, prompt library, generation identity,
    corpus census, hidden manifest, REPORT-008C.md and the increment-3
    summary with sha256/size computed from the committed blobs;
    public_report `research/prose-boundary/REPORT-008C.md`;
    public_configuration `research/prose-boundary/config/
    structural-policy-v2.json`; public_metrics the committed increment-3
    summary; source_manifest `none (no private source; committed
    data-free research subtree plus private-root hidden set referenced by
    manifest hashes only)`; pending_evidence `["008-d: blind hidden-
    acceptance evaluation of the frozen implementation (PASS/CONDITIONAL/
    FAIL), naturalistic label adjudication per the frozen annotation guide,
    end-to-end preservation on the hidden set"]`.
    (c) replace the top-level `scope` string exactly per scope item 19.
    (d) regenerate `research/tables/experiment-summary.csv` with
    `python3 -B -m research.tools.rebuild_tables` and verify with `--check`.
14. Run the Application baseline (real `scripts/verify_development_baseline.py`
    entry point), Research reproducibility, OAP bootstrap acceptance, and
    OAP report history checks green at the final head; no weakening,
    skipping, or redefinition. The full research suite (including every
    existing 007 protection/pipeline test and the frozen 007-o consistency
    test) must pass unchanged, plus the new focused test file.
15. One final report-only 008-c commit with the literal implementation head
    as sole parent and only `oap/reports/008-c-parser-first-protection.md`
    changed; verify remote PR head, exact report bytes, parent, and
    changed-path invariant; send response OK and stop. PR remains open and
    unmerged.

## Acceptance criteria

1. Protection layer = parser-first per frozen policy v2 with the narrow
   residual semantic recognizer; fallback fail-closed and tested; no
   fail-open path exists; no Markdown-delimiter regex remains in the
   residual layer.
2. Every current protection rule classified (4-way) in REPORT-008C.md;
   parser-obsolete Markdown-syntax rules no longer active on the happy
   path.
3. Dev-corpus tuning targets met and recorded: protected-bytes-exposed = 0
   and coordinate violations = 0 on the dev corpus (3,000 documents); the
   008-a 50-fixture baseline re-derived through the runtime path with zero
   invariant violations; the 008-a 100-sample differential shows no
   class-3 safety regression and the 22 class-7 spans remain protected by
   the second stage; end-to-end invariants 1-7 pass on dev documents. All
   dev results explicitly labeled tuning evidence, not acceptance.
4. Hidden set sealed before implementation freeze: `hidden-manifest.json`
   committed with per-file sha256/sizes; private-root content verified
   against the manifest both at seal time and again before the report-only
   commit; 2,000 hidden documents + label maps present in the private root
   (census recorded, content never committed).
5. Generation program executed within the recorded budget: actual call
   count <= 400; generation identity complete (model/profile, parameters,
   seeds, batch plan, failures, retries); 1,234 components across 76
   families (dev + hidden independent draws) and 150 naturalistic responses
   (80/70) produced; no generation output in public artifacts (counts/
   hashes/identities only); generated content explicitly not 009 data.
6. All focused tests pass at the final head; the four required CI checks
   green at the final head.
7. Zero linguistic-method changes (whole-round diff shows no change to the
   007-m frozen config, detector semantics, ranking, validator, acceptance,
   or any linguistic benchmark artifact); 009 untouched; the frozen 008-a
   baseline byte-identical (git diff base..final over experiment-008a.json,
   fixtures/, results/increment1|2/, REPORT.md, adapter/, identity/ empty);
   the 007 narrative sections of RESEARCH-STATE.md unrewritten.
8. Report-only commit invariant verified remotely; PR #9 open/unmerged.
9. Registry holds exactly 27 entries; the machine block matches the tree
   (registry_entries 27, oap_reports_reviewed 46, identity fields
   unchanged); the CSV is the byte-identical rebuild_tables output; the
   frozen 007-o consistency test passes.
10. STATUS.md no longer states PR #8 is open/unmerged; the new objective-
    008 paragraph states that the generated corpus tests structural safety,
    not repair quality.

## Verification

Focused: the new focused test file (all positives + planted negatives of
requirement 7); the differential-regression and end-to-end-invariant tools
re-run (determinism). Broader: the real Application baseline entry point;
research test discovery (the full research suite, including the 007
protection/pipeline tests and the 007-o consistency test, must pass
unchanged); the OAP suite; transcript/governance/report-history/protected-
source-diff/`git fsck` hygiene; `verify_report` (local) before push.
Evidence boundary: local commands at the literal implementation head plus
GitHub checks at that head; generation calls at the authorized endpoint
within budget; no live model calls of any other kind. Negative paths:
corrupted protocol -> fallback; missing helper -> fallback; non-zero
helper exit -> fallback; deliberately broken coordinate mapping caught;
fail-open impossible and asserted; hidden content unread after seal
(manifest-hash-only access, driver contract test); a tampered hidden file
in the private root would be caught by the manifest re-check (demonstrated
on a scratch copy only, never on the real sealed set).

## Local setup and constraints

CPU-only for the pipeline; the machine-local Rust toolchain (rustc/cargo
1.75.0, same private installation convention as 008-a) rebuilds the pinned
helper only if the 008-a binary is absent (presence verified by sha256
against 5df9a11d56b5bdec90c3ca09298802723975306f77e43e74ad1a72eb427c44bf;
rebuild from committed adapter source, pinned crate pulldown-cmark =0.13.4
with registry checksum e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e);
no system-wide Rust changes. Generation: the existing private endpoint via
env credentials (the 007 mechanism), within the hard budget of 400 calls;
the shared GPU/service is not reconfigured, not resized, and no second
large GPU model is loaded. No network beyond normal GitHub publication and
the authorized generation calls. No private customer data anywhere in the
program; generated content is project-authored benign topical test data and
stays out of public artifacts except committed dev-corpus files under the
repository license (explicitly project-authored structural test data);
private absolute paths stay out of committed documents.

## Documentation

REPORT-008C.md must state: the interface decision and its measurement
(helper startup cost, one call per document); the full 4-way rule
classification table (rule regex + disposition for EVERY rule); the
generation program record (frozen prompt library identity, generator
identity, budget vs actual calls, parameters, seeds, failures/retries);
the corpus census (components by family/category, dev/hidden document
counts, byte totals, interaction-coverage matrix); the hidden-seal
mechanics and the recorded D1 judgment with its residual-risk statement;
the dev-corpus metric aggregates for the scope item 15 set (explicitly
labeled tuning evidence, not acceptance); the end-to-end invariants 1-7
results; the performance measurement; the finding-B resolution (corrected
rule text codified in structural-policy-v2.json; experiment-008a.json left
byte-identical); the label transition of the adapter; the recorded policy
decisions (strike/sup/sub exposed; image incl. alt protected); an explicit
statement that this is a research-pipeline change only and that no
experimental-MVP linguistic acceptance, release, or deployment claim is
made; that the hidden acceptance is deferred to 008-d; and that objective
009 remains reserved against the post-objective-008 effective pipeline.
STATUS.md carries the scope item 17 corrections. RESEARCH-STATE.md carries
the scope item 18 additive section. The OAP report carries the round
record, per-head CI states, privacy/determinism statements, and the final-
head verification.

## Git and report publication

AMEND_EXISTING_PR on `oap/008-prose-boundary-qualification` (PR #9), base
49e4e70f1a8c304b4ad5ce27055a39e9e6e17288. Commit non-report work with
truthful messages (suggested boundaries: order+active activation; frozen
configs and prompt library; generation execution + corpus commit + hidden
seal; implementation + tools; dev evaluation + tests + freeze verification;
docs/registry/state). Wait for final-head CI; then one report-only commit
(SELF convention) with the literal implementation head as sole parent and
only `oap/reports/008-c-parser-first-protection.md` changed; push; verify
remote PR head, exact report bytes, parent, and changed-path invariant;
send exact response OK; stop. No merge, no auto-merge, no subsequent push
for this round.

## Decision classification

D0 overall: bounded, reversible engineering in the experimental research
pipeline, plus explicitly human-authorized bounded test-data generation
(the generation itself is a human-decided, budget-capped data program, not
a product change). The interface shape (pinned subprocess helper), module
layout, corpus layout, test representation, the two recorded policy
decisions (strike/sup/sub exposure; image-alt protection), the generation-
model policy (single pinned Qwen endpoint for auditability), the exact
corpus counts (76 families, 1,234 components, 5,000 mashups, 150
naturalistic, 400-call budget), and the finding-B codification path (new v2
config, 008-a config untouched) are routine reversible choices made and
recorded in-round and in the report.

Recorded D1 provisional judgment (not a CRIT entry): the hidden-set
seal mechanics in this single-workspace environment (dev/hidden split and
hidden-seal mechanics section). Dilemma: how to keep the hidden acceptance
set unavailable to the implementation agent until implementation freeze
when strategy and coding share one workspace. Governing authority: the
human decision of 2026-09-17 (seal by hash/manifest before implementation
finalization; independent generation preferred; strategy or an independent
evaluation process controls the hidden data). Alternatives considered:
(A) private-root storage + committed hash manifest + procedural prohibitions
+ 008-d hash verification (chosen); (B) commit hidden content to the repo
encrypted with a strategy-held key (rejected: key custody is not actually
separate in this environment, adds machinery, and the repo is readable by
the implementation agent anyway once any key material co-locates); (C)
hold the hidden set entirely outside the machine (rejected: not feasible
here; would block 008-d execution). Choice: (A), with the frozen-hash
integrity chain, the driver no-echo contract, the pre-freeze seal ordering,
the 008-d separate-round independence (frozen implementation, no
implementation changes, strategy-verified metrics), and the naturalistic
labels derived without consulting the implementation under test. Strongest
argument that this is wrong: the implementation agent's user account can
read the private root, so "unavailable" is procedural rather than
cryptographic, and a deviating implementation could in principle peek; the
mitigations (frozen hashes verified by strategy at two points, no-echo
driver contract, separate frozen-implementation evaluation round, manifest-
voiding on any mismatch) reduce but do not eliminate this residual risk,
which is recorded honestly in the report and in 008-d's evidential status.
Five-condition CRIT admission assessment: not admitted, because condition 1
fails - the explicit human decision resolves the substantive issue and
delegates the mechanics as reversible engineering; conditions 2-5 would
otherwise hold. Gate recorded for this judgment: before the 008-d hidden-
acceptance result is treated as the basis for proceeding to objective 009
or for any release-acceptability claim, a competent human may review the
seal mechanics and the 008-d evidential-status statement; no development
gate is crossed by this choice.

## Deferred human adjudication
- Decision: NONE
