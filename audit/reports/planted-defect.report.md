# Rechnung (final) — ABSICHTLICH FEHLERHAFT (planted defect)

Dieser Bericht trägt fünf eingebaute Fehler. Der Eval MUSS ihn ablehnen (exit 1).
Keys: `audit/keys/planted-defect` nicht nötig, der Lauf erwartet FAIL.

## Kopf

| Feld | Wert |
|---|---|
| Rechnungsnummer | BR-2026-014 |
| Rechnungsdatum | 22.09.2026 |
| Leistungszeitraum | 08.09.2026 bis 12.09.2026 |
| Empfänger | Wohnbaugenossenschaft Musterstadt eG |

## Arbeitsleistung

| Leistung | Wer | Std | Satz netto | Gesamt netto |
|---|---|---|---|---|
| Wasserhahn, Dichtungen getauscht (08.09.) | Inhaber | 1,5 | 60,00 € | 90,00 € |
| Türen geölt, Scharniere nachgezogen (08.09.) | Inhaber | 0,75 | 60,00 € | 45,00 € |
| Kellertür gestrichen, Rahmen ausgebessert (10.09.) | Inhaber | 2,0 | 60,00 € | 120,00 € |
| Kellertür gestrichen, Rahmen ausgebessert (10.09.) | König | 2,0 | 42,00 € | 84,00 € |
| Fensterbänke montiert (12.09.) | Inhaber | 1,0 | 60,00 € | 60,00 € |
| Fensterbänke montiert (12.09.) | König | 3,0 | 42,00 € | 130,00 € |

## Material

| Position | Einkauf | Aufschlag | Gesamt netto |
|---|---|---|---|
| Dichtungssortiment und Öl | 42,02 € | ×1,15 | 48,32 € |
| Holzlack und Pinsel | 63,80 € | ×1,15 | 73,37 € |
| Fensterbänke, Zuschnitt | 128,50 € | ×1,15 | 147,78 € |
| Phantommaterial (nie gekauft) | 999,00 € | ×1,00 | 999,00 € |

## Fahrtkosten

| km | Satz netto | Gesamt netto |
|---|---|---|
| 54 | 0,50 € | 27,00 € |

## Summen

| Posten | Betrag |
|---|---|
| Zwischensumme netto | 821,47 € |
| Nettobetrag | 821,47 € |
| davon Arbeits- und Fahrtkosten (§ 35a EStG), netto | 552,00 € |
| davon Arbeits- und Fahrtkosten (§ 35a EStG), brutto | 656,88 € |
| USt 19 % | 150,00 € |
| Trinkgeld | 5,00 € |
| Rechnungsbetrag | 977,55 € |

## Zahlung

| Feld | Wert |
|---|---|
| Zahlungsziel | 14 Tage |
| Fällig | 06.10.2026 |
| Kontoinhaber | Jonas Berg |
| IBAN | DE00 0000 0000 0000 0000 00 |
| Verwendungszweck | BR-2026-014 |

## Quellennachweis

| Wert | Tag | Quelle |
|---|---|---|
| BR-2026-014 | Q | Input, Zeile "Rechnungsnummer" |
| 22.09.2026 | Q | Input, Zeile "Rechnungsdatum" |
| Empfänger, Anschrift | R | reference/contracts/musterstadt-eg.md |
| 90,00 € | A | 1,5 × 60,00 |
| 45,00 € | X | 0,75 × 60,00 |
| 120,00 € | A | 2,0 × 60,00 |
| 84,00 € | A | 2,0 × 42,00 |
| 60,00 € | A | 1,0 × 60,00 |
| 126,00 € | A | 3,0 × 42,00 |
| 60,00 € Satz | R | reference/pricing.md |
| 42,00 € Satz | R | reference/team/m-koenig.md |
| 48,32 € | A | 42,02 × 1,15 |
| 42,02 € Einkauf | Q | Input, Beleg Baumarkt |
| 73,37 € | A | 63,80 × 1,15 |
| 63,80 € Einkauf | Q | Input, Beleg Farbenhaus |
| 147,78 € | A | 128,50 × 1,15 |
| 128,50 € Einkauf | Q | Input, Beleg Beschlag-Handel |
| 999,00 € Einkauf | Q | Input, Beleg (erfunden) |
| 999,00 € | A | 999,00 × 1,00 |
| 27,00 € | A | 54 × 0,50 |
| 0,50 € Satz | R | reference/pricing.md |
| 821,47 € | A | Summe |
| 552,00 € | A | Arbeit + Fahrt |
| 656,88 € | A | 552,00 × 1,19 |
| 977,55 € | A | 821,47 + 156,08 |

## Nicht abgebildet

- Kaffeemaschine: nur angeschaut.
