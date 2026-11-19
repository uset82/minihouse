# MiniHouse promo website · Design guide

**For every agent that designs, builds, writes or reviews the promo site: Antigravity, Cursor and DeepSeek, and Grok or WorkBuddy when a task brings them in.** Revision R2.5, 2026-11-19. Read this before you touch UI, copy or images. It holds the visual system, «Patina, made funkier» (G3), as rules you can check. [PLAN.md](PLAN.md) says what gets built and by whom.

**Built reference:** `fase4/promo/reference/` holds the look built by Claude Code to this guide: header, hero, key facts, the material passport, the irr band with the mirror frame, the journey with giant numerals, the copper follow band and the footer. Open `index.html` to see it at 360 px and 1280 px. When this guide and the reference seem to disagree, ask; don't guess.

**R2.5 changes, 2026-11-19:** Carlos's real photos and his Midtun film arrive (D16), and the landing page gets a review pass ([agents/task-landing-r3.md](agents/task-landing-r3.md)):

- §6.3: real photos carry what they show and who took it, never «Konseptbilde».
- §6.5: the gallery has 6 pictures, with two of the three mirror pictures out and the bathroom window in, and one note under the sheet instead of a caption under every tile.
- §6.6: from `64rem` the materials are shorter: narrower samples, and tags with two pairs per row.
- §6.12: the footer note and a «Historien» link.
- §6.16: the film and the photos of the old house. The home section gets the gable photo.
- §7: the rules for real photos.

**R2.4 changes, 2026-11-18:** Carlos asked for his story «Hvordan ideen oppstod» as its own page, in his own Norwegian, built by Grok and DeepSeek ([agents/task-story-page.md](agents/task-story-page.md)).

- §2.1 adds funk move 5: his question on a malmfuru band, on the story page only.
- §3: kalk type of 24 px and up may sit on malmfuru.
- §5 and §6.2: the story page's bands, the home page's new section and a fifth menu link.
- The new §6.16 describes the page.
- §9 lists his five sentences as the only exceptions to the banned words.

The same system, summarised in the DESIGN.md format, is in [web/promo/DESIGN.md](../../web/promo/DESIGN.md).

**R2.3 changes, 2026-11-18:** Carlos asked for «an automatic video presentation of the house» that is part of the whole site. The new §6.15 describes it:

- his concept film plays by itself, without sound, in the hero;
- its living-room and bathroom shots play in «Inne i MiniHouse», the bathroom inside the copper mirror;
- one pause button stops every film.

§6.8, §6.14, §7, §8 and §10 #19 changed with it.

**R2.2 changes, 2026-11-18:** four UX fixes Carlos approved («Yes, fix them»):

- §5: «Inne i MiniHouse» moves up, right after the key facts.
- §6.6: a compact two-column materials row below `64rem`.
- §6.7: both construction pictures are shown, and the tabs are gone.
- §6.2: «Huset» in the menu opens the gallery.

**R2.1 changes, 2026-11-18:** Claude Code built R2 in `web/promo` at Carlos's request ([its log](status/claude-code.md)), and these sections now describe the built page:

- §5: the hero bleed.
- §6.5: the contact-sheet gallery.
- §6.6: passports always visible, hanging off their samples.
- §6.7: the two-column build section.
- §6.8 and §6.14: the collage, with the mirror overlapping the photo.
- §6.9: the stand-in rule.
- §6.12: the footer wordmark.

**R2 changes, 2026-11-18:**

- The look is «Patina, made funkier» (G3), and there is no design-thinking process (D14). References to style tiles, wireframes and test rounds are gone.
- §2.1 adds the four funk moves. Copper still marks what you can press, with one exception: the mirror frame.
- §3 adds the token `--size-numeral` (the only token change), the copper-band pairs and the mirror-frame literals.
- §6.8 (irr band), §6.9 (journey) and §6.11 (follow form in the copper band) are rewritten, and §6.14 (mirror frame) is new.
- §10 says when a funk move is allowed.

Earlier revisions (R1.1–R1.3, 2026-11-17) set side margins to `--gutter`, listed the allowed literals, made the call to action «Følg prosjektet» and drew the passport as a timber tag.

The working method comes from the `frontend-design` skill that Carlos uses in Claude Code. The original is on this machine, read-only: `C:\Users\carlos\.claude\plugins\cache\claude-plugins-official\frontend-design\1.1.1\skills\frontend-design\SKILL.md`. This guide applies that method to MiniHouse. Where the two differ, this guide wins. `/frontend-design:frontend-design` exists only in Claude Code, so agents in other clients, such as Grok and DeepSeek, read that file directly. [web/promo/DESIGN.md](../../web/promo/DESIGN.md) is this guide's system in the DESIGN.md format (the "/design style").

---

## 1. The method: follow these steps in order, for every section

1. **Start from the subject.** MiniHouse is a small movable house built from old timber, with copper fittings and a steel base, made for Bergen. Every choice comes from that world: its materials, Norwegian craft, the fjord. Never start from "a nice modern website".
2. **Plan before you code.** In your status entry, write the tokens, type sizes and layout you will use for the section. A few lines are enough.
3. **Check the plan against the garbage list (§10).** If any part looks like something you would make for any other site, change it and write down why.
4. **Build with tokens only** (§3). No new hex values, font sizes or shadows.
5. **Critique with screenshots** at 360 px and 1280 px, comparing against this guide. Then remove the least necessary decoration (one thing) before you call it done, and say what you removed.

Boldness lives in a few named places: the material passport (§6.6) and the five funk moves (§2.1). Everything around them stays quiet.

---

## 2. The idea: Patina

Good materials get better with age. Old malmfuru weathers to silver, oak darkens and copper turns green (verdigris, *irr*). Patina connects old wood, the retro look and sustainability in one idea. Every colour on the page is a material of the house:

- Plaster walls are the page ground.
- Tar-black is the ink.
- Oak is the workbench where facts sit.
- Petrol-green tile is the interior band.
- Copper is the fittings: **if it's copper, you can press it.** The one exception is the mirror frame (§2.1).
- The footer is the steel base that carries everything.

"Modern retro Norwegian" here means 1950s–70s Norwegian craft:

- pine-panelled cabins;
- Cathrineholm and Figgjo enamel colours;
- stave-church malmfuru and tar;
- 19th-century wood type, revived in the 1950s.

All of it is laid out with modern calm: big photography, few words, generous space.

### 2.1 Made funkier

Carlos asked for a site that is modern and **funky**. The funk comes from five moves, and each one comes from a real material or object of the house:

| # | Move | Where it comes from | Where it's used | Spec |
|---|---|---|---|---|
| 1 | The wavy copper mirror frame, «speilramme» | the bathroom's wavy copper mirror | once: the bath photo in the irr band | §6.14 |
| 2 | A bold irr band | the petrol-green glazed bathroom tile | «Inne i MiniHouse» | §6.8 |
| 3 | Giant wood-type numerals | 19th-century wood type, cut in old wood | the journey's 1, 2 and 3 | §6.9 |
| 4 | A copper colour block | the copper fittings: the copper you press | the «Følg prosjektet» band, after D6 | §6.11 |
| 5 | A malmfuru colour block | the heartwood of the old boards that Carlos's story is about | once: his question on the story page (Carlos approved it with the story-page plan, 2026-11-18) | §6.16 |

Each move is used where the table says and nowhere else. A sixth move needs Carlos's OK and a new row here.

---

## 3. Tokens: copy these verbatim into `web/promo/src/styles/tokens.css`

```css
:root {
  /* Core material colours, sampled from images/ (PLAN §4) */
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
  --size-numeral: clamp(5rem, 3rem + 8vw, 9rem);          /* 80 → 144: journey numerals */
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
| kobber / kalk (both ways) | 4.81 | links, primary buttons, focus ring on light grounds; on the copper band: kalk text and links, the kalk focus ring, and kobber text on the inverted kalk button |
| kalk / kobber-mørk | 6.26 | button hover |
| malmfuru-mørk / kalk | 7.26 | captions, soft text |
| tjære / eik | 6.07 | key facts, spec table, hairlines on eik |
| kalk / irr | 7.59 | text and links on the interior band |
| tjære / kobber-lys | 6.43 | buttons on dark bands |
| kobber-lys / tjære | 6.43 | links in the footer |
| kobber-lys button edge / irr | 3.45 | button shape, focus ring and the mirror frame's stroke on irr: **no text in kobber-lys on irr** |
| malmfuru / kalk (both ways) | 4.24 | numerals and display type ≥ 24 px only, including the journey numerals; kalk type of 24 px and up on the story page's malmfuru band (§6.16) |
| sølvgrå / kalk | 3.27 | hairlines and borders only |

**Never use these pairs:**

- kobber on eik (2.06)
- kobber on irr (1.58): the mirror frame on irr is kobber-lys, never kobber
- tjære on kobber (2.95): on the copper band, all text is kalk, error messages included
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
- **The mirror frame's geometry** (§6.14): the path coordinates, in 0–1 units for the clip path and 400 × 500 units for the frame, and `stroke-width: 30` in those SVG units.
- **Layout units:** percentages, `fr` and aspect ratios.
- **Translucent colours,** but only through `color-mix()` with a token colour.

Anything else needs a token. If a value seems missing, ask in your status file rather than inventing one.

---

## 4. Typography

- **Besley** (display, weights 700–800) for h1–h3, the wordmark, the journey numerals (`--size-numeral`) and the material names. Besley is a Clarendon revival, the 19th-century wood type: old-wood letters.
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
  - kobber for the follow band, once D6 is decided;
  - malmfuru once, for Carlos's question on the story page (§6.16);
  - in page order: kalk hero, eik facts, irr «Inne i MiniHouse», kalk gallery, then the kalk sections (materials, the story section «Hvordan ideen oppstod», build, journey, status and FAQ), and the tjære footer ([content/sitemap.md](content/sitemap.md));
  - on the story page: the kalk opening, the malmfuru question band, the kalk story and ending, and the tjære footer;
  - tjære for the footer.
  - No two neighbouring bands share a colour, except kalk next to kalk with a sølvgrå hairline between them.
- **Spacing:** section padding is `--space-7` on desktop and `--space-6` on mobile. Use `--space-4` inside groups and `--space-5` between groups.
- **Images:** photos go edge to edge of their column, with square corners, no frames and no shadows. The one exception is the mirror frame (§6.14).
- **Hero:** from `64rem` the text keeps the content column and the house photo bleeds off the right edge of the screen. Below `64rem` the photo runs edge to edge, and its caption keeps the `--gutter` margin.
- **Layouts:** copy them from the reference in `reference/`, which shows every section with a fixed design at 360 px and 1280 px.
- **Reading order:** the page reads top to bottom, from roof to base, in the section order of [content/sitemap.md](content/sitemap.md).

---

## 6. Components

### 6.1 Actions
- **Primary button.**
  - Normal: `--kobber` background, `--kalk` text, Jost 500 at `--size-body`, padding `--space-3` × `--space-4` (16 × 24 px), `min-height: 48px`, `--radius`.
  - Hover: `--kobber-mork`. Focus: `--focus-ring` with `--focus-offset`.
  - No icon, no arrow, no shadow. The label says what happens: «Følg prosjektet».
- **On tjære or irr bands:** `--kobber-lys` background, `--tjaere` text and `--focus-ring-dark`.
- **On the copper band (inverted):** `--kalk` background and `--kobber` text; on hover the text turns `--tjaere`. The focus ring is 3 px solid `--kalk` with `--focus-offset`.
- **Text link.** `--kobber` text, 1 px underline with a 3 px offset; on hover the underline becomes 2 px. On tjære, links are kobber-lys. On irr, links are kalk with a kobber-lys underline.
- Never append "→" or "»" to a link or button.

### 6.2 Header
- The wordmark is "MiniHouse" set in Besley 800 at `--size-h3`. It is text, not an image.
- Nav: Huset, Materialer, Flytting, Spørsmål, Historien. Jost 500 at `--size-small` in tjære. «Huset» opens the gallery «Huset i bilder» (`#bilder`); the wordmark goes to the top. «Historien» («The story») opens Carlos's story page (§6.16) and carries `aria-current="page"` there. The link for the section in the address gets a 2 px kobber underline and `aria-current`; at the top of the page, none does.
- On the right sits the primary button «Følg prosjektet». Until D6 is decided there is nothing to follow, so the button isn't shown. The language link («English» / «Norsk») is a plain text link.
- Mobile: a text button «Meny» opens a full-screen kalk sheet. Close it with «Lukk» or Esc, and return focus to the button.
- Add a skip link, «Hopp til innhold».

### 6.3 Captions
- Jost at `--size-caption` in `--malmfuru-mork`, **below** the image, never on top of it.
- Every image of the house carries «Konseptbilde» in Norwegian or «Concept image» in English.
- **Real photos** (`kind: "photo"`, D16) carry what they show, then the credit: «Blyglassvinduet i lærerboligen. Foto: Joran Ingvaldsen» / "The stained-glass window in the residence. Photo: Joran Ingvaldsen". Never «Konseptbilde» on a photo, and never a photo without «Foto:».
- **The gallery** is the one exception to a caption under every picture: one note sits under the sheet (§6.5).

### 6.4 Key facts (eik band)
- A `<dl>`: labels in Jost 500 at `--size-small`, values in Jost 400 at `--size-body` with tabular figures, all in tjære.
- Desktop: 5 columns separated by 1 px tjære hairlines. Mobile: label and value rows.
- No icons. Statuses are plain words, such as «under utvikling».

### 6.5 Gallery «Bilder» and lightbox
- **A contact sheet.** From `48rem` the pictures sit in rows of equal height at their own proportions, with `--space-2` gaps. Each tile's `flex-grow` is its width-to-height ratio (`--ar`), so nothing is cropped or enlarged. The rows are fixed in `Gallery.astro`, and landscape and portrait alternate.
- **Pictures (R2.5):** meadow, shower and bench; then kitchen, bathroom window and storage. That's 6 in two rows of 3, each row landscape, portrait, landscape.
  - Out: the vanity (`bath-vanity`) and the doorway (`bath-doorway`), which both show the wavy copper mirror. It already shows in the hero film, the mirror frame (§6.14) and the copper sample, and a funk move needs scarcity. The shower is now the one gallery picture with the mirror.
  - The living-room photo isn't repeated here either, because the irr band shows it.
- **One note instead of 6 captions:**
  - Each tile keeps its «Konseptbilde» caption in the markup with `display: none`, because the lightbox reads its text.
  - A visually-hidden pattern would push the phone strip sideways, since the tiles aren't positioned.
  - Under the sheet: one line, `gallery.note` («Alle bildene her er konseptbilder.»), in Jost at `--size-caption` in `--text-soft`, `--space-3` below the last row.
- **Mobile:** one horizontal swipe strip with `scroll-snap` and a visible count, «3 av 6». Every tile is `calc(2 * var(--space-7) + var(--space-4))` high, landscape at 4:3 and portrait at 4:5.
- Each tile is a `<button>` that opens the lightbox.
- **Lightbox:** a `<dialog>` with a `color-mix(in srgb, var(--tjaere) 92%, transparent)` backdrop and the image at `contain`, with its caption below.
  - Controls («Forrige», «Neste», «Lukk») in kobber-lys.
  - Esc closes it; arrow keys and swipe navigate.
  - Focus is trapped inside, and returns to the tile that opened it.

### 6.6 Material passport (*materialpass*), the signature element
- **Always visible.** The passport is the signature element, so it's never folded behind a toggle.
- **Layout below `64rem`, one compact row per material:**
  - The sample (4:5) sits in a `2fr` column beside the material name (Besley 800 at `--size-h3`) and its lead in a `3fr` column, with a `--space-3` gap. The tag runs full width underneath.
  - **On phones** the tag is compact: a `--space-4` stub with the eyelet centred in it, `--space-3` padding, and one shared label column (`max-content`, using `subgrid`). Values and the material lead are set at `--size-small`, and materials are `--space-5` apart.
  - **From `48rem`:** the full tag (a `--space-5` stub, 2fr/3fr rows, values at body size), the lead at body size, and `--space-6` between materials.
  - On a 390 px phone the whole section is 2.7 screens, down from 4.3.
- **Layout from `64rem`, boards in a zig-zag:**
  - The columns are `3fr` sample, `7fr` words and tag, and `2fr` space, then the mirror image of it for the next material. The column gap is `--space-4`. (Until R2.5 they were `4fr 6fr 2fr`, and the section took 2.9 screens at 1280 × 900.)
  - The tag's `<dl>` shows two label–value pairs per row: Materiale and Opprinnelse, then Tidligere bruk and Brukes til, then Behandling and Status, with a `--space-4` gap between the pairs and `--space-1` between the rows.
  - Materials are `--space-5` apart from `64rem`.
  - At 1280 px, each material is at most 395 px tall and the section at most 2050 px. That's 21 % shorter than R2.4's 510 and 2584 px. The 3fr sample is 288 × 360 px, and with its caption, about 390 px is the floor.
  - Check 1024 px too: the value columns are narrow there, and «dokumenteres per parti» may wrap. Two lines are fine.
  - The tag's stub (`--space-5` wide) hangs over the edge of its sample, like a lot tag nailed to a board. The tag's text lines up with the material name.
  - In mirrored rows the stub and eyelet sit on the right. The tag has a kalk background.
  - The sample's caption keeps a `--space-5` padding on the stub's side, so a tag never covers it.
- **The tag** looks like a timber lot tag:
  - a 1 px sølvgrå edge and `--radius`;
  - a stub strip on the left, `--space-5` wide, cut off by a 1 px dashed sølvgrå perforation, with a 10 px eyelet (a 2 px sølvgrå ring) near the top. The hole lives in the stub so it can't be mistaken for a radio button;
  - the body: «Materialpass» in Jost 500 at `--size-small`, then a `<dl>` with the rows Materiale, Opprinnelse, Tidligere bruk, Brukes til, Behandling and Status;
  - labels in `--malmfuru-mork`, values in `--tjaere`, rows aligned on the text baseline and separated by spacing, not hairlines.
- **Built example:** `fase4/promo/reference/tile-a.html` and `tile-a.css`.
- **Values come from the content files.** When a value is unknown, the tag says so («dokumenteres per parti»). It never shows invented data or made-up lot numbers.
- **Order:** malmfuru, eik, kobber, stål, alternating left and right on desktop. On mobile the image sits above the text.
- **Later (P2), the patina toggle «Ny / 10 år / 100 år»:** a segmented control whose active state is kobber, with a crossfade of `--dur`.

### 6.7 «Under kledningen»: the outside and the construction, side by side
- No tabs: few people click a second tab, and the exploded drawing is the most interesting technical picture.
- Two views, stacked on phones and side by side from `48rem` (`--space-5` gap).
- Each view has its picture (3:2), an h3 in Besley 800 at `--size-h3` («Utvendig», «Konstruksjon»), and its sentence.
- Built in `web/promo/src/components/Build.astro`, which replaced `BuildTabs.astro` on 2026-11-18.

### 6.8 «Inne i MiniHouse» (irr band, funk move 2)
- **The wall of petrol-green tile.** A full-bleed `--irr` band. All text, captions included, is `--kalk`, and the focus ring is `--focus-ring-dark`.
- **Heading:** the h2 in Besley 800 at `--size-h1`, the largest heading on the page after the hero, then the lead sentence.
- **Pictures, now moving (§6.15):** the living-room shot of the concept film (3:2) with its caption row and pause button, and the bathroom shot inside the mirror frame (§6.14). Without the film media, the still photos `living` and `bath-window` take their places.
- **Position on the page:** right after the key facts, so the funky peak is the second screen.
- **Layout, a collage:**
  - From `64rem`, a 12-column grid with a `--space-4` gap. The heading and lead sit in columns 1–7, and the living film below them in columns 1–8. The mirror spans columns 8–12 over both rows, aligned to the bottom, so it hangs beside the heading and overlaps the film by one column.
  - Below `64rem`, stack the text and the living film. The mirror follows, right-aligned at 78 % width (60 % from `48rem`), with a `--space-4` gap and no overlap, so it never covers the film's pause button.
  - The mirror has `pointer-events: none`, because it holds nothing to press.
- **No room list.** The lead sentence names the rooms. The kitchen, bench, storage and shower pictures live in the gallery (§6.5).

### 6.9 Journey «Fra verksted til tomt» (kalk band, funk move 3)
- Three steps in an `<ol>`. Desktop: 3 columns from `48rem`. Mobile: stacked.
- **Giant numerals:** 1, 2 and 3 in Besley 800 at `--size-numeral`, in `--malmfuru` (4.24:1 on kalk), with `letter-spacing: -0.01em`. Each numeral is an `aria-hidden` span set above its photo with `margin-bottom: calc(-1 * var(--space-5))`, plus `position: relative` and `z-index: 1`, so it overlaps the photo's top edge like a stamp on a crate. The `<ol>` gives the order to screen readers.
- **Each step:** the numeral, then the photo at full column width (4:3), the title in Besley 800 at `--size-h3`, and one sentence.
- **Small stand-ins:** the workshop stand-in (288 × 144) is shown enlarged and looks soft until Carlos's render arrives (PLAN §7). That's acceptable in the preview only: a release build rejects stand-ins, and a release image is at least 1600 px wide.

### 6.10 Status and FAQ «Hvor langt har vi kommet?»
- One short paragraph on the real status.
- Then a list of the project phases from PROJECT.md, using honest words: done, in progress, not started.
- The FAQ uses `<details>`/`<summary>` with summaries in Jost 500 at `--size-lead` and a kobber «+» / «−» marker.

### 6.11 Follow form «Følg prosjektet» (copper band, funk move 4, after D6)
- **Build it only after D6** names the inbox and the form service. Until then, the section isn't on the page.
- **Purpose:** visitors leave an e-mail address to get updates about the project. MiniHouse isn't for sale (D10), so the form asks for nothing a sale would need.
- **The band:** a full-bleed `--kobber` band, the one large copper surface on the page. It's a copper colour block, because the whole band is the action. All text and links are `--kalk` (4.81:1), and the focus ring is 3 px solid `--kalk`. Never put tjære text on it (2.95:1).
- **Layout:** the h2 in Besley 800 at `--size-h1` and the lead on the left; from `64rem`, the form on the right (`minmax(0, 5fr) minmax(0, 6fr)`, gap `--space-6`). Below `64rem`, the form sits under the text.
- **Fields:** e-post (required), navn (optional). Collect nothing else.
- **Consent:** an unticked checkbox, «Ja, send meg oppdateringer om MiniHouse på e-post.», with a link to «Personvern». The privacy page says how often updates come and that every update has an unsubscribe link.
- **Submit:** the inverted button (§6.1) repeats the action: «Følg prosjektet».
- Labels sit above the fields, with "(valgfritt)" on optional fields. Never use placeholder-only labels.
- Inputs: kalk background, tjære text, 1 px tjære border, `--radius`, `min-height: 48px`.
- **Errors:**
  - Text in kalk, Jost 500, prefixed with «Feil:»; the field border becomes 2 px tjære.
  - Use `aria-invalid` and `aria-describedby`.
  - The message says how to fix it.
- **Success:** the form is replaced by «Takk! Du følger nå prosjektet.» in kalk at `--size-lead`. Then move focus to that message.

### 6.12 Footer, the steel base (tjære band)
- **Contents:**
  - the name «MiniHouse» in Besley 800 at `--size-h2`, like a maker's plate on the chassis;
  - contact;
  - the links «Historien» (first, since R2.5), «Personvern» and «For fagfolk» (the docs site and the 3D lab);
  - the image note «Bildene av MiniHouse er konseptbilder. Huset er under utvikling.»
- **The note changed in R2.5.** Until then it said «Alle bilder er konseptbilder». That is no longer true now that the story page shows real photos of the old house (D16).
- Padding `--space-6`. The name and note sit on the left, and the links on the right, aligned to the bottom.
- Text is kalk; links are kobber-lys.

### 6.13 Mobile sticky bar
- Mounted only once the follow form exists (D6).
- Appears after the hero has scrolled out of view, and hides while the form is visible.
- A kalk bar with a 1 px sølvgrå top border and a full-width primary button.
- Respects `env(safe-area-inset-bottom)`.

### 6.14 The mirror frame «speilramme» (funk move 1)
- **What it is:** the outline of the house's wavy copper bathroom mirror, used **once**, on the bath photo in the irr band (§6.8). It's the only copper on the page that you can't press, and the only framed photo.
- **The shape:** a closed, gently wavy oval in a 4:5 box. The path is drawn once and kept in `reference/tile-a.html` in two forms:
  - in 0–1 units for `<clipPath id="speilramme" clipPathUnits="objectBoundingBox">`, defined once per page in a hidden inline `<svg>`;
  - in 400 × 500 units for the frame overlay, `<svg viewBox="0 0 400 500" aria-hidden="true">`.
  - Copy both paths exactly. Don't redraw or scale them by hand.
- **The photo:** a portrait bath photo at 4:5 through the normal image pipeline, with `object-fit: cover` and `clip-path: url(#speilramme)`. Keep its subject inside the middle 80 %, so the wavy edge doesn't cut it. The alt text stays on the image.
- **The frame:** drawn on top with `fill: none`, `stroke: var(--kobber-lys)`, `stroke-width: 30`, `stroke-linejoin: round` and `overflow: visible`, so the stroke isn't cut off. On irr, kobber-lys measures 3.45:1, a clear shape. Plain kobber measures 1.58:1 and would disappear.
- **The caption** «Konseptbilde» sits below the frame in kalk, right-aligned under the shape, so it can't be read as a second caption for the living-room photo. This is the one right-aligned text on the page.
- **Film mode:** with `film="bath"`, the bathroom shot of the concept film plays inside the same clipped shape, above its still frame. The still carries the alt text, and the shared film controller plays and pauses it (§6.15). The caption then reads «Konseptfilm».
- **Built in** `web/promo/src/components/MirrorFrame.astro`.
- **No motion of its own.** The frame doesn't wobble, rotate or animate; only the film inside it moves.

### 6.15 The concept film «Konseptfilm» (Carlos, 2026-11-18)
- **What it is:** Carlos's own walkthrough of the house, `images/minihouse_walkthrough_v18_4k.mp4` (3840 × 2160, 24 fps, 17.04 s, five shots cut at 4.04, 7.04, 10.54 and 14.54 s: the hillside, the living room, the bed, the bathroom and a wide bathroom view). It's a rendered concept, never a recording of a built house: caption «Konseptfilm» (claim K-35).
- **Where it plays:**
  - the whole film in the hero, instead of the photo, at 16:9, because the house is too wide for a 4:5 phone crop;
  - the living-room shot in «Inne i MiniHouse»;
  - the bathroom shot inside the copper mirror.
  - **On the story page (R2.5),** Carlos's Midtun film (§6.16) plays with the same rules and the same shared button. It isn't a concept film, so its caption credits Carlos.
  - Everything else stays still.
- **The cuts:** `scripts/cut_film.py` (ffmpeg) makes them from the master, which is never changed. It reads the master's width and height with ffprobe, so the 3:2 and 4:5 crops land on the same subjects at any resolution. They are silent H.264 with `+faststart` and a GOP of 48.

  | File | Size | Length | Loop |
  |---|---|---|---|
  | `house-film-1920.mp4` | 1920 × 1080, 3.94 MB | 16.54 s | a 0.5 s crossfade at the seam; screens from `64rem` |
  | `house-film.mp4` | 1280 × 720, 2.40 MB | 16.54 s | a 0.5 s crossfade at the seam; smaller screens |
  | `living-loop.mp4` | 1440 × 960, 1.04 MB | 5.67 s | forward and back |
  | `bath-loop.mp4` | 1080 × 1350, 1.14 MB | 7.00 s | forward and back |
  | `midtun-film-1920.mp4` (R2.5, story page) | 1920 × 1080, at most 14 MB | about 71.9 s | a 0.5 s crossfade at the seam; screens from `64rem` |
  | `midtun-film.mp4` (R2.5, story page) | 1280 × 720, at most 8 MB | about 71.9 s | a 0.5 s crossfade at the seam; smaller screens |

  **The Midtun cuts** come only from Carlos's clean master, `images/midtun_teachers_residence_clean_4k.mp4` (no burned-in titles, D16), at 30 fps with a GOP of 60. The command is `python scripts/cut_film.py midtun`, which never re-encodes the house cuts. Their sizes go in this table once they're made.

  The posters are the first frame of each film's largest cut, so the hero poster comes from the 1920 cut (402 KB; the loops are 236 KB and 122 KB). The script refuses a master whose length differs from 17.04 s; re-check the shot times if the master changes.
- **The sharper desktop film:** the hero `<video>` carries `data-film-src-wide`, and the controller loads `house-film-1920.mp4` when `matchMedia('(min-width: 64rem)')` matches. The living and bath loops keep one file each; nothing else in the shared controller changes.
- **Markup (`Film.astro`):**
  - the still is a normal responsive `<Picture>` with the alt text (`film.alt`, `film.livingAlt`, `film.bathAlt`);
  - the `<video muted playsinline loop preload="none">` lies on top with `aria-hidden="true"`, and only shows once it plays, so a loading video never covers the still with black.
- **One pause for every film:**
  - The caption row holds «Konseptfilm» and a copper text button, «Pause filmen» / «Spill av filmen», at least 48 px high. It's never on the picture.
  - Any button pauses or plays every film, and the choice is kept in `sessionStorage` for the tab, with no cookie (D9).
  - The mirror has no button of its own: the living film's button sits beside it.
- **When it plays (`src/scripts/film.ts`):**
  - It plays by itself unless the visitor prefers reduced motion, has Data Saver on, or paused it earlier in the tab.
  - If the browser refuses autoplay, the still stays and the button offers «Spill av filmen».
  - Nothing loads before the window's `load` event; a film loads only when it comes within a quarter screen, and films off screen or in a hidden tab are paused.
- **Release:** `films.json` holds each cut's status, and a release build fails until Carlos approves them at G4, as with the images. The host must answer byte-range requests (206), which Safari needs for video. Canner's built-in static server doesn't, so the upload is `npm run bundle`, which adds `web/promo/deploy/serve.mjs`: byte ranges, `video/mp4` and `image/avif` types, a real 404, and no dotfiles.

### 6.16 Carlos's story «Hvordan ideen oppstod» (story page, funk move 5)

- **What it is:** Carlos's own account of how MiniHouse started, on a page of its own: `/historien/`, and `/en/historien/` in English.
  - His Norwegian ([agents/task-story-page.md](agents/task-story-page.md), Appendix A) is published as he wrote it, and the English follows his English.
  - It's signed «Av Carlos» / "By Carlos".
  - The words are the `story.*` group in `nb.json` / `en.json`. The page is built in `web/promo/src/components/Story.astro` and `src/styles/story.css`.
- **The idea since R2.5: the first life, then the second.** Carlos's film and photos (D16) show the old teachers' residence for real: its first life, before the question. The MiniHouse concept images come after the question, as the second life, and the house appears at the end as the payoff of the motto: old materials, new homes. (Before R2.5 the page opened in type only, because it had no pictures of the old house.)
- **One loud moment: the question on the old wood.** «Hvorfor skal materialenes levetid ta slutt bare fordi bygningen de kommer fra, blir revet?» sits on a full-bleed `--malmfuru` band, the heartwood of the boards the story is about (funk move 5, §2.1). Everything else on the page stays quiet.
- **Top to bottom:**
  1. **The opening (kalk).**
     - The h1 `story.title` in Besley 800 at `--size-h1`.
     - The byline `story.byline` in Jost 500 at `--size-small` in `--malmfuru-mork`.
     - The lead `story.lead` in Jost 400 at `--size-lead`.
     - Then `story.intro[0]`, the sentence that names the house.
     - **The Midtun film (R2.5)**, full bleed, outside the text column:
       - Carlos's clean film (D16), 16:9, through `Film.astro` (`id="midtun"`), silent and looping, controlled by the shared «Pause filmen» button (§6.15);
       - its caption row (`story.film.caption`, then the button) lines up with the content column;
       - `--space-6` above and below;
       - its still frame loads eagerly, because it's in the first screen on desktop.
     - Then `story.intro[1]` («Det var en vakker, gammel bygning …»).
     - **The trio (R2.5):** the stained-glass window, the stove and the stone slabs, across the full content width (not the text column):
       - from `48rem`, in one row at their own proportions (3:2, 3:4, 3:2), all the same height, `--space-2` apart;
       - below `48rem`, stacked at their own proportions;
       - `--space-6` above and below.

       They belong here, with the old building's character. After the question they would read as MiniHouse materials (K-37).
     - Then `story.intro[2]`, and the reference line: `story.reference.label` followed by a copper text link (`story.reference.link`), external, in the same tab, with no icon.
     - Then `story.noticed[]`, whose last sentence ends in a colon and leads into the band.
       - **Between `noticed[1]` and `noticed[2]`, the timber pair (R2.5):** the 1887 board and the old nail, both 3:2, side by side from `48rem` across the full content width (not the text column), `--space-4` apart, and stacked below `48rem`, with `--space-6` above and below.
     - The text sits in columns 1–8 from `64rem` and is never wider than `--measure`.
  2. **The question band (malmfuru), full bleed.**
     - `story.question` in Besley 800 in `--kalk`, at `--size-h2` below `48rem` and `--size-h1` from `48rem`, with `--leading-display`, `letter-spacing: -0.01em` and `text-wrap: balance`, in columns 1–10.
     - Under it, `story.questionFollow` in Jost 500 at `--size-h3` in `--kalk`, in columns 1–8.
     - Kalk on malmfuru measures 4.24:1, so **no text on the band is under 24 px**, and nothing on it can be focused or pressed.
     - Padding `--space-6`, and `--space-7` from `80rem`. Both texts are paragraphs, not headings.
  3. **The idea (kalk).**
     - `story.origin` at `--size-lead`.
     - Then the three `story.sections[]`, each an h2 in Besley 800 at `--size-h2` followed by its paragraphs.
     - In the first section, the drawing `exploded` (3:2) sits beside the text from `64rem` (text in columns 1–7, picture in 8–12) and under it on smaller screens, with «Konseptbilde» below it.
     - From here on, only concept images: the second life. No real photo comes after the question band.
  4. **The ending (kalk).**
     - The house, `hero-slope`, at 3:2 in columns 1–8 from `64rem` (the `wide` size, up to 800 px) and full width below, lazy-loaded, with «Konseptbilde» below.
     - Then `story.closing` at `--size-lead`.
     - Then `story.motto[]` as a stack of short lines, one per line, in Besley 800 in `--tjaere`, at `--size-h2` below `48rem` and `--size-h1` from `48rem`, like the question. At `--size-h1` on a 360 px phone, «Gamle materialer.» breaks onto two lines (CR-23).
     - On phones the h1 «Hvordan ideen oppstod» stacks one word per line. That's accepted: it's a three-word stack, not a lone last word, so the h1 keeps `--size-h1`.
     - Last, the primary button `story.cta` («Se huset») to `/#bilder` (English: `/en/#bilder`): the same words and action as the hero's.
  5. **The footer,** as on every page.
- **Body text** follows §4: Jost at 18 px, line height 1.55, `--space-4` between paragraphs and `--space-6` before each h2. It's left-aligned and ragged right.
- **Long Norwegian compounds:** below `48rem`, the h2s use `hyphens: auto`, so «Fra rivningsmaterialer til beredskapsboliger» breaks at the compound joints instead of leaving «Fra» and «til» alone on their lines (CR-24). The page is `lang="nb"`, so the browser's Bokmål dictionary applies.
- **The home section «Hvordan ideen oppstod»** (`StoryTeaser.astro`), right after «Gammelt tre, nytt hus»:
  - a kalk band with a sølvgrå hairline above;
  - the h2 `story.teaser.title` in Besley 800 at `--size-h2`;
  - one or two sentences, `story.teaser.body`, at `--size-lead` in columns 1–7;
  - the copper text link `story.teaser.link` («Les historien») to the story page;
  - **since R2.5, Carlos's gable photo** (`midtun-gable`, 4:5, «Lærerboligen under rivingen, april 2026. Foto: Carlos»): columns 9–12 from `48rem`, top-aligned with the h2, with the text in columns 1–7; below `48rem`, under the link at full width. It's the one real photo on the home page.

  No band colour. It names no emergency use (D11).
- **The header** gets a fifth link, «Historien» (§6.2).
- **Markup:**
  - one h1; the story is an `<article>` with h2 sections;
  - the question, the follow-up and the motto are `<p>` elements;
  - pictures come through `Figure.astro` (`ratio="wide"`), with the alt text and captions from `images.json`;
  - the photo pair and the trio render only when their photos resolve, as `Gallery.astro` does, so a missing master never leaves an empty gap. Without the film or the photos, the text columns still sit `--space-4` apart;
  - the page has its own `<title>` and description (`story.meta`), and `hreflang` points to its twin.
- **Never on this page:**
  - a drop cap or giant initial (wood-type giants belong to the journey, move 3);
  - numbered markers or a timeline;
  - a quote card with big quotation marks;
  - stats, icons or emoji;
  - the irr band, or the house film (the Midtun film is this page's film);
  - italics or colour for emphasis;
  - pictures from other sites, and photos showing people or number plates (D16);
  - text burned into the film (D16: the clean version only);
  - generated images;
  - scroll effects.
- **Claims:** the story says Carlos saw how good the old timber was. It never says MiniHouse uses timber from Øvsttunvegen, and nothing on the site may imply it. Reclaimed timber stays out of the load-bearing structure (K-06). Emergency housing appears on this page only (D11 as amended).

---

## 7. Images

- Show only the canonical house (`fase4/promo/canonical-house.md` and [PLAN.md §2](PLAN.md)). **Never** use the flat-roofed container renders.
- Every image is listed in `web/promo/src/content/images.json` with Norwegian and English alt text, a caption, its source, its status and a focal point.
- Aspect ratios:
  - the hero film 16:9 (the still `hero-slope` at 3:2 only when the film media is missing);
  - the living-room film in «Inne i MiniHouse» 3:2, and the bath film in the mirror frame 4:5 (§6.8, §6.14, §6.15);
  - gallery tiles at their own proportions from `48rem`, and 4:3 or 4:5 in the phone strip (§6.5);
  - the journey images 4:3;
  - textures 4:5;
  - Open Graph image 1200 × 630.
- No filters, duotones, grain overlays, vignettes, rounded corners, frames or text on images. The mirror frame (§6.14) is the one frame.
- Real photos of Carlos's actual reclaimed boards beat renders for the textures.
- **Real photos (R2.5, D16)** appear only when Carlos has cleared them.
  - Today that means his phone photos and Joran Ingvaldsen's four, and only of the old residence.
  - They are `kind: "photo"` in `images.json`, with a caption that says what they show and «Foto: …» (§6.3).
  - **Their file data is removed** on the site copies: EXIF, camera, name, phone number and place. The site copy is at most 2400 px on its long side.
  - **Never:** photos from other sites, photos where a person can be recognised, or a readable number plate.
- The hero loads eagerly with `fetchpriority="high"`; everything else lazy-loads. Serve AVIF and WebP with `srcset`, and always set width and height.
- A build meant for release must contain no images with the status `stand-in` or `pending`.
- **The film** (§6.15): the cuts are in `web/promo/public/film/`, the posters in `web/promo/src/assets/film/`, and the list in `web/promo/src/content/films.json`. They are media, so they stay out of git.

---

## 8. Motion

Allowed, and nothing else:

- the lightbox and menu sheet opening and closing (opacity or transform, `--dur`);
- the films (§6.15, and the Midtun film on the story page, §6.16). They're the only things that move by themselves: silent and looping, with a pause button beside them. They never play under reduced motion or Data Saver;
- the patina crossfade (P2).

Never use scroll-triggered reveals, parallax, hover lifts, auto-playing carousels, count-up numbers or animated gradients. With `prefers-reduced-motion: reduce`, everything is instant.

---

## 9. Words (Norwegian Bokmål first)

- **Voice:** plain, concrete and short. Active voice and sentence case. No filler, and no exclamation marks except «Takk!».
- **English:** mirrors the meaning, not the words.
- **Actions keep one name through the whole flow.** Button «Følg prosjektet» → submit «Følg prosjektet» → success «Takk! Du følger nå prosjektet.» «Se alle bildene» opens the gallery.
- **Errors** say what happened and how to fix it, for example «Feil: Skriv inn en e-postadresse, for eksempel navn@epost.no.»
- **Every factual sentence has a row in [the claims register](content/claims-register.csv).** Status words: «konsept», «planlagt», «under utvikling», «ikke bestemt».
- **Banned words**, unless a specific, documented fact follows them:
  - Norwegian: *revolusjonerende, unik, drømmehjem, sømløs, innovativ, fremtidens, bærekraftig, miljøvennlig, grønn*.
  - English: *revolutionary, unique, dream home, seamless, elevate, discover, unlock, experience, eco-friendly, sustainable, green, game-changing*.
- **Never claim:** «ingen byggesøknad», «TEK17-godkjent», U-values, a price, a delivery time, a weight, «verifisert», «garantert», customer counts or testimonials.
- **Carlos's signed story** (§6.16) is published as he wrote it.
  - His five sentences with «bærekraftig», "sustainable" or "experience" are the only exceptions to the banned words. They're listed in the claims register as his own view, and `check_promo.py` allows them on the story page and nowhere else (Carlos: «Keep my words», 2026-11-18).
  - Emergency housing («beredskapsboliger») appears only on that page (D11 as amended).

---

## 10. The garbage list: never ship any of these

Each of these marks a page as generated or templated. Antigravity's visual review and DeepSeek's `check_promo.py` look for them.

**Look**

1. A cream background (near `#F4F1EA`) with a high-contrast serif and a terracotta accent. Our ground is chalk `--kalk`, and copper only marks interaction.
2. A near-black page with one neon accent.
3. Gradient washes, glassmorphism, blurred blobs, noise overlays and glowing borders. The mirror frame isn't a blob: it traces a real object in the house, it has a hard copper edge, and it's used once.
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

19. Removed focus outlines, placeholder-only labels, text under 4.5:1 contrast, video that autoplays with sound or without a pause button beside it.

**Funk**

20. Funk without a source: a wavy shape, a giant number or a colour block that doesn't come from a material or object of the house. A funk move used twice, or outside the place §2.1 gives it, is decoration and goes on this list.

---

## 11. Definition of done (UI)

Before you call any section done, check every box in your status entry:

- [ ] Only tokens from `tokens.css`: no new hex values, font sizes, shadows or radii
- [ ] Only allowed colour pairs (§3); copper only on interactive elements, the copper band and the one mirror frame
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
Screenshot: fase4/promo/qa/screens/2026-11-18_hero_360.png
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
