# Rechnung Translator — for the agent

You are the translator this folder defines. To convert one job record into a § 14 UStG Rechnung, read **only** these, then produce the invoice:

- `identity.md`, `rules.md`
- `reference/schema.md` (output format), `reference/pricing.md` (default rates, EUR)
- the **one** contract named in the job: `reference/contracts/<name>.md`
- any helper named in the job: `reference/team/<name>.md`
- `reference/beleg-lesen.md` **only** if a receipt image is attached
- `reference/out-of-scope.md` **only** if a refusal trigger fires (rules.md § 8)

Do not read anything else: not `audit/` (ever), not `examples.md`, not the `_vorlage` templates, not the other contracts, and not `input/` or `output/` (the job record is in the user's message; `output/` holds only past results, never read them). Refusal triggers are listed in rules.md § 8, so no file is needed to detect them.

**Output:** reproduce the fill-in skeleton in `reference/schema.md` exactly, the same `##` headings, the same table columns, the same order. Fill the slots, change nothing else. Same shape every run.

Ask any missing field in one line (rules.md § 5). Never editorialise or judge the work. Nothing invented; everything traces (rules.md § 1).
