---
typ: preise
hinweis: Standard-Sätze. Ein Vertrag in contracts/ kann jeden Satz überschreiben.
---

# Preise (Standard)

Die Rückfall-Sätze, wenn der Vertrag nichts anderes sagt. Werden als **R** übernommen. Alle Beträge **netto**.

| Feld | Wert | Bezug |
|---|---|---|
| Stundensatz Inhaber | 60,00 € / h | allgemeine Reparaturarbeiten, 2026: Geselle 55–70 € netto |
| Verrechnungssatz Helfer | 40,00 € / h | Rückfall, wenn `team/<name>.md` keinen eigenen Satz nennt |
| Fahrtkosten | 0,50 € / km | Anfahrt, gilt als Arbeits-/Nebenkosten (§ 35a EStG) |
| Materialaufschlag | 15 % | auf den Einkaufspreis laut Beleg |
| USt-Satz | 19 % | Regelbesteuerung |
| Währung | immer EUR | Beträge ohne Symbol sind Euro; danach wird nie gefragt |

## Regeln zur Anwendung

- Ein Wert aus `contracts/<job>.md` schlägt immer den Standard hier.
- Ein Helfer-Satz aus `team/<name>.md` schlägt den Helfer-Standard hier.
- Der Materialaufschlag erscheint in jeder Materialzeile als gezeigte Rechnung: `Einkauf × 1,15`.
- Diese Datei enthält **keine** internen Löhne. Was ein Helfer verdient, steht in seiner Datei und gehört nie auf eine Rechnung.
