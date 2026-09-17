# 008-a — Prose-boundary parser qualification (research-only)

Order 008-a: *Qualify pulldown-cmark 0.13.4 as the structural prose boundary
(falsification experiment).* This subtree is the complete, reproducible,
data-safe record of that bounded experiment.

**Status: research / concept verification. Nothing here is production code and
nothing here is a runtime interface.** No application code in this repository
imports or executes any part of this subtree.

## Purpose

Falsify or validate, with machine-checkable evidence, the structural and
source-range contract of `pulldown-cmark` 0.13.4 as the *structural* prose
boundary for LLM-generated Markdown-like output:

- **Hard coordinate contract:** for every parser range `[start_byte, end_byte)`
  the original UTF-8 slice must be exact; no range may bisect a code point;
  the byte<->code-point mapping must be deterministic and exactly reversible.
- **Frozen structural policy:** which parser Text leaves are candidate prose
  (paragraphs, headings, list items, blockquotes, table cells, link labels,
  emphasis/strong) and which structures stay protected (inline/fenced/indented
  code, recognized math, HTML, Markdown syntax, link destinations/titles,
  metadata blocks, image structure).
- **Differential evaluation** against the current hand-written protection
  (`research/curated/protected.py`), classified by consequence (8 classes).

Outcome states: exactly one of GO / CONDITIONAL GO / NO-GO, decided in
`REPORT.md` against the predeclared acceptance criteria in `config/`.

## Measurement adapter (NOT a runtime interface)

`adapter/` contains a throwaway Rust binary **`prose-boundary-meas`** that is a
**MEASUREMENT ADAPTER**: it reads one UTF-8 document on stdin, parses it with
the pinned candidate crate (`pulldown-cmark = "=0.13.4"`, default features
off, registry checksum
`e9f068eba8e7071c5f9511831b44f32c740d5adf574e990f946ddb53db2f314e`, upstream
`pulldown-cmark/pulldown-cmark` tag `v0.13.4`), and emits deterministic JSONL
event lines `{"i","k","s","e"}` (kind token + exact byte offsets from
`Parser::into_offset_iter()`) followed by `{"eof":true}`.

It exists because the stock CLI `--events` mode emits ranges only in Rust
Debug text form, which is not a stable machine-readable contract. The adapter
adds no dependencies beyond the pinned crate, is research-only, and is
**explicitly not the future runtime interface**. The stock CLI
(`cargo install pulldown-cmark --version 0.13.4`, installed to a private
scratch root) is still used for an independent offset cross-check of every
fixture and profile.

Build recipe (private target dir, never committed):

```
CARGO_TARGET_DIR=<private scratch>/target cargo build --release
```

The binary SHA-256 is recorded in `identity/candidate-identity.json`
(`measurement_adapter_binary_sha256`).

## Data safety / privacy

- All fixture text is project-authored synthetic Slovenian material
  (deterministic, redistributable); no owner motivating examples.
- The representative corpus (Increment 2) is read from private preserved
  research roots at run time via a CLI argument; **no private path appears in
  this repository**, raw text never leaves the private root, and no new model
  calls are made. All committed aggregates carry counts/categories/hashes
  only.
- No wall-clock values appear in committed aggregates.

## Layout

```
README.md                     this file
REPORT.md                     public research report (answers all 13 order questions)
config/experiment-008a.json   frozen experiment configuration (predeclared order,
                              policy, acceptance, outcome states, privacy, determinism)
identity/candidate-identity.json  machine-readable candidate/upstream/license/MSRV/
                              dependency/install identity + adapter binary SHA-256
fixtures/fixtures.json        frozen fixture suite: 50 fixtures (38 required classes
                              + 12 extras), region roles and exact byte offsets,
                              frozen before first parser execution on the committed suite
fixtures/authoring-corrections.md  audit log of pre-commit authoring corrections
tools/fixture_defs.py         frozen fixture definitions (data + expected semantics)
tools/build_fixtures.py       deterministic builder (anchors -> exact byte offsets)
tools/coordinate.py           coordinate-contract helpers (byte <-> code point)
tools/run_increment1.py       deterministic Increment 1 evaluator (Hard invariants,
                              stock-CLI cross-check, determinism, negative self-test)
tools/select_corpus.py        deterministic representative-corpus selection (receipt only)
tools/run_differential.py     differential A-vs-B evaluator with 8-class consequence
                              classifier and controlled synthetic self-test
adapter/                      MEASUREMENT ADAPTER (Cargo project, pinned crate)
results/increment1/           per-profile event JSONL (project-authored input),
                              data-free aggregates, gate decision
results/increment2/           selection receipt, differential summary, challenger decision
```

## Reproduction

```
python3 tools/build_fixtures.py            # regenerate the frozen fixture suite
python3 tools/run_increment1.py <adapter-bin> <stock-cli>
python3 tools/select_corpus.py --runtime-root <private root>
python3 tools/run_differential.py --runtime-root <private root> --adapter-bin <adapter-bin>
```

All tools are deterministic: identical inputs produce identical output bytes.
