# The translator's eval

A translator you cannot check is just an opinion generator. This folder is the proof the Rechnung translator keeps its contract. It runs on the translator's **output** (a produced Rechnung), never on its factory files, the way `tests/` is evidence about code rather than part of it. **The translator never reads `audit/`.**

## Two layers

**Layer 1, `checks.py`** (deterministic, no model). Given a report:

| Gate | Invariant |
|---|---|
| shape | the declared sections, required fields, table headers, and order are present, or it is a refusal |
| html-integrity | an HTML invoice exactly matches the fixed renderer's output from its embedded audit source |
| arithmetic | every line, the Zwischensumme, the § 35a split, the 19 % USt and the Brutto recompute exactly (half up, two decimals) |
| trace-tags | every Quellennachweis row carries a valid tag (Q / R / A / ∅) |
| no-orphan | every euro amount in the invoice body appears in the Quellennachweis (nothing un-sourced) |
| source-Q | every Q amount actually appears in the job record (value-matched, so a German-formatted output traces to an English-written input) |
| source-R | every cited `reference/` file exists |
| gap-honesty | an incomplete draft marks its gaps `nicht in Quelle` |
| dialogue | an incomplete draft's Rückfragen name the missing required fields and nothing already present |
| refusal | an out-of-scope report is a refusal block with no invoice |
| key-match | (with `--key`) the Brutto and draft/final status match the answer key |

`no-orphan` plus `source-Q` catch some unsupported numbers. They do **not** prove that every claim traces to its stated line: `source-Q` matches amounts anywhere in the job record, and names, dates, descriptions, hours, and distances still need a source review. See `FINDINGS.md`.

**Layer 2** (a human or vision confirm, deliberately small). Two things a text script cannot judge: a value read from a **receipt photo**, and whether a Leistung is **concretely enough named** for § 14. Named in `FINDINGS.md`, not hidden.

## Run it

```bash
python audit/checks.py --all
python audit/checks.py audit/reports/01-clean-complete.report.html --input audit/fixtures/01-clean-complete.md --key audit/keys/01-clean-complete.key.md
```

Exit 0 if every hard gate passes, 1 if any fails. Usable as a CI gate before a Rechnung is trusted.

## Fixtures, keys, and the planted defect

`fixtures/` holds job records, one per case; `keys/` holds the expected Brutto and status, **outside** the fixtures so a case never carries its own answer. `01-clean-complete`, `02-missing-fields`, and `03-english-helper` are worked example pairs. Their HTML reports were rendered from prepared schema intermediates; passing them tests the checker and renderer, **not** whether a fresh model produces them. `04-plumbing`, `05-drywall`, `06-flooring` are separate English voice-note fixtures; their cold-run reports are placed in `reports/` and scored here. Fixture numbers are unique across both families so a stem never collides.

For a cold run, start a fresh agent with only `identity.md`, `rules.md`, `reference/schema.md`, `reference/stammdaten.md`, `reference/pricing.md`, the named contract, and any named team file. The agent may run `render_html.py` after filling the schema. Supply exactly one fixture as the user message. Keep `examples.md`, `audit/`, keys, and previous outputs outside the agent's context. Save its HTML file, then run this checker with `--input` and `--key`. Review each claim against its cited line or reference field by hand. For a draft, answer only its Rückfragen and check the continuation separately.

`reports/planted-defect.report.md` carries five deliberate defects (a wrong line total, a wrong USt, an invalid tag, a stray amount, an invented material). Every one is caught; the run fails with exit 1, as it must. A translator that only ever passes is worthless; this is the proof it refuses.

`reports/planted-html-tamper.report.html` proves the newest gate. It is `01-clean-complete` with one visible figure edited by hand (`977,55 €` shown as `877,55 €`) and the embedded audit source left untouched. Every content gate still passes, because they read the embedded source; only `html-integrity` catches it. That is the whole argument for the gate: without it, a hand-edited invoice would sail through.

See `eval-log.md` for the runs verbatim, including the round that failed, what it exposed, the fix, and the re-run. See `FINDINGS.md` for the honest read, including where this eval is deliberately shallow.
