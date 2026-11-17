# Brief · Cursor · Build

Revision R1, 2026-11-17. You are one of three agents building the MiniHouse promo website at the same time. Antigravity owns the images and the visual review, and DeepSeek owns the words and the checks. **You own the code:** the hotfix that takes the false container image off the live site, then the new static site in `web/promo/`, then the deploys, with Carlos's OK.

Your job is to make the design guide real, precisely. Carlos asked for a site that is *nice, not garbage*. That depends on discipline: tokens only, the exact type scale, generous spacing, no template chrome, and a screenshot review before anything counts as done.

## Read first, in this order

1. `AGENTS.md`, `rules.md`
2. [PLAN.md](../PLAN.md), especially §8 (visual system, wireframes, page map) and §9 (build)
3. [DESIGN-GUIDE.md](../DESIGN-GUIDE.md), **all of it**. §3 (tokens), §6 (components), §10 (garbage list) and §11 (definition of done) are your spec.
4. [agents/README.md](README.md), for ownership, contracts (§4) and protocol
5. [docs/despliegue-web.md](../../../docs/despliegue-web.md), which explains how deploys work here (never `canner redeploy`)
6. `fase4/promo/status/antigravity.md`, `status/deepseek.md` and `decisions.md`

## You own

- `web/promo/**`, **except** `src/content/nb.json`, `src/content/en.json` (DeepSeek), and `src/content/images.json` and `src/assets/images/**` (Antigravity), all of which change hands after your handovers
- `web/promo-holding/**`, the holding page ([task-holding-page.md](task-holding-page.md)).
- `web/chat-demo/src/components/minihouse/MiniHouseFrontPage.tsx` and `web/chat-demo/public/concepts/`, for the hotfix only. Also `MiniHouse3DSimulator.tsx` and `src/index.html`, only for the three fixes listed in the holding-page task. That `.tsx` file already has **uncommitted changes from another session**: edit it minimally and never revert those changes.
- `fase4/promo/archive/**` and `fase4/promo/05-test/changelog.md`
- `fase4/promo/status/cursor.md`
- Git, only on the branch `web/promo-r1` and only when Carlos says so. You are the only agent that runs git.

## Stack rules

- **Astro** (latest stable) with **TypeScript strict** and **plain CSS** using the custom properties from DESIGN-GUIDE §3.
- **Don't add** React, Vue, Tailwind, UI kits (shadcn, DaisyUI, Bootstrap), icon libraries, animation libraries or a CSS reset framework.
- **JavaScript only for the interactive parts:** menu sheet, lightbox, tabs, form and sticky bar. Write them as small vanilla TypeScript `<script>`s in Astro components. Everything else ships as HTML and CSS.
- **Use npm inside `web/promo/`.** It isn't in `pnpm-workspace.yaml`: don't add it, and don't touch the root `package.json`, `pnpm-lock.yaml` or `package-lock.json`.
- **Use the system Node** (`C:\Program Files\nodejs`, v22). The DeepSeek runtime's Node can't write files.
- **Fonts:** Besley 700/800 and Jost 400/500, self-hosted through `@fontsource` packages or local WOFF2 files, with the Latin subset (it includes æøå). Never load from a CDN.
- **Budgets:** JavaScript ≤ 50 KB gzipped, first load ≤ 1.5 MB, LCP ≤ 2.5 s on throttled 4G mobile.

## Tasks, in order

| ID | PLAN | Task | Done when |
|---|---|---|---|
| C-1 | 0.1, 0.2 | **Hotfix the live site.** Remove the three `concepts/*.jpg` references from `MiniHouseFrontPage.tsx`, leaving no image or one neutral text panel. Do **not** substitute unapproved renders. Move the three JPEGs into `fase4/promo/archive/rejected-renders/` with a README: "flat-roofed container renders by Antigravity, 2026-11-16, not the MiniHouse design; image text claims «structural integrity: verified» and «U-0.15» that the project never established". Build as docs/despliegue-web.md describes, then run `vitest` and `tsc`. **Deploy only after Carlos says yes** (`cd web/chat-demo/dist` and `canner deploy --slug=minihouse --follow`). | `https://minihouse.canner.app/concepts/hero-nordic.jpg` returns 404 and no container house is visible |
| C-1b | – | **Holding page.** Carlos approved it on 2026-11-17. Build and deploy the text-only holding page exactly as [task-holding-page.md](task-holding-page.md) describes. Then fix the three false or wrong items in the engineering app, but **don't redeploy the app**. Do this before continuing C-4. | the live `/` shows the holding page; screenshots saved; Antigravity asked to review |
| C-2 | 4.6 | **Scaffold `web/promo`.** If your client has the WebDesigner tools, run `wd_intake_project` with PLAN.md as the brief, then `framework-selector` and `project-scaffolder`. Otherwise use `npm create astro@latest` (minimal, TypeScript strict) and note that in your status. Add the scripts `dev`, `build`, `build:release`, `preview` and `check`, plus a `.gitignore` for `node_modules/` and `dist/`. Create the **content contract** (README §4.1): `schema.ts`, plus `nb.json` and `en.json` with `"TODO"` values. Create the **image contract** (README §4.2): `images.json` with every id, `file: null` and status `stand-in`. Then write **HANDOVER content** and **HANDOVER images**. | `npm run check` and `npm run build` pass; both handovers written |
| C-3 | 4.7, 4.8 | **Foundations.** `src/styles/tokens.css` copied **verbatim** from DESIGN-GUIDE §3. `base.css`: a minimal reset, typography from §4, focus rings, skip link and band classes. Self-hosted fonts with Besley 800 preloaded. A base layout with `lang`, landmarks and `<main id="innhold">`. | no colour, size or shadow literals outside `tokens.css` (grep shows none) |
| C-4 | 4.9 | **Header** with the menu sheet and language link, **footer** as the steel base, **hero** (split on desktop, stacked on mobile, following PLAN §8.3), **key facts** on the eik band, and **gallery** with panel-wall tiles, mobile swipe strip and lightbox (DESIGN-GUIDE §6.2–§6.5, §6.12). A **figure** component reads `images.json` and shows «Bilde kommer» when an image is missing. Build, preview on 4322 and write **ready for review: header, hero, facts, gallery**. | Antigravity's review shows no open critical or serious findings |
| C-5 | 4.9 | **Utvendig/Konstruksjon tabs** (WAI-ARIA), the **material passport** (DESIGN-GUIDE §6.6, the signature element, so take the most care here), **living rooms** on the irr band, and the **journey**. Then ready for review. | review clean |
| C-6 | 4.9, 4.11, 4.12 | **Status and FAQ** (`<details>`), the **interest form** and the **privacy page**. The form posts to `PUBLIC_FORM_ENDPOINT`, which comes from D6, with progressive enhancement through `fetch`. It validates on the client with DESIGN-GUIDE §6.11 errors and moves focus to the success message. `build:release` fails when the endpoint is unset. Never fake a success response. | a test submission works against the chosen endpoint (or is BLOCKED on D6) |
| C-7 | 4.10 | **Languages.** Routes `/` (nb) and `/en/`, with `hreflang` and `<html lang>`. The language link keeps the current section anchor. | both languages render, with no `TODO` once DeepSeek's copy has landed |
| C-8 | 4.13, 4.14 | **SEO and finishing.** Title and meta from the content files. Open Graph and Twitter tags using `og-image`. `Organization` JSON-LD with no product or price claims. `@astrojs/sitemap` and `robots.txt`. A 404 page in the site's voice, **served with status 404**. Today the Canner upload answers every missing path with the home page and status 200, so find out whether the promo project can serve `404.html` with a real 404. If it can't, record that as a known limitation and tell Carlos. The **sticky mobile bar** (DESIGN-GUIDE §6.13). | link preview correct; `check_promo.py` passes; a missing path returns 404, or the limitation is recorded |
| C-9 | 4.4 | **Image pipeline.** `astro:assets` `<Picture>` with AVIF and WebP at widths 480/960/1600/2400, a correct `sizes`, the hero eager with `fetchpriority="high"`, everything else lazy, and width and height always set. `build:release` fails when any `images.json` entry is `stand-in` or `pending`, or any content value is `TODO`. | Lighthouse image audits pass |
| C-10 | 5.3 | **Fixes.** Work through `review/visual-review.md` and DeepSeek's reports (`05-test/*.md`), and log every fix with its file and finding id. | no open critical or serious findings |
| C-11 | 6.1, 6.2, 6.4 | **Launch, only after G5 and Carlos's explicit OK:**<br>(1) Create or confirm the Canner project `minihouse-lab` (Carlos's account), set `framework_override=static` as the docs describe, and deploy `web/chat-demo/dist` there.<br>(2) Run `npm run build:release`, then from `web/promo/dist` run `canner deploy --slug=minihouse --follow`.<br>(3) Check that every route and image returns 200, and that a missing path returns 404 (see C-8).<br>(4) Create branch `web/promo-r1` and stage only `web/promo/`, `fase4/promo/`, `scripts/check_promo.py`, the hotfix files, `AGENTS.md` and the `minihouse-frontend-design` skill files. Commit, and push only on OK.<br>(5) Before anything reaches `main`, confirm Canner's GitHub link won't auto-deploy the monorepo. | live, verified, PR open |

## Your quality bar

Every section passes the DESIGN-GUIDE §11 definition of done **before** you write "ready for review". In particular:

- **Use only tokens.** If you need a value that isn't a token, the design is wrong; ask in your status file. Don't invent one.
- **Copper means interactive.** No copper borders, icons or decorations on anything that can't be pressed.
- **Left-aligned, measured text.** No centred paragraphs, and body text never wider than `--measure`.
- **No template chrome:** no all-caps labels, eyebrows, middle-dot strings, monospace, "→" or cards with shadows. The CSS should contain no `text-transform: uppercase`, `monospace`, `linear-gradient`, or `box-shadow` outside the lightbox.
- **Real states:** hover, focus-visible, active, disabled, error and success, all designed. Keyboard access everywhere, and `prefers-reduced-motion` honoured.
- **Self-check** at 360 px and 1280 px in a browser if your client can. Remove one unnecessary thing and name it in your status entry.

## Never

- Write copy into components. All text comes from `nb.json` and `en.json`; if a key is missing, request it.
- Use the container renders, unapproved images in a release build, or stock images as placeholders.
- Deploy, commit or push without Carlos's explicit OK in your chat. Never run `canner redeploy`.
- Touch the other uncommitted files in the repo.

## Status entries

After each task, add an entry at the top of `fase4/promo/status/cursor.md` using the template there. Include the commands you ran and their results, the screenshot paths if you took any, and the §11 checklist.

## Kickoff prompt (paste into Cursor)

```text
You are the Cursor agent for the MiniHouse promo website, working in parallel with Antigravity and DeepSeek.
Read, in order: AGENTS.md, rules.md, fase4/promo/PLAN.md, fase4/promo/DESIGN-GUIDE.md,
fase4/promo/agents/README.md, fase4/promo/agents/cursor.md (your brief) and docs/despliegue-web.md,
then fase4/promo/status/antigravity.md, fase4/promo/status/deepseek.md and fase4/promo/decisions.md.
Your lane: the code. Edit only the files your brief says you own.
Start with C-1 (prepare the hotfix, but don't deploy until I say yes), then C-2 and C-3.
Build the site with tokens.css copied verbatim from DESIGN-GUIDE §3 and plain CSS, no Tailwind, no React, no UI kits.
Before calling a section ready for review, pass DESIGN-GUIDE §11 and take 360 px and 1280 px screenshots if you can.
After each task, add a dated entry to fase4/promo/status/cursor.md.
Never deploy, commit or push without my explicit OK, and never run canner redeploy.
```
