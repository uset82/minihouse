# Status · DeepSeek

Only DeepSeek writes this file; the other agents and Carlos read it. Put the newest entry at the top of the log. Brief: [agents/deepseek.md](../agents/deepseek.md). Protocol: [agents/README.md §5](../agents/README.md).

## Requests to other agents

Open requests go here, one line each, for example "→ Antigravity: …". Mark them done when they're answered.

- → Carlos: D6 will determine the recipient and service for the future subscription. The current preview and privacy routes are working. K-29 stays open if contact details are to be added later.
- → Carlos: the 15–20 reference images for the taste question (kit §1.5) and the photos of the real boards (including end grain) — those are the strongest proof for the material passport.
- → Antigravity: the 5-second test and the preference test scripts for the G3 pack are in [kit.md §5](../archive/design-thinking/01-empathize/kit.md). Use them verbatim so the results stay comparable across the three directions.
- → Cursor: for the usability round ([kit.md §6](../archive/design-thinking/01-empathize/kit.md)), start the preview with `npm run preview -- --port 4322 --host` and tell me the LAN address it prints, so Carlos's phone can open it on the same Wi-Fi. A preview deploy only if Carlos approves it.
- → Cursor: `nb.json` and `en.json` are filled and the contract check passes. Please run `npm run check` and `npm run build`, then `python scripts/check_promo.py --dist web/promo/dist`. The only expected failures are the 19 image alt texts Antigravity still owes.
- → Cursor: D-7 findings, all in `web/promo/**` (yours): (1) the five figcaptions on the irr band are 1.04:1 — set captions inside `.band--irr` to `--kalk` per DESIGN-GUIDE §6.8; (2) `favicon.ico` 404s; (3) `/personvern/` and `/en/personvern/` do not resolve; (4) the EN page fails Lighthouse's `hreflang` audit. After the fix, rebuild and tell me, and I re-run axe and Lighthouse.
- → Cursor and Carlos: closed for this preview. D13 uses the gallery action. D1 applies to the future subscription once D6 is resolved. Both privacy routes describe the current browsing experience.
- → Carlos (or Cursor): run a Patentstyret search for «MiniHouse» before G5 and record the result in `05-test/claims-audit.md` §5; the Brønnøysund check returned 0 hits.
- → Cursor: the follow-form schema change is closed on both sides — `schema.ts` holds only `fields { email, name, optional }` and both JSON files match (2026-11-17 22:26). No action.
- → WorkBuddy: when W-2 lands, name the four output sizes and whether any budget needed a CRF raise; in W-3, say explicitly whether any of the five shots changed content from v11 to v18, since that decides whether I rewrite `film.alt`, `film.livingAlt` or `film.bathAlt`. Details in `qa/film-v18.md` §5.
- → Grok: the G-8 upload is missing the two story routes. `web/promo/.bundle` has no `historien/` and `check_promo.py --dist web/promo/.bundle` counts 5 pages, so the preview answers 404 for `/historien/` and `/en/historien/`. Run `cd web/promo && npm run bundle` from the current build and redeploy to `minihouse-preview`; tell me the deployment id and I re-run D-23. Also: `hreflang` points at `minihouse.canner.app` from the preview — decide with Carlos whether that is intended.
- → Antigravity: `scripts/check_promo.py` is the gate for image alt/caption text and for `--release`; when the 19 entries have their alts in both languages, the release check has one class of failure left (no image may be `stand-in` or `pending`).
- → Cursor: the claims register is live at [02-define/claims-register.csv](../content/claims-register.csv). `schema.ts` may need one key I expect to use: a per-image `alt`/`caption` pair already exists, so no change is requested yet. If the copy needs a claims note in the UI, I'll ask before touching `nb.json`.

## Log

### 2026-11-18 23:54 · D-23 live check · BLOCKED: the preview does not carry the story pages
Files: `fase4/promo/qa/story.md` (§6 the live check, §7 what remains).
Plan (DESIGN-GUIDE §1, step 2): no UI. Check the live preview exactly as D-23 asks, and report what answers.
Evidence:
- **Routes:** `/` **200**, `/en/` **200**, `/historien/` **404**, `/en/historien/` **404**. The 404s are real, not a routing quirk: `web/promo/.bundle` has no `historien/` or `en/historien/`, and `check_promo.py --dist web/promo/.bundle` counts **5 pages**, not 7. The bundle on disk is the **pre-story build**, so G-8 did not upload the story pages even though the local `dist` has them.
- **`hreflang`:** the pages that answer carry the landing pairs (`nb → minihouse.canner.app/`, `en → /en/`, `x-default → /`), pointing at the **production** host. The correct story pairs exist only in the local build (`/historien/` ↔ `/en/historien/`). Two findings: the bundle must be rebuilt and redeployed, and the absolute host should either be relative or made configurable per deployment.
- **What passes:** the build (`--dist web/promo/dist`, 7 pages), axe (0 violations on both story pages), Lighthouse (100s, LCP 0.8 s phone / 0.2 s desktop, CLS 0) and the claims audit. The page is ready in `dist`; it is not on the preview.
- I did not deploy: G-8 belongs to Grok, and a deploy I ran would hide whose build is live.
Checks: 4 `curl` status codes, `hreflang` extraction on 4 pages, `check_promo.py --dist web/promo/.bundle` (5 pages).
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
**HANDOVER → Carlos:** the story page is **not** on minihouse-preview yet, so G4 has nothing to look at there. Grok needs one more `npm run bundle` and a deploy to `minihouse-preview`; when `/historien/` and `/en/historien/` answer 200, I re-run D-23 and hand over again. The page itself is finished in the build (claims audit, axe and Lighthouse all pass).
→ Grok: rebuild `.bundle` from the current `dist` and redeploy; the bundle you uploaded predates the story pages. Also decide the absolute-host question with Carlos.
Next: D-23b after the corrected upload — four status codes, `hreflang` pairs on the story pages, `--dist .bundle` expecting 7 pages.

### 2026-11-18 23:48 · D-21 closed, D-22 done · done
Files: `scripts/check_promo.py` (D-21, closed by the new build), `fase4/promo/qa/story.md` (new), `qa/a11y.md`, `qa/perf.md`, `qa/reports/axe-story.{txt,json}`, `qa/reports/lighthouse-story-page-{mobile,desktop}.json`, `fase4/promo/content/sitemap.md`.
Plan (DESIGN-GUIDE §1, step 2): no UI. Verify the built story pages with the tools I can run, and audit every rendered sentence against the register.
Evidence:
- **D-21 closed:** `check_promo.py --dist web/promo/dist` → **7 pages, all checks passed**, with 12 contrast pairs, DESIGN.md parity 10/10 and the five kept sentences green.
- **D-22 claims audit:** every block on both story pages traces to K-01, K-06, K-19, K-20, K-36…K-44 or is «Carlos's own view»; table in `qa/story.md` §1. The page repeats nothing the register does not carry, and it never implies the Øvsttunvegen timber is MiniHouse material (K-37).
- **External link:** `curl … https://totalbyggoganlegg.no/ovsttunvegen/` → **200 text/html** (2026-11-18 23:30); the rendered tag is the same URL in the same tab.
- **axe:** **0 violations** on `/historien/` and `/en/historien/`, axe-core 4.14.1, raw files in `qa/reports/`.
- **Lighthouse:** performance/accessibility/best-practices/SEO **100/100/100/100** on both form factors; LCP **0.8 s** phone and **0.2 s** desktop; CLS **0**; TBT 0; JS 0 bytes; 74 KB and 131 KB. All D-22 gates pass.
- **Sitemap updated:** the two story routes, the fifth menu link, the home teaser, the `story.*` content group and the story's one external link are recorded.
- What I did not do: judge the layout, the band or the crops (Grok's G-6 and Carlos's G4), build, deploy or touch git.
Checks: `check_promo.py --dist` (7 pages), axe (2 pages), Lighthouse (2 runs), curl (1 link), all recorded with versions and dates.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard (Grok's G-6)  [N/A] reduced motion  [N/A] 360/1280 screenshots (Grok's; I did not look)  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: → Grok: D-21 and D-22 pass on your build; G-8 can upload once G-6 and G-7 are done. → Carlos: the story page is ready for his eyes at G4 after the preview upload.
Next: D-23 after G-8 — the four HTML routes, the `hreflang` pairs and `check_promo.py --dist web/promo/.bundle` on the live preview.

### 2026-11-18 23:36 · D-21 checker: exception, D11 guard, DESIGN.md parity, pair · done pending the story build
Files: `scripts/check_promo.py` only.
Plan (DESIGN-GUIDE §1, step 2): no UI. The five kept sentences must pass **and nothing else**; the guard must keep emergency words off the home page; DESIGN.md and tokens.css must not drift.
Evidence:
- **(a) The exception.** `story_hits()` allows «bærekraftig», "sustainable" and "experience" only when the string sits under `story.*` **and** equals one of the five kept sentences verbatim (apostrophes normalised). The source run went from 5 problems to **all checks passed**, and the five that turned green are exactly the five that were red.
- **(b) The D11 guard.** «beredskap», «krise», «naturkatastrof», «nødbolig», "emergency", "disaster" and "crisis" are allowed under `story.*` only, never in `story.teaser`; anywhere else they fail. The teaser text I wrote carries none.
- **(c) DESIGN.md parity.** New `check_design_parity()` compares every hex in `web/promo/DESIGN.md` with the colour variables in `tokens.css`, both directions: **10 and 10, no difference**.
- **(d) The pair.** kalk on malmfuru (4.24, the story band, 24 px and up) is now an explicit entry, so the bands' only text pair is covered even though the ratio is symmetric with the existing numerals pair. 12 pairs recomputed.
- **(e) Self-tests.** 14 new assertions, **47 in total, all pass**: kept sentence passes under story, the same words fail outside it, a non-kept story paragraph fails, the curly-apostrophe variant still matches, an emergency word passes under story and fails in the teaser and on the home page, parity catches an extra colour on either side, and the 4.24 pair is both listed and recomputed.
- **`--dist` on the current build passes** (5 pages), but that build predates the story page: Grok has not run G-5 yet, so the two story pages are not in `web/promo/dist`. D-21's last clause ("--dist passes on Grok's latest build") waits for that build, and I re-run it the moment it exists.
Checks: `check_promo.py --selftest` (47/47), source run (all pass), `--dist` on the current build (all pass).
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots (Grok's)  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: → Grok: the checker now lets the five kept sentences through and blocks the words everywhere else. G-5 can run; when the build exists I run `--dist` and then D-22.
Next: D-22 after G-5 — claims audit of both story pages, the external link check, `content/sitemap.md`, axe and Lighthouse.

### 2026-11-18 23:28 · D-18 copy deck, D-19 claims, D-20 JSON · done
Files: `fase4/promo/content/copy-story.md` (new); `fase4/promo/content/claims-register.csv` (K-36…K-44, K-01 expanded); `web/promo/src/content/nb.json` and `en.json` (`nav.story` + the whole `story` group). No other code touched.
Plan (DESIGN-GUIDE §1, step 2): no UI. Carlos's Norwegian is the master; the deck copies it, the register proves it, the JSON carries it.
Evidence:
- **D-18:** the deck holds his Norwegian and English side by side per key with the claim for each paragraph, the five changes and the five kept sentences. A script compared all **34** of his strings in the deck against Appendix A: **all verbatim**, zero differences.
- **D-19:** read https://totalbyggoganlegg.no/ovsttunvegen/ on 2026-11-18. It confirms the 2026 demolition by Totalentreprenør AS (roof and upper floor by crowbar), **43 tonnes** of good-quality materials preserved, **52 % reuse**, and **46 tonnes** of natural stone; the permit was conditioned on rebuilding in approximately identical form and style. Added **K-36…K-44**: his part in the demolition, the building and the figures (verified but not published, because his text has none), the redevelopment plan, the reuse goal, the emergency-housing purpose (`intensjon`, story page only), the transport-and-crane frame (→ K-05), the material checks (→ K-22), the prototype first (→ K-19/K-26), and his five kept sentences as his own view. **K-01** now also allows «omtrent 3 × 6 meter» / "approximately 3 × 6 metres". **Never-claim note recorded:** the Øvsttunvegen timber is never stated or implied to be MiniHouse material. 44 rows, unique ids, legal statuses.
- **D-20:** `nav.story` («Historien» / "The story") and the full `story` group are in both files, from the deck. `node scripts/check-content.mjs` → **content check passed**.
- **D-21 is the next step and its failures are known by design:** `check_promo.py` now reports exactly five, all the kept sentences — «bærekraftig» ×2 (nb), "sustainable" ×2 and "experience" ×1 (en). The exception rule in D-21(a) is what turns them green, under `story.*` only.
- I did not touch `Story.astro`, `story.css`, the pages or any Grok file; no build, no screenshots, no deploy, no git.
Checks: `check-content.mjs` passes; `check_promo.py` source run is at the five expected story exceptions.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots (Grok's; I did not look)  [x] garbage list clear (my words; his are his)  [N/A] one accessory removed
HANDOVER: → Grok: the JSON is filled and the content check passes; `npm run check` and `npm run build` can run now. G-7's comparison should use `content/copy-story.md`, where every string is already verified against Appendix A.
→ Carlos (proposals, not edits, in `copy-story.md` §5): his English «tiny homes» and his «experience» are kept as written; the reference link opens in the same tab unless Grok decides otherwise.
Next: D-21 (checker exceptions, D11 guard, DESIGN.md parity, selftest), then D-22 once Grok builds.

### 2026-11-18 23:08 · D-15, D-16, D-17 closed · done
Files: `fase4/promo/qa/film-v18.md` (§4 now holds D-15–D-17), `fase4/promo/qa/perf.md` (film section), `qa/reports/lighthouse-story-{mobile,desktop}.json`. No JSON, cut or master touched.
Plan (DESIGN-GUIDE §1, step 2): no UI. WorkBuddy's W-7 closed the last visual question, so the three film tasks could finish without guessing.
Evidence:
- **D-15 closed by W-7:** no shot changed from v11 to v18, both crops keep their subject, and the CRF-33/32 files show no banding at full size. So `film.alt`, `film.livingAlt` and `film.bathAlt` stand, and K-35 already cites the 4K master.
- **D-16:** Lighthouse 13.6.0, phone (412) and desktop (1350) against 4322. Performance 100 both; LCP **1.7 s / 0.4 s**; CLS 0 / 0.009; largest paint is the **poster `img.film-still`** in both; every film request starts **after** `load` (746 vs 712 ms; 486 vs 391 ms). Film bytes: **2.29 MB** phone (720p), **5.84 MB** desktop (1080p hero 3.76 + both loops). The hero file is inside its 4.5 MB budget; the desktop total is larger only because the two loops enter the load window.
- **D-17:** live check of https://minihouse-preview.canner.app — `/` and `/en/` 200 `text/html`; all four films **206 `video/mp4`** with a 2-byte range; `/.env.production`, `/package.json`, `/serve.mjs` **404**; `check_promo.py --dist web/promo/.bundle` **all checks passed** (5 pages, one `h1` each, correct `lang`).
- I did not deploy, commit or push; the preview WorkBuddy deployed (`78aaecbf`) is the one checked.
Checks: two Lighthouse runs and five `curl` checks, all recorded with commands and versions in the QA files.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots (Grok/WorkBuddy looked; I did not)  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: task-film-v18 is closed on my side. → Cursor: W-7's note that commit `232573e` already carried my D-14 work; nothing of mine is uncommitted except the QA/perf and status edits.
Next: task-story-page D-18 (copy deck), then D-19 (claims).

### 2026-11-18 20:58 · D-14 closed, D-15 source updated · done / in progress
Files: `fase4/promo/qa/film-v18.md` (D-14 final), `fase4/promo/content/claims-register.csv` (K-35 source). The alt keys are untouched.
Plan (DESIGN-GUIDE §1, step 2): no UI. WorkBuddy's W-2 entry confirms the cuts, so D-14 is final; the K-35 source line moves now because it depends on the master, not on a visual judgement.
Evidence:
- **D-14 done.** Their sizes in decimal MB (3.94 / 2.40 / 1.04 / 1.14) match my binary measurements, and their ffprobe agrees on video-only H.264 at 24 fps with `moov` before `mdat`. They raised CRF to 33 for the 1920 hero and 32 for the living loop to stay inside budget, which is a quality trade-off rather than a defect; I asked W-3 to look for banding in the sky, the cladding and the copper mirror, since that is the one thing my tools cannot see.
- **D-15, source half.** K-35 now cites `images/minihouse_walkthrough_v18_4k.mp4` (3840 × 2160, 408 frames, 17.041 s) and names the four cuts with their sizes, plus the v11 archive. The caption wording «Konseptfilm» is unchanged because the film is still a rendered concept, not a recording.
- **Alt texts deliberately untouched.** `film.alt`, `film.livingAlt` and `film.bathAlt` stay as they are until W-3 says whether a shot changed; I do not judge pictures.
- Checks: `check_promo.py` passes (source mode), `check-content.mjs` passes. No master, cut, poster, `films.json`, `films.ts`, `Film.astro` or `film.ts` touched.
Checks: as above; all read-only except the register and the two QA/status documents.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER / BLOCKED: D-15 finishes when W-3 reports; D-16 waits for W-5 and the 4322 preview; D-17 waits for W-6 and the preview URL.
Next: D-15 on W-3's answer, then D-16.

### 2026-11-18 20:52 · D-14 measured on the four cuts (preliminary) · done pending W-2 entry
Files: `fase4/promo/qa/film-v18.md` (updated §2). No cut, master or JSON touched.
Plan (DESIGN-GUIDE §1, step 2): no UI. The four outputs appeared complete at 20:42–20:43, so they were measured now; a W-2 re-encode only costs a re-run of the same commands.
Evidence:
- **All four cuts probed:** `house-film-1920.mp4` 1920 × 1080, 397 frames, 16.542 s, **3.76 MiB** (budget 4.5); `house-film.mp4` 1280 × 720, 397 frames, 16.542 s, **2.29 MiB** (2.5); `living-loop.mp4` 1440 × 960 (3:2), 136 frames, 5.667 s, **0.99 MiB** (1.2); `bath-loop.mp4` 1080 × 1350 (4:5), 168 frames, 7.000 s, **1.08 MiB** (1.3). All H.264 High, 24/1 fps, every size inside its budget.
- **No audio in any cut.** The master carries an AAC track, so this was the check most likely to fail; it passes on all four.
- **Fast start on all four:** top-level order is `ftyp`, `moov`, `free`, `mdat` in every file. Checked by reading top-level boxes, not by re-encoding.
- **The 16.542 s hero is correct, not a truncation:** the master is 17.041 s and the loop seam trims about half a second, the same way the v11 cut ended at 16.5 s.
- Status in `workbuddy.md` still shows only W-1, so this is labelled preliminary until their W-2 entry lands.
Checks: ffprobe 8.0.1 and a stdlib box reader; all read-only.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER / BLOCKED: D-14 has no technical finding to report. The only open questions are visual and belong to W-3: crop subjects and any shot change. **D-15 waits for W-3**, D-16 for W-5, D-17 for W-6.
Next: D-15 once WorkBuddy reports W-3.

### 2026-11-18 20:45 · D-14 prepared: master measured, cuts pending W-2 · in progress
Files: `fase4/promo/qa/film-v18.md` (new, partial). No cut, no master, no JSON touched.
Plan (DESIGN-GUIDE §1, step 2): no UI. Read `agents/task-film-v18.md` and `status/workbuddy.md` first, then measure what already exists without waiting on anything WorkBuddy has not finished.
Evidence:
- **Master probed** with ffprobe 8.0.1: 3840 × 2160, H.264 High, yuv420p, 24/1 fps, 408 frames, **17.041016 s**, 138 380 521 B, and an AAC stereo track at 48 kHz. Every number matches the task's table, so the master is the one Carlos described.
- **The audio stream matters:** the master has sound, the site's films must be silent (DESIGN-GUIDE §6.15), so D-14 will fail any cut that keeps an audio track. Recorded in the QA file as a check, not an assumption.
- **Fast-start method tested** before it was needed: a top-level box read puts `moov` before `mdat` on the archived v11 cut and on the new 1920 cut. No decoder needed, so the check is cheap for all four outputs.
- **W-2 is mid-flight:** `house-film-1920.mp4` exists at 3 943 047 B (within the 4.5 MB budget), `house-film.mp4` was 48 bytes at 20:42 (ffmpeg still writing), and the two loops are still the old v11 files. WorkBuddy's status still shows only W-1, so **I did not start D-14 proper**: measuring a half-written file would record garbage. The QA file says exactly that.
- Did not touch `films.json`, `films.ts`, `Film.astro`, `film.ts` or the cuts — WorkBuddy owns them during this task.
Checks: ffprobe and the atom scan are read-only; `qa/film-v18.md` records the commands so the run is repeatable.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER / BLOCKED: **waiting for WorkBuddy's W-2 entry.** Then D-14 runs on the four finished cuts in one pass, and W-3's answer decides whether D-15 touches the alt texts.
Next: D-14 on the finished cuts; then D-15 after W-3.

### 2026-11-18 00:20 · Carlos's Drive folder checked against the local media · done
Files: `fase4/promo/05-test/asset-check.md` (new). Nothing committed to git; no media added to the repo.
Plan (DESIGN-GUIDE §1, step 2): no UI. Carlos shared the media folder, so I verified it instead of assuming it was new material.
Evidence:
- **All 16 entries downloaded and hashed** (15 PNG + the walkthrough MP4). Every SHA-256 matches the file already in `images/` on this PC: **16 identical, 0 missing, 0 different**. The folder is the same set, not a new render round.
- **They are too small for the plan's own bar.** The largest width is **1536 px**; the hero needs **2400** and section images **1600** (PLAN §2.4, DESIGN-GUIDE §7). The four bathroom renders are 1122 × 1402, exactly the "fine for gallery tiles, soft in a full-screen lightbox" note already in `bildeliste.csv`.
- **The shot list still stands:** only the four `bath-*` ids exist; the other 15 ids (hero, meadow, exploded, living, kitchen, bench, storage, three journey shots, four textures, og-image) are to produce at size. D5's render round is still the unblocker.
- **Video:** 31.3 MB, and nothing in the plan puts video on the page. Asked Carlos to confirm whether it is meant to be used.
- I did not judge any picture: bytes and pixels only. Fidelity, gallery choice and crops remain Antigravity's review with Carlos.
Checks: downloads verified by magic bytes and hash; temp files removed; nothing staged (working tree clean apart from the new doc).
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: → Carlos: the folder is the reference set, not the production set; the hero and section renders still need to be made at ≥ 2400 / ≥ 1600 px. → Antigravity: references are in `images/` and at the Drive link; `asset-check.md` lists the pixels.
Next: the D-9 built-page re-run after Cursor's rebuild; the render round is the long pole.

### 2026-11-17 23:41 · Workshop-to-plot review

Antigravity confirmed that the enlarged workshop illustration still depicts the fabrication hall, the second image the truck and the third the house at rest. Updated the three descriptions in the two languages and their copy decks. K-05 identifies transport as an intention, and K-27 supports checking the route first.

Checked the new local static build from 23:39:29. Both homepages served the matching workshop image and all six final descriptions. Both homepages and both privacy pages returned HTTP 200 and contained zero forms or links to a subscription. The [axe run](../qa/reports/axe-landing.txt) found zero automated violations on either landing page.

The built-page link checker now looks for real identifiers or named anchors in the destination HTML page. A missing in-page target and a missing cross-page target both fail the fixture. Existing fragments, URL-encoded Norwegian text, named anchors and ordinary links pass. All 36 self-tests and all five built pages passed.


### 2026-11-17 23:58 · D-9 re-audit, copy batch applied, D-7 corroborated · done
Files: `05-test/claims-audit.md` (rewritten to v1); `web/promo/src/content/nb.json`, `en.json` (kitchen, bench, storage); `02-define/claims-register.csv` (K-34, renumbered after a duplicate)
Plan (DESIGN-GUIDE §1, step 2): no UI. Correct my own first pass against the rendered page, finish the copy batch, and check the fresh build with both tools.
Evidence:
- **I corrected a finding rather than defending it.** The 23:29 build has **no form, no inputs and no «Følg prosjektet» button**: the D13 landing does not mount `interest.*` or `nav.cta`. So the privacy sentence is true of the page today, and the contradiction I reported is **latent** — it becomes real only when the follow form is mounted. That is now a decision for Carlos (form and D-5 privacy text, or no form and park the dead keys), not a copy defect. `claims-audit.md` §1 says so plainly.
- **Copy batch:** the kitchen, bench and storage details were still unsupported and are now softened in both languages; the bathroom tiles, the steel-frame sentence and both metadata items were fixed by the team in parallel within the same minutes. The files are consistent, and `check-content.mjs` and `check_promo.py` both pass.
- **D-7 re-run confirms the team's reports:** axe-core 4.14.1 gives **0 violations on both pages**; my Lighthouse run on the same build gave performance **0.99**, LCP **2.3 s**, CLS **0**, TBT **0 ms**, JS **0 bytes**, and accessibility / best-practices / SEO **100**. Their reports (`lighthouse-landing-*.json`, run 23:27–23:28) say 1.38 s and 1.83 s LCP; both are inside the 2.5 s gate, and the spread is normal run variance. The reports in `05-test/` are theirs now, with my baseline kept below.
- **Register:** 34 unique rows. The team's **K-33** (pine-heartwood tradition, Treteknisk + Riksantikvaren) stands; my canonical-facade row is **K-34**. I have not fetched their two sources — G4 check.
- **D-8 is off the critical path:** D13 supersedes the interview and card-sort prerequisites for this landing preview, so the synthesis waits for a future research round rather than blocking the page.
Checks: `check-content.mjs` passes; `check_promo.py` passes source mode; `--dist` passes on the 23:29 build (5 pages, both privacy routes now exist, 18 images per page with placeholder figures).
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: → Cursor: rebuild after the copy changes (the 23:29 build predates the kitchen/bench/storage edits); then I re-run the built-page audit. → Carlos: decide form or no form, which decides the privacy text.
Next: the built-page re-run of D-9 after the rebuild; D-7 manual half is with Antigravity or Carlos.

### 2026-11-17 · D13 verification on the integrated landing

The running static preview serves the new Bokmål and English copy and 18 responsive pictures on each homepage. Its privacy routes returned 200. Both landings and the two privacy pages were checked for visible email invitations and for coursework text. The image checker now verifies each URL in responsive image sets and has two regression checks.

[axe](../qa/a11y.md) reported zero violations on either homepage. [Mobile Lighthouse](../qa/perf.md) scored 100 in both languages, with LCP 1.38 s / 1.83 s and CLS 0 / 0.00005. The [current claims audit](../qa/claims-audit.md) records the rendered subscription state and the intended interior materials. Checked all 27 verifier self-tests.



### 2026-11-17 23:40 · D-9 claims audit · done (first pass, 1 critical finding)
Files: `fase4/promo/05-test/claims-audit.md` (new); `02-define/claims-register.csv` (K-34 added after finding a duplicate id)
Plan (DESIGN-GUIDE §1, step 2): no UI. Read every sentence of the current copy against the register, check the environmental wording, and check the name.
Evidence:
- **Audited the new copy, not the old build.** The team integrated fresh text at about 23:20 (`nb.json`/`en.json` now read «Vi tegner et hus for Bergen …»), so the audit is against the source of the next build; `dist` is from 22:36 and does not contain it. **1 500 words, `check_promo.py` source run fully clean** (the 19 image alts are filled; 0 problems).
- **Critical finding:** the privacy page says «Denne siden har ingen påmelding og ber ikke om navn eller e-postadresse» / "This site has no sign-up form …" while the page carries the «Følg prosjektet» form asking for e-mail and name. It also replaced the D-5 text and covers none of the required points. Owner: Cursor to place, Carlos/D6 to name the recipient; before G4.
- **Five sentences need softening** (bathroom «mørke fliser» vs the recorded petrol-green tile; bench cushion; drawer depth; kitchen worktop and «dempede fronter»; timber floor under the steel frame). Not applied: the team is still editing the same files and I will not race them.
- **Two smaller:** `meta.title` uses a middle dot (garbage list §10 no. 10), `meta.description` opens with «Utforsk»/«Explore».
- **Register housekeeping:** the team added their own **K-33** for the pine-heartwood tradition, with Treteknisk and Riksantikvaren sources; my canonical-facade row collided with it and is now **K-34**. 34 rows, all ids unique, all statuses legal. I have not fetched their two sources — that check belongs at G4.
- **Environmental:** no green claim anywhere; `check_promo.py` enforces the banned words. Forbrukertilsynet's guidance could not be read (every URL, including the root, answered with their 404 page to this fetcher); recorded as a limitation with the URL and the date.
- **Name:** Brønnøysund's open API returns **0 hits** for «MiniHouse» (2026-11-17). **Patentstyret not checked** — no browser route from here — and it is flagged as an open item for G5, with a note that the name is descriptive.
Checks: `check-content.mjs` passes; `check_promo.py` passes source mode; `--dist` still shows the old build's findings (2 broken privacy routes).
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: → Cursor and Carlos: the privacy contradiction is the one thing that must change before G4. → DeepSeek (me): the five softeners and the two metadata fixes, as one batch when the integration settles, then a re-run against the built page.
Next: apply the batch, re-run D-9 on the new build, then D-7 again after the contrast fix.

### 2026-11-17 · D13 landing copy · ready for preview

DeepSeek-V4.1-Flash drafted the Bokmål and English hero lead and three material descriptions in the MiniHouse desktop conversation (turn 12). Codex edited and integrated them into the two locale files and the matching copy decks. Cursor linked the new «Se huset» / “Explore the house” action to the gallery. D12 keeps Carlos’s chosen headline. The public copy now describes the unbuilt house for Bergen, planned reclaimed pine cladding, European oak at the thresholds and window sills, and the copper bathroom mirror. The website-development phase and email invitations were removed from the public experience. The privacy routes describe the current preview. D6 still governs enabling subscriptions.

The claims register ties the wood colour and traditional cladding use to [Treteknisk](https://www.treteknisk.no/resources/6.-publikasjoner/1.-fokus-pa-tre/Fokus-nr-34-1.pdf) and [Riksantikvaren](https://riksantikvaren.no/content/uploads/2023/04/Materialkvalitet_tre_veileder.pdf) in K-33. K-07 and K-08 retain the distinction between the intended wood and a documented batch. The current copy is in `04-prototype/copy-nb.md` and `copy-en.md`; the messaging guide now reflects D13 and the active gallery action.



### 2026-11-17 23:25 · D-7 accessibility and performance · done (first run)
Files: `fase4/promo/05-test/a11y.md`, `perf.md` (new); `reports/axe-4322.txt`, `axe-4322.json`, `lighthouse-nb.json`, `lighthouse-en.json` (new). Also `web/promo/src/content/{nb,en}.json` and both decks for the D-5 retention sentence.
Plan (DESIGN-GUIDE §1, step 2): no UI. Run the automated half of D-7 against Cursor's preview on 4322 and record exact commands, versions and numbers.
Evidence:
- **axe-core 4.14.1** (Chrome for Testing 157.0.8103.51, ChromeDriver 157 installed with `browser-driver-manager`): **5 violations per page, 10 in total**, all `color-contrast` (serious). Figcaptions in the irr band render `#6F3F1E` on `#2C4F40` = **1.04:1**, where DESIGN-GUIDE §6.8 says all text on that band is `--kalk`. Cursor's to fix (C-5); I cannot edit `web/promo/**`.
- **Lighthouse 13.6.0** (mobile, simulated throttling): **performance 100** on both pages; LCP **0.8 s**, CLS **0** / **0.004**, TBT **0 ms** / **20 ms**, JS **0 bytes**, first load **65 / 68 KiB**. All PLAN 5.5 gates pass on this build — because it still has no images and no client JavaScript, so this is a baseline, not a release certificate.
- **Two smaller findings for Cursor:** `/personvern/` and `/en/personvern/` do not resolve (40 errors in `check_promo.py --dist`, 38 of them the image alt texts), and `favicon.ico` 404s (the only console error Lighthouse logged). EN also fails Lighthouse's `hreflang` audit (SEO 0.9).
- **D-5 privacy:** added the retention sentence — «Vi lagrer opplysningene til du melder deg av eller ber om at de slettes» — so the page now covers what, why, who, how long, deletion, frequency and unsubscribe. It stays blocked on the legal name/organisation, the contact address and the form service (D6); `check_promo.py --release` still fails on the «før lansering» promise.
- Manual half of D-7 **not run** (keyboard walk, NVDA, 200 % zoom, reduced motion, hover/focus contrast). I cannot judge those by eye and did not claim them.
Checks: `node web/promo/scripts/check-content.mjs` → **content check passed** (1 615 words). `check_promo.py`: 25/25 self-tests.
Note: the Lighthouse and axe run used the 22:36 build; the privacy retention sentence landed afterwards, so a re-run is due with Cursor's contrast fix anyway.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: → Cursor: fix the irr-band caption colour (axe failure), add a favicon, build the two privacy routes, and fix `hreflang`; then I re-run both tools. The performance baseline is good enough that images and JS are the only things that can spoil it.
Next: D-9 claims audit when the contrast fix and the images land; D-8 waits on Carlos's interview notes.

### 2026-11-17 22:26 · D12 hero title and the follow-form key removal · done
Files: `web/promo/src/content/nb.json`, `en.json`; `04-prototype/copy-nb.md`, `copy-en.md`; `02-define/messaging.md`, `sitemap.md`, `claims-register.csv`
Plan (DESIGN-GUIDE §1, step 2): no UI. Carlos chose the title (D12) and Cursor narrowed the schema, so the copy follows both.
Evidence:
- **D12 in place.** `hero.title` is «Et lite hus, laget for å flyttes.» / "A small house, made to be moved." in both content files, both copy decks, messaging §4 and sitemap §2. The decks record it as decided at G2 instead of offering two options. **K-05** now notes that the title states the goal as intent, and forbids «et hus som kan flyttes», «klar til løft» and «kan løftes i dag».
- **Keys removed.** Cursor's schema holds only `interest.fields { email, name, optional }` plus `title`, `lead`, `consent`, `submit`, `success`, `errors`. `interest.price`, `municipality`, `use`, `useOptions`, `timeline`, `timelineOptions` and `message` are gone from both JSON files; the decks and the sitemap content model say so. Field order is now `email`, `name`, `optional`.
- **Previous nine fixes re-verified, not redone:** a script asserts all of them in both languages — permit answer, prototype question, «sitt eget pass», the steel lead, `build.exterior`/`structure`, journey intent, empty `footer.contact`, the blocked privacy body, the oak lead and the colon in `meta.title`. 16 of 16 pass.
Checks: `node web/promo/scripts/check-content.mjs` → **content check passed**. `check_promo.py`: 25/25 self-tests, source run 1 591 words (down from 1 670 with the dropped keys), 38 errors, all image alt texts Antigravity owes, «2 omitted» for the footer contact.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: → Cursor: the JSON now matches `schema.ts` exactly and `check-content.mjs` passes; a rebuild is enough to see D12 in the page. I checked `web/promo-holding/index.html`: it does not use the hero title, so it needs no change.
Next: D-5 metadata is in the files; the privacy page finishes with D6; D-7 waits for a build with content.

### 2026-11-17 22:15 · copy review fixes: permit, prototype, materials, intent wording · done
Files: `web/promo/src/content/nb.json`, `en.json`; `04-prototype/copy-nb.md`, `copy-en.md`; `02-define/claims-register.csv`, `messaging.md`, `pov-hmw.md`; `scripts/check_promo.py`
Plan (DESIGN-GUIDE §1, step 2): no UI. Nine review points, each applied in both languages and in the deck that documents it.
Evidence:
1. **Permit answer (K-14).** «Det avhenger av hva huset skal brukes til, og det er kommunen som avgjør.» / "It depends on how the house will be used, and the municipality decides." The offer of help is gone, and K-14's notes now forbid it explicitly.
2. **FAQ 3 (K-17).** «Når blir prototypen ferdig?» → «Det vet vi ikke ennå. Følg prosjektet, så sier vi fra.» The old question implied a sale; K-17 was re-scoped from delivery to the prototype and forbids a date.
3. **materials.lead.** «Hvert materiale har sitt eget pass.» (neuter «sitt»).
4. **Stål.** «Stålrammen bærer huset i chassiset.» — «og i veggene» is dropped, the wall structure is undecided.
5. **build.exterior / structure.** «Kledningen er tenkt som en ventilert regnskjerm …» (K-21 is now `planlagt`); «Chassiset er i dagens utkast … Profiler og dimensjoner er ikke valgt.»
6. **Journey as intent.** «Huset skal bygges ferdig inne», «Huset skal løftes på plass» — the two steps join «Målet er å frakte» as K-05 goals.
7. **footer.contact.** An empty string, rendered as nothing, until Carlos supplies an address (K-29). `check_promo.py` counts it as *omitted* rather than failing.
8. **Privacy.** Still blocked: the body now says the full name, organisation, contact address and form service are stated before launch, instead of naming only «Carlos». `check_promo.py --release` fails while that promise remains, so the page cannot ship incomplete.
9. **Minor.** The oak passport no longer mentions black frames (that lives in build.exterior); `meta.title` uses a colon, not a spaced dash, in both languages.
Hero title stays open for Carlos: A «Et lite hus som kan flyttes.» (in the JSON) and B «Et lite hus, laget for å flyttes.».
Checks: `node web/promo/scripts/check-content.mjs` → **content check passed**; `check_promo.py` self-test 25/25, source run 38 errors — all the image alt texts Antigravity owes, now with «2 omitted» for the footer contact; release mode additionally fails on the privacy promise and on every stand-in image, as intended.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: copy and deck agree again, and the register carries the sharper permit answer and the prototype question.
Next: Cursor's `schema.ts` change drops the seven unused interest keys; the privacy page finishes with D6; the hero title waits for G2.

### 2026-11-17 22:20 · CTA change: «Følg prosjektet» everywhere · done
Files: `02-define/messaging.md`, `metrics.md`, `sitemap.md`, `pov-hmw.md`, `claims-register.csv`; `01-empathize/kit.md`, `03-ideate/card-sort.md`; `04-prototype/copy-nb.md`, `copy-en.md`; `web/promo/src/content/nb.json`, `en.json`; `scripts/check_promo.py`
Plan (DESIGN-GUIDE §1, step 2): no UI. D1 is «Følg prosjektet» and D10 says nothing is for sale, so every sentence that assumed a sale had to change.
Evidence:
- **Copy and content files.** Button, header, form title and submit are «Følg prosjektet»; success «Takk! Du følger nå prosjektet.»; the consent checkbox is «Ja, send meg oppdateringer om MiniHouse på e-post.» (unticked, with the privacy link). The form asks for e-mail (required) and name (optional) and nothing else. The FAQ's price question became «Er huset til salgs?» with «Nei. …» (K-31). The footer contact is «Kontakt: svar på en av e-postene du får.» The privacy page now says how often updates come and that every e-mail has an unsubscribe link (K-30). `node scripts/check-content.mjs` → **content check passed**.
- **Register.** K-16 rewritten (D2 superseded by D10: no price at all), K-24 reworded for the follow form, and three rows added: **K-30** update frequency and unsubscribe (planlagt, D6 still open), **K-31** not for sale (bekreftet, D10), **K-32** the form asks only e-mail and name (bekreftet, D1 and §6.11). 32 rows, all validated.
- **Define docs.** messaging §3 is the new flow, §5 drops the emergency-cabin persona (D11) and adds the curious follower, §6 is now «FINN kit: cancelled» (D10), and the never-say table lists both superseded phrases. metrics' one number is now **sign-ups to follow the project**, and G5 expects the new success line. sitemap's section 9 is «Følg prosjektet» at `#folg`, and the content model names the keys Cursor must remove. pov-hmw's POV is a plot owner, A-1/A-4 are rewritten, and Q-2 is the update frequency.
- **Kit and card sort.** Usability T5 is the follow flow with its success criterion; card 11 is «Følg prosjektet»; the session plan drops the emergency persona; the questionnaire's CTA question is D6 for the follow form.
- **Checker.** `check_promo.py` gained two regression patterns — the superseded «Meld interesse» and «Pris kommer» — and two matching self-tests; 25 assertions pass, and the source run is unchanged at the 38 image-alt errors Antigravity still owes.
Open: Cursor has not yet edited `schema.ts`, so `municipality`, `use`, `useOptions`, `timeline`, `timelineOptions`, `message` and `price` are still in the schema and their (unreferenced) values stay in both JSON files. The privacy page stays blocked on D6. The one-a-month ceiling is my proposal and needs Carlos's yes at G4.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: the CTA, the form and the privacy promise now agree in both languages, and the register carries the three rows that make them checkable.
Next: D-5 metadata is already in the files; the privacy page finishes when D6 lands; D-7 waits for a build with content.

### 2026-11-17 22:05 · D-6 `scripts/check_promo.py` · done
Files: `scripts/check_promo.py` (new; no other script touched)
Plan (DESIGN-GUIDE §1, step 2): no UI. One stdlib-only checker with `--selftest`, `--dist PATH`, `--release`, exit 1 on any error.
Evidence: 665 lines. Checks: (1) the 10 tokens in `tokens.css` against the guide's table and all 11 allowed pairs plus the 3 forbidden pairs, **recomputing every WCAG ratio from the hex values** (tolerance 0.01 — all 14 numbers in the guide reproduce exactly); (2) `nb.json`/`en.json` key parity (recursive, arrays included) and no `TODO`/empty string; (3) the §9 banned words per language, matched as word prefixes so «petrolgrønn» is not «grønn», plus specific forbidden claims (no-permit, TEK17, U-value, price in kroner, delivery time, weight, «garantert», «verifisert», testimonials) while «Pris kommer.» passes; (4) every `images.json` entry has alt and caption in both languages, `--release` additionally requires `approved` and a file; (5) the built dist: missing `lang` (and `en` on `/en/`), exactly one `h1` per page, `<img>` without or with empty alt, external resource requests (outbound `<a>` links allowed), TODO text, «→» in text or alt, and CSS `text-transform: uppercase`, `monospace`, `linear-gradient`, `box-shadow` outside a lightbox/dialog selector; (6) every internal href/src/srcset/poster resolves (directories map to `index.html`). `--selftest` runs 22 assertions on synthetic input (contrast maths, token parsing, banned-word edges, key parity, HTML scan, CSS rules, link resolution in a temp fixture) — all pass.
Current report (the script telling the truth, not a green tick): source mode → 38 errors, all of them `images.json` alt text that Antigravity owns; `--dist web/promo/dist` → 48 errors: the same 38 plus TODO text in both pages, because the built dist predates my copy (C-3 built it with the placeholder JSON). `--release` would add the stand-in gate. The checker is clean the moment Antigravity fills the alts and Cursor rebuilds.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: → Cursor: after merging my `nb.json`/`en.json`, run `npm run check` and `npm run build`, then `python scripts/check_promo.py --dist web/promo/dist`; the only expected failures now are the 19 missing alt texts (Antigravity). → Antigravity: `check_promo.py` is the gate for alt/caption and for `--release`.
Next: D-7 once there is a build with content; D-5 metadata is already in the content files.

### 2026-11-17 22:02 · D-4 copy deck and content files · done
Files: `fase4/promo/04-prototype/copy-nb.md`, `copy-en.md` (new); `web/promo/src/content/nb.json`, `en.json` (filled; schema untouched)
Plan (DESIGN-GUIDE §1, step 2): no UI. Copy only, from the register and the messaging v0.
Evidence: 1 674 words across both languages, every string tagged with its `K-xx` in the deck. The contract check passes (`node scripts/check-content.mjs` → `content check passed`): all schema keys present, arrays sized, ids stable. Wording follows the six review points: hero titles A «Et lite hus som kan flyttes.» (in the JSON) and B «Et lite hus, laget for å flyttes.» for G2; the one-sentence message uses «laget for Bergen og Vestlandet» and «med et mål om å kunne flyttes i ett stykke», with no moving frequency; the CTA is «Meld interesse» at every step, including submit; the passport says «dokumenteres per parti»; buyer status is plain words («Tegninger og plan · første utkast klart», «Beregninger · pågår», «Prototype · ikke bygget», «Nettsiden · under arbeid») with no «Fase 0» anywhere on the page. Six FAQ answers, each tracing to a row. No price, date, weight, U-value, permit promise or invented contact: the footer points at the form (K-29) and the privacy text names Carlos as responsible without claiming a provider (K-24).
Open for G4: the privacy page still has to name the inbox and the form service (D6). Native Norwegian review is the next reader.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [x] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: → Cursor: `npm run check` and a rebuild; → Carlos: pick A or B for the hero at G2 and send the copy to a native reader.
Next: D-5 metadata (already written into the files) and D-6.

### 2026-11-17 21:58 · review follow-ups: messaging, sitemap, kit, K-26 · done
Files: `fase4/promo/02-define/messaging.md`, `sitemap.md`, `claims-register.csv`, `01-empathize/kit.md`
Plan (DESIGN-GUIDE §1, step 2): no UI. Apply the six points exactly.
Evidence:
1. **messaging §1:** the sentence now reads «… laget for Bergen og Vestlandet, med et mål om å kunne flyttes i ett stykke …». «bygget i Bergen» and «når du vil» are gone; the fragment table and the paragraph below it were rewritten to match (K-13 for the location, K-05 as a goal, moving frequency explicitly unknown).
2. **messaging §3:** submit is «Meld interesse», not «Send», with a sentence saying the button keeps its name and only the state changes.
3. **messaging proof 1:** «to be documented per lot» (K-22 is planlagt).
4. **sitemap §5:** only the four `bath-*` images are `pending`; every other image is **to produce**, per `bildeliste.csv`.
5. Copy deck and JSON: status in plain words (see D-4 entry), and the two hero titles are offered for G2 in both the deck and messaging §4. `K-26` was rewritten to carry the plain-words wording and to say «Fase 0–4» never appears on the buyer page.
6. **kit §7:** point 4 lists DeepSeek, Cursor, Claude Code **and Antigravity**; point 2 says «på Carlos sin PC» (nb) and "on Carlos's PC" (en).
Checks: CSV re-parsed (29 rows, 8 columns, legal statuses); every relative link in the five touched documents resolves.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: the message, the CTA and the status wording are now consistent across messaging, deck and JSON. G2 gets a real choice of two hero titles.
Next: D-4 and D-6 (both done above).

### 2026-11-17 21:47 · D-3 basis: market scan excluded until CR-16 · done
Files: `fase4/promo/02-define/pov-hmw.md`, `messaging.md`, `metrics.md`, `sitemap.md`
Plan (DESIGN-GUIDE §1, step 2): no UI. Make the evidence base of D-3 explicit and keep the unreviewed market scan out of it.
Evidence:
- **pov-hmw.md:** the basis line now separates "not yet available" (Carlos's questionnaire answers, the interviews) from **"excluded on purpose"**: `01-empathize/market-scan.md` stays out until **CR-16** is closed ([claude-code-review.md](../review/claude-code-review.md)), because it has no per-entry sources and one entry misdescribes the FINN listing. A new note under the assumption table says market evidence is limited to PLAN Appendix A, which is why A-1 and A-4 stay hypotheses.
- **messaging.md:** basis line names the claims register, the kit and PLAN §6, states the CR-16 exclusion, and credits PLAN Appendix A for the structure borrowed from the FINN listing.
- **metrics.md:** basis line states the exclusion, so no target or benchmark comes from the scan's unsourced figures.
- **sitemap.md:** basis line states the exclusion; the section order now explicitly rests on PLAN §8.6 and Carlos's concepts. The v1 table gains a row: market-derived emphasis and trust signals wait on the A-3 redo.
- Nothing in D-3 ever quoted or depended on the scan; this entry records the exclusion as a rule so v1 cannot pick it up by accident either.
Checks: bundled Python — all relative links in the four documents resolve (including the new `../review/claude-code-review.md`); CR-16 is cited in all four.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: v0 stands on the register, the kit and PLAN alone. When Antigravity closes CR-16, the scan can inform v1 (market patterns, the four gaps) — at that point the POV and messaging may be tightened, not rewritten.
Next: D-5 FAQ and metadata copy; D-6 once `tokens.css` exists.

### 2026-11-17 21:38 · D-3 define documents v0 · done
Files: `fase4/promo/02-define/pov-hmw.md`, `messaging.md`, `metrics.md`, `sitemap.md` (all new)
Plan (DESIGN-GUIDE §1, step 2): no UI. v0 drafts from PLAN §6, grounded in the claims register. Carlos's questionnaire and Antigravity's market scan are not available yet, so every persona-dependent statement is marked **hypothesis** with the test that would falsify it, and nothing is presented as approved.
Evidence:
- **pov-hmw.md** — one-sentence POV naming one buyer and one tension; a table separating what is claimed (K-13, K-05, K-19…) from what is hypothesis; five HMW questions mapped to their section and claim rows; six assumptions with falsifiers; five obligations the POV puts on the site; four open questions to Carlos (Q-1 buyer, Q-2 emergency, Q-3 D6, Q-4 Bergen scope). It explicitly refuses "warm, solid" as a performance claim (K-15).
- **messaging.md** — the one sentence with a fragment-by-fragment table of what each part may never become; three proofs (material, move, honesty) with allowed and forbidden wording per proof and its K-xx; one CTA with the same words through the flow (D1); hero slot constraints; message per audience; a FINN skeleton deliberately postponed to G5; a "never say" table for every row that has no claim (K-14…K-18, K-07, K-22, K-24, K-29).
- **metrics.md** — D9 makes a rate impossible, so the primary metric is a **submission count**, and the doc lists what it cannot measure (gallery opens, time on page, language switch) instead of inventing proxies; seven quality gates with numbers (axe 0, LCP 2.5 s, CLS 0.1, INP 200 ms, JS 50 KB, contrast 4.5:1, claims audit 0); the five human tests with pass criteria; an explicit "what we will not do" list; G5 success conditions.
- **sitemap.md** — seven routes including both languages, the privacy page (blocked on D6), 404, sitemap and robots; the ten sections with anchor, content key group, `images.json` ids and claim ids; nav labels flagged as card-sort-dependent; the content model per key group; the image→section map with image status; heading, landmark and ARIA rules; what changes at v1 and what must not.
Checks: bundled Python — every relative link resolves in all four documents; every `K-xx` referenced exists in the register (23, 23, 0, 28 distinct rows per document; metrics names none by design); banned-word scan finds them only inside the "never say" tables, never as a sentence of our own.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: Cursor can build against the anchors and key groups; Antigravity can use the image→section map for the shot list and the G4 approval. Carlos gets Q-1…Q-4 in `pov-hmw.md` §5 plus the G2 questions. G2 is **not** requested yet — v0 has to survive the interviews first.
Next: D-5 FAQ and metadata copy (the privacy page stays blocked on D6), and D-6 can start as soon as Cursor's `tokens.css` exists. D-4 waits for Cursor's **HANDOVER content**.

### 2026-11-17 21:33 · kit and claims follow-ups (Claude Code review 2) · done
Files: `fase4/promo/01-empathize/kit.md`, `fase4/promo/02-define/claims-register.csv`
Plan (DESIGN-GUIDE §1, step 2): no UI. Fix the three points so the consent is true for a public repo on a shared PC, and so one claim stops implying a fixed pitch.
Evidence:
1. **§7 consent, nb and en.** Point 2 now says the notes «publiseres ikke» (not «deles ikke») and adds that they are read by the AI tools in point 4 and by the people working on the site on this PC. Point 3 uses **participant codes P1–P5** instead of initials, with the code-to-person list only in Carlos's private notes and only anonymised summaries with the code published. Point 4 names the tools (DeepSeek, Cursor, Claude Code) and states that some of them may process text outside the **EU/EEA**. The consent field is «Deltakerkode: P__» / "Participant code: P__". The same change was made in the opening framing (§3.1) and the recruiting message (§2), which now promises a code, not initials.
2. **§8 note template.** Raw notes are `interviews/raw/P1.md` … `P5.md`, written with the code, never a name or initials; the published `P1…P5.md` summaries keep the code but no identifying detail. The rules line says "the code only".
3. **Overview table, row 1:** «kept on this PC (git-ignored)» instead of "stored in the repo".
4. **K-27 note:** "the 20° reference case in the height screening", with "the pitch is not fixed" added, so the row no longer implies a chosen pitch.
Checks: CSV re-parsed (29 rows, 8 columns, legal statuses); the remaining "initial" matches in `kit.md` are all explicit "not initials" phrases; links in `kit.md` still resolve.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: the consent is now usable on a shared PC with a public repo. This entry supersedes the initials wording in the D-2 entry and in the earlier review-fixes entry.
Next: D-3 define documents v0.

### 2026-11-17 21:15 · D-1/D-2 review fixes (Claude Code review) · done
Files: `fase4/promo/02-define/claims-register.csv`, `fase4/promo/01-empathize/kit.md` (`card-sort.md` unchanged)
Plan (DESIGN-GUIDE §1, step 2): no UI. Apply the five review points without widening scope: tighten two claims that were stated too strongly, make the research honest about a public repo, and fix a setup that could not work.
Evidence:
1. **K-06 → konsept.** Nothing is built and C-08 (the timber lot) is open, so the cladding/finishes role is a default, not a fact. Notes now forbid «bærende». Status mix is now **6 bekreftet, 10 konsept** (this supersedes the counts in the D-1 entry below).
2. **K-08 allowed wording** → «Eik er planlagt i terskler og vindusbrett.» / "Oak is planned for thresholds and window boards." The canonical house has black frames (`canonical-house.md` §2.3, decisions D8), so the notes now forbid «karmer»/frames.
3. **K-27 note** now says it is never used on the buyer page without K-05, because the height screen still exceeds 4.00 m at the concept's 20° pitch (registro §M, §N) — width alone must not read as «it fits on the road».
4. **kit §7 consent, nb and en, rewritten.** The repo is public: raw notes stay on Carlos's PC (`interviews/raw/` is git-ignored, confirmed in `.gitignore` lines 24–28), only anonymised summaries without initials are published, AI summarisation (DeepSeek) is disclosed as a point of its own, and retention is now «[dato Carlos fyller ut]» / "[date Carlos fills in]" instead of «til nettsiden er ferdig».
5. **kit §1** says `carlos-interview.md` is git-ignored and stays on this PC, because it covers budget and price ambition.
6. **kit §6 setup** replaced: a participant's phone cannot open `localhost:4322`. Two paths — same Wi-Fi with `npm run preview -- --port 4322 --host` and the LAN address, or a preview deploy only with Carlos's OK — plus a rule never to type a participant's real name or e-mail into a test form.
7. **kit §5.2 pass bar tightened** from "first or second of three" to **ranked first by ≥2 of 5 and walked away from by ≤1**, with "no direction clears → finding at G3" so a weak field is reported instead of papered over.
8. **kit §8** now separates the two tiers: initials are fine in the git-ignored `raw/` folder, and the published `P1…P5.md` summaries carry no initials, names or identifying details.
Checks: bundled Python `csv` — 29 rows, 8 columns, legal statuses, source rule, no duplicate ids: OK. Link check on `kit.md` and `card-sort.md`: all relative links resolve. PII pattern scan on both files: nothing. Banned-word scan (§9): nothing.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: the register is still the gate, and Cursor can wire K-xx into `schema.ts` copy when the content files land. Antigravity should use the tightened §5.2 bar in the G3 pack. The kit now reads correctly for a public repo, and Carlos can print the consent with his own deletion date.
Next: D-3 define documents v0.

### 2026-11-17 20:46 · D-2 research and test kit · done
Files: `fase4/promo/01-empathize/kit.md` (new), `fase4/promo/03-ideate/card-sort.md` (new)
Plan (DESIGN-GUIDE §1, step 2): no UI. The kit fixes the words the research uses, so the copy can't get ahead of the evidence. Norwegian for everything a participant reads or hears (recruitment, consent, cards, tasks); English mirror for the interview guide, consent and the Antigravity scripts; the questionnaire for Carlos is bilingual so he can answer in Spanish, English or Norwegian.
Evidence: 8 artefacts in `kit.md` — written questionnaire (§1), recruiting message (§2), 30-minute interview guide in nb+en (§3), pointer to the card sort (§4), 5-second and preference scripts with pass criteria (§5), usability script with the five PLAN §10 tasks and success criteria (§6), consent wording (§7), note template with initials only (§8) — plus the session plan (§9). `card-sort.md`: 12 cards, open-sort script, recording sheets, co-occurrence analysis, and a result table that reads «not run» until the sessions happen. Checks run: link check with the bundled Python — all relative links resolve; no names, e-mail addresses or phone numbers anywhere in either file (grep for `@` and `+47` returns nothing); no recruitment message is sent by an agent, it is text for Carlos.
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear (no hype words, no «bærekraftig», no invented specs)  [N/A] one accessory removed
HANDOVER: Carlos can run a session unaided: paste §2 for recruiting, read §7 before the call, follow §3, hand the cards in `card-sort.md` to three people, and keep notes with §8 outside the repo. Antigravity can drop §5 straight into the G3 test pack.
Next: D-3 define documents v0 (POV/HMW, messaging, metrics, sitemap) — blocked on nothing, but it improves after Carlos's questionnaire and Antigravity's market scan.

### 2026-11-17 20:40 · D-1 claims register · done
Files: `fase4/promo/02-define/claims-register.csv` (new)
Plan (DESIGN-GUIDE §1, step 2): no UI. Columns exactly as the brief: `id, claim_nb, claim_en, status, source, allowed_nb, allowed_en, notes`. Status vocabulary limited to bekreftet, konsept, intensjon, mål, planlagt, ikke bestemt, ikke beregnet, ikke målt.
Evidence: 29 rows. Every row of PLAN §12 is present as K-01…K-18 (size, 18 m², steel+reclaimed timber, gable roof, moved in one piece, malmfuru, oak, pressure treatment, bathroom, kitchen/bench/storage, Bergen, building permit, TEK17/U-values, price, delivery, weight — plus the materials split into cladding vs structure where §12 merges them). K-19…K-29 add the sentences the page will need and could not otherwise prove: under development, concept images, ventilated rainscreen, per-lot documentation, copper, form destination, one storey, phase status, the 3.25 m width screening, the docs-site link, the missing contact address. Each was checked against `PROJECT.md`, `fase1/registro-decisiones.md` (§A, §B, §D, §F, §M, §N), `fase1/clasificacion-uso-decision.md` §4, `fase1/geometria-R0.md`, `knowledge/comparisons/module-brief.md` (§1–§4), `fase4/brief-web.md` and `decisions.md`. Status mix: 7 bekreftet, 9 konsept, 1 intensjon, 1 mål, 1 planlagt, 8 ikke bestemt, 1 ikke beregnet, 1 ikke målt. Validation with the bundled Python `csv` module: 8 columns on every row, all statuses legal, no duplicate ids, no empty claims, and every row without a file path is «ikke bestemt» (K-07, K-08, K-17, K-29 by design; K-09 and K-24 point at `decisions.md` and stay unclaimable).
Definition of done (DESIGN-GUIDE §11, for anything visual): [N/A] tokens only  [N/A] allowed pairs  [N/A] copy from content files  [N/A] images from images.json  [N/A] keyboard  [N/A] reduced motion  [N/A] 360/1280 screenshots  [x] garbage list clear  [N/A] one accessory removed
HANDOVER: the register is the gate for every sentence on the site. Copy (D-4) tags each sentence with its `K-xx`; `check_promo.py` (D-6) will enforce the banned words and the unclaimable rows; the claims audit (D-9) re-reads the built site against it.
Next: D-2 research and test kit.
