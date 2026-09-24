# Examples

Three input/output pairs show the same schema on a complete job, an incomplete job, and an English job note. The report files are worked examples and answer keys for the audit. **Do not give them to the agent during a cold run.**

| Case | Input | Expected output | What it exercises |
|---|---|---|---|
| 1 — complete repair job | [job record](audit/fixtures/01-clean-complete.md) | [HTML invoice](audit/reports/01-clean-complete.report.html) | Multiple days, two workers, three materials, travel, non-billable note. |
| 2 — missing fields | [job record](audit/fixtures/02-missing-fields.md) | [HTML draft](audit/reports/02-missing-fields.report.html) | `nicht in Quelle`, concise Rückfragen, no invented date or number. |
| 3 — English note | [job record](audit/fixtures/03-english-helper.md) | [HTML invoice](audit/reports/03-english-helper.report.html) | German output, helper's billable rate, one round-trip distance, net receipt amount. |

The input and output are kept in separate files so a test runner can expose only the input to a fresh agent. The HTML outputs are rendered from the fixed intermediate form in `reference/schema.md`; the agent should reproduce its **contract**, not memorize its wording.

## Case 2 in full, so this file stands on its own

**Input** ([`02-missing-fields.md`](audit/fixtures/02-missing-fields.md)):

```
Vertrag: Musterstadt eG

19.09.2026: Gartentor, lockeres Scharnier befestigt. Inhaber 2 Std.
Notiz: Mieter fragte nach einem neuen Rollladen für nächsten Monat. Dazu wurde heute nichts ausgeführt.
```

**Output**, the lines that carry the contract (full file: [`02-missing-fields.report.html`](audit/reports/02-missing-fields.report.html)):

```
# Rechnung (Entwurf)

Entwurf unvollständig — offen: Rechnungsnummer, Rechnungsdatum

| Rechnungsnummer   | nicht in Quelle |
| Rechnungsdatum    | nicht in Quelle |
| Leistungszeitraum | 19.09.2026      |

| Gartentor, lockeres Scharnier befestigt | Inhaber | 2 | 60,00 € | 120,00 € |

| Fällig | nicht in Quelle |

## Quellennachweis
| Rechnungsnummer, Rechnungsdatum | ∅ | nicht in Quelle |
| 19.09.2026                      | Q | Input, Arbeitszeile |
| 60,00 €                         | R | reference/contracts/musterstadt-eg.md, Stundensatz Inhaber |
| 120,00 €                        | A | 2 × 60,00 |

## Nicht abgebildet
- Notiz: Mieter fragte nach einem neuen Rollladen ... — keine ausgeführte Leistung.

## Rückfragen
- Rechnungsnummer? (BR-JJJJ-NNN)
- Rechnungsdatum? (TT.MM.JJJJ)
```

Note what did **not** happen: no invoice number invented, no today's date stamped in, no Fälligkeit guessed from a date that does not exist, and the tenant's Rollladen request surfaced rather than dropped. Every figure traces: the rate to the contract, the total to its formula, the date to the input line.

## Follow-up for case 2

If the user answers `Rechnungsnummer: BR-2026-022. Rechnungsdatum: 22.09.2026.`, the translator must replace the two missing fields, derive `Fällig: 06.10.2026`, and return a final invoice with the same labor and sums. It must keep the Rollladen note in `Nicht abgebildet` and remove `Rückfragen`.

## Audio test

A recorded voice note can be the input after transcription. Preserve the transcription verbatim as the source; do not silently repair uncertain words or numbers. Run the fresh agent with the transcript and the allowed reference files, then compare every invoice fact to the transcript or a named reference field. Audio itself and the transcription are separate evidence: if the transcription is uncertain, ask rather than infer.
