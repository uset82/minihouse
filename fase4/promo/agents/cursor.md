# Brief · Cursor · Code

Revision R2, 2026-11-18. You own the code of the MiniHouse promo site in `web/promo/`, the deploys and git, each with Carlos's OK. Antigravity owns the images and the visual review, and DeepSeek owns the words and the checks.

Most of the site is built (R1 tasks C-1 to C-9; see your log). The look is «Patina, made funkier» (G3), and there is no design-thinking process (D14). Don't build anything for interviews, usability rounds or style tiles.

**Update, 2026-11-18:** at Carlos's request, Claude Code built C-12 itself: the mirror frame, the irr collage, the giant numerals, the contact-sheet gallery, the hanging passport tags, the two-column build section, the hero bleed and the footer wordmark. Its files and checks are in [status/claude-code.md](../status/claude-code.md). Start with C-12b.

## Read first, in this order

1. `AGENTS.md`, `rules.md`
2. [PLAN.md](../PLAN.md) R2
3. [DESIGN-GUIDE.md](../DESIGN-GUIDE.md) R2, **all of it**. §6.8, §6.9, §6.11 and §6.14 are new or changed.
4. The reference: open [reference/index.html](../reference/index.html), then read `reference/tile-a.html` and `tile-a.css`. This is the built example you port.
5. [agents/README.md](README.md): ownership, contracts and protocol
6. [docs/despliegue-web.md](../../../docs/despliegue-web.md): how deploys work here (never `canner redeploy`)
7. `status/antigravity.md`, `status/deepseek.md` and [decisions.md](../decisions.md)

## You own

- `web/promo/**`, **except** `src/content/nb.json` and `en.json` (DeepSeek), and `src/content/images.json` and `src/assets/images/**` (Antigravity)
- `web/promo-holding/**`, and the `web/chat-demo` files named in [task-holding-page.md](task-holding-page.md)
- `fase4/promo/archive/rejected-renders/**` and `fase4/promo/qa/changelog.md`
- `fase4/promo/status/cursor.md`
- Git, only on the branch `web/promo-r1` and only when Carlos says so

## Stack rules (unchanged)

- Astro 7.4.1 with TypeScript strict and plain CSS through the custom properties in `tokens.css`. Use npm inside `web/promo/` with the system Node (`C:\Program Files\nodejs`, v22).
- Don't add React, Vue, Tailwind, UI kits, icon libraries, animation libraries or a CSS reset framework.
- JavaScript only for the menu sheet, lightbox, tabs, form and sticky bar.
- Fonts are self-hosted through `@fontsource`. Nothing loads from a CDN.
- Budgets: JavaScript ≤ 50 KB gzipped, first load ≤ 1.5 MB, LCP ≤ 2.5 s on throttled 4G.

## Tasks, in order

| ID | Task | Done when |
|---|---|---|
| C-12 | **Done by Claude Code, 2026-11-18.** The funk layer is ported. The notes below describe what was built. | – |
| C-12b | **Review and tidy C-12.** Read Claude Code's diff in `web/promo/src` and keep it. Remove `living.rooms` from `schema.ts` and the content contract, since the room list is no longer rendered, then ask DeepSeek to remove the keys. Fix anything Antigravity's A-9 review finds. | `npm run check`, `npm run build` and `check_promo.py --dist` pass; Antigravity's review has no open critical or serious findings |
| C-13 | **Follow form in the copper band, after D6 only** (DESIGN-GUIDE §6.11). Post to `PUBLIC_FORM_ENDPOINT` with progressive enhancement through `fetch`, validate on the client, and move focus to the success message. `build:release` fails when the endpoint is unset. Never fake a success response. Then mount the sticky bar (§6.13) and the header button «Følg prosjektet». | a test submission arrives at the endpoint Carlos chose |
| C-10 | **Fixes** from `review/visual-review.md`, `review/claude-code-review.md` and DeepSeek's reports in `qa/`. Log each fix with its file and finding id in `qa/changelog.md`. | no open critical or serious findings |
| C-11 | **Launch, only after G5 and Carlos's explicit OK.** Move the lab to `minihouse-lab` first (`web/chat-demo/dist`, `framework_override=static`). Run `npm run build:release` and `npm run bundle`, then from `web/promo/.bundle` run `canner deploy --slug=minihouse --follow`. The bundle carries `deploy/serve.mjs` (byte ranges, MIME types, a real 404, no dotfiles): don't upload `dist/` on its own, because the film won't play in Safari. Check that every route and image returns 200, a missing path returns 404, `/film/house-film.mp4` answers a range with 206, and `/.env.production` returns 404. Commit only the promo files on `web/promo-r1`, and push only on OK. | live and verified |

### What Claude Code changed after C-12 (2026-11-18, DESIGN-GUIDE R2.2 and R2.3)

- **Four UX fixes:**
  - «Inne i MiniHouse» now follows the key facts in both index pages;
  - the materials use a compact row below 64rem, in `base.css`;
  - `Build.astro` replaces `BuildTabs.astro`: two views, no tabs;
  - «Huset» in the menu goes to `#bilder` (`SiteHeader.astro`).
- **The concept film:**
  - `Film.astro`;
  - `MirrorFrame.astro` film mode;
  - `src/scripts/film.ts`: one shared play/pause state, kept in `sessionStorage`;
  - `src/content/films.ts` and `films.json`;
  - the `film.*` keys in `schema.ts` and `content-contract.mjs`;
  - a film status check in `release-check.mjs`.

  The media come from `scripts/cut_film.py`.
- **For C-11, add one launch check:** Canner must answer byte-range requests for `/film/*.mp4` with 206, or Safari won't play the film.

### What C-12 built (DESIGN-GUIDE R2.1 is the spec)

- **`MirrorFrame.astro`** (§6.14): the clip path and the copper frame, both copied from `reference/tile-a.html`, around `bath-window`.
- **`Living.astro`** (§6.8): the 12-column collage. The room list is gone, but `living.rooms` is still in `schema.ts`; removing it is C-12b.
- **`Journey.astro`** (§6.9): giant numerals over 4:3 photos.
- **`Gallery.astro`** (§6.5): the contact sheet. The tile ratio is computed from each master and passed as `--ar`.
- **`Materials.astro`** (§6.6): the passports are plain markup, with no `<details>`. The hanging tags are pure CSS from `64rem`.
- **`BuildTabs.astro`** (§6.7), `Figure.astro` (the new `step` ratio and updated `sizes`), `SiteFooter.astro` (§6.12), and `base.css`.
- **The copper band** (§6.11) is still C-13, after D6.

## Your quality bar

- **Tokens only.** If you need a value that isn't a token or an allowed literal (§3), ask in your status file. Don't invent one.
- **Copper means "press here".** The mirror frame is the one exception, and it's used once.
- **No template chrome:** no all-caps labels, eyebrows, middle-dot strings, monospace, "→" or cards with shadows. The CSS has no `text-transform: uppercase`, `monospace`, `linear-gradient`, or `box-shadow` outside the lightbox.
- **Real states:** hover, focus-visible, active, disabled, error and success. Keyboard access everywhere, and `prefers-reduced-motion` respected.

## Never

- Write copy into components. All text comes from `nb.json` and `en.json`; if a key is missing, request it.
- Use the container renders, unapproved images in a release build, or stock images as placeholders.
- Deploy, commit or push without Carlos's explicit OK in your chat. Never run `canner redeploy`.
- Touch the other uncommitted files in the repo, or anything in `archive/design-thinking/`.

## Status entries

After each task, add an entry at the top of `fase4/promo/status/cursor.md` with the commands you ran and their results, the screenshot paths and the DESIGN-GUIDE §11 checklist.

## Kickoff prompt (paste into Cursor)

```text
You are the Cursor agent for the MiniHouse promo website, working in parallel with Antigravity and DeepSeek.
The design-thinking work is archived (D14) and the look is «Patina, made funkier» (G3).
Read, in order: AGENTS.md, rules.md, fase4/promo/PLAN.md (R2), fase4/promo/DESIGN-GUIDE.md (R2),
fase4/promo/reference/index.html with tile-a.html and tile-a.css, fase4/promo/agents/README.md,
fase4/promo/agents/cursor.md (your brief) and docs/despliegue-web.md,
then fase4/promo/status/antigravity.md, fase4/promo/status/deepseek.md and fase4/promo/decisions.md.
Claude Code already built C-12 (fase4/promo/status/claude-code.md). Start with C-12b: review that diff and remove living.rooms from the schema.
Edit only the files your brief says you own. Tokens only, plain CSS, no new libraries.
Before calling it ready for review, pass DESIGN-GUIDE §11 with 360 px and 1280 px screenshots.
After each task, add a dated entry to fase4/promo/status/cursor.md.
Never deploy, commit or push without my explicit OK, and never run canner redeploy.
```
