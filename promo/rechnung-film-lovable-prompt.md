# Lovable prompt — Rechnung-Übersetzer film (DE + EN)

Add a new silent, looping teaser film to this project, in the exact same style and architecture as the existing `reisemapper` and `auditor` films. Do not touch existing routes or films. Reuse the existing scaffold; do not reinvent it.

## Reuse (already in the repo — import, don't rebuild)
- `@/components/anim/StagePortrait` — fixed 1080×1350 (4:5) stage, letterboxed for clean screen-recording.
- `@/lib/anim` — `useLoopClock`, `ease`, `clamp01`, `window01`, `typedSlice`, `typeThenDelete`.
- Copy the local timing helpers used in `ReisemapperFilm.tsx`:
  - `const w = (ms,a,b) => ease(window01(ms,a,b));`
  - `const band = (ms,a,b,d=350) => clamp01(Math.min((ms-a)/d,(b-ms)/d,1));`
- Follow the **two-language pattern of the auditor film**: one `content.ts` holds the real invoice data (always German, verbatim) plus a DE and EN caption pack; the `RechnungFilm` component takes a `pack` prop and only the framing captions differ. Real invoice content is identical in both versions.

## Files to create
- `src/components/anim/rechnung/tokens.ts`
- `src/components/anim/rechnung/content.ts`
- `src/components/anim/rechnung/RechnungFilm.tsx`  (exports `RechnungFilm({ pack }: { pack: Pack })`)
- `src/routes/rechnung.tsx`      → renders `<RechnungFilm pack={DE} />`
- `src/routes/rechnung-en.tsx`   → renders `<RechnungFilm pack={EN} />`

## tokens.ts — reuse the reisemapper palette so the films look like one set
```ts
export const R = {
  paper: "#F1E7D3", paperLit: "#FBF4E6", card: "#FCF6EA",
  ink: "#22333B", inkSoft: "#4C5F63",
  ochre: "#E0A32E", teal: "#2A9D8F", coral: "#E4633C",
  skin: "#F0C9A8", hair: "#4A3B33",
};
export const SERIF = '"Fraunces", Georgia, serif';
export const SANS  = '"Nunito", system-ui, sans-serif';
export const TOTAL_MS = 60000; // ~60s silent loop
export const BEATS = {
  feierabend:  [0, 7000],
  notiz:       [7000, 16000],
  rechenwerk:  [16000, 27000],  // the transform — the money shot, give it the most room
  rechnung:    [27000, 38000],
  posteingang: [38000, 44000],
  check:       [44000, 49500],
  raus:        [49500, 54000],
  daumen:      [54000, 60000],
} as const;
```

## content.ts — REAL tool output (German, verbatim in BOTH versions)

Messy phone note that types in during beat 2 (use `typedSlice`, chat-style, slightly sloppy):
```
Musterstadt eG
Mo 08.09. Wasserhahn 3.OG Dichtung 1,5 Std. 2 Türen geölt 0,75 Std. Anfahrt 18 km.
Mi 10.09. Kellertür gestrichen, ich 2 Std, König 2 Std. Anfahrt 18 km.
Fr 12.09. 3 Fensterbänke EG, König 3 Std, ich 1 Std. Anfahrt 18 km.
Belege: Baumarkt 42,02 · Farbenhaus 63,80 · Beschlag 128,50
Kaffeemaschine Gemeinschaftsraum läuft nicht — nur angeschaut.
```

Clean invoice (beat 4). Every figure is real and traces to a source:
- Kopf: Rechnungsnummer **BR-2026-014** · Datum **22.09.2026** · Leistungszeitraum **08.–12.09.2026**
- Aussteller: **Berg Reparatur- & Hausmeisterservice** · Empfänger: **Wohnbaugenossenschaft Musterstadt eG**
- Arbeitsleistung (§ 35a) — [Leistung, Wer, Std, Satz, Gesamt]:
  - Wasserhahn, Dichtungen (08.09.) · Inhaber · 1,5 · 60,00 € · **90,00 €**
  - Türen geölt, Scharniere (08.09.) · Inhaber · 0,75 · 60,00 € · **45,00 €**
  - Kellertür gestrichen (10.09.) · Inhaber · 2,0 · 60,00 € · **120,00 €**
  - Kellertür gestrichen (10.09.) · König · 2,0 · 42,00 € · **84,00 €**
  - Fensterbänke montiert (12.09.) · Inhaber · 1,0 · 60,00 € · **60,00 €**
  - Fensterbänke montiert (12.09.) · König · 3,0 · 42,00 € · **126,00 €**
- Material (Einkauf ×1,15) — [Position, Einkauf, Gesamt]:
  - Dichtungen und Öl · 42,02 € · **48,32 €**
  - Holzlack und Pinsel · 63,80 € · **73,37 €**
  - Fensterbänke, Zuschnitt · 128,50 € · **147,78 €**
- Fahrtkosten: 54 km × 0,50 € = **27,00 €**
- Summen: Nettobetrag **821,47 €** · davon Arbeit+Fahrt (§ 35a) netto **552,00 €** / brutto **656,88 €** · USt 19 % **156,08 €** · **Rechnungsbetrag 977,55 €** · Fällig **06.10.2026**
- Nicht abgebildet (the dropped line — show it visibly leave the invoice): **„Kaffeemaschine im Gemeinschaftsraum — nur angeschaut, nichts abzurechnen."**
- Quellennachweis flashes (small, 2–3, to prove traceability): `90,00 € = 1,5 × 60,00` · `60,00 € Satz → contracts/musterstadt-eg.md` · `42,00 € Satz → team/m-koenig.md`

## Caption packs (framing prose only). Big italic serif line + small "Beat N · title" sub, like reisemapper.

DE:
1. „Feierabend. Und dann noch die Rechnungen schreiben." — Beat 1 · der Papierkram
2. „Ich tippe es so, wie ich es sagen würde." — Beat 2 · die Notiz
3. „Kein Zaubertrick. Jede Zahl kommt aus einer Quelle." — Beat 3 · das Rechenwerk
4. „Fertige Rechnung nach § 14 UStG. Und die Kaffeemaschine? Bleibt draußen." — Beat 4 · die Rechnung
5. „Landet im Postausgang. Ein Blick genügt." — Beat 5 · der Posteingang
6. „Passt." — Beat 6 · der Haken
7. „Raus damit." — Beat 7 · gesendet
8. „977,55 €. In zwei Minuten statt am Sonntagabend." — Beat 8 · Daumen hoch

EN:
1. "End of the day. And still the invoices to write." — Beat 1 · the paperwork
2. "I just type it the way I'd say it." — Beat 2 · the note
3. "No magic trick. Every number comes from a source." — Beat 3 · the reckoning
4. "A finished invoice, § 14 UStG. And the coffee machine? Left out." — Beat 4 · the invoice
5. "It lands in the outbox. One glance is enough." — Beat 5 · the outbox
6. "Checks out." — Beat 6 · the check
7. "Off it goes." — Beat 7 · sent
8. "977.55 €. In two minutes, not on a Sunday night." — Beat 8 · thumbs up

## Storyboard — draw everything as hand inline SVG in a `viewBox="0 0 780 480"` stage (same as reisemapper). Warm paper radial-gradient background, uppercase eyebrow at top ("RECHNUNG-ÜBERSETZER" / "INVOICE TRANSLATOR"), progress bar at bottom, caption block near the bottom. One character throughout: a friendly Handwerker, drawn in the same simple style as the reisemapper people (round head, skin/hair tokens, teal overalls). He smiles the whole way through; the smile just grows.

- **Beat 1 · feierabend (0–7000):** Handwerker sitting in the van seat, phone in one hand, small tired-but-good smile. Beside him a small stack of crumpled job notes / receipts with a coral "3" badge (the backlog). Gentle idle bob.
- **Beat 2 · notiz (7000–16000):** Push in on the phone. The messy note types in on the screen (`typedSlice` over ~7000–15000), chat-style, imperfect. He's thumbing it in. Half-smile.
- **Beat 3 · rechenwerk (16000–27000) — the money shot, let it breathe:** The typed note detaches from the phone and flies into a friendly machine/hopper (gears or a stylised funnel in ochre/teal). Inside, values snap into place: `§ 14 UStG` and `§ 35a` labels attach to rows, numbers tick up, the Quellennachweis flashes (`90,00 € = 1,5 × 60,00`, a rate resolving to `contracts/musterstadt-eg.md`). The Kaffeemaschine chip is visibly pushed OFF to the side (foreshadow the drop). No frantic energy — precise, calm, satisfying.
- **Beat 4 · rechnung (27000–38000):** A clean invoice sheet rises/slides out of the machine (like the reisemapper folder rising). Header (BR-2026-014 · 22.09.2026), a few labor rows appearing in sequence (stagger, like the folder ROWS), a material row, then the big **Rechnungsbetrag 977,55 €** lands with weight. The **Kaffeemaschine line drops down into a small „Nicht abgebildet" strip** with a callout badge: DE „erfindet nichts" / EN "invents nothing". This is the proof beat.
- **Beat 5 · posteingang (38000–44000):** The invoice shrinks into an email/outbox card (reuse the reisemapper email-envelope drawing style), sliding into an outbox tray.
- **Beat 6 · check (44000–49500):** He taps; a green (teal) check ✓ scales in over the card (reuse the folder-row check animation).
- **Beat 7 · raus (49500–54000):** The envelope whooshes off-screen (a "sent" arc), a little motion trail.
- **Beat 8 · daumen (54000–60000):** Handwerker gives a big thumbs up, full grin. Then the `EndCard` fades in over the top (~57000).

## EndCard (fades in ~57000, same layout as reisemapper's)
- eyebrow (uppercase, teal): DE „FEIERABEND" / EN "CLOCKING OFF"
- title (Fraunces italic, large): **„Bauen an der Schwelle"** (same brand line as the reisemapper film — keep it identical across the set)
- sub (bold sans): DE „Bau dir deinen KI-Begleiter." / EN "Build your own AI companion."
- pill CTA (ink bg, card text): **stepintomore.co**

## Routes — copy the reisemapper route meta pattern
- `/rechnung`: title "Rechnung-Übersetzer — Bauen an der Schwelle · Stumme Animation", `robots: noindex`, og `video.other`. Description: eine Handwerker-Notiz wird in ~60 Sekunden zur fertigen § 14 UStG Rechnung — jede Zahl mit Quelle, nichts erfunden.
- `/rechnung-en`: English equivalents.

## Voice / house rules
- Silent film. No audio. It must read cleanly with the sound off.
- Same warm, first-person, slightly dry caption voice as reisemapper. **No em-dashes or en-dashes as punctuation in the captions** (commas, periods, or restructure). German compound hyphens like „KI-Begleiter" are fine.
- The whole point of the tool is that it invents nothing: the „erfindet nichts / invents nothing" drop of the Kaffeemaschine line is the emotional payoff, don't cut it.
- Keep it a clean loop: the last frame should sit comfortably before it snaps back to beat 1.
