# Copy deck · Norwegian Bokmål · landing preview

**Landing preview, 2026-11-17 (D13).** Task D-4. Every string in `web/promo/src/content/nb.json`, with the claims-register row it traces to. A sentence without a row does not ship ([design guide](../DESIGN-GUIDE.md) §9).

Rules applied: sentence case, short sentences, no banned words, «guillemets», decimal comma, `ca.`, `×`. Actions keep one name: «Følg prosjektet» → «Takk! Du følger nå prosjektet.» MiniHouse is not for sale (D10), so there is no price, no ordering and no sales wording anywhere.

**Hero title selected by Carlos (D12): «Et lite hus, laget for å flyttes.»** It replaced option A «Et lite hus som kan flyttes.» and now sits in the JSON.

---

## meta

| Key | Text | Claims |
|---|---|---|
| `meta.title` | MiniHouse for Vestlandet | K-01, K-13 |
| `meta.description` | Et huskonsept for Bergen på ca. 6 × 3 m. Se romløsningen og planen for gjenbruk av gamle furubord. | K-01, K-03, K-07, K-08, K-13, K-19, K-23 |
| `meta.ogAlt` | Konseptbilde av MiniHouse, et lite hus med saltak i svart metall og kledning av gjenbrukt tre, på en vestlandsk skråning. | K-04, K-20 |

## nav

| Key | Text | Claims |
|---|---|---|
| `nav.skip` | Hopp til innhold | – |
| `nav.house` | Huset | – |
| `nav.materials` | Materialer | – |
| `nav.moving` | Flytting | – |
| `nav.questions` | Spørsmål | – |
| `nav.cta` | Følg prosjektet | D1 |
| `nav.menu` | Meny | – |
| `nav.close` | Lukk | – |
| `nav.language` | English | D3 |

## hero

| Key | Text | Claims |
|---|---|---|
| `hero.title` | Et lite hus, laget for å flyttes. | K-01, K-05 |
| `hero.lead` | Vi tegner et hus for Bergen med gamle furubord utenpå, eik i tersklene og kobber rundt speilet på badet. | K-06, K-07, K-08, K-13, K-19, K-23 |
| `hero.cta` | Følg prosjektet | D1 |
| `hero.gallery` | Se huset | D13 |
| `hero.caption` | Konseptbilde | K-20 |

## facts

| Key | Text | Claims |
|---|---|---|
| `facts.items[0]` | Størrelse · ca. 6 × 3 m | K-01 |
| `facts.items[1]` | Konstruksjon · stålramme og gjenbrukt tre | K-03 |
| `facts.items[2]` | Tak · saltak i metall (konsept) | K-04 |
| `facts.items[3]` | Flytting · mål om å flyttes i ett stykke | K-05 |
| `facts.items[4]` | Status · under utvikling | K-19 |

## gallery

| Key | Text | Claims |
|---|---|---|
| `gallery.title` | Huset i bilder | K-20 |
| `gallery.count` | `{current} av {total}` (template; «3 av 12») | – |
| `gallery.prev` | Forrige | – |
| `gallery.next` | Neste | – |
| `gallery.close` | Lukk | – |

## build

| Key | Text | Claims |
|---|---|---|
| `build.title` | Under kledningen | K-03, K-06 |
| `build.lead` | I tegningene møter værgrå bord et svart saltak. Under huset ligger en lav ramme av stål. | K-03, K-04, K-06, D8 |
| `build.tabExterior` | Utvendig | – |
| `build.tabStructure` | Konstruksjon | – |
| `build.exterior` | Vi planlegger en luftespalte bak kledningen så bordene kan tørke mellom regnbygene. Døren og vindusrammene er tegnet i svart. | K-21, D8 |
| `build.structure` | To langsgående stålbjelker og kortere tverrbjelker danner understellet i utkastet. Dimensjonene er fortsatt åpne. | K-03, K-19 |

## materials

| Key | Text | Claims |
|---|---|---|
| `materials.title` | Gammelt tre, nytt hus | K-03 |
| `materials.lead` | Vi vil gi gamle bord et nytt liv som kledning. Når vi finner treet, skal materialpasset vise hvor det kommer fra og hva det ble brukt til før. | K-06, K-07, K-22 |
| `materials.passportTitle` | Materialpass | – |
| `materials.rows.material` | Materiale | – |
| `materials.rows.origin` | Opprinnelse | – |
| `materials.rows.previousUse` | Tidligere bruk | – |
| `materials.rows.usedFor` | Brukes til | – |
| `materials.rows.treatment` | Behandling | – |
| `materials.rows.status` | Status | – |

### Malmfuru

| Key | Text | Claims |
|---|---|---|
| `items[0].name` | Malmfuru | K-07 |
| `items[0].lead` | Rødbrun kjerneved av furu har lenge vært brukt i norsk kledning. Vi ser etter gamle bord av saktevokst furu. | K-07, K-33 |
| `items[0].passport.material` | furu, kjerneved | K-07 |
| `items[0].passport.origin` | dokumenteres per parti | K-22 |
| `items[0].passport.previousUse` | dokumenteres per parti | K-22 |
| `items[0].passport.usedFor` | kledning | K-06 |
| `items[0].passport.treatment` | ikke bestemt | K-09 |
| `items[0].passport.status` | planlagt | K-07 |

### Eik

| Key | Text | Claims |
|---|---|---|
| `items[1].name` | Europeisk eik | K-08, D13 |
| `items[1].lead` | Vi har tegnet inn eik der hånden hviler på vindusbrettet og foten treffer terskelen. | K-08 |
| `items[1].passport.material` | europeisk eik | K-08, D13 |
| `items[1].passport.origin` | dokumenteres per parti | K-22 |
| `items[1].passport.previousUse` | dokumenteres per parti | K-22 |
| `items[1].passport.usedFor` | terskler og innvendige vindusbrett | K-08 |
| `items[1].passport.treatment` | ikke bestemt | K-09 |
| `items[1].passport.status` | planlagt | K-08 |

### Kobber

| Key | Text | Claims |
|---|---|---|
| `items[2].name` | Kobber | K-23 |
| `items[2].lead` | I skissen har speilet på badet en smal kobberkant mot de petrolgrønne flisene. | K-23, D8 |
| `items[2].passport.material` | kobber | K-23 |
| `items[2].passport.origin` | dokumenteres | K-22 |
| `items[2].passport.previousUse` | ikke bestemt | – |
| `items[2].passport.usedFor` | detaljer, blant annet på badet | K-23 |
| `items[2].passport.treatment` | ikke bestemt | K-09 |
| `items[2].passport.status` | konsept | K-23 |

### Stål

| Key | Text | Claims |
|---|---|---|
| `items[3].name` | Stål | K-03 |
| `items[3].lead` | I tegningene ligger stålrammen under huset og binder understellet sammen. | K-03 |
| `items[3].passport.material` | stål | K-03 |
| `items[3].passport.origin` | dokumenteres | K-22 |
| `items[3].passport.previousUse` | ikke bestemt | – |
| `items[3].passport.usedFor` | ramme og chassis | K-03 |
| `items[3].passport.treatment` | ikke bestemt | K-09 |
| `items[3].passport.status` | konsept | K-03 |

## living

| Key | Text | Claims |
|---|---|---|
| `living.title` | Inne i MiniHouse | K-10, K-12 |
| `living.lead` | I skissen deler kjøkkenet og vindusbenken ett rom. Skuffene ligger under setet, og badet får plass i den ene enden. | K-10, K-12 |
| `rooms[0]` | Kjøkken · Benkeplate i tre og dempede fronter langs veggen. | K-12, D8 |
| `rooms[1]` | Sittebenk · En polstret benk følger vinduet. | K-12, D8 |
| `rooms[2]` | Oppbevaring · Dype skuffer tar vare på plassen under benken. | K-12, D8 |
| `rooms[3]` | Bad · Fargeskissen for badet viser petrolgrønne fliser, tre og kobber. | K-10, K-23, D8 |

## journey

| Key | Text | Claims |
|---|---|---|
| `journey.title` | Fra verksted til tomt | – |
| `steps[0]` | Verksted · Planen er å bygge huset ferdig i verkstedet. | K-05 |
| `steps[1]` | Transport · Målet er å frakte huset i ett stykke på lastebil. Ruten må sjekkes først. | K-05, K-27 |
| `steps[2]` | Tomt · På tomten ser vi for oss at en kran løfter huset på plass på støttene. | K-05 |

## status

| Key | Text | Claims |
|---|---|---|
| `status.title` | Hvor står prosjektet? | K-19 |
| `status.body` | MiniHouse finnes foreløpig på tegnebordet. Vi arbeider med stålrammen og leter etter tre til kledningen. | K-03, K-07, K-19, K-26 |
| `phases[0]` | Tegninger og plan · første utkast klart | K-26 |
| `phases[1]` | Beregninger · pågår | K-26 |
| `phases[2]` | Prototype · ikke bygget | K-19, K-26 |

Plain words, no phase numbers: «Fase 0–4» belongs to the documents, never to the buyer page (K-26 note).

## faq

| Key | Question | Answer | Claims |
|---|---|---|---|
| `items[0]` | Trenger huset byggesøknad? | Det avhenger av hva huset skal brukes til, og det er kommunen som avgjør. | K-14 |
| `items[1]` | Er huset til salgs? | MiniHouse er et huskonsept under utvikling. Det finnes ingen ferdig modell å kjøpe. | K-19, K-31 |
| `items[2]` | Når blir prototypen ferdig? | Vi har ennå ingen dato for en prototype. | K-17, K-19 |
| `items[3]` | Hvordan flyttes huset? | Målet er at det skal kunne flyttes i ett stykke på lastebil. Hver rute må sjekkes før den brukes. | K-05, K-27 |
| `items[4]` | Hva er et konseptbilde? | Et konseptbilde viser hvordan vi ser for oss huset. Bildene av badet viser farger og materialer, mens planløsningen fortsatt er åpen. | K-10, K-20, D8 |
| `items[5]` | Hvilket tre vil dere bruke om igjen? | Vi ser etter gamle furubord til kledningen. Når vi finner et egnet parti, vil vi dokumentere hvor bordene kommer fra og hva de ble brukt til før. | K-06, K-07, K-22 |

## interest

Reserved copy for the future follow form (DESIGN-GUIDE §6.11). E-mail required, name optional, nothing else (K-32). Cursor's schema now holds exactly `fields { email, name, optional }` plus `title`, `lead`, `consent`, `submit`, `success` and `errors`; the old `price`, `municipality`, `use`, `useOptions`, `timeline`, `timelineOptions` and `message` keys are gone from both JSON files.

| Key | Text | Claims |
|---|---|---|
| `interest.title` | Følg prosjektet | D1 |
| `interest.lead` | Legg igjen e-postadressen din, og få en melding når det skjer noe i prosjektet. | K-30 |
| `fields.email` | E-post | – |
| `fields.name` | Navn | – |
| `fields.optional` | (valgfritt) | – |
| `interest.consent` | Ja, send meg oppdateringer om MiniHouse på e-post. | D1, K-32 |
| `interest.submit` | Følg prosjektet | D1 |
| `interest.success` | Takk! Du følger nå prosjektet. | D1 |
| `errors.required` | Feil: Skriv inn e-postadressen din. | – |
| `errors.email` | Feil: Skriv inn en e-postadresse, for eksempel navn@epost.no. | – |
| `errors.network` | Feil: Noe gikk galt. Prøv igjen om et øyeblikk. | – |

The consent checkbox is unticked by default and carries the «Personvern» link. The success line is the only place the state changes: the button stays «Følg prosjektet».

## footer

| Key | Text | Claims |
|---|---|---|
| `footer.contact` | *(omitted until Carlos supplies an address — K-29)* | K-29 |
| `footer.privacy` | Personvern | – |
| `footer.pro` | For fagfolk | – |
| `footer.docs` | Dokumentasjon | K-28 |
| `footer.lab` | 3D-lab | K-28 |
| `footer.imagesNote` | Alle bilder er konseptbilder. Huset er under utvikling. | K-19, K-20 |

## privacy

| Key | Text | Claims |
|---|---|---|
| `privacy.title` | Personvern | – |
| `privacy.body` | Du kan se bildene og lese om huset uten å registrere deg. Denne siden har ingen påmelding og ber ikke om navn eller e-postadresse. | K-24, D6 |

The preview has no sign-up form. D6 covers the service, recipient and privacy notice for a future email subscription. The interest strings are reserved for that feature.

---

## What this deck deliberately does not say

No price, no «Pris kommer», no ordering, no sales wording, no FINN ad (D10) — the house is not for sale (K-31). No delivery date, no weight, no U-value, no «ingen byggesøknad», no «bærekraftig», no contacts that do not exist, no claim about moving frequency, no named timber lot. Every one of those has a row in the register that says why.

## notFound

| Key | Text |
|---|---|
| `notFound.title` | Siden finnes ikke |
| `notFound.body` | Adressen stemmer ikke. |
| `notFound.home` | Til forsiden |
