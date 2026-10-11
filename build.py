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
                 r["labels"], r["tunnel_code"], r["classification_code"], r.get("select_by", "")])
    return json.dumps(out, ensure_ascii=False, separators=(",", ":"))


def main():
    src = (HERE / "src" / "app.html").read_text()
    import datetime
    version = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    page = src.replace("/*__UN_TABLE__*/{}", compact_table()).replace("__VERSION__", version)
    (HERE / "index.html").write_text(page)

    pwa = HERE / "docs"
    pwa.mkdir(exist_ok=True)
    splashes = "".join(
        f'<link rel="apple-touch-startup-image" href="icons/splash-{w}x{h}.png" media="(device-width: {round(w / r)}px) '
        f'and (device-height: {round(h / r)}px) and (-webkit-device-pixel-ratio: {r}) and (orientation: portrait)">'
        for w, h, r in [(1290, 2796, 3), (1179, 2556, 3), (1284, 2778, 3), (1170, 2532, 3), (1125, 2436, 3),
                        (1242, 2688, 3), (828, 1792, 2), (750, 1334, 2), (1080, 2340, 3)])
    head = ('<!doctype html><html lang="sv"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<link rel="manifest" href="manifest.webmanifest">'
            '<meta name="theme-color" content="#15191c">'
            '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
            '<meta name="apple-mobile-web-app-title" content="ADR-kollen"><meta name="format-detection" content="telephone=no">'
            '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">'
            '<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">' + splashes +
            '<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style></head><body>')
    tail = ("<script>if('serviceWorker' in navigator){let r=!navigator.serviceWorker.controller;"
            "navigator.serviceWorker.register('sw.js');"
            "navigator.serviceWorker.addEventListener('controllerchange',()=>{if(!r){r=1;location.reload()}})}</script>"
            "</body></html>")
    (pwa / "index.html").write_text(head + page + tail)
    for d in ("vendor", "exempel"):
        shutil.copytree(HERE / d, pwa / d, dirs_exist_ok=True)
    print("index.html", len(page) // 1024, "KB; pwa/ klar")


if __name__ == "__main__":
    main()
