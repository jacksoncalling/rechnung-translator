#!/usr/bin/env python3
"""Render the fixed Rechnung Markdown form as one self-contained, printable HTML file.

The Markdown is an intermediate document. Keep only the HTML in output/.
No packages, network assets, or external fonts are required.
"""
import argparse
import base64
import html
import re
from pathlib import Path


ORDER = ["Kopf", "Arbeitsleistung", "Material", "Fahrtkosten", "Summen",
         "Zahlung", "Quellennachweis", "Nicht abgebildet", "Rückfragen"]


def table(lines):
    rows = []
    for line in lines:
        line = line.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        cells = [cell.strip() for cell in line[1:-1].split("|")]
        if all(re.fullmatch(r":?-{2,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return ""
    header, *body = rows
    head = "".join(f"<th scope='col'>{html.escape(cell)}</th>" for cell in header)
    data = "".join("<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>" for row in body)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{data}</tbody></table>"


def render(markdown):
    lines = markdown.replace("\r\n", "\n").strip().splitlines()
    if not lines or lines[0] not in ("# Rechnung (final)", "# Rechnung (Entwurf)"):
        raise ValueError("Input must start with the fixed Rechnung title")
    headings = [(i, line[3:]) for i, line in enumerate(lines) if line.startswith("## ")]
    names = [name for _, name in headings]
    expected = [name for name in ORDER if name in names]
    if names != expected or any(name not in ORDER for name in names):
        raise ValueError("Invoice sections do not follow the schema order")
    if any(name not in names for name in ("Kopf", "Arbeitsleistung", "Material", "Summen", "Zahlung", "Quellennachweis", "Nicht abgebildet")):
        raise ValueError("Invoice is missing a required section")
    sections = {}
    for index, (start, name) in enumerate(headings):
        end = headings[index + 1][0] if index + 1 < len(headings) else len(lines)
        sections[name] = lines[start + 1:end]
    intro = [line for line in lines[1:headings[0][0]] if line.strip()]
    draft = "Entwurf" in lines[0]
    note = next((line for line in intro if line.startswith("Entwurf unvollständig")), "")
    issuer = [line for line in intro if not line.startswith("Entwurf unvollständig")]
    if len(issuer) != 2:
        raise ValueError("Invoice must have two issuer lines")
    status = "Entwurf" if draft else "Rechnung"
    main_sections = []
    for name in names:
        if name in ("Quellennachweis", "Nicht abgebildet", "Rückfragen"):
            continue
        content = table(sections[name])
        if name == "Zahlung":
            footer = [line.strip() for line in sections[name] if line.strip() and not line.strip().startswith("|")]
            content += "".join(f"<p class='footer-line'>{html.escape(line)}</p>" for line in footer)
        main_sections.append(f"<section><h2>{html.escape(name)}</h2>{content}</section>")
    bullets = lambda name: "".join(f"<li>{html.escape(line.lstrip('- ').strip())}</li>" for line in sections.get(name, []) if line.strip().startswith("- "))
    questions = bullets("Rückfragen")
    unmapped = bullets("Nicht abgebildet")
    source_table = table(sections["Quellennachweis"])
    encoded = base64.b64encode(markdown.encode("utf-8")).decode("ascii")
    note_html = f"<div class='notice'>{html.escape(note)}</div>" if note else ""
    questions_html = f"<section class='questions'><h2>Rückfragen</h2><ul>{questions}</ul></section>" if questions else ""
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{status}</title><style>
:root{{--ink:#1e2935;--muted:#64717c;--rule:#d9e0e5;--accent:#17646a;--paper:#fff;--bg:#eef2f3}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}}
.toolbar{{max-width:920px;margin:22px auto 0;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:0 16px}}
button{{border:0;border-radius:6px;padding:9px 15px;background:var(--accent);color:#fff;font:inherit;cursor:pointer}}
.sheet{{max-width:920px;margin:16px auto 40px;background:var(--paper);padding:52px 58px;box-shadow:0 10px 35px #263e4818}}
h1{{font-size:28px;letter-spacing:.02em;margin:0 0 18px}}h2{{font-size:15px;text-transform:uppercase;letter-spacing:.09em;color:var(--accent);margin:32px 0 10px}}
.issuer{{color:var(--muted);margin-bottom:30px}}.issuer div:first-child{{font-weight:650;color:var(--ink)}}
.notice{{border-left:4px solid #be7b1b;background:#fff7e8;padding:12px 16px;margin:20px 0}}.questions{{border:1px solid #e8c993;background:#fffaf0;padding:0 18px 14px}}
table{{border-collapse:collapse;width:100%;font-size:14px}}th{{color:var(--muted);font-weight:600;text-align:left;border-bottom:2px solid var(--rule)}}td{{border-bottom:1px solid var(--rule);vertical-align:top}}th,td{{padding:8px 10px 8px 0}}td:last-child,th:last-child{{text-align:right}}.footer-line{{margin:8px 0}}
details{{margin-top:34px;border-top:2px solid var(--rule);padding-top:14px}}summary{{cursor:pointer;color:var(--accent);font-weight:650}}details table{{margin-top:16px}}ul{{padding-left:20px}}.small{{color:var(--muted);font-size:13px}}
@media print{{@page{{size:A4;margin:16mm}}body{{background:#fff;font-size:11pt}}.toolbar,details,.questions{{display:none!important}}.sheet{{max-width:none;margin:0;padding:0;box-shadow:none}}h2{{break-after:avoid}}tr{{break-inside:avoid}}table{{font-size:9pt}}th,td{{padding:5px 7px 5px 0}}}}
</style></head><body>
<div class="toolbar"><span class="small">{status} · Quellen im selben Dokument</span><button type="button" onclick="window.print()">Drucken / als PDF speichern</button></div>
<main class="sheet"><h1>{status}</h1>{note_html}<div class="issuer"><div>{html.escape(issuer[0])}</div><div>{html.escape(issuer[1])}</div></div>
{''.join(main_sections)}
{questions_html}
<details><summary>Quellennachweis und nicht abgebildete Angaben anzeigen</summary><h2>Quellennachweis</h2>{source_table}<h2>Nicht abgebildet</h2><ul>{unmapped}</ul></details>
</main><script id="audit-source" type="text/plain">{encoded}</script></body></html>
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Temporary Markdown invoice")
    parser.add_argument("destination", type=Path, help="Final HTML invoice")
    args = parser.parse_args()
    args.destination.write_text(render(args.source.read_text(encoding="utf-8")), encoding="utf-8")


if __name__ == "__main__":
    main()
