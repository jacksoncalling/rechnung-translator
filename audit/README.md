# The translator's eval

A translator you cannot check is just an opinion generator. This folder is the proof the Rechnung translator keeps its contract. It runs on the translator's **output** (a produced Rechnung), never on its factory files, the way `tests/` is evidence about code rather than part of it. **The translator never reads `audit/`.**

## Two layers

**Layer 1, `checks.py`** (deterministic, no model). Given a report:

| Gate | Invariant |
|---|---|
| shape | the required sections are present, or it is a well-formed refusal |
| arithmetic | every line, the Zwischensumme, the § 35a split, the 19 % USt and the Brutto recompute exactly (half up, two decimals) |
| trace-tags | every Quellennachweis row carries a valid tag (Q / R / A / ∅) |
| no-orphan | every euro amount in the invoice body appears in the Quellennachweis (nothing un-sourced) |
| source-Q | every Q amount actually appears in the job record (value-matched, so a German-formatted output traces to an English-written input) |
| source-R | every cited `reference/` file exists |
| gap-honesty | an incomplete draft marks its gaps `nicht in Quelle` |
| dialogue | an incomplete draft's Rückfragen name the missing required fields and nothing already present |
| refusal | an out-of-scope report is a refusal block with no invoice |
| key-match | (with `--key`) the Brutto and draft/final status match the answer key |

`no-orphan` plus `source-Q` are the mechanical form of the comp's own rule: every number in the output traces to the input, and nothing was invented.

**Layer 2** (a human or vision confirm, deliberately small). Two things a text script cannot judge: a value read from a **receipt photo**, and whether a Leistung is **concretely enough named** for § 14. Named in `FINDINGS.md`, not hidden.

## Run it

```bash
python audit/checks.py --all
python audit/checks.py audit/reports/01-clean-complete.report.md --input audit/fixtures/01-clean-complete.md --key audit/keys/01-clean-complete.key.md
```

Exit 0 if every hard gate passes, 1 if any fails. Usable as a CI gate before a Rechnung is trusted.

## Fixtures, keys, and the planted defect

`fixtures/` holds job records, one per case; `keys/` holds the expected Brutto and status, **outside** the fixtures so a case never carries its own answer. `01-clean-complete` is the full one-pass invoice. `02-plumbing`, `03-drywall`, `04-flooring` are the three English voice-note cases; their **cold-run** reports (produced by a fresh Claude that never saw the build) drop into `reports/` and get scored here.

`reports/planted-defect.report.md` carries five deliberate defects (a wrong line total, a wrong USt, an invalid tag, a stray amount, an invented material). Every one is caught; the run fails with exit 1, as it must. A translator that only ever passes is worthless; this is the proof it refuses.

See `FINDINGS.md` for the honest read, including where this eval is deliberately shallow.
