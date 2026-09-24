# Eval log — the runs, verbatim

Receipts, not claims. Each round records what `checks.py` actually printed, including the round that failed. A suite that was green the first time would prove less than this.

---

## Round 1 — 2026-09-24, first cold round scored

Three fresh agents were each given one English voice note and nothing else (`04-plumbing`, `05-drywall`, `06-flooring`), rendered their own HTML, and the results were scored against keys frozen before the runs.

```
| Bericht                          | erwartet | Ergebnis | ok? |
| 01-clean-complete.report.html    | PASS     | PASS     | ok  |
| 02-missing-fields.report.html    | PASS     | PASS     | ok  |
| 03-english-helper.report.html    | PASS     | PASS     | ok  |
| 04-plumbing.report.html          | PASS     | FAIL     | X   |
| 05-drywall.report.html           | PASS     | FAIL     | X   |
| 06-flooring.report.html          | PASS     | FAIL     | X   |
| planted-defect.report.md         | FAIL     | FAIL     | ok  |
| planted-html-tamper.report.html  | FAIL     | FAIL     | ok  |

**Suite: FAIL**
```

Per report (`04-plumbing`, the other two were the same shape of failure):

```
| html-integrity | PASS | sichtbare Rechnung entspricht der Prüfquelle |
| shape          | FAIL | Ausstellerblock fehlt |
| arithmetic     | PASS | alle Summen stimmen |
| trace-tags     | PASS | jede Nachweiszeile getaggt |
| no-orphan      | PASS | jeder Betrag im Nachweis belegt |
| source-R       | PASS | alle zitierten reference-Dateien existieren |
| source-Q       | PASS | jeder Q-Betrag steht im Job-Record |
| gap-honesty    | PASS | Lücke als 'nicht in Quelle' markiert |
| dialogue       | FAIL | Rückfragen unvollständig: fehlend ['Rechnungsnummer', 'Rechnungsdatum', 'Empfänger'], gestellt ['Rechnungsnummer', 'Rechnungsdatum'] |
| key-match      | PASS | entspricht dem Schlüssel |
```

### What that says

Every fidelity gate passed on all three, and `key-match` passed, meaning each run hit the Brutto frozen into its key before the run: **267,61 €**, **1.354,47 €**, **2.764,97 €**.

The two failures were defects in **this checker**, not in the translator:

1. `dialogue` required the literal string `Empfänger`, while `rules.md` § 5 instructs the agent to ask `Welcher Vertrag/Kunde?`. All three asked correctly and were failed for following the rules.
2. `shape` required a punctuation style for the issuer block that the schema never specified. The three agents wrote:
   - `Berg Reparatur- und Hausmeisterservice, Jonas Berg`
   - `Berg Reparatur- und Hausmeisterservice, Inhaber Jonas Berg`
   - `Berg Reparatur- und Hausmeisterservice — Inhaber Jonas Berg`

   All three are fair readings of the old placeholder `<Betrieb, Inhaber — R: stammdaten.md>`, whose own em-dash likely produced the third.

### The fix

- `conventions.json` gained `required_field_synonyms`, so a required field counts as asked under any documented wording. The code still carries no domain vocabulary.
- The issuer test became structural: two non-empty lines directly before `## Kopf`, the same rule `render_html.py` already enforces. Separator style is schema guidance, not a fidelity property.
- `reference/schema.md` pins the issuer form (`<Betrieb> · <Inhaber>`) so the ambiguity cannot recur.

No fidelity gate was changed.

---

## Round 2 — same artifacts, after the fix

```
| 01-clean-complete.report.html    | PASS | PASS | ok |
| 02-missing-fields.report.html    | PASS | PASS | ok |
| 03-english-helper.report.html    | PASS | PASS | ok |
| 04-plumbing.report.html          | PASS | PASS | ok |
| 05-drywall.report.html           | PASS | PASS | ok |
| 06-flooring.report.html          | PASS | PASS | ok |
| planted-defect.report.md         | FAIL | FAIL | ok |
| planted-html-tamper.report.html  | FAIL | FAIL | ok |

**Suite: PASS**
```

### Negative control

A fix that makes a gate pass is worthless if it made the gate stop working. `01-clean-complete` with its two issuer lines deleted was scored again:

```
| shape | FAIL | Ausstellerblock fehlt (zwei Zeilen vor ## Kopf erwartet) |
**Gesamt: FAIL**
```

The gate still refuses a genuinely missing issuer block. Typography was relaxed; structure was not.

### The honest caveat

The checker was changed after seeing the results. That deserves naming, because it is the move that turns an eval into theatre. The justification here is that in both cases the checker contradicted its own written contract, verifiable by anyone who opens `rules.md` § 5 and `reference/schema.md`, and that no fidelity gate was touched. Round 1 is left in this log exactly as it came out.

---

## Round 3 — 2026-09-24, fresh cold round against the fixed schema

Round 2 only re-scored existing artifacts, so it proved the checker fix and not the schema fix. Three fresh agents were given the same three voice notes again.

**The narrow test.** Round 1 produced three different issuer lines. Round 3 produced one, byte-identical across all three runs:

```
04-plumbing  'Berg Reparatur- und Hausmeisterservice \xb7 Jonas Berg'
05-drywall   'Berg Reparatur- und Hausmeisterservice \xb7 Jonas Berg'
06-flooring  'Berg Reparatur- und Hausmeisterservice \xb7 Jonas Berg'
```

The pinned schema form held. That fix is now demonstrated, not asserted.

**Full suite:**

```
| 01-clean-complete.report.html    | PASS | PASS | ok |
| 02-missing-fields.report.html    | PASS | PASS | ok |
| 03-english-helper.report.html    | PASS | PASS | ok |
| 04-plumbing.report.html          | PASS | PASS | ok |
| 05-drywall.report.html           | PASS | PASS | ok |
| 06-flooring.report.html          | PASS | PASS | ok |
| planted-defect.report.md         | FAIL | FAIL | ok |
| planted-html-tamper.report.html  | FAIL | FAIL | ok |

**Suite: PASS**
```

All three cold runs passed `shape`, `dialogue` and `key-match`, hitting the Brutto frozen before round 1.

### What round 3 exposed

The invoice content is now stable, but the **output filename is not**. The same three jobs across two rounds:

| job | round 1 | round 3 |
|---|---|---|
| 4B | `apartment-4b-plumbing-draft.html` | `wohnung-4b-kueche-entwurf.html` |
| Oak Street | `entwurf-oakstreet-2026-09-24.html` | `entwurf-oak-street-2026-09-24.html` |
| unit 12 | `entwurf-einheit-12-boden.html` | `entwurf-einheit12-boden-20260924.html` |

English versus German, different hyphenation, date present or absent, and two date formats. `rules.md` said only `output/<unique-name>.html`, which pins nothing. Fixed by naming the file in `reference/schema.md` and `rules.md` § 10:

- draft: `entwurf_<kunde-slug>_<job-slug>.html`, or `entwurf_kunde-offen_<job-slug>.html` when no contract is named
- final: `<rechnungsnummer>_<kunde-slug>_<rechnungsdatum>.html`

Lowercase, German, hyphens inside a part, underscores between parts, ISO dates.

---

## Open

The filename convention is pinned but not yet exercised by a fresh cold run. Same status the issuer form had before round 3: fixed, unproven. A fourth round would close it.
