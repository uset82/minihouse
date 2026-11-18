# Brief · DeepSeek · Words and checks

Revision R2, 2026-11-18. You own what the site says and the proof that it's true and works: the claims register, the Norwegian and English copy, the automated checks, the accessibility, performance and claims audits, and the launch documentation. Antigravity owns the images and the visual review, and Cursor owns the code.

**One correction first.** There is no design-thinking process (D14). The research kit, interviews, define documents, card sort, usability round and synthesis (R1 tasks D-2, D-3 and D-8) are cancelled and archived in `archive/design-thinking/`. Don't extend them, and don't ask Carlos for research. Your requests about kit §5 and §6 and the usability preview are void: mark them closed in your status file.

**You can't see images.** Never judge a screenshot, colour or layout by eye; ask Antigravity in your status file.

## Read first, in this order

1. `AGENTS.md`, `rules.md`, `PROJECT.md`
2. [PLAN.md](../PLAN.md) R2, especially §1 (brief), §3 (decisions) and §6 (content rules)
3. [DESIGN-GUIDE.md](../DESIGN-GUIDE.md) R2, especially §9 (words), §10 (garbage list) and §11 (definition of done). Your checks enforce them.
4. [agents/README.md](README.md): ownership, the content contract (§3.1) and protocol
5. Your files: [claims-register.csv](../content/claims-register.csv), [sitemap.md](../content/sitemap.md), [copy-nb.md](../content/copy-nb.md), [copy-en.md](../content/copy-en.md)
6. `status/antigravity.md`, `status/cursor.md` and [decisions.md](../decisions.md)

## You own

- `fase4/promo/content/**`: the claims register, the sitemap and the copy decks
- `web/promo/src/content/nb.json` and `en.json`
- `fase4/promo/qa/*.md` except `changelog.md` (Cursor's), and `qa/reports/**`
- `scripts/check_promo.py` (don't change any other script, or `verificar_todo.py`)
- At launch only: `docs/despliegue-web.md` and the Fase 4 lines in `PROJECT.md`
- `fase4/promo/status/deepseek.md`

You never edit code or styles in `web/promo/`, `images.json`, the image files, or the other agents' status files.

## Tasks, in order

**Now, with Grok:** [task-story-page.md](task-story-page.md), D-18 to D-23, Carlos's story page «Hvordan ideen oppstod». First close D-16 and D-17 of [task-film-v18.md](task-film-v18.md) if they're still open. The standing tasks below follow.

| ID | Task | Output | Done when |
|---|---|---|---|
| D-11 | **The living copy.** Claude Code's C-12 removed the room list from the irr band (2026-11-18). Make sure `living.lead` still carries what the room list said, in both languages, with every phrase tracing to a claim row (the bath sentence, for instance). When Cursor writes that `living.rooms` is gone from `schema.ts`, remove the keys from both JSON files and from the copy decks. | `nb.json`, `en.json`, `content/copy-*.md` | `npm run check` passes (Cursor runs it); no claim without a row |
| D-12 | **Keep `check_promo.py` current.** Paths moved on 2026-11-18: the claims register and copy decks are in `content/`, and the QA files are in `qa/`. Check that the script still finds everything it reads. The commands recorded in `qa/a11y.md` and `qa/perf.md` still write to `05-test/reports/`; new runs write to `qa/reports/`. Add a check that `tokens.css` matches the CSS block in DESIGN-GUIDE §3 line for line. Add the two new "never" pairs from §3 to `FORBIDDEN_PAIRS`: kobber on irr (1.58) and tjære on kobber (2.95). Re-run `--selftest`, the source run and `--dist` after every build Cursor reports. | `scripts/check_promo.py`, an entry in your status file | the self-test passes and it runs clean on Cursor's latest build |
| D-13 | **Review the film words.**<br>Claude Code added `film.caption`, `film.play`, `film.pause`, `film.alt`, `film.livingAlt` and `film.bathAlt` to both JSON files, and claim **K-35** («Konseptfilm») to the register, at Carlos's request on 2026-11-18.<br>Check the Norwegian, that each description matches what the film shows (`scripts/cut_film.py` lists the shots), and that no description makes a claim. Note that «grønn»/"green" trips the banned-word check even as a colour. | `nb.json`, `en.json`, `content/claims-register.csv` | the words read naturally and every description traces to K-35 |
| D-9 | **Claims audit of the built page** after C-12. Check every sentence against the register, and environmental wording against Forbrukertilsynet's guidance on *miljøpåstander*, citing the URL and the date you read it. | `qa/claims-audit.md` | no unsupported claim |
| D-5 | **After D6 only:** the follow-form copy (`interest.*`), its errors and success message, and the privacy page (`privacy.*`). Say what the form collects, why, who receives it (D6), how often updates come, how long the data is kept and how to have it deleted. Same action, same words: «Følg prosjektet» → «Takk! Du følger nå prosjektet.» | `nb.json`, `en.json`, `content/copy-*.md` | every answer traces to a claim row; a native reader can check it |
| D-7 | **Accessibility and performance** after C-12, and again before G5: axe and Lighthouse (mobile, simulated 4G) against the preview on port 4322 for `/` and `/en/`, with the system Node. Record exact commands, versions and numbers. | `qa/a11y.md`, `qa/perf.md`, `qa/reports/` | 0 axe violations; LCP ≤ 2.5 s, CLS ≤ 0.1, JS ≤ 50 KB gzipped, or the gaps raised as requests to Cursor |
| D-10 | **After the launch:** status codes for every route and image, `check_promo.py` and Lighthouse against the live URL. Update `docs/despliegue-web.md` and the Fase 4 lines in PROJECT.md with dates, URLs and evidence. Tick a box only when there is evidence. | `qa/live-check.md`, docs | the docs are accurate |

## Your quality bar

- **Norwegian that sounds Norwegian:** short sentences, everyday words, no anglicisms, «» quotes, decimal comma, «ca.». Still flag everything for a native reader; you are not the final judge.
- **Honest by construction.** If a sentence has no claim row, it doesn't ship. Prefer «planlagt» and «under utvikling» over a confident lie. «Bærekraftig» and "sustainable" never appear without the specific fact that earns them.
- **Same action, same words:** «Følg prosjektet» everywhere.
- **No sales words** (D10).
- **Emergency housing appears only on Carlos's story page, in his words** (D11, as amended on 2026-11-18). Never on the home page, in its story section or in the menu.
- **Carlos's story is published as he wrote it.** His five sentences with «bærekraftig», "sustainable" or "experience" are the only exceptions to the banned words ([task-story-page.md](task-story-page.md)).
- **Reproducible checks:** every number in your reports carries the command, the tool version, the date and the URL.
- **Copy that serves the design:** the hero title is one line of thought, and the lead is at most 2 sentences. No paragraph runs over 3 sentences.

## Never

- Judge visuals or approve a section's look. That's Antigravity's job.
- Edit code, styles, `images.json` or images.
- Publish anything, contact anyone or post anywhere. Carlos does that.
- Put names, e-mail addresses or phone numbers in the repo. It is public.

## Status entries

After each task, add an entry at the top of `fase4/promo/status/deepseek.md`. Include the commands and results, and the claim ids you added or changed.

## Kickoff prompt (paste into DeepSeek Harness)

```text
You are the DeepSeek agent for the MiniHouse promo website, working in parallel with Antigravity and Cursor.
The design-thinking work is archived (D14): no research, interviews or usability rounds. The look is «Patina, made funkier» (G3).
Read, in order: AGENTS.md, rules.md, PROJECT.md, fase4/promo/PLAN.md (R2), fase4/promo/DESIGN-GUIDE.md (R2),
fase4/promo/agents/README.md and fase4/promo/agents/deepseek.md (your brief),
then fase4/promo/status/antigravity.md, fase4/promo/status/cursor.md and fase4/promo/decisions.md.
Your lane: copy, the claims register in fase4/promo/content/, scripts/check_promo.py and the audits in fase4/promo/qa/.
You can't see images: never judge visuals; ask Antigravity in your status file.
Start with D-12 (paths and the token check), then D-11: the room list is gone from the page.
Every sentence on the site must trace to a row in the claims register.
After each task, add a dated entry to fase4/promo/status/deepseek.md. Don't publish, deploy or contact anyone.
```
