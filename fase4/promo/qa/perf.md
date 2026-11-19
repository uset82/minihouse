# Performance · D13 photo landing

## R3 build · D-27 (2026-11-19)

Build measured: `web/promo/dist`, **built 2026-11-19 01:51**, 7 pages, served on `http://127.0.0.1:4322`. Lighthouse 13.6.0, mobile emulation and the desktop preset, system Node v22.22.0. Reports: `qa/reports/lighthouse-r3-{home,story}-{mobile,desktop}.json`.

```powershell
npx lighthouse http://127.0.0.1:4322/           --output=json --output-path=fase4/promo/qa/reports/lighthouse-r3-home-mobile.json    --chrome-flags="--headless=new --no-sandbox" --quiet
npx lighthouse http://127.0.0.1:4322/           --preset=desktop --output=json --output-path=fase4/promo/qa/reports/lighthouse-r3-home-desktop.json   --chrome-flags="--headless=new --no-sandbox" --quiet
npx lighthouse http://127.0.0.1:4322/historien/ --output=json --output-path=fase4/promo/qa/reports/lighthouse-r3-story-mobile.json  --chrome-flags="--headless=new --no-sandbox" --quiet
npx lighthouse http://127.0.0.1:4322/historien/ --preset=desktop --output=json --output-path=fase4/promo/qa/reports/lighthouse-r3-story-desktop.json --chrome-flags="--headless=new --no-sandbox" --quiet
```

| | `/` phone | `/` desktop | `/historien/` phone | `/historien/` desktop |
|---|---:|---:|---:|---:|
| Performance | **0.97** | **1.00** | **1.00** | **1.00** |
| Accessibility / best practices / SEO | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 1 | 1 / 1 / 1 |
| LCP | **2.3 s** | **0.5 s** | **0.8 s** | **0.5 s** |
| CLS | **0** | **0.009** | **0** | **0.005** |
| TBT | 150 ms | 0 ms | 20 ms | 0 ms |
| Transfer | 2 795 KB | 6 436 KB | 285 KB | 310 KB |
| JavaScript | 1 765 B | 1 765 B | 1 419 B | 1 419 B |

**Largest paint, and what it is:**

| Run | LCP element |
|---|---|
| `/` phone | the house film's poster, `figure.film > div.film-frame > picture > img.film-still` |
| `/` desktop | the same poster |
| `/historien/` phone | a paragraph, `div.story-open … div.story-col > p` (text, not a picture) |
| `/historien/` desktop | the stone photo, `div.story-photo > figure > picture > img.ratio-wide` (`midtun-stone`) |

All three D-27 gates pass: axe 0 violations (see [a11y.md](a11y.md)), LCP at most 2.5 s on mobile, CLS at most 0.1.

**Two notes for the record, neither a failure:**

1. **LCP on the phone home page is 2.3 s, 0.2 s inside the gate.** The largest paint is the **poster** of the house film, so the film itself still does not delay the paint (its requests start after `load`). It was 1.7 s on the 23:27 build; the R3 home page carries the gable photo as well, and this run read 2 795 KB. Worth watching, not worth changing now.
2. **The Midtun film is not on the story page**, because `images/midtun_teachers_residence_clean_4k.mp4` does not exist yet (G-16 blocked). So the film still is *not* the largest paint there: it is text on the phone and the stone photo on the desktop. The card's expectation for that case is recorded in [story.md](story.md) §8.4.

---

## Earlier runs

Lighthouse 13.6.0 measured the local static pages on 17 November 2026 at 23:27 and 23:28 Europe/Oslo. Both runs used the mobile form factor and simulated throttling.

| Metric | Bokmål | English |
|---|---:|---:|
| Performance score | 100/100 | 100/100 |
| Largest Contentful Paint | 1.38 s | 1.83 s |
| Cumulative Layout Shift | 0 | 0.00005 |
| Total Blocking Time | 74 ms | 58 ms |
| Image requests on initial load | 7 | 7 |
| Image transfer on initial load | 238,313 B | 238,313 B |
| Total transfer, rounded | 303 KiB | 303 KiB |

The observed LCP and CLS meet the project targets of 2.5 s and 0.1. These are lab runs against a loopback preview. Field interaction latency requires actual visitor data.

## Story page · D-22 (2026-11-18)

`/historien/` on Grok's story build, two Lighthouse 13.6.0 runs:

```powershell
npx lighthouse http://127.0.0.1:4322/historien/ --output=json --output-path=fase4/promo/qa/reports/lighthouse-story-page-mobile.json --chrome-flags="--headless=new --no-sandbox" --quiet
npx lighthouse http://127.0.0.1:4322/historien/ --preset=desktop --output=json --output-path=fase4/promo/qa/reports/lighthouse-story-page-desktop.json --chrome-flags="--headless=new --no-sandbox" --quiet
```

| | Phone (412) | Desktop (1350) |
|---|---:|---:|
| Performance | **100** | **100** |
| Accessibility / best practices / SEO | 100 / 100 / 100 | 100 / 100 / 100 |
| LCP | **0.8 s** | **0.2 s** |
| CLS | **0** | **0** |
| TBT | 0 ms | 0 ms |
| Transfer | 74 KB | 131 KB |
| JavaScript | 0 bytes | 0 bytes |

The story page is text and two images: no film, no script, and the two concept pictures are lazy-loaded. All four of D-22's gates pass (0 axe violations, LCP ≤ 2.5 s, CLS ≤ 0.1).

## Film performance · D-16 of task-film-v18 (2026-11-18)

Two Lighthouse 13.6.0 runs on the film build, against the local preview on 4322, system Node v22.22.0:

```powershell
npx lighthouse http://127.0.0.1:4322/ --output=json --output-path=fase4/promo/qa/reports/lighthouse-story-mobile.json --chrome-flags="--headless=new --no-sandbox" --quiet
npx lighthouse http://127.0.0.1:4322/ --preset=desktop --output=json --output-path=fase4/promo/qa/reports/lighthouse-story-desktop.json --chrome-flags="--headless=new --no-sandbox" --quiet
```

| | Phone (412 × 823, mobile emulation) | Desktop (1350 × 940) |
|---|---:|---:|
| Performance score | **100** | **100** |
| LCP | **1.7 s** | **0.4 s** |
| CLS | 0 | 0.009 |
| Largest paint | **the poster `img.film-still`** | **the poster `img.film-still`** |
| `load` event | 712 ms | 391 ms |
| Film requested at | 746 ms (after load) | 486 ms (after load) |
| Film bytes in the run | **2.29 MB** (`house-film.mp4`, 1280 × 720) | **5.84 MB** (1920 hero 3.76 + living 0.99 + bath 1.08) |
| Poster + images | 12 requests, 428 KB | 12 requests, 428 KB |

The largest paint is the poster image in both runs, so the page is readable before any film arrives; every film starts **after** the `load` event, which is what DESIGN-GUIDE §6.15 promises. The phone takes the 720p film and the desktop the 1080p one, exactly the split Carlos chose.

The desktop run pulls 5.84 MB of film, not the ~4.5 MB of the hero file alone: at 1350 px the living and bath loops are also within the load window. The hero file itself is **3.76 MB**, inside its 4.5 MB budget. All of it is lazy, so it does not delay LCP.

Reproduce with the local preview on port 4322 and the installed Lighthouse 13.6.0 CLI.

```powershell
npx lighthouse@13.6.0 http://127.0.0.1:4322/ --only-categories=performance --output=json --output-path=fase4/promo/05-test/reports/lighthouse-landing-nb.json --chrome-flags="--headless=new" --quiet
npx lighthouse@13.6.0 http://127.0.0.1:4322/en/ --only-categories=performance --output=json --output-path=fase4/promo/05-test/reports/lighthouse-landing-en.json --chrome-flags="--headless=new" --quiet
```

[Raw Bokmål report](reports/lighthouse-landing-nb.json) · [Raw English report](reports/lighthouse-landing-en.json)

## Earlier baseline with empty image slots

Task D-7 (PLAN 5.5). Run against the local preview on **http://localhost:4322/**, 2026-11-17 23:10–23:20. Build: `web/promo/dist` built 2026-11-17 22:36. Lighthouse 13.6.0, mobile form factor, simulated throttling, system Node v22.22.0.

**Result: every gate passes on this build — with a caveat that matters.** The page is fast because it holds no photography yet: 0 images, 0 bytes of JavaScript, two self-hosted WOFF2 fonts. The image round (Antigravity) and the form and gallery JavaScript (Cursor) can change this, so this run is a baseline, not a release certificate.

---

## 1 · Command

```powershell
npx --yes lighthouse http://localhost:4322/   --output=json --output-path=fase4/promo/05-test/reports/lighthouse-nb.json --chrome-flags="--headless=new --no-sandbox" --quiet
npx --yes lighthouse http://localhost:4322/en/ --output=json --output-path=fase4/promo/05-test/reports/lighthouse-en.json --chrome-flags="--headless=new --no-sandbox" --quiet
```

## 2 · Numbers

| Metric | Gate (PLAN 5.5) | `/` nb | `/en/` | Pass |
|---|---|---|---|---|
| Largest Contentful Paint | ≤ 2.5 s | **0.8 s** | **0.8 s** | yes |
| Cumulative Layout Shift | ≤ 0.1 | **0** | **0.004** | yes |
| Total Blocking Time (lab proxy for INP) | INP ≤ 200 ms | **0 ms** | **20 ms** | yes |
| JavaScript transfer | ≤ 50 KB gzipped | **0 bytes** | **0 bytes** | yes |
| First load, total transfer | ≤ 1.5 MB | **65 KiB** | **68 KiB** | yes |
| First Contentful Paint | – | 0.8 s | 0.8 s | – |
| Speed Index | – | 0.9 s | 0.8 s | – |
| Performance score | – | 100 | 100 | – |

Lighthouse reported 0 script requests on both pages: the Astro build ships no client JavaScript yet. The only third-party request is none — fonts are self-hosted (two preloaded WOFF2 for Besley 800 and Jost 400).

## 3 · What will move these numbers

- **Images (Antigravity, A-7/A-8):** the hero at 3:2, 2400 px, AVIF ≤ 180 KB, plus the gallery. LCP will follow the hero image; `fetchpriority="high"` and the width/height attributes are Cursor's tasks (4.4, 4.9).
- **JavaScript (Cursor, C-5/C-6):** the lightbox, tabs, menu sheet and the form's `fetch`. The ≤ 50 KB gate applies to all of it.
- **Form (Cursor, C-6, blocked on D6):** one network request on submit, not on load.
- Re-run both pages after each of those lands. The command and the gates do not change.

## 4 · Related console finding

Lighthouse logged one console error on both pages: `GET /favicon.ico` → **404**. Minor, but it is the only console error on the site and it is Cursor's to fix (an icon in `public/`, or a `<link rel="icon">`).

## 5 · Status

| Item | State |
|---|---|
| Run | done, 2 pages, 2 JSON reports in `reports/` |
| Gates | all pass on this build |
| Caveat | no images and no JavaScript yet |
| Owner of the next change | Cursor (JS, favicon), Antigravity (images) |
| Re-run | after the image and JS work, before G5 |
