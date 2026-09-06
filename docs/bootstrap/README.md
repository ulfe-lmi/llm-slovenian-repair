# LLM Slovenian Repair — vhodni paket za bootstrap

**Različica 2.0 · 6. september 2026**

Razširi ZIP v **nov, prazen začasni imenik**, ki ni znotraj coding ali strategic
imenika. `AGENTS.md` je neposredno v korenu ZIP-a in je namenjen izključno agentu,
ki bo ustvaril bootstrap. Ne mešaj teh datotek s prejšnjo različico.

V tem začasnem imeniku zaženi izbranega močnega coding agenta in mu daj:

```text
Read AGENTS.md and execute INSTRUCTIONS.md. Use the bundled PLAN.md,
ARCHITECTURE.md, CRITICAL.md, specifications and original OAP source documents.
Materialize and validate the complete coding and strategic workspaces.
Stop before operational activation and write BOOTSTRAP-RECEIPT.md.
```

Privzeta cilja sta:

```text
~/codex-work/llm-slovenian-repair
~/codex-supervision/llm-slovenian-repair
```

Drugačna cilja lahko izrecno določiš pred zagonom z `OAP_REPO_ROOT` in
`OAP_STRATEGIC_HOME`. Vsi trije imeniki morajo biti ločeni in ne smejo biti drug
znotraj drugega. Obstoječih spremenjenih datotek agent ne sme prepisati.

## Kaj naredi bootstrap agent

Ustvari dejanska delovna imenika, operativna navodila, preizkušene OAP pomožne
programe, zaganjalnike, 56 podrobnih neaktivnih osnutkov nalog in gradivo za
neodvisne zaključne preglede. Pred tem prebere priložena izvorna dokumenta OAP;
ne potrebuje dostopa do prej nedosegljive spletne strani ali prejšnjih arhivov.

Končna razmejitev navodil je:

```text
začasni imenik/AGENTS.md                    bootstrap agent
coding repozitorij/AGENTS.md                minimalni usmerjevalnik vlog
coding repozitorij/oap/coding-instructions/AGENTS.md
                                           gosta navodila coding agentu
strategic imenik/AGENTS.md                  polna strateška konstitucija
```

`PLAN.md` ostane bajtno nespremenjen. Arhitektura vsebuje dogovorjeni celotni
prevzem odgovora, CPU-pregled in izolirano Qwenovo presojo označenih besed/zvez.
Register CRITICAL se začne brez dejanskih vnosov. Coding agent ne prejme celotnega
plana, arhitekture, roadmapa ali registra kot rutinskega konteksta.

## Kaj ostane namenoma izključeno

Bootstrap ne začne razvoja aplikacije, ne aktivira naloge, ne zažene nobenega
operativnega agenta, ne kliče Qwena, ne prenaša velikih korpusov/modelov in ne
spreminja obstoječe modelske storitve. Prav tako sam ne ustvari/publikuje oddaljenega
repozitorija ter ne kopira prijavnih podatkov med vlogami.

Po izdelavi v tem začasnem imeniku nastane `BOOTSTRAP-RECEIPT.md` z dejanskimi
rezultati preverjanj in preostalimi pogoji za aktivacijo. Izbira operativnih modelov,
prijava, oddaljeni repozitorij in dovoljenje za začetek zanke so ločena nastavitev;
agent pripravi tudi ločen dvopanelni način za to nastavitev.

## Vsebina paketa

Glavne datoteke so [INSTRUCTIONS.md](INSTRUCTIONS.md), [PLAN.md](PLAN.md),
[ARCHITECTURE.md](ARCHITECTURE.md) in [CRITICAL.md](CRITICAL.md).
[specifications/ROLE-CONTEXT.md](specifications/ROLE-CONTEXT.md) določa konteksta vlog,
[specifications/OAP-PROTOCOL.md](specifications/OAP-PROTOCOL.md) protokol,
[specifications/WORK-PROGRAM.md](specifications/WORK-PROGRAM.md) program nalog in
[specifications/BOOTSTRAP-ACCEPTANCE.md](specifications/BOOTSTRAP-ACCEPTANCE.md)
preverjanja, ki jih mora bootstrap agent tudi izvesti.

Izvorni [Concentrated OAP](sources/concentrated-oap.md) in [OAP](sources/oap.md)
sta ohranjena v celoti. [SOURCE-MAP.md](SOURCE-MAP.md) loči izvorne zahteve od
projektnih odločitev. `PACKAGE-MANIFEST.json` in `INPUTS.sha256` omogočata preverjanje
celovitosti. Paket sam je specifikacija: ni dokaz že delujočega OAP okolja ali
kakovosti bodočega jezikovnega popravljalnika.
