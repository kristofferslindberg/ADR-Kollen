#!/usr/bin/env python3
"""Bygger ADR-kollen.

- Läser ../adr_tabell_a.csv och bäddar in en kompakt UN-tabell i src/app.html  -> index.html
  (index.html är sidan som publiceras som Artifact, utan <html>/<head>).
- Skriver pwa/index.html: samma sida som fristående installerbar webbapp (manifest + service worker).

    python3 build.py
"""
import csv, json, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
TABLE = HERE / "data" / "adr_tabell_a.csv"
STATUS = {"RAKNAS": "R", "KATEGORI_0_INGET_UNDANTAG": "0", "TRANSPORT_FORBJUDEN": "F",
          "OMFATTAS_EJ_AV_ADR": "E", "INGEN_TRANSPORTKATEGORI": "N"}


def compact_table():
    out = {}
    with open(TABLE, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            out.setdefault(r["un_number"], []).append(
                [r["transport_category"], r["pg_hint"], STATUS[r["status"]], r["adr_class"], r["name_en"],
                 r["labels"], r["tunnel_code"], r["classification_code"]])
    return json.dumps(out, ensure_ascii=False, separators=(",", ":"))


def main():
    src = (HERE / "src" / "app.html").read_text()
    page = src.replace("/*__UN_TABLE__*/{}", compact_table())
    (HERE / "index.html").write_text(page)

    pwa = HERE / "docs"
    pwa.mkdir(exist_ok=True)
    head = ('<!doctype html><html lang="sv"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#F28C00">'
            '<link rel="apple-touch-icon" href="icon.svg"><meta name="apple-mobile-web-app-capable" content="yes">'
            '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
            'body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style></head><body>')
    tail = ("<script>if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js')</script>"
            "</body></html>")
    (pwa / "index.html").write_text(head + page + tail)
    for d in ("vendor", "exempel"):
        shutil.copytree(HERE / d, pwa / d, dirs_exist_ok=True)
    print("index.html", len(page) // 1024, "KB; pwa/ klar")


if __name__ == "__main__":
    main()
