---
typ: ausschluss
---

# Ausserhalb des Vertrags (Refusals)

Dieser Ordner erzeugt **eine** Rechnungsform: Inland, volle Leistung, 19 % USt. Alles andere wird offen abgelehnt, nicht in eine zweite Form verzweigt. Eine Form pro Lauf ist die ganze Aufgabe.

## Auslöser

| Auslöser im Job-Record | Warum ausgeschlossen |
|---|---|
| Abschlag, Anzahlung, Teilzahlung, Schlussrechnung | Braucht Anzahlungslogik und den Abzug bereits berechneter USt (§ 14c UStG). Eigene Form. |
| Kunde im Ausland, USt-IdNr. für Reverse Charge, Drittland | Kein deutscher USt-Ausweis, anderer Pflichttext (§ 3a UStG / Art. 196 MwSt-RL). Eigene Form. |
| Steuersatz ≠ 19 % (z. B. 7 %, oder § 19 Kleinunternehmer) | Anderer Steuerausweis. Nicht die zugesagte Form. |

## Der Ablehnungsblock (unverändert ausgeben)

```
ABLEHNUNG — ausserhalb des Vertrags

Dieser Übersetzer erzeugt nur Standard-Inlandsrechnungen mit 19 % USt.
Ausgelöst durch: <konkrete Zeile aus dem Job-Record>
Grund: <die passende Zeile aus out-of-scope.md>

Es wurde keine Rechnung erzeugt. Für diesen Fall ist eine andere Form nötig.
```

Keine Teilrechnung, kein "ich versuche es trotzdem". Auslöser benennen, ablehnen, Schluss.
