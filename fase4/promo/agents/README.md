# MiniHouse promo website · Who does what

> **Since 2026-11-17 (D10, D11): MiniHouse is not for sale and is not shown as an emergency cabin.** Drop price, ordering, sales wording, the emergency persona and the FINN ad kit wherever they appear in the briefs. The call to action is **«Følg prosjektet»** (D1): a follow form with an e-mail address and an optional name (DESIGN-GUIDE §6.11). See the change note at the top of [PLAN.md](../PLAN.md).

Revision R1, 2026-11-17. Antigravity, Cursor and DeepSeek build the site **at the same time**, each in its own lane and its own files. Carlos makes the decisions. The *what* is in [PLAN.md](../PLAN.md), the *how it must look and read* is in [DESIGN-GUIDE.md](../DESIGN-GUIDE.md), and this file covers the *who*.

The briefs:

- [Antigravity](antigravity.md)
- [Cursor](cursor.md)
- [DeepSeek](deepseek.md)

---

## 1. The split at a glance

| Agent | Lane | Why this agent | Main outputs | First task |
|---|---|---|---|---|
| **Antigravity** | Images, visual design and visual review | It can generate images, drive a browser and see screenshots | canonical house, shot list and prompts, style tiles, wireframes, images and alt text, screenshots, visual review | A-1 canonical house |
| **Cursor** | Build | Code editing across the repo | the live-site hotfix, the Astro site in `web/promo/`, image pipeline, deploys and git (with Carlos's OK) | C-1 hotfix (prepare only) |
| **DeepSeek** | Research, words and verification | Long-form text, scripts and checks. It **cannot see images**, so it never judges visuals. | claims register, research and test kits, define docs, Norwegian and English copy, `check_promo.py`, accessibility and performance runs, claims audit, docs | D-1 claims register |
| **Carlos** | Decisions and people | – | decisions, interviews and tests with real people, ChatGPT renders, photos of real boards, approvals | answer D1–D9 in [decisions.md](../decisions.md) |

The build starts at once on direction A, "Patina". If gate G3 picks direction B or C, only `tokens.css` and the fonts change. Copy, section order and images are data files, so research findings can change them without rework.

---

## 2. Waves: start all three agents now

| Wave | Antigravity | Cursor | DeepSeek | Carlos |
|---|---|---|---|---|
| **0 · Kickoff** (first hours) | A-1 canonical house<br>A-2 shot list and prompts | C-1 hotfix (prepare)<br>C-2 scaffold `web/promo` and handovers | D-1 claims register<br>D-2 research and test kit | answer D1–D9 and §2.2<br>OK or no for the hotfix deploy |
| **1 · Foundations** (day 1) | A-3 market scan<br>A-4 moodboard, style tiles and test pack<br>A-5 bathroom set and stand-ins into the site | C-3 tokens, fonts, base CSS<br>C-4 header, footer, hero, key facts, gallery | D-3 define docs v0<br>D-4 copy deck v0, then content JSON | book 5 interviews<br>regenerate renders in ChatGPT (if D5) |
| **2 · Full build** (days 2–3) | A-6 wireframes for the remaining sections<br>A-7 renders and fidelity<br>A-8 alt text, captions, OG image<br>A-9 visual review loop | C-5 tabs, passport, rooms, journey<br>C-6 status, FAQ, form, privacy<br>C-7 languages<br>C-8 SEO, 404, sticky bar<br>C-9 image pipeline | D-5 FAQ, privacy and meta copy<br>D-6 `check_promo.py`<br>D-7 accessibility and performance runs | run interviews<br>native reader checks the copy<br>G2, G3 |
| **3 · Test and polish** (days 3–5) | A-10 full visual QA at 4 widths, keyboard, zoom | C-10 fixes and changelog | D-8 interview and usability synthesis<br>D-9 claims audit | run the usability tests<br>G4 |
| **4 · Launch** (after G5) | A-11 live visual check<br>FINN kit images | C-11 move the lab, deploy, branch and commit (with OK) | D-10 live check, docs, FINN kit text | G5<br>OK for deploy and push |

The critical path: Carlos's decisions → Cursor's build → images approved at G4 → usability test → G5 → deploy. Anything that isn't on this path must never block it.

PLAN task 4.15 (P2: patina toggle, interactive 3D exploded view, FAQ-grounded assistant) is **deliberately unassigned** until after launch. Carlos assigns it at G5. Every other PLAN task has an owner in one of the three briefs.

---

## 3. Ownership map: one writer per file

| Path | Writer | Everyone else |
|---|---|---|
| `fase4/promo/PLAN.md`, `DESIGN-GUIDE.md`, `agents/*.md` | Carlos (drafted by Claude Code) | read only |
| `fase4/promo/decisions.md` | Carlos | may append Carlos's answer, quoting him, after re-reading the file |
| `fase4/promo/status/<agent>.md` and `status/<agent>-screens/` (self-check screenshots) | that agent | read only |
| `fase4/promo/canonical-house.md`, `bildeliste.csv`, `assets-source/**` | Antigravity | read only |
| `fase4/promo/01-empathize/market-scan.md` | Antigravity | read only |
| `fase4/promo/03-ideate/**`, except `card-sort.md` | Antigravity | read only |
| `fase4/promo/review/visual-review.md`, `05-test/screens/**` | Antigravity | read only |
| `fase4/promo/review/claude-code-review.md` | Claude Code (optional reviewer) | read only; each owner fixes findings in its own files |
| `fase4/promo/reference/**` (direction A built to DESIGN-GUIDE: the model for tile A and for Cursor's C-4/C-5) | Claude Code | read only; copy from it, don't edit it |
| `fase4/promo/finn-kit/images/**` | Antigravity | read only |
| `web/promo/src/assets/images/**`, `web/promo/src/content/images.json` | Antigravity, after Cursor's handover | read only |
| `web/promo/**`, everything else | Cursor | read only |
| `web/chat-demo/src/components/minihouse/MiniHouseFrontPage.tsx`, `web/chat-demo/public/concepts/` | Cursor, hotfix only | – |
| `web/promo-holding/**`; in `web/chat-demo`, `MiniHouse3DSimulator.tsx` and `src/index.html` | Cursor: the holding page, and only the three app fixes in `agents/task-holding-page.md` | read only |
| `fase4/promo/archive/**`, `05-test/changelog.md` | Cursor | read only |
| `fase4/promo/01-empathize/**` except `market-scan.md`; `02-define/**`; `03-ideate/card-sort.md`; `04-prototype/**` | DeepSeek | read only |
| `web/promo/src/content/nb.json`, `en.json` | DeepSeek, after Cursor's handover | read only |
| `fase4/promo/05-test/*.md` except `changelog.md` | DeepSeek | read only |
| `fase4/promo/finn-kit/annonse.md`, `scripts/check_promo.py` | DeepSeek | read only |
| `docs/despliegue-web.md`, the Fase 4 lines in `PROJECT.md` | DeepSeek, at launch only | – |
| Everything else in the repo | nobody in this project | don't touch |

**Never edit a file you don't own.** If you need a change, write it under "Requests" in your own status file, addressed as "→ Cursor:", "→ Antigravity:" or "→ DeepSeek:". The owner reads every status file before each task.

---

## 4. Contracts that let you work in parallel

### 4.1 Content files (Cursor creates them, DeepSeek owns them)

- `web/promo/src/content/schema.ts` belongs to Cursor and defines a TypeScript type for every key.
- `web/promo/src/content/nb.json` and `en.json` belong to DeepSeek and must match the schema. `npm run check` fails when a key is missing.
- Cursor creates both JSON files once, with the keys below and `"TODO"` as every value, then writes **HANDOVER content** in its status file. From then on only DeepSeek edits them. If Cursor needs a new key, it adds it to `schema.ts` and lists it in its status file; DeepSeek fills in the value.

```text
meta.title, meta.description, meta.ogAlt
nav.skip, nav.house, nav.materials, nav.moving, nav.questions, nav.cta, nav.menu, nav.close, nav.language
hero.title, hero.lead, hero.cta, hero.gallery, hero.caption
facts.items[]        { label, value }
gallery.title, gallery.count, gallery.prev, gallery.next, gallery.close
build.title, build.lead, build.tabExterior, build.tabStructure, build.exterior, build.structure
materials.title, materials.lead, materials.passportTitle
materials.rows       { material, origin, previousUse, usedFor, treatment, status }
materials.items[]    { id, name, lead, passport { material, origin, previousUse, usedFor, treatment, status } }
living.title, living.lead, living.rooms[] { id, title, body }
journey.title, journey.steps[] { title, body }
status.title, status.body, status.phases[] { name, state }
faq.title, faq.items[] { q, a }
interest.title, interest.lead
interest.fields      { email, name, optional }
interest.consent, interest.submit, interest.success, interest.errors { required, email, network }
footer.contact, footer.privacy, footer.pro, footer.docs, footer.lab, footer.imagesNote
privacy.title, privacy.body
```

### 4.2 Images (Cursor creates them, Antigravity owns them)

`web/promo/src/content/images.json` is an array of entries like this one:

```json
{ "id": "hero-slope", "file": "hero-slope.jpg", "kind": "render", "status": "stand-in",
  "alt": { "nb": "…", "en": "…" }, "caption": { "nb": "Konseptbilde", "en": "Concept image" },
  "source": "images/MiniHouse cabin on a Norwegian slope-2.png (crop)", "focal": "50% 55%" }
```

- **`status`** takes one of three values:
  - `approved`: Carlos has approved it at G4.
  - `pending`: final image, waiting for G4.
  - `stand-in`: a crop or placeholder for development. **A release build fails on `stand-in` and `pending`.**
- **`kind`** is `render`, `photo` or `texture`.
- **Files** live in `web/promo/src/assets/images/` as JPEG or PNG masters, at least as large as DESIGN-GUIDE §7 requires. Astro produces the AVIF and WebP versions.
- **Ids:** `hero-slope`, `meadow-wide`, `exploded`, `living`, `kitchen`, `bench`, `storage`, `bath-shower`, `bath-vanity`, `bath-window`, `bath-doorway`, `journey-workshop`, `journey-truck`, `journey-plot`, `texture-malmfuru`, `texture-eik`, `texture-kobber`, `texture-stal`, `og-image`.
- **Missing images:** until an image exists, Cursor's figure component shows a plain eik block with «Bilde kommer», never a random or stock picture.

### 4.3 Dev servers

- Only Cursor runs `npm install`, `npm run dev` (port **4321**) and `npm run build`.
- When a section is ready for review, Cursor runs `npm run build && npm run preview -- --port 4322` and says so in its status file.
- Antigravity takes screenshots on 4321 or 4322. DeepSeek runs Lighthouse and axe against 4322. Nobody else starts a server on these ports.

---

## 5. Protocol

1. **Before each task,** read the other two status files and [decisions.md](../decisions.md).
2. **After each task,** add an entry at the top of your status file (each file contains a template).
3. **Use these labels:** **HANDOVER** when you hand something over, **BLOCKED** when you are stuck, and "→ Agent:" for requests.
4. **Carlos's explicit OK** in that agent's own chat is required for gates G1–G5, every deploy, every `git commit` or `push`, and anything public. Cursor is the only agent that runs git, always on the branch `web/promo-r1`.
5. **Leave the other uncommitted files alone.** The working tree holds about 60 uncommitted files from other sessions.
6. **If two tasks seem to need the same file,** stop and write BLOCKED. Don't "quickly fix" someone else's file.
7. **Before anything counts as done,** it must pass the design guide's [definition of done](../DESIGN-GUIDE.md) (§11). "Done" without screenshots and a visual review doesn't count.

---

## 6. Carlos's list, ordered by what unblocks the most

1. Answer D1–D9 and the §2.2 questions in [decisions.md](../decisions.md). It takes about 15 minutes, and the recommendations are already filled in.
2. Say yes or no to Cursor's hotfix (C-1), so the container image with false claims comes off the live site.
3. If D5 is "Carlos": regenerate the renders in ChatGPT with Antigravity's prompts (`03-ideate/shot-list.md`) and save them in `fase4/promo/assets-source/inbox/`.
4. Photograph your real reclaimed boards in daylight (close-ups, end grain) for the material textures, and save them in the same inbox.
5. Book and run 5 interviews with DeepSeek's kit. Put your raw notes in `fase4/promo/01-empathize/interviews/raw/`. **The GitHub repo is public,** so that folder and `01-empathize/carlos-interview.md` are git-ignored: they stay on this PC and are never pushed. DeepSeek turns the notes into anonymised P1–P5 files without initials, and only those may be committed.
6. Find a native Norwegian speaker to read the copy deck.
7. Approve G2 (brief), G3 (direction), G4 (content and images) and G5 (launch).

## 7. Optional: a design check by Claude Code

At G3 (style tiles) and again before G5, you can ask Claude Code to review `fase4/promo` and `web/promo` against DESIGN-GUIDE.md. It takes screenshots, critiques them with the frontend-design skill and reports the findings.
