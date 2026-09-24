# Rules

How the translator maps a job record to a Rechnung. This is the contract. When in doubt, this file wins.

---

## 0. Run flow — read only what the conversion needs

To convert one job record, read exactly these, then produce the invoice:

- `identity.md` and `rules.md` (this file)
- `reference/schema.md` (the output format)
- `reference/stammdaten.md` (issuer identity and payment details)
- `reference/pricing.md` (default rates, EUR)
- the **one** contract named in the job: `reference/contracts/<name>.md` (not the others)
- any helper named in the job: `reference/team/<name>.md` (only those)
- `reference/beleg-lesen.md` **only** if a receipt image is attached
- `reference/out-of-scope.md` **only** if a refusal trigger fires (§ 8)

The job record is supplied in the user's message. Do not read unrelated contracts or `_vorlage` templates. During a cold test, the test runner keeps `audit/`, answer keys, `examples.md`, and past `output/` results out of the agent's context. The refusal triggers are listed in § 8, so you do not need to open a file to detect them.

---

## 1. The provenance tags

Every single value that appears in the output carries exactly one origin. Nothing may appear without one.

| Tag | Meaning | What it cites |
|-----|---------|---------------|
| **Q** | Quelle. Taken from a line in the job record. | The input line it came from. |
| **R** | Referenz. A declared constant from `reference/`. | The file and field. |
| **A** | Arithmetik. Computed from Q and/or R values. | The formula, with the input values shown. |
| **∅** | Nicht in Quelle. A required field with no source. | Printed literally as `nicht in Quelle`. Never filled. |

If a value is not Q, R, or A, it does not go in the invoice. There is no fifth option called "reasonable guess." A guess is the one way to lose.

## 2. What the translator reads

**Working input (new every run):** one job record. It must be tagged to a contract (a name that matches a file in `reference/contracts/`). It may contain, in any order and any wording:
- a work log: dated entries, each naming what was done, the hours, and whose hours (owner or a named helper)
- materials: receipts described in text (vendor, item, amount, date)
- travel: kilometers or trips
- optionally a Rechnungsnummer and a Rechnungsdatum

**Reference (every run), pulled by the contract name:**
- `reference/stammdaten.md` — issuer identity, Steuernummer, IBAN
- `reference/pricing.md` — default rates and the VAT rate
- `reference/contracts/<job>.md` — customer, agreed rates, payment term, warranty; overrides pricing defaults
- `reference/team/<helper>.md` — a helper's **billable rate**

If the job names a contract that has no file, stop and say so. Do not invent a customer.

## 3. Field-by-field mapping

### Header
| Invoice field | Source | Rule |
|---|---|---|
| Issuer (name, address, Steuernummer) | R | `stammdaten.md`. |
| Recipient (name, Rechtsform, address) | R | `contracts/<job>.md`. Never from the job record. |
| Rechnungsnummer | Q or ∅ | From the job record. If absent, `nicht in Quelle` and flag it: a § 14 invoice needs one, assigned by the register. |
| Rechnungsdatum | Q or ∅ | From the job record. If absent, `nicht in Quelle`. Never today's date. Without it the invoice is marked incomplete. |
| Leistungszeitraum | A | Earliest to latest date in the work log: `min(dates) bis max(dates)`. If only one date, that date. |
| Bezug | R | The contract reference from `contracts/<job>.md`, if the contract names one. |

### Leistungen — labor
- One line per distinct activity, or grouped by worker, preserving the concrete description from the work log (§ 14 requires the *Art der Leistung* named concretely, not "Arbeit").
- Owner hours: sum of all owner hours in the log **(Q)** × Stundensatz from the contract, else pricing **(R)** = line total **(A)**.
- Helper hours: per named helper, sum of that helper's hours **(Q)** × that helper's billable rate from `team/<helper>.md`, else contract, else pricing **(R)** = line total **(A)**.
- If a named helper has **no `team/<name>.md` file**, apply the **default helper rate** from `pricing.md` (**R**), flag it, and add a Rückfrage offering to create the file so the worker is on record and can be paid: `David hat noch keine Datei. Ich rechne mit dem Standard-Helfersatz. Lege ich eine Datei an (Verrechnungssatz + interner Lohn)?` The internal wage is for your records and payroll only, never on the invoice.
- Never sum hours the log did not state. Never apply a rate not found in contract/pricing/team.

### Leistungen — material
- A receipt may be **described in text** in the job record, or **supplied as a photo / scan / PDF** in `input/belege/` (or attached). Either way the amount is **Q**. For an image the cited source is the file name; read it per `reference/beleg-lesen.md`.
- One line per receipt. Description and purchase amount are **Q**.
- Line net = purchase amount **(Q)** × (1 + Materialaufschlag **(R)**), shown as **(A)**: `Einkauf X,XX € × 1,NN = Y,YY €`.
- If a receipt's amount is not stated, not readable, or only partly legible, the line stays, the amount is `nicht in Quelle` / `nicht sicher lesbar`, and it is **excluded from every sum** and flagged. Never estimate a material cost, and never guess a smudged digit into a plausible one.
- If the text gives a purchase amount without saying whether it is net or gross, ask which it is before applying the markup. Keep the material line unresolved and exclude it from sums until answered.

### Leistungen — travel
- Add a travel line only for kilometers explicitly recorded for the job. Fahrtkosten = recorded km **(Q)** × €/km **(R, contract else pricing)** = **(A)**.
- Use the recorded distance exactly once. Do not double an `Anfahrt` value to assume a return journey, and do not add a trip to a supplier unless that trip and its kilometers are explicitly recorded. Never derive kilometers from an address or map.
- If the record says someone drove for this job but gives no kilometers, leave out the travel line, mark the distance `nicht in Quelle` in the Quellennachweis, and keep the invoice as an **Entwurf**. Ask one short question: `Fahrt: gefahrene Kilometer? (km) Oder nicht berechnen?` Do not ask for kilometers when no trip is mentioned.
- If the person supplies kilometers, calculate the travel line. If they confirm `nicht berechnen`, omit the travel line, record that decision under `Nicht abgebildet`, and finalize when no other gaps remain. Do not invent a zero-kilometer trip.

### Sums
| Field | Source | Rule |
|---|---|---|
| Zwischensumme netto | A | Sum of all labor, material, and travel line nets. |
| Nachlass | R or omitted | Only if the contract states an agreed reduction. Otherwise the line does not appear. |
| Nettobetrag | A | Zwischensumme minus Nachlass. |
| **davon Arbeits- und Fahrtkosten (§ 35a EStG)** | A | Labor + travel nets (material excluded by law), shown net and brutto. This line appears every run. |
| USt 19 % | A | Nettobetrag × VAT rate **(R)**, rounded to 2 decimals. |
| Rechnungsbetrag (brutto) | A | Nettobetrag + USt. |

### Payment
| Field | Source | Rule |
|---|---|---|
| Fälligkeit | A or ∅ | Rechnungsdatum **(Q)** + Zahlungsziel **(R, contract)**. If Rechnungsdatum is ∅, Fälligkeit is ∅. Never guess the date. |
| IBAN, Kontoinhaber | R | `stammdaten.md`. |
| Verwendungszweck | Q or ∅ | The Rechnungsnummer. |

### Footer
| Field | Source | Rule |
|---|---|---|
| Gewährleistung | R | The warranty clause from `contracts/<job>.md` (e.g. 2 Jahre ab Abnahme, § 634a BGB). |
| Steuernummer, IBAN | R | `stammdaten.md`. |

## 4. Rounding and format

- **Currency is always EUR.** An amount written with no symbol (e.g. `85.40`) is euros. Never ask which currency. All money comma decimal, two places, rounded half up (`48,323 → 48,32`; `147,775 → 147,78`).
- Round each material line **before** summing; the sum is of the rounded line nets.
- Hours as written in the log (`1,5`, `0,75`). Never round hours.

## 5. Gaps — ask, do not guess, do not dead-end

A missing field starts a short dialogue. It is not an error, and it is never a place to invent.

- Produce the **best faithful draft** from what is present, with every missing required field, unresolved billable amount, or mentioned trip with no distance/waiver shown as `nicht in Quelle` (or `nicht sicher lesbar`) and the header note `Entwurf unvollständig`. Do not label a partial sum as the final invoice amount.
- Then add a **Rückfragen** block. Each Rückfrage is **one line**: the field and the format needed, nothing more. No justification, no reasoning, no comment on the work. `Rechnungsnummer? (BR-JJJJ-NNN)` · `Rechnungsdatum? (TT.MM.JJJJ)` · `Welcher Vertrag/Kunde?`. The `nicht in Quelle` marker stays for traceability; the one-liner makes it actionable.
- **Ask only for missing data. Never editorialise.** The translator does not weigh in on whether the work fits the contract, whether an item should be billed, or anything else. That is judgment, and judgment is not its job. If a fact is missing, name it; do not argue about it.
- When the person answers, continue from the draft and finalize only when the required fields, billable amounts, and mentioned trips are resolved. A run may take more than one pass.
- **Never ask for what is already there or derivable.** Currency is always EUR, so it is never asked (§ 4). The Leistungszeitraum is derived from the work dates, not asked, when dates are present. A redundant question is itself a defect.

## 6. Nothing dropped — the `Nicht abgebildet` rule

Any line in the job record that carries no billable value (an aside, a "just looked at it, did nothing", a future request, an item you could not classify) is listed verbatim under a closing section **`Nicht abgebildet`**, with a one-line reason. A record that silently omits something the person wrote is a failure, even if there was nothing to bill.

## 7. The Quellennachweis (required, every run)

After the invoice, a table: one row per output value, columns `Wert | Tag (Q/R/A/∅) | Quelle`. For A rows, the Quelle column holds the formula with its input values. This is what makes every claim checkable. No invoice ships without it.

## 8. Refusals — one shape only

Before mapping, scan the job record. If it implies any of the following, **do not produce an invoice.** Return the refusal block from `reference/out-of-scope.md`, naming the trigger:
- an Abschlag, Anzahlung, Teilzahlung, or Schlussrechnung
- a customer outside Germany, an EU USt-IdNr. for reverse charge, or a Drittland
- a tax rate other than 19 % (e.g. 7 %, or Kleinunternehmer § 19)

The folder handles standard domestic full-service 19 % invoices. It refuses the rest openly rather than branching into a second shape.

## 9. The never-invent list

The translator must never put in the output:
- a date the input did not state (no today's date, no inferred Leistungsdatum beyond min/max of stated dates)
- a distance, quantity, or hour the input did not state
- a rate not found in contract, pricing, or the helper's file
- a customer detail not in the contract
- a material amount not on a described receipt
- a **helper's internal wage** — only the billable rate ever reaches the invoice; the wage in `team/<helper>.md` is internal and stays off every output
- a next step, a sentiment, a judgment, or a "usually" spelling of a name

One invented fact and the entry is out. If it is not in the source, the output says so.

## 10. Output order (the fixed shape)

1. Header note (only if incomplete)
2. Issuer block
3. Recipient block
4. Rechnungsnummer / Rechnungsdatum / Leistungszeitraum / Bezug
5. Leistungen: labor, then material, then travel
6. Sums: Zwischensumme, [Nachlass], Nettobetrag, davon Arbeits-/Fahrtkosten (§ 35a), USt 19 %, Rechnungsbetrag
7. Zahlung: Fälligkeit, IBAN, Verwendungszweck
8. Footer: Gewährleistung, Steuernummer, IBAN
9. **Quellennachweis**
10. **Nicht abgebildet**
11. **Rückfragen** — only when a required field, billable amount, or mentioned trip is unresolved, or a worker has no file yet

Same order every run. Items 1 and 11 appear only when there is something to say. On a complete input the invoice is final in one pass, with no Rückfragen.

**Reproduce the exact skeleton in `reference/schema.md` as a temporary intermediate**: the same `##` headings, table columns, and order. Render it with `python render_html.py <temporary.md> output/<unique-name>.html`. Save no Markdown invoice in `output/`; the one delivered file is HTML. **Where no shell exists** (a claude.ai Project, for example), the filled skeleton itself is the delivered invoice: return it in full and say the render was not possible. The schema is the contract; HTML is the preferred carrier, not the contract itself. Do not retype or recalculate the invoice in HTML. The renderer puts the Quellennachweis in a collapsible section and hides it when printing. Return only a short file link and the unresolved Rückfragen, if any, in chat. Use the invoice number in a final filename; use a distinct job identifier for a draft so a second draft on the same day cannot overwrite it. Two runs of the same job must keep the same data shape.
