# Reproduction recipes

These recipes describe the historical variants without downloading resources or
launching a model. The public repository contains no datasets, corpora, indexes,
weights, traces, filled prompts, or response bodies.

## Offline table rebuild

```sh
python3 -B -m research.tools.rebuild_tables --check
```

## Mechanical tests

```sh
python3 -B -m unittest discover -s research/tests -v
```

## Private identity replay

Set explicit mappings from each logical ledger root to its current private root,
then run the exact compressed ledger:

```sh
python3 -B -m research.tools.replay \
  --manifest research/registry/file-census.json.gz \
  --root-map 'experiments/=/caller/private/experiments' \
  --root-map 'recovery-executions/=/caller/private/recovery-executions' \
  --representative-roots \
  --limit 100
```

The compact `file-census.json` is only a summary and is rejected by the
verifier; it is not an entry ledger. Exact mappings also cover relocated native
roots by using an exact root mapping before a prefix mapping. Replay verifies
disposition, size, SHA-256, and regular-file/non-symlink identity, and performs
zero network/model calls.
`--representative-roots` additionally checks one deterministic eligible entry for each supplied logical mapping and emits only mapping keys, counts, statuses, and hashes; an unmapped or empty private root is reported as unavailable.
The historical live commands remain opt-in documentation and require separately
authorized data, endpoint, model, credentials, and resource budgets.

## Saved-sample replay

Small-study records and campaign records both use the offline replay boundary:

```sh
python3 -B -m research.tools.replay \
  --saved-record PRIVATE_RECORD.json \
  --index PRIVATE_INDEX.sqlite
```

The record must carry its detector cap (or explicit uncapped marker), first and
retry decisions, expected final value, and numeric English evidence. Missing
English evidence is an error, never an implicit zero. A malformed record fails
the complete replay rather than producing a partial receipt.

## Historical variant plan

```sh
python3 -B -m research.tools.reproduce \
  --variant low-unigram-retry \
  --input-root "$RESEARCH_INPUT_ROOT" \
  --index "$RESEARCH_INDEX_PATH" \
  --output-root "$RESEARCH_OUTPUT_ROOT" \
  --credential-env RESEARCH_CREDENTIAL_REF
```

This renders a zero-call plan. With `--allow-live`, the retained historical
driver executes only against the caller-owned records/index/output roots after
validating the explicit endpoint, model, credential reference, and bounded
resource flags. Live use is not enabled by imports or tests.

The driver selection is historical, not a latest-pipeline alias. In particular,
`low-plus-validator` consumes frozen first-stage decisions without resampling;
`low-unigram-retry` uses the contextual JSON retry body; the word-only and
hyphen families use the word parser; the three `ten-run-*` variants preserve
scheduled trial/STOPPED semantics; `prijigrala-retry10` repeats the raw first
proposal anchor; and `dassle-uv-audit` executes the owned data-free analyzer.
Campaign execution uses the retained phase/worker entrypoints with injected
caller-owned rows. No model/network call is made by plan/import/default modes.
