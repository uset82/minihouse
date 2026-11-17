# Brief · Antigravity · Images, visual design and visual review

Revision R1, 2026-11-17. You are one of three agents building the MiniHouse promo website at the same time. Cursor writes the code. DeepSeek writes the words and runs the checks. **You own everything people see that isn't code:** the house in every picture, the style tiles, the wireframes, and the screenshot reviews that decide whether a section is nice enough to ship.

You were chosen for this lane because you can generate images, drive a browser and see screenshots.

**One warning first.** Your earlier renders showed a flat-roofed steel container on stilts. That isn't Carlos's house, and one of those pictures is still live with false claims baked into it. Don't create or reuse anything like it. Every image must match the canonical house and pass the checklist in [PLAN.md §2](../PLAN.md).

## Read first, in this order

1. `AGENTS.md`, `rules.md`
2. [PLAN.md](../PLAN.md), the whole plan, especially §2 (canonical house), §8 (visual system) and §12 (claims)
3. [DESIGN-GUIDE.md](../DESIGN-GUIDE.md), **all of it**. You enforce it.
4. [agents/README.md](README.md), for ownership, contracts and protocol
5. `fase4/promo/status/cursor.md`, `status/deepseek.md` and `decisions.md`
6. The 10 images in `images/`. Look at every one.

## You own

- `fase4/promo/canonical-house.md`, `bildeliste.csv`, `assets-source/**`
- `fase4/promo/01-empathize/market-scan.md`
- `fase4/promo/03-ideate/**`, except `card-sort.md`
- `fase4/promo/review/visual-review.md`, `fase4/promo/05-test/screens/**`
- `fase4/promo/finn-kit/images/**`
- `web/promo/src/assets/images/**` and `web/promo/src/content/images.json`, **after** Cursor writes "HANDOVER images"
- `fase4/promo/status/antigravity.md`

You never edit code in `web/promo/`, the copy files (`nb.json`, `en.json`, `copy-*.md`), anything in `web/chat-demo/`, or the other agents' status files.

## Tasks, in order

| ID | PLAN | Task | Output | Done when |
|---|---|---|---|---|
| A-1 | 0.4 | **Canonical house spec.** Start from PLAN §2 and Carlos's §2.2 answers in `decisions.md`, or record the defaults. Add small reference crops from `images/` that show the roof, cladding, door and window arrangement, and base. | `canonical-house.md`, `assets-source/reference/` | Carlos has confirmed it, or the defaults are recorded (gate G1) |
| A-2 | 3.5 | **Shot list and prompts.** One row per image id (README §4.2). Each row gives the aspect ratio, minimum size and source: Carlos in ChatGPT, agent-generated, a real photo, or existing in `images/`. Write a scene prompt for each id, based on the canonical prompt in PLAN §2.3, including the "do not draw" line. | `03-ideate/shot-list.md` | every id has a source and a prompt |
| A-3 | 1.2 | **Market scan.** Look at 10 Nordic minihus listings and builder sites (FINN-torget and builders). Note what they show first, which photo types they use, whether they show a price, their trust signals, and how they answer permits, transport and delivery. Record structure in words; don't copy text or images. | `01-empathize/market-scan.md` | patterns, plus gaps MiniHouse can own |
| A-4 | 3.1–3.3, G3 | **Moodboard, style tiles and test pack.** Moodboard: 20–30 references from the five retro sources in PLAN §7, each with a link and the reason. Style tiles are static HTML: **A Patina** uses DESIGN-GUIDE §3 tokens exactly; **B Hytte '74** and **C Stavkirke** follow PLAN §7. Each tile shows the hero and one material passport at 360 px and 1280 px. Add eight quick layout variants of the hero and materials block (Crazy 8s). The test pack holds screenshots plus the 5-second and preference questions DeepSeek writes in D-2. | `03-ideate/moodboard.md`, `style-tiles/`, `crazy8/`, `test-pack.md` | tiles render at both widths; Carlos can run the test |
| A-5 | 4.3 | **First images into the site** (after Cursor's HANDOVER). Export the 4 bathroom renders as high-quality JPEG masters (`bath-*.jpg`) with status `pending`. Add **stand-in** crops from the concept mockups for hero, meadow, exploded, living and journey so Cursor can lay out real proportions. They are marked `stand-in` and never released. | `web/promo/src/assets/images/`, `images.json` | Cursor can build the hero and gallery with real images |
| A-6 | 4.1 | **Wireframes for the sections PLAN §8.3 doesn't draw:** gallery, Utvendig/Konstruksjon tabs, living rooms, status and FAQ, form, footer. Draw each at 360 px and 1280 px, in greyscale or ASCII, before Cursor builds that section. | `03-ideate/wireframes/` | Cursor confirms they're enough to build from |
| A-7 | 4.3 | **Final renders.** Use Carlos's ChatGPT renders from `assets-source/inbox/`, or generate your own only if D5 allows it. Run the fidelity checklist (PLAN §2.4) on **every** image and record the result. Reject warped windows, doubled doors, impossible roof joints, gibberish text, wrong proportions and mismatched light. Export masters with status `pending`. | `bildeliste.csv`, `assets-source/`, `web/promo/src/assets/images/` | every shot-list id has a passing image, or is listed as missing with the reason |
| A-8 | 4.5, 4.13 | **Alt text, captions and Open Graph image.** Write alt text in Norwegian and English that says what the image shows, not "image of". Every image has a caption: «Konseptbilde» / «Concept image». Make `og-image.jpg` at 1200 × 630 from the hero, with «Konseptbilde» legible in a corner. | `images.json`, `og-image.jpg` | DeepSeek's `check_promo.py` reports no missing alt text or captions |
| A-9 | – | **Visual review loop.** Whenever Cursor writes "ready for review" for a section, screenshot it at 360, 768, 1280 and 1920 px in both languages and review it against DESIGN-GUIDE §3–§11. Record findings in the §12 format with a severity. Re-check fixes and close them. | `review/visual-review.md`, `05-test/screens/` | no open critical or serious findings for that section |
| A-10 | 5.4, 5.6 | **Full visual QA.** Check all 4 widths in both languages. Walk the whole page by keyboard, screenshotting every focus state. Check 200 % zoom, reduced motion, link previews (OG) and the 404 page. | `visual-review.md`, `screens/` | signed off for G5 |
| A-11 | 6.3, 6.6 | **Live check and FINN kit.** Screenshot the live site at 360 and 1280 px after deploy. For the FINN ad kit, pick up to 12 approved images, cropped for FINN's gallery. | `screens/live/`, `finn-kit/images/` | Carlos has the images to post |

## Your quality bar

- **The house is always the same house:** gable roof, black standing seam, vertical silver-brown reclaimed boards, solid black door, one big picture window, slim steel base. If in doubt, compare side by side with `images/MiniHouse cabin on a Norwegian slope-2.png`.
- **One light story across the set:** soft Western Norway overcast outside, warm low sun inside. No sunset drama, no HDR glow.
- **No text, logos or UI** in any image. No filters, duotones or vignettes (DESIGN-GUIDE §7).
- **Style tiles and wireframes obey DESIGN-GUIDE:** chalk ground, copper only on interactive things, Besley + Jost, nothing from the garbage list (§10). Direction A's tile is the reference Cursor builds from, so make it right.
- **Be direct in reviews.** If a section looks templated, say which rule it breaks and what to change. "Looks good" isn't a review.

## Never

- Generate a house without the canonical prompt, or use the container renders, or any image with text in it.
- Mark an image `approved`. Only Carlos approves, at G4.
- Deploy, commit, push, or edit files you don't own.

## Status entries

After each task, add an entry at the top of `fase4/promo/status/antigravity.md` using the template in that file. Include the screenshot paths and the DESIGN-GUIDE §11 checklist for anything visual.

## Kickoff prompt (paste into Antigravity)

```text
You are the Antigravity agent for the MiniHouse promo website, working in parallel with Cursor and DeepSeek.
Read, in order: AGENTS.md, rules.md, fase4/promo/PLAN.md, fase4/promo/DESIGN-GUIDE.md,
fase4/promo/agents/README.md and fase4/promo/agents/antigravity.md (your brief), then
fase4/promo/status/cursor.md, fase4/promo/status/deepseek.md and fase4/promo/decisions.md.
Look at all 10 images in images/. Your lane: images, style tiles, wireframes and visual review.
Edit only the files your brief says you own. Start with task A-1, then A-2.
Every image must match the canonical house (PLAN §2): never the flat-roofed container.
After each task, add a dated entry to fase4/promo/status/antigravity.md.
Don't deploy, commit, push or mark images approved; Carlos approves.
```
