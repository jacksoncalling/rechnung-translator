---
typ: beleg-lesen
zweck: Wie ein Beleg aus einem Foto, Scan oder PDF gelesen wird, ohne eine Ziffer zu erfinden.
---

# Beleg lesen (Foto / Scan / PDF)

Ein Beleg kann im Job-Record **als Text beschrieben** sein oder als **Bild/Scan/PDF** in `input/belege/` liegen (oder angehängt sein). Bei einem Bild liest der Übersetzer den Beleg direkt. Das Bild ist dann die Quelle. Der gelesene Wert ist **Q**, zitiert wird der Dateiname.

## Die eiserne Regel

Ein Foto senkt die Messlatte nicht, es hebt sie. Der eine Weg, diese Aufgabe zu verlieren (eine erfundene Zahl), ist beim Lesen eines unscharfen Belegs am leichtesten zu gehen.

- **Nur lesen, was klar gedruckt steht.** Zeichen exakt übernehmen, deutsches Zahlenformat (Komma).
- **Keine Ziffer raten.** Eine verschmierte 3 ist keine plausible 8. Ist ein Zeichen nicht sicher lesbar, gilt das ganze Feld als `nicht sicher lesbar`, wird aus jeder Summe ausgenommen und zur Bestätigung markiert.
- **Nichts hinzudichten.** Kein Datum, kein Betrag, kein Händler, der nicht auf dem Beleg steht.

## Was gelesen wird

Händler, Datum, die relevante(n) Materialposition(en) mit Betrag, sowie Netto / USt / Brutto, falls ausgewiesen.

**Basis für den Materialaufschlag ist der Netto-Einkauf** (die Vorsteuer wird gezogen):
- Zeigt der Beleg Netto und Brutto, wird der **Netto**-Betrag genommen.
- Ist nur ein Bruttobetrag lesbar und der Beleg nennt 19 % USt, dann `netto = brutto ÷ 1,19`, als **A** mit gezeigter Rechnung.
- Ist unklar, ob eine Zahl netto oder brutto ist, wird sie **nicht** aufgeteilt. Der gedruckte Wert wird so übernommen, wie der Beleg ihn benennt, und zur Bestätigung markiert.

## Zwischenschritt: Beleg-Extraktion (Prüffläche)

Bevor die Rechnung gebaut wird, gibt der Übersetzer eine Extraktionstabelle aus, die ein Mensch bestätigt. Nur bestätigte Werte fliessen in die Rechnung. Hier wird ein Lesefehler gefangen, bevor er zu einer Rechnung wird.

```
Beleg-Extraktion
| Datei | Händler | Datum | Position | Betrag netto | Lesbarkeit |
```

Jede Zeile taucht später im Quellennachweis wieder auf, getaggt `Q → Beleg-Foto <datei>`.
