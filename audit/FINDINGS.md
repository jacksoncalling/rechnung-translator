# FINDINGS — the honest read of the eval

What layer 1 proves mechanically, and where it stops on purpose. Naming the edge is the point; a checker that hid its blind spots would be the thing it audits against.

## What is fully deterministic

- **Arithmetic.** Every line, subtotal, the § 35a split, the 19 % USt and the Brutto are recomputed half-up to two decimals and compared. This is the judges' hand-trace, automated. It already caught a real rounding-convention mismatch during the build.
- **Amount coverage.** `no-orphan` refuses euro figures in the line items and sums that are absent from the Quellennachweis; `source-Q` checks that Q-tagged euro amounts appear somewhere in the job record. This catches common inventions, but does not prove the cited line supports the value.
- **Trace structure.** Every Quellennachweis row must carry a valid tag; every cited `reference/` file must exist. The checker does not yet verify the cited field's contents.

## The two layer-2 boundaries (a human or vision confirm)

1. **Receipt-photo values.** When an amount is read from an image in `input/belege/`, a text script cannot verify it against the job record, because the source is a picture. That value's fidelity is confirmed by vision or by a person, not by `checks.py`. This is the same boundary the auditor drew when it left the "does the provision support the class" call to a human.
2. **"Concretely enough named."** Whether a Leistung description satisfies § 14's *konkret benannte Leistung* is semantic. The script checks that a description exists and traces; it does not grade its specificity.

## Where it is deliberately shallow (and the next hardening)

- **`source-Q` is value-presence, not yet scoped-to-line.** It confirms an amount appears somewhere in the job record, not that it appears on the specific activity it is billed under. The auditor shipped the same shape first and added a scoped `quote-in-section` gate in a later round; this eval is built to take the same step. It is named here rather than left for a reader to find.
- **Non-money claims need review.** Dates, names, descriptions, hours, and kilometers are not mechanically checked against their cited source lines. The shape gate checks sections, fields, headers, and order, but not every optional-field rule.
- **Due-date arithmetic** is checked only when the report prints the Zahlungsziel next to the Rechnungsdatum. Without both on the page, the script does not reach into the contract to recompute the date.
- A number that a defect happens to make equal to an unrelated figure already in the job record could pass `source-Q` by coincidence. Low probability, named for honesty.

## What the cold round found (2026-09-24)

Three fresh agents, each given one English voice note and nothing else, produced `04-plumbing`, `05-drywall` and `06-flooring`. Every fidelity gate passed on all three: arithmetic, no-orphan, source-Q, trace-tags, gap-honesty, html-integrity, and **key-match against totals frozen before the runs** (267,61 € / 1.354,47 € / 2.764,97 €).

Two gates failed, and both were defects in **this checker**, not in the translator:

1. **`dialogue`** demanded the literal word `Empfänger` in the Rückfragen, while `rules.md` § 5 tells the agent to ask `Welcher Vertrag/Kunde?`. All three asked correctly and were failed for it. Fixed with a synonym list in `conventions.json`, so the code still carries no domain.
2. **`shape`** demanded a punctuation style for the issuer block that the schema never specified. The three agents wrote `service, Jonas Berg`, `service, Inhaber Jonas Berg` and `service — Inhaber Jonas Berg`, all reasonable readings of the old placeholder `<Betrieb, Inhaber — …>`. The check is now structural (two lines before `## Kopf`, the same rule `render_html.py` enforces) and the schema pins the form so the ambiguity cannot recur.

Worth stating plainly: the checker was changed after seeing the results, which is a thing to be careful about. The justification is that in both cases the checker contradicted the documented contract, which anyone can verify by reading `rules.md` § 5 and the schema. No fidelity gate was relaxed; removing the issuer lines entirely still fails `shape`.

## What this means

The deterministic layer is strong precisely because a repair invoice is mostly arithmetic and provenance, which machines check better than people. The two boundaries are real and small, and they are exactly the places a human should still look. That division, stated out loud, is the point of the folder.
