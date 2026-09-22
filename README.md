# Rechnung Translator

A folder-based AI translator. It takes **one repair job's raw record** (hours, receipts described in text, travel, tagged to a contract) and returns **one § 14 UStG-compliant German invoice (Rechnung)**, with the same shape every time and **nothing invented**.

Not a summarizer. Not a writer. A converter with a contract.

It is also a **learning system**. Because the folder is plain language, you and it converge on a shared format: when something is missing it asks a specific question instead of throwing an error, and you can edit any rule to fit how you actually work.

## Who does this by hand today

Every solo tradesperson and small maintenance operator in Germany. They spend an evening a week turning a notebook page and a shoebox of receipts into an invoice that has to be *exactly right*, because a wrong or missing field means the customer cannot claim the Vorsteuer and sends it back. The conversion is mechanical, hated, and never automated because the last tool that tried it made numbers up.

## What it guarantees

1. **Fixed shape.** Same sections, same order, every run, however messy the input. A field with no source is printed as `nicht in Quelle`, never dropped.
2. **Nothing invented.** Every number, name, and date in the invoice traces to a line in the input, to a declared constant in `reference/`, or to an arithmetic whose formula is shown. If the translator cannot find it, the field says so. It never estimates a distance from "drove there" or rounds an hour nobody wrote down.
3. **Nothing dropped.** Anything in the input it could not place is listed under `Nicht abgebildet`, not silently omitted.

Every invoice ends with a **Quellennachweis**: one row per output value, tagged with where it came from. A reader can open the input and check every line. Cartographers cite the line, auditors cite the rule, this one cites the source.

## How to use it

1. Drop this folder into a Claude project.
2. Feed it a job record shaped like [`input/beispiel-job-musterstadt.md`](input/beispiel-job-musterstadt.md). Receipts can be **described in text**, or dropped in as **photos / scans** in `input/belege/`. The translator reads the image directly and refuses to guess an unreadable digit (see [`reference/beleg-lesen.md`](reference/beleg-lesen.md)).
3. Get back a finished Rechnung plus its Quellennachweis. It lands in `output/`.

The instruction to Claude: *"You are the translator defined by `identity.md` and `rules.md`. Convert the job record I give you into a Rechnung. Follow the contract exactly."*

## What it refuses

One invoice shape only: **standard domestic, full service, 19 % USt.** If the input implies an Abschlags-/Schlussrechnung, a foreign customer, or reverse charge, the translator **refuses and says why** (see [`reference/out-of-scope.md`](reference/out-of-scope.md)). It does not branch into a second shape. One shape every time is the whole point.

## Structure

```
identity.md        what it converts, from what, to what
rules.md           the mapping: input part to invoice field, provenance, gaps, refusals
examples.md        three input/output pairs showing the contract hold, break gracefully, and refuse
reference/         the contract this folder promises to keep
  schema.md          the fixed invoice shape + the § 14 UStG field definitions
  stammdaten.md      the issuer's identity (pseudonymized)
  pricing.md         default rates: labor, helper, travel, material markup, VAT
  out-of-scope.md    what the translator refuses and why
  team/              one file per worker; the billable rate lives here, the wage stays internal
  contracts/         one file per job; parties, agreed rates, payment terms
  beleg-lesen.md     how to read a receipt photo/scan without inventing a digit
input/             a real sample job record you can run
  belege/            receipt photos/scans; read directly, not transcribed
output/            where finished invoices land
```

## Roadmap

This is v1, and it does one thing well: a domestic 19 % repair invoice from a job record. It is built to grow, because real use always exceeds the first use case.

- **Now:** one invoice shape; text or photo receipts; any input language into a German invoice; a dialogue when a field is missing.
- **Next:** more workers on file; per-job routing (one record, many buildings); the Abschlags-/Schlussrechnung shape; more Bundesländer conventions.
- **Always:** whatever people feed it that we did not predict. Affordances beat specifications. The contract (nothing invented, everything traced) does not change as the shapes multiply.

## Note on the data

All identities, addresses, tax numbers, bank details, and the Wohnbaugenossenschaft Musterstadt eG are **fictional**. The folder is the method; real invoices run against a private `reference/` that never ships. Nothing here is a real person, a real company, or a real bank account.

MIT-licensed method (ICM, Van Clief & McDermott, arXiv:2603.16021).
