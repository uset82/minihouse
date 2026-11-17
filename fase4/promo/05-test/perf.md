# Performance · D13 photo landing

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
