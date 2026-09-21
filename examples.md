# Examples

Three pairs. Example 1 shows the contract holding on a clean job. Example 2 shows it breaking gracefully on missing fields, marking gaps instead of filling them. Example 3 shows it refusing an out-of-scope input instead of branching. All figures trace; check them.

All three run against `reference/contracts/musterstadt-eg.md` (Stundensatz 60,00 €, Helfer laut Datei, Materialaufschlag 15 %, Fahrt 0,50 €/km, Zahlungsziel 14 Tage).

---

## Example 1 — clean job, contract holds

### Input

```
Vertrag: Musterstadt eG
Rechnungsnummer: BR-2026-011
Rechnungsdatum: 15.09.2026

Di 02.09.: Wohnungstür klemmt, Schloss nachgestellt. 2,0 Std. Anfahrt 10 km.
Material: Baumarkt 02.09., Schmiermittel und Kleinteile. 11,90 €
```

### Output

```
Berg Reparatur- und Hausmeisterservice · Jonas Berg
Beispielweg 12, 52070 Aachen · jonas@berg-reparatur.example

An:
Wohnbaugenossenschaft Musterstadt eG
z. Hd. Frau Hartmann, Technik
Genossenschaftsplatz 1, 45000 Musterstadt

Rechnungsnummer    BR-2026-011
Rechnungsdatum     15.09.2026
Leistungszeitraum  02.09.2026
Bezug              Rahmenauftrag Instandhaltung 2026 (WG-Musterstadt)

Leistungen

  Arbeitsleistung
  | Leistung                          | Std | Satz netto | Gesamt netto |
  | Wohnungstür, Schloss nachgestellt | 2,0 |   60,00 €  |    120,00 €  |

  Material
  | Position                        | Einkauf  | Aufschlag | Gesamt netto |
  | Schmiermittel und Kleinteile    | 11,90 €  | × 1,15    |    13,69 €   |

  Fahrtkosten
  | km | Satz netto | Gesamt netto |
  | 10 |  0,50 €    |    5,00 €    |

  Zwischensumme netto                              138,69 €
  Nettobetrag                                      138,69 €
  davon Arbeits- und Fahrtkosten (§ 35a EStG)      125,00 € netto / 148,75 € brutto
  zzgl. 19 % USt                                    26,35 €
  Rechnungsbetrag                                  165,04 €

Zahlung
  Zahlbar ohne Abzug bis 29.09.2026
  Kontoinhaber: Jonas Berg · IBAN DE00 0000 0000 0000 0000 00
  Verwendungszweck: BR-2026-011

Gewährleistung: 2 Jahre ab Abnahme (§ 634a BGB)
Steuernummer 201/1234/5678 · IBAN DE00 0000 0000 0000 0000 00

Quellennachweis
  | Wert                         | Tag | Quelle |
  | BR-2026-011                  | Q   | Input, Zeile "Rechnungsnummer" |
  | 15.09.2026                   | Q   | Input, Zeile "Rechnungsdatum" |
  | Kunde, Anschrift             | R   | contracts/musterstadt-eg.md |
  | Leistungstext                | Q   | Input, "Wohnungstür ... Schloss nachgestellt" |
  | 2,0 Std                      | Q   | Input, "2,0 Std" |
  | 60,00 € Satz                 | R   | contracts/musterstadt-eg.md |
  | 120,00 € Arbeit              | A   | 2,0 × 60,00 |
  | 11,90 € Einkauf              | Q   | Input, Beleg Baumarkt 02.09. |
  | 13,69 € Material netto       | A   | 11,90 × 1,15 = 13,685 → 13,69 |
  | 10 km                        | Q   | Input, "Anfahrt 10 km" |
  | 5,00 € Fahrt                 | A   | 10 × 0,50 |
  | 138,69 € Zwischensumme/Netto | A   | 120,00 + 13,69 + 5,00 |
  | 125,00 € § 35a netto         | A   | 120,00 + 5,00 (Material ausgenommen) |
  | 148,75 € § 35a brutto        | A   | 125,00 × 1,19 |
  | 26,35 € USt                  | A   | 138,69 × 0,19 = 26,3511 → 26,35 |
  | 165,04 € Brutto              | A   | 138,69 + 26,35 |
  | 29.09.2026 Fälligkeit        | A   | 15.09.2026 + 14 Tage (contract) |

Nicht abgebildet
  (nichts — jede Zeile des Job-Records wurde abgebildet)
```

---

## Example 2 — missing fields, marked not filled

Input has no Rechnungsdatum, an illegible receipt amount, no distance for the trip, and a future request. The translator marks each gap and refuses to invent.

### Input

```
Vertrag: Musterstadt eG
Rechnungsnummer: BR-2026-012

Do 04.09.: Gartentor, Scharnier getauscht. 1,0 Std.
Material: Beleg Scharnier vorhanden, Betrag unleserlich.
Notiz: Mieter fragte nach neuem Rollladen, kommt später.
```

### Output

```
Entwurf unvollständig — fehlende Pflichtangabe: Rechnungsdatum

Berg Reparatur- und Hausmeisterservice · Jonas Berg
Beispielweg 12, 52070 Aachen

An:
Wohnbaugenossenschaft Musterstadt eG
z. Hd. Frau Hartmann, Technik
Genossenschaftsplatz 1, 45000 Musterstadt

Rechnungsnummer    BR-2026-012
Rechnungsdatum     nicht in Quelle
Leistungszeitraum  04.09.2026
Bezug              Rahmenauftrag Instandhaltung 2026 (WG-Musterstadt)

Leistungen

  Arbeitsleistung
  | Leistung                     | Std | Satz netto | Gesamt netto |
  | Gartentor, Scharnier getauscht | 1,0 | 60,00 €   |    60,00 €   |

  Material
  | Position           | Einkauf         | Aufschlag | Gesamt netto |
  | Scharnier          | nicht in Quelle | —         | nicht in Quelle (aus Summe ausgenommen) |

  Fahrtkosten
  | keine — Distanz nicht in Quelle |

  Zwischensumme netto                              60,00 €
  Nettobetrag                                      60,00 €
  davon Arbeits- und Fahrtkosten (§ 35a EStG)      60,00 € netto / 71,40 € brutto
  zzgl. 19 % USt                                   11,40 €
  Rechnungsbetrag                                  71,40 €

Zahlung
  Zahlbar ohne Abzug bis nicht in Quelle (benötigt Rechnungsdatum)
  Kontoinhaber: Jonas Berg · IBAN DE00 0000 0000 0000 0000 00
  Verwendungszweck: BR-2026-012

Gewährleistung: 2 Jahre ab Abnahme (§ 634a BGB)
Steuernummer 201/1234/5678

Quellennachweis
  | Wert                    | Tag | Quelle |
  | BR-2026-012             | Q   | Input, "Rechnungsnummer" |
  | Rechnungsdatum          | ∅   | nicht in Quelle |
  | 04.09.2026 Zeitraum     | A   | einziges Datum im Log |
  | 1,0 Std                 | Q   | Input, "1,0 Std" |
  | 60,00 € Arbeit          | A   | 1,0 × 60,00 |
  | Scharnier Betrag        | ∅   | nicht in Quelle (Beleg unleserlich) |
  | Fahrtdistanz            | ∅   | nicht in Quelle (nicht notiert) |
  | 60,00 € Netto           | A   | nur Arbeit; Material und Fahrt fehlen |
  | 11,40 € USt             | A   | 60,00 × 0,19 |
  | 71,40 € Brutto          | A   | 60,00 + 11,40 |
  | Fälligkeit              | ∅   | braucht Rechnungsdatum |

Nicht abgebildet
  | Rollladen-Anfrage des Mieters — keine Leistung erbracht, kein Auftrag, Zukunft |
```

Note what did **not** happen: no invented date, no guessed material cost, no distance derived from the address, and the tenant's request was surfaced, not dropped. The invoice is produced so the person sees exactly the two things to fix (date, receipt amount) before it can go out.

---

## Example 3 — out of scope, refused

Input asks for a partial invoice. The folder handles one shape only, so it refuses.

### Input

```
Vertrag: Musterstadt eG
Rechnungsnummer: BR-2026-013
Rechnungsdatum: 20.09.2026

Kunde möchte 50 % Abschlag jetzt, Rest nach Abschluss.
Mo 15.09.: Fassade Vorarbeiten. 4 Std.
```

### Output

```
ABLEHNUNG — ausserhalb des Vertrags

Dieser Übersetzer erzeugt nur Standard-Inlandsrechnungen mit 19 % USt.
Ausgelöst durch: "Kunde möchte 50 % Abschlag jetzt, Rest nach Abschluss."
Grund: Abschlag/Anzahlung braucht Anzahlungslogik und den Abzug bereits
berechneter USt in der Schlussrechnung (§ 14c UStG). Das ist eine eigene Form.

Es wurde keine Rechnung erzeugt. Für diesen Fall ist eine andere Form nötig.
```

No partial invoice. No attempt to bill the 4 hours anyway. Trigger named, refused, done.
