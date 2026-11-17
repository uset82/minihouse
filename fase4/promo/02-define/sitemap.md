# Sitemap and content model · v0

**v0 draft, 2026-11-17.** Task D-3 (PLAN 2.5, matching PLAN §8.6). Revise to v1 after the card sort (D-8) and before G2.

Two routes, one page each: `/` in Norwegian Bokmål (default) and `/en/` in English. Everything below must exist in both languages unless it says otherwise.

Basis: the claims register, [kit.md](../01-empathize/kit.md), PLAN §8.6 and the content keys in [agents/README.md](../agents/README.md) §4.1. Antigravity's market scan is **excluded** until CR-16 is closed ([claude-code-review.md](../review/claude-code-review.md)), so the section order comes from PLAN §8.6 and Carlos's concept mockups, not from competitor patterns.

---

## 1 · Routes

| Route | Language | Content | Status |
|---|---|---|---|
| `/` | nb (`<html lang="nb">`) | the promo page | to build |
| `/en/` | en (`<html lang="en">`) | the same page, mirrored | to build |
| `/personvern` and `/en/privacy` | nb / en | privacy page (D-5), linked from the form and the footer | blocked on D6 |
| `/404` | nb | not found, with a link home | to build |
| `/sitemap.xml`, `/robots.txt` | – | both languages | to build (Cursor, C-8) |
| `hreflang` | – | `nb` ↔ `en` pairs, `x-default` = `/` | to build |

External links only in the footer: the documentation site ([K-28](claims-register.csv)) and, after launch, the lab (PLAN 6.1).

---

## 2 · Sections, in order (PLAN §8.6)

| # | Section (Norwegian working title) | Anchor | Content keys | Images (`images.json` ids) | Claims |
|---|---|---|---|---|---|
| – | Header | – | `nav.*`, `meta.*` | – | none |
| 1 | Hero: «Et lite hus, laget for å flyttes.» | `#hjem` | `hero.*` | `hero-slope` | K-01, K-05, K-19, K-20, K-21 |
| 2 | Nøkkelinfo (key facts) | `#nokkelinfo` | `facts.items[]` | – | K-01, K-02, K-03, K-04, K-05, K-19, K-25 |
| 3 | Bilder (gallery and lightbox) | `#bilder` | `gallery.*` | 4 × `bath-*`, plus the render set | K-20, K-10, K-11 |
| 4 | Slik er det bygget (tabs: Utvendig / Konstruksjon) | `#bygget` | `build.*` | `meadow-wide`, `exploded`, textures | K-03, K-04, K-21 |
| 5 | Gammelt tre, nytt hus (materials and passports) | `#materialer` | `materials.*` | `texture-malmfuru`, `texture-eik`, `texture-kobber`, `texture-stal` | K-03, K-06, K-07, K-08, K-09, K-22, K-23 |
| 6 | Slik bor du i MiniHouse (irr band) | `#bo` | `living.*` | `living`, `kitchen`, `bench`, `storage`, `bath-*` | K-10, K-11, K-12 |
| 7 | Fra verksted til tomt (journey) | `#flytting` | `journey.*` | `journey-workshop`, `journey-truck`, `journey-plot` | K-05, K-27 |
| 8 | Hvor langt har vi kommet? (status and FAQ) | `#sporsmal` | `status.*`, `faq.*` | – | K-14, K-15, K-16, K-17, K-18, K-19, K-26 |
| 9 | Følg prosjektet (follow form) | `#folg` | `interest.*` | – | K-30, K-32, K-24 |
| 10 | Footer (steel base) | – | `footer.*` | – | K-19, K-20, K-28, K-29 |

The bands, in order: kalk (hero), eik (key facts), kalk (gallery), kalk with a sølvgrå hairline (build), kalk (materials), irr (living), kalk (journey), kalk (status/FAQ), kalk (form), tjære (footer). No two neighbouring bands share a colour except kalk-kalk with a hairline ([DESIGN-GUIDE.md](../DESIGN-GUIDE.md) §5).

---

## 3 · Navigation

| Slot | v0 labels | Source | Open |
|---|---|---|---|
| Primary, desktop | Huset, Materialer, Flytting, Spørsmål | PLAN §8.6 | card sort may rename them; the anchors stay |
| Primary, mobile | same, in a «Meny» sheet | DESIGN-GUIDE §6.2 | – |
| Header action | «Følg prosjektet» | D1 | – |
| Language | «English» / «Norsk» | D3 | – |
| Footer | Personvern, For fagfolk, e-post | PLAN §8.6 | address missing ([K-29](claims-register.csv)) |

The nav labels are the one thing the card sort can change cheaply. If three participants call a cluster «Hva det er laget av», the label changes and the anchor does not ([card-sort.md](../03-ideate/card-sort.md) §5).

---

## 4 · Content model

Cursor owns `schema.ts`; DeepSeek owns `nb.json` and `en.json`. The keys are fixed in [agents/README.md](../agents/README.md) §4.1; this table is the map from section to key group, so a missing key is caught before build.

| Key group | Sections | Notes |
|---|---|---|
| `meta.*` | head | title, description, OG alt text, both languages |
| `nav.*` | header | `skip`, `menu`, `close`, `language`, `cta` |
| `hero.*` | 1 | `title`, `lead`, `cta`, `gallery`, `caption` |
| `facts.items[]` | 2 | five `{ label, value }` pairs; values are status-bearing sentences |
| `gallery.*` | 3 | `title`, `count`, `prev`, `next`, `close` |
| `build.*` | 4 | two tab labels, two bodies; the tab panel text is in `exterior` / `structure` |
| `materials.*` | 5 | `title`, `lead`, `passportTitle`, `rows` (labels), `items[]` (one per material, with passport values) |
| `living.*` | 6 | `title`, `lead`, `rooms[] { id, title, body }` |
| `journey.*` | 7 | `title`, `steps[] { title, body }` — exactly three |
| `status.*` | 8 | `title`, `body`, `phases[] { name, state }` |
| `faq.*` | 8 | `title`, `items[] { q, a }` — each `a` traces to a claim row |
| `interest.*` | 9 | `title`, `lead`, `fields` (`email` required, `name` optional, `optional`), `consent` (the checkbox), `submit`, `success`, `errors.*`. Cursor's schema holds only these; `price`, `municipality`, `use`, `useOptions`, `timeline`, `timelineOptions` and `message` are gone from both JSON files |
| `footer.*` | 10 | `contact`, `privacy`, `pro`, `docs`, `lab`, `imagesNote` |
| `privacy.*` | privacy page | `title`, `body` — blocked on D6 |

`materials.items[]` order: malmfuru, eik, kobber, stål ([DESIGN-GUIDE.md](../DESIGN-GUIDE.md) §6.6). The passport values for eik are «planlagt», and for malmfuru «dokumenteres per parti» until C-08 lands.

---

## 5 · Image → section map

| `images.json` id | Section | Kind | Status at v0 |
|---|---|---|---|
| `hero-slope` | 1 | render | to produce |
| `meadow-wide`, `exploded` | 4 | render | to produce |
| `living`, `kitchen`, `bench`, `storage` | 6 | render | to produce |
| `bath-shower`, `bath-vanity`, `bath-window`, `bath-doorway` | 3, 6 | render | **pending** (the only four that exist) |
| `journey-workshop`, `journey-truck`, `journey-plot` | 7 | render | to produce |
| `texture-malmfuru`, `texture-eik`, `texture-kobber`, `texture-stal` | 5 | texture | to produce, prefer real photos |
| `og-image` | head | render | to produce |

Every one carries alt text and a caption in both languages; every image of the house carries «Konseptbilde» / «Concept image» ([K-20](claims-register.csv)). The bathroom set is captioned as material mood until the R1 plan confirms the size ([K-10](claims-register.csv), decisions D8).

---

## 6 · Structure and accessibility

- One `<h1>` per page (the hero title). Sections use `<h2>`, sub-parts `<h3>`.
- Landmarks: `header`, `nav`, `main`, `footer`; a «Hopp til innhold» skip link.
- Reading order follows the page map; the mobile sticky CTA is last in the DOM, first visually when it appears.
- `<dl>` for the key facts and for each passport; `<details>` for the FAQ; WAI-ARIA tablist for the build tabs; `<dialog>` for the lightbox.
- The language switch is a link to the mirrored route, not a button that reloads the page.
- No section relies on an image to carry a fact: if the render fails, the sentence and the caption still work.

---

## 7 · What changes at v1

| Item | Depends on |
|---|---|
| Nav labels and section order | card sort (D-8) |
| Which concept image feeds which section | Antigravity's shot list and the G4 approval |
| Bathroom section wording | R1 plan (K-10) |
| The form and the privacy route | D6 (K-24) |
| Footer contact | K-29 |
| Market-derived section emphasis or trust signals | Antigravity's A-3 redo (CR-16 closed) |

The anchors and the content keys should not change at v1: they are what Cursor builds against, and renaming them late breaks the copy port.
