# EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE

This is one deliberately isolated research spike. It is not the production
application, a release, a deployment, a corpus redistribution, or a linguistic
quality claim. It uses standard-library Python 3.12, one synchronous process,
bounded finite HTTP calls, and a loopback-only proxy at `127.0.0.1:18024`.

The loader consumes only explicit external archive paths. It verifies regular
non-symlink owner/link-count-one files, exact size/MD5/SHA-256, selected member
names, 14-line preambles, header/marker hashes, CRLF, UTF-8, widths, and row
limits before inserting a derived SQLite index. Word absence is `UNAVAILABLE`;
missing n-grams are `CENSORED` with an unknown denominator. The archives and
index are private local data and must never be staged or packaged.

## Commands

From the repository root:

```sh
python3.12 -m unittest discover -s concept-verification/tests -v
python3.12 concept-verification/eval/perturb.py
python3.12 concept-verification/corpus.py prepare \
  --words-archive EXTERNAL_WORDS_ZIP \
  --ngrams-archive EXTERNAL_NGRAMS_ZIP \
  --output EXTERNAL_SQLITE
python3.12 concept-verification/eval/run_eval.py --phase dev \
  --config concept-verification/eval/config.json \
  --index EXTERNAL_SQLITE --results LOCAL_DEV
python3.12 concept-verification/eval/run_eval.py --freeze \
  --config concept-verification/eval/config.json --index EXTERNAL_SQLITE \
  --output concept-verification/eval/frozen-experiment.json
python3.12 concept-verification/eval/run_eval.py --phase heldout \
  --config concept-verification/eval/config.json --index EXTERNAL_SQLITE \
  --frozen concept-verification/eval/frozen-experiment.json --results LOCAL_HELDOUT
CONCEPT_INDEX=EXTERNAL_SQLITE CONCEPT_UPSTREAM_URL=http://UPSTREAM_HOST:PORT \
  ./concept-verification/run_proxy.sh
python3.12 concept-verification/eval/collect.py --cases 8 \
  --proxy http://127.0.0.1:18024/v1 --results LOCAL_WORKLOAD
python3.12 concept-verification/eval/score.py --controlled LOCAL_HELDOUT/heldout.json \
  --workload LOCAL_WORKLOAD --output concept-verification/eval/results/summary.json
python3.12 concept-verification/eval/review_sheet.py --input LOCAL_WORKLOAD \
  --output LOCAL_REVIEW_SHEET
```

The two prompt variants and four threshold settings are dev-only. The frozen
file binds the selected mode, threshold, prompt bytes/config identity, dataset
hashes, and index identity; held-out execution refuses mismatches. Detector
selection is separate from reviewer proposal and exact acceptance. Accepted
edits are applied only to original spans right-to-left, with protected slices
and all outside code points asserted unchanged.

## Protocol and evaluation boundaries

The proxy buffers a complete Responses SSE before CPU review. It changes only
assistant `output_text` belonging to natural message items. Reasoning, tools,
function arguments, IDs, usage, event order/count, and no-safe-text responses
are preserved. Incomplete upstream generations are errors, never successful
repairs. Reviewer calls are fresh non-streaming calls containing only compact
instructions, the exact sentence, and one target; only one strict JSON result
shape is accepted, and a wider edit or uncertainty keeps the original.

The controlled split is deterministic and project-authored: dev has 16 cases
and held-out has 32, including `točniej`, `rjavo-zlati`, `lase`,
`kitaraš/vokal`, `najslovnijih`, contextual constructions, typos, valid-word
controls, mixed technical prose, Markdown, commands, URLs, and paths. The
held-out report must include raw/no-repair, detector-only, reviewer-decision,
full conservative, unigram-only, and local-context ablations with denominators,
candidate enrichment, recall, reviewer accuracy, accepted/correct/harmful/
missed counts, protected changes, recovery, and latency.

Real workload benefit or harm is `AWAITING_HUMAN_REVIEW` until a human labels
the deterministic blinded sheet. Model self-review is not a human label.
Eight bounded workload cases include one tool-loop-shaped request; raw traces
remain under ignored local results. A missing endpoint is recorded once as an
external availability failure, not converted into a quality success.
