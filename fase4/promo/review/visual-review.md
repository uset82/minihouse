# Visual review

## Concept landing page after D13 · 2026-11-17

Reviewed the rebuilt local site on port 4322 in Bokmål and English. The 1536 × 1024 exterior shows the complete dark gable, weathered timber and lit interior on desktop and phone. The oak-coloured facts band leads into a gallery of the room, bathroom and exterior. The material section shows the grain of old wood, the window board, copper-coloured mirror and dark base in context.

| View | Bokmål | English |
| --- | --- | --- |
| 360 px | [Opening](../qa/screens/landing-concept/nb-360.jpg) | [Opening](../qa/screens/landing-concept/en-360.jpg) |
| 768 px | [Opening](../qa/screens/landing-concept/nb-768.jpg) | [Opening](../qa/screens/landing-concept/en-768.jpg) |
| 1280 px | [Opening](../qa/screens/landing-concept/nb-1280.jpg) | [Opening](../qa/screens/landing-concept/en-1280.jpg) |
| 1920 px | [Opening](../qa/screens/landing-concept/nb-1920.jpg) | [Opening](../qa/screens/landing-concept/en-1920.jpg) |

The browser decoded all 18 in-page images in each of the eight viewport and language combinations. The page width matched the viewport in every case. Both the narrow and wide gallery crops keep the subjects visible. The captions sit below the individual illustrations and identify the material references as concept images. [Phone gallery](../qa/screens/landing-concept/en-360-gallery.jpg) · [Desktop interior](../qa/screens/landing-concept/en-1280-inside.jpg) · [Pine](../qa/screens/landing-concept/en-1280-material.jpg) · [Oak](../qa/screens/landing-concept/en-1280-oak.jpg) · [Copper](../qa/screens/landing-concept/en-1280-copper.jpg)

**VR-01 closed.** The local build shows the corrected exports. The 292 × 182 px workshop panel is the only indoor workshop source in the project artwork. Its 288 × 144 px detail keeps the overhead beams and timber in view. On both language pages the detail measured approximately 106 × 53 CSS px at 360, 224 × 112 at 768 and 288 × 144 at 1280 and 1920. The three steps keep their own supplied workshop, truck and site views. The workshop stand-in still needs a larger original for a future full-size or high-density rendition. [Workshop on desktop](../qa/screens/landing-concept/en-1280-journey.jpg) · [Workshop on a phone](../qa/screens/landing-concept/en-360-journey.jpg)

**Mobile follow control closed.** A floating follow button appeared in an intermediate phone build. Cursor removed it. On the final English and Bokmål 360 px pages, the bottom of the material section is unobstructed and the document contains zero links to the unavailable follow form. [Final copper detail on a phone](../qa/screens/landing-concept/en-360-copper.jpg)

## Full Site Review · Sections 1–10 & Privacy · 2026-11-17

Preview: `http://127.0.0.1:4322/` and `http://127.0.0.1:4322/en/` (plus `/personvern` and `/en/personvern`).
Reviewed against DESIGN-GUIDE §3–§11, PLAN §8.3 and §6 at 360, 768, 1280 and 1920 px in both Norwegian and English.

Screenshots archived in [05-test/screens/review/](../qa/screens/review/):
- Norwegian home: [360 px](../qa/screens/review/nb-360.png), [768 px](../qa/screens/review/nb-768.png), [1280 px](../qa/screens/review/nb-1280.png), [1920 px](../qa/screens/review/nb-1920.png)
- English home: [360 px](../qa/screens/review/en-360.png), [768 px](../qa/screens/review/en-768.png), [1280 px](../qa/screens/review/en-1280.png), [1920 px](../qa/screens/review/en-1920.png)
- Norwegian privacy: [360 px](../qa/screens/review/personvern-nb-360.png), [1280 px](../qa/screens/review/personvern-nb-1280.png)
- English privacy: [360 px](../qa/screens/review/personvern-en-360.png), [1280 px](../qa/screens/review/personvern-en-1280.png)

Findings: **0 critical, 0 serious, 1 minor (rebuild to display new images).**

---

### Detailed Section Audit

1. **Header (DESIGN-GUIDE §6.2):**
   - Wordmark: "MiniHouse" in Besley 800 at `--size-h3`.
   - Nav (desktop): Huset, Materialer, Flytting, Spørsmål, English. Jost 500 in tjære.
   - Action: Primary button «Følg prosjektet» in `--kobber` with `--kalk` text (4.81:1).
   - Mobile: Nav hidden behind «Meny» button. Opens full-screen kalk sheet; Esc closes and returns focus to Meny.
   - Skip link: «Hopp til innhold» present at top.

2. **Hero (PLAN §8.3 & D12):**
   - Title matches D12: «Et lite hus, laget for å flyttes.» / "A small house, made to be moved." in Besley 800.
   - Lead in Jost 400.
   - Actions: Primary button «Følg prosjektet» and text link «Se alle bildene».
   - Desktop (1280 & 1920 px): Split layout with text on left and image container bleeding to the right edge.
   - Caption: «Konseptbilde» / «Concept image» positioned below image.

3. **Key Facts (DESIGN-GUIDE §6.4):**
   - Full-width eik band (`#BA936B`), tjære text (`#241A13`, contrast 6.07:1).
   - Mobile: Stacked label/value rows.
   - Desktop: 5 columns separated by 1 px tjære hairlines. Tabular figures for numbers.

4. **Bilder / Gallery & Lightbox (DESIGN-GUIDE §6.5):**
   - Mobile: Horizontal scroll-snap strip with visible count «1 av 10».
   - Desktop: Panel wall of 4:5 vertical board tiles side by side with `--space-2` gaps, plus wide 16:9 landscape row.
   - Lightbox: `<dialog>` on `color-mix(in srgb, var(--tjaere) 92%, transparent)`, contained image, `--kobber-lys` controls, Esc closes, arrow keys navigate, focus trapped and returned on close.

5. **Slik er det bygget / BuildTabs (DESIGN-GUIDE §6.7):**
   - WAI-ARIA tablist: `Utvendig` and `Konstruksjon`.
   - Active tab marked with 3 px kobber underline. Arrow keys navigate tabs.
   - Clean 4:3 diagram display with caption below.

6. **Gammelt tre, nytt hus / Materialpass (DESIGN-GUIDE §6.6):**
   - All 4 materials implemented: Malmfuru, Europeisk eik, Kobber, Stål.
   - Alternating layout on desktop (sample left/right).
   - Timber lot tag: 1 px sølvgrå border, `--space-5` stub on left with 10 px circular eyelet ring, 1 px dashed perforation border.
   - Tag body: «Materialpass» in Jost 500 at `--size-small`, `<dl>` with 6 rows (Materiale, Opprinnelse, Tidligere bruk, Brukes til, Behandling, Status). All data strictly from `nb.json` / `en.json`.

7. **Slik bor du i MiniHouse / Living (DESIGN-GUIDE §6.8):**
   - Full-width heldekkende `--irr` band (`#2C4F40`) with `--kalk` text (`#ECEAE4`, contrast 7.59:1).
   - Large 3:2 living image at top.
   - 4 room cards: Kjøkken, Sittebenk, Oppbevaring, Bad, each with 4:3 image, Besley 700 title, and Jost description.

8. **Fra verksted til tomt / Journey (PLAN §8.6, revised 2026-11-17 23:44):**
   - 3 steps: 1. Verksted, 2. Transport, 3. Tomt.
   - Numerals set in Besley 800 at `--size-h1` in `--malmfuru` (`#9D5F30`).
   - Native image framing verified: `workshop` master displayed at 288×144 px without awkward enlargement; `truck` displayed at 192×144 px; `plot` displayed at 256×144 px.
   - At 1280 px desktop, all three images share a uniform 144 px height across the band with their natural aspect ratios intact.
   - At 360 px mobile, each picture sits beside the step numeral and sentence at 106 px wide.
   - Zero horizontal overflow (`scrollWidth == innerWidth`).
   - Screenshots: [journey-1280.png](../qa/screens/qa/journey-1280.png) · [journey-360.png](../qa/screens/qa/journey-360.png).

9. **Status & FAQ (DESIGN-GUIDE §6.10):**
   - Status: Clean text-based phase list showing completed, in-progress, and planned milestones without ruled table clutter.
   - FAQ: Native `<details>` and `<summary>` elements with copper +/− indicator. Accessible without JS.

10. **Bunntekst som stålbase / Footer (DESIGN-GUIDE §6.12):**
    - Full-width `--tjaere` band (`#241A13`), light text, `--kobber-lys` links (`#E08A52`, contrast 6.43:1).
    - Disclaimer: «Alle bilder er konseptbilder. Huset er under utvikling.»
    - Links: Personvern, For fagfolk (docs site and lab), language switch.

11. **Personvern / Privacy Page (PLAN §9.2 4.12):**
    - Clean dedicated routes `/personvern` and `/en/personvern`.
    - Single measured reading column on `--kalk` with Besley 800 heading and Jost body.

12. **Garbage-list check (DESIGN-GUIDE §10):**
    - Zero badges, zero pill buttons, zero drop shadows, zero tracked all-caps, zero arrows on links.

---

### Findings

- **VR-01 · Rebuild preview for newly delivered images (minor):**
  - Preview rebuilt by Cursor in C-8; all 18 in-page images decode and display cleanly.
  - Owner: Cursor · Status: **closed 2026-11-17**.

- **VR-02 · Mobile follow action, closed for D13.** The fixed follow control has no destination while D6 is open. The mobile landing page directs visitors to the house and materials. Revisit follow navigation when a working subscription destination is available.

---

## Full Visual QA & Accessibility Audit (Task A-10) · 2026-11-17

Automated and manual visual verification conducted using headless Chromium via Playwright against the local preview on `http://127.0.0.1:4322/`.

Screenshots archived in [05-test/screens/qa/](../qa/screens/qa/):
- **Responsive Breakpoints:**
  - Norwegian Home: [360 px](../qa/screens/qa/nb-home-360px.png) · [768 px](../qa/screens/qa/nb-home-768px.png) · [1280 px](../qa/screens/qa/nb-home-1280px.png) · [1920 px](../qa/screens/qa/nb-home-1920px.png) · [Full-page 1280](../qa/screens/qa/nb-home-1280px-full.png)
  - English Home: [360 px](../qa/screens/qa/en-home-360px.png) · [768 px](../qa/screens/qa/en-home-768px.png) · [1280 px](../qa/screens/qa/en-home-1280px.png) · [1920 px](../qa/screens/qa/en-home-1920px.png) · [Full-page 1280](../qa/screens/qa/en-home-1280px-full.png)
  - Privacy (/personvern): [Norwegian 360 px](../qa/screens/qa/nb-personvern-360px.png) · [Norwegian 1280 px](../qa/screens/qa/nb-personvern-1280px.png) · [English 360 px](../qa/screens/qa/en-personvern-360px.png) · [English 1280 px](../qa/screens/qa/en-personvern-1280px.png)
  - 404 Route (/nonexistent): [404 360 px](../qa/screens/qa/404-360px.png) · [404 1280 px](../qa/screens/qa/404-1280px.png)
- **Reflow & Zoom (WCAG 1.4.10):**
  - [320 px Reflow](../qa/screens/qa/reflow-320px.png): `scrollWidth` = 320 px, `innerWidth` = 320 px. Zero horizontal scrolling, no clipped text.
- **Dialogs & Interactive States:**
  - Mobile Menu Sheet: [Open at 360 px](../qa/screens/qa/dialog-menu-open-360.png). Focus trapped on open; Escape closes and restores focus to `menu-button`.
  - Lightbox Dialog: [Open at 1280 px](../qa/screens/qa/dialog-lightbox-open-1280.png). Fullscreen image stage, Prev/Next controls, Lukk button. Closes on Escape and restores focus to triggering tile.
- **Keyboard Walk & Focus Rings:**
  - 25 interactive elements traversed sequentially via Tab key.
  - Skip-link activates first (`.skip-link:focus`).
  - Elements on kalk ground display 3 px solid `--kobber` outline (`rgb(169, 72, 28)`).
  - Elements on tjære footer display 3 px solid `--kobber-lys` outline (`rgb(224, 138, 82)`).
- **Reduced Motion (WCAG 2.3.3):**
  - Evaluated under `prefers-reduced-motion: reduce`. Computed `--dur` token evaluates to `'0s'` (instant transitions).
- **Metadata & Open Graph Verification:**
  - Title: `MiniHouse for Vestlandet`
  - Meta description: `Et huskonsept for Bergen på ca. 6 × 3 m. Se romløsningen og planen for gjenbruk av gamle furubord.`
  - Canonical: `https://minihouse.canner.app/`
  - Open Graph Image: `https://minihouse.canner.app/_astro/og-image.5zMvU3bu.jpg` (canonical hero with «Konseptbilde»)
  - Open Graph Image Alt: `Konseptbilde av MiniHouse, et lite hus med saltak i svart metall og kledning av gjenbrukt tre, på en vestlandsk skråning.`
  - Twitter Card: `summary_large_image`
  - Hreflang: absolute links for `nb`, `en`, and `x-default`
  - Schema.org: Organization JSON-LD present.

---

## Holding page · 2026-11-17

Live page: https://minihouse.canner.app (deployment `f3dece04`).
Confirmed pass: 0 open findings.
