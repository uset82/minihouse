# MiniHouse · Wireframes (Oppgave A-6)

Dato: 2026-11-17.
Ansvarlig: Antigravity (Oppgave A-6, PLAN §4.1 og brief A-6).
Styrende dokumenter: [PLAN.md](../../PLAN.md) §8.3, [DESIGN-GUIDE.md](../../DESIGN-GUIDE.md) §6, [tokens.css](../../../../web/promo/src/styles/tokens.css).

Dette dokumentet definerer layout, komponentoppbygging, ARIA-semantikk og token-bindinger for de seksjonene PLAN §8.3 ikke tegnet ut. Hver seksjon er spesifisert i både **360 px mobil** (4 kolonner, 24 px gutter) og **1280 px desktop** (12 kolonner, maks 1200 px innhold, 24 px gutter).

---

## Innholdsfortegnelse

1. [Seksjon 3 · Bilder (Galleri & Lightbox)](#1-seksjon-3--bilder-galleri--lightbox)
2. [Seksjon 4 · Slik er det bygget (Tabs: Utvendig & Konstruksjon)](#2-seksjon-4--slik-er-det-bygget-tabs-utvendig--konstruksjon)
3. [Seksjon 6 · Slik bor du i MiniHouse (Irr-bånd)](#3-seksjon-6--slik-bor-du-i-minihouse-irr-bånd)
4. [Seksjon 7 · Fra verksted til tomt (3 steg)](#4-seksjon-7--fra-verksted-til-tomt-3-steg)
5. [Seksjon 8 · Status og Spørsmål (Faser & FAQ)](#5-seksjon-8--status-og-spørsmål-faser--faq)
6. [Seksjon 9 · Følg prosjektet (Skjema)](#6-seksjon-9--følg-prosjektet-skjema)
7. [Seksjon 10 · Bunntekst som stålbase (Footer)](#7-seksjon-10--bunntekst-som-stålbase-footer)

---

## 1. Seksjon 3 · Bilder (Galleri & Lightbox)

DESIGN-GUIDE §6.5: Panelvegg av vertikale bord (4:5) på desktop; horisontal sveipestripe med `scroll-snap` på mobil. Hvert bilde er en `<button>` som åpner `<dialog>` lightbox med fokusfelle.

### 1.1 Mobil (360 px)
```text
┌──────────────────────────────────────────┐
│ Bilder                                   │ Besley 800, --size-h2
│ Se huset fra ulike vinkler.              │ Jost 400, --size-lead
│                                          │
│ ┌──────────────────────┐ ┌────────────── │ Horisontal scroll-snap
│ │                      │ │               │ aspect-ratio: 4/5
│ │   [bilde 1: bad]     │ │ [bilde 2]     │ border-radius: var(--radius)
│ │                      │ │               │
│ └──────────────────────┘ └────────────── │
│ 1 av 12                                  │ Jost 500, --size-caption
│ Konseptbilde                             │ --malmfuru-mork
└──────────────────────────────────────────┘
```

### 1.2 Desktop (1280 px)
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Bilder                                                                      │
│ Se huset fra ulike vinkler og opplev materialene på nært hold.              │
│                                                                             │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐                 │
│ │            │ │            │ │            │ │            │                 │
│ │ bath-shower│ │ bath-vanity│ │ bath-window│ │bath-doorway│ 4:5 bordpanel    │
│ │ (4:5)      │ │ (4:5)      │ │ (4:5)      │ │ (4:5)      │ gap: --space-2  │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘                 │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────┐                 │
│ │                                                         │ 16:9 bred rad   │
│ │ meadow-wide (16:9)                                      │                 │
│ └─────────────────────────────────────────────────────────┘                 │
│ Konseptbilde                                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Lightbox Dialog (`<dialog>`)
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ [× Lukk (Esc)]                                                              │
│                                                                             │
│                        ┌────────────────────────┐                           │
│     [‹ Forrige]        │                        │       [Neste ›]           │
│                        │   Aktivt bilde         │                           │
│                        │   object-fit: contain  │                           │
│                        │                        │                           │
│                        └────────────────────────┘                           │
│                        Konseptbilde · 3 av 12                               │
│                        Dusjhjørne med stående petrolgrønne fliser           │
└─────────────────────────────────────────────────────────────────────────────┘
```
- Backdrop: `color-mix(in srgb, var(--tjaere) 92%, transparent)`.
- Navigasjon: tastatur piltaster venstre/høyre, Esc lukker, swipe på mobil.
- Returfokus: fokus returnerer til utløsende knapp når dialog lukkes.

---

## 2. Seksjon 4 · Slik er det bygget (Tabs: Utvendig & Konstruksjon)

DESIGN-GUIDE §6.7: WAI-ARIA tablist. Aktiv fane markeres med 3 px kobber understrek, ingen piller eller bokser.

### 2.1 Mobil (360 px)
```text
┌──────────────────────────────────────────┐
│ Slik er det bygget                       │ Besley 800, --size-h2
│                                          │
│ [ Utvendig ]   [ Konstruksjon ]          │ role="tablist"
│ ════════════                             │ 3 px kobber understrek på aktiv
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │                                      │ │
│ │  meadow-wide eller exploded (4:3)    │ │
│ │                                      │ │
│ └──────────────────────────────────────┘ │
│ Konseptbilde                             │
│                                          │
│ Kledningen er tenkt som en ventilert     │ Jost 400, --size-body
│ regnskjerm i stående gjenbrukt tre.      │
└──────────────────────────────────────────┘
```

### 2.2 Desktop (1280 px)
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Slik er det bygget                                                          │
│ En robust konstruksjon for krevende klima, basert på ærlige materialer.    │
│                                                                             │
│ [ Utvendig ]      [ Konstruksjon ]                                          │
│ ════════════                                                                │
│                                                                             │
│ ┌──────────────────────────────────────┬──────────────────────────────────┐ │
│ │                                      │ Kledningen er tenkt som en       │ │
│ │  meadow-wide eller exploded          │ ventilert regnskjerm i stående   │ │
│ │  aspect-ratio: 4/3                   │ gjenbrukt treverk.               │ │
│ │                                      │                                  │ │
│ │                                      │ Stålrammen i bunn gir et stivt   │ │
│ │                                      │ fundament for løft og flytting.  │ │
│ └──────────────────────────────────────┴──────────────────────────────────┘ │
│ Konseptbilde                                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```
- ARIA: `role="tablist"`, `role="tab"`, `aria-selected="true"`, `aria-controls="panel-id"`, `role="tabpanel"`.
- Tastatur: Piltaster venstre/høyre bytter aktiv fane.

---

## 3. Seksjon 6 · Slik bor du i MiniHouse (Irr-bånd)

DESIGN-GUIDE §6.8: Heldekkende bånd i `--irr` (`#2C4F40`), lys kalktekst (`#ECEAE4`, 7.59:1 kontrast). Ett stort bilde (3:2) for oppholdsrom, deretter 4 romkort (4:3) med Besley-overskrift og to linjer Jost.

### 3.1 Mobil (360 px)
```text
├────────────────── irr-bånd ──────────────────┤
│ Slik bor du i MiniHouse                      │ Besley 800, --size-h2, --kalk
│ Kompakt, lyst og gjennomtenkt for hverdagen. │ Jost 400, --size-lead, --kalk
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ living (3:2)                             │ │ Stort bilde
│ └──────────────────────────────────────────┘ │
│ Konseptbilde                                 │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ kitchen (4:3)                            │ │
│ └──────────────────────────────────────────┘ │
│ Kjøkken                                      │ Besley 700, --size-h3
│ Kompakt kjøkkenhjørne i dempet grønt med     │ Jost 400, --size-small
│ heltre benkeplate og vindu.                  │
│                                              │
│ [Sittebenk], [Oppbevaring], [Bad]...         │
├──────────────────────────────────────────────┤
```

### 3.2 Desktop (1280 px)
```text
├──────────────────────────────── irr-bånd ───────────────────────────────────┤
│ Slik bor du i MiniHouse                                                     │
│ Kompakt, lyst og gjennomtenkt for hverdagen.                                │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                                                                         │ │
│ │ living (3:2) · Lyst oppholdsrom med integrert sittebenk                 │ │
│ │                                                                         │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│ Konseptbilde                                                                │
│                                                                             │
│ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐     │
│ │ kitchen (4:3) │ │ bench (4:3)   │ │ storage (4:3) │ │ bath (4:3)    │     │
│ └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘     │
│ Kjøkken           Sittebenk         Oppbevaring       Bad                   │
│ Kompakt hjørne i  Plassbygd benk    Smarte skuffer    Stående fliser        │
│ dempet grønt med  med dyp skuff     i heltre integrert og dusjhjørne med    │
│ benk i heltre.    under vindu.      i konstruksjonen. glassdør.             │
├─────────────────────────────────────────────────────────────────────────────┤
```

---

## 4. Seksjon 7 · Fra verksted til tomt (3 steg)

PLAN §8.6 Seksjon 7: 3 trinn fra bygging under kontrollerte forhold i hall, til transport i ett stykke, og skånsom plassering på tomt.

### 4.1 Mobil (360 px)
```text
┌──────────────────────────────────────────┐
│ Fra verksted til tomt                    │ Besley 800, --size-h2
│ Tre steg fra planlegging til ferdig hus. │
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │ journey-workshop (4:3)               │ │
│ └──────────────────────────────────────┘ │
│ 1. Verksted                              │ Besley 700, --size-h3
│ Bygges tørt og presist innendørs.        │ Jost 400
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │ journey-truck (4:3)                  │ │
│ └──────────────────────────────────────┘ │
│ 2. Transport                             │
│ Fraktes som én modul på semitrailer.     │
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │ journey-plot (4:3)                   │ │
│ └──────────────────────────────────────┘ │
│ 3. Tomt                                  │
│ Løftes på plass på enkle støttepunkter.  │
└──────────────────────────────────────────┘
```

### 4.2 Desktop (1280 px)
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Fra verksted til tomt                                                       │
│ Bygges tørt og sikkert innendørs, transporteres som én ferdig modul.        │
│                                                                             │
│ ┌────────────────────────┐ ┌────────────────────────┐ ┌───────────────────┐ │
│ │ journey-workshop (4:3) │ │ journey-truck (4:3)    │ │ journey-plot(4:3) │ │
│ └────────────────────────┘ └────────────────────────┘ └───────────────────┘ │
│ 1. Verksted                2. Transport               3. Tomt               │
│ Bygges komplett i verksted Fraktes på lavbygd trailer Løftes skånsomt       │
│ med dokumentert treverk og som én samlet modul.       på plass på tomtens   │
│ stålchassis.                                          fundament.            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Seksjon 8 · Status og Spørsmål (Faser & FAQ)

DESIGN-GUIDE §6.10: Prosjektstatus som ren teksttidslinje; FAQ bygget på native `<details>` og `<summary>` uten JavaScript.

### 5.1 Mobil (360 px)
```text
┌──────────────────────────────────────────┐
│ Hvor langt har vi kommet?                │ Besley 800, --size-h2
│ Prosjektet er under utvikling.           │
│                                          │
│ [●] Konsept og arkitektur (fullført)     │
│ [●] Struktur og teknisk skisse (pågår)   │ Statusliste
│ [○] Prototypebygging (planlagt)          │
│ [○] Transporttest og evaluering          │
│                                          │
│ Ofte stilte spørsmål                     │ Besley 700, --size-h3
│                                          │
│ ▶ Trenger jeg byggetillatelse?           │ <summary> Jost 500, min 48px touch
│                                          │
│ ▼ Når blir prototypen ferdig?            │ Åpen <details>
│   Det vet vi ikke ennå. Følg prosjektet, │ Jost 400, --size-body
│   så sier vi fra når det skjer.          │
│                                          │
│ ▶ Kan huset flyttes flere ganger?        │
└──────────────────────────────────────────┘
```

### 5.2 Desktop (1280 px)
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Hvor langt har vi kommet?                                                   │
│                                                                             │
│ ┌──────────────────────────────┬──────────────────────────────────────────┐ │
│ │ Status                       │ Ofte stilte spørsmål                     │ │
│ │                              │                                          │ │
│ │ ● Konsept og design          │ ▶ Trenger jeg byggetillatelse?           │ │
│ │   Fullført november 2026     │                                          │ │
│ │                              │ ▼ Når blir prototypen ferdig?            │ │
│ │ ◐ Teknisk dimensjonering     │   Det vet vi ikke ennå. Følg prosjektet, │ │
│ │   Pågår nå                   │   så sier vi fra når det skjer.          │ │
│ │                              │                                          │ │
│ │ ○ Prototype og verifisering  │ ▶ Hva veier modulen?                     │ │
│ │   Planlagt                   │                                          │ │
│ │                              │ ▶ Kan huset kobles til strøm og vann?   │ │
│ └──────────────────────────────┴──────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Seksjon 9 · Følg prosjektet (Skjema)

D1 & D10: MiniHouse er ikke til salgs. Skjemaet samler kun e-post (påkrevd) og navn (valgfritt) for prosjektoppdateringer. Ingen priser eller kjøpsavtaler.

### 6.1 Mobil (360 px)
```text
┌──────────────────────────────────────────┐
│ Følg prosjektet                          │ Besley 800, --size-h2
│ Få oppdateringer når prototypen tar form │ Jost 400, --size-lead
│ og materialene dokumenteres.             │
│                                          │
│ E-postadresse *                          │ Jost 500, --size-small
│ ┌──────────────────────────────────────┐ │
│ │ din.epost@eksempel.no                │ │ <input type="email"> min 48px
│ └──────────────────────────────────────┘ │ border: 1px solid var(--solvgra)
│                                          │
│ Navn (valgfritt)                         │
│ ┌──────────────────────────────────────┐ │
│ │ Ola Nordmann                         │ │ <input type="text"> min 48px
│ └──────────────────────────────────────┘ │
│                                          │
│ [ ] Jeg samtykker til å motta          │ <input type="checkbox"> 24x24 px
│     prosjektoppdateringer.             │ + lenke til personvern
│                                          │
│ ┌──────────────────────────────────────┐ │
│ │ Følg prosjektet                      │ │ Primærknapp: background --kobber
│ └──────────────────────────────────────┘ │ farge --kalk, min-height: 48px
└──────────────────────────────────────────┘
```

### 6.2 Desktop (1280 px)
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ ┌────────────────────────────────────┬────────────────────────────────────┐ │
│ │ Følg prosjektet                    │ E-postadresse *                    │ │
│ │                                    │ ┌────────────────────────────────┐ │ │
│ │ Bli med på reisen. Vi deler        │ │ din.epost@eksempel.no          │ │ │
│ │ erfaringer fra dimensjonering,     │ └────────────────────────────────┘ │ │
│ │ testing og gjenbruk av treverk     │                                    │ │
│ │ underveis.                         │ Navn (valgfritt)                   │ │
│ │                                    │ ┌────────────────────────────────┐ │ │
│ │ Ingen spam. Kun faglige            │ │ Ola Nordmann                   │ │ │
│ │ oppdateringer og invitasjon til    │ └────────────────────────────────┘ │ │
│ │ visning av prototypen.             │                                    │ │
│ │                                    │ [ ] Jeg samtykker til oppdatering. │ │
│ │                                    │                                    │ │
│ │                                    │ [ Følg prosjektet ]                │ │
│ └────────────────────────────────────┴────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Seksjon 10 · Bunntekst som stålbase (Footer)

DESIGN-GUIDE §6.12 & PLAN §8.3: Fullbredde `--tjaere` bånd (`#241A13`) med lys tekst og `--kobber-lys` lenker (`#E08A52`, 6.43:1 kontrast). Representerer stålfundamentet som bærer huset.

### 7.1 Mobil (360 px)
```text
├────────────────── tjaere-bånd ──────────────────┤
│ MiniHouse                                       │ Besley 800, --size-h3
│                                                 │
│ Alle bilder er konseptbilder.                   │ Jost 400, --size-caption
│ Huset er under utvikling.                       │
│                                                 │
│ • Personvern                                    │ Jost 500, lenker i --kobber-lys
│ • For fagfolk (dokumentasjon)                   │
│ • English                                       │
│                                                 │
│ © 2026 MiniHouse                                │
├─────────────────────────────────────────────────┤
```

### 7.2 Desktop (1280 px)
```text
├──────────────────────────────── tjaere-bånd ────────────────────────────────┤
│ ┌─────────────────────────────────────┬───────────────────────────────────┐ │
│ │ MiniHouse                           │ Lenker                            │ │
│ │                                     │                                   │ │
│ │ Alle bilder er konseptbilder.       │ • Personvern                      │ │
│ │ Huset er under utvikling.           │ • For fagfolk (dokumentasjon)     │ │
│ │ Ingen kommersiell produksjon i dag. │ • English                         │ │
│ │                                     │                                   │ │
│ │                                     │ © 2026 MiniHouse                  │ │
│ └─────────────────────────────────────┴───────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────────┤
```
