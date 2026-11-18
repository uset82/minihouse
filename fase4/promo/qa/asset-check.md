# Asset check · Carlos's Drive folder

2026-11-18 00:20. Source: Carlos's shared folder <https://drive.google.com/drive/folders/1JnJQmVP6BsLEc5lNt83kjYBe-MBRXwws>, "images". Read-only check; no media is committed to git (Carlos asked for that, and `.gitignore` enforces it).

**Result: the folder holds exactly the media already on this PC — 16 files, byte-identical — and none of it is large enough for the hero or the section images the shot list specifies.** The folder is the canonical *reference* set, not the production set.

---

## 1 · What was compared

All 16 folder entries were downloaded and hashed (SHA-256), then compared with `images/` on this PC.

| Files | Byte-identical | Missing locally | Different |
|---|---|---|---|
| 16 (15 PNG + 1 MP4) | **16** | 0 | 0 |

So the Drive copy adds no new picture. If Carlos expected new renders there, they are not in this folder.

## 2 · Resolution against the plan

PLAN §2.4 and DESIGN-GUIDE §7 ask for **≥ 2400 px** on the hero and **≥ 1600 px** on section images, with a 1200 × 630 Open Graph image.

| Image | Pixels | Can serve |
|---|---|---|
| MiniHouse cabin on a Norwegian slope-2 | 1536 × 1024 | reference, gallery tile, not the hero |
| MiniHouse Nordic Meadow Homepage-1 | 1536 × 1024 | reference, gallery |
| MiniHouse_ From Base to Roof-1 | 1536 × 1024 | reference, gallery |
| MiniHouse cabin interior-1 | 1536 × 1024 | reference, gallery |
| MiniHouse_ From workshop to terrain-2 | 1536 × 1024 | reference, gallery |
| MiniHouse_ Movable Nordic cabin concept-2 | 1024 × 1536 | reference, portrait tile |
| Weathered timber cabin with a glowing interior | 1536 × 1024 | reference, gallery |
| Tiny cabin with double bed and loft-1 | 1536 × 1024 | reference, gallery |
| Two-Bed Tiny Cabin with Low Loft-2 | 1536 × 1024 | reference, gallery |
| Fisheye view of a rustic bathroom | 1536 × 1024 | gallery |
| Inside the shower, oak door ahead | 1536 × 1024 | gallery |
| MiniHouse Bathroom with Petrol-Green Shower | 1122 × 1402 | gallery tile (4:5), soft full screen |
| Compact bathroom with window, plant, and toilet-2 | 1122 × 1402 | gallery tile (4:5), soft full screen |
| Reclaimed Vanity View in a MiniHouse Bathroom-1 | 1122 × 1402 | gallery tile (4:5), soft full screen |
| Shower-side view toward the timber doorway-3 | 1122 × 1402 | gallery tile (4:5), soft full screen |
| minihouse_walkthrough_v11.mp4 | 31.3 MB | video, not a page asset |

**Largest width 1536 px.** The hero needs 2400, sections 1600. Every image is therefore below the release bar, and the four bathroom renders are exactly what `bildeliste.csv` already calls "fine for gallery tiles, soft in a full-screen lightbox".

That matches the shot list: the four `bath-*` ids are the only ones marked `pending`; the other 15 ids (hero, meadow, exploded, living, kitchen, bench, storage, three journey shots, four textures, og-image) are **to produce** — they are not in this folder, and they must be rendered at the required size.

## 3 · What this means

- **The folder is the canonical reference set.** It fixes the house's look for the fidelity checklist and supplies gallery material. It does not replace the shot list.
- **The hero and section images still have to be made**, at ≥ 2400 px for the hero and ≥ 1600 px for sections (D5: Carlos renders them in ChatGPT with the Antigravity prompt and puts them in the assets inbox).
- **Nothing here was added to git.** Media stays local and publicly reachable only through the Drive link above; the text of the project can cite it, the repository cannot carry it.
- **I cannot judge the pictures.** Whether these are the canonical house, and which of them deserve a place in the gallery, is Antigravity's review with Carlos; this file only records bytes, pixels and provenance.

## 4 · Open

| # | Owner | Item |
|---|---|---|
| 1 | Carlos | Re-render the hero and section shots at the required size, per the shot list |
| 2 | Antigravity | Fidelity checklist against these references, gallery selection, alt text and captions (already in `images.json` for the 19 ids) |
| 3 | Carlos | Say whether the 31 MB walkthrough video is meant to go on the page — nothing in the plan uses video today |
