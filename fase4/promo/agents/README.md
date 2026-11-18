# MiniHouse promo website · Who does what

Revision R2, 2026-11-18. Antigravity, Cursor and DeepSeek build the site **at the same time**, each in its own lane and its own files. Carlos makes the decisions. The *what* is in [PLAN.md](../PLAN.md), the *look and the words* are in [DESIGN-GUIDE.md](../DESIGN-GUIDE.md), and this file covers the *who*.

**Two things changed on 2026-11-18:**

- **There is no design-thinking process (D14).** Interviews, personas, the card sort, preference and usability tests, style tiles and gate G2 are cancelled. Their files are in `archive/design-thinking/`. Don't read, extend or cite them, and don't ask Carlos for research.
- **The look is «Patina, made funkier» (G3).** The light Patina site stays as built, plus the funk moves in DESIGN-GUIDE §2.1 (five since R2.4). The built example is in [reference/](../reference/index.html). Direction C (Stavkirke) is not used.

The briefs:

- [Cursor](cursor.md): code
- [Antigravity](antigravity.md): images and visual QA
- [DeepSeek](deepseek.md): words and checks
- WorkBuddy has no standing brief. It joins for single tasks, most recently [task-film-v18.md](task-film-v18.md): the 4K film (closed on 2026-11-18).
- Grok has no standing brief either. It joins DeepSeek for [task-story-page.md](task-story-page.md): Carlos's story page «Hvordan ideen oppstod».

---

## 1. The split

| Agent | Lane | First task now |
|---|---|---|
| **Cursor** | the code in `web/promo/`, the image pipeline, deploys and git (each with Carlos's OK) | C-12b: review Claude Code's C-12 and remove `living.rooms` from the schema |
| **Antigravity** | images, alt text and visual QA. It can see screenshots. | A-9: review Claude Code's C-12 at 4 widths, then A-12 |
| **DeepSeek** | copy, the claims register and the automated checks. It **can't see images**, so it never judges visuals. | D-16 and D-17 of the film task if they're open, then [task-story-page.md](task-story-page.md): D-18 to D-23; D-12 and D-11 after |
| **Codex** | supervisor, if Carlos uses it | follows this file; edits only what its task names |
| **WorkBuddy** | the project's engineering agent (`.workbuddy-ai/`). It runs scripts and sees its output through Playwright screenshots. | none: [task-film-v18.md](task-film-v18.md) (W-1 to W-7) closed on 2026-11-18 |
| **Grok** | the xAI Grok CLI (`grok`), started in the repo root with the folder trusted. It edits code, runs the build and Playwright, and can look at screenshots. It never generates images for this site. | [task-story-page.md](task-story-page.md): G-1 to G-8, Carlos's story page |
| **Claude Code** | `PLAN.md`, `DESIGN-GUIDE.md`, the briefs, `reference/` and its review. On 2026-11-18, at Carlos's request, it also built C-12 in `web/promo`: see [its log](../status/claude-code.md). | – |
| **Carlos** | decisions, renders and photos | D6, then G4 and G5 (§5) |

The critical path is D6 (the follow form), the new images, G4, G5 and then the deploy. Nothing else may block it.

---

## 2. Ownership map: one writer per file

| Path | Writer | Everyone else |
|---|---|---|
| `fase4/promo/PLAN.md`, `DESIGN-GUIDE.md`, `agents/*.md`, `reference/**`, `web/promo/DESIGN.md` | Claude Code, for Carlos | read only; copy from the reference, don't edit it |
| `fase4/promo/decisions.md` | Carlos | may append Carlos's answer, quoting him, after re-reading the file |
| `fase4/promo/status/<agent>.md`, `status/<agent>-screens/`, including `status/claude-code.md` | that agent | read only |
| `fase4/promo/canonical-house.md`, `shot-list.md`, `bildeliste.csv`, `assets-source/**` | Antigravity | read only |
| `fase4/promo/review/visual-review.md`, `qa/screens/**`, `scripts/run_visual_qa.py`, `scripts/test_dialog_sticky.py` | Antigravity | read only |
| `web/promo/src/assets/images/**`, `web/promo/src/content/images.json` | Antigravity | read only |
| The concept film: `web/promo/public/film/**`, `web/promo/src/assets/film/**`, `web/promo/src/content/films.json` | Antigravity (made by Claude Code on 2026-11-18) | read only |
| `scripts/cut_film.py` | Claude Code | read only; ask Claude Code to re-run it when the walkthrough changes |
| **While [task-story-page.md](task-story-page.md) is open** (paths in `web/promo/`):<br>• new: `src/pages/historien.astro`, `src/pages/en/historien.astro`, `src/components/Story.astro`, `src/components/StoryTeaser.astro`, `src/styles/story.css`;<br>• edits: `src/content/schema.ts`, `scripts/content-contract.mjs`, `src/layouts/Base.astro`, `src/content/locale-paths.ts`, `src/components/SiteHeader.astro`, both `index.astro` files, and only the header rules in `src/styles/base.css`;<br>• `status/grok.md` and `status/grok-screens/` | Grok, instead of Cursor. DeepSeek keeps its own files, listed in the task | read only; Cursor and Antigravity leave these files alone until the task is closed |
| `fase4/promo/review/claude-code-review.md` | Claude Code | read only; each owner fixes findings in its own files |
| `web/promo/**`, apart from the files listed for Antigravity, DeepSeek and Claude Code | Cursor | read only |
| `web/promo-holding/**`, and the `web/chat-demo` files named in [task-holding-page.md](task-holding-page.md) | Cursor | read only |
| `fase4/promo/archive/rejected-renders/**`, `qa/changelog.md` | Cursor | read only |
| `fase4/promo/content/**`: claims register, sitemap, copy decks | DeepSeek | read only |
| `web/promo/src/content/nb.json`, `en.json` | DeepSeek | read only |
| `fase4/promo/qa/*.md` except `changelog.md`, `qa/reports/**`, `scripts/check_promo.py` | DeepSeek | read only |
| `docs/despliegue-web.md`, the Fase 4 lines in `PROJECT.md` | DeepSeek, at launch only | – |
| `fase4/promo/archive/design-thinking/**` | nobody | don't read, don't edit |
| Everything else in the repo | nobody in this project | don't touch |

**Never edit a file you don't own.** If you need a change, write it under "Requests" in your own status file, addressed as "→ Cursor:", "→ Antigravity:" or "→ DeepSeek:". The owner reads every status file before each task.

---

## 3. Contracts that let you work in parallel

### 3.1 Content files

- `web/promo/src/content/schema.ts` belongs to Cursor and defines a TypeScript type for every key.
- `nb.json` and `en.json` belong to DeepSeek and must match the schema. `npm run check` fails when a key is missing.
- **New key:** Cursor adds it to `schema.ts` and lists it in its status file, and DeepSeek fills in both languages.
- **Removed key:** Cursor removes it from `schema.ts` and the component and lists it, and then DeepSeek removes it from both JSON files.

The key groups are listed in [content/sitemap.md](../content/sitemap.md) §4.

### 3.2 Images

`web/promo/src/content/images.json` has one entry per image:

```json
{ "id": "hero-slope", "file": "hero-slope.jpg", "kind": "render", "status": "stand-in",
  "alt": { "nb": "…", "en": "…" }, "caption": { "nb": "Konseptbilde", "en": "Concept image" },
  "source": "images/MiniHouse cabin on a Norwegian slope-2.png (crop)", "focal": "50% 55%" }
```

- **`status`** is one of:
  - `approved`: Carlos approved it at G4.
  - `pending`: a final image waiting for G4.
  - `stand-in`: a crop for development. **A release build fails on `stand-in` and `pending`.**
- **`kind`** is `render`, `photo` or `texture`.
- **Files** are JPEG or PNG masters in `web/promo/src/assets/images/`. Astro makes the AVIF and WebP versions. They stay out of git, because the repo is public.
- **A missing image** shows a plain eik block with «Bilde kommer», never a random or stock picture.

### 3.3 Dev servers

- Only Cursor runs `npm install`, `npm run dev` (port **4321**) and `npm run build`, always with the system Node (`C:\Program Files\nodejs`).
- When a change is ready for review, Cursor runs `npm run build && npm run preview -- --port 4322` and says so in its status file.
- Antigravity takes screenshots on 4321 or 4322, and DeepSeek runs its checks against 4322. Nobody else starts a server on these ports.
- **While [task-story-page.md](task-story-page.md) is open,** Grok runs `npm run check`, `npm run build` and the 4322 preview in Cursor's place. It adds no dependencies, and it never stops a server it didn't start.

---

## 4. Protocol

1. **Before each task,** read the other status files and [decisions.md](../decisions.md).
2. **After each task,** add a dated entry at the top of your status file, using the template there.
3. **Use these labels:** **HANDOVER** when you hand something over, **BLOCKED** when you are stuck, and "→ Agent:" for requests.
4. **Carlos's explicit OK** in that agent's own chat is required for G4, G5, every deploy, every `git commit` or `push`, and anything public. Cursor is the only agent that runs git, always on the branch `web/promo-r1`.
5. **Leave the other uncommitted files alone.** The working tree holds uncommitted work from other sessions.
6. **If two tasks seem to need the same file,** stop and write BLOCKED. Don't "quickly fix" someone else's file.
7. **Before anything counts as done,** it passes the design guide's [definition of done](../DESIGN-GUIDE.md) (§11), including screenshots at 360 px and 1280 px.

---

## 5. Carlos's list, ordered by what unblocks the most

1. **D6:** name the inbox and the form service for «Følg prosjektet». Until then there is no form and no copper band.
2. **The workshop image:** render it in ChatGPT with the `journey-workshop` prompt from [shot-list.md](../shot-list.md), at least 1600 × 1200 (4:3), and save it in `fase4/promo/assets-source/inbox/`. The other renders in the shot list follow the same way when you have time.
3. **Photos of the real reclaimed boards** in daylight (close-ups and end grain), and of the steel base if it exists, saved in the same inbox. They are the strongest proof for the material passports.
4. **Look at the preview.** Claude Code's C-12 is built and served at http://127.0.0.1:4322/ while Cursor's preview runs. Then approve G4 (content and images) and G5 (launch).
5. **Optional:** ask a native Norwegian speaker to read the copy before G4.
6. **Your story page:** when Grok writes its HANDOVER, open https://minihouse-preview.canner.app/historien/ and look at it.
   - **Your own photos (optional):** photos you took yourself of the old timber at Øvsttunvegen can go on the story page. Use only photos you may publish, with no one's face in them, and save them in `fase4/promo/assets-source/inbox/`. Until you add and approve them, the page shows no picture of the old building.
