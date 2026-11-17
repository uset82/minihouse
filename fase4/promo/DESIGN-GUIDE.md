# MiniHouse promo website · Design guide

**For every agent that designs, builds, writes or reviews the promo site: Antigravity, Cursor and DeepSeek.** Revision R1.3, 2026-11-17. Read this before you touch UI, copy or images. It turns the visual system in [PLAN.md §8](PLAN.md) into rules you can check.

**Built reference:** `fase4/promo/reference/` holds direction A built by Claude Code to this guide: header, hero, key facts, the material passport and the footer, at 360 px and 1280 px. Open `index.html`. When this guide and the reference seem to disagree, ask; don't guess.

R1.3 changes: §6.6 now describes the passport as built in the reference: a stub with an eyelet and a perforation, the material name at `--size-h3`, and no hairlines between rows.

R1.2 changes: the call to action is «Følg prosjektet» (D1), and §6.11 is now a follow form (e-mail and optional name), because MiniHouse isn't for sale (D10).

R1.1 changes:

- Side margins are `--gutter` at every width.
- §3 now lists the breakpoints and the few values allowed outside `tokens.css`.
- Every component size in §6 is now given as a token name.
- No token value changed, so `tokens.css` stays as it is.

The working method comes from the `frontend-design` skill that Carlos uses in Claude Code. The original is on this machine, read-only: `C:\Users\carlos\.claude\plugins\cache\claude-plugins-official\frontend-design\1.1.1\skills\frontend-design\SKILL.md`. This guide applies that method to MiniHouse. Where the two differ, this guide wins.

---

## 1. The method: follow these steps in order, for every section

1. **Start from the subject.** MiniHouse is a small movable house built from old timber, with copper fittings and a steel base, made for Bergen. Every choice comes from that world: its materials, Norwegian craft, the fjord. Never start from "a nice modern website".
2. **Plan before you code.** In your status entry, write the tokens, type sizes and layout you will use for the section. A few lines are enough.
3. **Check the plan against the garbage list (§10).** If any part looks like something you would make for any other site, change it and write down why.
4. **Build with tokens only** (§3). No new hex values, font sizes or shadows.
5. **Critique with screenshots** at 360 px and 1280 px, comparing against this guide. Then remove the least necessary decoration (one thing) before you call it done, and say what you removed.

Spend boldness in **one** place, the material passport (§6.6). Everything around it stays quiet.

---

## 2. The idea: Patina

Good materials get better with age. Old malmfuru weathers to silver, oak darkens and copper turns green (verdigris, *irr*). Patina connects old wood, the retro look and sustainability in one idea. Every colour on the page is a material of the house:

- Plaster walls are the page ground.
- Tar-black is the ink.
- Oak is the workbench where facts sit.
- Petrol-green tile is the interior band.
- Copper is the fittings: **if it's copper, you can press it.**
- The footer is the steel base that carries everything.

"Modern retro Norwegian" here means 1950s–70s Norwegian craft:

- pine-panelled cabins;
- Cathrineholm and Figgjo enamel colours;
- stave-church malmfuru and tar;
- 19th-century wood type, revived in the 1950s.

All of it is laid out with modern calm: big photography, few words, generous space.

---

## 3. Tokens: copy these verbatim into `web/promo/src/styles/tokens.css`

```css
:root {
  /* Core material colours, sampled from images/ (PLAN §8.1) */
  --kalk: #ECEAE4;          /* lime plaster: page ground */
  --tjaere: #241A13;        /* pine tar: text, footer */
  --malmfuru: #9D5F30;      /* heartwood pine: large wood surfaces, numerals ≥ 24px */
  --eik: #BA936B;           /* oak: key facts band, spec table */
  --kobber: #A9481C;        /* copper: interactive on light grounds */
  --irr: #2C4F40;           /* petrol-green tile / verdigris: interior band */

  /* Support */
  --kobber-mork: #8E3B16;   /* copper hover (kalk text on it: 6.26:1) */
  --kobber-lys: #E08A52;    /* copper on dark bands (tjære, irr) only */
  --solvgra: #8C7E71;       /* weathered cladding: hairlines on kalk only */
  --malmfuru-mork: #6F3F1E; /* wood-toned text, captions on kalk */

  /* Roles */
  --bg: var(--kalk);
  --text: var(--tjaere);
  --text-soft: var(--malmfuru-mork);
  --line: var(--solvgra);
  --action: var(--kobber);
  --action-hover: var(--kobber-mork);
  --action-on-dark: var(--kobber-lys);

  /* Type */
  --font-display: "Besley", Georgia, "Times New Roman", serif;
  --font-text: "Jost", "Segoe UI", system-ui, sans-serif;
  --size-caption: 0.875rem;                               /* 14 */
  --size-small: 1rem;                                     /* 16 */
  --size-body: 1.125rem;                                  /* 18 */
  --size-lead: 1.3125rem;                                 /* 21 */
  --size-h3: 1.5rem;                                      /* 24 */
  --size-h2: clamp(1.75rem, 1.4rem + 1.6vw, 2.25rem);     /* 28 → 36 */
  --size-h1: clamp(2.75rem, 1.9rem + 3.8vw, 4.5rem);      /* 44 → 72 */
  --leading-text: 1.55;
  --leading-display: 1.08;
  --measure: 64ch;

  /* Space and shape */
  --space-1: 4px;  --space-2: 8px;  --space-3: 16px; --space-4: 24px;
  --space-5: 40px; --space-6: 64px; --space-7: 96px;
  --radius: 2px;
  --max-content: 1200px;
  --gutter: 24px;
  --focus-ring: 3px solid var(--kobber);
  --focus-ring-dark: 3px solid var(--kobber-lys);
  --focus-offset: 3px;

  /* Motion */
  --dur: 180ms;
  --ease: cubic-bezier(.2, .7, .2, 1);
}

@media (prefers-reduced-motion: reduce) {
  :root { --dur: 0ms; }
}
```

### Allowed colour pairs (measured, WCAG 2.x)

| Foreground / background | Ratio | Use it for |
|---|---|---|
| tjære / kalk | 14.17 | body text, inputs |
| kobber / kalk (both ways) | 4.81 | links, primary buttons, focus ring on light grounds |
| kalk / kobber-mørk | 6.26 | button hover |
| malmfuru-mørk / kalk | 7.26 | captions, soft text |
| tjære / eik | 6.07 | key facts, spec table, hairlines on eik |
| kalk / irr | 7.59 | text and links on the interior band |
| tjære / kobber-lys | 6.43 | buttons on dark bands |
| kobber-lys / tjære | 6.43 | links in the footer |
| kobber-lys button edge / irr | 3.45 | button shape and focus ring on irr: **no text in kobber-lys on irr** |
| malmfuru / kalk | 4.24 | numerals and display type ≥ 24 px only |
| sølvgrå / kalk | 3.27 | hairlines and borders only |

**Never use these pairs:**

- kobber on eik (2.06)
- kobber-lys on kalk (2.20)
- sølvgrå on eik (1.40)
- any text on malmfuru below 24 px
- the copper button anywhere on the eik band (that is why the form sits on kalk)

### Values allowed outside `tokens.css`

CSS custom properties don't work inside `@media`, and a few small values aren't worth a token. These are the only literals allowed:

- **Breakpoints:**
  - `48rem` (768 px): 4 columns become 12;
  - `64rem` (1024 px): the hero splits into text and image;
  - `80rem` (1280 px): section padding becomes `--space-7`.
  - No other breakpoints.
- **Line widths** of 1–3 px for borders, hairlines, underlines and outlines, plus `text-underline-offset: 3px`.
- **`letter-spacing: -0.01em`** on headings (§4).
- **`min-height: 48px`** on buttons, inputs and other touch targets.
- **Show and hide values:** transforms and `0` values that hide or reveal the skip link and the menu sheet.
- **The punched hole** in the passport tag: 10 px.
- **Layout units:** percentages, `fr` and aspect ratios.
- **Translucent colours,** but only through `color-mix()` with a token colour.

Anything else needs a token. If a value seems missing, ask in your status file rather than inventing one.

---

## 4. Typography

- **Besley** (display, weights 700–800) for h1–h3, the wordmark, journey numerals and the material names. Besley is a Clarendon revival, the 19th-century wood type: old-wood letters.
- **Jost** (text and UI, weights 400/500) for everything else.
- Self-host both as WOFF2 subsets that include `æøåÆØÅ × ² « »`. Don't load anything from the Google Fonts CDN. Preload Besley 800.
- Check Jost for `font-variant-numeric: tabular-nums`. If it isn't supported, set numbers in the facts table in Albert Sans and nowhere else.
- Body text is 18 px, line height 1.55, at most 64 characters per line. Headings use line height 1.08, `letter-spacing: -0.01em` and `text-wrap: balance`.
- Use sentence case everywhere. No `text-transform: uppercase`, no letter-spaced labels, no monospace anywhere.
- Headlines are one colour and one weight. Never put a single word of a headline in italics, colour or bold.
- Follow Norwegian conventions:
  - «guillemets» for quotes;
  - decimal comma (18,0 m²);
  - a space as the thousands separator (6 000 mm);
  - `ca.` for approximate values and `×` in dimensions;
  - `lang="nb"` / `lang="en"` on `<html>`.

---

## 5. Layout

- **Grid:** 12 columns from `48rem` up and 4 columns below it. At most 1200 px of content (`--max-content`), with `--gutter` gutters. **Side margins are `--gutter` (24 px) at every width.**
- **Alignment:** text is **left-aligned, ragged right**. Nothing is centred except the lightbox image.
- **Bands:** every section is a full-width band in one material colour:
  - kalk for reading sections;
  - eik for key facts;
  - irr for living and the bathroom;
  - tjære for the footer.
  - No two neighbouring bands share a colour, except kalk next to kalk with a sølvgrå hairline between them.
- **Spacing:** section padding is `--space-7` on desktop and `--space-6` on mobile. Use `--space-4` inside groups and `--space-5` between groups.
- **Images:** photos go edge to edge of their column, with square corners, no frames and no shadows.
- **Wireframes:** follow the hero, materials and journey wireframes in [PLAN.md §8.3](PLAN.md). Wireframes for the other sections come from Antigravity in `03-ideate/wireframes/`.
- **Reading order:** the page reads top to bottom, from roof to base. Follow the page map in [PLAN.md §8.6](PLAN.md).

---

## 6. Components

### 6.1 Actions
- **Primary button.**
  - Normal: `--kobber` background, `--kalk` text, Jost 500 at `--size-body`, padding `--space-3` × `--space-4` (16 × 24 px), `min-height: 48px`, `--radius`.
  - Hover: `--kobber-mork`. Focus: `--focus-ring` with `--focus-offset`.
  - No icon, no arrow, no shadow. The label says what happens: «Følg prosjektet».
- **On tjære or irr bands:** `--kobber-lys` background, `--tjaere` text and `--focus-ring-dark`.
- **Text link.** `--kobber` text, 1 px underline with a 3 px offset; on hover the underline becomes 2 px. On tjære, links are kobber-lys. On irr, links are kalk with a kobber-lys underline.
- Never append "→" or "»" to a link or button.

### 6.2 Header
- The wordmark is "MiniHouse" set in Besley 800 at `--size-h3`. It is text, not an image.
- Nav: Huset, Materialer, Flytting, Spørsmål. Jost 500 at `--size-small` in tjære. The current page gets a 2 px kobber underline and `aria-current`.
- On the right sits the primary button «Følg prosjektet». The language link («English» / «Norsk») is a plain text link.
- Mobile: a text button «Meny» opens a full-screen kalk sheet. Close it with «Lukk» or Esc, and return focus to the button.
- Add a skip link, «Hopp til innhold».

### 6.3 Captions
- Jost at `--size-caption` in `--malmfuru-mork`, **below** the image, never on top of it.
- Every image of the house carries «Konseptbilde» in Norwegian or «Concept image» in English.

### 6.4 Key facts (eik band)
- A `<dl>`: labels in Jost 500 at `--size-small`, values in Jost 400 at `--size-body` with tabular figures, all in tjære.
- Desktop: 5 columns separated by 1 px tjære hairlines. Mobile: label and value rows.
- No icons. Statuses are plain words, such as «under utvikling».

### 6.5 Gallery «Bilder» and lightbox
- **Panel wall:** on desktop, portrait 4:5 tiles side by side like vertical cladding boards, with `--space-2` gaps. Landscape renders get their own wide row.
- **Mobile:** a horizontal swipe strip with `scroll-snap` and a visible count, «3 av 12».
- Each tile is a `<button>` that opens the lightbox.
- **Lightbox:** a `<dialog>` with a `color-mix(in srgb, var(--tjaere) 92%, transparent)` backdrop and the image at `contain`, with its caption below.
  - Controls («Forrige», «Neste», «Lukk») in kobber-lys.
  - Esc closes it; arrow keys and swipe navigate.
  - Focus is trapped inside, and returns to the tile that opened it.

### 6.6 Material passport (*materialpass*), the signature element
- **Layout:** a texture sample (4:5) with its caption on the left, about a third of the content width. On the right: the material name in Besley 800 at `--size-h3`, one lead sentence, then the tag. On mobile the sample sits above, at 60 % width.
- **The tag** looks like a timber lot tag:
  - a 1 px sølvgrå edge and `--radius`;
  - a stub strip on the left, `--space-5` wide, cut off by a 1 px dashed sølvgrå perforation, with a 10 px eyelet (a 2 px sølvgrå ring) near the top. The hole lives in the stub so it can't be mistaken for a radio button;
  - the body: «Materialpass» in Jost 500 at `--size-small`, then a `<dl>` with the rows Materiale, Opprinnelse, Tidligere bruk, Brukes til, Behandling and Status;
  - labels in `--malmfuru-mork`, values in `--tjaere`, rows aligned on the text baseline and separated by spacing, not hairlines.
- **Built example:** `fase4/promo/reference/tile-a.html` and `tile-a.css`.
- **Values come from the content files.** When a value is unknown, the tag says so («dokumenteres per parti»). It never shows invented data or made-up lot numbers.
- **Order:** malmfuru, eik, kobber, stål, alternating left and right on desktop. On mobile the image sits above the text.
- **Later (P2), the patina toggle «Ny / 10 år / 100 år»:** a segmented control whose active state is kobber, with a crossfade of `--dur`.

### 6.7 Tabs «Utvendig / Konstruksjon»
- A WAI-ARIA tablist with arrow-key support.
- The active tab has a 3 px kobber underline. No pills, no boxes.

### 6.8 «Slik bor du i MiniHouse» (irr band)
- One large interior image (3:2), then the rooms (Kjøkken, Sittebenk, Oppbevaring, Bad) as image (4:3) plus a Besley title at `--size-h3` and two lines of Jost.
- All text is kalk.

### 6.9 Journey «Fra verksted til tomt» (kalk band)
- Three steps. Numerals 1, 2, 3 in Besley 800 at `--size-h1` in `--malmfuru`.
- Each step has an image (4:3) and one sentence.
- Desktop: 3 columns. Mobile: stacked.

### 6.10 Status and FAQ «Hvor langt har vi kommet?»
- One short paragraph on the real status.
- Then a list of the project phases from PROJECT.md, using honest words: done, in progress, not started.
- The FAQ uses `<details>`/`<summary>` with summaries in Jost 500 at `--size-lead` and a kobber «+» / «−» marker.

### 6.11 Follow form «Følg prosjektet» (on kalk, never on eik)
- **Purpose:** visitors leave an e-mail address to get updates about the project. MiniHouse isn't for sale (D10), so the form asks for nothing a sale would need.
- **Fields:** e-post (required), navn (optional). Collect nothing else.
- **Consent:** an unticked checkbox, «Ja, send meg oppdateringer om MiniHouse på e-post.», with a link to «Personvern». The privacy page says how often updates come and that every update has an unsubscribe link.
- **Submit:** the button repeats the action: «Følg prosjektet».
- Labels sit above the fields, with "(valgfritt)" on optional fields. Never use placeholder-only labels.
- Inputs: kalk background, 1 px tjære border, `--radius`, `min-height: 48px`.
- **Errors:**
  - Text in tjære, Jost 500, prefixed with «Feil:»; the field border becomes 2 px tjære.
  - Use `aria-invalid` and `aria-describedby`.
  - The message says how to fix it.
- **Success:** an irr band with kalk text, «Takk! Du følger nå prosjektet.» Then move focus to that message.

### 6.12 Footer, the steel base (tjære band)
- Contents: contact, «Personvern», «For fagfolk» (links to the docs site and the 3D lab) and the image note «Alle bilder er konseptbilder. Huset er under utvikling.»
- Text is kalk; links are kobber-lys.

### 6.13 Mobile sticky bar
- Appears after the hero has scrolled out of view, and hides while the form is visible.
- A kalk bar with a 1 px sølvgrå top border and a full-width primary button.
- Respects `env(safe-area-inset-bottom)`.

---

## 7. Images

- Show only the canonical house (`fase4/promo/canonical-house.md` and [PLAN.md §2](PLAN.md)). **Never** use the flat-roofed container renders.
- Every image is listed in `web/promo/src/content/images.json` with Norwegian and English alt text, a caption, its source, its status and a focal point.
- Aspect ratios:
  - hero 3:2;
  - the one large living-room image at the top of «Slik bor du i MiniHouse» 3:2 (§6.8);
  - gallery tiles 4:5;
  - the room images below it, and the journey images, 4:3;
  - textures 4:5;
  - Open Graph image 1200 × 630.
- No filters, duotones, grain overlays, vignettes, rounded corners, frames or text on images.
- Real photos of Carlos's actual reclaimed boards beat renders for the textures.
- The hero loads eagerly with `fetchpriority="high"`; everything else lazy-loads. Serve AVIF and WebP with `srcset`, and always set width and height.
- A build meant for release must contain no images with the status `stand-in` or `pending`.

---

## 8. Motion

Allowed, and nothing else:

- the lightbox and menu sheet opening and closing (opacity or transform, `--dur`);
- the tab panel swap (instant or a 120 ms fade);
- the patina crossfade (P2).

Never use scroll-triggered reveals, parallax, hover lifts, auto-playing carousels, count-up numbers or animated gradients. With `prefers-reduced-motion: reduce`, everything is instant.

---

## 9. Words (Norwegian Bokmål first)

- **Voice:** plain, concrete and short. Active voice and sentence case. No filler, and no exclamation marks except «Takk!».
- **English:** mirrors the meaning, not the words.
- **Actions keep one name through the whole flow.** Button «Følg prosjektet» → submit «Følg prosjektet» → success «Takk! Du følger nå prosjektet.» «Se alle bildene» opens the gallery.
- **Errors** say what happened and how to fix it, for example «Feil: Skriv inn en e-postadresse, for eksempel navn@epost.no.»
- **Every factual sentence has a row in [the claims register](PLAN.md)** (PLAN §12, later `02-define/claims-register.csv`). Status words: «konsept», «planlagt», «under utvikling», «ikke bestemt».
- **Banned words**, unless a specific, documented fact follows them:
  - Norwegian: *revolusjonerende, unik, drømmehjem, sømløs, innovativ, fremtidens, bærekraftig, miljøvennlig, grønn*.
  - English: *revolutionary, unique, dream home, seamless, elevate, discover, unlock, experience, eco-friendly, sustainable, green, game-changing*.
- **Never claim:** «ingen byggesøknad», «TEK17-godkjent», U-values, a price, a delivery time, a weight, «verifisert», «garantert», customer counts or testimonials.

---

## 10. The garbage list: never ship any of these

Each of these marks a page as generated or templated. Antigravity's visual review and DeepSeek's `check_promo.py` look for them.

**Look**

1. A cream background (near `#F4F1EA`) with a high-contrast serif and a terracotta accent. Our ground is chalk `--kalk`, and copper only marks interaction.
2. A near-black page with one neon accent.
3. Gradient washes, glassmorphism, blurred blobs, noise overlays and glowing borders.
4. A broadsheet look: hairline rules everywhere, dense newspaper columns.

**Layout**

5. The SaaS card kit: identical rounded cards, one radius on everything, the same grey shadow under each.
6. A hero made of a big number, a small label, three stats and a gradient.
7. Numbered markers (01 / 02 / 03) on things that aren't a sequence. Only the journey is numbered.
8. Centred paragraphs, or lines longer than 80 characters.

**Type and chrome**

9. Tracked-out ALL-CAPS eyebrow labels above headings, or any all-caps label.
10. Meta strings joined with middle dots (A · B · C), and labels styled "WORD — fragment".
11. `#111` / `#0B0B0B` as black. Our darkest colour is `--tjaere`.
12. Monospace for small labels or numbers.
13. "→" appended to links and buttons.
14. One word in a headline set in a different colour, italics or weight.

**Motion**

15. Fade-and-slide-up on every section, hover animations on every card, auto-rotating carousels.

**Images**

16. The container house, any image with text or UI baked in, mixed house designs, or a render without «Konseptbilde».
17. Stock photos of people, icons used as decoration, emoji in the UI.

**Copy and claims**

18. Hype words (§9), vague green claims, invented specs, prices or numbers, fake testimonials, "verified" badges.

**Accessibility**

19. Removed focus outlines, placeholder-only labels, text under 4.5:1 contrast, autoplaying video.

---

## 11. Definition of done (UI)

Before you call any section done, check every box in your status entry:

- [ ] Only tokens from `tokens.css`: no new hex values, font sizes, shadows or radii
- [ ] Only allowed colour pairs (§3); copper only on interactive elements
- [ ] All text comes from `nb.json` / `en.json`, nothing hard-coded, and both languages render
- [ ] Every image comes from `images.json`, with alt text and a caption
- [ ] Keyboard: every control can be reached in a logical order with a visible focus ring; Esc closes dialogs and sheets
- [ ] Reduced motion respected
- [ ] Screenshots at 360 px and 1280 px taken and looked at: no overflow, no single-word last lines in headings, no clipped focus rings
- [ ] Nothing from the garbage list (§10)
- [ ] One accessory removed in the final pass, and named
- [ ] Antigravity's visual review has no open *critical* or *serious* items for this section

---

## 12. How to review

Antigravity writes visual reviews to `fase4/promo/review/visual-review.md`. Anyone else who spots a problem puts it under "Requests" in their own status file. One entry per finding:

```text
### VR-012 · Hero · 360 px · serious
Screenshot: fase4/promo/05-test/screens/2026-11-18_hero_360.png
Rule: DESIGN-GUIDE §5 (left-aligned, measure ≤ 64ch)
What: the lead text is centred and runs to 74 characters per line.
Fix: left-align it and set max-width: var(--measure).
Owner: Cursor · Status: open
```

Severity:

- **critical** blocks launch;
- **serious** must be fixed before G5;
- **minor** should be fixed if there is time.

The owner fixes the issue and notes the commit or file in their own status file. Antigravity re-checks it and marks it closed.
