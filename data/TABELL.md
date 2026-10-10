# ADR Tabell A: UN-nummer, transportkategori och multiplikator

Filer: `adr_tabell_a.csv` (semikolonseparerad, UTF-8, öppnas direkt i Excel) och `adr_tabell_a.json` (samma rader plus metadata).
2 940 rader, 2 344 unika UN-nummer.

## Källa och utgåva
- Bas: ADR 2019, Tabell A (kapitel 3.2), UNECE. Hämtad via det öppna datasetet i Odoo-modulen
  `l10n_eu_product_adr` (OCA, AGPL), som i sin tur är konverterad från CEPA:s Excelversion av Tabell A 2019.
- Tillägg: UN 3549 till 3560, som kommit till i ADR 2021, 2023 och 2025. Värdena är kontrollerade mot
  freightutils.com (ADR 2025-data), utom fyra nummer som är markerade `verified = nej`.
- Gällande utgåva är ADR 2025. Ändringar av transportkategori för *befintliga* UN-nummer mellan 2019 och 2025
  är inte inlagda. De bör stämmas av mot UNECE:s officiella Tabell A 2025 innan programmet används skarpt.

## Kolumner
| Kolumn | Betydelse |
|---|---|
| un_number | UN-nummer, 4 siffror |
| variant / variant_count | Radnummer inom samma UN-nummer (flera rader = olika förpackningsgrupp eller variant) |
| name_en | Officiell engelsk benämning |
| adr_class / classification_code | Klass och klassificeringskod |
| transport_category | 0–4 (tom om ingen kategori) |
| multiplier | 1.1.3.6.4: kat 1 = 50, kat 2 = 3, kat 3 = 1, kat 4 = 0, kat 0 = tom (inget undantag) |
| status | RAKNAS, KATEGORI_0_INGET_UNDANTAG, TRANSPORT_FORBJUDEN, OMFATTAS_EJ_AV_ADR, INGEN_TRANSPORTKATEGORI |
| needs_packing_group | `ja` om raderna för UN-numret har olika kategorier, då måste förpackningsgruppen läsas av på fraktsedeln |
| pg_hint | Förpackningsgrupp (I/II/III) som raden motsvarar, bara där den behövs. Härledd ur klass, transportkategori och LQ. Obs: klass 6.1 förpackningsgrupp III har kategori 2, inte 3 |
| select_by | Hur rätt rad väljs när UN-numret har flera kategorier: `forpackningsgrupp`, `etiketter` (aerosoler UN 1950 och gaspatroner UN 2037, t.ex. 2.1 = brandfarlig = kat 2) eller `forpackningsgrupp+benamning` (UN 2215, SMÄLT = kat 0) |
| tunnel_code | Tunnelrestriktionskod |
| labels | Etiketter |
| limited_quantity | Begränsad mängd (LQ) per innerförpackning |
| source / verified | Varifrån raden kommer och om värdet är kontrollerat |

## Regel för beräkningen (1.1.3.6)
Summa = mängd kat 1 × 50 + mängd kat 2 × 3 + mängd kat 3 × 1 (kat 4 räknas 0).
Över 1 000 eller någon rad med kategori 0 eller TRANSPORT_FORBJUDEN betyder att undantaget inte gäller.
Mängd är nettomassa (kg) för fasta ämnen, liter för vätskor, nominell volym för gasbehållare och bruttomassa för föremål.

## Ändringslogg
- 2026-10-10: Kontroll av alla rader mot källan och mot reglerna i 1.1.3.6.3: inga fel i transportkategori eller multiplikator. Rättat `pg_hint` för 86 rader i klass 6.1 (förpackningsgrupp III stod som II) och 4 rader i klass 4.2. Ny kolumn `select_by`.

## Kända luckor
- UN 3553, 3554, 3556 och 3557 kunde inte kontrolleras (källsidan begränsade antalet anrop). Värdena är angivna efter bästa kunskap.
- Förpackningsgrupp finns inte i källdatat, därför är `pg_hint` härledd.
- Svenska benämningar saknas.
