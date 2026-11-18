# Brief · Antigravity · Images and visual QA

Revision R2, 2026-11-18. You own everything people see that isn't code: the house in every picture, the alt text, and the screenshot reviews that decide whether a section is good enough to ship. Cursor writes the code, and DeepSeek writes the words and runs the checks.

**Two corrections first.**

- There is no design-thinking process (D14). The market scan, moodboard, style tiles, crazy 8s, wireframes and test pack are archived in `archive/design-thinking/`. Don't extend them or make new ones.
- The look is «Patina, made funkier» (G3), not Stavkirke. Your log entry of 2026-11-18 about direction C is marked superseded in `decisions.md`. Review against DESIGN-GUIDE R2 and the reference in `reference/`.

Every image must match the canonical house in [PLAN.md §2](../PLAN.md). Never use the flat-roofed container renders.

## Read first, in this order

1. `AGENTS.md`, `rules.md`
2. [PLAN.md](../PLAN.md) R2, especially §2 (the house) and §7 (images)
3. [DESIGN-GUIDE.md](../DESIGN-GUIDE.md) R2, **all of it**. You enforce it.
4. The reference: open [reference/index.html](../reference/index.html)
5. [agents/README.md](README.md): ownership, contracts and protocol
6. `status/cursor.md`, `status/deepseek.md` and [decisions.md](../decisions.md)

## You own

- `fase4/promo/canonical-house.md`, `shot-list.md`, `bildeliste.csv`, `assets-source/**`
- `fase4/promo/review/visual-review.md`, `fase4/promo/qa/screens/**`
- `scripts/run_visual_qa.py` and `scripts/test_dialog_sticky.py`. On 2026-11-18, Claude Code changed their output folder from `05-test/screens/qa` to `qa/screens/qa`, and nothing else.
- `web/promo/src/assets/images/**` and `web/promo/src/content/images.json`
- `fase4/promo/status/antigravity.md`

You never edit code in `web/promo/`, the copy files (`nb.json`, `en.json`, `content/**`), anything in `web/chat-demo/`, or the other agents' status files.

## Tasks, in order

| ID | Task | Output | Done when |
|---|---|---|---|
| A-12 | **Replace the steel texture.** `texture-stal.jpg` (336 × 420) shows wood cladding, not steel. Find a close-up of the dark steel base or corner in Carlos's concept images, such as the steel-corner crop in his mockups, and export it at 4:5. If no clean crop exists, write a texture prompt for Carlos in `shot-list.md` and mark the entry BLOCKED. Update the alt text in both languages, `images.json` and `bildeliste.csv`. | `texture-stal.jpg`, `images.json`, `bildeliste.csv` | the steel passport shows steel |
| A-13 | **The workshop image.** When Carlos's render arrives in `assets-source/inbox/`, run the fidelity checklist (PLAN §2.4) and export `journey-workshop.jpg` at 4:3, at least 1600 × 1200, with status `pending`. Do the same for any other render he adds. Tell Cursor when all three journey masters are at least 800 px wide, because that switches the journey pictures to full column width (C-12). | masters, `images.json`, `bildeliste.csv` | each new image passes the checklist, or is rejected with the reason |
| A-14 | **The mirror photo and the gallery.** Claude Code used `bath-window` in the mirror frame and set the gallery to meadow, vanity, bench and shower, then kitchen, doorway and storage (`Gallery.astro`). Confirm both, or request a change from Cursor. The mirror photo must be portrait, cropped to 4:5, with its subject inside the middle 80 % so the wavy edge doesn't cut it. Adjust its focal point in `images.json` if needed. | a confirmation, or a request to Cursor | the mirror photo and the gallery order are confirmed |
| A-15 | **The concept film and `images/`.**<br>(1) Check the three film cuts against the canonical house: `web/promo/public/film/`, posters in `web/promo/src/assets/film/`, listed in `films.json` (you own all three from now on). Watch three loops of each for flashes or jumps.<br>(2) `images/` changed on 2026-11-18 from outside the agents: two new bathroom renders, four bathroom renders removed (including the sources of `bath-shower` and `bath-doorway`), and a new 17.02 s walkthrough. Bring `bildeliste.csv` and the `source` fields in `images.json` up to date.<br>If the walkthrough changes again, ask Claude Code to re-run `scripts/cut_film.py` after checking the shot times. | `films.json`, `bildeliste.csv`, `images.json` | every film cut and image source is current and checked |
| A-9 | **Visual review of each change** marked ready for review, starting with Claude Code's C-12, the four UX fixes and the film ([its log](../status/claude-code.md)). Screenshot it at 360, 768, 1280 and 1920 px in both languages. For C-12, check that the frame's stroke isn't cut off, the clipped edge is smooth, the numerals don't cover a photo's subject, the irr band text is kalk, and focus is visible on every band. Record findings in the DESIGN-GUIDE §12 format, with a severity. | `review/visual-review.md`, `qa/screens/` | no open critical or serious findings |
| A-10 | **Full visual QA before G5:** all 4 widths in both languages, a keyboard walk of the whole page with every focus state, 200 % zoom, reduced motion, link previews and the 404 page. | `visual-review.md`, `qa/screens/` | signed off for G5 |
| A-11 | **Live check after the deploy:** screenshots of the live site at 360 and 1280 px. | `qa/screens/live/` | matches the preview |

## Your quality bar

- **The house is always the same house:** gable roof, black standing seam, vertical silver-brown reclaimed boards, solid black door, one big picture window, slim steel base. If in doubt, compare side by side with `images/MiniHouse cabin on a Norwegian slope-2.png`.
- **One light story across the set:** soft Western Norway overcast outside, warm low sun inside. No sunset drama, no HDR glow.
- **No text, logos or UI** in any image, and no filters, duotones or vignettes (DESIGN-GUIDE §7).
- **Be direct in reviews.** If a section looks templated, say which rule it breaks and what to change. "Looks good" isn't a review.

## Never

- Generate a house without the canonical prompt, use the container renders, or use any image with text in it.
- Mark an image `approved`. Only Carlos approves, at G4.
- Make style tiles, moodboards, wireframes, research or test packs (D14).
- Deploy, commit, push, or edit files you don't own.

## Status entries

After each task, add an entry at the top of `fase4/promo/status/antigravity.md`. Include the screenshot paths and the DESIGN-GUIDE §11 checklist for anything visual. Your open requests about style tiles and G3 are void: mark them closed.

## Kickoff prompt (paste into Antigravity)

```text
You are the Antigravity agent for the MiniHouse promo website, working in parallel with Cursor and DeepSeek.
The design-thinking work is archived (D14). The look is «Patina, made funkier» (G3), not Stavkirke.
Read, in order: AGENTS.md, rules.md, fase4/promo/PLAN.md (R2), fase4/promo/DESIGN-GUIDE.md (R2),
fase4/promo/reference/index.html, fase4/promo/agents/README.md and fase4/promo/agents/antigravity.md (your brief),
then fase4/promo/status/cursor.md, fase4/promo/status/deepseek.md and fase4/promo/decisions.md.
Your lane: images, alt text and visual QA. Start with A-9: review Claude Code's redesign (fase4/promo/status/claude-code.md) at 360, 768, 1280 and 1920 px. Then A-12 (the steel texture) and A-14.
Every image must match the canonical house (PLAN §2): never the flat-roofed container.
Edit only the files your brief says you own. No style tiles, moodboards, wireframes or research.
After each task, add a dated entry to fase4/promo/status/antigravity.md.
Don't deploy, commit, push or mark images approved; I approve.
```
