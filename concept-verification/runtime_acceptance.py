"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.
Runtime lexical acceptance policy (order 028-a).

One identical runtime policy serves BOTH individual validation
(proxy.RepairEngine per-proposal acceptance) and composed-result
validation (composed_validation._revalidate), routed through this
single callable: the same stale-coordinate, whole-token mapping,
protection, barrier, grapheme, size, lexical-shape, unigram,
contiguous-context and anchored-comparison rules apply at both
stages.  ``repair.accept`` and ``repair.apply_edits`` stay frozen;
only the acceptance routing changes.

Policy (order 028-a, requirements 2-5; uncalibrated contained
engineering policy, not a quality result):

1. Structural guards, no corpus queries, labels preserved:
   stale-candidate-bounds, stale-neighbor-bounds, protected,
   barrier-between-neighbor, reviewer-kept, wider-or-identity,
   control-or-newline, grapheme-sensitive-replacement, markup,
   replacement-size (1-4 words, sum of word lengths <= 80).

2. Whole-token mapping proof (order 028-a, R2/R3): the candidate
   span must be tiled by actual frozen ``tokenize`` tokens - some
   token starts exactly at the span start, a token ends exactly at
   the span end, and no token straddles a span boundary.  Each
   claimed external neighbor must be the exact frozen token
   IMMEDIATELY adjacent to the whole span in the frozen
   tokenization - the token directly before the span's first token
   (left) or directly after the span's last token (right).  A
   same-key token elsewhere (a skipped intervening word, or the
   same key from another occurrence) cannot supply the adjacency
   evidence, a partial word (the span "alpha" inside "alphabeta")
   or a neighbor claimed from inside the target is stale, and
   missing or unproved bounds cannot manufacture support.

3. R2 lexical-unit gate on the raw (unnormalized) bytes: every
   whitespace-split replacement unit AND every original-span word
   must be a maximal frozen-tokenizer shape (``WORD_RE.fullmatch``)
   whose characters are all Unicode letters (category L*) or one
   of the tokenizer's own internal joiners (ASCII apostrophe,
   typographic apostrophe, ASCII hyphen).  Numeric No/Nl shapes
   (superscript two, Roman numerals, vulgar fractions), digits,
   underscores, paths, markup and machine fragments are rejected
   even when a synthetic or malicious vocabulary contains them,
   and a tokenizer-split shape such as "foo—bar" (em dash) is not
   one lexical unit of the actual tokenization.  Labels:
   replacement-not-lexical, original-span-not-lexical (original
   spans are at most 4 words).

4. Every replacement word requires an EXACT unigram row with a
   positive count (a known zero or missing row is not known):
   replacement-unigram-uncertain.

5. Route selection.  A single-word original whose unigram is EXACT
   positive uses the ordinary R4 route (even when orthographically
   close to the replacement).  A single-word original whose
   unigram is UNAVAILABLE or nonpositive uses the narrow R5
   possible-typo route when the casefolded replacement differs by
   exactly ONE code-point insertion/deletion/substitution and both
   units have at least 3 code points; otherwise it uses R4 as a
   distant unknown.  The original unigram determines ONLY the
   R4/R5 classification - it is never a threshold baseline.
   Multiword originals have no corpus unigram as a unit, so R4
   applies.  The unknown original stays unknown - never proved
   malformed or zero.

6. R3/R4 anchored context evaluation, deterministic query order:
   - a multiword replacement first proves every internal
     replacement bigram/trigram EXACT positive (a known zero or
     censored internal adjacency is not positive support);
   - then the comparable fixed-anchor original/replacement
     context pairs at the SAME ngram order are queried replacement
     side first, and the original side only when the replacement
     side is a positive EXACT row (an unknown replacement context
     is neutral for single words - R4 still needs at least one
     factor-two comparison and no weaker known comparison; for a
     multiword replacement every ELIGIBLE external boundary whose
     neighbor is proved is REQUIRED phrase support, so a
     censored/missing boundary adjacency rejects rather than
     neutralizing):
     * single word: left pair (L r)/(L o), right pair (r R)/(o R),
       trigram (L r R)/(L o R) - only the proved immediate
       neighbors;
     * same word count >= 2: the external boundary pairs
       (L r1)/(L o1) and (rm R)/(o_last R) are required positive
       phrase support (when the neighbor is proved) and may also
       support by the factor-two comparison.  The internal
       positional pairs (ri rj)/(oi oj) anchor support only when
       at least one same-position word is ACTUALLY UNCHANGED
       inside the comparable ngram - a wholly rewritten internal
       ngram has no fixed anchor and can only oppose, never
       support (an anchorless same-count phrase cannot be
       authorized by raw whole-phrase frequency);
     * changed word count: BOTH proved external anchors are
       required (a missing neighbor rejects), and only the two
       boundary pairs are compared - each is required positive
       phrase support, and each may support by the factor-two
       comparison.  NEVER a left+first+last+right spanning
       trigram for a multiword replacement, and never
       different-length whole-phrase raw counts.
   - verdict per pair: a non-EXACT replacement context is
     neutral for an ordinary single-word pair (CENSORED/
     UNAVAILABLE stays unknown, not zero) but REJECTS an
     eligible multiword boundary (required phrase support); a
     known zero/nonpositive replacement context is opposing
     evidence (immediate reject, no further queries).  A
     positive EXACT replacement context supports ONLY against a
     matching EXACT original context of the SAME ngram order
     with the factor-two margin candidate_count >= 2 *
     max(original_context_count, 1), and never below the known
     corresponding original context count (a weaker known local
     context opposes).  An unknown original context supplies NO
     ordinary-route support - no floor, no inferred count.
     Under the narrow R5 possible-typo route a single EXACT
     positive adjacent count (count 1 suffices) is positive
     support, NOT subject to the factor-two floor, and the
     original side is consulted only to oppose a known larger
     original context.
   - the first opposing pair rejects immediately; support is
     recorded and later pairs can still oppose; accept iff at
     least one supporting pair and none opposing.  Accept labels:
     accepted-independent-evidence (R4) or accepted-possible-typo
     (R5).

Query budget: only the owned RuntimeCorpus read-only interface is
used (one unigram per replacement word, at most one unigram for a
single-word original, one ngram per side of each available pair);
no cache/index construction, no extra connection, no direct
SQLite bypass.  A known technical/budget failure
(RuntimeCorpusError) propagates untouched for the caller's
late-abort path.
"""

from __future__ import annotations

import re
import unicodedata

from detector import WORD_RE, Candidate, tokenize
from pandoc_protection import grapheme_sensitive
from protected import Interval, is_protected
from qwen_client import Proposal
from repair import Acceptance

from corpus import Corpus, Evidence

# Fixed content-free reason labels added by order 028-a.
REPLACEMENT_NOT_LEXICAL = "replacement-not-lexical"
ORIGINAL_SPAN_NOT_LEXICAL = "original-span-not-lexical"
ACCEPTED_POSSIBLE_TYPO = "accepted-possible-typo"

# Internal joiners consistent with the frozen tokenizer: WORD_RE
# joins letter runs with the ASCII apostrophe, the typographic
# apostrophe or the ASCII hyphen only; any other Unicode Pd (for
# example the em dash) SPLITs the frozen token, so a unit
# containing it is not one lexical unit of the actual
# tokenization.
_JOINERS = frozenset({"'", "\u2019", "-"})

# One context pair: (replacement key, original key, ngram length,
# may this pair support, is this an eligible multiword boundary
# whose replacement side must be an EXACT positive row).
_PAIR = tuple[str, str, int, bool, bool]


def is_lexical_unit(unit: str) -> bool:
    """True iff ``unit`` is one frozen tokenizer unit composed solely
    of Unicode letter runs (category L*) joined by single internal
    apostrophe/hyphen joiners from the tokenizer's own joiner class
    (order 028-a, R2).

    Both conditions are checked on the raw bytes, with no
    casefold/normalization:

    * ``WORD_RE.fullmatch`` proves the unit is a maximal frozen
      token shape - digits, underscores, paths, symbols and any
      non-joiner punctuation fail here, and a tokenizer-split shape
      (em dash) fails because the tokenizer produces two tokens;
    * the letter-only pass rejects the numeric word characters
      ``WORD_RE`` itself admits (No/Nl shapes such as superscript
      two, Roman numerals and vulgar fractions, including embedded
      in a longer unit), so a synthetic or malicious vocabulary
      cannot certify them as words.
    """
    if not unit or WORD_RE.fullmatch(unit) is None:
        return False
    return all(
        char in _JOINERS or unicodedata.category(char).startswith("L")
        for char in unit
    )


def _one_codepoint_edit(a: str, b: str) -> bool:
    """True iff exactly ONE code-point insertion, deletion or
    substitution converts ``a`` into ``b`` (order 028-a, R5)."""
    length_a, length_b = len(a), len(b)
    if length_a == length_b:
        return sum(1 for x, y in zip(a, b, strict=True) if x != y) == 1
    if abs(length_a - length_b) != 1:
        return False
    if length_a < length_b:
        a, b, length_a, length_b = b, a, length_b, length_a
    # len(a) == len(b) + 1: one deletion of a code point of a.
    index = 0
    while index < length_b and a[index] == b[index]:
        index += 1
    return a[index + 1 :] == b[index:]


def _positive_exact(evidence: Evidence) -> int | None:
    """The count when the row is EXACT with a positive integer
    count, else None (UNAVAILABLE/CENSORED and known zeros are not
    positive support; order 028-a, R3)."""
    if (
        evidence.state == "EXACT"
        and isinstance(evidence.count, int)
        and evidence.count > 0
    ):
        return evidence.count
    return None


def _classify_pair(
    replacement: Evidence,
    original: Evidence,
    *,
    typo_route: bool,
) -> str:
    """Classify one comparable fixed-anchor pair as 'opposing',
    'supporting' or 'neutral'.

    The replacement side decides first: a non-EXACT context stays
    unknown (neutral; the caller never queried the original side),
    a known zero or nonpositive count is opposing.  Under the
    ordinary R4 route a positive replacement context supports ONLY
    against a matching EXACT original context of the SAME ngram
    order, by the factor-two margin ``2 * max(original_count, 1)``
    and never below the known corresponding count (a weaker known
    local context opposes); an unknown original context supplies
    NO ordinary-route support.  Under the narrow R5 possible-typo
    route a single EXACT positive adjacent count (count 1 suffices)
    is positive support, not subject to the factor-two floor, and
    the original side opposes only when it is a known larger count.
    """
    if replacement.state != "EXACT" or replacement.count is None:
        return "neutral"
    if replacement.count <= 0:
        return "opposing"
    if typo_route:
        if (
            original.state == "EXACT"
            and original.count is not None
            and replacement.count < original.count
        ):
            return "opposing"
        return "supporting"
    if original.state != "EXACT" or original.count is None:
        return "neutral"
    if replacement.count < original.count:
        return "opposing"
    if replacement.count >= 2 * max(original.count, 1):
        return "supporting"
    return "neutral"


def _evaluate_pairs(
    corpus: Corpus,
    pairs: list[_PAIR],
    *,
    internal: dict[str, Evidence],
    typo_route: bool,
) -> bool:
    """Evaluate the comparable fixed-anchor pairs in fixed order.

    Returns True when at least one pair supports and no pair
    opposes; the first opposing pair rejects before any further
    query.  The replacement side is queried first; the original
    side is queried only for a positive EXACT replacement context
    (an unknown replacement context is neutral for an ordinary
    single-word pair, so its original side is never queried).  An
    eligible multiword boundary pair (flagged by the pair tuple)
    whose replacement side is not an EXACT positive row rejects
    immediately: the required phrase support is missing and the
    absence stays unknown, never a fabricated zero or a neutral.
    Pairs flagged as unable to support (wholly rewritten internal
    positional ngrams - no fixed anchor) can only oppose.  Proven
    internal replacement ngrams are reused from ``internal``
    instead of re-queried.
    """
    supported = False
    for replacement_key, original_key, length, can_support, boundary in pairs:
        replacement = internal.get(replacement_key)
        if replacement is None:
            replacement = corpus.ngram(replacement_key, length)
        if replacement.state != "EXACT" or replacement.count is None:
            if boundary:
                # Required multiword boundary support missing:
                # unknown, not zero, and not neutralizable.
                return False
            continue  # CENSORED/UNAVAILABLE stays unknown, not zero
        if replacement.count <= 0:
            return False  # known nonpositive: opposing, stop
        original = corpus.ngram(original_key, length)
        verdict = _classify_pair(replacement, original, typo_route=typo_route)
        if verdict == "opposing":
            return False
        if can_support and verdict == "supporting":
            supported = True
    return supported


def _internal_anchored(
    original: list[str], words: list[str], index: int, length: int
) -> bool:
    """True iff the internal positional ngram at ``index`` (of
    ``length`` same-position words) contains at least one ACTUALLY
    UNCHANGED word: only then is it a fixed-anchor comparison that
    may support; a wholly rewritten internal ngram cannot anchor
    support (order 028-a, R3/R4)."""
    return any(
        original[index + offset] == words[index + offset]
        for offset in range(length)
    )


def accept(
    text: str,
    candidate: Candidate,
    proposal: Proposal,
    corpus: Corpus,
    intervals: list[Interval],
    *,
    left: str | None = None,
    right: str | None = None,
    left_bounds: tuple[int, int] | None = None,
    right_bounds: tuple[int, int] | None = None,
) -> Acceptance:
    """The single runtime acceptance policy (order 028-a, R1-R5).

    Same call/return surface as the frozen historical
    ``repair.accept``; the composed-validation pass routes to this
    same callable so individual and combined stages cannot drift.
    """
    # Stale-coordinate validation (order 013-a, requirement 14):
    # candidate and neighbor tokens must still match the exact
    # original slices before any acceptance decision.  Bounds are
    # validated before any slicing so negative or oversized
    # coordinates cannot match by Python slice semantics.
    if not 0 <= candidate.start < candidate.end <= len(text):
        return Acceptance(False, "stale-candidate-bounds", None)
    if text[candidate.start : candidate.end] != candidate.text:
        return Acceptance(False, "stale-candidate-bounds", None)
    # Whole-token span proof (order 028-a, R2/R3): the span must be
    # tiled by actual frozen tokens; a partial word ("alpha" inside
    # "alphabeta") is stale candidate bounds.
    tokens = tokenize(text, intervals)
    start_index = next(
        (i for i, token in enumerate(tokens) if token.start == candidate.start),
        None,
    )
    if start_index is None:
        return Acceptance(False, "stale-candidate-bounds", None)
    end_index = start_index
    while end_index < len(tokens) and tokens[end_index].end < candidate.end:
        end_index += 1
    if end_index >= len(tokens) or tokens[end_index].end != candidate.end:
        return Acceptance(False, "stale-candidate-bounds", None)
    # Stale-neighbor validation plus the IMMEDIATE-adjacent frozen
    # token proof (order 028-a, R2/R3): each claimed neighbor must
    # be the exact token directly adjacent to the whole span in the
    # frozen tokenization.  A same-key token elsewhere - a skipped
    # intervening word or the same key from another occurrence -
    # cannot supply the adjacency evidence.  A neighbor key without
    # proved bounds is unproved adjacency and cannot be used for
    # support.
    if left is not None and left_bounds is not None:
        left_start, left_end = left_bounds
        if not 0 <= left_start < left_end <= len(text):
            return Acceptance(False, "stale-neighbor-bounds", None)
        # Neighbor tokens arrive as tokenizer keys (casefolded);
        # compare the original slice under the same convention.
        if text[left_start : left_end].casefold() != left:
            return Acceptance(False, "stale-neighbor-bounds", None)
        if start_index == 0:
            return Acceptance(False, "stale-neighbor-bounds", None)
        adjacent = tokens[start_index - 1]
        if (left_start, left_end) != (adjacent.start, adjacent.end):
            return Acceptance(False, "stale-neighbor-bounds", None)
    elif left is not None:
        left = None
    if right is not None and right_bounds is not None:
        right_start, right_end = right_bounds
        if not 0 <= right_start < right_end <= len(text):
            return Acceptance(False, "stale-neighbor-bounds", None)
        if text[right_start : right_end].casefold() != right:
            return Acceptance(False, "stale-neighbor-bounds", None)
        if end_index + 1 >= len(tokens):
            return Acceptance(False, "stale-neighbor-bounds", None)
        adjacent = tokens[end_index + 1]
        if (right_start, right_end) != (adjacent.start, adjacent.end):
            return Acceptance(False, "stale-neighbor-bounds", None)
    elif right is not None:
        right = None
    if is_protected(candidate.start, candidate.end, intervals):
        return Acceptance(False, "protected", None)
    # Context barrier at acceptance: protected content strictly
    # between a neighbor token and the candidate invalidates the
    # adjacency evidence.
    if left_bounds is not None and any(
        left_bounds[1] <= item.start and item.end <= candidate.start
        for item in intervals
    ):
        return Acceptance(False, "barrier-between-neighbor", None)
    if right_bounds is not None and any(
        candidate.end <= item.start and item.end <= right_bounds[0]
        for item in intervals
    ):
        return Acceptance(False, "barrier-between-neighbor", None)
    if proposal.keep:
        return Acceptance(False, "reviewer-kept", None)
    replacement = proposal.replacement
    if proposal.needs_wider_edit or not replacement or replacement == candidate.text:
        return Acceptance(False, "wider-or-identity", None)
    if "\n" in replacement or "\r" in replacement or any(
        ord(char) < 32 for char in replacement
    ):
        return Acceptance(False, "control-or-newline", None)
    # The replacement must be grapheme-stable throughout: a
    # combining mark or joiner anywhere in it (e.g. a mid-word NFD
    # sequence) is unproved.
    if any(grapheme_sensitive(char) for char in replacement):
        return Acceptance(False, "grapheme-sensitive-replacement", None)
    if re.search(r"[`<>\[\]{}]", replacement):
        return Acceptance(False, "markup", None)
    words = replacement.casefold().split()
    if not 1 <= len(words) <= 4 or sum(len(word) for word in words) > 80:
        return Acceptance(False, "replacement-size", None)
    # R2 lexical-unit gate on the raw bytes (no normalization):
    # symbols, digits, No/Nl numeric shapes, paths/configuration,
    # markup and machine fragments cannot become valid words even
    # when a synthetic or malicious vocabulary contains them.
    if not all(is_lexical_unit(word) for word in replacement.split()):
        return Acceptance(False, REPLACEMENT_NOT_LEXICAL, None)
    # Target lexical spans are at most 4 words, each an actual
    # lexical unit; a nonlexical or oversize target span is not a
    # word/phrase change this policy can validate.
    original_raw = candidate.text.split()
    if not 1 <= len(original_raw) <= 4 or not all(
        is_lexical_unit(word) for word in original_raw
    ):
        return Acceptance(False, ORIGINAL_SPAN_NOT_LEXICAL, None)
    # EXACT positive candidate unigram counts, not merely EXACT: a
    # known zero or missing row cannot certify the replacement word.
    for word in words:
        if _positive_exact(corpus.unigram(word)) is None:
            return Acceptance(False, "replacement-unigram-uncertain", None)
    original = [word.casefold() for word in original_raw]
    count_original = len(original)
    count_replacement = len(words)
    # Route selection (R4/R5): the original unigram determines ONLY
    # the route, never a threshold.  Corpus-known positive originals
    # use R4 even when orthographically close; an unknown/nonpositive
    # single-word original takes the narrow possible-typo route when
    # exactly one code point apart (both units >= 3 code points),
    # else R4 as a distant unknown.  Multiword originals have no
    # unit unigram, so R4 applies.
    typo_route = False
    if count_original == 1 and count_replacement == 1:
        original_unigram = _positive_exact(corpus.unigram(original[0]))
        if original_unigram is None and (
            _one_codepoint_edit(original[0], words[0])
            and len(original[0]) >= 3
            and len(words[0]) >= 3
        ):
            typo_route = True
    # R3: every internal replacement bigram/trigram must have
    # positive independent support; proven once, reused as the
    # replacement side of the internal positional comparisons.
    internal: dict[str, Evidence] = {}
    if count_replacement >= 2:
        for index in range(count_replacement - 1):
            phrase = f"{words[index]} {words[index + 1]}"
            evidence = corpus.ngram(phrase, 2)
            internal[phrase] = evidence
            if _positive_exact(evidence) is None:
                return Acceptance(False, "local-evidence-not-stronger", None)
        for index in range(count_replacement - 2):
            phrase = f"{words[index]} {words[index + 1]} {words[index + 2]}"
            evidence = corpus.ngram(phrase, 3)
            internal[phrase] = evidence
            if _positive_exact(evidence) is None:
                return Acceptance(False, "local-evidence-not-stronger", None)
    # Comparable fixed-anchor context pairs, fixed evaluation order.
    # Pair tuple: (replacement key, original key, ngram length, may
    # support, eligible multiword boundary requiring an EXACT
    # positive replacement side).
    pairs: list[_PAIR] = []
    if count_original == 1 and count_replacement == 1:
        if left is not None:
            pairs.append((f"{left} {words[0]}", f"{left} {original[0]}", 2, True, False))
        if right is not None:
            pairs.append((f"{words[0]} {right}", f"{original[0]} {right}", 2, True, False))
        if left is not None and right is not None:
            pairs.append(
                (
                    f"{left} {words[0]} {right}",
                    f"{left} {original[0]} {right}",
                    3,
                    True,
                    False,
                )
            )
    elif count_original == count_replacement:
        # Same word count: internal positional pairs anchor support
        # only when the comparable ngram keeps at least one
        # same-position word UNCHANGED; a wholly rewritten internal
        # ngram can only oppose, never support.  The external
        # boundary pairs are required positive phrase support and
        # may also support by the factor-two comparison.
        for index in range(count_original - 1):
            internal_key = f"{words[index]} {words[index + 1]}"
            pairs.append(
                (
                    internal_key,
                    f"{original[index]} {original[index + 1]}",
                    2,
                    _internal_anchored(original, words, index, 2),
                    False,
                )
            )
        for index in range(count_original - 2):
            internal_key = f"{words[index]} {words[index + 1]} {words[index + 2]}"
            pairs.append(
                (
                    internal_key,
                    (
                        f"{original[index]} {original[index + 1]} "
                        f"{original[index + 2]}"
                    ),
                    3,
                    _internal_anchored(original, words, index, 3),
                    False,
                )
            )
        if left is not None:
            pairs.append((f"{left} {words[0]}", f"{left} {original[0]}", 2, True, True))
        if right is not None:
            pairs.append((f"{words[-1]} {right}", f"{original[-1]} {right}", 2, True, True))
    else:
        # Changed word count: both proved external anchors are
        # required and only boundary evidence is comparable - each
        # boundary is required positive phrase support - never a
        # spanning trigram and never different-length whole-phrase
        # raw counts.
        if left is None or right is None:
            return Acceptance(False, "local-evidence-not-stronger", None)
        pairs = [
            (f"{left} {words[0]}", f"{left} {original[0]}", 2, True, True),
            (f"{words[-1]} {right}", f"{original[-1]} {right}", 2, True, True),
        ]
    if _evaluate_pairs(corpus, pairs, internal=internal, typo_route=typo_route):
        label = (
            ACCEPTED_POSSIBLE_TYPO
            if typo_route
            else "accepted-independent-evidence"
        )
        return Acceptance(True, label, replacement)
    return Acceptance(False, "local-evidence-not-stronger", None)
