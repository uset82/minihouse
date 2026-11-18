# Task · Move the site's film to the new 4K master (v18)

2026-11-18. **Agents:** WorkBuddy and DeepSeek. **Asked by Carlos:** «generate a task plan so workbuddy and deepseek update my new video · i have change the video for a new 4k resolution».

Plan by Claude Code. The film's design is in [DESIGN-GUIDE.md](../DESIGN-GUIDE.md) §6.15, and the protocol in [README.md](README.md).

## What changed

| | The old master | The new master |
|---|---|---|
| File | `images/minihouse_walkthrough_v11.mp4` (no longer on this PC) | [`images/minihouse_walkthrough_v18_4k.mp4`](../../../images/minihouse_walkthrough_v18_4k.mp4) |
| Picture | 1920 × 1080, 24 fps, 408 frames | **3840 × 2160**, 24 fps, H.264 High, 408 frames |
| Length | 17.02 s | **17.04 s** |
| Size | 42.7 MB | **138.4 MB**, with an AAC sound track |
| Shot cuts (ffmpeg scene detection) | 4.02, 7.02, 10.52, 14.52 s | **4.04, 7.04, 10.54, 14.54 s** |

It is the same edit, 0.02 s later. The five shots are the hillside, the living room with the loft ladder, the bed under the window, the bathroom with the copper mirror (ending in a whip pan), and a wide bathroom view. The loop windows in [`scripts/cut_film.py`](../../../scripts/cut_film.py) still fit their shots: living 4.10–6.95 s, bath 10.60–14.10 s.

**Two traps:**

1. **The crops.** `cut_film.py` hard-codes `SOURCE_SIZE = (1920, 1080)` and computes the living and bath crops from it. If only the file name changes, the crops land on the wrong part of a 4K frame. The script must read the size from the master with ffprobe.
2. **The only copies.** The v11 master is gone, so the cuts now on the site (`web/promo/public/film/*.mp4`, cut from v11) are the only copies of the v11 cuts. Back them up first (W-1).

## Carlos's choices (2026-11-18)

- **«Sharper on big screens».**
  - Screens of `64rem` and wider get a 1920 × 1080 hero film; smaller screens keep a 1280 × 720 one.
  - The two loops (living room, and the bathroom inside the copper mirror) get 1.5× more pixels.
  - Full 4K on the site was turned down as too heavy.
- **«Yes, after the checks».** When every check passes, the new film may be uploaded to **https://minihouse-preview.canner.app** only. The documentation site (minihouse-docs) and minihouse.canner.app are not touched.

## Rules for this task

- The master in `images/` is never changed, moved or re-encoded in place.
- Media (`*.mp4`, `*.jpg` and the rest) stays out of git; `.gitignore` already covers it. **No commit and no push** without Carlos's OK in your own chat.
- The only deploy allowed is W-6, to `minihouse-preview`, from `web/promo/.bundle`. Never `canner redeploy`.
- **Cursor and Antigravity don't touch** the files below while this task is open. Claude Code's design files stay as they are, apart from the facts W-7 updates.
- Before each step, read `status/workbuddy.md` and `status/deepseek.md`. After each step, add an entry at the top of your own status file (template at the end).

## WorkBuddy: the cut, the code, the visual checks, the preview

**You own, for this task:**

- `scripts/cut_film.py`;
- `web/promo/public/film/**` and `web/promo/src/assets/film/**` (the cuts and posters);
- `web/promo/src/content/films.json` and `films.ts`;
- `web/promo/src/components/Film.astro` and `web/promo/src/scripts/film.ts`;
- `fase4/promo/archive/film-v11/` (new; the backup);
- `fase4/promo/status/workbuddy.md` (new) and `status/workbuddy-screens/` (new);
- facts only: the cut table in DESIGN-GUIDE §6.15 and the film lines in PLAN §7.

| ID | Task | Done when |
|---|---|---|
| W-1 | **Back up.** Copy `web/promo/public/film/*.mp4` and `web/promo/src/assets/film/*.jpg` to `fase4/promo/archive/film-v11/`. | 3 videos and 3 posters are in the backup, with the same byte sizes |
| W-2 | **`cut_film.py` for v18:**<br>• `SOURCE` points at `minihouse_walkthrough_v18_4k.mp4`, with `EXPECTED_DURATION = 17.04`.<br>• Read the source width and height with ffprobe, and delete `SOURCE_SIZE`.<br>• Keep the shot times, the crossfade on the hero, and the forward-and-back loops.<br>• New outputs, each checked against its budget, with a warning if over:<br>  – `house-film-1920.mp4`: 1920 × 1080, ≤ 4.5 MB;<br>  – `house-film.mp4`: 1280 × 720, ≤ 2.5 MB;<br>  – `living-loop.mp4`: 1440 × 960 (3:2 crop at the centre), ≤ 1.2 MB;<br>  – `bath-loop.mp4`: 1080 × 1350 (4:5 crop at 45 % across), ≤ 1.3 MB.<br>• Silent H.264, `+faststart`, `-g 48`. Start at today's CRF (31 for the hero, 30 for the loops) and raise it only to meet a budget.<br>• Posters are the first frame of the largest cut of each film, so the hero poster comes from the 1920 cut. | the script runs clean and prints every size within its budget |
| W-3 | **Look before you trust it.**<br>• Make a contact sheet of v18: the start, middle and end frame of each of the five shots.<br>• Compare one frame of the v11 cut (the backup) with the v18 cut at full size.<br>• Check the living 3:2 crop, and the bath 4:5 crop under the mirror shape (the clip path is in `MirrorFrame.astro`).<br>• Watch three loops of each cut for a jump or a flash.<br>Report any shot whose content changed from v11 to DeepSeek (D-15). | the canonical house is confirmed (gable roof, vertical boards, black door, steel base, no container); the crops keep their subject; no seam |
| W-4 | **Code for the sharper desktop film:**<br>• `films.json`: an optional `wide` entry (`file`, `width`, `height`) on `house`.<br>• `films.ts`: expose it as `srcWide`.<br>• `Film.astro`: add `data-film-src-wide`, and allow a 1920 poster width.<br>• `src/scripts/film.ts`: when loading, use the wide file if `matchMedia('(min-width: 64rem)')` matches, otherwise the normal one.<br>The living loop and the mirror keep one file each. Nothing else in the controller changes: one shared pause, `sessionStorage`, no autoplay under reduced motion or Data Saver, nothing before `load`. | `npm run check`: 0 errors |
| W-5 | **Build and verify** with the system Node (`C:\Program Files\nodejs`):<br>• `npm run check`, `npm run build`, `python scripts/check_promo.py` and `--dist web/promo/dist`, then `python scripts/verificar_todo.py`.<br>• Playwright on the **installed Chrome** (`channel='chrome'`; Playwright's own Chromium has no H.264), at 390 × 844, 1280 × 900 and 1920 × 1080:<br>  – the right file per width (`currentSrc`);<br>  – it plays by itself without sound (`currentTime` advances);<br>  – one pause button stops every film, and the pause survives a reload;<br>  – nothing plays under `reduced_motion='reduce'`;<br>  – nothing overflows sideways.<br>• Screenshots of the hero and «Inne i MiniHouse» at 360, 768, 1280 and 1920 px. | all pass; screenshots in `status/workbuddy-screens/` |
| W-6 | **Upload to the preview** (Carlos: «Yes, after the checks»), only after W-5 and D-14 pass:<br>• in `web/promo`, run `npm run bundle`;<br>• from `web/promo/.bundle`, run `canner deploy --slug=minihouse-preview --follow`.<br>Then check the live site:<br>• every film answers `curl -r 0-1` with 206 and `video/mp4`;<br>• `/.env.production` returns 404;<br>• the film plays in Chrome and in Playwright's WebKit at 390 × 844 and 1920 × 1080. | live and verified |
| W-7 | **Close.** Write your log in `status/workbuddy.md` with commands, sizes and screenshot paths. Update the cut table in DESIGN-GUIDE §6.15 and the film lines in PLAN §7 with the measured numbers. Write a **HANDOVER** to DeepSeek. | logged |

## DeepSeek: proof, words and the live check

You can't see images: never judge a picture; ask WorkBuddy.

**You own, for this task:**

- `fase4/promo/qa/film-v18.md` (new) and `qa/perf.md`;
- the `film.*` keys in `web/promo/src/content/nb.json` and `en.json`;
- `fase4/promo/content/claims-register.csv`;
- `fase4/promo/status/deepseek.md`.

| ID | Task | Done when |
|---|---|---|
| D-14 | **After W-2, the facts.** Run ffprobe on the master and each cut:<br>• width, height, duration, frame rate and codec;<br>• that there's **no audio stream**;<br>• that the `moov` atom comes before `mdat` (fast start);<br>• each size against its W-2 budget.<br>Record every command and result in `qa/film-v18.md`. | facts recorded; anything off is a request to WorkBuddy |
| D-15 | **Words and claims.** Point K-35's source at `images/minihouse_walkthrough_v18_4k.mp4` (17.04 s, 4K). Keep `film.alt`, `film.livingAlt` and `film.bathAlt` unless W-3 reports a changed shot; if one changed, rewrite it from WorkBuddy's description, in both languages. Avoid «grønn» and "green", which trip the banned-word check even as a colour. | the register and both JSON files agree; `python scripts/check_promo.py` passes |
| D-16 | **After W-5, the weight.** Run Lighthouse, mobile and desktop, against the built site (`npm run preview -- --port 4322`, run by WorkBuddy). Record:<br>• that the largest paint is still the poster image;<br>• the film bytes per viewport (desktop about 4.5 MB, phone about 2 MB);<br>• that they load after the `load` event. | numbers and commands recorded in `qa/perf.md` |
| D-17 | **After W-6, the live check** of https://minihouse-preview.canner.app:<br>• status codes for the pages and every film;<br>• `Content-Type` and byte ranges (206) for each film;<br>• `/.env.production`, `/package.json` and `/serve.mjs` return 404;<br>• `check_promo.py --dist web/promo/dist` on the uploaded build. | recorded in `qa/film-v18.md` |

## Order

```
W-1 → W-2 → W-3 ─┬─→ W-4 → W-5 ─┬─→ W-6 → W-7
                 │              └─→ D-16
                 ├─→ D-15
         W-2 ────┴─→ D-14 ───────→ (W-6 waits for D-14)
                                   W-6 → D-17
```

## Status entry template (WorkBuddy: start `status/workbuddy.md` with this)

```text
# Status · WorkBuddy

Only WorkBuddy writes this file. Newest entry first. Task: agents/task-film-v18.md.

## Requests to other agents

## Log

### YYYY-MM-DD HH:MM · W-… title · done | in progress | BLOCKED
Files: …
Evidence: commands run and results, sizes, screenshot paths …
HANDOVER / BLOCKED: …
Next: …
```

## Kickoff prompts

**WorkBuddy**

```text
You are WorkBuddy on the MiniHouse promo website. Carlos replaced the film master with a 4K version:
images/minihouse_walkthrough_v18_4k.mp4. Read fase4/promo/agents/task-film-v18.md (your tasks W-1 to W-7),
then DESIGN-GUIDE.md §6.15 and fase4/promo/agents/README.md. Edit only the files the task gives you.
Start with W-1 (back up the current cuts), then W-2: cut_film.py must read the 4K size from ffprobe.
Never change the master, never commit or push, and deploy only to minihouse-preview in W-6 after the checks pass.
Log every step in fase4/promo/status/workbuddy.md.
```

**DeepSeek**

```text
You are the DeepSeek agent on the MiniHouse promo website. Carlos replaced the film master with a 4K version.
Read fase4/promo/agents/task-film-v18.md (your tasks D-14 to D-17) and fase4/promo/status/workbuddy.md.
You can't see images: verify with ffprobe and curl, and ask WorkBuddy about anything visual.
Start with D-14 once WorkBuddy reports W-2 done. Edit only the files the task gives you.
Don't publish, commit or push. Log every step in fase4/promo/status/deepseek.md.
```
