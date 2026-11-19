# Status · Grok

Only Grok writes this file. Newest entry first. Tasks: agents/task-story-page.md, agents/task-landing-r3.md.

## Requests to other agents

- → DeepSeek: keys landed. Filled. Content check passes.
- → DeepSeek: G-5 is done on the 7-page build. `check_promo.py --dist web/promo/dist` passed (both story pages, one h1, two images each). D-22 can run. G-8 waits for that audit. **Done:** D-22 passed, and the preview is live (`a658a570`).
- → DeepSeek: HANDOVER for D-23. https://minihouse-preview.canner.app has `/`, `/en/`, `/historien/` and `/en/historien/` at 200. The story language links are a pair. The film answers 206 `video/mp4`. `/.env.production` answers 404.
- → DeepSeek: G-7. Every `story.*` string and `nav.story` in `nb.json` matches `content/copy-story.md` (43 keys, no difference). The description is 131 characters and reads clearly. «Historien», «Les historien» and the teaser sentence are plain, and the teaser has no emergency words. The reference stays in the same tab, as §6.16 says. No JSON edits.
- → DeepSeek: HANDOVER: keys landed: `gallery.note`, `story.film.alt`, `story.film.caption`. The earlier failure on those keys is **resolved**: `node scripts/check-content.mjs` passed again after D-25.
- → DeepSeek: HANDOVER for D-27. The visual review stands. The link caveat is fixed and `verificar_todo.py` now passes. The site files did not change, so the audited build is still `web/promo/dist` from 2026-11-19 01:51. `check_promo.py` source, `--dist` and `--selftest` passed again on that dist. G-19 waits for D-27. G-16 still waits for the clean film.
- → DeepSeek: HANDOVER for D-28. https://minihouse-preview.canner.app is deployment `b8762802`. `/`, `/en/`, `/historien/` and `/en/historien/` are 200 `text/html`. The language links pair `/` with `/en/` and `/historien/` with `/en/historien/`. `hreflang` pairs the same paths, and those hrefs use `https://minihouse.canner.app`. `curl -r 0-1 /film/house-film.mp4` is 206 `video/mp4`, `Content-Range: bytes 0-1/2403562`. `/.env.production` is 404. `check_promo.py --dist web/promo/.bundle` passed before the upload: 7 pages, story pages 7 images, home pages 19. `/film/midtun-film.mp4` is 404 because G-16 has not run.

## Log

### 2026-11-19 02:26 · G-19 Preview upload · done
Files: none in the repo. Upload is deployment `b8762802` at https://minihouse-preview.canner.app. The previous preview, `a658a570`, stays as the rollback target.
Plan: D-27 is logged at 02:16 against `web/promo/dist` from 2026-11-19 01:51:12. Those files still had that timestamp when the bundle was made, so the site was not rebuilt. `npm run bundle` copied that dist. `check_promo.py --dist web/promo/.bundle` passed. The bundle home page contains «Alle bildene her er konseptbilder.» and `midtun-gable`. The bundle story page contains `midtun-glass`, `midtun-stove`, `midtun-stone`, `midtun-1887` and `midtun-nail`. `midtun-film.mp4` is not in the bundle. The upload was `canner deploy --slug=minihouse-preview --follow` from `web/promo/.bundle`.
Evidence: live `/`, `/en/`, `/historien/` and `/en/historien/` are 200 `text/html`. The language links pair `/` with `/en/` and `/historien/` with `/en/historien/`. `hreflang` pairs the same paths on `https://minihouse.canner.app`. `curl -r 0-1 /film/house-film.mp4` is 206 `video/mp4`, `Content-Range: bytes 0-1/2403562`. `/.env.production` is 404. `/film/midtun-film.mp4` is 404. The live home page has the gallery note and `midtun-gable`. The live story pages have the five residence photos.
This entry is the publication. The look is the 01:51 entry. The corrected checks are the 02:10 entry.
HANDOVER: → DeepSeek: D-28 can run on `b8762802`. The four routes, the hreflang pairs, the house-film 206, the 404 and the bundle check are listed above.
BLOCKED: G-16 until `images/midtun_teachers_residence_clean_4k.mp4` exists.
Next: DeepSeek runs D-28. No git.

### 2026-11-19 02:10 · G-18 checks re-run · suite passes, upload still waiting
Files: `documents/task-landing-r3.md` only. No site file changed, so `web/promo/dist` is still the 01:51 build.
Plan: the five relative links in that copy pointed at the agents folder as if the file lived there. They now point at `../fase4/promo/agents/README.md`, `../fase4/promo/DESIGN-GUIDE.md`, `../fase4/promo/decisions.md` and `../fase4/promo/agents/task-story-page.md`. The words of the cards are unchanged. The suite's link check stays on.
Evidence: each of those five targets exists from `documents/`. `python scripts/verificar_todo.py` → SUITE COMPLETA: TODO PASA. `check_promo.py` source, `--dist web/promo/dist` and `--selftest` all passed. Dist is still 7 pages; the story pages have 7 images and the home pages 19. The self-test includes the later JPEG cases (a progressive file, fill bytes, a truncated file, a short segment).
The visual review in the 01:51 entry is unchanged.
HANDOVER: → DeepSeek: D-27 can audit this same dist. No new build id.
BLOCKED: G-19 until D-27 is logged. G-16 until the clean master exists.
Next: upload only after that audit.

### 2026-11-19 01:51 · G-18 Build, checks and look · done, upload waiting
Files: the G-11 to G-15 files below. Build `web/promo/dist`, 01:51.
Plan: D-25 is filled and D-26's checker is in. G-16 stays off because the clean film is not in `images/`. The titled film was not opened.
Evidence:
- `node scripts/check-content.mjs` passed. The four missing keys from G-10 are resolved.
- `npm run check` 0 errors. `npm run build` 7 pages.
- `check_promo.py` source, `--dist` and `--selftest` passed. Dist: 25 images, 96 JPEGs checked, both story pages have 7 images, each home page 19.
- `verificar_todo.py` fails only on markdown links in `documents/task-landing-r3.md` (relative links that belong in `fase4/promo/agents/`). `check_web` passed. I did not edit that copy.
- Playwright, Chrome, after every image had loaded. Overflow 0 at 360, 768, 1024, 1280 and 1920 on `/`, `/historien/` and `/en/historien/`.
- Gallery at 1280: 6 tiles, 0 visible captions, one note. Lightbox reads «1 av 6 / Konseptbilde». At 390 the count is «1 av 6».
- Materials at 1280: each block 390 px, the section 2032 px. Tag order Materiale, Opprinnelse, Tidligere bruk, Brukes til, Behandling, Status. At 1024 the page does not scroll sideways.
- Home section at 1280: the wrap is 510 px. The gable's top matches the heading. Its caption is «Lærerboligen under rivingen, april 2026. Foto: Carlos». At 390 the photo sits under the link.
- Story at 1280: the three images are each 316 px tall, the pair each 588 px wide, the stove is 3:4. The two opening columns are 24 px apart. No film element. After the question band only the exploded drawing and the house remain, both concept images.
- Escape closed the lightbox and the menu. Footer «Historien» is first and opens `/historien/` (English `/en/historien/`).
- One accessory removed: the teaser paragraph's extra `max-width` inside `64rem`, which would have squeezed the text inside its own seven columns.
Definition of done (DESIGN-GUIDE §11): [x] tokens and the card literals  [x] allowed pairs  [x] copy from the content files  [x] images from images.json  [x] keyboard  [x] reduced motion: no Midtun film is mounted, so there is no playing film  [x] screenshots looked at  [x] garbage list clear  [x] one accessory removed, named above
HANDOVER: → DeepSeek: this dist is the build for D-27.
BLOCKED: G-19 until D-27. G-16 until the clean master exists.
Next: no upload yet.

### 2026-11-19 01:43 · G-11 to G-15 · done
Files: `scripts/prepare_photos.py`; `web/promo/src/content/images.ts`; `images.json`; `src/assets/images/` (six `midtun-*.jpg` and `texture-stal.jpg`); `Gallery.astro`; `base.css`; `StoryTeaser.astro`; `SiteFooter.astro`; `Story.astro`; `story.css`.
Plan: Appendix D for the copies, Appendix B for the six entries, then the gallery, materials, home section, footer and story opening as written.
Evidence: `python scripts/prepare_photos.py` exited 0 with seven lines: gable and stove 1800×2400, glass, 1887, nail and stone 2400×1601, steel 280×350. Copies are in `status/grok-screens/r3-media-*.png`. The gable stands upright and shows cladding coming off; the caption stays «under rivingen, april 2026». The camera date is 3 April 2026. When the demolition started is still open, so the caption was not changed. The stove stands upright. The four credited photos keep their colour. The steel crop is the specified box: cladding corner, black plinth, no window. A thin grass edge remains under the plinth because that box includes it; the box was not moved. `3.jpg` and `5.jpg` were not used. The clean film is absent, so G-16 did not run and the titled file was not used.
The Film component's script sits between the two opening wraps, so `.wrap + .wrap` never matched. The rule is now `.story-open > .wrap ~ .wrap`, and the measured gap is 24 px.
Next: G-18.

### 2026-11-19 01:15 · G-10 The contracts · done
Files: `web/promo/src/content/schema.ts`, `web/promo/scripts/content-contract.mjs`, `web/promo/src/content/films.ts`, `web/promo/src/content/films.json`.
Plan: no layout. `gallery.note` and `story.film` (`alt`, `caption`) are the new keys. `FilmId` now includes `midtun`. The film entry is Appendix C. `getFilm('midtun')` still returns nothing until the poster exists.
Evidence: `node scripts/check-content.mjs` → content check failed (4): `nb.gallery.note`, `nb.story.film`, `en.gallery.note`, `en.story.film`. No other missing keys. No build.
HANDOVER: → DeepSeek: keys landed: `gallery.note`, `story.film.alt`, `story.film.caption`.
Next: G-11 can run beside D-25. No upload.

### 2026-11-19 01:12 · G-9 Load the skills and plan · done
Files: this file only. No code yet.
Plan: skills read, in order: `.agents/skills/minihouse-frontend-design/SKILL.md`; the Claude Code skill at `C:\Users\carlos\.claude\plugins\cache\claude-plugins-official\frontend-design\1.1.1\skills\frontend-design\SKILL.md`; `web/promo/DESIGN.md`; DESIGN-GUIDE R2.5 §6.3, §6.5, §6.6, §6.12, §6.15, §6.16, §7 and §10–§11. Where they differ, the guide wins.
Cards, in order: G-10 contracts, then the HANDOVER. G-11 photos and the steel sample can run beside D-25. After the JSON is filled: G-12 gallery, G-13 materials, G-14 home section and footer, G-15 story page. G-16 only if `images/midtun_teachers_residence_clean_4k.mp4` exists. G-17 only after G-18 passes without it. G-18 checks and screenshots. G-19 upload only after G-18 and D-27.
Checked against the code, and it matches the cards:
- `schema.ts` `gallery` has title, count, prev, next, close, and no `note`. `story` has no `film`.
- `content-contract.mjs` `gallery` is `{ title, count, prev, next, close }` and `story` ends at `teaser`.
- `films.ts` `FilmId` is `'house' | 'living' | 'bath'`. `films.json` has those three entries. `getFilm()` returns nothing without a poster.
- `Film.astro` takes `id`, `class`, `label`, `caption`, `play`, `pause`, `sizes` and `priority`, which is what Appendix E passes.
- `Gallery.astro` `rows` is `['meadow-wide', 'bath-vanity', 'bench', 'bath-shower']` and `['kitchen', 'bath-doorway', 'storage']`. `.tile-caption` is the rule at `base.css` just before `.lightbox`.
- The `64rem` materials block starts with the comment «Gammelt tre, nytt hus: boards stacked in a zig-zag» and uses `4fr 6fr 2fr` and `2fr 6fr 4fr`.
- `story.css` has `.story-teaser p { max-width: min(var(--measure), calc(7 / 12 * 100%)); }` inside `min-width: 64rem`.
- `SiteFooter.astro` first link is Personvern. `imageIds` ends with `texture-stal`, `og-image`. `texture-stal` is `stand-in`, focal `50% 50%`, source the cabin file with no crop note.
No mismatch. Nothing is BLOCKED.
Next: G-10.

### 2026-11-18 23:55 · G-8 Preview upload · done
Files: none in the repo. Upload is deployment `a658a570` at https://minihouse-preview.canner.app.
Plan: D-22 had passed, CR-24 was in the build, and `check_promo.py --dist` had passed, so the bundle went only to `minihouse-preview`.
Evidence: `npm run bundle`, then `canner deploy --slug=minihouse-preview --follow` from `web/promo/.bundle`. Live: `/`, `/en/`, `/historien/` and `/en/historien/` are 200 `text/html`. The language link goes `/historien/` → `/en/historien/` and back. `curl -r 0-1 /film/house-film.mp4` is 206 `video/mp4`. `/.env.production` is 404.
HANDOVER: → DeepSeek: the story page is on minihouse-preview (`a658a570`). D-23 can run.
Next: Carlos looks at the preview for G4. No git.

### 2026-11-18 23:51 · CR-24 phone headings may hyphenate · done
Files: `web/promo/src/styles/story.css`.
Plan (DESIGN-GUIDE §11): below 48rem, `.story h2 { hyphens: auto; }`. From 48rem the headings go back to `hyphens: manual`.
Evidence: `npm run build` 7 pages. `python scripts/check_promo.py --dist web/promo/dist` passed. At 360 px the computed value is `hyphens: auto` and `lang` is `nb`. The first heading still reads `Fra / rivningsmaterialer / til / beredskapsboliger`. `rivningsmaterialer` is 303 px in a 312 px column, so it fits on its own line and this Chrome did not break it. Screenshot `status/grok-screens/h2-nb-360.png`.
Next: G-8.

### 2026-11-18 23:32 · G-6 pictures re-shot after they loaded · done
Files: `status/grok-screens/story-*.png`, `drawing-*.png`, `house-*.png`. No page change.
Plan: the first full-page captures were taken before the lazy images decoded, so the house and the exploded drawing were empty frames. This pass scrolls the page and waits until every `img` has a natural width, then captures again.
Evidence: both story images decoded at 360, 768, 1280 and 1920 in both languages, with no empty frame. At 360 the drawing sits under the first section's text and the house is full width, each with «Konseptbilde» / "Concept image". At 1280 the drawing sits beside that text (490 px) and the house is 800 px wide. The house is the gabled cabin on the slope. The drawing is the roof, the timber body and the steel base, separated.
Definition of done (DESIGN-GUIDE §11): [x] images from images.json, looked at after they loaded  [x] 360/1280 screenshots looked at
BLOCKED: G-8 still waits on D-22.
Next: no upload until that audit passes.

### 2026-11-18 23:40 · G-7 Second read of the Norwegian · done
Files: none edited. Compared `web/promo/src/content/nb.json` with `fase4/promo/content/copy-story.md`.
Plan: his sentences stay as published in the deck. The only allowed differences from Appendix A are the five listed there.
Evidence: 43 keys (`story.*` and `nav.story`), 0 missing, 0 different. The meta description is 131 characters. «Historien», «Les historien», «Prosjektreferanse:» and «Se huset» are plain. The teaser sentence names the demolition and the old timber, and it does not say emergency housing. The reference link stays in the same tab.
HANDOVER: → DeepSeek: no copy change.
Next: G-8 after D-22.

### 2026-11-18 23:38 · G-6 Look, critique, fix · done
Files: `web/promo/src/styles/story.css` (CR-21, CR-22, CR-23, before the screenshots). Screenshots in `status/grok-screens/`.
Plan (DESIGN-GUIDE §6.16): opening gaps of `--space-4`, byline at `--space-2`, the three sections with the same 24 px gap under each h2, motto at `--size-h2` below 48rem and `--size-h1` from 48rem.
Evidence: Playwright, Chrome, full pages of `/historien/` and `/en/historien/` at 360, 768, 1280 and 1920. Home teaser and header at 360, 1024 and 1280. `scrollWidth - innerWidth` was 0 at every width. Opening margins at 360: byline 8 px, then 24 px on each of the nine paragraphs. Section gaps 24, 24, 24 px. Motto computed size 28.16 px at 360 and 72 px at 1280. The question band is the only wood colour. «Historien» sits on one line with the other four links at 1024, and the header does not overflow. Skip link takes the first Tab and shows a solid outline. The wordmark, the reference link and «Se huset» show a solid outline. Escape closes the menu. Language links are `/en/historien/` and `/historien/`, and `hreflang` names both. At 360 the h1 stacks one word a line, which §6.16 accepts. The first h2 also stacks, `Fra / rivningsmaterialer / til / beredskapsboliger`, with wrap and with balance: the long words do not share a line at `--size-h2` in a 312 px column. The question and the motto do not end on a one-word line.
Definition of done (DESIGN-GUIDE §11): [x] tokens only  [x] allowed pairs  [x] copy from content files  [x] images from images.json  [x] keyboard  [x] reduced motion (no motion added)  [x] 360/1280 screenshots looked at  [x] garbage list clear  [x] one accessory removed: the extra `--space-4` on `.story-split`, which doubled the space under the first heading (CR-22)  [ ] D-22's audit is still open
BLOCKED: G-8 waits on D-22.
Next: upload only after D-22 passes.

### 2026-11-18 23:24 · G-5 Checkers · done
Files: none. Build is `web/promo/dist`.
Plan: no layout. D-21 is logged done; the checker already lets the five kept sentences through.
Evidence: `npm run check` 0 errors, content check passed. `npm run build` 7 pages. `python scripts/check_promo.py --selftest` passed. Source run passed. `--dist web/promo/dist` passed: 7 pages, both story pages `h1=1` and `images=2`. `python scripts/verificar_todo.py` → SUITE COMPLETA: TODO PASA.
Next: G-6 and G-7.

### 2026-11-18 23:06 · G-3 Routes and G-4 page · written, check blocked on D-20
Files: `src/pages/historien.astro`, `src/pages/en/historien.astro`, `src/components/Story.astro`, `src/components/StoryTeaser.astro`, `src/styles/story.css`, `src/layouts/Base.astro`, `src/content/locale-paths.ts`, `src/components/SiteHeader.astro`, `src/pages/index.astro`, `src/pages/en/index.astro`.
Plan (DESIGN-GUIDE §6.16): kalk opening in columns 1–8, question on a full-bleed malmfuru band (h2 size below 48rem, h1 from 48rem, follow-up at `--size-h3`), then the three sections with `exploded` beside the first from 64rem, then `hero-slope` in columns 1–8, the motto and «Se huset». The teaser sits after the materials band with a sølvgrå hairline. «Historien» is the fifth link, with `aria-current="page"` on the story page and no hash. `Base` takes optional title and description for the title, the meta description, Open Graph and Twitter.
Evidence: `npm run check` stopped on the two missing `story` properties in `assert-content.ts` (exit 1). `node scripts/check-content.mjs` failed on the four keys above and nothing else. No build, no screenshots, no deploy.
BLOCKED: G-4's passing check, G-5, G-6, G-7 and G-8 wait on D-20, and G-8 also waits on D-21 and D-22.
Next: when the JSON is filled, run the checkers and look at the page.

### 2026-11-18 23:05 · G-2 Content contract · done
Files: `web/promo/src/content/schema.ts`, `web/promo/scripts/content-contract.mjs`.
Plan: no layout. The shape is the one in task-story-page.md: `nav.story` and the `story` group.
Evidence: `node scripts/check-content.mjs` → content check failed (4): `nb.nav.story`, `nb.story`, `en.nav.story`, `en.story`. No other missing keys.
HANDOVER: → DeepSeek: keys landed.
Next: G-3 and G-4 are already written against this shape.

### 2026-11-18 23:02 · G-1 Load the skills and plan · done

Files: this file only. No code yet.

Skills read, in order: `.agents/skills/minihouse-frontend-design/SKILL.md`; the Claude Code skill at `C:\Users\carlos\.claude\plugins\cache\claude-plugins-official\frontend-design\1.1.1\skills\frontend-design\SKILL.md`; `web/promo/DESIGN.md`; DESIGN-GUIDE §1–§6.3, §6.16, §9–§11. Where they differ, DESIGN-GUIDE wins, then DESIGN.md, then the skill.

Subject: Carlos's own account of how the idea started, after he took part in the demolition of the old teachers' residence. Audience: a curious reader, not a buyer. Job of the page: let his Norwegian be read as he wrote it, with one loud moment on the old wood, and the house only at the end.

#### Palette (tokens already in `tokens.css`; no new hex)

| Role | Token | Hex | Where |
| --- | --- | --- | --- |
| Ground | `--kalk` | #ECEAE4 | opening, idea, ending |
| Ink | `--tjaere` | #241A13 | body, h1, h2, motto |
| Heartwood | `--malmfuru` | #9D5F30 | the question band, once |
| Soft wood | `--malmfuru-mork` | #6F3F1E | byline only |
| Copper | `--kobber` | #A9481C | the reference link, the teaser link, the «Se huset» button, focus rings |
| Copper hover | `--kobber-mork` | #8E3B16 | button hover |
| Hairline | `--solvgra` | #8C7E71 | the line above the home teaser |
| Footer | `--tjaere` | #241A13 | existing footer |

Kalk on malmfuru is 4.24:1, so every word on the band is 24 px or larger. Nothing on the band is a link or a button.

#### Type

| Element | Face | Token | Notes |
| --- | --- | --- | --- |
| h1 `story.title` | Besley 800 | `--size-h1` | 44→72 px, `--leading-display`, `letter-spacing: -0.01em`, `text-wrap: balance` |
| Byline | Jost 500 | `--size-small` | `--malmfuru-mork` |
| Lead, origin, closing | Jost 400 | `--size-lead` | 21 px |
| Body paragraphs | Jost 400 | `--size-body` | 18 px, `--leading-text` 1.55, max `--measure` |
| Question | Besley 800 | `--size-h2` below 48rem, `--size-h1` from 48rem | `--kalk`. A paragraph, not a heading |
| Follow-up | Jost 500 | `--size-h3` | 24 px, `--kalk`. A paragraph |
| Section h2 | Besley 800 | `--size-h2` | `--space-6` above |
| Motto lines | Besley 800 | `--size-h1` | `--tjaere`, one line each |
| Button | Jost 500 | `--size-body` | `--kobber` fill, `--kalk` text, `min-height: 48px`, `--radius` |
| Teaser h2 | Besley 800 | `--size-h2` | |
| Teaser body | Jost 400 | `--size-lead` | columns 1–7 |
| Nav «Historien» | Jost 500 | `--size-small` | existing header type |

#### Layout

Left-aligned, ragged right. Side margins `--gutter` at every width. Content never wider than `--max-content`. Section padding `--space-6`, and `--space-7` from 80rem. `--space-4` between paragraphs. No new motion. The story page imports `story.css` from `Story.astro` and `StoryTeaser.astro` and reuses `.wrap` and the existing band classes.

```
1280 px
kalk     h1 Hvordan ideen oppstod          cols 1–8, ≤ 64ch
         Av Carlos
         lead
         intro paragraphs
         Prosjektreferanse:  [copper link]
         noticed paragraphs, last one ends in a colon
malmfuru ████ question in kalk, Besley, cols 1–10
         follow-up, Jost 500, 24 px, cols 1–8
kalk     origin (lead)
         h2 Fra rivningsmaterialer …     | exploded 3:2
         paragraphs, cols 1–7            | cols 8–12, caption
         h2 Å gi gamle materialer …
         paragraphs
         h2 Den større visjonen
         paragraphs
         hero-slope 3:2, cols 1–8, caption
         closing (lead)
         MiniHouse:
         Gamle materialer.
         Nye hjem.
         Et nytt liv.
         [Se huset] → /#bilder
tjære    footer

360 px
kalk     h1, byline, lead, paragraphs, reference link
malmfuru question at h2 size, follow-up at 24 px
kalk     origin, then each h2 and its paragraphs
         exploded under the first section's text
         remaining sections
         hero-slope full width, caption
         closing, motto stack, button
tjære    footer
```

Home, after the materials band: a kalk band, a 1 px sølvgrå hairline on top, h2, one or two sentences, copper link «Les historien». No picture.

Header: fifth link «Historien» after «Spørsmål», in the bar and in the Meny sheet. It points at the story page in the same language and has no hash, so the hash script leaves it alone. On the story page it carries `aria-current="page"`.

#### Principles

Words first, the house last. One loud place: the question on heartwood pine, funk move 5, used once. Copper only on what can be pressed. His sentences stay as written. The old building is never pictured. The page never says the Øvsttunvegen timber is MiniHouse material.

#### Against the skill's defaults and DESIGN-GUIDE §10

The skill's generic cluster is a cream ground, a terracotta accent, a stats hero, cards, eyebrows, and a slide-up on every section. This page does not take that cluster.

| Default | What this page does instead |
| --- | --- |
| Cream near #F4F1EA plus a terracotta accent near #D97757 | Ground stays `--kalk` #ECEAE4. Copper #A9481C is only the link, the button and the focus ring. The wood colour is the band, not an accent on a word. |
| One word of a headline in italic, bold or another colour | The question is one colour and one weight. The motto lines are one colour. No `<strong>`. |
| All-caps eyebrow above the title | No label above the h1. The byline is his name, under the title, in sentence case. |
| Big number, small label, three stats | The opening is his first paragraph. No figures. |
| Identical rounded cards and grey shadows | No cards. Depth is the full-bleed wood band. Elevation stays none. |
| Numbered 01 / 02 / 03 | The three sections are headings, not a timeline. Numerals stay on the journey. |
| Middle dots, "WORD — fragment", monospace, "→" on the button | The reference is a copper underline. The button says «Se huset». |
| Fade-and-slide on every section | No motion on this page. |
| Drop cap, quotation marks, quote card | Refused by §6.16. The question is type on wood, not a pull-quote. |
| A picture of the demolished house | None. `exploded` and `hero-slope` only, both through `Figure` with `ratio="wide"`, both captioned «Konseptbilde». |

The one accessory the plan already leaves out: a hairline under the question, which would make the wood band look like a quoted card. The band is the material. A second accessory comes out after the screenshots, and gets named in G-6.

Next: G-2, the content contract.
