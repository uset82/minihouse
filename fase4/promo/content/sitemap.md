# Sitemap and content model

2026-11-18, revised for plan R2. This is the page structure the site is built against. Copy lives in `web/promo/src/content/nb.json` and `en.json`; every factual sentence traces to the [claims register](claims-register.csv). The look is in [DESIGN-GUIDE.md](../DESIGN-GUIDE.md), and the built example is in [reference/](../reference/).

---

## 1 · Routes

| Route | Language | Content | State |
|---|---|---|---|
| `/` | nb (`<html lang="nb">`) | the landing page | built |
| `/en/` | en (`<html lang="en">`) | the same page, mirrored | built |
| `/personvern`, `/en/privacy` | nb / en | privacy page, linked from the form and the footer | text blocked on D6 and the contact address |
| `/404` | nb + en | not found, with a link home | built (check that Canner returns a real 404) |
| `/sitemap.xml`, `/robots.txt` | – | both languages | built |
| `hreflang` | – | `nb` ↔ `en` pairs, `x-default` = `/` | built |

External links appear only in the footer: the documentation site ([K-28](claims-register.csv)) and, once it's live, the lab.

---

## 2 · Sections, in order

| # | Section | Anchor | Content keys | Images (`images.json` ids) | Claims |
|---|---|---|---|---|---|
| – | Header | – | `nav.*`, `meta.*` | – | none |
| 1 | Hero: «Et lite hus, laget for å flyttes.» (D12), with the **concept film** | `#bygget` (the top) | `hero.*`, `film.*` | the film `house` (still `hero-slope` without the film media) | K-01, K-05, K-19, K-20, K-21, K-35 |
| 2 | Nøkkelinfo (oak band) | `#nokkelinfo` | `facts.items[]` | – | K-01, K-02, K-03, K-04, K-05, K-19, K-25 |
| 3 | Inne i MiniHouse (**irr band, funk**, moved up 2026-11-18) | `#bo` | `living.title`, `living.lead`, `film.*` | the films `living` and `bath`, the bath one in the **mirror frame** (stills `living`, `bath-window` without the film media) | K-10, K-11, K-12, K-35 |
| 4 | Huset i bilder (contact-sheet gallery and lightbox; the nav's «Huset») | `#bilder` | `gallery.*` | `meadow-wide`, `bath-vanity`, `bench`, `bath-shower`, `kitchen`, `bath-doorway`, `storage` | K-20, K-10, K-11 |
| 5 | Gammelt tre, nytt hus (materials and passports) | `#materialer` | `materials.*` | `texture-malmfuru`, `texture-eik`, `texture-kobber`, `texture-stal` | K-03, K-06, K-07, K-08, K-09, K-22, K-23 |
| 6 | Under kledningen (two views: Utvendig and Konstruksjon, no tabs) | – | `build.*` | `meadow-wide`, `exploded` | K-03, K-04, K-21 |
| 7 | Fra verksted til tomt (journey, **giant numerals**) | `#flytting` | `journey.*` | `journey-workshop`, `journey-truck`, `journey-plot` | K-05, K-27 |
| 8 | Hvor langt har vi kommet? (status and FAQ) | `#sporsmal` | `status.*`, `faq.*` | – | K-14, K-15, K-16, K-17, K-18, K-19, K-26 |
| 9 | Følg prosjektet (**copper band**, once D6 is decided) | `#folg` | `interest.*` | – | K-30, K-32, K-24 |
| 10 | Footer (steel base) | – | `footer.*` | – | K-19, K-20, K-28, K-29 |

**Bands, in order:**

1. kalk (hero)
2. eik (key facts)
3. **irr** (living)
4. kalk (gallery)
5. kalk with a sølvgrå hairline (materials)
6. kalk with a sølvgrå hairline (build)
7. kalk (journey)
8. kalk with a sølvgrå hairline (status and FAQ)
9. **kobber** (follow)
10. tjære (footer)

The room list (`living.rooms[]`) is no longer shown: the lead sentence already names the rooms (DESIGN-GUIDE §6.8). The keys can stay in the content files until DeepSeek removes them.

---

## 3 · Navigation

| Slot | Labels | Source |
|---|---|---|
| Primary, desktop | Huset (→ `#bilder`), Materialer, Flytting, Spørsmål | page map |
| Primary, mobile | same, in a «Meny» sheet | DESIGN-GUIDE §6.2 |
| Header action | «Følg prosjektet» (until D6, the preview's action is «Se huset») | D1 |
| Language | «English» / «Norsk» | D3 |
| Footer | Personvern, For fagfolk, contact | address missing ([K-29](claims-register.csv)) |

---

## 4 · Content model

Cursor owns `web/promo/src/content/schema.ts`, which is the source of truth for the keys. DeepSeek owns `nb.json` and `en.json`.

| Key group | Section | Notes |
|---|---|---|
| `meta.*` | head | title, description, OG alt text |
| `nav.*` | header | `skip`, `menu`, `close`, `language`, `cta` |
| `hero.*` | 1 | `title`, `lead`, `cta`, `gallery`, `caption` |
| `facts.items[]` | 2 | five `{ label, value }` pairs |
| `gallery.*` | 3 | `title`, `count`, `prev`, `next`, `close` |
| `build.*` | 4 | two tab labels and two bodies |
| `materials.*` | 5 | `title`, `lead`, `passportTitle`, `rows`, `items[]`, in the order malmfuru, eik, kobber, stål |
| `living.*` | 6 | `title`, `lead` |
| `journey.*` | 7 | `title`, `steps[] { title, body }`, exactly three |
| `status.*`, `faq.*` | 8 | each FAQ answer traces to a claim row |
| `interest.*` | 9 | `title`, `lead`, `fields` (`email` required, `name` optional), `consent`, `submit`, `success`, `errors.*` |
| `footer.*` | 10 | `contact`, `privacy`, `pro`, `docs`, `lab`, `imagesNote` |
| `privacy.*` | privacy page | blocked on D6 |

---

## 5 · Structure and accessibility

- One `<h1>` per page (the hero title). Sections use `<h2>`; sub-parts use `<h3>`.
- Landmarks: `header`, `nav`, `main`, `footer`, plus a «Hopp til innhold» skip link.
- `<dl>` for the key facts and each passport, `<details>` for the FAQ, a WAI-ARIA tablist for the build tabs, `<dialog>` for the lightbox, `<ol>` for the journey.
- Decorative shapes (the mirror frame, the journey numerals) are `aria-hidden`. The images keep their alt text.
- No section relies on an image to carry a fact.

---

## 6 · Open items

| Item | Waiting for |
|---|---|
| The follow form, the copper band and the privacy text | D6 (where sign-ups go, the e-mail service) |
| Footer contact | the contact address (K-29) |
| Steel passport image (it shows wood cladding) | Antigravity |
| Workshop journey image (288 × 144 px, too small for the bigger layout) | Carlos's render via the shot list, then Antigravity |
