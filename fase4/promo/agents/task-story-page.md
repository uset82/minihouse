# Task · Grok and DeepSeek build Carlos's story page «Hvordan ideen oppstod»

Revision 1, 2026-11-18. Written by Claude Code at Carlos's request. **Grok** and **DeepSeek** carry it out, and Carlos decides. Who owns which file is in [README.md](README.md). The page's full spec is [DESIGN-GUIDE §6.16](../DESIGN-GUIDE.md), and the decisions are in [decisions.md](../decisions.md) (D11 as amended, D15).

## What Carlos asked

> «generate a detail task plan so deepseek and grok execute your plan · make sure deepseek and grok use /frontend-design:frontend-design and /design style so the fonts and design is modern funky natural cooper norwegian trees natural colors style palette · the page has to writen in Fluent norwegian»

He pasted his story in Norwegian and English. Both texts are in [Appendix A](#appendix-a--carloss-texts-verbatim), exactly as he sent them. His answers on 2026-11-18:

| Question | His answer | What it means |
|---|---|---|
| Emergency housing, which D11 kept off the site | «Story page only» | The story page tells the emergency-housing purpose in his words. The home page still shows MiniHouse as a minihouse and links to the story. |
| «bærekraftig», "sustainable" and "experience" in his text | «Keep my words» | His five sentences stay as written. They're the only exceptions to the banned words (DESIGN-GUIDE §9), and only on the story page. |
| Byline | «Av Carlos» | First name only, under the title. In English: "By Carlos". |
| Preview | «Yes, after the checks» | Grok uploads to minihouse-preview.canner.app once every check passes (G-8), and nowhere else. |

Carlos also approved the plan for this task, which adds **funk move 5**: his question, set large on a band of malmfuru, the old wood (DESIGN-GUIDE §2.1).

## The page in one paragraph

A page of its own, at `/historien/` and `/en/historien/`. **Words first, the house last:** the site has no pictures of the old teachers' residence and never borrows any, so the story opens in type, and the house appears only at the end, as the payoff of «Gamle materialer. Nye hjem. Et nytt liv.». **One loud moment:** Carlos's question sits on a full-bleed malmfuru band, the heartwood of the boards the story is about. Everything else stays quiet: kalk ground, tjære text, copper only for what you press. A short section on the home page, after «Gammelt tre, nytt hus», and a fifth link in the menu lead to it.

```
1280 px                                             360 px
kalk  h1 Hvordan ideen oppstod (Besley 800, h1)      kalk  h1 (h1 size)
      Av Carlos (Jost 500, small, malmfuru-mørk)           byline, lead, paragraphs
      lead + intro, «Prosjektreferanse:» link
      … «et enkelt spørsmål:»   [columns 1–8, ≤ 64ch]
malmfuru ████ «Hvorfor skal materialenes levetid     malmfuru ███ question (h2 size)
      ta slutt …?» Besley 800 h1, kalk, cols 1–10          follow-up (Jost 500, 24 px)
      «Hva om vi kunne …?» Jost 500 24 px, kalk
kalk  «Det var slik ideen om MiniHouse oppstod.»     kalk  origin, h2, paragraphs,
      h2 Fra rivningsmaterialer …   ¶ ¶ | exploded 3:2       picture under the text
      h2 Å gi gamle materialer …    ¶ ¶
      h2 Den større visjonen        ¶ ¶
      the house (hero-slope 3:2), «Konseptbilde»
      closing (lead) / MiniHouse: / Gamle materialer. / Nye hjem. / Et nytt liv.
      [Se huset] → /#bilder
tjære footer
```

## Rules for this task

1. **Carlos's words are the text.** His Norwegian in Appendix A is the master and is published as he wrote it. The English follows his English. The only changes are the five listed under [The changes to Carlos's text](#the-changes-to-carloss-text-the-complete-list). Anything else you would change goes to Carlos as a proposal in your status file.
2. **Fluent Norwegian.** His text already is. The few words the agents write (the menu label, the home section, the link labels, the meta description) follow DESIGN-GUIDE §9 and DeepSeek's quality bar. Grok reads them a second time (G-7).
3. **No new fonts, colours, sizes, shadows or radii:** tokens only (DESIGN-GUIDE §3). The site's look already is the "modern, funky, natural, copper and Norwegian woods" Carlos asked for:
   - Besley is 19th-century wood type, and Jost is a modern geometric sans.
   - Kobber is copper, malmfuru is pine heartwood, eik is oak, and tjære is pine tar.
4. **Images only from `images.json`:** `exploded` and `hero-slope`.
   - Never generate images or video. Grok has image and video tools; don't use them.
   - Never use pictures from totalbyggoganlegg.no or any other site, and never show the old building.
5. **Never write or imply that MiniHouse uses timber from Øvsttunvegen.** The story doesn't say so. Reclaimed timber stays out of the load-bearing structure (K-06).
6. **Emergency words appear only on the story page** (D11 as amended): never on the home page, in its story section or in the menu.
7. **No git.** No commit and no push. After the task, Cursor commits, with Carlos's OK.
8. **One deploy:** G-8, to `minihouse-preview` only, after the checks pass. Never `canner redeploy`, and never another slug.
9. **No new dependencies.** Nothing to install: Astro 7.4.1 and both fonts are already there.
10. **Leave every other uncommitted file alone.** The working tree holds other sessions' work (`fase1/`, `knowledge/`, `docs/`, structural scripts, `.workbuddy-ai/`).
11. **Cursor and Antigravity don't touch this task's files** until it's closed.

## Load the skills first (both agents)

Carlos asked both agents to use `/frontend-design:frontend-design` and the `/design` style.
- **`/frontend-design:frontend-design`** is a Claude Code plugin, so it doesn't exist in Grok or DeepSeek as a command. Read its file instead.
- **The `/design` style** is the DESIGN.md format from Carlos's WebDesigner plugin: a short design-system file that agents read. The promo site's copy is `web/promo/DESIGN.md`.

| # | What | Grok CLI | DeepSeek Harness |
|---|---|---|---|
| 1 | The project skill | `/minihouse-frontend-design`. Grok finds `.agents/skills/` once you trust the folder | `.agents/skills/minihouse-frontend-design/SKILL.md`, from the skill list or by path |
| 2 | **frontend-design**, which Carlos runs in Claude Code as `/frontend-design:frontend-design` | read `C:\Users\carlos\.claude\plugins\cache\claude-plugins-official\frontend-design\1.1.1\skills\frontend-design\SKILL.md` | the same file |
| 3 | **The /design style**, the DESIGN.md design system | read [web/promo/DESIGN.md](../../../web/promo/DESIGN.md) | the same file |
| 4 | The full rules | [DESIGN-GUIDE](../DESIGN-GUIDE.md) §1–§6.3, §6.16, §9–§11 | DESIGN-GUIDE §4, §6.16, §9–§11 |

**Where they differ,** DESIGN-GUIDE.md wins, then DESIGN.md, then the skill.

**WebDesigner pipeline skills you don't run:** `webdesigner-design-system` (its "Nightglass" look), `stitch-design`, `framework-selector` and `project-scaffolder`. The stack (Astro 7.4.1, plain CSS with tokens) and the look are fixed.

**What the skill asks of you on this page:**

- **Plan before code.** Write the palette, the type, the layout as ASCII and the principles. Then compare the plan with the skill's list of generated-page defaults and with DESIGN-GUIDE §10, and say what you changed and why.
- **One bold place:** the question band. Everything around it stays quiet.
- **Critique with screenshots,** then remove one accessory before you call it done.
- **Words** are plain and active, in sentence case. A button says what happens.

## Who writes what during this task

| Path | Writer |
|---|---|
| New: `web/promo/src/pages/historien.astro`, `src/pages/en/historien.astro`, `src/components/Story.astro`, `src/components/StoryTeaser.astro` and `src/styles/story.css` | Grok |
| `web/promo/src/content/schema.ts`, `web/promo/scripts/content-contract.mjs`, `src/layouts/Base.astro`, `src/content/locale-paths.ts`, `src/components/SiteHeader.astro`, `src/pages/index.astro` and `src/pages/en/index.astro`. In `src/styles/base.css`, only the header rules, and only if the fifth link needs them | Grok, in Cursor's place |
| New: `fase4/promo/status/grok.md` and `status/grok-screens/` | Grok |
| `web/promo/src/content/nb.json`, `en.json`, `fase4/promo/content/**` (including the new `copy-story.md`), `scripts/check_promo.py`, the new `fase4/promo/qa/story.md`, `qa/a11y.md`, `qa/perf.md`, `qa/reports/**` and `status/deepseek.md` | DeepSeek |
| This file, `web/promo/DESIGN.md`, `DESIGN-GUIDE.md`, `PLAN.md` and the briefs | Claude Code |
| Everything else | nobody in this task |

**The build and the preview server:** during this task, Grok runs `npm run check`, `npm run build` and `npm run preview -- --port 4322` in Cursor's place, with the system Node (`C:\Program Files\nodejs`).
- If something already listens on 4322, use it only after checking that it serves the new build (`/historien/` answers 200).
- Never stop a server you didn't start.

## The content contract

Both agents start at once from this shape:
- **Grok** adds the keys to `schema.ts` and `scripts/content-contract.mjs` (G-2).
- **DeepSeek** fills them in both JSON files (D-20).

```ts
nav: { /* …the existing keys… */ story: string };   // «Historien» / "The story"

story: {
  meta: { title: string; description: string };  // the page's <title> and meta description
  title: string;           // the h1
  byline: string;          // «Av Carlos»
  lead: string;            // his first paragraph
  intro: string[];         // the demolition and the building, before the reference
  reference: { label: string; link: string; href: string };
  noticed: string[];       // the old timber; the last item ends with a colon
  question: string;        // on the malmfuru band
  questionFollow: string;  // under it, on the band
  origin: string;          // «Det var slik ideen om MiniHouse oppstod.»
  sections: Array<{ title: string; paragraphs: string[] }>;  // exactly three
  closing: string;
  motto: string[];         // one line each
  cta: string;             // «Se huset», the same words and action as hero.gallery
  teaser: { title: string; body: string; link: string };     // the section on the home page
};
```

**Where each part of Appendix A goes:**

| Key | Norwegian | English |
|---|---|---|
| `story.meta.title` | «MiniHouse: Hvordan ideen oppstod» | "MiniHouse: How the idea started" |
| `story.meta.description` | DeepSeek, at most 155 characters, from the story | the same |
| `story.title` | «Hvordan ideen oppstod» | "How the idea started" |
| `story.byline` | «Av Carlos» | "By Carlos" |
| `story.lead` | «Jeg ønsker å se nærmere på …» | "I want to revisit a few concepts …" |
| `story.intro` (3 items) | «I 2026 var jeg med …»; «Det var en vakker, gammel bygning …» (both sentences); «Et av målene med prosjektet …» | "In 2026, I was involved …"; "It was a beautiful old building …" and "The property was being redeveloped …" as **one** item; "One of the redevelopment project's objectives …" |
| `story.reference` | label «Prosjektreferanse:», link «totalbyggoganlegg.no/ovsttunvegen», href `https://totalbyggoganlegg.no/ovsttunvegen/` | label "Project reference:", the same link and href |
| `story.noticed` (4 items) | «Arbeidet med rivingen …»; «Etter hvert som vi demonterte …» (both sentences); «Jeg syntes det var synd …»; «Denne opplevelsen fikk meg til å stille meg selv et enkelt spørsmål:» | "Working on that demolition …"; "As we dismantled the building …" (both sentences); "It seemed such a waste …"; "That experience made me ask myself a simple question:" |
| `story.question` | «Hvorfor skal materialenes levetid ta slutt bare fordi bygningen de kommer fra, blir revet?» | "Why should the life of a building's materials end when the building itself is demolished?" |
| `story.questionFollow` | «Hva om vi kunne ta vare på disse materialene …?» | "What if we could take those materials …?" |
| `story.origin` | «Det var slik ideen om MiniHouse oppstod.» | "That's where MiniHouse began." |
| `story.sections[0]` | «Fra rivningsmaterialer til beredskapsboliger» and its 4 paragraphs | "From demolition waste to emergency housing" and its 4 paragraphs |
| `story.sections[1]` | «Å gi gamle materialer et nytt formål» and its 5 paragraphs | "Giving old materials a new purpose" and its 5 paragraphs |
| `story.sections[2]` | «Den større visjonen» and its 3 paragraphs | "The bigger vision" and its 3 paragraphs |
| `story.closing` | «I stedet for å se på riving …» | "Instead of seeing demolition …" |
| `story.motto` (4 lines) | «MiniHouse:», «Gamle materialer.», «Nye hjem.», «Et nytt liv.» | "MiniHouse:", "Old materials.", "New homes.", "A second life." |
| `story.cta` | «Se huset» | "Explore the house" |
| `story.teaser` | DeepSeek: the title «Hvordan ideen oppstod», one or two sentences, and the link «Les historien» | "How the idea started", one or two sentences, "Read the story" |
| `nav.story` | «Historien» | "The story" |

### The changes to Carlos's text (the complete list)

1. **The h1:** «MiniHouse:» moves from the h1 to the page title (`story.meta.title`), because the header already says MiniHouse.
2. **English headings in sentence case** (DESIGN-GUIDE §4). For example, "From Demolition Waste to Emergency Housing" becomes "From demolition waste to emergency housing".
3. **One English paragraph from two:** "It was a beautiful old building …" and "The property was being redeveloped …" join into one item, because `check_promo.py` requires both languages to have arrays of the same length.
4. **His bold lines become the page's typography:** the question band, the closing and the motto. No `<strong>`.
5. **The bare URL becomes the link text** «totalbyggoganlegg.no/ovsttunvegen», without `https://`.

Nothing else. DeepSeek lists these five in the copy deck.

**The five kept sentences (Carlos: «Keep my words»):**

- nb «For meg handler prosjektet om å kombinere beredskap, ingeniørfag, bærekraftig bygging og sirkulærøkonomi.»
- nb «Hvis konseptet fungerer, kan MiniHouse etter hvert bli en praktisk løsning for å gi egnede rivningsmaterialer nytt liv som trygge og bærekraftige beredskapsboliger.»
- en "That experience made me ask myself a simple question:"
- en "It's about bringing together emergency preparedness, engineering, sustainable construction and the circular economy."
- en "If the concept works, MiniHouse could eventually become a practical way to transform suitable demolition materials into safe, sustainable emergency housing."

---

## Grok: code, layout, the visual review and the upload

Grok can open screenshots, so it does the visual review that Antigravity usually does. **For this task, G-6 replaces Antigravity's review in DESIGN-GUIDE §11.**

| ID | Task | Done when |
|---|---|---|
| G-1 | **Load the skills and plan.**<br>Read this file, then the four skill sources above, in order. Write the skill's design plan in `status/grok.md`:<br>• the token for each element;<br>• the type sizes;<br>• ASCII wireframes at 360 and 1280 px;<br>• the check against DESIGN-GUIDE §10 and the skill's list of defaults, naming anything generic and what you changed instead. | the plan entry is logged before any code |
| G-2 | **The content contract.** Add `nav.story` and the `story` group above to `web/promo/src/content/schema.ts` and `web/promo/scripts/content-contract.mjs`. Then write "→ DeepSeek: keys landed" in your status file. | `npm run check` fails only on keys DeepSeek hasn't filled yet, or passes |
| G-3 | **Routes and plumbing:**<br>• `src/pages/historien.astro` and `src/pages/en/historien.astro`, each a `Base` with `Story`;<br>• `Base.astro` takes optional `title` and `description` props, defaulting to `content.meta.*`, for `<title>`, the description, Open Graph and Twitter;<br>• `localePaths` maps `/historien` to `/en/historien`;<br>• `SiteHeader.astro` gets a fifth link, `nav.story`, after «Spørsmål», in the bar and in the «Meny» sheet, pointing to the page in the same language, with `aria-current="page"` on the story page. It has no `data-nav-hash`, so the hash script leaves it alone;<br>• `<StoryTeaser>` goes right after `<Materials>` on both home pages. | the language link on each story page opens its twin; `hreflang` names both |
| G-4 | **Build the page** to DESIGN-GUIDE §6.16:<br>• `Story.astro`, `StoryTeaser.astro` and `story.css`, which `Story.astro` and `StoryTeaser.astro` import;<br>• the existing `.wrap` and band classes;<br>• tokens only, and every word from `nb.json` / `en.json`;<br>• pictures through `Figure.astro` with `ratio="wide"`: `exploded` in the first section and `hero-slope` at the end. | `npm run check` and `npm run build` pass |
| G-5 | **Run every checker:** `npm run check`, `npm run build`, `python scripts/check_promo.py`, `python scripts/check_promo.py --dist web/promo/dist` (7 pages now: two homes, two stories, two privacy pages and the 404) and `python scripts/verificar_todo.py`. | all pass; the output is in your entry |
| G-6 | **Look, critique, fix.**<br>Serve the build on 4322. Take Playwright screenshots (Python, `channel='chrome'`):<br>• `/historien/` and `/en/historien/`, full page, at 360, 768, 1280 and 1920 px;<br>• the home page's story section and the header at 360, 1024 and 1280 px.<br>Look at every one:<br>• `scrollWidth - innerWidth` is 0;<br>• no one-word last line in a heading, the question or the motto;<br>• text lines stay within 64ch;<br>• the question band reads as the page's one loud moment;<br>• the fifth menu link fits at 1024 px.<br>Then the keyboard: the skip link, a logical Tab order, a visible focus ring on every link and the button, and Esc closing the «Meny» sheet. Remove one accessory and name it. | the §11 boxes are ticked in your entry, and the screenshots are in `status/grok-screens/`. If you can't open a PNG, write **BLOCKED → Claude Code** with the paths, and Claude Code reviews them |
| G-7 | **Second reader for the Norwegian.**<br>• Compare every `story.*` string in `nb.json` word for word with Carlos's text in `content/copy-story.md`. The only differences allowed are the five changes above.<br>• Read `nav.story`, `story.teaser.*`, `story.meta.*` and the link labels as a native reader would.<br>Report everything as "→ DeepSeek:" in your status file, and edit nothing in the JSON. | no unexplained difference is left |
| G-8 | **Upload to the preview** (Carlos: «Yes, after the checks»), only after G-5, G-6, G-7, D-21 and D-22 pass:<br>• `cd web/promo && npm run bundle`, then `cd .bundle && canner deploy --slug=minihouse-preview --follow`;<br>• on the live site: `/`, `/en/`, `/historien/` and `/en/historien/` answer 200 `text/html`; `curl -r 0-1 …/film/house-film.mp4` answers 206 `video/mp4`; `/.env.production` answers 404; the language link goes from each story page to its twin and back.<br>Never `canner redeploy`, never another slug, and no git. | live and checked, with the deployment id in your entry; then a HANDOVER → DeepSeek for D-23 |

## DeepSeek: words, claims and checks

DeepSeek can't see images, so it never judges screenshots, colours or layout.

| ID | Task | Done when |
|---|---|---|
| D-18 | **The copy deck,** a new `content/copy-story.md`:<br>• Carlos's Norwegian (the master) and his English, side by side, paragraph by paragraph, copied from Appendix A;<br>• the key each paragraph goes to;<br>• the claim id each paragraph traces to;<br>• the five changes, listed. | every paragraph has a claim id, or "Carlos's own view" for his first-person intentions |
| D-19 | **Claims,** in `content/claims-register.csv`:<br>• Read https://totalbyggoganlegg.no/ovsttunvegen/ and record the date you read it and what it says about the redevelopment and the reuse of materials.<br>• Add rows from K-36:<br>&nbsp;&nbsp;– his part in the 2026 demolition (his own account, 2026-11-18);<br>&nbsp;&nbsp;– the redevelopment plan;<br>&nbsp;&nbsp;– the project's reuse goal (sourced to the page where it says so, otherwise to his account);<br>&nbsp;&nbsp;– the emergency-housing purpose («intensjon», story page only, D11);<br>&nbsp;&nbsp;– the frame built for transport and crane lifting (→ K-05);<br>&nbsp;&nbsp;– checking every reclaimed material (→ K-22);<br>&nbsp;&nbsp;– the prototype as the first step (→ K-19, K-26);<br>&nbsp;&nbsp;– the five kept sentences, each recorded as Carlos's own view and followed by the reuse fact (K-06, K-22).<br>• Add «omtrent 3 × 6 meter» / "approximately 3 × 6 metres" to K-01's allowed forms.<br>• Add a never-claim note: the Øvsttunvegen timber is never stated to be MiniHouse material. | the register parses, and every sentence in the copy deck traces to a row |
| D-20 | **Fill the JSON:**<br>• `nav.story` and the whole `story` group in `nb.json` and `en.json`, from the copy deck;<br>• the byline «Av Carlos» / "By Carlos";<br>• in your own words: `story.meta.description`, `story.teaser.body` and any link label the contract leaves to you. They trace to claim rows and carry no emergency words. | `npm run check` passes after G-2, and every Carlos string matches the copy deck |
| D-21 | **`scripts/check_promo.py`:**<br>(a) **The exception:** «bærekraftig», "sustainable" and "experience" pass only inside the five kept sentences, matched verbatim, under `story.*`. The same word anywhere else still fails.<br>(b) **The D11 guard:** «beredskap», «krise», «naturkatastrof», «nødbolig», "emergency", "disaster" and "crisis" are allowed only under `story.*`, except `story.teaser`.<br>(c) **DESIGN.md parity:** every hex value in `web/promo/DESIGN.md` is a colour in `tokens.css`, and every colour in `tokens.css` appears in `DESIGN.md`.<br>(d) **The pair:** add kalk on malmfuru (4.24) to `PAIRS`, for type of 24 px and up on the story band.<br>(e) **A self-test for each of (a)–(d).** | `--selftest`, the source run and `--dist` all pass on Grok's latest build |
| D-22 | **Audit the built page,** after G-5:<br>• a claims audit of `/historien/` and `/en/historien/`, sentence by sentence, in a new `qa/story.md`;<br>• the external link answers 200, with the command recorded;<br>• `content/sitemap.md`: the routes, the menu, the home section, the content model, and the story's one external link (until now, external links were only in the footer);<br>• axe, and Lighthouse on mobile and desktop, for `/historien/` against 4322, in `qa/a11y.md` and `qa/perf.md`, with the reports in `qa/reports/`. | recorded with commands, tool versions, dates and numbers: 0 axe violations, LCP ≤ 2.5 s, CLS ≤ 0.1, or the gaps raised as "→ Grok:" |
| D-23 | **The live check,** after G-8:<br>• the status codes of the four HTML routes, the `hreflang` pairs, and `check_promo.py --dist` on `web/promo/.bundle`, recorded in `qa/story.md`;<br>• then a HANDOVER → Carlos: the page is on minihouse-preview and waits for his G4. | logged |

**If D-16 or D-17 of [task-film-v18.md](task-film-v18.md) is still open,** DeepSeek closes it before D-18.

## Order

1. **In parallel:** Grok's G-1 and G-2, and DeepSeek's D-18 and D-19.
2. **D-20** starts when G-2 has landed the keys.
3. **G-3 and G-4** run alongside D-21.
4. **G-5** needs G-4, D-20 and D-21.
5. **G-6, G-7 and D-22** run in parallel.
6. **G-8** needs G-5, G-6, G-7, D-21 and D-22 all passed.
7. **D-23** comes last, then the task closes.

**When it closes:**
- Claude Code removes the temporary ownership row from the README.
- Cursor reviews the code and commits the promo files on `web/promo-r1`, with Carlos's OK, and then picks up C-12b.
- Carlos looks at minihouse-preview and decides G4.

## Status entries

Grok creates `fase4/promo/status/grok.md`, starting with: "Only Grok writes this file. Newest entry first. Task: agents/task-story-page.md." DeepSeek keeps its own file. Both add one entry per task, newest first:

```text
### 2026-11-18 HH:MM · G-4 Build the story page · done
Files: …
Plan: the tokens, sizes and layout used (DESIGN-GUIDE §1, step 2)
Evidence: commands and their results; screenshot paths
Definition of done (DESIGN-GUIDE §11): [ ] tokens only  [ ] allowed pairs  [ ] copy from content files
  [ ] images from images.json  [ ] keyboard  [ ] reduced motion  [ ] 360/1280 screenshots looked at
  [ ] garbage list clear  [ ] one accessory removed: …
HANDOVER / BLOCKED / → Agent: …
Next: …
```

## Kickoff prompts

**Grok (Grok CLI).**
1. Open a terminal and change to the repo root: `cd C:\Users\carlos\PROYECTOS\minihouse`.
2. Start `grok`. When Grok asks, trust the folder, so it loads `AGENTS.md`, `CLAUDE.md` and the project skills.
3. Paste:

```text
You are Grok, joining the MiniHouse promo website for one task. Carlos wants his story «Hvordan ideen oppstod»
as its own page, in his own Norwegian, in the site's modern, funky and natural look: copper and Norwegian woods.
Read fase4/promo/agents/task-story-page.md: your tasks are G-1 to G-8. Then load the design skills, in this order:
1. /minihouse-frontend-design
2. C:\Users\carlos\.claude\plugins\cache\claude-plugins-official\frontend-design\1.1.1\skills\frontend-design\SKILL.md
   (the skill Carlos runs in Claude Code as /frontend-design:frontend-design)
3. web/promo/DESIGN.md (the /design style)
4. fase4/promo/DESIGN-GUIDE.md, especially §6.16 (this page), §10 and §11
Start with G-1: write your design plan in fase4/promo/status/grok.md before any code. Edit only the files the task gives you.
Never change Carlos's words, never generate images or video, never commit or push, and deploy only to
minihouse-preview in G-8, after every check passes. Log every step in fase4/promo/status/grok.md.
```

**DeepSeek (DeepSeek Harness),** started in the repo root:

```text
You are DeepSeek on the MiniHouse promo website. Carlos wants his story «Hvordan ideen oppstod» as its own page
in fluent Norwegian: his text, published as he wrote it.
Read fase4/promo/agents/task-story-page.md: your tasks are D-18 to D-23. Read fase4/promo/status/grok.md before each step.
Load the skills: .agents/skills/minihouse-frontend-design/SKILL.md, then
C:\Users\carlos\.claude\plugins\cache\claude-plugins-official\frontend-design\1.1.1\skills\frontend-design\SKILL.md
(for the few words the page needs: the menu label, the home section, link labels and the meta description),
then web/promo/DESIGN.md.
You can't see images: never judge visuals. Never rewrite Carlos's sentences; propose any change to Carlos in your status file.
If D-16 or D-17 of task-film-v18.md is still open, close it first; then start with D-18.
Don't publish, deploy, commit or push. Log every step in fase4/promo/status/deepseek.md.
```

---

## Appendix A · Carlos's texts, verbatim

Pasted by Carlos on 2026-11-18. The Norwegian is the master. Copy from here, not from memory.

### Norwegian (master)

```markdown
# MiniHouse: Hvordan ideen oppstod

Jeg ønsker å se nærmere på noen av tankene bak MiniHouse-prosjektet mitt, og først og fremst fortelle hvordan ideen oppstod.

I 2026 var jeg med på rivingen av den gamle lærerboligen til Midtun skole i Øvsttunvegen 21 i Bergen.

Det var en vakker, gammel bygning med særpreg, historie og mange minner knyttet til seg. Eiendommen skulle utvikles videre, og planen var å oppføre et nytt bygg på samme tomt, med utgangspunkt i den opprinnelige bygningens arkitektoniske uttrykk og form.

Et av målene med prosjektet var å gjenbruke så mye som mulig av de eksisterende byggematerialene.

**Prosjektreferanse:** https://totalbyggoganlegg.no/ovsttunvegen/

Arbeidet med rivingen fikk meg til å se på byggavfall på en helt annen måte.

Etter hvert som vi demonterte bygningen, la jeg stadig merke til kvaliteten på det gamle treverket. Noe av materialet hadde vært en del av bygningen i flere tiår, men var fortsatt i overraskende god stand og så ut til å kunne brukes videre.

Jeg syntes det var synd at materialer som allerede hadde tjent én generasjon, skulle kastes når de kanskje kunne komme til nytte for flere.

Denne opplevelsen fikk meg til å stille meg selv et enkelt spørsmål:

**Hvorfor skal materialenes levetid ta slutt bare fordi bygningen de kommer fra, blir revet?**

Hva om vi kunne ta vare på disse materialene og bruke dem til å skape noe helt nytt?

Det var slik ideen om MiniHouse oppstod.

## Fra rivningsmaterialer til beredskapsboliger

Ideen min er å utvikle og bygge små, prefabrikkerte beredskapsboliger på omtrent 3 × 6 meter, der vi bruker ombrukstre og andre byggematerialer som fortsatt er i god stand, så lenge det er praktisk mulig og sikkerhetsmessig forsvarlig.

Boligene skal bygges rundt en solid og nøye dimensjonert bærekonstruksjon. Den skal være konstruert for å tåle transport og gjøre det mulig å løfte og flytte hele boligen ved hjelp av en kran.

Jeg ønsker at disse boligene skal være praktiske, komfortable og holdbare, samtidig som de skal være enkle å produsere, transportere og sette opp.

De skal kunne brukes som midlertidige boliger for mennesker som er rammet av krisesituasjoner, naturkatastrofer eller andre hendelser der det oppstår et akutt behov for et trygt sted å bo.

## Å gi gamle materialer et nytt formål

MiniHouse handler ikke bare om å bygge små hus.

For meg handler prosjektet om å kombinere beredskap, ingeniørfag, bærekraftig bygging og sirkulærøkonomi.

Jeg ønsker å vise at materialer fra riveprosjekter fortsatt kan ha stor verdi, og at de ikke nødvendigvis trenger å ende opp som avfall.

Tanken er å ta vare på det som fortsatt kan brukes, kombinere det med moderne ingeniørløsninger og skape noe som får en helt ny funksjon.

Samtidig er det viktig at alle materialer som skal brukes på nytt, blir kontrollert og vurdert ut fra hva de egner seg til. Konstruksjonssikkerhet, isolasjon, fuktsikring og lang levetid skal være viktige deler av utviklingsarbeidet.

## Den større visjonen

Det langsiktige målet mitt er å utvikle et standardisert system for produksjon av transportable beredskapsboliger. Første steg blir å bygge en prototype som er grundig planlagt, dimensjonert og testet.

Hvis konseptet fungerer, kan MiniHouse etter hvert bli en praktisk løsning for å gi egnede rivningsmaterialer nytt liv som trygge og bærekraftige beredskapsboliger.

Det som startet som en tanke på en riveplass, kan kanskje utvikle seg til noe mye større.

**I stedet for å se på riving som slutten på en bygnings historie, ønsker jeg å se på det som en mulighet til å starte en ny.**

**MiniHouse: Gamle materialer. Nye hjem. Et nytt liv.**
```

### English

```markdown
# MiniHouse: How the Idea Started

I want to revisit a few concepts behind my MiniHouse project, starting with how the idea came to life.

In 2026, I was involved in the demolition of the old Midtun School Teachers' Residence at Øvsttunvegen 21 in Bergen, Norway.

It was a beautiful old building with character, history and memories attached to it.

The property was being redeveloped, with a new building planned for the site that would preserve the architectural character and form of the original.

One of the redevelopment project's objectives was to reuse as much of the existing building material as possible.

Project reference: https://totalbyggoganlegg.no/ovsttunvegen/

Working on that demolition made me look at construction waste differently.

As we dismantled the building, I kept noticing the quality of the old timber. Some pieces had been there for decades, yet they still looked remarkably good and potentially useful.

It seemed such a waste to throw away materials that had already served one generation and could potentially serve another.

That experience made me ask myself a simple question:

**Why should the life of a building's materials end when the building itself is demolished?**

What if we could take those materials and create something entirely new?

That's where MiniHouse began.

## From Demolition Waste to Emergency Housing

My idea is to design and build small, prefabricated emergency homes, approximately 3 × 6 metres, using reclaimed timber and other reusable construction materials wherever practical and safe.

The houses would be built around a properly engineered structural frame, designed to make them strong enough for transportation and suitable for lifting and relocation by crane.

I want these homes to be practical, comfortable and durable, but also easy to manufacture, transport and deploy.

They could provide temporary accommodation for people affected by emergencies, natural disasters or other situations where safe housing is urgently needed.

## Giving Old Materials a New Purpose

MiniHouse is not simply about building tiny homes.

It's about bringing together emergency preparedness, engineering, sustainable construction and the circular economy.

I want to show that materials recovered from demolition sites can become valuable resources rather than automatically ending up as waste.

The idea is to preserve what is still useful, combine it with modern engineering and create something that serves a completely new purpose.

Of course, every reclaimed material would need to be assessed for its suitability. Structural safety, insulation, moisture protection and long-term durability would remain essential parts of the design.

## The Bigger Vision

My long-term goal is to develop a repeatable system for manufacturing transportable emergency homes, starting with one properly engineered prototype.

If the concept works, MiniHouse could eventually become a practical way to transform suitable demolition materials into safe, sustainable emergency housing.

What began as a thought on a demolition site could become something much bigger.

**Instead of seeing demolition as the end of a building's story, I want to see it as an opportunity to begin another.**

**MiniHouse: Old materials. New homes. A second life.**
```
