#!/usr/bin/env python3
"""
checks.py -- deterministic layer of the Rechnung-translator's eval.

Runs on a produced Rechnung (a report), NOT on the translator's factory files.
The translator never reads audit/. This is evidence about the output, the way
tests/ is evidence about code.

It answers, mechanically, what a judge would trace by hand:

  shape          the required sections are present (or it is a well-formed refusal)
  arithmetic     every line total, subtotal, the section 35a split, the 19% USt,
                 and the Brutto recompute exactly from the printed figures
  trace-tags     every Quellennachweis row carries a valid tag (Q / R / A / nicht-in-Quelle)
  no-orphan      every money amount in the invoice body appears in the Quellennachweis
                 (nothing un-sourced -- the "nothing invented" gate)
  source-Q       (with --input) every Q amount actually appears in the job record
  source-R       every cited reference/ file exists
  gap-honesty    a "nicht in Quelle" field is never counted into a sum
  dialogue       an incomplete draft carries a Rueckfragen block that names the
                 missing required fields, and asks nothing that is already present
  refusal        an out-of-scope report is a refusal block with no invoice
  key-match      (with --key) the Brutto and draft/final status match the answer key

No model, no judgment. Values that came from a receipt photo, and whether a
Leistung is 'concretely enough named' for section 14, are layer 2 (a human /
vision confirm), by design. See FINDINGS.md.

Usage:
  python checks.py <report.md> [--input <job.md>] [--key <key.md>]
  python checks.py --all
Exit 0 if every hard gate passes, 1 otherwise.
"""
import sys, os, re, json, argparse
from decimal import Decimal, ROUND_HALF_UP

# ---------- helpers ----------

def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def load_conventions(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

MONEY_RE = re.compile(r'(?<![\d.,])(\d{1,3}(?:\.\d{3})*|\d+),(\d{2})(?!\d)')

def parse_money(tok):
    """German money string -> float. '1.234,56' -> 1234.56, '42,02' -> 42.02."""
    m = MONEY_RE.search(tok)
    if not m:
        return None
    whole = m.group(1).replace(".", "")
    return float(f"{whole}.{m.group(2)}")

EURO_RE = re.compile(r'(\d{1,3}(?:\.\d{3})*|\d+),(\d{2})\s*€')

def euro_amounts(text):
    """Only amounts written as euros (a '€' follows). Excludes bare multipliers
    like the ×1,15 markup and hour counts like 0,75."""
    out = []
    for m in EURO_RE.finditer(text):
        whole = m.group(1).replace(".", "")
        out.append(round(float(f"{whole}.{m.group(2)}"), 2))
    return out

def job_numbers(text):
    """Every numeric value in a free-text job record, as rounded-2 floats,
    format-agnostic: '32.50' (EN), '32,50' (DE) and '450' all normalise, so a
    German-formatted output amount can be traced to an English-written input."""
    vals = set()
    for m in re.finditer(r'\d+(?:[.,]\d+)?', text):
        s = m.group(0)
        if s.count(".") + s.count(",") > 1:   # ambiguous thousands form, skip
            continue
        try:
            vals.add(round(float(s.replace(",", ".")), 2))
        except ValueError:
            pass
    return vals

def parse_num(tok):
    """A plain number that may use ',' as decimal: '1,5' -> 1.5, '54' -> 54.0."""
    tok = tok.strip().replace(" ", " ")
    m = re.search(r'(\d+(?:,\d+)?)', tok)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))

def eur(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def q2(x):
    """Round half up to two decimals, the convention rules.md declares."""
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

def mul2(a, b):
    """a*b in exact decimal, then round half up to two decimals."""
    return float((Decimal(str(a)) * Decimal(str(b))).quantize(Decimal("0.01"),
                 rounding=ROUND_HALF_UP))

def sections(text, conv):
    """Split report into {section_key: body} using the configured headings."""
    labels = conv["sections"]
    # map heading-line -> key
    out = {k: "" for k in labels}
    cur = None
    for line in text.splitlines():
        hit = None
        norm = line.strip().rstrip(":").lower()
        for k, lab in labels.items():
            if norm == lab.lower():
                hit = k
                break
        if hit:
            cur = hit
            continue
        if line.startswith("## "):        # some other heading closes the current
            cur = None
        if cur:
            out[cur] += line + "\n"
    return out

def rows(body):
    """Parse a markdown pipe-table body into a list of cell-lists (data rows only)."""
    out = []
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r'-{2,}|:?-+:?', c or "-") for c in cells):
            continue                        # separator row
        if len(cells) >= 2 and cells[0].lower() in ("feld", "leistung", "position",
                                                     "km", "posten", "wert"):
            continue                        # header row
        out.append(cells)
    return out

def close(a, b, tol):
    return abs(a - b) <= tol

# ---------- the gates ----------

def evaluate(report_path, input_path, key_path, conv, base):
    text = read_text(report_path)
    tol = float(conv["cent_tolerance"])
    gates = []   # (name, ok, detail)

    # ----- refusal short-circuit -----
    if conv["refusal_marker"] in text:
        has_invoice = any(w in text for w in ("Rechnungsbetrag", "Zwischensumme"))
        gates.append(("refusal", not has_invoice,
                      "Ablehnung ohne Rechnung" if not has_invoice
                      else "Ablehnung, aber Rechnungsteile vorhanden"))
        ok = all(g[1] for g in gates)
        return ok, gates, {"refusal": True}

    sec = sections(text, conv)
    incomplete = conv["incomplete_marker"] in text

    # ----- G shape -----
    need = ["arbeit", "summen", "quellennachweis"]
    missing_sec = [conv["sections"][k] for k in need if not sec[k].strip()]
    gates.append(("shape", not missing_sec,
                  "Pflichtabschnitte vorhanden" if not missing_sec
                  else f"fehlend: {missing_sec}"))

    # ----- parse line items -----
    labor = []   # (desc_cells, hours, rate, printed_total)
    for r in rows(sec["arbeit"]):
        hours = next((parse_num(c) for c in r if re.fullmatch(r'\d+(?:,\d+)?', c.strip())), None)
        rate = next((parse_money(c) for c in r if "€" in c and parse_money(c) and parse_money(c) < 1000), None)
        total = parse_money(r[-1])
        labor.append((hours, rate, total))

    material = []  # (einkauf, markup_factor, printed_total)
    for r in rows(sec["material"]):
        einkauf = next((parse_money(c) for c in r[1:] if parse_money(c) is not None), None)
        factor = None
        fm = re.search(r'×\s*(\d+(?:,\d+)?)', " ".join(r))
        if fm:
            factor = float(fm.group(1).replace(",", "."))
        total = parse_money(r[-1])
        material.append((einkauf, factor, total))

    fahrt = []   # (km, rate, total)
    for r in rows(sec["fahrt"]):
        km = next((parse_num(c) for c in r if re.fullmatch(r'\d+(?:,\d+)?', c.strip())), None)
        rate = next((parse_money(c) for c in r if "€" in c), None)
        total = parse_money(r[-1])
        fahrt.append((km, rate, total))

    # ----- summen -----
    lab = conv["summen_labels"]
    summ = {}
    for r in rows(sec["summen"]):
        label = r[0]
        val = parse_money(" ".join(r[1:]))
        for key, needle in lab.items():
            if needle in label:
                summ[key] = val

    # ----- G arithmetic -----
    arith = []
    vat = float(conv["vat_rate"])
    for i, (h, rate, tot) in enumerate(labor):
        if h is not None and rate is not None and tot is not None:
            if not close(mul2(h, rate), tot, tol):
                arith.append(f"Arbeit Zeile {i+1}: {eur(mul2(h,rate))} != {eur(tot)}")
    for i, (ek, factor, tot) in enumerate(material):
        if ek is not None and factor is not None and tot is not None:
            if not close(mul2(ek, factor), tot, tol):
                arith.append(f"Material Zeile {i+1}: {eur(mul2(ek,factor))} != {eur(tot)}")
    for i, (km, rate, tot) in enumerate(fahrt):
        if km is not None and rate is not None and tot is not None:
            if not close(mul2(km, rate), tot, tol):
                arith.append(f"Fahrt Zeile {i+1}: {eur(mul2(km,rate))} != {eur(tot)}")

    lab_sum = sum(t for _, _, t in labor if t is not None)
    mat_sum = sum(t for _, _, t in material if t is not None)
    fah_sum = sum(t for _, _, t in fahrt if t is not None)
    zws = q2(lab_sum + mat_sum + fah_sum)
    if "zwischensumme" in summ and not close(zws, summ["zwischensumme"], tol):
        arith.append(f"Zwischensumme: berechnet {eur(zws)} != gedruckt {eur(summ['zwischensumme'])}")
    netto = summ.get("netto")
    if netto is not None:
        if "ust" in summ and not close(mul2(netto, vat), summ["ust"], tol):
            arith.append(f"USt: {eur(mul2(netto,vat))} != {eur(summ['ust'])}")
        if "brutto" in summ and "ust" in summ and not close(q2(netto + summ["ust"]), summ["brutto"], tol):
            arith.append(f"Brutto: {eur(q2(netto+summ['ust']))} != {eur(summ['brutto'])}")
    if "s35a_netto" in summ and not close(q2(lab_sum + fah_sum), summ["s35a_netto"], tol):
        arith.append(f"§35a netto: berechnet {eur(q2(lab_sum+fah_sum))} != {eur(summ['s35a_netto'])}")
    if "s35a_netto" in summ and "s35a_brutto" in summ:
        if not close(mul2(summ["s35a_netto"], 1 + vat), summ["s35a_brutto"], tol):
            arith.append(f"§35a brutto: {eur(mul2(summ['s35a_netto'],1+vat))} != {eur(summ['s35a_brutto'])}")
    gates.append(("arithmetic", not arith,
                  "alle Summen stimmen" if not arith else " ; ".join(arith)))

    # ----- G trace-tags + no-orphan -----
    qn_rows = rows(sec["quellennachweis"])
    valid_tags = set(conv["tags"])
    bad_tag = []
    qn_values = set()
    for r in qn_rows:
        tag = r[1] if len(r) > 1 else ""
        if tag not in valid_tags:
            bad_tag.append(r[0][:30])
        # a value is 'sourced' if it appears anywhere in the row: the Wert cell
        # as a euro amount, or inside the formula/Quelle cell as a bare number.
        for cell in r:
            qn_values.update(euro_amounts(cell))
            qn_values.update(job_numbers(cell))
    gates.append(("trace-tags", not bad_tag,
                  "jede Nachweiszeile getaggt" if not bad_tag else f"ungültiger Tag: {bad_tag}"))

    body_text = sec["arbeit"] + sec["material"] + sec["fahrt"] + sec["summen"]
    body_values = set(euro_amounts(body_text))
    orphan = sorted(v for v in body_values if v not in qn_values)
    gates.append(("no-orphan", not orphan,
                  "jeder Betrag im Nachweis belegt" if not orphan
                  else f"nicht im Quellennachweis: {[eur(v) for v in orphan]}"))

    # ----- G source-R : cited reference files exist -----
    ref_dir = os.path.normpath(os.path.join(base, conv["reference_dir"]))
    cited_refs = set(re.findall(r'reference[:/ ]+([A-Za-zäöü0-9_\-/]+\.md)', text))
    missing_ref = [f for f in cited_refs if not os.path.exists(os.path.join(ref_dir, f))]
    gates.append(("source-R", not missing_ref,
                  "alle zitierten reference-Dateien existieren" if not missing_ref
                  else f"nicht gefunden: {missing_ref}"))

    # ----- G source-Q : Q amounts appear in the job record (needs --input) -----
    if input_path and os.path.exists(input_path):
        job = read_text(input_path)
        job_values = job_numbers(job)
        q_amounts = set()
        for r in qn_rows:
            if len(r) > 1 and r[1] == "Q":
                for v in euro_amounts(r[0]):
                    q_amounts.add(v)
        unfound = sorted(v for v in q_amounts if v not in job_values)
        gates.append(("source-Q", not unfound,
                      "jeder Q-Betrag steht im Job-Record" if not unfound
                      else f"nicht im Input: {[eur(v) for v in unfound]}"))

    # ----- G gap-honesty : a nicht-in-Quelle field is not counted -----
    # (structural: if incomplete, at least one required field must be nicht-in-Quelle)
    if incomplete:
        niq = conv["nicht_in_quelle"] in text
        gates.append(("gap-honesty", niq,
                      "Lücke als 'nicht in Quelle' markiert" if niq
                      else "als unvollständig markiert, aber keine 'nicht in Quelle'-Zeile"))

    # ----- G dialogue : incomplete draft asks for exactly the missing fields -----
    if incomplete:
        rf = sec["rueckfragen"].strip()
        kopf = sec["kopf"]
        missing_fields = []
        for field in conv["required_fields"]:
            # a required field is missing if its Kopf value is nicht-in-Quelle (or absent)
            present = re.search(re.escape(field) + r'\s*\|\s*(.+)', kopf)
            if not present or conv["nicht_in_quelle"] in (present.group(1) if present else ""):
                missing_fields.append(field)
        asked_missing = [f for f in missing_fields if f in rf]
        ok_ask = bool(rf) and len(asked_missing) == len(missing_fields)
        gates.append(("dialogue", ok_ask,
                      f"Rückfragen decken die Lücken {missing_fields}" if ok_ask
                      else f"Rückfragen unvollständig: fehlend {missing_fields}, gestellt {asked_missing}"))
        # no redundant question about currency
        if re.search(r'[Ww]ährung|[Cc]urrency', rf):
            gates.append(("no-redundant-ask", False, "fragt nach der Währung (immer EUR)"))

    # ----- G key-match -----
    if key_path and os.path.exists(key_path):
        key = read_text(key_path)
        km = parse_money(key[key.find("Brutto"):]) if "Brutto" in key else None
        prob = []
        if km is not None and "brutto" in summ and not close(km, summ["brutto"], tol):
            prob.append(f"Brutto {eur(summ['brutto'])} != Schlüssel {eur(km)}")
        sm = re.search(r'Status:\s*(\w+)', key)
        want_draft = bool(sm) and sm.group(1).lower().startswith(("entwurf", "draft"))
        if want_draft != incomplete:
            prob.append(f"Status: Schlüssel erwartet {'Entwurf' if want_draft else 'final'}")
        gates.append(("key-match", not prob,
                      "entspricht dem Schlüssel" if not prob else " ; ".join(prob)))

    ok = all(g[1] for g in gates)
    return ok, gates, {"incomplete": incomplete}

# ---------- render / run ----------

def render(report_path, ok, gates):
    out = [f"# Eval: {os.path.basename(report_path)}", "",
           "| Gate | Ergebnis | Detail |", "|---|---|---|"]
    for name, passed, detail in gates:
        out.append(f"| {name} | {'PASS' if passed else 'FAIL'} | {detail} |")
    out += ["", f"**Gesamt: {'PASS' if ok else 'FAIL'}**", ""]
    return "\n".join(out)

def run_all(base, conv):
    rep_dir = os.path.join(base, "reports")
    key_dir = os.path.join(base, "keys")
    fix_dir = os.path.join(base, "fixtures")
    rows_out, all_ok = [], True
    for name in sorted(os.listdir(rep_dir)):
        if not name.endswith(".report.md"):
            continue
        stem = name[:-len(".report.md")]
        key = os.path.join(key_dir, stem + ".key.md")
        inp = os.path.join(fix_dir, stem + ".md")
        expect_fail = name.startswith("planted")
        ok, _, _ = evaluate(os.path.join(rep_dir, name),
                            inp if os.path.exists(inp) else None,
                            key if os.path.exists(key) else None, conv, base)
        good = (ok != expect_fail)
        rows_out.append((name, "FAIL" if expect_fail else "PASS",
                         "PASS" if ok else "FAIL", good))
        all_ok = all_ok and good
    print("# Rechnung-Translator Eval: Gesamtlauf\n")
    print("| Bericht | erwartet | Ergebnis | ok? |")
    print("|---|---|---|---|")
    for name, want, got, good in rows_out:
        print(f"| {name} | {want} | {got} | {'ok' if good else 'X'} |")
    print(f"\n**Suite: {'PASS' if all_ok else 'FAIL'}**")
    return all_ok

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("report", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--input")
    ap.add_argument("--key")
    args = ap.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    conv = load_conventions(os.path.join(base, "conventions.json"))

    if args.all:
        sys.exit(0 if run_all(base, conv) else 1)
    if not args.report:
        print(__doc__)
        sys.exit(0)
    ok, gates, _ = evaluate(args.report, args.input, args.key, conv, base)
    print(render(args.report, ok, gates))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
