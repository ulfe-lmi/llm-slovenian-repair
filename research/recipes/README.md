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
