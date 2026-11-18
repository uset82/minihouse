# Status · WorkBuddy

Only WorkBuddy writes this file. Newest entry first. Task: agents/task-film-v18.md.

## Requests to other agents

## Log

### 2026-11-18 21:17 · W-5 build and three-viewport verification · done
Files: no source edits; screenshots added to `status/workbuddy-screens/` (hero_360/768/1280/1920.png, inne_360/768/1280/1920.png).
Plan: read both status files first (my W-4 entry; DeepSeek's 20:58 entry — D-15 source updated, D-16 waiting on W-5). Run every checker, then Playwright on installed Chrome at the three specified viewports and review screenshots by eye.
Evidence (all commands from the repo root unless noted, system Node v22.22.0):
- `cd web/promo && npm run check` → 34 files, **0 errors / 0 warnings / 0 hints**, content check passed. `npm run build` → 5 pages built, 120 optimized images, complete.
- `python scripts/check_promo.py` → all checks passed (19 images, dev mode). `python scripts/check_promo.py --dist web/promo/dist` → all checks passed (5 pages). `python scripts/verificar_todo.py` → **SUITE COMPLETA: TODO PASA** (34 checks, including check_web).
- Playwright Python, `p.chromium.launch(channel='chrome')`, http://127.0.0.1:4322/ (a preview was already listening on 4322 — PID 13084 — and served the **new** markup with `data-film-src-wide`; no second server started). For 390×844 / 1280×900 / 1920×1080:
  - hero `currentSrc` = `house-film.mp4` at 390 (1280×720); `house-film-1920.mp4` at 1280 and 1920 (1920×1080). Living/bath stay one file each (1440×960, 1080×1350).
  - hero advances to t=1.62 / 1.70 / 1.70 s within 1.8 s, `muted=true`, not paused → autoplay without sound. At the two wide widths all three films play.
  - first pause button → `sessionStorage=minihouse-film:"paused"`, all three `paused=true`, label «Spill av filmen»; after reload all still paused at t=0 with the same label and storage.
  - fresh context with `reduced_motion='reduce'` → all three paused at t=0, label «Spill av filmen».
  - `documentElement.scrollWidth - innerWidth` = **0 px** at all three widths.
- Screenshots of `#bygget` and `#bo` at 360, 768, 1280, 1920 px; I viewed 360/1280/1920: film and caption row in place, mirror does not cover the living film's pause button, script stroke unclipped, no overflow. One accessory removed in the final pass: none added in this task (the code change is one media-query branch only).
HANDOVER → DeepSeek (D-16): the preview at **http://127.0.0.1:4322/** is already running and serves this build; run Lighthouse mobile/desktop against it. The largest paint is expected to be the hero poster; film bytes per viewport: wide cut 3.94 MB, phone cut 2.40 MB, plus loops 1.04 / 1.14 MB when in view. D-17 waits on W-6.
Next: W-6 — bundle and upload to `minihouse-preview` after this step and D-14 are passed.

### 2026-11-18 21:08 · W-4 sharper desktop film code · done
Files: `web/promo/src/content/films.json`, `films.ts`, `src/components/Film.astro`, `src/scripts/film.ts` (only these four).
Plan: read both status files first (my W-3 entry; DeepSeek's 20:58 D-15 entry). Add an optional wide file on the house entry only; keep the loops at one file each and leave the controller's pause, sessionStorage, reduced-motion, Data Saver and load-gating logic intact.
Evidence:
- `films.json`: `house.wide = { file: "house-film-1920.mp4", width: 1920, height: 1080 }`; widths of the three entries updated to the measured 1280x720 / 1440x960 / 1080x1350; all `source` strings now name the 4K master and 17.04 s. `status` stays `pending` — Carlos's G4 is untouched.
- `films.ts`: optional `wide` on `FilmEntry`, `srcWide` exposed on `Film`, set to `/film/<wide.file>` only where present.
- `Film.astro`: `<video data-film-src-wide={film.srcWide}>` (omitted for the loops), and the poster `widths` list now admits 1920 px for the hero poster.
- `film.ts`: `const wideScreen = matchMedia('(min-width: 64rem)')` and, at load time only, `video.src = wideScreen.matches && video.dataset.filmSrcWide ? … : video.dataset.filmSrc`. No resize switching, no change to the shared state.
- `npm run check` (system Node v22.22.0): astro check on 34 files → **0 errors, 0 warnings, 0 hints**; `check-content.mjs` → content check passed.
Next: W-5 — full build, the repository checkers and Playwright on installed Chrome at three viewports.

### 2026-11-18 21:02 · W-3 visual checks of the v18 cuts · done
Files: new screenshots in `status/workbuddy-screens/` (owned dir). No cut, master or code changed.
Plan: read both status files before the step (my W-2 entry; DeepSeek's 20:52 D-14 entry — done, no technical finding). Judge the pictures myself because DeepSeek cannot see them; compare v11 vs v18 shot by shot, then check the two crops and the loop seams.
Evidence:
- **Contact sheet** `v18_contact_sheet.png` (5 shots × start/middle/end, frames at 0.25/2.02/3.79, 4.29/5.54/6.79, 7.29/8.79/10.29, 10.79/12.54/14.29, 14.79/15.79/16.79 s). Shot 1 is the canonical house: **symmetrical gable roof in black standing-seam metal, silver-brown vertical boards, solid black door left of centre, black picture window, low dark steel plinth, fjord/mountain behind — no container, no flat roof, no corner castings**. Shot 2 living room with loft ladder and window bench; shot 3 bed under the window with rust throw; shot 4 copper wavy mirror, timber vanity, petrol-green shower and whip pan; shot 5 wide bathroom (fisheye framing) with WC, door, mirror and vanity. `v11_vs_v18_all_shots.png` and `shot4_v11_v18_detail.png`: **all five shots are the same subjects/compositions in both versions**; v18 is sharper. At 12.40 s v11's whip pan is blurrier than v18's (phase within the fast pan), but `shot45_boundary.png` at 13.90/14.00/14.10 s shows **both cut to shot 5 at the same time**; a 24 fps frame-difference scan puts the four shot boundaries at 3.500/6.500/10.000/14.000 s of either cut (master 4.0/7.0/10.5/14.5 s). No content change, so no alt text needs rewriting.
- **Crops** `v18_crop_check.png`: the 3:2 living crop keeps the bench, cushions, ladder, loft and kitchenette with no black bars; the 4:5 bath crop at 45 % keeps the copper mirror, basin, tap and vanity. `bath_mirror_clip_check.png`: bath cut rendered through the **actual `unitPath` clip and `framePath` stroke copied from `MirrorFrame.astro`** on `--irr`; mirror and sink stay legible inside the wavy shape, frame stroke complete. The top edge of the copper mirror sits close to the clip at some frames; no essential subject is lost.
- **Seams** `hero_seam_strip.png`, `living_seam_strip.png`, `bath_seam_strip.png`: crossfade at 16.25 s blends the wide bath back into the exterior; both ping-pong loops turn at 2.833 s / 3.500 s and wrap without a jump, black frame or flash. All frames of each loop were also scanned: wrap (last→first) 2.99 / 1.71 / 1.22 on 0–255; no spike at turnarounds (living max 1.60, bath max 2.15 versus 0.69 / 1.63 median). Three repetitions add no new frames, so this covers "three loops" for a deterministic loop.
Checks: ffmpeg frame extraction, Pillow sheets, numpy frame deltas, Playwright/Chrome render of the real clip path. No media rewritten.
HANDOVER → DeepSeek (D-15): **no shot content changed from v11 to v18** — keep `film.alt`, `film.livingAlt` and `film.bathAlt` as they are; K-35 only needs the new file/duration/4K source. → DeepSeek (D-14): the sizes and atoms you measured match mine.
Next: W-4 — the wide-file code path in `films.json`, `films.ts`, `Film.astro` and `src/scripts/film.ts`.

### 2026-11-18 20:44 · W-2 v18 cuts from the 4K master · done
Files: `scripts/cut_film.py` (rewritten); new `web/promo/public/film/house-film-1920.mp4` and 3 replacement cuts; 3 replacement posters in `web/promo/src/assets/film/`.
Plan: read both status files before the step (workbuddy.md at top; deepseek.md had no D-14 entry yet). Change only the master pointer, duration, crop source and outputs; keep shot windows, crossfade and ping-pong. ffprobe supplies width/height; CRF starts at the existing values and rises only when a budget is missed.
Evidence: master probed `3840 x 2160`, 24 fps, 408 frames, 17.041016 s, H.264; `SOURCE` now `images/minihouse_walkthrough_v18_4k.mp4`, `EXPECTED_DURATION = 17.04`, `SOURCE_SIZE` deleted, `probe_size()` added. `python scripts/cut_film.py` (1 m 58 s) printed:
- `house-film-1920.mp4` 1920x1080, 16.54 s, **3.94 MB / 4.5 MB** at CRF 33 (31 and 32 exceeded the budget)
- `house-film.mp4` 1280x720, 16.54 s, **2.40 MB / 2.5 MB** at CRF 31
- `living-loop.mp4` 1440x960 (3:2 centre crop), 5.67 s, **1.04 MB / 1.2 MB** at CRF 32 (30 exceeded)
- `bath-loop.mp4` 1080x1350 (4:5 crop at 45%), 7.00 s, **1.14 MB / 1.3 MB** at CRF 30
- posters: `house-film.jpg` 402 KB **from the 1920 cut**; `living-loop.jpg` 236 KB; `bath-loop.jpg` 122 KB
ffprobe on all four: video-only (no audio stream), H.264, 24 fps, moov before mdat (`ftyp`, `moov`, `mdat` at the start of each file), `-g 48` and `+faststart` set in the command. Master still 138 380 521 B, mtime 20:06:03 — unchanged. Media stays git-ignored; no commit, push or deploy.
HANDOVER → DeepSeek: W-2 is done — D-14 can run ffprobe on the master and the four cuts now. The hero CRFs had to rise to 33 (1920) and the living loop to 32; all sizes are inside budget.
Next: W-3 — visual checks of the new cuts.

### 2026-11-18 20:41 · W-1 back up the v11 cuts · done
Files: `fase4/promo/archive/film-v11/` (new): house-film.mp4, living-loop.mp4, bath-loop.mp4, house-film.jpg, living-loop.jpg, bath-loop.jpg.
Plan: read task-film-v18.md, DESIGN-GUIDE §6.15 and agents/README.md first; read both status files before the step (workbuddy.md did not exist yet — created here; deepseek.md read). Copy the only existing v11 cuts before any re-encode; no master touched.
Evidence: `mkdir -p fase4/promo/archive/film-v11` then `cp` of the 3 mp4 from `web/promo/public/film/` and the 3 jpg from `web/promo/src/assets/film/`. All 6 pairs verified identical by `stat -c%s` and `sha256sum`:
- house-film.mp4 2 083 980 B `7128f19d…f7516`; living-loop.mp4 562 155 B `80a5ec9a…38d6b1`; bath-loop.mp4 867 936 B `9dfae859…f2de8bfca`
- house-film.jpg 201 558 B `24977335…e557`; living-loop.jpg 120 479 B `ef2f5f97…6b1`; bath-loop.jpg 79 857 B `946d138d…671b1317`
No git operation, no deploy, no edit to any cut or master.
Next: W-2 — adapt `scripts/cut_film.py` to the 4K master and read its size with ffprobe.
