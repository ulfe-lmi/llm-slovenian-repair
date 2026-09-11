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

Set `PRIVATE_RESEARCH_ROOT` to the persistent native strategic root, then run:

```sh
python3 -B -m research.tools.replay \
  --private-root "$PRIVATE_RESEARCH_ROOT" \
  --manifest research/registry/file-census.json \
  --limit 100
```

Replay verifies bytes and identities only. It performs zero network/model calls.
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
