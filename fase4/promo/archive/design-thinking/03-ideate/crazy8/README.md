# Crazy 8s · Hero- og Materialpass-skisser

Dato: 2026-11-17.
Ansvarlig: Antigravity (Oppgave A-4, PLAN §3.3).
Styrende dokumenter: [DESIGN-GUIDE.md](../../../../DESIGN-GUIDE.md), [canonical-house.md](../../../../canonical-house.md), og [shot-list.md](../../../../shot-list.md).

---

## 1. Hensikt

Crazy 8s er en rask idéutviklingsmetode for å utforske 8 distinkte layout- og strukturgrep for nettsidens to viktigste seksjoner: **Hero** (førsteinntrykk, tittel, bilde, «Følg prosjektet») og **Materialpass** (dokumentasjon av treverk, malmfuru, egenskaper og opprinnelse).

---

## 2. De 8 layoutvariantene

### Variant 1: «Horisonten» (Asymmetrisk 50/50 Split)
- **Konsept:** Klassisk redaksjonell balanse. Tekst til venstre med raus hvitflate (kalk), stort 3:2 fotografi til høyre med overhengende fjordbakgrunn.
- **Hero-oppbygning:**
```
+------------------------------------+------------------------------------+
|  MiniHouse                         |                                    |
|                                    |                                    |
|  Et lite hus,                      |       [ 3:2 Hovedbilde:            |
|  laget for å flyttes.              |         MiniHouse på skråning ]    |
|                                    |                                    |
|  Bygget for vestlandsklima...      |                                    |
|                                    |       Konseptbilde                 |
|  [ Følg prosjektet ]               |                                    |
+------------------------------------+------------------------------------+
```
- **Materialpass:** Horisontal eikefarget modulbånd med tette tabellrader side om side med en kvadratisk materialprøve.
- **Vurdering:** Trygg, ryddig, og direkte i tråd med DESIGN-GUIDE §8.3 desktop-layout.

---

### Variant 2: «Panoramataket» (Full-bleed 16:9 Hero med forankret tekstboks)
- **Konsept:** Landskapet overtar førsteinntrykket. Fullbredde fjordutsikt med huset i sentrum; en enkel kalkhvit tekstplate forankret i nedre venstre hjørne.
- **Hero-oppbygning:**
```
+-------------------------------------------------------------------------+
| [================== Fullbredde 16:9 Panoramabilde ====================] |
|                                                                         |
|  +------------------------------+                                       |
|  | MiniHouse                    |                                       |
|  | Et lite hus, laget for å flyttes. |                                  |
|  | [ Følg prosjektet ]          |                                       |
|  +------------------------------+                                       |
+-------------------------------------------------------------------------+
```
- **Materialpass:** Trestegs interaktiv fanevelger der brukeren klikker mellom Malmfuru, Eik, Kobber og Stål.
- **Vurdering:** Kraftfullt natursug, men kan skyve tekst og statusmerknad for langt ned på mindre skjermer.

---

### Variant 3: «Den redaksjonelle spalten» (Sentrisk ro og smal satsflate)
- **Konsept:** Inspirert av klassiske norske arkitekturtidsskrifter. Teksten innleder i en smal, rolig spalte (60–66 tegn), etterfulgt av et stort, uforstyrret fotografi.
- **Hero-oppbygning:**
```
+-------------------------------------------------------------------------+
|                                MiniHouse                                |
|                                                                         |
|                   Et lite hus, laget for å flyttes.                     |
|                Bygget for vestlandsklima med gjenbrukt tre              |
|                           [ Følg prosjektet ]                           |
|                                                                         |
|                +---------------------------------------+                |
|                |       [ Sentrert 3:2 fotografi ]      |                |
|                |       Konseptbilde                    |                |
|                +---------------------------------------+                |
+-------------------------------------------------------------------------+
```
- **Materialpass:** Vertikal leseliste formet som et offisielt dokument eller sertifikat.
- **Vurdering:** Gir høy verdighet og bokfølelse, men bryter delvis med venstrejusteringsregelen i DESIGN-GUIDE §8.3.

---

### Variant 4: «Håndverksbenken» (Materialet først)
- **Konsept:** Snur hierarkiet på hodet: Nærbildet av det værbitte treverket og årringene møter brukeren først, før huset avsløres som helhet.
- **Hero-oppbygning:**
```
+------------------------------------+------------------------------------+
|  [ Makrofoto: Tettvokst malmfuru ] |  MiniHouse                         |
|  Årringer, kjerneved, harpiks      |                                    |
|                                    |  Huset formes av treverket.        |
|  +------------------------------+  |  Et 6x3 m modulhus...              |
|  | [ Lite oversiktsbilde hus ]  |  |                                    |
|  +------------------------------+  |  [ Følg prosjektet ]               |
+------------------------------------+------------------------------------+
```
- **Materialpass:** Dominant seksjon som fyller hele skjermbredden med taktile materialprøver og historisk opprinnelse.
- **Vurdering:** Svært spennende for designentusiaster, men kan forvirre førstegangsbesøkende som først vil forstå hva MiniHouse er.

---

### Variant 5: «Mobilkaskaden» (Kompakt 360 px standard)
- **Konsept:** Optimalisert utelukkende for mobil vertikal scrolling. Hvert element har full bredde med 24 px marger.
- **Hero-oppbygning (360 px):**
```
+------------------------------+
| MiniHouse             Meny = |
|                              |
| Et lite hus,                 |
| laget for å flyttes.         |
|                              |
| +--------------------------+ |
| | [ 3:2 Hovedbilde ]       | |
| +--------------------------+ |
| Konseptbilde                 |
|                              |
| Bygget for vestlandsklima... |
|                              |
| [ Følg prosjektet ]          |
+------------------------------+
```
- **Materialpass:** Ett samlet kort med oppsummerte nøkkeldata, etterfulgt av en horisontal sveipbar stripe med fargeprøver.
- **Vurdering:** Essensiell referanse for mobilvisningen; direkte kompatibel med PLAN §8.3 mobilhero.

---

### Variant 6: «Gavlprofilen» (Arkitektonisk rammeverk)
- **Konsept:** Saltakets karakteristiske vinkel (symmetrisk gavl) speiles subtilt i layoutens grafiske delelinjer og modulinndeling.
- **Hero-oppbygning:**
```
+-------------------------------------------------------------------------+
| MiniHouse                                                  Følg prosjektet |
|                 /\                                                      |
|                /  \   Et lite hus, laget for å flyttes.                 |
|               /    \  6 x 3 meter saltaksmodul                          |
|  +-----------+------+------------------------------------------------+  |
|  | [ Hovedfoto av huset innrammet av tynne, sobre rammer ]          |  |
|  +-------------------------------------------------------------------+  |
+-------------------------------------------------------------------------+
```
- **Materialpass:** Oppdelt i tre vertikale pilarer: Råvare (Malmfuru), Bæring (Stål/Eik) og Detalj (Kobber).
- **Vurdering:** Tydelig arkitektonisk identitet, men risikerer å bli for dekorativ dersom takvinkelen overdrives grafisk.

---

### Variant 7: «Dokumentar-tabellen» (Teknisk loggbok)
- **Konsept:** Konstruert som en nøktern ingeniør- og arkitektloggbok. Målestokk, orientering og faktaboks følger heroen tett.
- **Hero-oppbygning:**
```
+------------------------------------+------------------------------------+
|  MiniHouse · Prosjektnotat         |  [ 3:2 Hovedbilde ]                |
|  Mål: 6000 x 3000 mm               |  Konseptbilde                      |
|                                    +------------------------------------+
|  Et lite hus, laget for å flyttes. |  STATUS: Under utvikling           |
|                                    |  KLEDNING: Gjenbrukt malmfuru      |
|  [ Følg prosjektet ]               |  TAK: Svart båndtekking            |
+------------------------------------+------------------------------------+
```
- **Materialpass:** Strukturert som en formell varedeklarasjon med tekniske kjennetegn og prøveresultater.
- **Vurdering:** Skaper umiddelbar teknisk tillit, men kan oppleves tørr hvis den ikke balanseres med varme naturbilder.

---

### Variant 8: «Fjordflukten» (Asymmetrisk 60/40 med bildeblødning)
- **Konsept:** Hero-bildet blør helt ut mot høyre skjermkant, mens venstresiden holdes stramt innenfor 1200 px gridet.
- **Hero-oppbygning:**
```
+-----------------------------------------+-------------------------------+
|       MiniHouse                         |                               |
|                                         |   [ 3:2 Hovedbilde blør       |
|       Et lite hus,                      |     helt ut til høyre         |
|       laget for å flyttes.              |     skjermkant ]              |
|                                         |                               |
|       Bygget for vestlandsklima...      |                               |
|       [ Følg prosjektet ]               |   Konseptbilde                |
+-----------------------------------------+-------------------------------+
```
- **Materialpass:** To likeverdige kolonner: venstre kolonne med taktilt foto av kjerneved, høyre kolonne med passets faktainnhold på eikefarget bunn.
- **Vurdering:** Svært dynamisk på brede skjermer, forankrer huset i landskapet og gir god leserytme.

---

## 3. Anbefaling for Retning A (Patina)

For den anbefalte retningen (A · Patina) velges en syntese av **Variant 1 («Horisonten»)** på desktop og **Variant 5 («Mobilkaskaden»)** på mobil. Dette gir maksimal ro, overholder alle retningslinjer i DESIGN-GUIDE §8, og holder all tekst pålitelig innenfor godkjente kontrastkrav.
