# MiniHouse · Shot List & Image Generation Prompts

Revision R1 (redone), 2026-11-17.
Owner: Antigravity (Task A-2, PLAN §3.5).
Governing specifications: [canonical-house.md](canonical-house.md), [DESIGN-GUIDE.md](DESIGN-GUIDE.md), and [agents/README.md](agents/README.md).

---

## 1. Master Image Registry (README §4.2)

Every image used in `web/promo` maps to one of the 19 standard IDs below.
Status definitions:
- `stand-in`: Crop or placeholder used strictly during layout development.
- `pending`: Candidate image awaiting Carlos's formal sign-off at Gate G4.
- `approved`: Confirmed by Carlos at Gate G4 (production ready).
- Blank / to produce: File not yet generated.

| ID | Section (PLAN §8.6) | Aspect | Min Size | Preferred Source | Current Status |
|---|---|---|---|---|---|
| `hero-slope` | Hero | 3:2 | 2400 × 1600 | Carlos in ChatGPT | to produce |
| `meadow-wide` | Bilder | 16:9 | 2400 × 1350 | Carlos in ChatGPT | to produce |
| `exploded` | Fra bunn til tak: Konstruksjon | 4:3 | 1600 × 1200 | Carlos in ChatGPT | to produce |
| `living` | Slik bor du i MiniHouse: Stue | 3:2 | 2400 × 1600 | Carlos in ChatGPT | to produce |
| `kitchen` | Slik bor du i MiniHouse: Kjøkken | 4:3 | 1600 × 1200 | Carlos in ChatGPT | to produce |
| `bench` | Slik bor du i MiniHouse: Sittebenk | 4:3 | 1600 × 1200 | Carlos in ChatGPT | to produce |
| `storage` | Slik bor du i MiniHouse: Oppbevaring | 4:3 | 1600 × 1200 | Carlos in ChatGPT | to produce |
| `bath-shower` | Slik bor du i MiniHouse: Badet | 4:5 | 1122 × 1402 | `images/MiniHouse Bathroom with Petrol-Green Shower.png` | `pending` (soft in lightbox) |
| `bath-vanity` | Slik bor du i MiniHouse: Badet | 4:5 | 1122 × 1402 | `images/Reclaimed Vanity View in a MiniHouse Bathroom-1.png` | `pending` (soft in lightbox) |
| `bath-window` | Slik bor du i MiniHouse: Badet | 4:5 | 1122 × 1402 | `images/Compact bathroom with window, plant, and toilet-2.png` | `pending` (soft in lightbox) |
| `bath-doorway` | Slik bor du i MiniHouse: Badet | 4:5 | 1122 × 1402 | `images/Shower-side view toward the timber doorway-3.png` | `pending` (soft in lightbox) |
| `journey-workshop` | Fra verksted til tomt: Verksted | 4:3 | 1600 × 1200 | Carlos in ChatGPT | to produce |
| `journey-truck` | Fra verksted til tomt: Transport | 4:3 | 1600 × 1200 | Carlos in ChatGPT | to produce |
| `journey-plot` | Fra verksted til tomt: Tomt | 4:3 | 1600 × 1200 | Carlos in ChatGPT | to produce |
| `texture-malmfuru` | Materialpass: Malmfuru | 4:5 | 1280 × 1600 | Real photo (Carlos's daylight photo) | to produce |
| `texture-eik` | Materialpass: Eik | 4:5 | 1280 × 1600 | Real photo (Carlos's daylight photo) | to produce |
| `texture-kobber` | Materialpass: Kobber | 4:5 | 1280 × 1600 | Real photo / Macro render | to produce |
| `texture-stal` | Materialpass: Båndtekket stål | 4:5 | 1280 × 1600 | Real photo / Macro render | to produce |
| `og-image` | Social / Meta | 1.91:1 | 1200 × 630 | Derived master from `hero-slope` | to produce |

---

## 2. Prompts by Image ID

Every prompt is based on the canonical prompt formula (PLAN §2.3) and enforces the mandatory negative constraints.

> **Instruction for Carlos in ChatGPT:**
> For interior shots (`living`, `kitchen`, `bench`, `storage`), attach `images/MiniHouse cabin interior-1.png` as visual reference to keep styling, wood tones, and fittings consistent.
> For the exploded view (`exploded`), attach `images/MiniHouse_ From Base to Roof-1.png` as visual reference.

---

### 2.1 Exterior & Hero

#### ID: `hero-slope`
- **Location on site:** Hero section at top of landing page.
- **Composition:** Eye-level 3/4 perspective showing the long front façade (solid black door left of centre and large black-framed picture window with sill at table height) and one gable end with small window. Symmetrical gable roof in matte black standing seam. Cladding of vertical weathered silver-brown reclaimed timber boards. Low dark steel plinth resting on low supports.
- **Setting:** Grassy slope above a fjord in Western Norway. Birch trees, mossy rocks, soft overcast daylight.
- **Aspect Ratio & Size:** 3:2 landscape, minimum 2400 × 1600 px.
- **Prompt:**
```text
Photorealistic architectural photograph. No text, no website interface, no logos, no watermark. A small single-storey house about 6 m long and 3 m wide with a symmetrical gable roof in black standing-seam metal with slim eaves. Walls of vertical reclaimed timber boards, weathered silver-brown with natural variation. On the long façade: a solid black door left of centre and one large black-framed picture window with sill at table height; a small black-framed window on the gable end. A slim dark steel base close to the ground on low supports. Setting: grassy slope above a fjord in Western Norway, birch trees, mossy rocks, soft overcast daylight. Eye-level three-quarter view. Landscape 3:2, at least 2400 px wide.
Do not draw: a shipping container, a flat roof, a steel frame around the walls, stilts, wheels, trailer hitch, text, UI badges.
```

#### ID: `meadow-wide`
- **Location on site:** Bilder (Galleri) / context section.
- **Composition:** Wide landscape shot showing the MiniHouse sitting naturally on coastal meadow ground. Symmetrical gable roof in black standing seam, vertical weathered silver-brown timber cladding, black door and window framing.
- **Setting:** Coastal meadow in Western Norway, wild grasses, heather, granite rocks, soft overcast daylight.
- **Aspect Ratio & Size:** 16:9 panoramic landscape, minimum 2400 × 1350 px.
- **Prompt:**
```text
Photorealistic wide-angle architectural landscape photograph. No text, no website interface, no logos, no watermark. A small standalone single-storey house about 6 m long and 3 m wide with a symmetrical gable roof in matte black standing-seam metal. Walls of vertical weathered silver-brown reclaimed timber. Solid black entrance door and large black-framed picture window with sill at table height. The house sits low on the terrain on a slim dark steel base. Setting: coastal meadow in Western Norway, coastal grasses, heather, distant fjord and mountains under soft overcast sky. Wide 16:9 shot, at least 2400 px wide.
Do not draw: a shipping container, a flat roof, corner castings, exterior structural cage, high stilts, wheels, roads, power lines.
```

---

### 2.2 Bygging og anatomi: Fra bunn til tak

#### ID: `exploded`
- **Location on site:** Fra bunn til tak (Tab: Konstruksjon).
- **Composition:** Axonometric diagram on a clean, neutral chalk background. Three closed volumes floating vertically separated, exactly as in Carlos's *From Base to Roof* concept:
  1. Base: Dark steel plinth volume.
  2. Walls: Single closed wall box clad in vertical silver-brown reclaimed wood with black window and solid black door.
  3. Roof: Symmetrical gable roof volume in matte black standing seam.
  *(No internal studs, no joists, no insulation layers).*
- **Aspect Ratio & Size:** 4:3, minimum 1600 × 1200 px.
- **Prompt:**
```text
Architectural axonometric diagram render. Clean neutral studio background in warm off-white chalk tone. No text, no callout lines, no arrows, no labels, no website UI. A 6 × 3 m single-storey house separated vertically into three clean closed volumes: at the bottom, a dark steel base plinth; in the middle, a closed wall volume clad in vertical silver-brown reclaimed wood with black-framed picture window and solid black door; at the top, a symmetrical gable roof volume in matte black standing-seam metal. Clean diffuse studio lighting, sharp architectural detail. No internal framing or insulation layers shown. Medium 4:3, at least 1600 px wide.
Do not draw: container corner castings, flat roof, stilts, annotations, dimensions, graphic overlays, fake UI, internal joists or rafters.
```

---

### 2.3 Slik bor du i MiniHouse

*(Attach `images/MiniHouse cabin interior-1.png` in ChatGPT as visual reference)*

#### ID: `living`
- **Location on site:** Slik bor du i MiniHouse (Stue).
- **Composition:** Calm interior view of the compact cabin living space looking toward the large black-framed picture window. Pale pine panelled walls, natural timber floor. Built-in window bench with light linen cushions and a green throw pillow. Deep storage drawers under the bench. Sill at table height.
- **Aspect Ratio & Size:** 3:2 landscape, minimum 2400 × 1600 px.
- **Prompt:**
```text
Photorealistic architectural interior photograph. No text, no logos, no watermark. Interior of a compact 6 × 3 m Nordic cabin. Walls of pale natural Scandinavian pine boards. Soft natural light through a large black-framed picture window with its sill at table height, overlooking a fjord landscape. Built-in timber window bench with light linen cushions and a green accent cushion, with deep storage drawers underneath the bench. Warm, calm Scandinavian atmosphere. Soft overcast daylight. Eye-level shot. Landscape 3:2, at least 2400 px wide.
Do not draw: floor-to-ceiling glass, clutter, luxury chandeliers, plastic furniture, television, text, fake UI.
```

#### ID: `kitchen`
- **Location on site:** Slik bor du i MiniHouse (Kjøkken).
- **Composition:** Compact kitchenette built against the pale pine wall. Muted sage/olive green cabinet fronts, solid timber countertop, bronze/copper tap, small fold-down dining flap table attached to the wall.
- **Aspect Ratio & Size:** 4:3, minimum 1600 × 1200 px.
- **Prompt:**
```text
Photorealistic architectural interior photograph. No text, no logos, no watermark. Compact kitchenette in a Nordic timber cabin. Muted sage-green cabinet fronts paired with pale natural pine walls. Solid timber countertop with a small undermount sink and bronze-finish tap. Fold-down dining flap table attached to the pine wall. Clean, quiet Scandinavian craftsmanship. Soft natural daylight. Medium shot 4:3, at least 1600 px wide.
Do not draw: petrol-green cabinets, black gooseneck faucet, messy dishes, excessive appliances, text, brand names.
```

#### ID: `bench`
- **Location on site:** Slik bor du i MiniHouse (Sittebenk).
- **Composition:** Detail view of the built-in pine window bench beneath the black-framed window. Light linen bench cushions, green throw pillow, and deep wooden pull-out storage drawers integrated underneath.
- **Aspect Ratio & Size:** 4:3, minimum 1600 × 1200 px.
- **Prompt:**
```text
Photorealistic architectural interior photograph. No text, no watermark. Built-in window daybed bench in a modern timber cabin. The bench is built of pale solid pine with light linen cushions and a green throw pillow. Deep wooden storage drawers are visible under the seat. Beside it, the black frame of a picture window with sill at table height frames natural rocks and birches outside. Warm, calm atmosphere. Medium close-up 4:3, at least 1600 px wide.
Do not draw: cluttered items, gaudy patterns, synthetic glossy materials, text.
```

#### ID: `storage`
- **Location on site:** Slik bor du i MiniHouse (Oppbevaring).
- **Composition:** Focus on smart storage solutions in the compact 6 × 3 m plan: pull-out deep drawers beneath the timber window bench and compact built-in pine shelving.
- **Aspect Ratio & Size:** 4:3, minimum 1600 × 1200 px.
- **Prompt:**
```text
Photorealistic architectural interior photograph. No text, no watermark. Built-in storage detail in a compact 6 × 3 m pine cabin. Focus on deep pull-out timber drawers integrated under a window bench, with smooth flush faces and neat joinery. Pale natural pine surfaces under soft daylight. Clean, functional Nordic detail. Vignette 4:3, at least 1600 px wide.
Do not draw: floor-to-ceiling wardrobe wall eating the room, plastic containers, chaotic clothes, text.
```

---

### 2.4 Slik bor du i MiniHouse: Badet (Existing Master Concepts)

The four bathroom images exist in `images/` as concept renders. Status is `pending` for Carlos's review at Gate G4 (note: at 1122 × 1402 px they are fine for gallery tiles, but soft in a full-screen lightbox).

Captioned as: **«Konseptbilde av materialer og stemning»** / **«Concept image of materials and mood»**.

#### ID: `bath-shower`
- **Source:** `images/MiniHouse Bathroom with Petrol-Green Shower.png` (1122 × 1402 px).
- **Aspect Ratio:** 4:5.
- **Content:** Vertical glazed petrol-green tiles, brushed bronze shower fixtures, framed sliding glass shower door, warm timber wall beside shower.
- **Alt text (NB):** Dusjhjørne med stående petrolgrønne fliser, armaturer i børstet bronse og skyvedør i glass med mørk ramme.
- **Alt text (EN):** Shower corner with vertical petrol-green tiles, brushed bronze fixtures, and framed sliding glass door.

#### ID: `bath-vanity`
- **Source:** `images/Reclaimed Vanity View in a MiniHouse Bathroom-1.png` (1122 × 1402 px).
- **Aspect Ratio:** 4:5.
- **Content:** Reclaimed timber vanity counter, pale cream round stone vessel sink, deck-mounted bronze faucet, organic wavy copper-framed mirror.
- **Alt text (NB):** Servantbenk i gjenbrukt treverk med oppsatt servant i lys kremfarget stein, benkemontert kran i bronse og organisk bølget speil i kobberramme.
- **Alt text (EN):** Reclaimed timber vanity with pale cream stone vessel sink, deck-mounted bronze faucet, and wavy copper-framed mirror.

#### ID: `bath-window`
- **Source:** `images/Compact bathroom with window, plant, and toilet-2.png` (1122 × 1402 px).
- **Aspect Ratio:** 4:5.
- **Content:** Floor-standing ceramic toilet, oak-framed window letting in natural daylight, small trailing plant in a terracotta pot on the timber ledge, vertical petrol-green tiles.
- **Alt text (NB):** Baderom med stående petrolgrønne fliser, gulvstående toalett og eikeinnrammet vindu med hengeplante i terrakottapotte.
- **Alt text (EN):** Bathroom with vertical petrol-green tiles, floor-standing toilet, and oak-framed window with trailing plant in terracotta pot.

#### ID: `bath-doorway`
- **Source:** `images/Shower-side view toward the timber doorway-3.png` (1122 × 1402 px).
- **Aspect Ratio:** 4:5.
- **Content:** View from inside the petrol-green tiled shower area through the open timber doorway into the bright pine living space.
- **Alt text (NB):** Utsikt fra petrolgrønt flislagt dusjhjørne gjennom tredør mot lyst oppholdsrom med furupanel.
- **Alt text (EN):** View from petrol-green tiled shower area through timber doorway toward bright living space with pine paneling.

---

### 2.5 Fra verksted til tomt

#### ID: `journey-workshop`
- **Location on site:** Fra verksted til tomt (Trinn: Verksted).
- **Composition:** The completed 6 × 3 m MiniHouse standing in a clean, dry prefabrication workshop. Symmetrical black standing-seam gable roof, vertical weathered silver-brown timber cladding, solid black door, large black-framed picture window, slim dark steel base. Natural diffuse light from high workshop windows.
- **Aspect Ratio & Size:** 4:3, minimum 1600 × 1200 px.
- **Prompt:**
```text
Photorealistic architectural documentary photograph. No text, no logos, no watermark. A small single-storey house about 6 m long and 3 m wide with a symmetrical gable roof in black standing-seam metal with slim eaves. Walls of vertical reclaimed timber boards, weathered silver-brown with natural variation. On the long façade: a solid black door left of centre and one large black-framed picture window; a small black-framed window on the gable end. A slim dark steel base. Setting: inside a clean, modern timber prefabrication workshop. Natural diffuse light from high clerestory windows. Clean concrete floor, woodcraft tools in the background. Eye-level shot. Medium 4:3, at least 1600 px wide.
Do not draw: a shipping container, a flat roof, a steel frame around the walls, stilts, wheels, industrial mess, forklifts ramming the house, safety signage, text, logos, watermark.
```

#### ID: `journey-truck`
- **Location on site:** Fra verksted til tomt (Trinn: Transport).
- **Composition:** The complete 6 × 3 m MiniHouse loaded onto a low-bed flatbed transport trailer parked in a damp Norwegian transport yard. Symmetrical black standing-seam gable roof, vertical weathered silver-brown timber walls, solid black door, picture window, slim steel base. Damp ground reflecting grey sky. *(No legal road height claims).*
- **Aspect Ratio & Size:** 4:3, minimum 1600 × 1200 px.
- **Prompt:**
```text
Photorealistic documentary photograph. No text, no logos, no watermark. A small single-storey house about 6 m long and 3 m wide with a symmetrical gable roof in black standing-seam metal with slim eaves. Walls of vertical reclaimed timber boards, weathered silver-brown with natural variation. On the long façade: a solid black door left of centre and one large black-framed picture window; a small black-framed window on the gable end. A slim dark steel base. Setting: the house is loaded onto a low-bed flatbed transport trailer parked in a damp Norwegian transport yard. Wet asphalt ground reflecting grey Norwegian sky, coastal hills in background. Side profile three-quarter shot. Medium 4:3, at least 1600 px wide.
Do not draw: a shipping container, a flat roof, a steel frame around the walls, stilts, wheels attached to the house itself, oversized cartoon loads, container locks, text, logos, watermark.
```

#### ID: `journey-plot`
- **Location on site:** Fra verksted til tomt (Trinn: Tomt).
- **Composition:** The MiniHouse set down on its low supports on a rocky site overlooking a fjord, with a mobile crane in the background. Symmetrical black standing-seam gable roof, vertical weathered silver-brown timber walls, solid black door, picture window, slim steel base. No specific rigging details or point loads depicted.
- **Aspect Ratio & Size:** 4:3, minimum 1600 × 1200 px.
- **Prompt:**
```text
Photorealistic documentary photograph. No text, no logos, no watermark. A small single-storey house about 6 m long and 3 m wide with a symmetrical gable roof in black standing-seam metal with slim eaves. Walls of vertical reclaimed timber boards, weathered silver-brown with natural variation. On the long façade: a solid black door left of centre and one large black-framed picture window; a small black-framed window on the gable end. A slim dark steel base. Setting: the house is set down on its low supports on rocky coastal ground above a fjord in Western Norway. In the background, a mobile crane stands after completing the placement. Mossy rocks, small pines, soft overcast daylight. Medium 4:3, at least 1600 px wide.
Do not draw: a shipping container, a flat roof, a steel frame around the walls, stilts, wheels, container twistlocks, dangerous tilted angle, cartoon crane hook, text, logos, watermark.
```

---

### 2.6 Materialpass (Textures)

All material textures are 4:5 aspect ratio at minimum 1280 × 1600 px (DESIGN-GUIDE §7).

#### ID: `texture-malmfuru`
- **Location on site:** Materialpass: Malmfuru.
- **Subject:** Authentic weathered Heartwood Pine (*Malmfuru*). Close-up macro showing dense annual rings on the end grain and the silvery-grey natural oxidation on the vertical board face.
- **Aspect Ratio & Size:** 4:5, minimum 1280 × 1600 px.
- **Prompt:**
```text
Macro texture photograph of authentic Norwegian heartwood pine (malmfuru). Weathered naturally to a silvery-grey and warm brown patina. Close-up shows tight, dense annual growth rings on the cut end grain and rich natural wood grain on the weathered board surface. Soft, diffuse daylight. Crisp, tactile surface detail. Vertical 4:5, at least 1280 × 1600 px. No text, no varnish, no stain.
```

#### ID: `texture-eik`
- **Location on site:** Materialpass: Eik.
- **Subject:** European Oak (*Eik*), slow-grown dense structural timber. Macro showing warm golden-brown tone, prominent medullary rays, and rugged surface texture.
- **Aspect Ratio & Size:** 4:5, minimum 1280 × 1600 px.
- **Prompt:**
```text
Macro texture photograph of solid European oak (eik). Natural warm golden-brown tone, prominent medullary rays and dense structural grain. Untreated, finely planed surface showing subtle age and durability. Soft side daylight emphasizing tactile texture. Vertical 4:5, at least 1280 × 1600 px. No artificial orange stain, no high gloss, no text.
```

#### ID: `texture-kobber`
- **Location on site:** Materialpass: Kobber.
- **Subject:** Sheet copper with natural atmospheric weathering, showing deep reddish-brown copper transitioning into subtle verdigris patina along edges.
- **Aspect Ratio & Size:** 4:5, minimum 1280 × 1600 px.
- **Prompt:**
```text
Macro texture photograph of natural sheet copper with authentic atmospheric weathering. Warm reddish-brown copper tone with delicate traces of green verdigris patina along edges. Soft natural lighting catching the subtle metal texture. Vertical 4:5, at least 1280 × 1600 px. No computer graphics glow, no text.
```

#### ID: `texture-stal`
- **Location on site:** Materialpass: Båndtekket stål.
- **Subject:** Standing-seam sheet steel with matte black finish, showing a crisp folded standing seam joint.
- **Aspect Ratio & Size:** 4:5, minimum 1280 × 1600 px.
- **Prompt:**
```text
Macro architectural detail photograph of matte black standing-seam sheet steel (båndtekking). Focus on the crisp folded double-seam joint on a low-angle roof sheet. Matte dark finish, subtle sheen under soft overcast Nordic sky. Vertical 4:5, at least 1280 × 1600 px. No text, no rust, no camera reflection.
```

---

### 2.7 Sosiale medier: Open Graph

#### ID: `og-image`
- **Location on site:** HTML `<meta property="og:image">`.
- **Dimensions:** 1200 × 630 px (1.91:1 ratio).
- **Master source:** Crop from `hero-slope` master once generated.
- **Label:** Discrete corner label `Konseptbilde`.
- **Alt text (NB):** MiniHouse konseptmodell på skråning over fjord med saltak og trekledning.
- **Alt text (EN):** MiniHouse concept cabin on a hillside overlooking a fjord with gable roof and timber cladding.
