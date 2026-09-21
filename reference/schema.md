---
typ: schema
zweck: Die feste Rechnungsform und die Pflichtangaben nach § 14 UStG.
---

# Rechnungs-Schema

Die feste Ausgabeform. Jede Rechnung hat genau diese Abschnitte, in dieser Reihenfolge. Jedes Feld nennt seinen rechtlichen Grund.

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

## Die feste Form

```
[Kopfnotiz nur wenn unvollständig: "Entwurf unvollständig — fehlende Pflichtangabe: ..."]

<Betrieb, Inhaber>
<Anschrift> · <Kontakt>

An:
<Kunde mit Rechtsform>
<Ansprechpartner>
<Anschrift>

Rechnungsnummer   <BR-JJJJ-NNN | nicht in Quelle>
Rechnungsdatum    <TT.MM.JJJJ | nicht in Quelle>
Leistungszeitraum <TT.MM.JJJJ bis TT.MM.JJJJ>
Bezug             <Vertrag/Auftrag, falls genannt>

Leistungen

  Arbeitsleistung
  | Leistung (konkret) | Std | Satz netto | Gesamt netto |
  ... Inhaber, dann je Helfer ...

  Material
  | Position | Einkauf | Aufschlag | Gesamt netto |
  ... eine Zeile je Beleg; Aufschlag als gezeigte Rechnung ...

  Fahrtkosten (nur wenn km genannt)
  | km | Satz netto | Gesamt netto |

  Zwischensumme netto            <A>
  [Vereinbarter Nachlass]        <R, sonst entfällt>
  Nettobetrag                    <A>
  davon Arbeits- und Fahrtkosten (§ 35a EStG)  <A: netto / brutto>
  zzgl. 19 % USt                 <A>
  Rechnungsbetrag                <A>

Zahlung
  Zahlbar bis <A: Rechnungsdatum + Zahlungsziel | nicht in Quelle>
  Kontoinhaber / IBAN            <R>
  Verwendungszweck               <Q: Rechnungsnummer>

Gewährleistung                   <R, Vertrag>
Steuernummer / IBAN              <R>

Quellennachweis
  | Wert | Tag | Quelle |
  ... eine Zeile je Ausgabewert ...

Nicht abgebildet
  ... Zeilen aus dem Job-Record ohne abrechenbaren Wert, mit Grund ...
```
