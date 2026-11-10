"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.
Source-compatible runtime detection (order 029-b).

One runtime detector for the runnable proxy.  The legacy unknown/rare
word signal is preserved EXACTLY (UNAVAILABLE unigram 1.0, known count
at most threshold 0.5, the local-context exact-local penalty, round6,
deterministic non-overlap source-ordered bounded selection), and the
corrected source-compatible fixed-anchor contrast adds the
local-context-only WORD alarm (score 0.4) and the grouped 2-4 unit
PHRASE target (score 0.45) produced BEFORE review.  The frozen raw
``detector`` module and its historical callers are untouched; only the
engine import routing changes.

Policy (order 029-b, requirements 1-3; uncalibrated contained
suspicion policy only, not a quality result):

1. Safeguards: same signature/modes/defaults, existing
   Candidate/Token/tokenize, ONE ``_evidence`` pass for ALL raw tokens
   in original order (including units later ineligible for review), so
   the owned RuntimeCorpus keeps the exact SQL schedule of the frozen
   detector.  New signals derive ONLY from the already-collected
   evidence dictionaries: no extra query, no re-query after a raw
   detect, no denominator/probability/entropy, no alternative-unigram
   inference, no automatic replacement.  Unigram-only mode gains no
   context alarms.  Runtime maximum 4 / hard cap 8 with the frozen
   deterministic selection; a safe non-positive maximum returns NO
   targets.  RuntimeCorpus errors and caller control propagate to the
   existing engine boundary untouched.

   Before ANY target assignment - legacy candidates as well as context
   units and anchors - every unit must pass the shared lexical /
   maximal-original / grapheme gate: one frozen lexical unit that is
   not a fragment of a larger machine source unit (no adjoining
   combining mark, grapheme joiner, format or unsafe control
   character, digit or underscore; ordinary prose boundaries stay
   eligible, including ASCII space/tab and the proven LF/CR line
   terminators).  Ineligible units stay in the raw token/evidence
   sequence, so the query budget is unchanged and filtering cannot
   manufacture adjacency or consume the cap.

2. WORD alarm (local-context only, score 0.4): the original and BOTH
   immediate anchors are lowercase lexical source units (frozen
   ``is_lexical_unit``) with EXACT unigram counts above the legacy
   threshold; both actual adjacent original bigrams are EXACT
   POSITIVE; the centered original trigram is EXACT with a known
   nonnegative count C; and the already-fetched fixed-neighbor
   alternatives contain a DISTINCT casefolded middle lexical unit
   with count A >= 2 * max(C, 1).  Identical/casefold-identical or
   non-lexical alternatives never support; CENSORED/UNAVAILABLE
   originals supply no signal and a missing row never means zero.
   Both source gaps contain only ASCII spaces/tabs: no protection,
   punctuation, newline, removed token or unsafe grapheme boundary.

3. PHRASE (score 0.45): maximal source-adjacent runs of actual word
   alarms are grouped BEFORE review.  Source-adjacent means
   consecutive raw tokens joined by a space/tab gap; invalid,
   protected, rare or unknown intervening tokens cannot be removed to
   join alarms, and mere low counts without fixed-anchor contrast are
   never grouped.  A one-unit run stays a word (only within 128
   original code points); a 2-4 unit run within 128 original code
   points becomes ONE exact original slice including its horizontal
   whitespace, with both anchors outside the whole span; an over-4,
   over-128 or otherwise unprovable run leaves ALL its context-only
   alarms unchanged and produces NO targets - never a clipped
   sub-run, never a fallback to component words.  After
   deduplication the complete phrase is preferred over overlapping
   context words by the unchanged bounded deterministic selection
   (sort (-score, start, end), non-overlap, cap min(maximum, 8),
   source-ordered output).  No reviewer-chosen offsets, extension or
   second review; ranked alternatives are never sent to the reviewer.
"""

from __future__ import annotations

import unicodedata

from detector import Candidate, Token, _evidence, tokenize
from pandoc_protection import grapheme_boundary_sensitive
from protected import Interval
from runtime_acceptance import is_lexical_unit

from corpus import Corpus

# Fixed, uncalibrated suspicion policy (order 029-b, R2/R3).
WORD_ALARM_SCORE = 0.4
PHRASE_ALARM_SCORE = 0.45
PHRASE_MAX_UNITS = 4
PHRASE_MAX_CODEPOINTS = 128
HARD_CAP = 8

_HORIZONTAL_GAP = frozenset(" \t")


# Ordinary whitespace boundaries that form their own graphemes and keep
# a full word eligible: ASCII space plus the proven LF/CR/TAB
# terminators (frozen grapheme_boundary_sensitive).
_ORDINARY_WHITESPACE = frozenset(" \t\n\r")

def _horizontal_gap(gap: str) -> bool:
    """True iff the source gap holds only ASCII spaces and tabs."""
    return all(char in _HORIZONTAL_GAP for char in gap)


def _maximal_original_boundary(text: str, start: int, end: int) -> bool:
    """True iff the token is not a fragment of a larger machine source
    unit (order 029-b, R1; A R2): the source character adjoining the
    token on either side (when present) must not be a digit, an
    underscore, a grapheme-joining character (combining mark, ZWJ /
    ZWNJ, variation selector, regional indicator, emoji modifier,
    NEL/LS/PS, NUL, VT, FF - frozen
    ``grapheme_boundary_sensitive``), a format character (Cf) or any
    other unsafe control character.  Ordinary prose boundaries stay
    eligible: ASCII space and tab plus the proven line/column
    terminators LF and CR form their own graphemes."""
    for position in (start - 1, end):
        if 0 <= position < len(text):
            char = text[position]
            category = unicodedata.category(char)
            if (
                char.isdigit()
                or char == "_"
                or grapheme_boundary_sensitive(char)
                or category == "Cf"
                or (category == "Cc" and char not in _ORDINARY_WHITESPACE)
            ):
                return False
    return True


def _target_unit(text: str, token: Token) -> bool:
    """The shared lexical / maximal-original / grapheme gate applied
    before ANY target assignment (order 029-b, R1/R2): the token must
    be one frozen lexical unit and not a fragment of a larger machine
    source unit.  Ineligible units stay in the raw token/evidence
    sequence; they are simply never assigned as targets or context
    support."""
    return is_lexical_unit(token.text) and _maximal_original_boundary(
        text, token.start, token.end
    )


def _positive_exact(record: object) -> int | None:
    """The count when the evidence record is EXACT with a positive
    integer count; UNAVAILABLE/CENSORED states and known zeros are not
    positive support (order 029-b, R2)."""
    if not isinstance(record, dict) or record.get("state") != "EXACT":
        return None
    count = record.get("count")
    if type(count) is not int or count <= 0:
        return None
    return count


def _known_above(record: object, threshold: int) -> bool:
    """True iff the evidence record is EXACT with an integer count
    strictly above ``threshold`` (missing/censored/nonpositive rows
    never qualify)."""
    if not isinstance(record, dict) or record.get("state") != "EXACT":
        return False
    count = record.get("count")
    return type(count) is int and count > threshold


def _word_alarm(
    text: str,
    tokens: list[Token],
    index: int,
    evidence: dict[str, object],
    all_evidence: list[dict[str, object]],
    threshold: int,
) -> bool:
    """The fixed-anchor local-context word alarm (order 029-b, R2).

    Derives ONLY from the already-collected evidence dictionaries of
    the token and its two immediate anchors: it never issues an extra
    query, never uses a denominator or probability, and never treats a
    missing row as a zero.
    """
    token = tokens[index]
    left = tokens[index - 1]
    right = tokens[index + 1]
    for unit in (token, left, right):
        # Lowercase lexical source unit on the raw bytes, plus the
        # shared maximal-original / grapheme gate: a fragment of a
        # larger machine unit never alarms and never anchors.
        if (
            not is_lexical_unit(unit.text)
            or unit.text != unit.text.casefold()
            or not _maximal_original_boundary(text, unit.start, unit.end)
        ):
            return False
    if not _known_above(all_evidence[index - 1]["unigram"], threshold):
        return False
    if not _known_above(evidence["unigram"], threshold):
        return False
    if not _known_above(all_evidence[index + 1]["unigram"], threshold):
        return False
    if _positive_exact(evidence.get("left_bigram")) is None:
        return False
    if _positive_exact(evidence.get("right_bigram")) is None:
        return False
    trigram = evidence.get("trigram")
    if not isinstance(trigram, dict) or trigram.get("state") != "EXACT":
        return False
    centered = trigram.get("count")
    if type(centered) is not int or centered < 0:
        return False
    # Both source gaps must hold only horizontal ASCII whitespace;
    # the open-gap proof (presence of the bigram/trigram/alternatives
    # records) already excludes protected intervals between anchors.
    if not _horizontal_gap(text[left.end : token.start]):
        return False
    if not _horizontal_gap(text[token.end : right.start]):
        return False
    alternatives = evidence.get("alternatives")
    if not isinstance(alternatives, list):
        return False
    center = token.key
    for item in alternatives:
        if (
            not isinstance(item, tuple)
            or len(item) != 2
            or not isinstance(item[0], str)
            or type(item[1]) is not int
        ):
            continue
        middle, alternative_count = item
        if middle.casefold() == center:
            continue  # identical/casefold-identical never supports
        if not is_lexical_unit(middle):
            continue
        if alternative_count >= 2 * max(centered, 1):
            return True
    return False


def _source_adjacent(text: str, tokens: list[Token], first: int, second: int) -> bool:
    """True iff two alarm tokens are consecutive raw tokens joined by
    a space/tab gap: nothing between them may be removed to join the
    run (order 029-b, R3)."""
    return second == first + 1 and _horizontal_gap(
        text[tokens[first].end : tokens[second].start]
    )


def _group_candidates(
    text: str,
    tokens: list[Token],
    alarm_indices: list[int],
    all_evidence: list[dict[str, object]],
) -> list[Candidate]:
    """Group maximal source-adjacent runs of word alarms (order
    029-b, R3): a one-unit run stays a word and a 2-4 unit run within
    the code-point bound becomes ONE exact original slice; an over-4,
    over-128 or otherwise unprovable run leaves ALL its context-only
    alarms unchanged and yields NO targets - never a clipped sub-run
    and never a fallback to component words."""
    runs: list[list[int]] = []
    for index in alarm_indices:
        if runs and _source_adjacent(text, tokens, runs[-1][-1], index):
            runs[-1].append(index)
        else:
            runs.append([index])
    candidates: list[Candidate] = []
    for run in runs:
        first, last = run[0], run[-1]
        span_start = tokens[first].start
        span_end = tokens[last].end
        if span_end - span_start > PHRASE_MAX_CODEPOINTS:
            continue  # overlong run: alarms unchanged, no targets
        if len(run) == 1:
            candidates.append(
                Candidate(
                    tokens[first].start,
                    tokens[first].end,
                    tokens[first].text,
                    WORD_ALARM_SCORE,
                    all_evidence[first],
                )
            )
        elif len(run) <= PHRASE_MAX_UNITS:
            candidates.append(
                Candidate(
                    span_start,
                    span_end,
                    text[span_start:span_end],
                    PHRASE_ALARM_SCORE,
                    {
                        "context_phrase": True,
                        "units": [tokens[index].text for index in run],
                    },
                )
            )
        # A longer run is unprovable as one bounded target: all of its
        # context-only alarms stay unchanged, none becomes a target.
    return candidates


def detect(
    text: str,
    corpus: Corpus,
    intervals: list[Interval] | None = None,
    *,
    mode: str = "local-context",
    threshold: int = 3,
    maximum: int = 4,
) -> list[Candidate]:
    """Source-compatible runtime detection (order 029-b).

    Same signature, modes, defaults and legacy scoring as the frozen
    detector, plus the local-context-only fixed-anchor word alarms and
    grouped phrase targets.  One ``_evidence`` pass for ALL raw tokens
    in original order; the owned corpus keeps the exact SQL schedule
    and nothing is re-queried.
    """
    if mode not in ("unigram-only", "local-context"):
        raise ValueError("unknown detector mode")
    intervals = intervals or []
    tokens = tokenize(text, intervals)
    all_evidence: list[dict[str, object]] = [
        _evidence(corpus, tokens, index, intervals) for index in range(len(tokens))
    ]
    candidates: list[Candidate] = []
    for index, token in enumerate(tokens):
        evidence = all_evidence[index]
        unigram = evidence["unigram"]
        assert isinstance(unigram, dict)
        state = str(unigram["state"])
        count = unigram.get("count")
        score = 0.0
        if state == "UNAVAILABLE":
            score += 1.0
        elif isinstance(count, int) and count <= threshold:
            score += 0.5
        if mode == "local-context":
            exact_local = sum(
                isinstance(value, dict) and value.get("state") == "EXACT"
                for key, value in evidence.items()
                if key.endswith("bigram") or key == "trigram"
            )
            if exact_local:
                score -= min(0.35, 0.1 * exact_local)
        if score <= 0:
            continue
        # Common lexical / maximal-original / grapheme gate BEFORE any
        # target assignment: a nonlexical raw token or a fragment of a
        # larger machine source unit is never a target, and an
        # ineligible unit must not consume the cap or obscure an
        # eligible one.
        if not _target_unit(text, token):
            continue
        candidates.append(
            Candidate(token.start, token.end, token.text, round(score, 6), evidence)
        )
    if mode == "local-context":
        alarm_indices = [
            index
            for index in range(len(tokens))
            if 0 < index < len(tokens) - 1
            and _word_alarm(
                text, tokens, index, all_evidence[index], all_evidence, threshold
            )
        ]
        candidates.extend(_group_candidates(text, tokens, alarm_indices, all_evidence))
    cap = min(maximum, HARD_CAP)
    if cap <= 0:
        return []
    candidates.sort(key=lambda item: (-item.score, item.start, item.end))
    selected: list[Candidate] = []
    for candidate in candidates:
        if any(
            candidate.start < prior.end and candidate.end > prior.start
            for prior in selected
        ):
            continue
        selected.append(candidate)
        if len(selected) >= cap:
            break
    return sorted(selected, key=lambda item: (item.start, item.end))
