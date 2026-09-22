# FINDINGS — the honest read of the eval

What layer 1 proves mechanically, and where it stops on purpose. Naming the edge is the point; a checker that hid its blind spots would be the thing it audits against.

## What is fully deterministic

- **Arithmetic.** Every line, subtotal, the § 35a split, the 19 % USt and the Brutto are recomputed half-up to two decimals and compared. This is the judges' hand-trace, automated. It already caught a real rounding-convention mismatch during the build.
- **No invented amount.** `no-orphan` refuses any euro figure in the invoice that is not accounted for in the Quellennachweis; `source-Q` refuses any Q amount not present in the job record. Together they are the mechanical form of "nothing invented."
- **Trace discipline.** Every Quellennachweis row must carry a valid tag; every cited `reference/` file must exist.

## The two layer-2 boundaries (a human or vision confirm)

1. **Receipt-photo values.** When an amount is read from an image in `input/belege/`, a text script cannot verify it against the job record, because the source is a picture. That value's fidelity is confirmed by vision or by a person, not by `checks.py`. This is the same boundary the auditor drew when it left the "does the provision support the class" call to a human.
2. **"Concretely enough named."** Whether a Leistung description satisfies § 14's *konkret benannte Leistung* is semantic. The script checks that a description exists and traces; it does not grade its specificity.

## Where it is deliberately shallow (and the next hardening)

- **`source-Q` is value-presence, not yet scoped-to-line.** It confirms an amount appears somewhere in the job record, not that it appears on the specific activity it is billed under. The auditor shipped the same shape first and added a scoped `quote-in-section` gate in a later round; this eval is built to take the same step. It is named here rather than left for a reader to find.
- **Due-date arithmetic** is checked only when the report prints the Zahlungsziel next to the Rechnungsdatum. Without both on the page, the script does not reach into the contract to recompute the date.
- A number that a defect happens to make equal to an unrelated figure already in the job record could pass `source-Q` by coincidence. Low probability, named for honesty.

## What this means

The deterministic layer is strong precisely because a repair invoice is mostly arithmetic and provenance, which machines check better than people. The two boundaries are real and small, and they are exactly the places a human should still look. That division, stated out loud, is the point of the folder.
