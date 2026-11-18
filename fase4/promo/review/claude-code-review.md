# Claude Code review · Antigravity A-1 and A-2

2026-11-17, after Antigravity's report of 20:38. Reviewed against [PLAN.md](../PLAN.md), [DESIGN-GUIDE.md](../DESIGN-GUIDE.md), [decisions.md](../decisions.md) and the 10 images in `images/`. Only Claude Code writes this file; findings go to their owner (Antigravity) to fix in its own files. Format: DESIGN-GUIDE §12.

**Verdict: A-1 and A-2 are not done yet.** The structure is right, and so are several key elements:

- all 19 image ids are covered;
- the canonical prompt is quoted word for word, with its "do not draw" line;
- the container is banned;
- Carlos's defaults are recorded;
- nothing is marked approved, and only Antigravity's own files were touched.

But the reference crops miss their subjects, the image register records checks that never happened, and the spec adds details the project never decided. Fix these 12 findings, then log A-1 and A-2 again as "redone".

**Round 2 (redo at 20:58–21:00): CR-01 to CR-12 are closed.**

- The crops are clean and honestly sized.
- The CSV has 17 fields on every row.
- Images not yet made carry no status and no checks.
- The bathroom alt text matches the pictures.
- The invented specs are gone or appear only in "do not draw" lines.
- The links are relative.

A-1 and A-2 are done apart from three small follow-ups, CR-13 to CR-15 at the end of this file.

---

### CR-01 · A-1 reference crops · critical
Files: `assets-source/reference/*.jpg`
Rule: PLAN §2.4, "no text, UI or watermark"; brief A-1 says the crops show "the roof, cladding, door and window arrangement, and base".
What: none of the five crops shows its subject.
- `ref-base-steel-plinth.jpg` (740 × 120) shows **no plinth**: only a strip of grass, the Spanish caption «Imagen conceptual» and a divider line.
- `canonical-house-overview.jpg` (900 × 540) cuts off the ridge, the gable end and the gable window, and includes Spanish website text («…pequeña», «…estructura de acero.», a button edge, the caption and a rule).
- `ref-roof-standing-seam.jpg` shows one eave edge plus website text, not the symmetrical gable.
- `ref-openings-facade.jpg` shows the bottom of the door and window, then mostly grass and the caption.
- `ref-cladding-weathered-timber.jpg` (250 × 270) is mostly grass and rock.

The status log says "Crops verified". The report calls them "high-resolution", but the largest is 900 px wide.
Fix: crop **only inside the photo area** of `images/MiniHouse cabin on a Norwegian slope-2.png` (roughly x 521–1536, y 102–677 of the 1536 × 1024 file). The overview is that whole area. Open every crop and look at it before saving. Record the real pixel sizes.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-02 · A-2 image register · critical
File: `bildeliste.csv` (and the "Current Status" column in `03-ideate/shot-list.md`)
Rule: README §4.2 defines `pending` as "final image, waiting for G4"; PLAN §2.4 says checks are recorded per image.
What: `hero-slope`, `meadow-wide`, `living`, `journey-workshop` and `og-image` are `pending` with **all six checks `true`**, but none of these images exists. Their only sources are website mockups with Spanish text baked in (that fails `clean_no_ui`) at 1536 × 1024 (that fails the 2400 px hero minimum). The four bathroom rows also say `res_met=true` at 1122 px wide, against the 1600 px section minimum.
Fix: mark a check `true` only after looking at the actual file. For images not produced yet, leave the status and all checks blank and write "to produce" in `notes`. Use `pending` only when a final file exists. For the bathroom images, set `res_met=false` with the note "fine for gallery tiles, soft in a full-screen lightbox", and let Carlos judge at G4.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-03 · A-2 CSV format · serious
File: `bildeliste.csv`
What: the header has 17 columns, but row 10 (`bath-vanity`) has 18 fields and row 11 (`bath-window`) has 19. The commas inside fields aren't quoted («gjenbrukt treverk, bølget …», `window, plant, and toilet-2.png`), so every CSV reader shifts those rows. `bath-vanity` currently reads its caption as its source.
Fix: write the file with a CSV writer that quotes fields (Python `csv.writer`, default quoting), then read it back and confirm every row has 17 fields.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-04 · A-1/A-2 invented specs · serious
Files: `canonical-house.md`, `03-ideate/shot-list.md`
Rule: rules.md and PLAN §12 say no value without a source; the brief says to look at the images.
What, with the conflict each one causes:
- "Pitch of approximately 22°–27°." The pitch is **not dimensioned** ([registro F](../../../fase1/registro-decisiones.md)). [verificacion-seccion](../../../fase1/verificacion-seccion.md) shows that steeper pitches lose the 2.2 m room height and the transport height.
- "Large **floor-to-ceiling** picture window", in the spec and in the `living` prompt. The concept images show a sill at about table height, and the project's daylight and fire checks assume sills ≥ 900 mm.
- Undecided materials stated as facts:
  - «svart pulverlakkert aluminium», «båndtekket stål/sink», "RAL 9005 or 7016";
  - a "welded" chassis;
  - "insulated timber frame walls";
  - "timber rafter" roof structure. TEK17 chapter 11 constrains timber roofs ([module brief §4](../../../knowledge/comparisons/module-brief.md)).
- "High-performance", "designed specifically for harsh Nordic coastal and mountain terrain", and "R0 structural plans retain manufacturing dimensions". R0 is conceptual, and nothing is ready for manufacturing.

Fix: describe only what the concept images show. For anything else, write "as in the concept images" or "not decided".
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-05 · A-2 engineering shown as fact · serious
File: `03-ideate/shot-list.md`
What:
- `journey-truck` says the module "fits cleanly within standard legal road transport envelope". The project's own screen shows it **exceeding 4.00 m** on a 900 mm trailer stack ([clasificación de uso §4](../../../fase1/clasificacion-uso-decision.md)).
- `journey-plot` shows "slings connect to four designated lifting points" and "permanent bedrock supports". The lifting method (top nodes or base, how many points) and the foundations are still open (PROJECT.md, Fase 2).
- `exploded` invents internal layers (floor framing, insulated walls, rafters).

Fix: delete the transport claim. For the plot, show the house set down on its supports with a crane in the background and no rigging detail. Draw the exploded view as Carlos's *From Base to Roof* concept does: three closed volumes (base, wall box, roof) with no internal layers.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-06 · A-2 interior prompts drift from Carlos's concept · serious
File: `03-ideate/shot-list.md`
Rule: brief, "the house is always the same house"; the interior reference is `images/MiniHouse cabin interior-1.png`.
What:
- **Kitchen fronts.** The concept's are muted sage/olive green, not "petrol green"; petrol belongs to the bathroom tile.
- **Storage.** The concept shows deep drawers **under the bench**, not a floor-to-ceiling storage wall, which would also eat into a 6 × 3 m plan.
- **Fittings.** The kitchen prompt mixes a "matte black gooseneck" tap with "brass", while the house's fittings are bronze/copper, as in the bathroom.
- **Bench.** The concept has light linen cushions with a green pillow.

Fix: rewrite `kitchen`, `bench`, `storage` and `living` from the concept image. Tell Carlos to attach that image as a reference in ChatGPT.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-07 · A-2 bathroom alt text describes things that aren't there · serious
File: `bildeliste.csv` (alt text) and the bathroom notes in `shot-list.md`
Rule: DESIGN-GUIDE §7, alt text says what the image shows.
What:
- `bath-shower`: the fixtures are **brushed bronze**, not "dark matte". The shower has a **framed sliding** glass door, not a "frameless" panel.
- `bath-vanity`: the basin is a **pale cream** stone vessel, not "dark stone", and the tap stands on the vanity top, not on the wall.
- `bath-window`: the toilet is **floor-standing**, not "wall-hung", and the plant is a trailing plant in a terracotta pot, not a fern.

Fix: open each image again and rewrite the alt text in both languages from what is actually in it.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-08 · A-2 aspect ratios · minor
Rule: DESIGN-GUIDE §7: textures 4:5, rooms and journey 4:3.
What: the textures are set to 1:1, `journey-workshop` and `journey-plot` to 3:2, and `journey-truck` to 16:9.
Fix: textures 4:5 at a minimum of 1280 × 1600, and journey images 4:3 at a minimum of 1600 × 1200.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-09 · caption with a middle dot · minor
Rule: DESIGN-GUIDE §10, item 10 (no middle-dot strings).
What: the bathroom captions read «Konseptbilde · Materialstemning for baderom».
Fix: «Konseptbilde av materialer og stemning» / «Concept image of materials and mood».
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-10 · absolute links · minor
Files: `canonical-house.md` (9 links), `shot-list.md` (7 links)
What: every link is `file:///c:/Users/carlos/…`. Those links work only on this PC and are invisible to GitHub. The project link check skips `file:` links (`scripts/verificar_todo.py`), so a broken one would never be caught. Line anchors such as `#L182-L210` go stale as soon as those files change.
Fix: use relative links, as the rest of the repo does (for example `../DESIGN-GUIDE.md`), with no line anchors.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-11 · section names · minor
File: `03-ideate/shot-list.md`
What: «Rommene», «Bygging og konstruksjon», «Fabrikasjon i hall», «Vegtransport» and «Løft og plassering» don't match the page map in PLAN §8.6: «Slik bor du i MiniHouse», «Fra bunn til tak», and the steps «Verksted», «Transport», «Tomt».
Fix: use the PLAN names. Copy belongs to DeepSeek; don't create new headings.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

### CR-12 · status log · minor
File: `status/antigravity.md`
What: the log ticks definition-of-done boxes that don't apply to a spec document (tokens, allowed pairs, copy from content files, images from images.json). It calls banning the container "one accessory removed". And it says "Crops verified" (see CR-01).
Fix: mark boxes that don't apply as N/A, and write only checks that actually happened. The other agents rely on this log being true.
Owner: Antigravity · Status: closed 2026-11-17 (round 2)

---

## Round 2 follow-ups (2026-11-17, after the redo)

### CR-13 · A-2 journey prompts drop parts of the house · minor
File: `03-ideate/shot-list.md`
Rule: brief A-2 ("the house is always the same house"); PLAN §2.1.
What: the hero, meadow and exploded prompts carry every canonical trait, but the journey prompts don't:
- `journey-workshop` and `journey-truck` leave out the slim dark steel base;
- `journey-plot` also leaves out the silver-brown boards and the solid black door.

These three scenes have to read as the same house moving, so a generated image that drifts from the others would break the story.
Fix: paste the full canonical house sentence from PLAN §2.3 into all three journey prompts. Keep the container line in "Do not draw".
Owner: Antigravity · Status: closed 2026-11-17 (round 3)

### CR-14 · bathroom register rows · minor
File: `bildeliste.csv`
What:
- «vaskeskovl» is not a Norwegian word. A vessel basin is an «oppsatt servant», so write «oppsatt servant i lys kremfarget stein».
- «Baderomsbenk» should be «Servantbenk».
- `cladding_matches` and `openings_match` are `true` on the four interior images. Those checks describe the exterior, so leave them blank there, like `roof_matches` and `base_matches`.

Owner: Antigravity · Status: closed 2026-11-17 (round 3)

### CR-15 · `living` aspect and the gallery name · minor
File: `03-ideate/shot-list.md`
What:
- `living` is the one large interior image, which DESIGN-GUIDE §6.8 sets at **3:2**. It is listed as 4:3. My CR-08 and the old §7 wording caused this; §7 now names the exception. Make it 3:2, at least 2400 × 1600.
- The section for `meadow-wide` is called «Galleri». PLAN §8.6 calls the gallery «Bilder».

Owner: Antigravity · Status: closed 2026-11-17 (round 3)

---

## Round 3 (2026-11-17): CR-13 to CR-15 closed, and the A-3 market scan reviewed

CR-13 to CR-15 are checked and closed:

- The canonical sentence and the steel base are in all three journey prompts.
- «vaskeskovl» is gone.
- The interior rows have no exterior checks.
- `living` is 3:2 at 2400 × 1600.
- The gallery section is «Bilder».

### CR-16 · A-3 market scan has no sources, and one entry is wrong · serious
File: `01-empathize/market-scan.md`
Rule: brief A-3 asks you to look at 10 real listings and sites and record their structure; rules.md says every value needs a source.
What:
- **No sources.** None of the 10 entries gives a URL or a visit date, so nothing in the scan can be checked.
- **Actor 2 is wrong.** It's the FINN listing Carlos gave (417043406). The scan describes an 18 m² steel-frame annex with amateur phone photos, a price of 380 000–550 000 kr and the line "no permit under 50 m²". The real listing is Vagabond Haven's MAYA: a Swedish tiny house on a trailer, 20 m² including the loft, 485 956 kr, with professional photos. PLAN Appendix A records it.
- **Two entries aren't listings.** Actors 5 ("typical import module") and 10 ("converted barracks") are invented typical cases, not sites anyone opened.
- **Figures without a source:**
  - prices per company;
  - DNB/Cultura green loans;
  - "5 års garanti";
  - CE and UN-goal certifications;
  - "PBL fra 1. juli 2023";
  - "200 000–400 000 kr" in extra costs.
- **Names:**
  - Some check out on the web: Norske Mikrohus with Heim, Tind and Rast; Ålhytta, from a 1966 Ål kommune competition (Lund & Slaatto); Manta North; Rindalshytter.
  - Manta North is **Latvian** and Iglucraft **Estonian**, not Norwegian.
  - I couldn't confirm "Smart Hytte / Lille Vinkel" or "Norske Småhus / Mikrobu".
- **Gap 1** calls the planned material passport «reell dokumentasjon av malmfuru, eik». The reclaimed lot is undocumented (claims K-07 and K-08: ikke bestemt).

Fix:
1. Redo the scan with one URL and visit date per entry, using only listings and sites you actually opened. Leave out anything you can't open, or mark it «ikke verifisert».
2. Give no figure without the page it came from.
3. Describe the FINN listing as it really is, or point to PLAN Appendix A.
4. Mark the Baltic makers as Baltic.
5. Keep the four gaps, but describe the passport as planned, not documented.

Until it's redone, DeepSeek shouldn't use the scan for D-3.
Owner: Antigravity · Status: closed 2026-11-17 (round 4). Points 1, 3, 4 and 5 are done; point 2 is still open as CR-17.

---

## Round 4 (2026-11-17): A-3 redo reviewed

The redo is a real improvement:

- All 11 URLs resolve (status 200).
- The FINN MAYA listing is now described correctly.
- The invented typical cases are gone.
- The Baltic makers are labelled as Baltic.
- The passport is called planned.

I spot-checked the figures against the cited pages on 2026-11-17. Several match: Norske Mikrohus' Flor at "Fra 1 450 000 NOK" (30 m²) and Heim at "Fra 1 290 000 NOK" (20 m²), its TEK17 statement and its green-mortgage note (energy class B); Tiny House Norge's Shadow 3×6 m at 590 000 kr including VAT; and Brda Midi at 669 000 kr, 16 m², an A-frame.

### CR-17 · details and figures that aren't on the cited pages · serious
File: `01-empathize/market-scan.md`
Rule: CR-16 point 2; the redo says "every price and dimension is cited directly from the specific visited page".
What, checked on 2026-11-17:
- **Tiny House Norge (FINN 372179395)** says «Frakt og leveringskostnader beregnes i hvert enkelt tilfelle» and that the buyer prepares the foundation. It gives **no transport range and no foundation range**, so "45 000–110 000" and "30 000–80 000" aren't from the page. The scan's §3 table then uses those two ranges as its evidence.
- The same listing doesn't mention a steel frame (it says C24 timber), a TEK17 declaration or a drawing pack for one-step permit applications. It does say something the scan missed: the 3 m wide house comes on a tractor trailer and «kan ikke kjøres på offentlig vei på grunn av bredden (300 cm)». That's directly relevant to the MiniHouse transport story.
- **Norske Mikrohus**'s homepage gives no "inkl. mva", no «samsvarserklæring» and no paid permit service; it only says building needs an application. The Rast and Tind prices aren't on the homepage. If they're on model pages, cite those pages.
- **Iglucraft:** neither the homepage nor `/en/products` shows any price or warranty, so the three model prices and "5 års garanti" have no source.
- **Manta North:** the homepage shows no price, size, warranty, award, solar or smart-home feature, so "€66 900–€129 000+" and the trust signals have no source.
- **Hedda Hytter:** the homepage names no architect (no «Jon Haug»), mentions neither modules, low eaves nor untreated wood that greys, and sends visitors to the company, not a dealer. It says «lokaler i Hedalen», not a factory.

Fix: for every figure and every specific detail, cite the exact page where it appears (a subpage URL if needed), or delete it. If you can't point at the sentence, the detail goes. Rebuild the §3 price row from what pages actually say, for example "shipping is calculated per case; the buyer prepares the foundation". Add the Tiny House Norge sentence about 300 cm width and public roads.
Owner: Antigravity · Status: closed 2026-11-17 (round 5)

### CR-18 · leftovers · minor
File: `01-empathize/market-scan.md`
What:
- Gap 4 still says «Meld interesse». The call to action is now «Følg prosjektet» (D1), and MiniHouse isn't for sale (D10).
- §3 still cites "mikrohusreglene (PBL 2023)" without a source.
- Gap 2 says the site explains how the house «hviler skånsomt på lave fundamentpunkter på svaberg/fjell». The foundation isn't designed; say «på et fundament tilpasset tomta» or leave it out.

Owner: Antigravity · Status: closed 2026-11-17 (round 5)

---

## Round 5 (2026-11-17): market scan closed, A-4 style tiles and moodboard reviewed

**CR-17 and CR-18 are closed.**

- The unsourced figures are gone.
- The Norske Mikrohus model pages are cited. Rast checked: 15 m², «Pris fra 1 090 000 NOK».
- The Tiny House Norge terms are quoted, including the 300 cm sentence.
- «Følg prosjektet» is in Gap 4.

The scan can now feed D-3.

I rendered the three style tiles with headless Chrome at 1760 px, so both their 360 px and 1280 px frames are visible.

### CR-19 · style tiles don't show the design and repeat invented claims · serious
Files: `03-ideate/style-tiles/direction-a-patina.html`, `direction-b-hytte74.html`, `direction-c-stavkirke.html`
Rule: brief A-4 (tile A is "the reference Cursor builds from, so make it right"); DESIGN-GUIDE §3, §6.6, §10; claims register; D12.
What:
1. **The fonts never load.** No tile has an `@font-face`, and Besley, Jost, Caprasimo, Quicksand and Cinzel aren't installed here. Tile A renders in Georgia and Segoe UI, and C in a Georgia-like fallback. B only looks right because Cooper Black happens to be installed. A preference test would compare fallback fonts. The stacks also fall back to Fraunces and Playfair, the very defaults the guide rejected.
2. **The three tiles are the same layout in different colours:** same header, same boxed split hero, same band with a two-column table, same swatches. A preference test can then only measure colour taste.
3. **The signature element is missing everywhere.** DESIGN-GUIDE §6.6 asks for a material passport shaped like a timber tag: a texture photo, the name in Besley, one lead sentence, and a tag with a 1 px border, a punched hole and a `<dl>`. All three tiles show a plain table.
4. **Invented claims and a false credit:**
   - «Bygget for vestlandsklima» (built for West Norway weather): the house isn't built (K-19).
   - «6 × 3 meter transportabel modul med verdighet / med ekte hyttepreg» ("transportable module with dignity / with real cabin feel").
   - Malmfuru «naturlig motstandsdyktig mot fukt og sopp» (naturally resistant to damp and fungus): no source.
   - «uten (behov for) kjemisk trykkimpregnering» (without chemical pressure treatment): treatment is undecided (K-09, «Not sure yet»).
   - «Konseptbilde · Foto: Carlos» presents a ChatGPT render as Carlos's photo, and uses a middle-dot string.
5. **Outdated copy:** the hero title is the old one, not D12's «Et lite hus, laget for å flyttes.», and the nav says «Transport», not «Flytting».
6. **Contrast below 4.5:1** (measured):
   - A, captions in sølvgrå: 3.27;
   - A, table labels: 4.48;
   - B, white on the rya-orange button: 4.08;
   - C, pergament on the copper button: 3.31;
   - C, copper labels on tjære: 3.89.
7. **Garbage-list items** (DESIGN-GUIDE §10):
   - C uses tracked all-caps for the wordmark, nav and buttons.
   - B uses pill buttons with drop shadows.
   - A frames the photo with a border, and the hero image doesn't bleed to the edge as in PLAN §8.3.
   - A hard-codes sizes (a 56 px h1 at 1280) instead of using `tokens.css`.

Fix:
1. **Fonts:** load them with `@font-face`. For A, use the self-hosted files Cursor already installed in `web/promo/node_modules/@fontsource/besley` and `/jost` (relative paths are fine for a tile). For B and C, use OFL files saved next to the tiles. Drop Fraunces and Playfair from the stacks.
2. **Copy:** take every word from `web/promo/src/content/nb.json`: hero title (D12), lead, «Følg prosjektet», and the malmfuru passport rows. Captions say only «Konseptbilde».
3. **Passport:** build the material passport exactly as §6.6 describes, in every tile, with the cladding reference crop as the texture stand-in.
4. **Distinct directions:** make each direction differ in structure where its idea calls for it, not only in colour. A is chalk, bleed and bands. B is warm pine panelling, softer shapes and rya colour. C is dark, a full-bleed photo and carved display type, with nav and buttons in sentence case.
5. **Contrast and garbage list:** bring every text pair to 4.5:1 or more and remove the §10 items. A uses `tokens.css` verbatim.

**Don't run the G3 test until this is closed.** Five people's time should test real directions.
Owner: Antigravity · Status: cancelled 2026-11-18 (D14). There is no G3 test, and the style tiles are archived. Carlos chose «Patina, made funkier».

### CR-20 · moodboard references can't be opened · minor
File: `03-ideate/moodboard.md`
What: it says "25 verified references", but there are only 6 unique links, and most are homepages (digitaltmuseum.no, riksantikvaren.no, aalhytta.no). The specific objects it describes can't be looked at: the 1970s pine daybed, the Cathrineholm pots, the Figgjo glaze, Bonytt 1970–74. Carlos's taste question (kit Q18) needs references he can open and sort.
Fix: link each reference to the object or collection page you actually looked at (DigitaltMuseum item pages, museum object URLs), or mark it «ingen lenke». Drop "verified" unless every entry has a link.
Owner: Antigravity · Status: cancelled 2026-11-18 (D14). The moodboard is archived.

---

## Round 6 (2026-11-18): design-thinking material cancelled

Carlos cancelled the design-thinking process (D14) and chose «Patina, made funkier» (G3). CR-19 and CR-20 are cancelled, not fixed. Their files are in `archive/design-thinking/03-ideate/`. Every finding in this file is now closed or cancelled. New findings follow the R2 plan and DESIGN-GUIDE R2.
