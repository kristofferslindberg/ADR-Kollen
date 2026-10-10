# ADR-kollen (mobilapp)

Webbapp för chaufförer, **bara väg (ADR) och järnväg (RID)**. Flygdokument (IATA) och ID-nummer ger rött.
Val Väg/Järnväg överst: på järnväg finns inget poängundantag, så där visas listan utan poäng och "Full RID gäller".

 fota fraktsedeln (eller välj PDF/bild, eller skriv in själv) och få
**OK att köra** (grön) eller **Får inte köras utan full ADR** (röd) plus uträknad lista enligt ADR 1.1.3.6.

Demo (Artifact): https://claude.ai/artifact/XQPQ5Hw8xPBMuUx9VGJKyV

## Allt körs i telefonen
- OCR: Tesseract.js 6 (WebAssembly) med svenska + engelska språkdata, i `vendor/tess/`. Ingen server, inget skickas iväg.
- PDF med textlager läses exakt med pdf.js (`vendor/`); skannade PDF:er går via OCR.
- UN-tabellen (../adr_tabell_a.csv) bäddas in i sidan vid bygget.
- Logiken är en JS-port av ../reader/reader.py (fritextläget + beräkningen). Stopp: summa > 1000, kategori 0,
  transport förbjuden, okänt UN-nummer, oläslig mängd. Saknas förpackningsgrupp används strängaste kategorin.

## Filer
- `src/app.html` källkod, `data/adr_tabell_a.csv` UN-tabellen.
- `python3 build.py` bygger `docs/`: den installerbara appen (manifest + service worker, fungerar utan täckning efter första start).
- `docs/` publiceras med GitHub Pages (Settings > Pages > Deploy from branch > main /docs). Öppna adressen på telefonen och välj "Lägg till på hemskärmen".

## Testat (Chromium, telefonbredd)
- godsdeklaration_adr_exempel.pdf: 2 600 poäng, röd (stämmer med dokumentet).
- adr_syntetisk.png (OCR): 1 800 poäng, röd, alla tre rader rätt.
- En IATA-flygblankett känns igen som flygdokument och ger rött (exemplet är borttaget ur appen).
