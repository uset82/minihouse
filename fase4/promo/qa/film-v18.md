# Film v18 · QA

Task D-14 to D-17 ([task-film-v18.md](../agents/task-film-v18.md)). 2026-11-18. Master: `images/minihouse_walkthrough_v18_4k.mp4`. Cuts: made by WorkBuddy in W-2.

**State: D-14 to D-17 done.** Master and four cuts measured (§1–§2); words and claims closed (§4); the live preview checked (§4). Everything here is read-only; nothing was re-encoded.

Tools: ffprobe/ffmpeg 8.0.1 (Gyan build, `C:\Users\carlos\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin`). No ffprobe on `PATH` in this session; the full path above is used in every command.

## 1 · The master

```powershell
ffprobe -v error -show_entries format=duration,size,bit_rate,format_name `
  -show_entries stream=index,codec_name,profile,width,height,r_frame_rate,avg_frame_rate,nb_frames,pix_fmt,sample_rate,channels `
  -of json images\minihouse_walkthrough_v18_4k.mp4
```

| Fact | Measured | Matches the task |
|---|---|---|
| Picture | 3840 × 2160, H.264 **High**, yuv420p | yes |
| Frame rate | 24/1 (average 24/1) | yes |
| Frames | 408 | yes |
| Duration | **17.041016 s** | yes (17.04) |
| Size | 138 380 521 B (132.0 MiB) | yes (138.4 MB decimal) |
| Overall bit rate | 64 963 507 bit/s | – |
| Sound | AAC LC, 48 kHz, 2 channels, 805 frames | yes (an audio track exists) |

The master has an audio stream. The cuts must not: D-14 checks each cut for **no audio stream**, and a leaked audio track would also break the "silent film" rule in DESIGN-GUIDE §6.15.

## 2 · The cuts — measured on W-2's outputs

Measured on the files WorkBuddy produced, then confirmed against their W-2 entry. WorkBuddy raised the hero CRF to 33 (1920) and the living loop to 32 to stay inside budget, and their decimal sizes (3.94 / 2.40 / 1.04 / 1.14 MB) match the binary sizes below. The CRF rise is a quality trade-off, not a technical defect — it is W-3's job to look for compression artefacts, and I have asked for exactly that.

```powershell
ffprobe -v error -show_entries format=duration,size `
  -show_entries stream=index,codec_type,codec_name,profile,width,height,r_frame_rate,nb_frames `
  -of json web\promo\public\film\<cut>.mp4
```

| Cut | Picture | Frames | Duration | Size | Budget | Audio | Profile |
|---|---|---:|---:|---:|---:|---|---|
| `house-film-1920.mp4` | 1920 × 1080 | 397 | 16.542 s | 3.76 MiB (3 943 047 B) | ≤ 4.5 MB | **none** | High |
| `house-film.mp4` | 1280 × 720 | 397 | 16.542 s | 2.29 MiB (2 403 562 B) | ≤ 2.5 MB | **none** | High |
| `living-loop.mp4` | 1440 × 960 (3:2) | 136 | 5.667 s | 0.99 MiB (1 041 410 B) | ≤ 1.2 MB | **none** | High |
| `bath-loop.mp4` | 1080 × 1350 (4:5) | 168 | 7.000 s | 1.08 MiB (1 137 205 B) | ≤ 1.3 MB | **none** | High |

Every cut is inside its budget; none carries an audio stream, which is the check that matters because the master has one. Frame rate is 24/1 on all four, and the aspect ratios are exactly the ones W-2 asked for (3:2 living, 4:5 bath).

The hero films are 16.542 s rather than the master's 17.041 s: that is the loop seam, trimmed the same way the v11 cut was (16.5 s in DESIGN-GUIDE §6.15). Not a defect.

Fast start, on all four:

| Cut | Top-level order | Verdict |
|---|---|---|
| `house-film-1920.mp4` | `ftyp`, `moov`, `free`, `mdat` | fast start |
| `house-film.mp4` | `ftyp`, `moov`, `free`, `mdat` | fast start |
| `living-loop.mp4` | `ftyp`, `moov`, `free`, `mdat` | fast start |
| `bath-loop.mp4` | `ftyp`, `moov`, `free`, `mdat` | fast start |

**Anything off: nothing.** D-14 has no request for WorkBuddy except the W-2 confirmation itself. One question remains for W-3, and it is visual, not technical: did any shot's content change, and do the two crops keep their subject (§5).

## 3 · Fast start: how it is checked

The `moov` atom must precede `mdat`, or Safari waits for the whole file. Reading the top-level box order is enough and does not need a decoder:

```python
import struct
with open(path, 'rb') as f:
    while True:
        head = f.read(8)
        if len(head) < 8: break
        size, typ = struct.unpack('>I4s', head)
        print(typ.decode('latin-1'), size)
        if size < 8: break
        f.seek(size - 8, 1)
```

Already run on two files as a method check:

| File | Order | Verdict |
|---|---|---|
| `fase4/promo/archive/film-v11/house-film.mp4` (the v11 cut) | `ftyp`, `moov`, `free`, `mdat` | fast start |
| `web/promo/public/film/house-film-1920.mp4` (new, mid-W-2) | `ftyp`, `moov`, `free`, `mdat` | fast start |

## 4 · D-15, D-16, D-17

### D-15 · words and claims · done

WorkBuddy's W-7 states it plainly: **no shot changed** from v11 to v18, and the two crops keep their subject. So `film.alt`, `film.livingAlt` and `film.bathAlt` stay exactly as they are in both languages, and K-35 now cites the 4K master with the four cuts named (that edit landed at 20:58). The caption remains «Konseptfilm»: the film is still a rendered concept, never a recording of a built house.

The CRF-33 hero and CRF-32 living loop were checked at full size by WorkBuddy, who can see pictures: no visible banding in the sky, the cladding, the wall or the copper. That closes the one quality question my tools could not answer.

### D-16 · weight · done

Full table in [perf.md](perf.md). Against the 4322 preview, Lighthouse 13.6.0:

| | Phone (412) | Desktop (1350) |
|---|---:|---:|
| Performance | 100 | 100 |
| LCP | 1.7 s | 0.4 s |
| Largest paint | poster `img.film-still` | poster `img.film-still` |
| Film bytes | **2.29 MB** (720p) | **5.84 MB** (1080p hero 3.76 + both loops) |
| Films start after `load` | yes, 746 ms vs 712 ms | yes, 486 ms vs 391 ms |

The page paints the poster first, and no film request begins before the `load` event. The desktop figure is larger than the hero's 4.5 MB budget because both loops also enter its load window; the hero file itself is 3.76 MB and every film is lazy, so LCP is untouched.

Raw reports: `qa/reports/lighthouse-story-mobile.json`, `lighthouse-story-desktop.json`.

### D-17 · live check of the preview · done

Against <https://minihouse-preview.canner.app>, 2026-11-18 23:05, `curl` 8.x:

| Check | Result |
|---|---|
| `/` and `/en/` | 200 `text/html; charset=utf-8` |
| `house-film-1920.mp4`, `house-film.mp4`, `living-loop.mp4`, `bath-loop.mp4` with `-r 0-1` | **206 Partial Content**, `video/mp4`, 2 bytes |
| `/.env.production`, `/package.json`, `/serve.mjs` | **404** |
| `python scripts/check_promo.py --dist web/promo/.bundle` | **all checks passed**, 5 pages, 19 images per page, both `lang` values correct, one `h1` per page |

The uploaded bundle on the server is the one checked: `.bundle` holds the built pages and the four films, and its byte counts match the deployed requests. Nothing else was deployed, and no `canner redeploy` was run.

## 5 · Requests to WorkBuddy — closed

1. W-2 confirmed; W-3 answered the banding question at full size (no visible artefacts).
2. W-3 confirmed no shot changed and both crops keep their subject; the alt texts therefore stand.

