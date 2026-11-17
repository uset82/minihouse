# MiniHouse · Canonical House Specification

Revision R1 (redone), 2026-11-17. Single source of visual truth for MiniHouse promo images.
Owner: Antigravity. Enforced at Gate G1 and Gate G4.

Reference images source: `images/MiniHouse cabin on a Norwegian slope-2.png`.

---

## 1. Overview & Core Architecture

MiniHouse is a single-storey transportable modular house of approximately 6 × 3 m (roughly a 2:1 rectangular plan ratio). It is built with a dark steel base and clad in vertical reclaimed timber.

![Canonical House Overview](assets-source/reference/canonical-house-overview.jpg)
*(Overview crop: 1014 × 575 px, from the clean photo area without UI or text)*

### Key Rules
- **Form:** Symmetrical gable roof, single storey, rectangular volume.
- **NEVER a shipping container:** No flat roof, no corrugated shipping container walls, no container corner casting blocks, no peripheral cage/external exo-frame, no stilts, no wheels.

---

## 2. Visual Reference Breakdown

The five reference crops in `assets-source/reference/` were cropped strictly inside the photo area of `images/MiniHouse cabin on a Norwegian slope-2.png` and verified free of UI, text, and borders:

### 2.1 Roof: Black Standing-Seam Metal (Båndtekking)
![Roof Reference](assets-source/reference/ref-roof-standing-seam.jpg)
*(Crop size: 610 × 170 px)*
- **Profile:** Symmetrical gable roof with slim eaves, as shown in the concept images. Pitch is not dimensioned.
- **Material appearance:** Matte black standing-seam sheet metal.
- **Eaves & Ridges:** Clean, low-profile eaves and verge trims as shown in the concept renders.

### 2.2 Cladding: Vertical Weathered Reclaimed Timber
![Cladding Reference](assets-source/reference/ref-cladding-weathered-timber.jpg)
*(Crop size: 130 × 260 px)*
- **Orientation:** Vertical board arrangement with natural variation.
- **Tone & Patina:** Weathered silver-brown, as in the slope and meadow concept images.
- **Treatment:** Natural weathered look; no stain or paint.

### 2.3 Façade Openings: Door & Picture Window
![Openings Reference](assets-source/reference/ref-openings-facade.jpg)
*(Crop size: 430 × 255 px)*
- **Long Façade:**
  - **Entrance Door:** Solid black door, positioned left of centre, as shown in the concept images.
  - **Main Window:** Large black-framed picture window with a sill at table height (not floor-to-ceiling).
- **Gable End:**
  - Secondary smaller black-framed window for daylight and ventilation.
- **Frames:** Slim dark/black frames, as shown in the concept images.

### 2.4 Foundation & Base: Slim Steel Plinth on Low Supports
![Base Reference](assets-source/reference/ref-base-steel-plinth.jpg)
*(Crop size: 550 × 80 px)*
- **Base Structure:** Low-profile dark steel plinth.
- **Supports:** Resting close to the ground on low supports adjusted to the terrain.
- **Forbidden:** No high stilts, no wheels, no container corner castings.

---

## 3. Interior & Atmosphere

Described strictly from Carlos's concept images:
- **Living Area (`images/MiniHouse cabin interior-1.png`):** Pale pine panelled walls, built-in window bench with light linen cushions and deep storage drawers underneath, compact kitchenette with muted sage/olive green fronts, solid timber counter, and bronze/copper fittings. Window sill is at table height.
- **Bathroom (`images/MiniHouse Bathroom with Petrol-Green Shower.png`, `Reclaimed Vanity View in a MiniHouse Bathroom-1.png`, etc.):** Petrol-green glazed vertical tiles, reclaimed timber vanity with pale cream stone vessel sink and deck-mounted bronze faucet, wavy organic copper mirror, brushed bronze shower fixtures, framed sliding glass shower door, and an oak-framed window with a trailing plant. Captioned as material mood.
- **Lighting Condition:** Soft, overcast Western Norway daylight.

---

## 4. Settled Inconsistencies (Decisions Log 2026-11-17)

Carlos approved the default parameters in [decisions.md](decisions.md):

| Component | Canonical Specification | Context & Notes |
|---|---|---|
| **Door** | **Solid black** | Matches 5 of Carlos's concept images. |
| **Base** | **Slim plinth on low supports** | Plinth hugs the terrain with minimal visual gap. |
| **Cladding tone** | **Silver-brown** | Weathered reclaimed timber tone, as in the slope and meadow images. |
| **Openings** | **Follow concept renders** | Captioned explicitly as «Konseptbilde». Functional plans retain technical layout. |
| **Bathroom imagery** | **Caption as «materialstemning»** | Represents material palette and ambiance until R1 interior plan fixes final plumbing envelope. |
| **Wood specification** | **"Planned"** | Reclaimed heartwood pine (*malmfuru*) and European oak (*eik*) are listed as planned specifications. |
| **Chemical Treatment** | **«Ikke bestemt» / unstated** | The site makes no claim regarding chemical pressure treatment until batch provenance is verified. |

---

## 5. Canonical Prompt Formula for New Renders

When generating clean concept imagery (Carlos in ChatGPT, or agent-generated if approved):

```text
Photorealistic architectural photograph. No text, no website interface, no logos, no watermark. A small single-storey house about 6 m long and 3 m wide with a symmetrical gable roof in black standing-seam metal. Walls of vertical reclaimed timber boards, weathered silver-brown with natural variation. On the long façade: a solid black door left of centre and one large black-framed picture window; a small black-framed window on the gable end. A slim dark steel base. Setting: grassy slope above a fjord in Western Norway, birch trees, mossy rocks, soft overcast daylight. Eye-level three-quarter view. Landscape 3:2, at least 2400 px wide.
Do not draw: a shipping container, a flat roof, a steel frame around the walls, stilts, wheels.
```

---

## 6. Image Fidelity Checklist

Before any image is added to the catalogue or considered for publication, verify every item:

- [ ] **Roof form:** Symmetrical gable roof in black standing seam with slim eaves.
- [ ] **Cladding:** Vertical reclaimed boards in weathered silver-brown tone.
- [ ] **Openings:** Solid black door left of centre, black-framed picture window with table-height sill, no white frames.
- [ ] **Base:** Slim dark steel plinth close to ground; zero container features, no stilts, no wheels.
- [ ] **Artifact clean:** Zero UI graphics, no browser mockups, no logos, no baked-in labels.
- [ ] **Resolution:** Minimum 2400 px wide for hero shots, minimum 1600 px for section photos, minimum 1280 × 1600 px for textures.
- [ ] **Metadata:** Captioned as «Konseptbilde» / «Concept image» (or «Konseptbilde av materialer og stemning» for bathrooms) with Norwegian & English alt text.
- [ ] **Approval:** Explicitly approved by Carlos at Gate G4.

---

## 7. Prohibited Images Archive

The 3 rejected container renders have been archived into [archive/rejected-renders/](archive/rejected-renders/):
1. `hero-nordic.jpg` (flat roof, container corners, stilts, fake browser UI).
2. `exploded-materials.jpg` (container styling, unverified technical claims baked in).
3. `3d-lifting-sim.jpg` (container geometry, unverified crane rating).
