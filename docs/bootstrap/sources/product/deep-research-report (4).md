# Conservative Corpus-Grounded Lexical Repair for Slovenian: Prior Art, Available Resources, and Novelty

## Executive finding

The central idea is **not new in its classical statistical core**. In particular, a 2009 EMNLP paper by Aminul Islam and Diana Inkpen, *Real-Word Spelling Correction using Google Web 1T 3-grams*, implements something strikingly close to the proposed `(left_word, right_word) → candidate_middle_words` mechanism. For a token \(w_i\), their system looks at the observed trigram \(w_{i-1},w_i,w_{i+1}\), then searches for trigrams in which **the two neighboring words remain fixed and only the middle word changes**; alternatives whose corpus frequency exceeds that of the original are considered correction candidates. citeturn10view0turn12view0turn12view1

That precedent is strong enough that a paper claiming novelty simply for “detect a suspicious valid word by looking up what words normally occur between its two neighbors in a very large corpus” would have a difficult novelty case. Earlier context-sensitive spelling work had already established trigram/confusion-set correction, including Golding and Schabes's 1996 ACL work combining trigram and feature-based methods. citeturn25search0turn25search20

However, I did **not** find an existing system matching the proposed architecture end-to-end:

> open-world lexical anomaly detection over ordinary LLM output → strong abstention based on corpus support → parallel surface/lemma evidence → invoke an LLM only at the flagged position → demand a one-token repair → independently re-score the proposed repair against corpus evidence → make no edit unless the corpus likelihood improvement is large.

The important distinction is that most classical systems constrain replacements to **known confusion sets or orthographically similar words**, while most modern systems either detect spelling/grammar errors neurally or directly rewrite/correct the input. The proposed system instead treats the corpus as an independent *gatekeeper* around an LLM and explicitly optimizes for **very low false-positive rates and minimal intervention**. The closest classical system does not include that neural candidate-generation/corpus-veto architecture, morphological dual scoring, or the stated abstention criterion. citeturn12view0turn27search2turn26search0

For Slovenian specifically, the resource situation is unusually favorable. CLARIN.SI already distributes **Gigafida 2.0 unigram frequency lists and word-level 2-, 3-, 4-, and 5-gram frequency lists**, including files involving lower-cased word forms, lemmas and morphosyntactic tags. The n-gram release is public under CC BY-SA 4.0. citeturn20view0turn20view1 The catch is important: the packaged n-grams include only n-grams occurring at least **2 times per million words**. Since Gigafida 2.0 contains 1,134,693,933 words, that corresponds to roughly **2,269 occurrences**. Thus the downloadable n-gram package is a compact list of very frequent n-grams, not a complete low-frequency trigram database suitable for all anomaly decisions. citeturn20view0turn22search2

The bottom-line classification is therefore:

| Class | Finding |
|---|---|
| **A. Essentially the proposed architecture already** | **Islam & Inkpen 2009 is nearly identical to the classical middle-token/fixed-neighbors core**, but not to the complete proposed hybrid architecture. |
| **B. Closely related/adaptable** | Context-sensitive real-word spelling correction; LanguageTool's statistical n-gram confusion rules; SloNSpell; GECToR; masked-LM scoring; ELECTRA-style replaced-token detection. |
| **C. Related but different problem** | General GEC, lexical substitution where the target position is already known, ordinary spell checking, learner-language correction, unconstrained LLM post-editing and broad hallucination/factuality checking. |
| **D. Slovenian components** | Gigafida 2.x; Gigafida frequency/n-gram resources; Sloleks; CLASSLA/JOS-style morphology; LIST; Gigafida collocations; Šolar; SloBERTa/SloNSpell; Trendi n-grams. |

My assessment is: **a basic Gigafida trigram checker would mostly be a Slovenian reimplementation of an established technique. The exact conservative corpus-gated LLM repair system would still be meaningful new engineering, and could constitute research if the novelty is framed around open-world detection, morphology-aware abstention, corpus-independent verification of LLM repairs, and evaluation on naturally occurring LLM lexical-selection errors rather than ordinary spelling/learner errors.**

## Systems essentially implementing the proposed statistical core

The most important prior art is not a modern grammar checker but the literature on **real-word/context-sensitive spelling correction**. “Real-word” is precisely the important case here: the offending token is itself a legal word and therefore cannot be found by dictionary lookup. citeturn10view0turn25search0

### Islam and Inkpen: the nearest match

Islam and Inkpen's *Real-Word Spelling Correction using Google Web 1T 3-grams* is, structurally, extremely close to the proposed detector. It used Google's Web 1T corpus resource, whose underlying collection contained roughly a trillion words and n-grams up to order five, although the method in this paper specifically used trigrams. citeturn10view0turn11view0

The algorithm does approximately this at an interior token:

\[
L=w_{i-1},\qquad x=w_i,\qquad R=w_{i+1}.
\]

It obtains the corpus frequency

\[
c(L,x,R)
\]

and then retrieves trigrams

\[
(L,y,R)
\]

where **only \(y\) differs from the input token**, keeping both immediate neighbors constant. Candidates must have a trigram frequency exceeding that of the original. citeturn12view0turn12view1

That is effectively the same information as the proposed index:

```text
(left_word, right_word) -> {
    middle_word_1: count,
    middle_word_2: count,
    ...
}
```

The paper then brings in additional context, including another trigram on the left, and combines a normalized n-gram-frequency score with a modified longest-common-subsequence/string-similarity score. citeturn12view0 Candidate generation is therefore *open over observed corpus alternatives in the fixed context*, but candidate acceptance is heavily constrained by **orthographic similarity to the original**. That last part is the major difference: it is designed for spelling-like real-word substitutions such as a wrong valid word caused by a typo, rather than arbitrary semantic or lexical-choice mistakes where the appropriate replacement can look completely different. citeturn10view0turn12view0

Its evaluation also illustrates why simply reproducing the method would not meet your conservative objective. In the reported experiment the proposed detector achieved recall around 0.89 but precision around 0.445, and the correction stage had precision around 0.381; the optimization regime was therefore very different from a system intended to touch only exceptionally well-supported errors. citeturn11view3

**Classification: A — essentially the same classical detection/candidate-frequency core; not the same complete system.**

Direct source: [Islam & Inkpen, EMNLP 2009, ACL Anthology](https://aclanthology.org/D09-1129/).

### The Mays–Damerau–Mercer / Golding line

The idea sits in an older tradition. Context-sensitive spelling correction treats words such as *there/their* as a disambiguation problem rather than asking whether the token exists in a dictionary. Golding and Schabes's ACL 1996 system explicitly combined a trigram-based model with feature-based contextual evidence, while Golding's preceding Bayesian work compared its method with a trigram correction method and proposed selecting models according to properties of the confusion set. citeturn25search0turn25search20

These systems generally differ from your proposal because they work with **predefined confusion sets**: once the system knows that a position contains one member of a set such as `{weather, whether}`, it decides which member is most probable in context. A contemporary survey-like discussion of those early systems notes that the coverage of Golding and Schabes's experiment was limited to 18 small confusion sets. citeturn25search8

That is a significant difference from what you propose. Your detector effectively creates a *dynamic confusion set from the corpus*:

\[
C(L,R)=\{y:c(L,y,R)>0\},
\]

and can therefore notice an inappropriate word even when nobody anticipated the pair of confusable words in advance.

**Classification: A/B — established statistical principle, but narrower candidate universe than the proposed system.**

Direct source: [Golding & Schabes, ACL 1996](https://aclanthology.org/P96-1010/).

### Why this prior art matters for the novelty claim

The most defensible historical statement is therefore not “nobody has done this,” but:

> **Corpus-frequency-based real-word correction, including holding both adjacent words constant and varying the middle word, is established prior art. What appears much less standard is using it as a high-precision, open-world anomaly gate around a modern LLM, with morphology-aware evidence and a final independent corpus veto.**

That distinction is crucial. Islam and Inkpen already give you the basic lookup relation; the potentially novel part starts *after* that observation. citeturn12view0turn12view1

## Closely related systems and research that solve a different problem

Several systems are close enough to borrow from, but none should be mistaken for the exact architecture.

| System / line of work | Detection | Candidate generation / ranking | Valid-but-wrong word? | Edit granularity | Availability | Closeness |
|---|---|---|---|---|---|---|
| **Islam & Inkpen 2009** | Trigram frequency with fixed surrounding words | Corpus alternatives; orthographic similarity + normalized trigram frequency | **Yes** | One word | Paper; Google Web 1T itself is historical | **Very high** |
| **Golding & Schabes 1996** | Trigram + contextual features over confusion sets | Choose among predefined confusables | **Yes** | One word | Paper | High conceptually |
| **LanguageTool n-gram rules** | Large external n-gram statistics for confusable forms | Rule/confusion-set candidates, probability comparisons | **Yes** | Usually local | Open-source engine; n-gram datasets supported | High operationally |
| **SloNSpell 2024** | Fine-tuned SloBERTa token/error classifier | **No correction generation in the paper** | Context helps, but training errors are spelling-oriented | Detection at token/span level | Code + model open | Medium |
| **GECToR 2020** | Transformer sequence tagging | Predict edit tags/replacements | **Yes** | Local edits | Official code open | Medium |
| **MLM scoring** | \(P(w_i\mid\text{rest})\) via masking / pseudo-log-likelihood | Compare candidate masked-token probabilities | **Yes** | Can be one-token | Paper + code | Medium/high |
| **ELECTRA-style detection** | Discriminator predicts whether an input token has been replaced | Normally no lexical repair stage | **Yes, in principle** | Token-level detector | Models/method open | Medium |
| **General neural/LLM GEC** | Learned sentence-level error model or generative prompt | Generates corrected sequence | Yes | Often multiple edits/rephrasing | Many systems | Low-to-medium |

### LanguageTool: useful production precedent for conservative n-gram checks

LanguageTool is particularly relevant because its official developer documentation explicitly supports using **large n-gram datasets to detect errors that ordinary spell checking cannot**, including confusion between individually valid words. Its n-gram rule infrastructure computes statistical evidence for alternative usages rather than relying solely on lexical validity. citeturn13search1turn14search24

Even more relevant to your intended operating point, LanguageTool's guidance for writing statistical n-gram rules says that **precision is expected to be very high and should be close to 1**, favoring precision over aggressive recall. citeturn13search5 That is an important production precedent for your argument that a corpus checker can reasonably be designed to **abstain almost all the time**.

The difference is architectural. LanguageTool's statistical rules are primarily built around known error/confusion phenomena; it is not, as far as the documentation reviewed here indicates, a generic open-world loop over every token that asks “what other middle words dominate this arbitrary left/right context?” It therefore demonstrates feasibility and the desirability of high-precision corpus scoring but not your full detector. Its core checker is open-source. citeturn13search1turn14search0

**Classification: B — readily adaptable design ideas, particularly calibration and abstention.**

Direct links: [LanguageTool source](https://github.com/languagetool-org/languagetool) and [LanguageTool development documentation](https://dev.languagetool.org/).

### SloNSpell: the closest modern Slovenian detector

The 2024 TSD paper *Neural Spell-Checker: Beyond Words with Synthetic Data Generation* introduces two Slovene systems: **SloSpell**, a classical lexicon-based checker built from Sloleks 3.0, and **SloNSpell**, a contextual detector based on fine-tuned SloBERTa. The authors explicitly motivate neural checking partly by the ability to consider whether a word is suitable in context, rather than merely whether it is in a dictionary. citeturn27search2turn27academia21

But there is an especially important limitation for this research question: the authors explicitly state that their work focuses on **spelling-error detection without proposing corrections**. The synthetic training corruption includes phenomena such as split words, concatenated words, commonly misspelled words and character swaps. Thus SloNSpell is a useful ready-made *suspicious-token detector*, but it was not designed specifically for arbitrary lexical-selection mistakes of the kind an LLM may make. citeturn27search2

The source code and fine-tuned model are available, including the `SloBERTa-slo-word-spelling-annotator` model. citeturn26search2turn26search6

**Classification: B — probably the most useful Slovenian neural component to benchmark against; not the same task and no correction/rescoring stage.**

Direct links: [paper](https://arxiv.org/abs/2410.23514), [code](https://github.com/matejklemen/slonspell), [model](https://huggingface.co/cjvt/SloBERTa-slo-word-spelling-annotator).

### GECToR: modern precedent for “edit, do not rewrite”

GECToR's title captures the relevant idea: *Grammatical Error Correction: Tag, Not Rewrite*. Rather than running unconstrained sequence-to-sequence generation, it frames correction as tagging tokens with edit operations. It is therefore substantially more compatible with a minimal-change requirement than ordinary generative GEC. The authors released an implementation, and the original code repository remains available. citeturn26search0turn26search4

Its limitation for your purpose is almost the opposite of Islam and Inkpen's. GECToR has a modern contextual neural representation and local edit discipline, but its decision is **model-internal rather than independently justified by transparent reference-corpus counts**. It also covers grammatical error types more broadly than lexical anomaly detection. citeturn26search0

**Classification: B — strong architectural inspiration for enforcing local edits, but a different detector/scorer.**

Direct links: [paper](https://aclanthology.org/2020.bea-1.16/) and [official repository](https://github.com/grammarly/gector).

### Masked-language-model scoring

A masked language model gives a natural neural analogue of your quantity:

\[
P(w_i\mid w_1,\ldots,w_{i-1},w_{i+1},\ldots,w_n).
\]

Salazar et al.'s *Masked Language Model Scoring* formalized pseudo-log-likelihood scoring by masking tokens one by one and asking the MLM for the probability of the observed token given the remaining context. They demonstrated that this can function as an unsupervised measure of linguistic acceptability and as a rescoring mechanism. citeturn26search1turn26search5

For your problem one need not sum the whole sentence PLL. One can inspect the conditional probability at one token and contrast:

\[
\log P(y\mid \text{context})-\log P(x\mid\text{context}),
\]

for proposed replacement \(y\) and original \(x\). That is the neural equivalent of the corpus-frequency ratio you are proposing.

It has superior context coverage and can capture dependencies far beyond adjacent words, but the score is less interpretable than “this construction occurs 8,247 times with *y* and 3 times with *x*.” It is also correlated with the biases and training distribution of the pretrained LM rather than being a visibly independent corpus observation. Salazar et al. released their MLM-scoring code. citeturn26search5turn26search9

**Classification: B — perhaps the strongest modern alternative detector/scorer.**

Direct links: [paper](https://aclanthology.org/2020.acl-main.240/) and [implementation](https://github.com/awslabs/mlm-scoring).

### ELECTRA: an unusually close neural formulation of anomaly detection

ELECTRA trains a discriminator to decide, at every token position, whether the token is genuine or has been replaced by a plausible token generated by another model. The authors call the objective **replaced-token detection**. citeturn25search6turn25search10

Conceptually this is remarkably close to the detector part of your target application: “does this word look as though somebody substituted a plausible but wrong word here?” Unlike BERT masking, the suspicious token remains present in its normal sentence when the discriminator judges it. The drawback is that an off-the-shelf ELECTRA discriminator is detecting the statistical traces of its *pretraining corruption distribution*, not necessarily calibrated LLM lexical mistakes, and its score does not directly expose corpus examples/counts. citeturn25search6

SloNSpell's related-work discussion explicitly notes neural spelling-error work using ELECTRA-like discriminators, while SloNSpell itself uses SloBERTa. citeturn27search2

**Classification: B — excellent neural baseline for suspicious-token detection; not an independent corpus validator.**

Direct link: [ELECTRA, ICLR 2020](https://openreview.net/forum?id=r1xMH1BtvB).

### General Slovenian GEC and learner correction

There is now active Slovenian GEC work. A 2025 study on grammatical correction of Slovenian school essays using LLMs explicitly observes that excessive paraphrasing by generative models is undesirable in educational correction settings. citeturn26search3turn26search15 That is unusually aligned with your motivation for avoiding wholesale rewriting.

The Šolar developmental corpus has evolved to version 3.0 and contains learner writing with error/correction annotation, making it valuable for evaluating correction systems. Its error distribution, however, is school/learner language rather than LLM output. citeturn26search11

These systems and datasets answer the broader question “how do we make incorrect Slovenian grammatical?” rather than “given mostly correct generated Slovenian, which one lexical item is anomalous enough that we should dare to touch it?”

**Classification: C for general GEC; D as an evaluation/training resource.**

## Slovenian resources from which the system can be assembled

The Slovenian-resource investigation changes the practical answer considerably: much of the infrastructure that would otherwise be expensive to build already exists.

### Gigafida is not merely a corpus; relevant frequency tables already exist

Gigafida 2.0 contains **1,134,693,933 words, 59,861,870 sentences and 38,310 texts**, covering written standard Slovene from 1990–2018. It was deliberately cleaned toward standard written Slovene and linguistically annotated, which makes it a particularly sensible normative/reference source for this use. citeturn22search2turn22search5turn22search20

The corpus has subsequently been updated. The current interface identifies **Gigafida 2.2**, published on December 8, 2025, with about **1.160 billion words and 61.9 million sentences**. citeturn22search4turn22search18 The derived downloadable n-gram resource I found, however, is specifically the 2019 **Gigafida 2.0** release, not a corresponding 2.2 n-gram dump. citeturn20view0turn23search0

More importantly, CLARIN.SI already publishes exactly the kinds of derived statistics the proposal anticipates.

The [Gigafida 2.0 word-frequency resource](https://www.clarin.si/repository/xmlui/handle/11356/1273) contains all corpus words with absolute and relative frequencies and text-type distributions. Separate data cover lemmas, lower-case surface forms, parts of speech and morphosyntactic information. citeturn20view1

The [Gigafida 2.0 word-level n-gram resource](https://www.clarin.si/repository/xmlui/handle/11356/1274) contains **2-, 3-, 4- and 5-grams**, absolute and relative frequencies, text-type distributions, and several association measures including Dice, t-score, mutual information variants, logDice and log-likelihood. The repository preview shows separate files involving lower-case word forms, lemmas and morphosyntactic tags for multiple n-gram orders. citeturn20view0

This means the surface-versus-lemma idea is not something for which you need to invent a Slovene normalization pipeline from scratch.

There is, however, a critical limitation:

\[
\text{published n-gram threshold}=2/\text{million}.
\]

With 1,134,693,933 words,

\[
2\times\frac{1{,}134{,}693{,}933}{1{,}000{,}000}
\approx 2{,}269.
\]

So the downloadable package includes only n-grams occurring on the order of **2,269 times or more** in Gigafida 2.0. citeturn20view0turn22search2

That explains why a trillion-character-scale corpus can yield a relatively small zipped n-gram package. It also has an important algorithmic consequence: **an absent trigram in that release does not mean “unseen in Gigafida”; it means “less frequent than approximately 2 per million.”** Treating absence from the downloadable table as zero would therefore be a serious error.

This distinction may be the most important implementation finding of the Slovenian-specific research.

### The exact `(left,right) → middle` table does not appear to be prepackaged

The CLARIN resource distributes ordinary contiguous n-grams. I found no indication that CLARIN.SI distributes a ready-made **skip-context index** of the exact form

```text
(left, right) -> [(middle, count), ...]
```

or a complete skip-gram frequency dump from Gigafida. The supplied trigram table can trivially be inverted into that index:

```text
for (left, middle, right, count) in trigrams:
    index[(left, right)][middle] += count
```

but because the published input has the high `2/million` cutoff, that inverted table will contain only very common complete trigrams. citeturn20view0

For an initial **ultra-high-precision** detector, that may actually be useful: your strongest desired case is precisely one in which the surrounding pattern is extremely well attested. For broad coverage, however, you would want a lower-frequency/full trigram extraction or direct corpus query.

### LIST substantially reduces the extraction engineering

The Gigafida frequency resources were produced with **LIST**, a CLARIN.SI corpus-extraction tool. Its documented functionality includes extracting character, word-part, word and word-set/n-gram lists from annotated corpora and producing tabular results; it supports corpus formats used by Slovenian resources and was the tool used to generate the Gigafida lists. citeturn6view3turn20view0turn20view1

Thus, assuming the required corpus-level access/licensing can be obtained, rebuilding frequency data at a lower threshold is not conceptually difficult.

One caution is licensing/access. The derived Gigafida 2.0 frequency and n-gram packages are explicitly public under **CC BY-SA 4.0**, while the current Gigafida 2.2 online corpus states that access to the underlying work is governed by agreements between the University of Ljubljana and text providers. One should therefore not infer from the open derived lists that unrestricted redistribution or arbitrary local processing of all raw Gigafida 2.2 text is automatically permitted. citeturn20view0turn20view1turn22search18

### Gigafida collocations are useful, but solve a different statistical problem

CLARIN.SI also distributes **collocation frequency lists from Gigafida 2.1**. The resource is based on a set of predefined syntactic structures and includes frequent syntactic collocations; the accompanying project information describes 81 syntactic structures and a frequency cutoff for extracted collocations. citeturn2search10turn23search1

That is valuable supplementary evidence. A word can be anomalous even when its exact neighboring trigram is sparse, but its dependency/collocational relationship with another word may be strongly abnormal. A second-stage feature such as

\[
\text{collocation-score}(\text{head lemma},\text{dependent lemma})
\]

could therefore reduce the brittleness of exact adjacency.

It is **not**, however, a substitute for the proposed arbitrary middle-token index. Syntactic collocations abstract away from word adjacency and are extracted for predefined structures, whereas the proposed detector specifically wants exhaustive lexical alternatives in a local slot.

**Classification: D.**

### Sloleks solves much of the morphological-normalization problem

Sloleks is the reference Slovene morphological lexicon. Historical/current releases provide lemmas, inflected forms and grammatical features, and SloNSpell's classical SloSpell baseline uses Sloleks 3.0 as its lexicon. A newer Sloleks 3.1 resource is present in the CLARIN infrastructure. citeturn24search1turn24search3turn27search2

For the proposed system it can perform several distinct jobs:

* distinguish known Slovene forms from identifiers/noise;
* map surface forms to possible lemmas;
* constrain a replacement to morphologically plausible inflections;
* identify when apparent surface rarity is merely the result of rich inflection.

Earlier Sloleks releases also associate corpus frequency information with forms, although the large Gigafida frequency tables are more directly appropriate for your probabilistic scoring. citeturn24search1turn20view1

**Classification: D — highly relevant supporting component, not a contextual corrector.**

### CLASSLA/JOS-style annotation is the natural preprocessing layer

The Slovenian ecosystem already has mature tokenization, morphosyntactic annotation and lemmatization infrastructure, including the CLASSLA tool/resource family and JOS-compatible annotation traditions. The CLARIN.SI CLASSLA knowledge infrastructure makes the relevant South Slavic processing models and documentation available. citeturn1search0

There is therefore little reason to build a Slovene tokenizer, POS tagger and lemmatizer specifically for this project. The interesting engineering is in **preserving mappings between the original surface text and linguistically analyzed tokens**, because replacements must be surgical and must leave punctuation, whitespace, Markdown, URLs, code and identifiers untouched.

The older Obeliks/JOS lineage is relevant primarily as preprocessing/annotation infrastructure; in the resources reviewed I found no evidence that Obeliks itself implements the open-world contextual real-word correction system under investigation.

**Classification: D.**

### Other useful Slovenian data

CLARIN.SI also lists word-level n-gram frequency resources for the **Trendi 2021** corpus. A contemporary/news-oriented corpus can be valuable beside Gigafida because Gigafida 2.0's texts end in 2018; recent proper names, technologies and terminology are precisely the cases in which an old reference corpus is most likely to generate false alarms. citeturn23search27turn22search5

Šolar 3.0 provides authentic annotated learner corrections and is useful for stress-testing false positives and studying error categories, although LLM lexical-choice errors should ideally receive their own benchmark. citeturn26search11

The practical Slovenian stack could therefore already be:

```text
original text
      |
safe span segmentation
      |
CLASSLA / morphological analysis
      |
surface + lemma n-gram statistics
      |                 \
Gigafida 2.x             Sloleks / morphosyntax
      |
high-confidence anomaly detector
      |
LLM proposes 1–k one-token alternatives
      |
Gigafida surface + lemma + morphology re-scoring
      |
abstain unless evidence margin is large
```

Almost every box except the **anomaly/abstention logic and corpus-gated repair controller** has an existing Slovenian component.

## Classical corpus methods versus modern neural alternatives

For this particular objective, the classical method is less obsolete than it might initially appear. Its disadvantages are real, but several characteristics match the product requirements unusually well.

### Corpus n-grams

With a complete trigram table the direct statistic is:

\[
N(L,R)=\sum_m c(L,m,R)
\]

and

\[
\hat P(m\mid L,R)
=
\frac{c(L,m,R)}
     {N(L,R)}.
\]

This immediately implements your crucial distinction between two kinds of zero:

**Sparse context**

\[
c(L,x,R)=0,\qquad N(L,R)\approx0
\]

means “we know almost nothing.”

**Strongly represented context with anomalous original**

\[
c(L,x,R)\approx0,\qquad N(L,R)\gg0
\]

with perhaps

\[
c(L,y,R)\gg c(L,x,R)
\]

means “this slot is well known and the corpus overwhelmingly prefers something else.”

Islam and Inkpen's procedure is concrete evidence that fixed-neighbor trigram alternatives are workable for real-word correction, while LanguageTool demonstrates that large n-gram resources can support high-precision production rules. citeturn12view0turn13search1turn13search5

The benefits for your target use are substantial:

| Property | Corpus n-gram approach | Neural/LLM approach |
|---|---|---|
| Determinism | Excellent | Depends on model/inference |
| Cost | Extremely low after indexing | Neural inference required |
| Throughput | Very high | Lower |
| Exact interpretability | Excellent: actual counts/examples | Limited |
| Independence from generating LLM | Excellent | Depends on chosen verifier |
| Easy abstention rule | Excellent | Requires probability calibration |
| Long-range context | Poor | Strong |
| Sparsity resistance | Poor | Strong |
| Morphological generalization | Poor by default; improved by lemmas | Usually better |
| Semantic understanding | Weak | Much stronger |
| Domain robustness | Limited by corpus composition | Still limited, but generally broader |

The most attractive property is **not necessarily accuracy averaged over every possible error**. It is the ability to say:

> “I will make no decision unless I have several thousand independent corpus observations showing an overwhelming alternative.”

That operating point is unusually compatible with your low-false-positive objective.

### Masked language models

An MLM can effectively replace exact-count statistics with a smoothed high-dimensional model:

\[
P_\theta(w_i\mid\text{all surrounding context}).
\]

This substantially reduces sparsity and captures nonadjacent agreement, selectional restrictions and syntax. Pseudo-log-likelihood scoring is already established as a way to turn BERT-style models into sentence/candidate scorers. citeturn26search1turn26search5

For example, candidate comparison could be:

\[
\Delta_{\text{MLM}}
=
\log P_\theta(y\mid C)
-
\log P_\theta(x\mid C).
\]

That is arguably a better general detector. But it loses one of the most important safeguards in your proposal: the evidence is generated by another learned model rather than directly exposing reference-corpus usage. For a system intended to be *deliberately suspicious of neural generation*, an independent corpus score is a valuable second epistemic channel.

A good hybrid would therefore use an MLM as **additional evidence**, not necessarily as final authority.

### Neural grammatical-error correction

Modern GEC systems optimize a much broader problem. GECToR shows that neural systems can explicitly favor local edit operations rather than free generation. citeturn26search0turn26search4 Slovenian LLM-based GEC work likewise recognizes the problem of unwanted paraphrasing. citeturn26search3turn26search15

But a GEC model is normally rewarded for correcting anything judged ungrammatical or stylistically deficient. That objective is not the same as:

> preserve every token unless there is unusually strong evidence that this precise lexical choice is anomalous.

For a 90–95%-correct input stream, **precision on edits** and **damage caused to correct tokens** deserve more emphasis than aggregate sentence-level correction quality.

### LLM-as-a-judge

An LLM can read substantially more context than any trigram system and can notice semantic errors that remain perfectly plausible locally. It can also reason over terminology and discourse. But letting an LLM both identify the error and decide its replacement weakens the independence that motivates the proposed architecture.

A stronger use is precisely the one in the proposal:

```text
corpus / independent detector:
    "position 17 is suspicious"

LLM:
    "given that this ONE position is suspect,
     return at most k one-word alternatives"

independent evidence:
    "candidate B is much better attested than the original"

controller:
    edit or abstain
```

That is architecturally different from asking an LLM to “proofread this text.” The former bounds its authority; the latter delegates the whole correction problem.

### Token probability and perplexity

For an autoregressive model one can flag unusually low token log-probabilities; for an MLM, Salazar-style conditional scoring provides a bidirectional equivalent. citeturn26search1turn26search5

The key problem is **calibration**. Rare proper nouns, numbers, technical phrases and creative constructions can have low probability without being wrong. Conversely, a semantically erroneous but cliché-like continuation may have high probability. The corpus method suffers from analogous problems, but an exact-count design can explicitly demand a large context denominator and a concentrated set of alternatives before acting.

Using probabilities from the **same model that generated the text** is also a weaker independent check than using a separate model or corpus: a model can naturally assign high probability to the same mistake it produced. That is a logical reason—not a claim that this happens universally—to prefer an independent scorer.

### Contrastive substitution scoring

The most appropriate neural comparison is not raw perplexity but **contrastive scoring**:

\[
\Delta =
S(\text{sentence with candidate})
-
S(\text{sentence with original}).
\]

This is precisely what both classical trigram correction and MLM candidate rescoring naturally support. Islam and Inkpen effectively perform the corpus version by comparing candidate versus original n-gram frequencies; MLM scoring makes the same operation possible using contextual probabilities. citeturn12view0turn26search5

The proposed corpus-veto architecture is therefore best understood as a **contrastive lexical substitution system with an explicit abstention prior**, not as an ordinary grammar checker.

## What an implementation should retain and what should change

The prior art suggests that the proposal is technically sound, but a literal recreation of a 2009 trigram corrector would miss several requirements.

### The anomaly statistic should model context reliability explicitly

A robust decision should depend on at least four quantities:

\[
c_0=c(L,x,R),
\]

\[
N=\sum_m c(L,m,R),
\]

\[
c_*=\max_{m\ne x}c(L,m,R),
\]

and the concentration of the conditional distribution

\[
P(m\mid L,R).
\]

A candidate is much more compelling when, for example,

```text
N(left,right)       = 8,400
original count      = 1
candidate A count   = 7,600
candidate B count   = 310
everything else     = small
```

than when

```text
N(left,right)       = 8,400
original count      = 1
1,500 different middles each occur a few times
```

even though the original frequency is identical.

Thus a good detector should include not only rarity but **context support and distribution concentration**, perhaps via entropy, top-candidate share, or a likelihood ratio:

\[
R=\frac{c_*+\alpha}{c_0+\alpha}.
\]

An edit could then require simultaneously:

\[
N>T_N,\quad
P(x\mid L,R)<T_p,\quad
R>T_R,\quad
P(y\mid L,R)>T_y.
\]

The exact thresholds should be calibrated against the false-positive target rather than chosen linguistically.

### Surface and lemma evidence should be combined conservatively

The Gigafida resources make parallel form/lemma evidence practical. citeturn20view0turn20view1

A particularly useful policy is asymmetric:

* strong surface anomaly **without** lemma anomaly → suspect inflection/sparsity; abstain or ask a morphology model;
* strong lemma anomaly **and** strong surface anomaly → much stronger lexical-error signal;
* good lemma context but wrong morphological features → grammatical/morphological error rather than lexical-choice error;
* replacement lemma is strongly supported but proposed surface inflection is not → reject that surface candidate.

This distinction is particularly important for Slovenian because one underlying lexeme has many inflected realizations; Sloleks exists specifically to encode that relation. citeturn24search1turn24search6

### Morphosyntactic compatibility should probably precede corpus ranking

An LLM may propose a semantically appropriate lemma in the wrong case, number, gender or person. A candidate should therefore pass something like

\[
\text{MSD}(y) \approx \text{required MSD at position }i
\]

before a high lexical frequency is allowed to win.

The existing Gigafida resources already expose morphosyntactic-tagged n-grams, and Sloleks provides the form–lemma–grammar relation. citeturn20view0turn24search1 This is one place where a Slovenian implementation could improve substantially on old English trigram correctors.

### Exact immediate neighbors cannot be the only context

If the assumed error rate is 5–10% per word and errors were approximately independent, the probability that at least one of the two immediate neighbors is also erroneous would be:

\[
1-(1-0.05)^2=9.75\%
\]

at 5%, and

\[
1-(1-0.10)^2=19\%
\]

at 10%.

So a detector that absolutely depends on both adjacent words being correct can lose a nontrivial fraction of anomalies.

Useful fallbacks include ordinary left/right bigrams, longer n-grams when available, lemma n-grams, POS/MSD patterns, dependency collocations and a masked-LM score. Gigafida already provides 2–5-gram and collocational resources from which several of those signals can be built. citeturn20view0turn2search10

### The downloadable Gigafida n-grams are excellent for a prototype, not a complete detector

The 2/million cutoff creates an interesting opportunity. A first version can deliberately operate only where the downloadable table has coverage. Since every represented trigram is extremely frequent, its interventions can be spectacularly conservative. citeturn20view0

That version could be implemented with very little infrastructure:

```text
1. Load Gigafida 2.0 trigram TSV.
2. Create:
       (left, right) -> sorted [(middle, count)]
3. Do the same for lemma-containing records.
4. Run text through Slovene tokenization/lemmatization.
5. Ignore protected spans.
6. Flag only contexts in the high-frequency index.
7. Require a very large candidate/original evidence margin.
8. Ask the LLM for one-word replacements only after flagging.
9. Reject any candidate not independently stronger in:
       surface context,
       lemma context,
       morphology.
```

What it **cannot** safely do is interpret “not present in the CLARIN file” as “zero occurrences in Gigafida.” The repository's explicit frequency cutoff makes that invalid. citeturn20view0

### Named entities and domain language need an explicit abstention layer

Current Gigafida 2.2 reaches only about 1.16 billion words and remains a curated reference corpus with a particular time/domain distribution; Gigafida 2.0 contains texts only through 2018. citeturn22search4turn22search5 This makes proper names, newly coined terminology, software/API names, scientific language and recent events predictable false-positive zones.

A production system should therefore regard any of the following as *negative evidence for editing* even when the trigram is strange: named-entity status, mixed case inside a word, digits, URI/email structure, programming syntax, recently coined terminology, document-local repeated terminology and low overall corpus frequency of either neighbor.

A more contemporary resource such as Trendi could supplement Gigafida for recent vocabulary. CLARIN.SI already distributes Trendi word-level n-gram frequency data. citeturn23search27

### Semantic errors remain the hardest blind spot

Consider an LLM sentence whose wrong word forms a perfectly ordinary phrase:

> “The company **increased** the price from €100 to €80.”

Every local collocation may be completely normal. No n-gram method can infer from local lexical frequency that *decreased* is semantically required by the numbers.

Likewise, discourse-level reference errors, factual mistakes and antonym mistakes in locally common constructions need semantic/world reasoning. This is where a masked LM, NLI-style model or LLM judge has an inherent advantage.

The right design is therefore not “n-grams replace neural models.” It is:

> **use corpus statistics for the subset of errors on which corpus statistics can provide unusually strong, independently inspectable evidence, and abstain elsewhere.**

That is exactly compatible with your low-recall/high-precision objective.

## Novelty assessment and closest precedents

The answer depends strongly on what is claimed as the contribution.

### What would not be genuinely new

These ideas are clearly established prior art:

**Detecting a valid dictionary word that is wrong in context.** That is the classical real-word/context-sensitive spelling-correction problem. citeturn25search0turn10view0

**Using trigram frequency to choose among valid alternatives.** This dates back through the classical context-sensitive spelling literature. citeturn25search0turn25search20

**Holding both neighbors fixed and enumerating alternative middle words from a massive corpus.** Islam and Inkpen 2009 do essentially this directly. citeturn12view0turn12view1

**Using an n-gram system conservatively to resolve frequently confused valid words.** LanguageTool is a production precedent. citeturn13search1turn13search5

**Making local corrections rather than free rewriting.** GECToR is an explicit modern example. citeturn26search0

**Scoring a word bidirectionally by masking it.** MLM pseudo-log-likelihood and related scoring techniques already provide the neural analogue. citeturn26search1turn26search5

**Contextual Slovene spelling-error detection with SloBERTa.** SloNSpell exists and is openly released. citeturn27search2turn26search2

**Building unigram/lemma/2–5-gram statistics from Gigafida.** CJVT/CLARIN.SI already did so and distributes them. citeturn20view0turn20view1

A project that simply downloads the Gigafida trigrams, indexes them as `(left,right)->middle`, and replaces low-frequency middle words with high-frequency ones is therefore **mostly implementation of established ideas**.

### What appears genuinely distinct in the proposed combination

I did not find the following combination as an existing Slovenian system, nor as one unified architecture in the broader prior art reviewed:

**Open-world rather than confusion-set detection.** Every natural-language token is eligible for inspection; candidates arise dynamically rather than from manually supplied pairs.

**A context-reliability criterion separate from original-trigram rarity.** The important statistic is not merely “the trigram is absent,” but “the surrounding slot has very high support and a sharply concentrated alternative distribution.”

**Parallel surface-form and lemma evidence with morphology-aware abstention.** The available Gigafida/Sloleks infrastructure makes this particularly natural in Slovenian. citeturn20view0turn20view1turn24search1

**Separation of detection and generation.** A cheap deterministic detector operates on every token; an expensive LLM is called only for a tiny set of suspicious positions.

**Constrained LLM authority.** The LLM is not asked to rewrite or even decide whether a passage is bad. It receives a fixed target position and proposes only one-word alternatives.

**Independent corpus veto after neural generation.** The LLM's favorite answer is *not sufficient*. A replacement is accepted only if reference-corpus evidence independently favors it by a large margin.

**Optimization explicitly for damage avoidance.** The relevant objective is not conventional GEC \(F_1\), but something closer to “how many already-correct words did the system unnecessarily change per million tokens?” LanguageTool's high-precision philosophy supports the practical desirability of such an operating point, but it is not the same open-world architecture. citeturn13search5

**Evaluation on LLM-generated Slovenian lexical-selection errors.** SloNSpell evaluates spelling-oriented synthetic and human datasets, while Šolar/GEC work targets learner writing. Neither is the same error distribution. citeturn27search2turn26search11

That last point could be scientifically important. A benchmark built by taking mostly-good Slovenian LLM output, having expert annotators mark only genuinely inappropriate lexical choices, and measuring edit precision at very low intervention rates could itself fill a gap.

### The strongest research framing

The technically defensible research question is not:

> “Can n-grams detect a wrong word?”

That is settled prior art.

It is closer to:

> **Can an independently corpus-grounded, morphology-aware abstention layer reduce lexical-selection errors in otherwise fluent Slovenian LLM output while preserving virtually all correct tokens, and does corpus-gated one-token LLM repair outperform either corpus-only correction or neural/LLM proofreading at an equal false-edit budget?**

That gives several meaningful experiments:

\[
\text{Corpus only}
\]

versus

\[
\text{SloBERTa/MLM only}
\]

versus

\[
\text{LLM proofreader}
\]

versus

\[
\text{corpus detector}\rightarrow
\text{LLM candidates}\rightarrow
\text{corpus veto}.
\]

The key evaluation curve should be **recall as a function of false edits**, or precision/coverage at increasingly strict abstention thresholds, rather than only conventional overall accuracy. A system that catches only 20–30% of genuine lexical errors but makes one false edit in tens of thousands of correct tokens may be substantially more useful for your stated application than a normal GEC system with much higher recall.

### Overall verdict

**Would implementing this for Slovenian be genuinely new engineering/research?**

**As engineering: yes.** There does not appear to be a ready-made Slovenian tool implementing the complete pipeline. You would need to construct the anomaly index, combine surface/lemma/MSD evidence, calibrate sparse-context abstention, implement safe token/span handling, control LLM candidate generation, and build independent post-generation acceptance logic.

**As an algorithmic idea: only partly.** The foundational method—context-sensitive real-word correction using trigram statistics, including fixed left/right neighbors with alternative middle tokens—is established and particularly closely anticipated by Islam & Inkpen 2009. citeturn12view0turn12view1

**As Slovenian corpus engineering: easier than it initially appears.** Gigafida frequency and 2–5-gram products, lemma/morphosyntactic information, Sloleks, LIST and modern Slovenian neural models already provide much of the substrate. citeturn20view0turn20view1turn27search2

**As research: potentially yes, with the right claim.** The most credible novelty is the *combination and operating objective*: open-world lexical anomaly detection + explicit context-support statistics + surface/lemma morphology + selective one-token LLM proposal + independent corpus veto + extreme precision/abstention, evaluated specifically on LLM-generated Slovenian. I found no evidence of that exact architecture in the prior art reviewed.

There is also one practical surprise that materially changes the project estimate: **CLARIN's ready-made Gigafida n-gram package is not sufficient by itself for a full detector because its 2-per-million cutoff eliminates everything below roughly 2,269 occurrences in Gigafida 2.0.** It is excellent for a first ultra-conservative proof of concept, but a serious coverage-oriented system would need lower-threshold corpus statistics, corpus-query access, or a complementary model/resource. citeturn20view0turn22search2

The closest intellectual lineage is therefore:

\[
\boxed{
\text{classical real-word trigram correction}
+
\text{Slovene morphology/resources}
+
\text{modern constrained LLM candidate generation}
+
\text{independent corpus acceptance gate}
}
\]

Of those four elements, the first two are well established and largely available; the third is technically straightforward with present LLMs; **the fourth, together with strict abstention and the LLM-output-specific evaluation regime, is where the proposed system is most differentiated.**

### Primary sources and resources

The most directly relevant primary links are:

[Islam & Inkpen, *Real-Word Spelling Correction using Google Web 1T 3-grams*, EMNLP 2009](https://aclanthology.org/D09-1129/) — the closest precedent to the `(left,right) → middle` mechanism. citeturn10view0turn12view0

[Golding & Schabes, *Combining Trigram-Based and Feature-Based Methods for Context-Sensitive Spelling Correction*, ACL 1996](https://aclanthology.org/P96-1010/) — foundational context-sensitive real-word/confusion-set work. citeturn25search0

[Gigafida 2.0 word-level n-gram frequency lists, CLARIN.SI](https://www.clarin.si/repository/xmlui/handle/11356/1274) — public 2–5-gram lists with form/lemma/morphosyntactic variants and corpus statistics. citeturn20view0

[Gigafida 2.0 word-frequency lists, CLARIN.SI](https://www.clarin.si/repository/xmlui/handle/11356/1273) — surface-form and lemma unigram information. citeturn20view1

[Gigafida current corpus interface](https://viri.cjvt.si/gigafida/en) — currently Gigafida 2.2, approximately 1.16B words. citeturn22search4turn22search18

[Gigafida 2.0 paper, LREC 2020](https://aclanthology.org/2020.lrec-1.409/) — reference-corpus design and construction. citeturn22search20

[SloNSpell paper, *Neural Spell-Checker: Beyond Words with Synthetic Data Generation*](https://arxiv.org/abs/2410.23514) — current contextual Slovenian spelling detector based on SloBERTa. citeturn27search2

[SloNSpell source](https://github.com/matejklemen/slonspell) and [released SloBERTa spelling model](https://huggingface.co/cjvt/SloBERTa-slo-word-spelling-annotator). citeturn26search2turn26search6

[Sloleks project](https://www.cjvt.si/en/research/cjvt-projects/sloleks-morphological-lexicon-of-slovene/) — Slovenian morphology and inflection infrastructure. citeturn24search6

[GECToR, *Grammatical Error Correction: Tag, Not Rewrite*](https://aclanthology.org/2020.bea-1.16/) and [official code](https://github.com/grammarly/gector) — modern local-edit alternative to rewriting. citeturn26search0turn26search4

[Salazar et al., *Masked Language Model Scoring*, ACL 2020](https://aclanthology.org/2020.acl-main.240/) and [MLM-scoring code](https://github.com/awslabs/mlm-scoring) — the main neural analogue of contextual conditional scoring. citeturn26search1turn26search9

[Clark et al., *ELECTRA: Pre-training Text Encoders as Discriminators Rather Than Generators*](https://openreview.net/forum?id=r1xMH1BtvB) — token-level replaced-token detection, conceptually relevant to contextual misuse detection. citeturn25search6

[LanguageTool source](https://github.com/languagetool-org/languagetool) — production evidence that large n-gram statistics can be used for high-precision valid-word/confusion checks. citeturn13search1turn13search5turn14search0