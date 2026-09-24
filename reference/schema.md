---
typ: schema
zweck: Die feste Rechnungsform und die Pflichtangaben nach § 14 UStG.
---

# Rechnungs-Schema

Die feste Datenform. Jede Rechnung hat genau diese Abschnitte, in dieser Reihenfolge. Dieses Markdown ist ein **Zwischenschritt** für `render_html.py`; die einzige ausgelieferte Rechnungsdatei ist ein eigenständiges, druckbares HTML. Jedes Feld nennt seinen rechtlichen Grund.

## Pflichtangaben nach § 14 UStG

Fehlt eine davon, darf der Kunde die Vorsteuer nicht ziehen. Fehlt sie in der Quelle, steht `nicht in Quelle` und die Rechnung wird als unvollständig markiert.

1. voller Name und Anschrift des Rechnungsstellers (R, `stammdaten.md`)
2. voller Name, Rechtsform und Anschrift des Kunden (R, `contracts/`)
3. Steuernummer des Gewerbes oder USt-IdNr. (R, `stammdaten.md`)
4. Rechnungsdatum (Q)
5. fortlaufende Rechnungsnummer (Q)
6. Menge und **konkret benannte** Art der Leistung, nicht "Arbeit" (Q)
7. Leistungszeitraum oder Leistungsdatum (A, aus den Log-Daten)
8. Nettoentgelt, Steuersatz, Steuerbetrag, Bruttobetrag, jeweils getrennt (A)
9. jede vorher vereinbarte Entgeltminderung (R, Vertrag, sonst entfällt die Zeile)

## Zusatz: § 35a EStG (Arbeitskosten getrennt)

Privatkunden können 20 % der Arbeitskosten (max. 1.200 € / Jahr) absetzen, aber nur wenn die **Arbeits- und Fahrtkosten getrennt vom Material** ausgewiesen sind und unbar gezahlt wurde. Deshalb trägt jede Rechnung die Zeile *davon Arbeits- und Fahrtkosten (§ 35a EStG)*, netto und brutto. Material zählt hier nicht mit.

## Die feste Form — dieses Skelett genau so ausgeben

Das ist ein Formular zum Ausfüllen, keine Beschreibung. **Gib es Zeichen für Zeichen so aus:** dieselben `##`-Überschriften, dieselben Spaltenköpfe, dieselbe Reihenfolge. Fülle die `<...>`-Platzhalter mit Werten, ändere sonst nichts. Nicht umbenennen, nicht umformatieren, nicht einrücken, kein `&nbsp;`, keine `Leistungen`-Klammer.

Die beiden Ausstellerzeilen kommen aus `stammdaten.md` und stehen genau so, mit `·` als Trenner, direkt vor `## Kopf`.

Weglassen (nur diese): **Fahrtkosten**, wenn keine km genannt sind; **Rückfragen**, wenn die Rechnung vollständig ist; die **Nachlass**-Zeile, wenn der Vertrag keine nennt. Alles andere bleibt stehen. Wenn keine Materialposition genannt ist, bleibt die Materialtabelle ohne Datenzeile. In `Nicht abgebildet` steht `- nichts`, wenn nichts offen ist. Fehlende Werte stehen als `nicht in Quelle`. Solange eine abrechenbare Position oder eine im Job erwähnte Fahrt ohne Kilometerangabe bzw. ausdrücklichen Verzicht ungeklärt ist, bleibt die Ausgabe ein Entwurf; die gezeigten Summen sind nur die Summe der gesicherten Positionen.

```
# Rechnung (<Entwurf | final>)

<nur bei Entwurf, sonst weglassen:> Entwurf unvollständig — offen: <Felder oder Positionen, kommagetrennt>

<Betrieb> · <Inhaber>
<Anschrift> · <E-Mail> · <Telefon>

## Kopf

| Feld | Wert |
|---|---|
| Rechnungsnummer | <BR-JJJJ-NNN | nicht in Quelle> |
| Rechnungsdatum | <TT.MM.JJJJ | nicht in Quelle> |
| Leistungszeitraum | <TT.MM.JJJJ bis TT.MM.JJJJ | nicht in Quelle> |
| Empfänger | <Kunde mit Rechtsform — R: contracts/ | nicht in Quelle> |
| Bezug | <Vertrag/Auftrag | nicht in Quelle> |

## Arbeitsleistung

| Leistung | Wer | Std | Satz netto | Gesamt netto |
|---|---|---|---|---|
| <konkrete Leistung> | <Inhaber / Helfername> | <x,x> | <x,xx> € | <x,xx> € |

## Material

| Position | Einkauf | Aufschlag | Gesamt netto |
|---|---|---|---|
| <Position laut Beleg> | <x,xx> € | ×1,15 | <x,xx> € |

## Fahrtkosten

| km | Satz netto | Gesamt netto |
|---|---|---|
| <x> | 0,50 € | <x,xx> € |

## Summen

| Posten | Betrag |
|---|---|
| Zwischensumme netto | <x,xx> € |
| Vereinbarter Nachlass | <− x,xx € — nur wenn im Vertrag> |
| Nettobetrag | <x,xx> € |
| davon Arbeits- und Fahrtkosten (§ 35a EStG), netto | <x,xx> € |
| davon Arbeits- und Fahrtkosten (§ 35a EStG), brutto | <x,xx> € |
| USt 19 % | <x,xx> € |
| Rechnungsbetrag | <x,xx> € |

## Zahlung

| Feld | Wert |
|---|---|
| Zahlungsziel | <N Tage — R: Vertrag | nicht in Quelle> |
| Fällig | <TT.MM.JJJJ | nicht in Quelle> |
| Kontoinhaber | <R: stammdaten.md> |
| IBAN | <R: stammdaten.md> |
| Verwendungszweck | <BR-JJJJ-NNN | nicht in Quelle> |

Gewährleistung: <Vertragstext | nicht in Quelle>
Steuernummer <R: stammdaten.md> · IBAN <R: stammdaten.md>

## Quellennachweis

| Wert | Tag | Quelle |
|---|---|---|
| <Betrag/Name/Datum> | <Q / R / A / ∅> | <Input-Zeile, reference-Datei, oder Formel mit Zahlen> |

## Nicht abgebildet

- <Zeile aus dem Job-Record ohne abrechenbaren Wert, mit knappem Grund>

## Rückfragen

- <nur bei Entwurf: ein fehlendes Feld je Zeile, Feldname + Format, eine Zeile, keine Erklärung>
```

> `render_html.py` erzeugt aus diesem Skelett die HTML-Vorlage mit Druckansicht und einklappbarem Quellennachweis. Der Eval (`audit/checks.py`) prüft, dass die sichtbare HTML-Rechnung genau aus dem eingebetteten Zwischenschritt gerendert wurde, und prüft dann Form und Rechenwerte. Das Zwischen-Markdown nicht als zweite Ausgabedatei in `output/` ablegen. Steht keine Shell zur Verfügung (z. B. ein claude.ai-Project), ist das ausgefüllte Skelett selbst die gelieferte Rechnung: dann vollständig ausgeben und den fehlenden Render benennen. Der Prüfer liest beide Formate.
