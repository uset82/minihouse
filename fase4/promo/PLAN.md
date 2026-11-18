# MiniHouse · Promotional website · Build plan R2

**Revision R2, 2026-11-18.** Replaces R1 of 2026-11-17. R1 wrongly turned Carlos's separate design-thinking course into research stages, tests and gates. R1 and that material are archived in [archive/design-thinking/](archive/design-thinking/README.md) (decision D14). Older status logs and reviews cite R1 section numbers. §1 and §2 keep their numbers here; any other R1 number refers to the [archived R1](archive/design-thinking/PLAN-R1.md).

Role: frontend-designer, with the [project frontend skill](../../.agents/skills/minihouse-frontend-design/SKILL.md). The look is specified in [DESIGN-GUIDE.md](DESIGN-GUIDE.md), Carlos's answers are in [decisions.md](decisions.md), and who does what is in [agents/README.md](agents/README.md).

## The goal

Build a landing page that presents MiniHouse the way [the MAYA listing on FINN](https://www.finn.no/recommerce/forsale/item/417043406?ci=3) presents its house: pictures first, then the key facts, then the details. It shows **our** house, from Carlos's concept images in [images/](../../images/), in Bokmål and English (D13).

The look is **modern retro Norwegian**, built on old, reclaimed and renewable timber. It uses copper and the natural colours of **malmfuru** (heartwood pine) and **eik** (European oak). It must feel **modern and funky**, never templated (D14, G3).

The work is: build the page, check it, show it to Carlos.

---

## 1. Brief

- **The house.** MiniHouse is a small house of about 6 × 3 m with a steel base, reclaimed timber and a gable roof. It is designed in Bergen to be moved in one piece by truck and crane. It is under development and isn't built yet, so every picture is a concept.
- **What the site does.** It shows the house and invites people to follow the project with «Følg prosjektet» (D1).
  - MiniHouse **isn't for sale** (D10): no price, no ordering and no sales wording.
  - It **isn't presented as an emergency cabin** (D11). It's a minihouse, like other minihouses.
- **Who it's for.** People who like small houses: homeowners with a plot, cabin owners and the curious. Professionals such as builders and crane or transport firms follow «For fagfolk» to the documentation site.
- **What we borrow from FINN:** the order of information only. That means pictures, key facts, the description and an honest note on status, but not its look, text, photos or the sale (Appendix A).
- **Languages:** Bokmål at `/`, English at `/en/` (D3).
- **Not in scope:** a price, ordering, an AI chat on the page, the 3D lab and a configurator.

---

## 2. The house we show (image fidelity)

Every image of the house is a concept and carries the caption «Konseptbilde» / "Concept image". Antigravity keeps the full spec in [canonical-house.md](canonical-house.md).

### 2.1 What every image of MiniHouse must show

This is taken from Carlos's six exterior and interior concepts.

- One storey, a long rectangle roughly 2:1 in plan.
- A symmetrical gable roof in black standing-seam metal, with slim eaves.
- Vertical reclaimed boards with natural variation. The weathered silver-brown of the *slope* and *meadow* images is the reference tone.
- On the long façade: a solid black door left of centre and one large black-framed picture window. A small black-framed window on the gable end.
- A dark steel base that reads as a thin plinth. No exposed steel frame on the walls, no container corner castings, no stilts, no wheels.
- Setting: Western Norway, with fjord, birch, rock and heather under soft overcast light.
- Interior: pale pine panelled walls, a built-in bench with storage, a small kitchen with green fronts and a fold-down table. The bathroom has petrol-green glazed tile, a wavy copper mirror, a reclaimed-timber vanity and an oak window frame.

### 2.2 Settled questions

Carlos answered the questions about the door, base, cladding tone, openings and bathroom captions on 2026-11-17. The answers are under "Canonical house questions" in [decisions.md](decisions.md). No dimensions are taken from images ([registro F](../../fase1/registro-decisiones.md)).

### 2.3 Canonical prompt for clean re-renders

Carlos made the originals in ChatGPT, so the most faithful clean versions come from the same tool, ideally in the same conversation.

> Photorealistic architectural photograph. No text, no website interface, no logos, no watermark. A small single-storey house about 6 m long and 3 m wide with a symmetrical gable roof in black standing-seam metal. Walls of vertical reclaimed timber boards, weathered silver-brown with natural variation. On the long façade: a solid black door left of centre and one large black-framed picture window; a small black-framed window on the gable end. A slim dark steel base. Setting: grassy slope above a fjord in Western Norway, birch trees, mossy rocks, soft overcast daylight. Eye-level three-quarter view. Landscape 3:2, at least 2400 px wide.
> Do not draw: a shipping container, a flat roof, a steel frame around the walls, stilts, wheels.

The scene prompts for each image id are in [shot-list.md](shot-list.md).

### 2.4 Fidelity checklist

Run this for each image and record the result as a row in [bildeliste.csv](bildeliste.csv).

- [ ] Roof form matches §2.1
- [ ] Cladding direction and tone match
- [ ] Door and window arrangement matches
- [ ] Base matches; nothing that looks like a container
- [ ] No text, UI or watermark
- [ ] Resolution: at least 2400 px for the hero, 1600 px for sections
- [ ] Caption and alt text written in Norwegian and English
- [ ] Approved by Carlos

### 2.5 Rejected images

Never publish these: `web/chat-demo/public/concepts/*.jpg` and Antigravity's `hero_*`, `detail_*`, `exploded_*` and `minihouse_*` renders. They show a flat-roofed container on stilts with a fake browser frame, and false claims are baked into the pictures. They're archived in `archive/rejected-renders/` with a README that says why.

---

## 3. Decisions in force

The full wording and dates are in [decisions.md](decisions.md).

| | Decision | What it means for the page |
|---|---|---|
| D1 | «Følg prosjektet» | the only call to action: visitors leave an e-mail address for project news |
| D3 | Bokmål first, plus English | `/` and `/en/` |
| D6 | where sign-ups go: **still open** | no follow form and no copper band until Carlos names the inbox and the form service |
| D10 | not for sale | no price, no «Pris kommer», no ordering or sales words |
| D11 | not an emergency cabin | shown as a minihouse, like other minihouses |
| D12 | the hero title | «Et lite hus, laget for å flyttes.» / "A small house, made to be moved." |
| D13 | a working landing page | exterior, living space and materials, in both languages |
| D14 | no design-thinking process | build, check, show Carlos |
| G3 | «Patina, made funkier» | §4 |

---

## 4. The look: Patina, made funkier

**Patina is the idea:** good materials get better with age. Old malmfuru weathers to silver, oak darkens and copper turns green (*irr*). Every colour on the page is a material of the house.

| Colour | Material | Job on the page |
|---|---|---|
| kalk `#ECEAE4` | lime-plaster walls | page ground |
| tjære `#241A13` | pine tar | text, the footer |
| malmfuru `#9D5F30` | heartwood pine | wood surfaces, large numerals |
| eik `#BA936B` | oak | the key-facts band |
| kobber `#A9481C` | copper | everything you can press |
| irr `#2C4F40` | petrol-green tile | the interior band |

The type is **Besley** for headings and numerals, a revival of Clarendon, the 19th-century wood type. **Jost** sets the text. The tokens, colour pairs and rules are in [DESIGN-GUIDE.md](DESIGN-GUIDE.md) §3.

**The built site keeps this look.** Four funk moves make it bolder, and each one comes from a real part of the house:

1. **The wavy copper mirror frame, «speilramme».** It traces the bathroom mirror and is used once: the bath photo in the interior band hangs in it. It's the one copper shape you can't press (DESIGN-GUIDE §6.14).
2. **A bold irr band, «Inne i MiniHouse».** Full-bleed petrol green with a large heading, and the living-room photo beside the mirror (§6.8).
3. **Giant wood-type numerals.** The journey's 1, 2 and 3 are set in Besley 800 in malmfuru, overlapping the top of each step's photo (§6.9).
4. **A copper follow band, «Følg prosjektet».** Full-bleed copper with kalk text and an inverted kalk button. It's built only after D6 (§6.11).

The built example is in [reference/](reference/index.html). Open `index.html` to see it at 360 px and 1280 px side by side. Cursor copies from it, and only Claude Code edits it.

**The house moves (2026-11-18).** Carlos's concept film plays by itself, silently, in the hero. Its living-room and bathroom shots keep playing in «Inne i MiniHouse», the bathroom inside the copper mirror, so the film runs through the page rather than sitting in a box. One «Pause filmen» button stops all of it. Reduced motion and Data Saver show the stills instead (DESIGN-GUIDE §6.15).

---

## 5. Page sections: built and left

The section order, anchors and content keys are in [content/sitemap.md](content/sitemap.md).

| # | Section | In `web/promo` now | Left to do |
|---|---|---|---|
| 1 | Hero «Et lite hus, laget for å flyttes.» | built; Carlos's concept film plays by itself, silently, bleeding off the right edge | Carlos approves the film cuts at G4 |
| 2 | Nøkkelinfo (eik band) | built | – |
| 3 | Inne i MiniHouse (irr band) | built, the funk version; the living-room film plays, and the bathroom film plays inside the mirror; moved up | remove the unused `living.rooms` keys (Cursor, DeepSeek) |
| 4 | Huset i bilder (gallery and lightbox) | built as a contact sheet of 7 uncropped pictures | – |
| 5 | Gammelt tre, nytt hus (material passports) | built; passports always visible, compact on phones, tags hanging off their samples on desktop | replace the steel image, which shows mostly wood cladding (Antigravity) |
| 6 | Under kledningen | built; both views side by side, no tabs | – |
| 7 | Fra verksted til tomt (journey) | built with giant numerals over 4:3 pictures | a workshop image of at least 1600 × 1200 (Carlos renders it, Antigravity checks it) |
| 8 | Hvor langt har vi kommet? (status and FAQ) | built | – |
| 9 | Følg prosjektet (copper band and form) | not built | waits for D6 |
| 10 | Footer (steel base) | built | a contact address (K-29) |
| – | Personvern, 404, sitemap, robots | built | the privacy text waits for D6; check that Canner serves a real 404 |

The sticky mobile bar exists but stays off until the form exists. Review findings are in [review/visual-review.md](review/visual-review.md), and QA reports are in [qa/](qa/a11y.md).

---

## 6. Content rules

- Every factual sentence on the site has a row in the [claims register](content/claims-register.csv). No row, no sentence.
- Every image of the house carries «Konseptbilde» / "Concept image" below it.
- Malmfuru and eik are «planlagt» (planned) until the reclaimed lot is documented (C-08). Pressure treatment is «ikke bestemt».
- Never claim that no building permit is needed, TEK17 compliance, U-values, a price, a delivery time, a weight or «verifisert».
- The copy lives in `web/promo/src/content/nb.json` and `en.json`. The rules for words are in DESIGN-GUIDE §9.

---

## 7. Images

- The masters are in `web/promo/src/assets/images/` and listed in `images.json` with alt text, captions, source and status. They stay on this PC and out of git, because the repo is public.
- **Missing or wrong:**
  - `texture-stal` (336 × 420) shows wood cladding, not steel. Replace it with a steel close-up of the base, cropped from the concept images or newly rendered.
  - `journey-workshop` is 288 × 144. The bigger journey layout needs at least 1600 × 1200 at 4:3. Carlos renders it with the shot-list prompt, and Antigravity checks it.
  - The mirror frame now plays the bathroom shot of the film. Its fallback still is `bath-window` (1122 × 1402).
  - Every section image is still below the 1600 px bar, and the hero is below 2400 px ([asset check](qa/asset-check.md)).
- **`images/` changed on 2026-11-18 between 06:38 and 07:12, from outside this project's agents:**
  - two new bathroom renders appeared;
  - four bathroom renders disappeared, including the sources of `bath-shower` and `bath-doorway`;
  - the walkthrough was replaced by a 17.02 s cut.

  The site's masters are copies, so nothing on the page broke. Antigravity re-checks the image sources in `bildeliste.csv`.
- **The concept film** (DESIGN-GUIDE §6.15): Carlos asked on 2026-11-18 for «an automatic video presentation of the house» that is part of the whole site.
  - `scripts/cut_film.py` cuts his walkthrough into three silent loops: the whole film for the hero, the living room, and the bathroom inside the mirror.
  - They are listed in `films.json`, with the posters in `src/assets/film/` and the videos in `public/film/`, all out of git.
- New images follow §2: the canonical prompt, the fidelity checklist and a row in `bildeliste.csv`.
- Only Carlos approves images and the film cuts, at G4. A release build fails on any image or film marked `stand-in` or `pending`.

---

## 8. Work per agent

The file ownership, contracts and protocol are in [agents/README.md](agents/README.md), with one brief per agent. In short:

- **Cursor** (code) tidies Claude Code's funk build (C-12b), builds the copper band after D6, fixes review findings, and deploys only with Carlos's OK.
- **Antigravity** (images and visual QA) replaces the steel texture, prepares the workshop and mirror images, and screenshots every change at 360, 768, 1280 and 1920 px.
- **DeepSeek** (words and checks) keeps the copy, the claims register and `check_promo.py` current, and re-runs the checks after each build.
- **Codex**, if Carlos uses it as a supervisor, follows the same rules and edits only what its task names.
- **Claude Code** keeps this plan, the design guide and the reference. On 2026-11-18 Carlos asked it to work on the site itself, so it built three things in `web/promo` ([its log](status/claude-code.md)):
  - the funk layer and the section polish;
  - four UX fixes;
  - the concept film.

---

## 9. Launch

1. **D6:** Carlos names the inbox and the form service. Then Cursor builds the follow form in the copper band, and DeepSeek writes the privacy text.
2. **G4:** Carlos approves the content and images for publication. This also closes the first Fase 4 box in [PROJECT.md](../../PROJECT.md).
3. **G5:** Carlos approves the launch.
4. **Deploy,** by Cursor with Carlos's OK:
   1. Move the lab to `minihouse-lab` first.
   2. Run `npm run build:release`, then `npm run bundle`, with the system Node. The bundle adds `deploy/serve.mjs`, a small server with byte ranges, the right file types and a real 404. Canner's own static server has none of these, and Safari can't play the film without byte ranges.
   3. From `web/promo/.bundle`, run `canner deploy --slug=minihouse --follow`. **Never use `canner redeploy`** ([despliegue-web.md](../../docs/despliegue-web.md)).
5. **After the deploy:** check every route and image, the link previews and the 404 page. Then DeepSeek updates the Fase 4 boxes in PROJECT.md with the evidence.
   - **The film needs byte ranges.** Check that `curl -r 0-1 https://minihouse.canner.app/film/house-film.mp4` returns 206 with `video/mp4`, and that `/.env.production` returns 404. The bundle's server does both on the preview.
6. **Git:** only on `web/promo-r1`, only the promo files, and only when Carlos says so.

Where things live:

- `minihouse.canner.app`: the promo site. It shows the holding page until G5.
- `minihouse-preview.canner.app`: a preview of the promo site, so Carlos can see it online before G4 and G5. It was created on 2026-11-18 at his request, is upload-only, and is not linked to GitHub. Anyone with the link can open it. Update it from `web/promo/.bundle` with `canner deploy --slug=minihouse-preview --follow`.
- `minihouse-lab.canner.app`: the chat and the 3D lab, after the move.
- `minihouse-docs.canner.app`: the documentation site.

---

## Appendix A · What we take from the FINN listing

Seen on 2026-11-17; we noted the structure only. The MAYA listing opens with a 12-image gallery, then a keyword-packed title, «Til salgs» with the price, the condition, an emotional paragraph and a practical one. Price details follow, then a «MERK» note (every house is built to order, and the photos show options), the delivery time, the company's story, the contact box and more models from the seller.

- **MiniHouse takes:** pictures first, a key-facts block where FINN has the price, a short honest note on status, a clear answer about moving, and a contact box in the footer.
- **MiniHouse leaves out:** the price and everything about buying (D10), the trailer, the keyword-packed title and the list of models.

## Appendix B · Where the files live

```
fase4/promo/
  PLAN.md               this plan
  DESIGN-GUIDE.md       tokens, components, garbage list, definition of done
  decisions.md          D1–D14 and the gates, with Carlos's words
  agents/               who does what, plus one brief per agent
  status/               one log per agent
  reference/            the built example (Claude Code)
  content/              claims register, sitemap, copy decks
  canonical-house.md    the house every image must show
  shot-list.md          image prompts
  bildeliste.csv        one row per image
  qa/                   accessibility, performance, claims audit, screenshots
  review/               visual review and Claude Code's review
  archive/              rejected renders and the design-thinking material (don't use)
web/promo/              the Astro site
scripts/check_promo.py  automated checks
```
