# Data source preparation

PLAN identifies Gigafida frequencies/n-grams, Sloleks, collocations and optional CPU
analyzers as resources to verify. Original research is preserved under docs/bootstrap;
its release/cutoff/rights claims are historical source content, not fresh inventory.
005 must verify actual release, format, terms, acquisition limits and redistribution.

Manifest each source checksum, version, acquisition reference, rights status,
cutoff/completeness, normalization/tagging, importer and deterministic build params.
Preserve EXACT/CENSORED/UNAVAILABLE and unknown full denominator; missing retained
ngram is not zero and retained forms cannot reconstruct complete lemma statistics.
Use sparse read-only indexes. Public query access is not bulk permission. Large
data/weights/private evaluations stay out of Git. No corpus downloaded by bootstrap.
