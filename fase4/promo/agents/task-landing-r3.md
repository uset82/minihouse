# Task · R3: Carlos's photos and Midtun film, and six fixes on the home page

Revision 1, 2026-11-19. Written by Claude Code for Carlos after a design review of https://minihouse-preview.canner.app. **Grok** and **DeepSeek** carry it out. Ownership is in [README.md](README.md). The rules are [DESIGN-GUIDE](../DESIGN-GUIDE.md) R2.5: §6.3, §6.5, §6.6, §6.12, §6.15, §6.16 and §7. The decision is [decisions.md](../decisions.md) D16.

**Read this first.**
- Every file name, selector, value and key in this file was checked against the code on 2026-11-19 by Claude Code's reviewer agent. Follow the cards literally.
- If what you find doesn't match a card, stop and write **BLOCKED** with what you found. Don't improvise a design.

## What Carlos asked, and what he decided

> «go into https://minihouse-preview.canner.app using your skills and agents as designer … make a list of changes to improve the landing page so later on grok and deepseek will execute … add the video in the https://minihouse-preview.canner.app/historien/»

He attached eight demolition photos and his film `images/midtun_teachers_residence_v3_4k_send.mp4`. His answers on 2026-11-19 (D16):

| Question | His answer | What it means |
|---|---|---|
| Which pictures may be published | «My phone photos», «Ingvaldsen's four photos», «The whole Midtun film» | Use `IMG_1343.jpg` and `6.jpg`, credited «Foto: Carlos», and `0V0A2359`, `0V0A2394`, `0V0A2535` and `0V0A2667`, credited «Foto: Joran Ingvaldsen». Use his film. |
| The English titles burned into the film | «A clean version» | Carlos exports the same film without titles as `images/midtun_teachers_residence_clean_4k.mp4`. **Never cut, show or upload the titled v3.** |
| How the film plays | «Silent, by itself» | Like the house film: muted, looping, with the shared «Pause filmen». The music is left out. |
| Photos with people | «Leave them out» | **Never use `3.jpg`** (a worker and a readable number plate) or **`5.jpg`** (a worker on the scaffolding). |

He approved the plan, which includes Grok's upload to minihouse-preview after every check passes (G-19).

## What changes, in one paragraph each

- **The story page becomes «the first life, then the second».**
  - His film of the old teachers' residence plays full width, right after the sentence that names the house.
  - Three photos follow «Det var en vakker, gammel bygning …»: the stained glass, the stove and the stones.
  - Two photos follow the paragraph about the old timber: the board with «1887» in pencil, and an old nail.
  - The malmfuru question band stays the one loud moment. After it come only the concept images of MiniHouse.
- **The home page gets six fixes:**
  1. The «Hvordan ideen oppstod» section gets Carlos's gable photo, the only real photo on the home page.
  2. The gallery keeps 6 pictures with the mirror shown only once.
  3. One note replaces 7 captions under the gallery.
  4. The materials section is 21 % shorter on desktop.
  5. The steel sample shows steel.
  6. The footer note is true again, and the footer gets a «Historien» link.

## Rules for this task

1. **Tokens only.** The only literal values allowed are the ones written in these cards.
2. **Photos:**
   - only the six named above;
   - never `3.jpg` or `5.jpg`;
   - never change the originals in `images/`;
   - never copy the photographer's name, phone number or any file data into a file, a log or a commit message. Credit him only as «Foto: Joran Ingvaldsen».
3. **The film:** only the clean master, silent. Never the titled v3.
4. **Words:**
   - Carlos's story text doesn't change.
   - New strings come from Appendix A.
   - DeepSeek owns `nb.json` and `en.json`.
   - Grok enters the photo alt text and captions in `images.json`, copied from Appendix B. If DeepSeek rewords one, it writes "→ Grok: replace … with …".
5. **No generated images or video.** No new dependencies. No git. One upload, G-19, to `minihouse-preview` only, never `canner redeploy`.
6. **Widths:** test at **360, 768, 1024, 1280 and 1920 px**. Before a full-page screenshot, scroll to the bottom and back and wait until every `img` has `naturalWidth > 0`, because lazy images otherwise show as empty frames.
7. **Leave every other uncommitted file alone,** including other sessions' work.

## Load the skills first (both agents)

These are the same as in [task-story-page.md](task-story-page.md):
1. `/minihouse-frontend-design` (Grok), or `.agents/skills/minihouse-frontend-design/SKILL.md` (DeepSeek);
2. `C:\Users\carlos\.claude\plugins\cache\claude-plugins-official\frontend-design\1.1.1\skills\frontend-design\SKILL.md`, which Carlos runs in Claude Code as `/frontend-design:frontend-design`;
3. `web/promo/DESIGN.md`;
4. DESIGN-GUIDE R2.5 §6.3, §6.5, §6.6, §6.12, §6.15, §6.16, §7 and §10–§11.

## Who writes what

| Path | Writer |
|---|---|
| The repo's `scripts/prepare_photos.py` (new) and `scripts/cut_film.py` | Grok |
| `web/promo/src/content/images.ts`; in `images.json`, the six new `midtun-*` entries and the `texture-stal` entry; the matching masters in `src/assets/images/` | Grok |
| `web/promo/src/content/films.json`, `films.ts`, `src/assets/film/**`, `public/film/**` | Grok |
| `schema.ts`, `scripts/content-contract.mjs`, `Gallery.astro`, `StoryTeaser.astro`, `SiteFooter.astro`, `Story.astro`, `Base.astro`, `story.css`; in `base.css`, only the gallery note and the materials rules from `64rem` | Grok |
| `status/grok.md`, `status/grok-screens/` | Grok |
| `nb.json`, `en.json`, `fase4/promo/content/**` (the copy deck, the claims register, `sitemap.md`), `scripts/check_promo.py`, `fase4/promo/qa/**` except `changelog.md`, `status/deepseek.md` | DeepSeek |
| This file, `DESIGN-GUIDE.md`, `web/promo/DESIGN.md`, `PLAN.md`, the briefs | Claude Code |

**The build:** Grok runs `npm run check`, `npm run build` and the 4322 preview, with the system Node (`C:\Program Files\nodejs`). It never stops a server it didn't start.

## Order

1. **Any time:** DeepSeek D-23r, the re-run of the story page's live check.
2. **Grok G-9, then G-10** (the contracts), then the HANDOVER to DeepSeek.
   - **DeepSeek D-24** (copy deck, claims, sitemap) can start at once.
   - **D-25** (the JSON) starts after G-10.
   - **Grok G-11** (photos and steel sample) runs in parallel.
3. **After D-25:**
   - Grok G-12 (gallery), G-13 (materials), G-14 (home section and footer) and G-15 (story page);
   - DeepSeek D-26 (the checker).
4. **Grok G-16** (film cuts) whenever `images/midtun_teachers_residence_clean_4k.mp4` exists. Until then the page has no film, and everything else goes ahead.
5. **Grok G-17** (share image) is optional, and comes only after G-18 passes without it.
6. **Grok G-18** (build, checks and visual QA) comes after G-12 to G-15, D-26, and G-16 if the film exists.
7. **DeepSeek D-27** (audits) comes after G-18.
8. **Grok G-19** (upload) comes after G-18 and D-27 pass.
   - If the clean film arrives later: G-16, then G-18, then G-19 again.
   - That later re-upload of the same task needs no new OK.
9. **DeepSeek D-28** (the live check) comes after G-19.

---

## Grok

### G-9 · Load the skills and plan
Write a status entry before any code:
- the four skill sources read;
- the cards you'll do, in order;
- anything in the code that doesn't match a card. Any mismatch is BLOCKED.

**Done when:** the entry is logged.

### G-10 · The contracts (keys, film id, film entry)
**`web/promo/src/content/schema.ts`:**
- in `gallery`, add `note: string;`;
- in `story`, add `film: { alt: string; caption: string };`.

**`web/promo/scripts/content-contract.mjs`:**
- `gallery` becomes `{ title: '', count: '', prev: '', next: '', close: '', note: '' }`;
- inside `story`, add `film: { alt: '', caption: '' },`.

**`web/promo/src/content/films.ts`:** `export type FilmId = 'house' | 'living' | 'bath' | 'midtun';`

**`web/promo/src/content/films.json`:** append the entry in Appendix C. It's safe before the film exists, because `getFilm()` returns nothing without a poster.

**Then write:** «HANDOVER → DeepSeek: keys landed: `gallery.note`, `story.film.alt`, `story.film.caption`.»

**Done when:** `node scripts/check-content.mjs` (in `web/promo`) fails only on those three keys in nb and en, or passes if D-25 is done. Don't build until it passes.

### G-11 · Photo masters and the steel sample
- **Write `scripts/prepare_photos.py`** exactly as in Appendix D, and run `python scripts/prepare_photos.py`.
  - It converts the photographer's Adobe RGB files to sRGB. Without that, the photos look dull.
  - It saves every copy without EXIF, IPTC, XMP or a colour profile.
  - It refuses `3.jpg` and `5.jpg`.
- **`web/promo/src/content/images.ts`:** add these six ids inside the `imageIds` array, before `] as const`, in single quotes, with no comments inside the array (`content-contract.mjs` reads them with a regex):
  ```ts
  'midtun-gable',
  'midtun-1887',
  'midtun-nail',
  'midtun-glass',
  'midtun-stove',
  'midtun-stone',
  ```
- **`web/promo/src/content/images.json`,** in the **same step:** `assert-images.ts` throws if the two disagree.
  - Append the six entries in Appendix B, exactly.
  - Edit the `texture-stal` entry: `"source": "images/Weathered timber cabin with a glowing interior.png, crop x 1024 y 480 w 280 h 350: the front-right corner with the dark steel plinth across the bottom fifth"` and `"focal": "50% 50%"`. Keep its status (`stand-in`), its alt text and its caption.

**Done when:**
- The script prints seven lines with the sizes in Appendix D and exits 0.
- `node scripts/check-content.mjs` passes the image check.
- **You looked at each copy next to its original:**
  - the four Ingvaldsen photos have the same colour, not duller or greyer;
  - the gable and the stove stand upright;
  - the steel crop shows the corner of the cladding with the black plinth across the bottom, with no grass band and no window frame.
- Screenshots of the seven copies are in `status/grok-screens/r3-media-*.png`.

### G-12 · Gallery: 6 pictures, one note
**`web/promo/src/components/Gallery.astro`:** replace the `rows` array with:
```ts
const rows: ImageId[][] = [
  ['meadow-wide', 'bath-shower', 'bench'],
  ['kitchen', 'bath-window', 'storage'],
];
```
Each row is landscape, portrait, landscape, and only `bath-shower` still shows the wavy mirror. Also update the component's comment to "two rows of three".

**Markup:** right after the closing `</div>` of `.gallery-strip`, still inside `.wrap`:
```astro
<p class="gallery-note">{content.gallery.note}</p>
```

**`web/promo/src/styles/base.css`:** add right after the `.tile-caption { … }` rule:
```css
.gallery-tile .tile-caption {
  display: none;
}

.gallery-note {
  margin-top: var(--space-3);
  color: var(--text-soft);
  font-size: var(--size-caption);
}
```
Don't use a visually-hidden pattern here. The tiles aren't positioned, so the hidden captions would push the phone strip sideways. The lightbox reads the caption's `textContent`, which still works with `display: none`.

**Done when:**
- **At 1280:** 6 tiles in 2 rows, 0 visible tile captions, 1 note under the sheet. Opening a tile shows «1 av 6 / Konseptbilde» under the big picture.
- **At 390:** the strip's count reads «1 av 6», and `document.documentElement.scrollWidth - innerWidth === 0`.

### G-13 · Materials, 21 % shorter from 64rem
**`web/promo/src/styles/base.css`,** inside the `@media (min-width: 64rem)` block that starts with the comment "Gammelt tre, nytt hus: boards stacked in a zig-zag", which comes after both `48rem` blocks:
- in `.material`, change `grid-template-columns` to `minmax(0, 3fr) minmax(0, 7fr) minmax(0, 2fr)`;
- in `.material--flip`, change `grid-template-columns` to `minmax(0, 2fr) minmax(0, 7fr) minmax(0, 3fr)`;
- add at the end of that block:
```css
.material + .material {
  margin-top: var(--space-5);
}

.passport dl {
  display: grid;
  grid-template-columns: max-content minmax(0, 1fr) max-content minmax(0, 1fr);
  column-gap: var(--space-4);
  row-gap: var(--space-1);
}

.passport dl > div {
  grid-column: span 2;
  grid-template-columns: subgrid;
  column-gap: var(--space-3);
  padding-block: 0;
}
```
The `48rem` block sets `display: block` on the dl and its own columns and padding on each div. These rules come later with the same specificity, so they win. Phones and tablets don't change.

**Done when:**
- **At 1280:**
  - each `.material` is at most 395 px tall, and `#materialer` at most 2050 px (it was 510 and 2584);
  - each tag shows 3 rows of 2 pairs, in the order Materiale | Opprinnelse, Tidligere bruk | Brukes til, Behandling | Status;
  - the stub, the eyelet and the zig-zag look as before.
- **At 1024:** no value runs out of its column. «dokumenteres per parti» on two lines is fine.
- **At 390:** the section looks exactly as before. Compare screenshots.

### G-14 · The home story section with the gable photo, and the footer
**`web/promo/src/components/StoryTeaser.astro`:** add `import Figure from './Figure.astro';` to the frontmatter, and make the section:
```astro
<section class="story-teaser" aria-labelledby="story-teaser-title">
  <div class="wrap story-teaser-grid">
    <div class="story-teaser-text">
      <h2 id="story-teaser-title">{content.story.teaser.title}</h2>
      <p>{content.story.teaser.body}</p>
      <a href={href}>{content.story.teaser.link}</a>
    </div>
    <Figure imageId="midtun-gable" lang={lang} class="story-teaser-photo" ratio="tile" />
  </div>
</section>
```

**`web/promo/src/styles/story.css`:**
- Delete this rule inside `@media (min-width: 64rem)`. It would squeeze the text to 7/12 of its 7 columns.
  ```css
  .story-teaser p {
    max-width: min(var(--measure), calc(7 / 12 * 100%));
  }
  ```
- Add:
  ```css
  .story-teaser-photo {
    margin-top: var(--space-5);
  }

  @media (min-width: 48rem) {
    .story-teaser-grid {
      display: grid;
      grid-template-columns: repeat(12, minmax(0, 1fr));
      column-gap: var(--space-4);
      align-items: start;
    }

    .story-teaser-text {
      grid-column: 1 / 8;
    }

    .story-teaser-photo {
      grid-column: 9 / 13;
      margin-top: 0;
    }
  }
  ```

**`web/promo/src/components/SiteFooter.astro`:**
- add `const story = lang === 'en' ? '/en/historien/' : '/historien/';` to the frontmatter;
- make the first `<li>` of the link list `<li><a href={story}>{content.nav.story}</a></li>`.

**Done when:**
- **At 1280:**
  - `.story-teaser .wrap` is at most 560 px tall (the whole section, with its padding, is about 710 px);
  - the photo's left edge is at grid line 9;
  - its top is within 4 px of the h2's top;
  - its caption reads «Lærerboligen under rivingen, april 2026. Foto: Carlos».
- **At 390:** the photo sits under «Les historien» at full content width.
- **The footer:** «Historien» comes first in both languages and opens the right page. After D-25, the note reads «Bildene av MiniHouse er konseptbilder. Huset er under utvikling.»

### G-15 · The story page: the film slot, the trio and the pair
**`web/promo/src/components/Story.astro`:**
- Replace the frontmatter and the whole `<div class="story-open">…</div>` block with Appendix E.
- Keep everything from `<div class="story-band">` down unchanged.
- The pair and the trio render only when their photos resolve, as in `Gallery.astro`, so a missing master never leaves an empty gap.

**`web/promo/src/styles/story.css`:** add:
```css
/* R3 (DESIGN-GUIDE §6.16): the Midtun film, the trio and the pair, all in the first life. */
.story-film {
  margin-block: var(--space-6);
}

.story-film .film-caption {
  max-width: calc(var(--max-content) + 2 * var(--gutter));
  margin-inline: auto;
  padding-inline: var(--gutter);
}

/* Without the film (or without a photo block), the text columns still keep their gap. */
.story-open .wrap + .wrap,
.story-col + .story-col {
  margin-top: var(--space-4);
}

.story-photos {
  margin-block: var(--space-6);
}

.story-photos--pair,
.story-photos--row {
  display: grid;
  gap: var(--space-4);
}

.story-photo img {
  aspect-ratio: var(--ar);
}

@media (min-width: 48rem) {
  .story-photos--pair {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .story-photos--row {
    display: flex;
    gap: var(--space-2);
  }

  .story-photo {
    flex: var(--ar) 1 0;
    min-width: 0;
  }
}
```

**Done when (with the photos present):**
- **The trio, at 1280:** the three `img` elements are the same height to within 1 px (about 316 px). Measure the images, not the figures, because the captions differ.
- **The pair, at 1280:** both images are 588 px wide to within 2 px.
- **Both blocks:** they line up with the content edge, not the text column, with 64 px above and below.
- **At 390:** both are stacked, each photo at its own proportion (the stove 3:4).
- **No real photo comes after the question band.** `exploded` and `hero-slope` still say «Konseptbilde».
- **Without the film files:** no empty gap. The two text columns are 24 px apart.
- **With the film files (after G-16):**
  - the film spans the page width (1265 px at 1280 with a scrollbar, or 1280 px headless) at 16:9;
  - its caption row's left edge equals the content edge (40 px at 1280, 24 px at 390);
  - it's the only eagerly loaded image on the page.

### G-16 · The Midtun film cuts (only from the clean master)
**Before cutting, check the master.** Each failure is BLOCKED, with what you found.
1. `images/midtun_teachers_residence_clean_4k.mp4` exists. It's 3840 × 2160, and `ffprobe` reports 72.37 s ± 0.1 s.
2. **No black ends:** the frame at 0.5 s and the frame at the end minus 0.5 s each have a mean brightness of at least 16 out of 255. The poster is the frame at 0.5 s, and the loop's crossfade joins the last half second to the first.
3. **The contact sheet:** one frame every 6 s, 12 frames, saved as `status/grok-screens/r3-midtun-sheet.png`. Look at it:
   - **BLOCKED:** any burned-in text, any face you could recognise, any readable number plate.
   - **Not blocking:** names readable on the old calling cards. List them in your status file for Carlos, who cleared everything in his film.

**`scripts/cut_film.py`** handles one master today: the global `SOURCE`, the hard-coded `-g 48`, flat `CUTS`, `BUDGET_MB` and `POSTER_FROM`, and a `main()` that exits when that one file is missing.
- **Restructure it into a `MASTERS` dict,** one entry per master, with `source`, `duration`, `gop`, `cuts`, `budget_mb`, `posters`, `crf_ceiling` and `over_budget` (`'warn'` or `'fail'`):
  - `house` keeps today's values exactly (GOP 48, its four cuts, budgets and posters, and today's warn-and-continue behaviour);
  - `midtun`:
    - source `images/midtun_teachers_residence_clean_4k.mp4`;
    - duration `72.37`, with a tolerance of `0.1`;
    - GOP `60`;
    - cuts:
      - `'midtun-film-1920': (0.0, None, None, (1920, 1080), 0.5, 30)`;
      - `'midtun-film': (0.0, None, None, (1280, 720), 0.5, 30)`;
    - budgets `{'midtun-film-1920': 14.0, 'midtun-film': 8.0}`;
    - posters `{'midtun-film': 'midtun-film-1920'}`;
    - CRF ceiling `34`, over budget `'fail'`.
- **`cut()` takes the source and the GOP as arguments.**
- **The midtun cuts and poster add `-map_metadata -1 -map_chapters -1`,** so no master metadata is copied.
- **The command line:** `python scripts/cut_film.py midtun`, and `python scripts/cut_film.py house` (the default when there's no argument). **Run only `midtun`.** Never re-encode the house cuts.
- **Exit 1:** when the master is missing, when its length is outside the tolerance, or when a `'fail'` cut is still over budget at its CRF ceiling. Then write BLOCKED with the sizes.

**Done when:**
- `midtun-film-1920.mp4` is at most 14 MB and `midtun-film.mp4` at most 8 MB. Write down the CRF each one needed.
- `ffprobe` on both shows H.264, 30 fps, no audio stream, and `moov` before `mdat`.
- `web/promo/src/assets/film/midtun-film.jpg` is the first frame of the 1920 cut, and it isn't black.
- The house cuts' timestamps haven't changed.

### G-17 · The share image (optional, only after G-18 passes without it)
**`web/promo/src/layouts/Base.astro`:**
- add optional props `ogImage?: ImageMetadata` and `ogAlt?: string`;
- when `ogImage` is set, use `await getImage({ src: ogImage, width: 1200, height: 630, fit: 'cover', format: 'jpg' })` for `og:image` and `twitter:image`, and `ogAlt` for both alt tags;
- otherwise keep today's `og-image` and `content.meta.ogAlt`.

**Both story pages** pass the `midtun-film.jpg` poster (through `getFilm('midtun')?.posterImage`) and `story.film.alt`. Without the poster, they pass nothing.

**Done when:** `/historien/` has a 1200 × 630 `og:image` of the drone shot, and `/` is unchanged.

### G-18 · Build, check and look
- **Run:**
  - `npm run check`;
  - `npm run build`;
  - `python scripts/check_promo.py`;
  - `python scripts/check_promo.py --dist web/promo/dist` (7 pages);
  - `python scripts/check_promo.py --selftest`;
  - `python scripts/verificar_todo.py`.
- **Playwright** (Python, `channel='chrome'`) at 360, 768, 1024, 1280 and 1920 px:
  - full pages of `/`, `/historien/` and `/en/historien/`, after scrolling so every image has loaded;
  - record every measurement from the "Done when" lines of G-12 to G-16 in your status entry;
  - at every width: `scrollWidth - innerWidth === 0`.
- **The keyboard:** the skip link, Tab through the gallery tiles, the footer's «Historien» and the film button. The focus ring shows everywhere, and Esc closes the lightbox and the «Meny» sheet.
- **Reduced motion** (`reduced_motion='reduce'`): the Midtun film shows its still, and the button reads «Spill av filmen».
- **The film,** if G-16 is done: `currentSrc` is `midtun-film-1920.mp4` at 1280 and 1920, and `midtun-film.mp4` at 360 and 768. It's muted and its time advances. After a pause and a reload it stays paused.
- **Look at every screenshot** against DESIGN-GUIDE §10–§11. Remove one accessory and name it.

**Done when:** every command passes, every measurement is within its card, the §11 boxes are ticked, and the screenshots are in `status/grok-screens/r3-*.png`. Then write HANDOVER → DeepSeek for D-27.

### G-19 · Upload to the preview (only after G-18 and D-27 pass)
```text
cd web/promo && npm run bundle
cd .bundle && canner deploy --slug=minihouse-preview --follow
```

**On the live site:**
- `/`, `/en/`, `/historien/` and `/en/historien/` answer 200 `text/html`;
- `curl -r 0-1` on `/film/house-film.mp4`, and on `/film/midtun-film.mp4` if it exists, answers 206 `video/mp4`;
- `/.env.production` answers 404.

**Never:** `canner redeploy`, another slug, or git. **Done when:** it's live, with the deployment id logged. Then write HANDOVER → DeepSeek for D-28.

---

## DeepSeek

DeepSeek can't see images, so it never judges screenshots, colours or layout.

### D-23r · Re-run the story page's live check
The D-23 run at 23:54 on 2026-11-18 came one minute before Grok's upload (G-8, 23:55), so the story pages were missing. Run it again:
- status codes for `/`, `/en/`, `/historien/` and `/en/historien/`;
- the `hreflang` pairs;
- `check_promo.py --dist web/promo/.bundle`.

Record it in `qa/story.md`.

**Done when:** it's logged, with a HANDOVER to Carlos for the story page.

### D-24 · Copy deck, claims and sitemap
- **`content/copy-story.md` §6 (new):** the words in Appendices A and B, in nb and en, each with its claim id.
  - Review the Norwegian. If you change anything, write "→ Grok: replace … with …" for the `images.json` strings, and use your version in the JSON keys.
  - Keep «grønn» and "green" out: the banned-word scan catches them, even as a colour.
- **The claims register:**
  - **K-45:** the six photos are real photos from the 2026 demolition, credited as Appendix B says. Source: D16 (Carlos, 2026-11-19).
  - **K-46:** «1887» is written in pencil on a board in the residence (the photo), and the reference page calls it «the historic 1887 building».
  - **K-47:** the film is Carlos's, with photos by Joran Ingvaldsen and Carlos (D16). It's not a concept film, so never «Konseptfilm» (that's K-35, the house film).
  - **Update K-20 to** «Bildene av MiniHouse er konseptbilder.», because the old residence's photos are real.
  - **Check the gable caption's date:** its camera date is 2026-04-03. If the demolition hadn't started then, write «før rivingen» and tell Grok.
  - **Keep K-37's never-claim:** no caption may say or suggest that MiniHouse uses timber, stone, glass or the stove from Øvsttunvegen.
- **`content/sitemap.md`:**
  - §2: the gallery row now has 6 pictures (meadow, shower, bench, kitchen, bathroom window, storage) and one note;
  - the home section now has a photo;
  - the story page now has the film, the trio and the pair;
  - §4: `gallery.note` and `story.film`.

**Done when:** the register parses, and every new string traces to a row.

### D-25 · Fill the JSON (after G-10's HANDOVER)
In `nb.json` and `en.json`:
- `gallery.note`;
- `story.film.alt` and `story.film.caption`;
- the new `footer.imagesNote`.

All from Appendix A, or your D-24 version.

**Done when:** `node scripts/check-content.mjs` passes, then a HANDOVER → Grok: «JSON filled».

### D-26 · `scripts/check_promo.py`
- **(a) Captions by kind, per language:**
  - for a `photo`, `caption.nb` must contain «Foto:» and `caption.en` "Photo:", and neither may contain «Konseptbilde» or "Concept image";
  - for a `render` or `texture`, `caption.nb` must contain «Konseptbilde» and `caption.en` "Concept image".

  All 19 current entries pass.
- **(b) No file data in the pictures:** walk the JPEG segments of every `.jpg` and `.jpeg` in `web/promo/src/assets/images/` and `web/promo/src/assets/film/`, and, with `--dist`, in `dist/_astro/`.
  - **Fail on:** APP1 with an `Exif\0\0` or XMP (`http://ns.adobe.com/xap/1.0/`) header, and on any APP13 (IPTC, "Photoshop 3.0").
  - **Don't fail on:** comment segments (the posters carry ffmpeg's encoder comment) or APP2 colour profiles.
- **(c) A self-test for each:** a photo without «Foto:», a render without «Konseptbilde», and a tiny JPEG with an APP1 Exif, an XMP and an APP13 segment.

**Done when:** `--selftest`, the source run and `--dist` all pass on Grok's G-18 build.

### D-27 · Audits after G-18
- **A claims audit** of the new captions, the film words, the gallery note and the footer note, in `qa/story.md`;
- **axe,** and **Lighthouse** on mobile and desktop, for `/` and `/historien/` against 4322, in `qa/a11y.md` and `qa/perf.md`, with the reports in `qa/reports/`;
- the film still may now be the largest paint on `/historien/`.

**Done when:** axe shows 0 violations, LCP is at most 2.5 s on mobile, and CLS at most 0.1, or the gaps are raised as "→ Grok:".

### D-28 · The live check after G-19
- the four HTML routes;
- `hreflang`;
- 206 `video/mp4` on the films;
- 404 on `/.env.production`;
- `check_promo.py --dist web/promo/.bundle`.

Record it in `qa/story.md`, then write a HANDOVER → Carlos for G4.

---

## Appendix A · New strings (DeepSeek's JSON keys)

| Key | nb | en |
|---|---|---|
| `gallery.note` | Alle bildene her er konseptbilder. | All the pictures here are concept images. |
| `footer.imagesNote` | Bildene av MiniHouse er konseptbilder. Huset er under utvikling. | The pictures of MiniHouse are concept images. The house is under development. |
| `story.film.alt` | Film fra lærerboligen i Øvsttunvegen: huset og Midtun skole sett fra luften, blyglassvinduet, årstallet 1887 i et bord, den gamle komfyren og rivingen. | Film of the teachers' residence at Øvsttunvegen: the house and Midtun school from the air, the stained-glass window, the year 1887 on a board, the old stove and the demolition. |
| `story.film.caption` | Film: Carlos. Foto i filmen: Joran Ingvaldsen og Carlos. | Film: Carlos. Photos in the film: Joran Ingvaldsen and Carlos. |

If G-16 finds the clean film's shots differ from this description, Grok writes "→ DeepSeek:" with what it shows.

## Appendix B · The six `images.json` entries (Grok appends them exactly)

These are six objects to add at the end of the existing top-level array in `images.json`, with a comma after the current last entry. Keep the file valid JSON, and keep the ids in the same order as `images.ts`.

```json
{
  "id": "midtun-gable",
  "file": "midtun-gable.jpg",
  "kind": "photo",
  "status": "pending",
  "alt": {
    "nb": "Gavlen på den gamle lærerboligen under rivingen. Kledningen er delvis tatt av, og et blyglassvindu sitter fortsatt i veggen.",
    "en": "The gable of the old teachers' residence during the demolition. Part of the cladding is off, and a stained-glass window is still in the wall."
  },
  "caption": {
    "nb": "Lærerboligen under rivingen, april 2026. Foto: Carlos",
    "en": "The teachers' residence during the demolition, April 2026. Photo: Carlos"
  },
  "source": "images/IMG_1343.jpg, Carlos's phone photo (2026-04-03), upright, file data removed, 1800 x 2400",
  "focal": "50% 38%"
},
{
  "id": "midtun-1887",
  "file": "midtun-1887.jpg",
  "kind": "photo",
  "status": "pending",
  "alt": {
    "nb": "Gamle bord med blyantskrift i løkkeskrift. Årstallet 1887 står skrevet på det midterste bordet.",
    "en": "Old boards with looping pencil writing. The year 1887 is written on the middle board."
  },
  "caption": {
    "nb": "Årstallet 1887, skrevet med blyant på et bord i lærerboligen. Foto: Joran Ingvaldsen",
    "en": "The year 1887, written in pencil on a board in the residence. Photo: Joran Ingvaldsen"
  },
  "source": "images/0V0A2394.jpg, photo by Joran Ingvaldsen, used with permission (D16), converted to sRGB, file data removed, 2400 x 1601",
  "focal": "50% 50%"
},
{
  "id": "midtun-nail",
  "file": "midtun-nail.jpg",
  "kind": "photo",
  "status": "pending",
  "alt": {
    "nb": "En rusten, firkantet spiker stikker skrått opp av et gammelt trestykke.",
    "en": "A rusty square nail sticks out at an angle from an old piece of timber."
  },
  "caption": {
    "nb": "En gammel spiker i treverket. Foto: Joran Ingvaldsen",
    "en": "An old nail in the timber. Photo: Joran Ingvaldsen"
  },
  "source": "images/0V0A2535.jpg, photo by Joran Ingvaldsen, used with permission (D16), converted to sRGB, file data removed, 2400 x 1601",
  "focal": "50% 50%"
},
{
  "id": "midtun-glass",
  "file": "midtun-glass.jpg",
  "kind": "photo",
  "status": "pending",
  "alt": {
    "nb": "Et blyglassvindu med trær, skyer, en seilbåt, et fyrtårn og en soloppgang rundt en stor rute i ravfarget glass.",
    "en": "A stained-glass window with trees, clouds, a sailing boat, a lighthouse and a sunrise around a large amber pane."
  },
  "caption": {
    "nb": "Blyglassvinduet i lærerboligen. Foto: Joran Ingvaldsen",
    "en": "The stained-glass window in the residence. Photo: Joran Ingvaldsen"
  },
  "source": "images/0V0A2359.jpg, photo by Joran Ingvaldsen, used with permission (D16), converted to sRGB, file data removed, 2400 x 1601",
  "focal": "50% 50%"
},
{
  "id": "midtun-stove",
  "file": "midtun-stove.jpg",
  "kind": "photo",
  "status": "pending",
  "alt": {
    "nb": "En gammel komfyr i støpejern foran en pipe der pussen er slått av og teglsteinen ligger bar.",
    "en": "An old cast-iron cooking stove in front of a chimney with the plaster knocked off and the bricks bare."
  },
  "caption": {
    "nb": "Den gamle komfyren under rivingen. Foto: Carlos",
    "en": "The old stove during the demolition. Photo: Carlos"
  },
  "source": "images/6.jpg, Carlos's phone photo, file data removed, 1800 x 2400",
  "focal": "50% 50%"
},
{
  "id": "midtun-stone",
  "file": "midtun-stone.jpg",
  "kind": "photo",
  "status": "pending",
  "alt": {
    "nb": "Stabler med flate steinheller på paller i gresset, med et anleggsgjerde bak.",
    "en": "Stacks of flat stone slabs on pallets in the grass, with a site fence behind."
  },
  "caption": {
    "nb": "Steinheller som ble tatt vare på under rivingen. Foto: Joran Ingvaldsen",
    "en": "Stone slabs saved during the demolition. Photo: Joran Ingvaldsen"
  },
  "source": "images/0V0A2667.jpg, photo by Joran Ingvaldsen, used with permission (D16), converted to sRGB, file data removed, 2400 x 1601",
  "focal": "50% 50%"
}
```

## Appendix C · The `films.json` entry (Grok appends it in G-10)

```json
{
  "id": "midtun",
  "file": "midtun-film.mp4",
  "poster": "midtun-film.jpg",
  "width": 1280,
  "height": 720,
  "wide": {
    "file": "midtun-film-1920.mp4",
    "width": 1920,
    "height": 1080
  },
  "status": "pending",
  "source": "images/midtun_teachers_residence_clean_4k.mp4 (Carlos's film without titles, 3840 x 2160, 30 fps, 72.37 s), the whole film with a 0.5 s crossfade at the loop; cut by scripts/cut_film.py midtun"
}
```

## Appendix D · `scripts/prepare_photos.py` (Grok writes it exactly)

```python
#!/usr/bin/env python3
"""Make the site copies of Carlos's demolition photos and the steel sample (task-landing-r3 G-11).

The originals in images/ are never changed. Every copy is converted to sRGB and saved with no
EXIF, IPTC, XMP or colour profile: the photographer's files carry his name and phone number,
and none of that may reach the site (DESIGN-GUIDE §7, D16). Needs Pillow (10.4 is installed).
"""
from __future__ import annotations

import io
import os
import sys

from PIL import Image, ImageCms, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'images')
OUT = os.path.join(ROOT, 'web', 'promo', 'src', 'assets', 'images')

# site copy: (original in images/, width, height, crop box (left, top, right, bottom) or None)
JOBS = {
    'midtun-gable.jpg': ('IMG_1343.jpg', 1800, 2400, None),
    'midtun-stove.jpg': ('6.jpg', 1800, 2400, None),
    'midtun-glass.jpg': ('0V0A2359.jpg', 2400, 1601, None),
    'midtun-1887.jpg': ('0V0A2394.jpg', 2400, 1601, None),
    'midtun-nail.jpg': ('0V0A2535.jpg', 2400, 1601, None),
    'midtun-stone.jpg': ('0V0A2667.jpg', 2400, 1601, None),
    # The steel sample: the front-right corner, the dark plinth across the bottom fifth.
    'texture-stal.jpg': ('Weathered timber cabin with a glowing interior.png', 280, 350, (1024, 480, 1304, 830)),
}
NEVER = {'3.jpg', '5.jpg'}  # workers and a readable number plate (D16: «Leave them out»)
SRGB = ImageCms.createProfile('sRGB')


def to_srgb(image: Image.Image, icc: bytes | None) -> Image.Image:
    if icc:
        source = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        return ImageCms.profileToProfile(image, source, SRGB, outputMode='RGB')
    return image.convert('RGB')


def private_segments(path: str) -> list[str]:
    """APP1 (EXIF or XMP) and APP13 (IPTC) segments left in a JPEG."""
    with open(path, 'rb') as handle:
        data = handle.read()
    found, i = [], 2
    while i + 4 <= len(data) and data[i] == 0xFF:
        marker = data[i + 1]
        if marker in (0xD9, 0xDA):
            break
        length = int.from_bytes(data[i + 2:i + 4], 'big')
        if marker == 0xE1:
            found.append('APP1')
        elif marker == 0xED:
            found.append('APP13')
        i += 2 + length
    return found


def main() -> int:
    for name, (original, width, height, box) in JOBS.items():
        if original in NEVER:
            print(f'refused: {original} is excluded (D16)')
            return 1
        path = os.path.join(SRC, original)
        if not os.path.isfile(path):
            print(f'missing: {path}')
            return 1
        with Image.open(path) as opened:
            icc = opened.info.get('icc_profile')
            image = to_srgb(ImageOps.exif_transpose(opened), icc)
        if box:
            image = image.crop(box)
        if image.size != (width, height):
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        target = os.path.join(OUT, name)
        # No exif=, icc_profile= or xmp= argument, on purpose.
        image.save(target, 'JPEG', quality=90 if box else 86, optimize=True, progressive=True)
        left = private_segments(target)
        if left:
            print(f'{name}: file data survived ({", ".join(left)})')
            return 1
        print(f'{name}: {width} x {height}, {os.path.getsize(target) / 1e6:.2f} MB, from {original}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

It prints seven lines: six photos (four at 2400 × 1601, two at 1800 × 2400) and the steel sample at 280 × 350.

## Appendix E · `Story.astro`: the new frontmatter and opening (Grok writes it exactly)

```astro
---
import type { ImageMetadata } from 'astro';
import type { Content } from '../content/schema';
import { images } from '../content/assert-images';
import type { ImageId } from '../content/images';
import Figure from './Figure.astro';
import Film from './Film.astro';
import '../styles/story.css';

interface Props {
  content: Content;
  lang: 'nb' | 'en';
}

const { content, lang } = Astro.props;
const story = content.story;
const houseHref = lang === 'en' ? '/en/#bilder' : '/#bilder';

/* Real photos render only when their master and alt text exist, as in Gallery.astro. */
const masters = import.meta.glob<{ default: ImageMetadata }>('../assets/images/*.{jpg,jpeg,png,webp}');
const ratioOf = async (id: ImageId) => {
  const image = images.find((entry) => entry.id === id);
  if (!image?.file || !image.alt[lang] || image.alt[lang] === 'TODO') return undefined;
  const load = masters[`../assets/images/${image.file}`];
  if (!load) return undefined;
  const { width, height } = (await load()).default;
  return width / height;
};
const resolve = async (ids: ImageId[]) =>
  (await Promise.all(ids.map(async (id) => ({ id, ratio: await ratioOf(id) }))))
    .filter((photo): photo is { id: ImageId; ratio: number } => photo.ratio !== undefined);
const trio = await resolve(['midtun-glass', 'midtun-stove', 'midtun-stone']);
const pair = await resolve(['midtun-1887', 'midtun-nail']);
---

<article class="story">
  <div class="story-open">
    <div class="wrap">
      <div class="story-col">
        <h1>{story.title}</h1>
        <p class="story-byline">{story.byline}</p>
        <p class="story-lead">{story.lead}</p>
        <p>{story.intro[0]}</p>
      </div>
    </div>
    <Film
      id="midtun"
      class="story-film"
      label={story.film.alt}
      caption={story.film.caption}
      play={content.film.play}
      pause={content.film.pause}
      sizes="100vw"
      priority
    />
    <div class="wrap">
      <div class="story-col">
        <p>{story.intro[1]}</p>
      </div>
      {trio.length > 0 && (
        <div class="story-photos story-photos--row">
          {trio.map((photo) => (
            <div class="story-photo" style={`--ar: ${photo.ratio.toFixed(4)}`}>
              <Figure imageId={photo.id} lang={lang} ratio="wide" />
            </div>
          ))}
        </div>
      )}
      <div class="story-col">
        <p>{story.intro[2]}</p>
        <p>
          {story.reference.label}{' '}
          <a href={story.reference.href}>{story.reference.link}</a>
        </p>
        <p>{story.noticed[0]}</p>
        <p>{story.noticed[1]}</p>
      </div>
      {pair.length > 0 && (
        <div class="story-photos story-photos--pair">
          {pair.map((photo) => (
            <Figure imageId={photo.id} lang={lang} ratio="wide" />
          ))}
        </div>
      )}
      <div class="story-col">
        <p>{story.noticed[2]}</p>
        <p>{story.noticed[3]}</p>
      </div>
    </div>
  </div>
```

After this block, keep `<div class="story-band">` and everything below it exactly as it is.

---

## For Carlos: one export

Export your film again **without the titles**: the same edit, the same length (72.37 s), 3840 × 2160. Save it as:

```text
images/midtun_teachers_residence_clean_4k.mp4
```

Until it's there, the agents build everything else, and the story page simply has no film. They never use the titled v3.

## Status entries

Both agents add one entry per card, newest first, with the same template as [task-story-page.md](task-story-page.md):
- Files;
- Plan;
- Evidence: commands, results and measurements;
- the §11 boxes;
- HANDOVER, BLOCKED or "→ Agent:";
- Next.

## Kickoff prompts

**Grok (Grok CLI),** started with `grok` in `C:\Users\carlos\PROYECTOS\minihouse`, with the folder trusted:

```text
You are Grok on the MiniHouse promo website, task R3. Read fase4/promo/agents/task-landing-r3.md: your cards are G-9 to G-19.
Load the skills as the file says (/minihouse-frontend-design, the frontend-design SKILL.md path, web/promo/DESIGN.md,
DESIGN-GUIDE R2.5). Every selector, value and file name in the cards was checked against the code: follow them literally,
and if something doesn't match, write BLOCKED instead of improvising.
Start with G-9, then G-10 and its HANDOVER to DeepSeek. Never use images/3.jpg or images/5.jpg, never the titled film
(only images/midtun_teachers_residence_clean_4k.mp4), never write the photographer's file data anywhere, never generate
images or video, never commit or push. Upload only in G-19, to minihouse-preview, after G-18 and DeepSeek's D-27 pass.
Log every card in fase4/promo/status/grok.md.
```

**DeepSeek (DeepSeek Harness),** started in the repo root:

```text
You are DeepSeek on the MiniHouse promo website, task R3. Read fase4/promo/agents/task-landing-r3.md: your cards are
D-23r and D-24 to D-28. Read fase4/promo/status/grok.md before each step. Load .agents/skills/minihouse-frontend-design/SKILL.md
and web/promo/DESIGN.md. You can't see images: never judge visuals.
Start with D-23r (the story page's live check, re-run) and D-24 (copy deck §6, claims K-45 to K-47 and K-20, sitemap).
Fill the JSON (D-25) only after Grok's G-10 HANDOVER. Carlos's story text never changes; Appendix A and B hold the new words.
Don't publish, deploy, commit or push. Log every card in fase4/promo/status/deepseek.md.
```
