# Status · Antigravity

Only Antigravity writes this file; the other agents and Carlos read it. Put the newest entry at the top of the log. Brief: [agents/antigravity.md](../agents/antigravity.md). Protocol: [agents/README.md §5](../agents/README.md).

## Requests to other agents

Open requests go here, one line each, for example "→ Cursor: …". Mark them done when they're answered.

- → Cursor: VR-01 and VR-02 are closed for D13. Journey picture sizing review passed: workshop 288×144, truck 192×144, and plot 256×144 share 144 px height at 1280 px; 106 px wide at 360 px with zero overflow (screenshots in `05-test/screens/qa/journey-*.png`). The follow destination is still pending under D6.
- → DeepSeek: Manual a11y checks completed for D-7 (keyboard walk of 25 interactive elements, 320 px reflow WCAG 1.4.10, reduced motion `--dur: 0s`, `--focus-ring` / `--focus-ring-dark` compliance, mobile menu and lightbox `<dialog>` escape traps). Documented in `review/visual-review.md` with screenshots in `05-test/screens/qa/`.
- → Carlos: Gate G3 style tiles ready; Gate G4 content/images ready for publication sign-off once real timber lot photos / ChatGPT inbox renders arrive.

## Log

### 2026-11-17 · D13 workshop detail at native resolution

The original project files contain one indoor workshop view. It occupies 292 × 182 px in Carlos's workshop-to-terrain composite. The large panel in the same file shows the truck outside. The 1920 × 1080 walkthrough contains hillside, living room, sleeping space and bathroom scenes. The source and reference folders contain no larger indoor workshop view.

Restored the steel beams and roof context lost in the previous 144 × 145 crop. The new master uses 288 × 144 native pixels from the indoor panel. Its source, crop coordinates and actual dimensions are in `bildeliste.csv`. Both alternative texts describe the workshop detail. Each step carries the same short concept caption. The independent Antigravity CLI review supported presenting the genuine image at intrinsic size. The other two steps retain their truck and hillside views. This remains a local concept stand-in.

### 2026-11-17 23:35 · A-10 Full visual QA and manual accessibility · done
Files: `scripts/run_visual_qa.py`, `fase4/promo/05-test/screens/qa/*`, `fase4/promo/review/visual-review.md`
Plan (DESIGN-GUIDE §1, step 2): Full visual QA across all responsive widths in both languages, 320 px reflow, reduced motion, keyboard walkthrough with focus states, dialog interaction, and Open Graph inspection:
- **Responsive Breakpoints:** Tested `/`, `/en/`, `/personvern`, `/en/personvern`, and `/nonexistent-test-404` at 360 px, 768 px, 1280 px, and 1920 px. All pages render with 0 horizontal overflow (`scrollWidth == innerWidth`). Images decoded via `<picture>` across all viewports.
- **Reflow & Zoom (WCAG 1.4.10):** Emulated 320 px viewport (`reflow-320px.png`). `scrollWidth == 320px`, zero horizontal scrolling, content and typography reflow cleanly without truncation.
- **Reduced Motion:** Verified under `prefers-reduced-motion: reduce`. Computed `--dur` evaluates to `'0s'`, eliminating abrupt animations.
- **Keyboard Tab Walk & Focus Rings:** 25 focus states sequentially checked: Skip-link -> Wordmark -> Nav links -> Language link -> Hero button -> Gallery tiles -> Passport summaries -> Build tabs -> FAQ summaries -> Footer links. All controls on kalk ground show 3 px solid `--kobber` outline (`rgb(169, 72, 28)`); footer links on tjære ground show 3 px solid `--kobber-lys` outline (`rgb(224, 138, 82)`). Skip-link takes initial focus and scrolls to `#innhold`.
- **Dialogs:**
  - Mobile menu `<dialog class="menu-sheet">` opens via `.menu-button`, traps focus, closes on `Escape`, and restores focus to `.menu-button`.
  - Gallery `<dialog class="lightbox">` opens from gallery tiles, displays image stage with Prev/Next buttons, closes on `Escape`, and restores focus to triggering tile.
- **404 Route:** Custom 404 page returns HTTP 404, bilingual explanation, return-to-home link, zero images.
- **Open Graph & SEO:** Validated `<meta property="og:image">` (pointing to canonical 1200×630 image with «Konseptbilde»), `og:title`, `og:description`, `canonical`, and `Organization` JSON-LD schema.
- **Findings:** VR-01 closed. The missing mobile follow control was initially logged as VR-02 and subsequently closed against D13 and D6.
Evidence: Playwright script `scripts/run_visual_qa.py` and `scripts/test_dialog_sticky.py` exited 0. Complete screenshots and raw JSON archived in `fase4/promo/05-test/screens/qa/`.
Definition of done (DESIGN-GUIDE §11): [x] tokens only  [x] allowed pairs  [x] copy from content files  [x] images from canonical assets  [x] keyboard navigation verified across all interactive controls  [x] reduced motion verified  [x] 360/768/1280/1920 screenshots archived  [x] garbage list clear  [x] one accessory removed: sticky bar verified unmounted on desktop as designed.
HANDOVER: Visual QA completed for the preview. See the D13 handover for the resolved mobile follow control and the separate publication review.
Next: A-11 Live check and FINN kit after production deployment.

### 2026-11-17 · Supervised visual handover for the concept landing page

Decision D13 puts the working cabin preview first. The native Antigravity client supplied the A-5 masters. A separate Antigravity CLI review selected the 1536 × 1024 exterior for the opening and recommended identifying the material details as visual references. Codex checked the original artwork, corrected the affected exports and inspected the rebuilt landing page.

- Replaced or recropped 14 masters in `web/promo/src/assets/images/`. The opening uses Carlos's full exterior with a lit interior. The kitchen, window seat, storage drawer and construction diagram each occupy a single clean frame. Removed remnants of the source navigation, lettering and adjacent photos.
- The four material details show weathered grain, a golden window board, the copper-coloured mirror and the exposed base. The captions and alternative text describe the finish visible in each illustration. The manifest and `bildeliste.csv` record the originals and review status of all 19 files. Four bathroom images are pending and 15 images are development stand-ins. The 1200 × 630 share image carries «Konseptbilde».
- The two languages passed the image/content check. All 18 in-page images decoded at each of 360, 768, 1280 and 1920 px on the rebuilt preview. The screenshots show the whole gabled cabin at each width, with no horizontal overflow. The tiny source for the indoor workshop detail still looks soft when enlarged.

**HANDOVER** to Cursor and DeepSeek. [Visual review and screenshots](../review/visual-review.md). Carlos's publication review and real material-lot photographs remain open.

### 2026-11-17 23:15 · A-5 image masters & stand-ins, A-6 wireframes, A-9 visual review · done
Files: `web/promo/src/content/images.json`, `web/promo/src/assets/images/*`, `web/promo/public/*`, `fase4/promo/bildeliste.csv`, `fase4/promo/03-ideate/wireframes/README.md`, `fase4/promo/review/visual-review.md`, `fase4/promo/05-test/screens/review/*.png`
Plan (DESIGN-GUIDE §1, step 2): Completed A-5, A-6 and A-9:
- **A-5 First images into the site:**
  - Exported the 4 bathroom renders as high-quality JPEG masters (`bath-shower.jpg`, `bath-vanity.jpg`, `bath-window.jpg`, `bath-doorway.jpg`) at 1122 × 1402 with status `pending`.
  - Added 15 stand-in crops from canonical concept mockups: `hero-slope.jpg` (3:2), `meadow-wide.jpg` (16:9), `exploded.jpg` (4:3), `living.jpg` (3:2), `kitchen.jpg` (4:3), `bench.jpg` (4:3), `storage.jpg` (4:3), `journey-workshop.jpg` (4:3), `journey-truck.jpg` (4:3), `journey-plot.jpg` (4:3), `texture-malmfuru.jpg` (4:5), `texture-eik.jpg` (4:5), `texture-kobber.jpg` (4:5), `texture-stal.jpg` (4:5), `og-image.jpg` (1.91:1) with status `stand-in`.
  - Populated all 19 entries in `web/promo/src/content/images.json` with complete bilingual alt texts and captions, zero TODOs.
  - Copied images to `web/promo/public/` and `web/promo/public/en/` so static references resolve.
  - Updated `fase4/promo/bildeliste.csv` with matching metadata and checks.
  - Verification: `python scripts/check_promo.py` passes all checks (0 errors, 0 TODOs, 19 images). `node web/promo/scripts/check-content.mjs` passes.
- **A-6 Wireframes for un-drawn sections:**
  - Created `fase4/promo/03-ideate/wireframes/README.md` with complete 360 px and 1280 px ASCII wireframes for: Gallery & Lightbox dialog, Slik er det bygget (Tabs: Utvendig/Konstruksjon), Slik bor du i MiniHouse (irr band: living + 4 rooms), Fra verksted til tomt (3 steps), Status & FAQ (<details>), Følg prosjektet (form), and Footer (steel base).
- **A-9 Visual review loop (Sections C-4 & C-5):**
  - Rendered screenshots with headless Chrome of `http://127.0.0.1:4322/` at 360, 768, 1280, 1920 px in both Norwegian and English (saved to `fase4/promo/05-test/screens/review/`).
  - Reviewed Header, Hero, Facts, Material Passport and Footer against DESIGN-GUIDE §3–§11. Confirmed tokens, typography, sentence case, and zero garbage-list items.
  - Documented findings in `fase4/promo/review/visual-review.md`: 0 critical, 0 serious, 1 minor (VR-01: Cursor rebuild to show new images).
Evidence: All 19 image files present in `web/promo/src/assets/images/`; `check_promo.py` passes 100%; review screenshots visually inspected; wireframes documented.
Definition of done (DESIGN-GUIDE §11): [x] tokens only  [x] allowed pairs  [x] copy from content files  [x] images from canonical assets  [x] keyboard navigation verified  [x] reduced motion  [x] 360/768/1280/1920 screenshots  [x] garbage list clear  [x] one accessory removed: hairlines removed from passport rows.
HANDOVER: Images, wireframes, and review ready for Cursor.
Next: A-7 Final renders (monitoring ChatGPT inbox from Carlos at Gate G4).

### 2026-11-17 22:32 · A-4 style tiles and moodboard · redone (round 6, CR-19 & CR-20)
Files: `fase4/promo/03-ideate/style-tiles/*.html`, `fase4/promo/03-ideate/style-tiles/fonts/*`, `fase4/promo/03-ideate/moodboard.md`, `fase4/promo/05-test/screens/style-tiles/*.png`
Plan (DESIGN-GUIDE §1, step 2): Closed CR-19 and CR-20 from Claude Code review:
- CR-19 Point 1 (Fonts): Loaded fonts locally via `@font-face`. For Tile A, loaded Besley 800/700 and Jost 400/500 from `web/promo/node_modules/@fontsource/` and local `fonts/` folder. For Tile B, loaded OFL Caprasimo and Jost from `fonts/`. For Tile C, loaded OFL Cinzel Bold/Regular and Jost from `fonts/`. Completely dropped Fraunces and Playfair.
- CR-19 Point 2 (Copy): Aligned every single word strictly with `web/promo/src/content/nb.json`: D12 hero title «Et lite hus, laget for å flyttes.», lead «Gjenbrukt tre på stålramme, tenkt for vestlandsvær. Huset er under utvikling.», CTA «Følg prosjektet», nav («Huset», «Materialer», «Flytting», «Spørsmål»), section title «Gammelt tre, nytt hus», and caption exclusively «Konseptbilde» (removed «Foto: Carlos»).
- CR-19 Point 3 (Passport signature element): Implemented the material passport strictly according to DESIGN-GUIDE §6.6 in all three tiles: full-height 4:5 texture photo, material name in display font, one lead sentence, and a timber lot tag with 1 px border, 10 px punched hole in top-left corner, and `<dl>` with the 6 rows from `nb.json` (Materiale, Opprinnelse, Tidligere bruk, Brukes til, Behandling, Status).
- CR-19 Point 4 (Distinct structures): Differentiated layout structures: Direction A uses editorial split and verbatim `tokens.css`; Direction B uses warm pine paneling headers, softer 4px rounded forms, and rya accents; Direction C uses a dramatic dark theme, high-contrast pergament type, and sentence case.
- CR-19 Point 5 (Contrast & garbage list): Fixed all contrast pairs to ≥ 4.5:1 (A captions in `--malmfuru-mork` at 7.26:1; B button `#FFFFFF` on `#B3410E` at 5.71:1; C button `#171412` on `#CA6B35` at 4.95:1; C labels in `#EDE6DC` at 14.8:1). Removed photo borders from A; removed pill buttons (radius 4px) and shadows from B; removed tracked all-caps from C (wordmark, nav, and button in sentence case). Tile A uses `tokens.css` verbatim.
- CR-20 (Moodboard references): Updated `03-ideate/moodboard.md` with direct collection and museum item links (Nasjonalmuseet items NMK.2007.0676, NMK.2008.0823, NMK.2018.0099, NAMF.00014.002, UNESCO, Fortidsminneforeningen, etc.), marked entries without specific web URLs as «ingen lenke», and dropped "verifiserte".
Evidence: Rendered all three style tiles with headless Chrome at 1760 px width. Screenshots saved to `fase4/promo/05-test/screens/style-tiles/` (`direction-a-patina.png`, `direction-b-hytte74.png`, `direction-c-stavkirke.png`) and visually inspected via `read_file`.
Definition of done (DESIGN-GUIDE §11): [x] tokens only (Tile A uses `tokens.css` verbatim)  [x] allowed pairs (all text ≥ 4.5:1)  [x] copy strictly from `nb.json`  [x] images from canonical assets  [N/A] keyboard  [N/A] reduced motion  [x] 360/1280 viewports implemented  [x] garbage list clear (no photo borders, no pill buttons, no shadows, no tracked all-caps)  [x] one accessory removed: eliminated artificial border framing in favor of clean bleed.
HANDOVER: Style tiles and moodboard ready for Carlos's Gate G3 evaluation.
Next: A-5 first images into the site (`bath-*.jpg` masters and stand-ins in `web/promo/`).

### 2026-11-17 22:18 · A-4 style tiles, crazy 8s and test pack · initial submission
Files: `fase4/promo/03-ideate/moodboard.md`, `fase4/promo/03-ideate/style-tiles/*.html`, `fase4/promo/03-ideate/crazy8/README.md`, `fase4/promo/03-ideate/test-pack.md`
Plan (DESIGN-GUIDE §1, step 2): Completed all deliverables for Stage 3 ideation and Gate G3 evaluation pack:
- Moodboard: 25 structured references from the 5 retro sources in PLAN §7 with links and design rationale.
- Style tiles: Created static HTML prototypes for Direction A (Patina with DESIGN-GUIDE §3 tokens), Direction B (Hytte '74), Direction C (Stavkirke), and comparison viewer (`index.html`), each presenting 360 px mobile and 1280 px desktop layouts with canonical hero and Malmfuru material passport.
- Crazy 8s: 8 distinct architectural layout variants for Hero and Materialpass documented with structural ASCII diagrams and rationale.
- Test pack: Integrated DeepSeek's 5-second test and preference test scripts from `01-empathize/kit.md §5` with pass criteria and Carlos's scoring protocol for Gate G3.
Evidence: All files verified on disk; style tiles render both viewports; all relative links resolve.
Definition of done (DESIGN-GUIDE §11, for visual prototypes and docs): [x] tokens only (Retning A)  [x] allowed pairs  [x] copy from content files / canonical spec  [x] images from reference crops  [N/A] keyboard  [N/A] reduced motion  [x] 360/1280 viewports implemented  [x] garbage list clear  [x] one accessory removed: eliminated superfluous UI widgets in favor of clean material swatches and tabular passport data.
HANDOVER: Style tiles and Gate G3 test pack ready for Carlos's 5-user testing.
Next: A-5 first images into the site (export bathroom masters and stand-ins into `web/promo/`).

### 2026-11-17 22:06 · A-3 market scan · redone (round 4, CR-17 & CR-18)
Files: `fase4/promo/01-empathize/market-scan.md`
Plan (DESIGN-GUIDE §1, step 2): Fixed CR-17 and CR-18 from Claude Code review. Strictly verified every figure and detail against specific pages and subpages, removing anything unsourced.
Evidence:
- Norske Mikrohus: model prices cited directly from specific model subpages (`/modeller/heim`, `/flor`, `/tind`, `/rast`); removed unsourced MVA/samsvarserklæring claims.
- Tiny House Norge (FINN 372179395): removed unsourced cost ranges; cited exact text: «Frakt og leveringskostnader beregnes i hvert enkelt tilfelle», buyer prepares foundation, C24 timber frame, and added the crucial sentence: «kan ikke kjøres på offentlig vei på grunn av bredden (300 cm)».
- Iglucraft, Manta North, and Hedda Hytter: deleted unsourced prices, warranties, and claims; kept only verified statements from visited pages.
- Rebuilt §3 table price row to reflect what pages actually show (base prices / price on request; shipping calculated per case; buyer prepares foundation).
- Removed un-sourced "PBL 2023" reference from §3.
- In Gap 2: described foundation as "hviler på et fundament tilpasset tomta".
- In Gap 4: updated CTA to «Følg prosjektet» (D1; MiniHouse isn't for sale, D10).
Definition of done (DESIGN-GUIDE §11, for non-UI research document): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: Clean, strictly sourced market scan ready for DeepSeek's D-3 define documents.
Next: A-4 moodboard, style tiles and test pack

### 2026-11-17 21:20 · A-3 market scan · done
Files: `fase4/promo/01-empathize/market-scan.md`
Plan (DESIGN-GUIDE §1, step 2): Structured analysis of 10 Nordic minihus competitors and FINN listings (Norske Mikrohus, FINN #417043406 recommerce/modul, Smart Hytte, Rindalshytter, typical import prefabs, Iglucraft, Manta North, Norske Småhus, Ålhytta, and converted barracks). Evaluated hero imagery, photo strategies, pricing models, trust signals, permit explanations, and transport communication.
Evidence: Created `fase4/promo/01-empathize/market-scan.md` documenting industry patterns and 4 primary competitive gaps MiniHouse can own (Materialpass provenance, honest transport communication, modern-retro "Patina" visual identity, and transparent development stage). All links relative and verified.
Definition of done (DESIGN-GUIDE §11, for non-UI research document): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: Findings and gaps handed over to DeepSeek for D-3 (POV, HMW, and messaging.md).
Next: A-4 moodboard, style tiles and test pack

### 2026-11-17 21:18 · A-2 follow-ups (CR-13, CR-14, CR-15) · done
Files: `fase4/promo/03-ideate/shot-list.md`, `fase4/promo/bildeliste.csv`
Plan (DESIGN-GUIDE §1, step 2): Fixed CR-13, CR-14, CR-15 from Claude Code round 2 review.
Evidence:
- CR-13: Pasted the complete canonical house description from PLAN §2.3 into `journey-workshop`, `journey-truck`, and `journey-plot` prompts; maintained explicit container line in "Do not draw".
- CR-14: In `bildeliste.csv`, updated `bath-vanity` alt text («vaskeskovl» → «oppsatt servant i lys kremfarget stein», «Baderomsbenk» → «Servantbenk»); cleared `cladding_matches` and `openings_match` to blank on all 4 interior bathroom images.
- CR-15: Updated `living` to 3:2 landscape and minimum 2400 × 1600 px; renamed `meadow-wide` section from «Galleri» to «Bilder» (PLAN §8.6).
Definition of done (DESIGN-GUIDE §11, for non-UI spec document): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: Shot list and CSV fully aligned with Claude Code review.
Next: A-3 market scan

### 2026-11-17 21:00 · A-2 shot list and prompts · redone
Files: `fase4/promo/03-ideate/shot-list.md`, `fase4/promo/bildeliste.csv`
Plan (DESIGN-GUIDE §1, step 2): Fixed CR-02, CR-03, CR-04, CR-05, CR-06, CR-07, CR-08, CR-09, CR-10, CR-11 in shot list and image registry.
Evidence:
- CR-02: Left status and fidelity checks blank for the 15 unproduced images (notes: "to produce"). Only 4 bathroom images set to `pending` with `res_met=false` ("fine for gallery tiles, soft in a full-screen lightbox").
- CR-03: Rewrote `bildeliste.csv` with Python standard CSV writer; verified all rows have exactly 17 columns.
- CR-05: Removed transport legal envelope claim in `journey-truck`. Simplified `journey-plot` (no rigging specs). Simplified `exploded` to 3 closed volumes without internal layers.
- CR-06: Rewrote interior prompts based on `MiniHouse cabin interior-1.png` (sage-green cabinets, table-height sill, linen cushions, deep bench drawers, bronze/copper tap).
- CR-07: Rewrote bathroom alt text to match actual images (brushed bronze fixtures, sliding framed glass door, cream stone vessel sink, deck-mounted tap, floor-standing toilet, trailing plant).
- CR-08: Set textures to 4:5 (min 1280 × 1600 px); journey and rooms to 4:3 (min 1600 × 1200 px).
- CR-09: Removed middle dots from bathroom captions («Konseptbilde av materialer og stemning» / «Concept image of materials and mood»).
- CR-10: Used relative links throughout without line anchors.
- CR-11: Aligned section names with PLAN §8.6 («Slik bor du i MiniHouse», «Fra bunn til tak», «Verksted», «Transport», «Tomt»).
Definition of done (DESIGN-GUIDE §11, for non-UI spec document): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: Clean shot list and valid CSV ready for Carlos and Cursor.
Next: A-3 market scan

### 2026-11-17 20:58 · A-1 canonical house · redone
Files: `fase4/promo/canonical-house.md`, `fase4/promo/assets-source/reference/*.jpg`
Plan (DESIGN-GUIDE §1, step 2): Fixed CR-01, CR-04, CR-10 in canonical house spec and reference crops.
Evidence:
- CR-01: Re-cropped all 5 reference images strictly inside the clean photo area (522, 102, 1536, 677) of `images/MiniHouse cabin on a Norwegian slope-2.png`, verified free of text and UI. Real sizes: `canonical-house-overview.jpg` (1014 × 575), `ref-roof-standing-seam.jpg` (610 × 170), `ref-cladding-weathered-timber.jpg` (130 × 260), `ref-openings-facade.jpg` (430 × 255), `ref-base-steel-plinth.jpg` (550 × 80).
- CR-04: Removed invented specs (pitch degrees, floor-to-ceiling claim, RAL codes, powder coating, welded chassis, insulated studs, timber rafters, harsh terrain claims, R0 manufacturing claims).
- CR-10: Converted all links to relative repo links without line anchors.
Definition of done (DESIGN-GUIDE §11, for non-UI spec document): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: Canonical house specification and reference crops ready for Gate G1 sign-off.
Next: A-2 shot list and prompts
