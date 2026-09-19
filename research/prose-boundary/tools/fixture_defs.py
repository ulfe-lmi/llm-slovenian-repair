"""008-a frozen fixture definitions (data only).

Every fixture is project-authored synthetic material (no private data, no
owner motivating examples).  ``regions`` declare the EXPECTED STRUCTURAL
SAFETY SEMANTICS, frozen BEFORE any parser output is inspected
(order 008-a requirement 3).

Region location (code points, then converted to byte offsets by
build_fixtures.py):
  start = start of ``start_anchor`` (first occurrence; ``start_anchor_last``
          selects the last occurrence)
  end   = end of ``end_anchor`` (first occurrence; ``end_anchor_last``
          selects the last occurrence)
  ``start_cp`` / ``end_cp`` (optional) override the anchor-derived bounds and
  are required for single-character delimiter regions.
Anchors must occur exactly as written (uniqueness is asserted unless a
``*_anchor_last`` flag is set).

Roles:
  PROSE_CANDIDATE  must be exposed as candidate prose under the frozen policy
  PROTECTED        must never be exposed as candidate prose
  NEUTRAL          no assertion (conservative behaviour recorded as tradeoff)

``role_by_profile`` may override the default role per parser profile.
Profiles (frozen in config/experiment-008a.json):
  P0 = CommonMark core
  P1 = P0 + tables + strikethrough + tasklists + math
  P2 = P1 + YAML-style metadata blocks
"""

FIXTURES = [
    # ---- class 1: plain Slovenian prose ---------------------------------
    dict(
        id="F01", cls=1, cls_name="plain-slovenian-prose",
        text="V Ljubljani je danes sončno in toplo. Zvečer se zadiha rahel vetrič z reke.\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="V Ljubljani", end_anchor="z reke."),
        ],
        note="Whole visible text is prose; the trailing line ending is never prose.",
    ),
    # ---- class 2: prose + inline code ------------------------------------
    dict(
        id="F02", cls=2, cls_name="prose-inline-code",
        text="Uporabi ukaz `git status` preden nadaljuješ.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Uporabi", end_anchor="ukaz "),
            dict(name="inline-code", role="PROTECTED",
                 start_anchor="`git", end_anchor="status`"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor=" preden", end_anchor="nadaljuješ."),
        ],
        note="Inline code span (with delimiters) is structurally protected.",
    ),
    # ---- class 3: multi-backtick inline code ------------------------------
    dict(
        id="F03", cls=3, cls_name="multi-backtick-inline-code",
        text="Vnaprej pripravljeno `` a ` b `` ostane nedotaknjeno.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Vnaprej", end_anchor="pripravljeno "),
            dict(name="inline-code", role="PROTECTED",
                 start_anchor="`` a", end_anchor="b ``"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor=" ostane", end_anchor="nedotaknjeno."),
        ],
        note="Double-backtick code span containing a single backtick.",
    ),
    # ---- class 4: prose + fenced Python ----------------------------------
    dict(
        id="F04", cls=4, cls_name="prose-fenced-python",
        text="Naredi to:\n\n```python\nprint('hello')\n```\n\nNato preveri izhod.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Naredi", end_anchor="to:"),
            dict(name="fence", role="PROTECTED",
                 start_anchor="```python", end_anchor="```", end_anchor_last=True),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Nato", end_anchor="izhod."),
        ],
        note="Fenced block includes delimiters and content; excludes following newline.",
    ),
    # ---- class 5: tilde fences --------------------------------------------
    dict(
        id="F05", cls=5, cls_name="tilde-fences",
        text="Tilne ograje:\n\n~~~\necho x\n~~~\n\nKonec.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Tilne", end_anchor="ograje:"),
            dict(name="fence", role="PROTECTED",
                 start_anchor="~~~\necho", end_anchor="~~~", end_anchor_last=True),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Konec.", end_anchor="Konec."),
        ],
        note="Tilde fenced block.",
    ),
    # ---- class 6: variable-length fences ----------------------------------
    dict(
        id="F06", cls=6, cls_name="variable-length-fences",
        text="Najdaljše ograje:\n\n````\n```\nnotcode\n```\n````\n\nKonec.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Najdaljše", end_anchor="ograje:"),
            dict(name="fence", role="PROTECTED",
                 start_anchor="````", end_anchor="````", end_anchor_last=True),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Konec.", end_anchor="Konec."),
        ],
        note="Four-backtick fence containing literal triple-backtick lines.",
    ),
    # ---- class 7: unfinished fenced code ----------------------------------
    dict(
        id="F07", cls=7, cls_name="unfinished-fenced-code",
        text="Ograja se nikoli ne zaključi:\n\n```\nsam začetek\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Ograja", end_anchor="zaključi:"),
            dict(name="unfenced", role="PROTECTED",
                 start_anchor="```\nsam", end_anchor="sam začetek\n"),
        ],
        note="Malformed: fence never closed; conservative expectation is that the "
             "remainder is still treated as a code block (never exposed as prose).",
    ),
    # ---- class 8: markdown-looking material inside code --------------------
    dict(
        id="F08", cls=8, cls_name="markdown-inside-code",
        text="V kodi oznake niso markdown:\n\n```md\n# Naslov\n**odebeljeno** [link](https://primer.si)\n```\n\nPojasnilo.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="V kodi", end_anchor="markdown:"),
            dict(name="fence", role="PROTECTED",
                 start_anchor="```md", end_anchor="```", end_anchor_last=True),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Pojasnilo.", end_anchor="Pojasnilo."),
        ],
        note="Markdown syntax inside a fenced block must stay protected.",
    ),
    # ---- class 9: math-looking material inside code ------------------------
    dict(
        id="F09", cls=9, cls_name="math-inside-code",
        text="Enačba v kodi:\n\n```\na = b + c\n$ ne_math $\n```\n\nKončno.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Enačba", end_anchor="v kodi:"),
            dict(name="fence", role="PROTECTED",
                 start_anchor="```\na", end_anchor="```", end_anchor_last=True),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Končno.", end_anchor="Končno."),
        ],
        note="Dollar signs inside a fenced block are code, not math.",
    ),
    # ---- class 10: dollar inline math ---------------------------------------
    dict(
        id="F10", cls=10, cls_name="dollar-inline-math",
        text="Veljavnost: $x^2 + 1 = 0$ pomeni ničeln koren.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Veljavnost:", end_anchor=": "),
            dict(name="math", role="PROTECTED",
                 role_by_profile={"P0": "PROSE_CANDIDATE"},
                 start_anchor="$x^2", end_anchor="= 0$"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor=" pomeni", end_anchor="koren."),
        ],
        note="Under P0 (no math extension) the dollars are literal text; under P1/P2 "
             "the span is recognized inline math and must stay protected.",
    ),
    # ---- class 11: dollar display math --------------------------------------
    dict(
        id="F11", cls=11, cls_name="dollar-display-math",
        text="Zapišimo:\n\n$$E = mc^2$$\n\nin nadaljujmo.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Zapišimo:", end_anchor="Zapišimo:"),
            dict(name="display-math", role="PROTECTED",
                 role_by_profile={"P0": "PROSE_CANDIDATE"},
                 start_anchor="$$E", end_anchor="2$$"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="in nadaljujmo.", end_anchor="in nadaljujmo."),
        ],
        note="Display math block recognized only with the math extension.",
    ),
    # ---- class 12: paren-delimited TeX ----------------------------------------
    dict(
        id="F12", cls=12, cls_name="paren-tex",
        text="Označeno: (\\alpha + \\beta) je izraz.\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Označeno:", end_anchor="je izraz."),
        ],
        note="Expected residual semantic category (paren TeX): the parser sees plain "
             "text; exposure is the bounded second-stage problem, not a safety bug.",
    ),
    # ---- class 13: bracket-delimited TeX ---------------------------------------
    dict(
        id="F13", cls=13, cls_name="bracket-tex",
        text="Ulomek: [\\frac{1}{2}] velja za polovico.\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Ulomek:", end_anchor="polovico."),
        ],
        note="Expected residual semantic category (bracket TeX).",
    ),
    # ---- class 14: begin-end TeX environments (align) -----------------------------
    dict(
        id="F14", cls=14, cls_name="begintex-align",
        text="Sistem:\n\n\\begin{align}\na &= b \\\\\nc &= d\n\\end{align}\n\nKonec sistema.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Sistem:", end_anchor="Sistem:"),
            dict(name="gap-1", role="NEUTRAL", start_cp=7, end_cp=9),
            dict(name="begin-line", role="PROSE_CANDIDATE", start_cp=9, end_cp=22),
            dict(name="softbreak-1", role="NEUTRAL", start_cp=22, end_cp=23),
            dict(name="line-a", role="PROSE_CANDIDATE", start_cp=23, end_cp=30),
            dict(name="escape-1", role="PROTECTED", start_cp=30, end_cp=31),
            dict(name="literal-backslash", role="PROSE_CANDIDATE", start_cp=31, end_cp=32),
            dict(name="softbreak-2", role="NEUTRAL", start_cp=32, end_cp=33),
            dict(name="line-c", role="PROSE_CANDIDATE", start_cp=33, end_cp=39),
            dict(name="softbreak-3", role="NEUTRAL", start_cp=39, end_cp=40),
            dict(name="end-line", role="PROSE_CANDIDATE", start_cp=40, end_cp=51),
            dict(name="gap-2", role="NEUTRAL", start_cp=51, end_cp=53),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Konec sistema.", end_anchor="Konec sistema."),
        ],
        note="Expected residual semantic category (begin-end TeX environment): the "
             "environment text is exposed as ordinary text under every frozen "
             "profile. Token-level declaration: the escape-backslash byte (first "
             "backslash of the double-backslash pair) is Markdown escape syntax "
             "and stays protected; the escaped literal backslash is exposed; "
             "soft-break newlines are line endings and never prose (NEUTRAL).",
    ),
    # ---- class 15: malformed TeX ---------------------------------------------------
    dict(
        id="F15", cls=15, cls_name="malformed-tex",
        text="Napak: \\begin{align} a = b\n\ntukaj manjka konec.\n",
        regions=[
            dict(name="line-1", role="PROSE_CANDIDATE", start_cp=0, end_cp=26),
            dict(name="blank-line", role="NEUTRAL", start_cp=26, end_cp=28),
            dict(name="line-2", role="PROSE_CANDIDATE", start_cp=28, end_cp=47),
        ],
        note="Unpaired begin environment; every text byte of both paragraphs is "
             "exposed (residual + malformed recovery observation). The blank-line "
             "bytes are line endings and never prose (NEUTRAL).",
    ),
    # ---- class 16: paired dollar currency -------------------------------------------
    dict(
        id="F16", cls=16, cls_name="paired-dollar-currency",
        text="Cene: 5 $ in 10 $ ter 3 €. Kupila sem tri jabolka za 2,50 $.\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Cene:", end_anchor="za 2,50 $."),
        ],
        note="Policy: do not assume dollar quotes are math. Currency dollars must not "
             "form a math span under any frozen profile; if they do, that is a "
             "material dollar-math finding.",
    ),
    # ---- class 17: escaped dollar signs ---------------------------------------------
    dict(
        id="F17", cls=17, cls_name="escaped-dollars",
        text="Cena je \\$ 5 (escapirano) in \\$\\$\\$ trojno.\n",
        regions=[
            dict(name="prose-1", role="PROSE_CANDIDATE", start_cp=0, end_cp=8),
            dict(name="escape-1", role="PROTECTED", start_cp=8, end_cp=9),
            dict(name="prose-2", role="PROSE_CANDIDATE", start_cp=9, end_cp=29),
            dict(name="escape-2", role="PROTECTED", start_cp=29, end_cp=30),
            dict(name="dollar-1", role="PROSE_CANDIDATE", start_cp=30, end_cp=31),
            dict(name="escape-3", role="PROTECTED", start_cp=31, end_cp=32),
            dict(name="dollar-2", role="PROSE_CANDIDATE", start_cp=32, end_cp=33),
            dict(name="escape-4", role="PROTECTED", start_cp=33, end_cp=34),
            dict(name="prose-3", role="PROSE_CANDIDATE", start_cp=34, end_cp=43),
        ],
        note="Escaped dollars are literal text: the dollar bytes and all "
             "unescaped text are exposed; each escape-backslash byte is Markdown "
             "escape syntax and stays protected.",
    ),
    # ---- class 18: emphasis/strong containing prose ----------------------------------
    dict(
        id="F18", cls=18, cls_name="emphasis-strong-prose",
        text="To je *poudarjeno* in **močno** besedilo.\n",
        regions=[
            dict(name="prose-1", role="PROSE_CANDIDATE", start_cp=0, end_cp=6),
            dict(name="emph-delim-open", role="PROTECTED", start_cp=6, end_cp=7),
            dict(name="emph-text", role="PROSE_CANDIDATE", start_cp=7, end_cp=17),
            dict(name="emph-delim-close", role="PROTECTED", start_cp=17, end_cp=18),
            dict(name="prose-2", role="PROSE_CANDIDATE", start_cp=18, end_cp=22),
            dict(name="strong-delim-open", role="PROTECTED", start_cp=22, end_cp=24),
            dict(name="strong-text", role="PROSE_CANDIDATE", start_cp=24, end_cp=29),
            dict(name="strong-delim-close", role="PROTECTED", start_cp=29, end_cp=31),
            dict(name="prose-3", role="PROSE_CANDIDATE", start_cp=31, end_cp=41),
        ],
        note="Prose-bearing containers expose their textual leaves; only the "
             "Markdown delimiters stay protected.",
    ),
# ---- class 19: heading containing prose ---------------------------------------
    dict(
        id="F19", cls=19, cls_name="heading-prose",
        text="# Naslov prvega stopnja\n\nBesedilo pod naslovom.\n",
        regions=[
            dict(name="head-marker", role="PROTECTED", start_cp=0, end_cp=2),
            dict(name="head-text", role="PROSE_CANDIDATE",
                 start_anchor="Naslov", end_anchor="stopnja"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Besedilo", end_anchor="naslovom."),
        ],
        note="Heading marker is syntax; heading text is a prose leaf.",
    ),
    # ---- class 20: list item containing prose ---------------------------------------
    dict(
        id="F20", cls=20, cls_name="list-item-prose",
        text="Seznam:\n- prvi element\n- drugi element\n\nKonec seznama.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Seznam:", end_anchor="Seznam:"),
            dict(name="bullet-1", role="PROTECTED", start_cp=8, end_cp=10),
            dict(name="item-1", role="PROSE_CANDIDATE",
                 start_anchor="prvi", end_anchor="prvi element"),
            dict(name="bullet-2", role="PROTECTED",
                 start_anchor="\\n- drugi", end_anchor="\\n- "),
            dict(name="item-2", role="PROSE_CANDIDATE",
                 start_anchor="drugi", end_anchor="drugi element"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Konec seznama.", end_anchor="Konec seznama."),
        ],
        note="List markers are syntax; item text is a prose leaf.",
    ),
    # ---- class 21: blockquote containing prose ---------------------------------------
    dict(
        id="F21", cls=21, cls_name="blockquote-prose",
        text="Citat:\n> Prva vrstica citata.\n> Druga vrstica citata.\n\nPojasnilo.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Citat:", end_anchor="Citat:"),
            dict(name="quote-mark-1", role="PROTECTED", start_cp=7, end_cp=9),
            dict(name="quote-1", role="PROSE_CANDIDATE",
                 start_anchor="Prva", end_anchor="Prva vrstica citata."),
            dict(name="quote-mark-2", role="PROTECTED",
                 start_anchor="\\n> Druga", end_anchor="\\n> "),
            dict(name="quote-2", role="PROSE_CANDIDATE",
                 start_anchor="Druga", end_anchor="Druga vrstica citata."),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Pojasnilo.", end_anchor="Pojasnilo."),
        ],
        note="Blockquote markers are syntax; quoted text is a prose leaf.",
    ),
    # ---- class 22: markdown link with prose label and URL destination ------------------
    dict(
        id="F22", cls=22, cls_name="link-prose-label-url",
        text="Obišči [slovenski primer](https://primer.si/path?q=1) za podrobnosti.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Obišči", end_anchor="Obišči "),
            dict(name="bracket-open", role="PROTECTED", start_cp=7, end_cp=8),
            dict(name="label", role="PROSE_CANDIDATE",
                 start_anchor="slovenski primer", end_anchor="slovenski primer"),
            dict(name="bracket-close-paren", role="PROTECTED", start_cp=24, end_cp=26),
            dict(name="dest", role="PROTECTED",
                 start_anchor="https://primer.si/path?q=1", end_anchor="https://primer.si/path?q=1"),
            dict(name="paren-close", role="PROTECTED", start_cp=52, end_cp=53),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor=" za podrobnosti.", end_anchor="podrobnosti."),
        ],
        note="Link label is a prose leaf; link destination and syntax are protected.",
    ),
    # ---- class 23: image syntax ----------------------------------------------------------
    dict(
        id="F23", cls=23, cls_name="image-syntax",
        text="Slika: ![alt besedilo](https://primer.si/slika.png)\n\nNaprej.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Slika:", end_anchor="Slika: "),
            dict(name="image", role="PROTECTED",
                 start_anchor="![alt", end_anchor="slika.png)"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Naprej.", end_anchor="Naprej."),
        ],
        note="Image structure is protected by conservative default (including alt text; "
             "recorded tradeoff: alt text is arguably prose).",
    ),
    # ---- class 24: autolink -----------------------------------------------------------------
    dict(
        id="F24", cls=24, cls_name="autolink",
        text="Neposredno: https://primer.si/avto in <https://primer.si/kotnik> končata tu.\n",
        regions=[
            dict(name="prose-1", role="PROSE_CANDIDATE",
                 start_anchor="Neposredno:", end_anchor="Neposredno: "),
            dict(name="bare-url", role="PROSE_CANDIDATE",
                 start_anchor="https://primer.si/avto", end_anchor="https://primer.si/avto"),
            dict(name="prose-2", role="PROSE_CANDIDATE",
                 start_anchor=" in ", end_anchor=" in "),
            dict(name="angle-autolink", role="PROTECTED",
                 start_anchor="<https://primer.si/kotnik>", end_anchor="<https://primer.si/kotnik>"),
            dict(name="prose-3", role="PROSE_CANDIDATE",
                 start_anchor=" končata tu.", end_anchor="končata tu."),
        ],
        note="Frozen profiles do not enable ENABLE_GFM, so the bare URL is ordinary "
             "text (expected residual category: dialect-missed URL/autolink); the "
             "angle-bracket autolink is CommonMark core and protected.",
    ),
    # ---- class 25: table containing prose and inline code -------------------------------------
    dict(
        id="F25", cls=25, cls_name="table-prose-and-code",
        text="Tablica:\n\n| besedilo | `kodna celica` |\n|----------|----------------|\n| drugi vrstica | `x = 1` |\n\nOpomba.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Tablica:", end_anchor="Tablica:"),
            dict(name="cell-1", role="PROSE_CANDIDATE",
                 role_by_profile={"P0": "PROSE_CANDIDATE"},
                 start_anchor="besedilo", end_anchor="besedilo"),
            dict(name="cell-code-1", role="PROTECTED",
                 start_anchor="`kodna", end_anchor="celica`"),
            dict(name="row-2-text", role="PROSE_CANDIDATE",
                 role_by_profile={"P0": "PROSE_CANDIDATE"},
                 start_anchor="drugi vrstica", end_anchor="drugi vrstica"),
            dict(name="cell-code-2", role="PROTECTED",
                 start_anchor="`x = 1`", end_anchor="`x = 1`"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Opomba.", end_anchor="Opomba."),
        ],
        note="Under P1/P2 (tables enabled) cells are prose leaves and inline code "
             "stays protected; under P0 the table rows are plain paragraph text, "
             "but the inline code span is still parsed as CommonMark-core code "
             "(Code event, never candidate prose). Inline code is core CommonMark, "
             "so the code spans stay PROTECTED under every profile.",
    ),
    # ---- class 26: raw HTML --------------------------------------------------------------------
    dict(
        id="F26", cls=26, cls_name="raw-html",
        text="Vrstica pred HTML:\n\n<div class=\"ok\">vsebina diva</div>\n\nInline <b>odebeljeno</b> tu.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Vrstica", end_anchor="pred HTML:"),
            dict(name="html-block", role="PROTECTED",
                 start_anchor="<div", end_anchor="</div>"),
            dict(name="prose-mid", role="PROSE_CANDIDATE",
                 start_anchor="Inline", end_anchor="Inline "),
            dict(name="html-open", role="PROTECTED", start_cp=63, end_cp=66),
            dict(name="html-text", role="PROSE_CANDIDATE", start_cp=66, end_cp=76),
            dict(name="html-close", role="PROTECTED", start_cp=76, end_cp=80),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor=" tu.", end_anchor=" tu."),
        ],
        note="HTML blocks and inline-HTML tags are protected; the ordinary text "
             "between inline-HTML tags is a prose leaf and exposed.",
    ),
    # ---- class 27: bare JSON ---------------------------------------------------------------------
    dict(
        id="F27", cls=27, cls_name="bare-json",
        text="Izvoz:\n\n{\n  \"ime\": \"Ana\",\n  \"starost\": 30\n}\n\nKončano.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Izvoz:", end_anchor="Izvoz:"),
            dict(name="json-open", role="PROSE_CANDIDATE", start_cp=8, end_cp=9),
            dict(name="newline-1", role="NEUTRAL", start_cp=9, end_cp=10),
            dict(name="indent-1", role="NEUTRAL", start_cp=10, end_cp=12),
            dict(name="line-1", role="PROSE_CANDIDATE", start_cp=12, end_cp=25),
            dict(name="newline-2", role="NEUTRAL", start_cp=25, end_cp=26),
            dict(name="indent-2", role="NEUTRAL", start_cp=26, end_cp=28),
            dict(name="line-2", role="PROSE_CANDIDATE", start_cp=28, end_cp=41),
            dict(name="newline-3", role="NEUTRAL", start_cp=41, end_cp=42),
            dict(name="json-close", role="PROSE_CANDIDATE", start_cp=42, end_cp=43),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Končano.", end_anchor="Končano."),
        ],
        note="Expected residual semantic category (bare JSON): structurally "
             "unrecognized; every non-whitespace byte is exposed as ordinary text "
             "under every frozen profile. Whitespace bytes (newlines, "
             "indentation) are never prose (NEUTRAL).",
    ),
    # ---- class 28: YAML/TOML/config-like material ----------------------------------------------------
    dict(
        id="F28", cls=28, cls_name="yaml-toml-config",
        text="Nastavitev:\n\n[toml_section]\nkey = \"vrednost\"\n\nyaml_razdelek:\n  kljuc: vrednost\n\nKončano.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Nastavitev:", end_anchor="Nastavitev:"),
            dict(name="toml-line-1", role="PROSE_CANDIDATE", start_cp=13, end_cp=27),
            dict(name="newline-1", role="NEUTRAL", start_cp=27, end_cp=28),
            dict(name="toml-line-2", role="PROSE_CANDIDATE", start_cp=28, end_cp=44),
            dict(name="blank-1", role="NEUTRAL", start_cp=44, end_cp=46),
            dict(name="yaml-line-1", role="PROSE_CANDIDATE", start_cp=46, end_cp=60),
            dict(name="newline-2", role="NEUTRAL", start_cp=60, end_cp=61),
            dict(name="indent-1", role="NEUTRAL", start_cp=61, end_cp=63),
            dict(name="yaml-line-2", role="PROSE_CANDIDATE", start_cp=63, end_cp=78),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Končano.", end_anchor="Končano."),
        ],
        note="Expected residual semantic categories (TOML section, YAML-style "
             "mapping): structurally unrecognized mid-document; every "
             "non-whitespace byte is exposed as ordinary text; whitespace bytes "
             "are never prose (NEUTRAL).",
    ),
    # ---- class 29: shell commands ---------------------------------------------------------------------
    dict(
        id="F29", cls=29, cls_name="shell-commands",
        text="Ukazi v terminalu:\n\n$ ls -la /tmp\n# komentar\nsudo apt update\n\nPojasnilo.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Ukazi", end_anchor="terminalu:"),
            dict(name="shell-line-1", role="PROSE_CANDIDATE", start_cp=20, end_cp=33),
            dict(name="newline-1", role="NEUTRAL", start_cp=33, end_cp=34),
            dict(name="heading-marker", role="PROTECTED", start_cp=34, end_cp=36),
            dict(name="heading-text", role="PROSE_CANDIDATE", start_cp=36, end_cp=44),
            dict(name="newline-2", role="NEUTRAL", start_cp=44, end_cp=45),
            dict(name="shell-line-2", role="PROSE_CANDIDATE", start_cp=45, end_cp=60),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Pojasnilo.", end_anchor="Pojasnilo."),
        ],
        note="Expected residual semantic category (shell commands): exposed as "
             "ordinary text under every frozen profile. Dialect finding: the "
             "'# komentar' line is parsed as an ATX heading (S.Head:1) by the "
             "CommonMark core; the heading marker stays protected and the heading "
             "text is a prose leaf.",
    ),
    # ---- class 30: paths -------------------------------------------------------------------------------
    dict(
        id="F30", cls=30, cls_name="paths",
        text="Datoteke so v /var/dokumenti in D:\\programi\\test ter ./relativna/put.\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Datoteke", end_anchor="relativna/put."),
        ],
        note="Expected residual semantic category (paths): exposed as ordinary text.",
    ),
    # ---- class 31: environment variables ------------------------------------------------------------------
    dict(
        id="F31", cls=31, cls_name="env-vars",
        text="Sprotno: $HOME in $PATH_JAVA ter JAVA_HOME=/opt/java.\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Sprotno:", end_anchor="/opt/java."),
        ],
        note="Expected residual semantic category (environment variables).",
    ),
    # ---- class 32: identifier-heavy tokens -----------------------------------------------------------------
    dict(
        id="F32", cls=32, cls_name="identifier-heavy",
        text="Funkcija parse_lexer_input() kliče validate_token_set().\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Funkcija", end_anchor="validate_token_set()."),
        ],
        note="Expected residual semantic category (identifier-heavy tokens).",
    ),
    # ---- class 33: Slovenian c-caron/s-caron/z-caron as UTF-8 -------------------------------------------------
    dict(
        id="F33", cls=33, cls_name="slovenian-carons",
        text="Reč, še, žvečiti, čez, vrč, žrtev, češ.\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Reč", end_anchor="češ."),
        ],
        note="Multi-byte carons: byte boundaries must never bisect a code point.",
    ),
    # ---- class 34: emoji -------------------------------------------------------------------------------------
    dict(
        id="F34", cls=34, cls_name="emoji",
        text="Oznaka 👍 pomeni strinjanje, 🔥 je odlično, 🚀🚀 se podvoji.\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Oznaka", end_anchor="se podvoji."),
        ],
        note="4-byte emoji: byte boundaries must never bisect a code point.",
    ),
    # ---- class 35: decomposed Unicode combining sequences ------------------------------------------------------
    dict(
        id="F35", cls=35, cls_name="decomposed-unicode",
        text="Zloženo: e\u0301 (e + U+0301) in a\u030c (a + U+030C).\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Zloženo:", end_anchor="U+030C)."),
        ],
        note="Decomposed sequences (base + combining mark) must stay intact across "
             "byte boundaries; no re-composition anywhere in the measurement.",
    ),
    # ---- class 36: CRLF line endings ------------------------------------------------------------------------------
    dict(
        id="F36", cls=36, cls_name="crlf",
        text="Prva vrstica.\r\nDruga vrstica.\r\n\r\nTretja vrstica.\r\n",
        regions=[
            dict(name="line-1", role="PROSE_CANDIDATE",
                 start_anchor="Prva", end_anchor="Prva vrstica."),
            dict(name="line-2", role="PROSE_CANDIDATE",
                 start_anchor="Druga", end_anchor="Druga vrstica."),
            dict(name="line-3", role="PROSE_CANDIDATE",
                 start_anchor="Tretja", end_anchor="Tretja vrstica."),
        ],
        note="CRLF byte pairs are line endings: never candidate prose. Parser must "
             "treat CRLF as line breaks deterministically.",
    ),
    # ---- class 37: malformed links --------------------------------------------------------------------------------
    dict(
        id="F37", cls=37, cls_name="malformed-links",
        text="Slabi: [brez cilja] in [slomljen( in ](osamljen) konec.\n",
        regions=[
            dict(name="prose-1", role="PROSE_CANDIDATE", start_cp=0, end_cp=7),
            dict(name="literal-link-1", role="PROSE_CANDIDATE", start_cp=7, end_cp=19),
            dict(name="prose-mid", role="PROSE_CANDIDATE", start_cp=19, end_cp=23),
            dict(name="link-open", role="PROTECTED", start_cp=23, end_cp=24),
            dict(name="link-label", role="PROSE_CANDIDATE", start_cp=24, end_cp=37),
            dict(name="link-close-paren", role="PROTECTED", start_cp=37, end_cp=39),
            dict(name="link-dest", role="PROTECTED", start_cp=39, end_cp=47),
            dict(name="link-close", role="PROTECTED", start_cp=47, end_cp=48),
            dict(name="prose-after", role="PROSE_CANDIDATE", start_cp=48, end_cp=55),
        ],
        note="Link recovery: '[brez cilja]' has no destination or definition and "
             "stays literal prose (all its bytes exposed). '[slomljen( in "
             "](osamljen)' is a well-formed CommonMark link (link labels may "
             "contain parentheses; relative destination): the label is a prose "
             "leaf, while the link syntax and the destination stay protected.",
    ),
    # ---- class 38: mixed malformed Markdown/HTML/TeX ----------------------------------------------------------------
    dict(
        id="F38", cls=38, cls_name="mixed-malformed",
        text="Mix:\n# Naslov\n\n```\nekod <div> $x$\n\n[link](nek) **polovica\n<ol><li>nestanovitno \\frac{1}{2}\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Mix:", end_anchor="Mix:"),
            dict(name="heading", role="PROSE_CANDIDATE",
                 start_anchor="Naslov", end_anchor="Naslov"),
            dict(name="rest", role="NEUTRAL",
                 start_anchor="```", end_anchor="\\frac{1}{2}\n"),
        ],
        note="Mixed malformed Markdown/HTML/TeX with an unfinished fence: only the "
             "heading text is assertive; the remainder is a deterministic-recovery "
             "observation (conservative expectation: the unclosed fence swallows the "
             "rest as code).",
    ),
    # ---- class 39 (extra): GFM task list ----------------------------------------------------------------------------
    dict(
        id="F39", cls=39, cls_name="gfm-task-list",
        text="Naloge:\n- [x] narejeno\n- [ ] odprto\n\nKonec.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Naloge:", end_anchor="Naloge:"),
            dict(name="task-1", role="PROSE_CANDIDATE",
                 role_by_profile={"P0": "PROSE_CANDIDATE"},
                 start_anchor="narejeno", end_anchor="narejeno"),
            dict(name="task-2", role="PROSE_CANDIDATE",
                 role_by_profile={"P0": "PROSE_CANDIDATE"},
                 start_anchor="odprto", end_anchor="odprto"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Konec.", end_anchor="Konec."),
        ],
        note="Task-list markers are syntax under P1/P2; under P0 the brackets are "
             "literal text (dialect finding).",
    ),
    # ---- class 40 (extra): GFM strikethrough ------------------------------------------------------------------------
    dict(
        id="F40", cls=40, cls_name="gfm-strikethrough",
        text="Prečrtano: ~~stara~~ nova oblika.\n",
        regions=[
            dict(name="prose-1", role="PROSE_CANDIDATE",
                 start_anchor="Prečrtano:", end_anchor="Prečrtano: "),
            dict(name="strike-text", role="NEUTRAL",
                 role_by_profile={"P0": "PROSE_CANDIDATE"},
                 start_anchor="stara", end_anchor="stara"),
            dict(name="prose-2", role="PROSE_CANDIDATE",
                 start_anchor=" nova oblika.", end_anchor="nova oblika."),
        ],
        note="Frozen policy names emphasis/strong as prose-bearing; strikethrough "
             "content is conservatively suppressed under P1/P2 (recorded tradeoff).",
    ),
    # ---- class 41 (extra): YAML front matter ------------------------------------------------------------------------
    dict(
        id="F41", cls=41, cls_name="yaml-front-matter",
        text="---\ntitle: Naslov dok\nauthor: Ana\n---\n\nVsebina po glavi.\n",
        regions=[
            dict(name="rule-1", role="PROTECTED", start_cp=0, end_cp=3),
            dict(name="newline-1", role="NEUTRAL", start_cp=3, end_cp=4),
            dict(name="title-line", role="PROSE_CANDIDATE",
                 role_by_profile={"P2": "PROTECTED"}, start_cp=4, end_cp=21),
            dict(name="newline-2", role="NEUTRAL", start_cp=21, end_cp=22),
            dict(name="author-line", role="PROSE_CANDIDATE",
                 role_by_profile={"P2": "PROTECTED"}, start_cp=22, end_cp=33),
            dict(name="newline-3", role="NEUTRAL", start_cp=33, end_cp=34),
            dict(name="setext-rule", role="PROTECTED", start_cp=34, end_cp=37),
            dict(name="gap-1", role="NEUTRAL", start_cp=37, end_cp=39),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Vsebina", end_anchor="po glavi."),
        ],
        note="Dialect finding: under P0/P1 the leading '---' is a thematic break "
             "(Rule) and the following 'title: ...' paragraph plus the closing "
             "'---' form a setext H2 heading, so the key/value lines are heading "
             "text (prose leaves; residual config). Under P2 (metadata blocks "
             "enabled) the whole front matter is a metadata block and protected.",
    ),
    # ---- class 42 (extra): nested list with prose ---------------------------------------------------------------------
    dict(
        id="F42", cls=42, cls_name="nested-list-prose",
        text="Globina:\n- ena\n  - ena ena\n  - ena dva\n- dva\n\nKonec.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Globina:", end_anchor="Globina:"),
            dict(name="item-1", role="PROSE_CANDIDATE",
                 start_anchor="\\n- ena", end_anchor="\\n- ena"),
            dict(name="item-1-1", role="PROSE_CANDIDATE",
                 start_anchor="ena ena", end_anchor="ena ena"),
            dict(name="item-1-2", role="PROSE_CANDIDATE",
                 start_anchor="ena dva", end_anchor="ena dva"),
            dict(name="item-2", role="PROSE_CANDIDATE",
                 start_anchor="\\n- dva", end_anchor="\\n- dva"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Konec.", end_anchor="Konec."),
        ],
        note="Nested list item text are prose leaves under every profile.",
    ),
    # ---- class 43 (extra): thematic break -------------------------------------------------------------------------------
    dict(
        id="F43", cls=43, cls_name="thematic-break",
        text="Zgornja.\n\n---\n\nSpodnja.\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Zgornja.", end_anchor="Zgornja."),
            dict(name="rule", role="PROTECTED",
                 start_anchor="---", end_anchor="---"),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Spodnja.", end_anchor="Spodnja."),
        ],
        note="Thematic break is Markdown syntax, never prose.",
    ),
    # ---- class 44 (extra): reference link -------------------------------------------------------------------------------
    dict(
        id="F44", cls=44, cls_name="reference-link",
        text="Glej [primer][ref] spodaj.\n\n[ref]: https://primer.si/ref\n",
        regions=[
            dict(name="prose-1", role="PROSE_CANDIDATE",
                 start_anchor="Glej", end_anchor="Glej "),
            dict(name="label", role="PROSE_CANDIDATE",
                 start_anchor="primer", end_anchor="primer"),
            dict(name="ref-syntax", role="PROTECTED",
                 start_anchor="][ref]", end_anchor="][ref]"),
            dict(name="prose-2", role="PROSE_CANDIDATE",
                 start_anchor=" spodaj.", end_anchor="spodaj."),
            dict(name="definition", role="PROTECTED",
                 start_anchor="[ref]:", end_anchor="https://primer.si/ref"),
        ],
        note="Reference link: label is a prose leaf; the [ref] syntax and the "
             "definition line (with its destination) are protected.",
    ),
    # ---- class 45 (extra): CRLF with carons -------------------------------------------------------------------------------
    dict(
        id="F45", cls=45, cls_name="crlf-carons",
        text="Reč in vrč.\r\nDruga: še.\r\n",
        regions=[
            dict(name="line-1", role="PROSE_CANDIDATE",
                 start_anchor="Reč", end_anchor="Reč in vrč."),
            dict(name="line-2", role="PROSE_CANDIDATE",
                 start_anchor="Druga:", end_anchor="Druga: še."),
        ],
        note="Combination: CRLF line endings plus multi-byte carons.",
    ),
    # ---- class 47 (extra): Windows paths ----------------------------------------------------------------------------------
    dict(
        id="F47", cls=47, cls_name="windows-paths",
        text="Put: C:\\Program Files\\app\\bin.exe in C:/drugo.\n",
        regions=[
            dict(name="prose", role="PROSE_CANDIDATE",
                 start_anchor="Put:", end_anchor="C:/drugo."),
        ],
        note="Expected residual semantic category (Windows path dialect).",
    ),
    # ---- class 48 (extra): angle autolink and mailto ---------------------------------------------------------------------
    dict(
        id="F48", cls=48, cls_name="angle-autolink-mailto",
        text="Pošta: <ana@primer.si> in <https://primer.si/kotnik>.\n",
        regions=[
            dict(name="prose-1", role="PROSE_CANDIDATE",
                 start_anchor="Pošta:", end_anchor="Pošta: "),
            dict(name="mailto", role="PROTECTED",
                 start_anchor="<ana@primer.si>", end_anchor="<ana@primer.si>"),
            dict(name="prose-2", role="PROSE_CANDIDATE",
                 start_anchor=" in ", end_anchor=" in "),
            dict(name="url-autolink", role="PROTECTED",
                 start_anchor="<https://primer.si/kotnik>", end_anchor="<https://primer.si/kotnik>"),
            dict(name="prose-3", role="PROSE_CANDIDATE", start_cp=52, end_cp=53),
        ],
        note="Angle-bracket autolinks (URL and mailto) are CommonMark core and "
             "protected under every profile.",
    ),
    # ---- class 49 (extra): unclosed backtick -------------------------------------------------------------------------------
    dict(
        id="F49", cls=49, cls_name="unclosed-backtick",
        text="Neparični: `nepoln konec.\n\nKonec.\n",
        regions=[
            dict(name="line-1", role="PROSE_CANDIDATE", start_cp=0, end_cp=25),
            dict(name="blank-line", role="NEUTRAL", start_cp=25, end_cp=27),
            dict(name="line-2", role="PROSE_CANDIDATE", start_cp=27, end_cp=33),
        ],
        note="Unmatched single backtick: CommonMark treats it as literal text, so "
             "every text byte of both paragraphs (including the backtick) is "
             "exposed; the blank-line bytes are line endings and never prose "
             "(NEUTRAL). Deterministic recovery observation (dialect finding, not "
             "a safety bug).",
    ),
    # ---- class 50 (extra): CRLF with fenced code ---------------------------------------------------------------------------
    dict(
        id="F50", cls=50, cls_name="crlf-fenced-code",
        text="Pred:\r\n\r\n```\nokod\r\n```\r\n\r\nPo.\r\n",
        regions=[
            dict(name="prose-before", role="PROSE_CANDIDATE",
                 start_anchor="Pred:", end_anchor="Pred:"),
            dict(name="fence", role="PROTECTED",
                 start_anchor="```", end_anchor="```", end_anchor_last=True),
            dict(name="prose-after", role="PROSE_CANDIDATE",
                 start_anchor="Po.", end_anchor="Po."),
        ],
        note="CRLF inside and around a fenced block.",
    ),
]

# Class 46 (extra): long paragraph stress, generated deterministically at build time.
LONG_PARAGRAPH_SENTENCES = [
    "V dolini pod visokimi vrhovi je pozno popoldne tiho.",
    "Potniki odložijo torbe in poslušajo tišino.",
    "Nad jezerom lebdi tanek pas meglice.",
    "Ker se dan polahoma zaključuje, se barve zameglijo.",
    "Vode so mirne in odsevajo zadnjo svetlobo.",
    "Nekje daleč zaspi prvi petel.",
    "V zraku miriši po mokri travi in hladnem kamnu.",
    "Ob obrežju ostanejo le tihi sledi dneva.",
]

LONG_PARAGRAPH_FIXTURE = dict(
    id="F46", cls=46, cls_name="long-paragraph-stress",
    text=None,  # built by build_fixtures.py
    regions=[
        dict(name="long-prose", role="PROSE_CANDIDATE",
             start_anchor="__LONG_START__", end_anchor="__LONG_END__"),
    ],
    note="Deterministic ~2.5 kB Slovenian paragraph (repeated sentences with "
         "numbering) exercising long spans and repeated substrings; the trailing "
         "newline is never prose.",
)
