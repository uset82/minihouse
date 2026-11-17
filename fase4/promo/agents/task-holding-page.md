# Task · Holding page for minihouse.canner.app

2026-11-17. Approved by Carlos («Yes, holding page», [decisions.md](../decisions.md)). **Owner: Cursor** (build and deploy). Review: Antigravity (screenshots after the deploy). Copy check: DeepSeek (doesn't block the deploy).

## Why

The main address shows Antigravity's engineering app to anyone who visits. That app shows:

- deflections from a hypothetical beam example;
- an invented "2750 mm clear height";
- a claim that the cabin is "engineered to be lifted";
- an AI chat that needs the visitor's own key.

Until the promo site launches (G5), the address shows one quiet, honest page instead.

## What it is

One static HTML page. No JavaScript, no images (none is approved yet; that's G4) and no external requests. Every sentence on it comes from the [claims register](../02-define/claims-register.csv).

## Copy: claims-register wording only

Norwegian (`<html lang="nb">`):

| Element | Text | Claim |
|---|---|---|
| h1 | MiniHouse | wordmark |
| p | Et lite hus på ca. 6 × 3 m, med stålramme og gjenbrukt tre. | K-01, K-03 |
| p | Huset er under utvikling. | K-19 |
| p | Målet er at huset skal kunne flyttes i ett stykke. | K-05 |
| p | Laget for Bergen og Vestlandet. | K-13 |

English block (`lang="en"`), below the hairline:

| Text | Claim |
|---|---|
| A small house of about 6 × 3 m, with a steel frame and reclaimed timber. | K-01, K-03 |
| The house is under development. | K-19 |
| The goal is to move the house in one piece. | K-05 |
| Made for Bergen and Western Norway. | K-13 |

Footer link: «For fagfolk: prosjektdokumentasjon» / "For professionals: project documentation", pointing to https://minihouse-docs.canner.app (K-28).

The `<head>`:

- `<title>MiniHouse</title>`.
- Meta description: «Et lite hus på ca. 6 × 3 m, med stålramme og gjenbrukt tre. Huset er under utvikling.»
- `<meta name="robots" content="noindex">`, on **this page only**. Never carry it into `web/promo`.

**Not on the page:**

- a contact address (K-29 is open);
- the interest form (D6 is open);
- prices, dates or images;
- any "[CONCEPTUAL]" badge;
- anything from the engineering app.

## Design (DESIGN-GUIDE R1.1)

```
┌────────────────────────────────────────┐
│                                        │
│ MiniHouse                              │  Besley 800, --size-h1 (the one bold thing)
│                                        │
│ Et lite hus på ca. 6 × 3 m, med        │  Jost 400, --size-lead
│ stålramme og gjenbrukt tre.            │
│ Huset er under utvikling.              │
│ Målet er at huset skal kunne flyttes   │
│ i ett stykke.                          │
│ Laget for Bergen og Vestlandet.        │
│ ──────────────────────────────         │  1 px --solvgra hairline, --space-5 above
│ A small house of about 6 × 3 m, …      │  Jost 400, --size-body, lang="en"
│                                        │
├──────────── --tjaere band ─────────────┤
│ For fagfolk: prosjektdokumentasjon     │  --kobber-lys link: the only copper
└────────────────────────────────────────┘
```

- **Tokens:** copy `tokens.css` verbatim. The ground is `--kalk` and the text `--tjaere`.
- **Layout:** left-aligned, `max-width: var(--measure)`, `--gutter` side margins, top padding `--space-6`, and `--space-7` from `80rem` up.
- **Footer:** a full-width `--tjaere` band with `--space-6` padding. The link takes the guide's underline and `--focus-ring-dark`.
- **Fonts:** the same self-hosted Besley 800 and Jost 400 WOFF2 files as `web/promo`, copied in. No CDN.
- **Garbage list:** nothing from DESIGN-GUIDE §10. No badges, eyebrow labels, arrows, shadows or icons.

## Steps (Cursor)

1. Create `web/promo-holding/` with `index.html`, `holding.css` (the verbatim tokens plus the page rules) and `fonts/`. Nothing else.
2. Check it at a real 360 px and 1280 px viewport. Save `holding-360.png` and `holding-1280.png` in `fase4/promo/status/cursor-screens/`.
3. If DeepSeek's `scripts/check_promo.py` exists, run it on the folder. Otherwise check by hand: no external requests, `lang` set, exactly one `<h1>`, the link works, the focus ring is visible.
4. From `web/promo-holding/`, run `canner deploy --slug=minihouse --follow`. Carlos approved this deploy.
5. Check the live site:
   - `/` shows the holding page.
   - `/diario.html` and `/static/js/main.167ace0f.js` no longer serve the engineering app. Expect the holding page with status 200, because of Canner's single-page fallback.
   - The docs link returns 200.
6. Log the work in `status/cursor.md`, ending with "→ Antigravity: holding page live, please review".

## The engineering app: don't redeploy it yet

This deploy takes the app offline, and that's intended. Before it's ever deployed again (to minihouse-lab in C-11, which needs Carlos's own yes), fix these in `web/chat-demo`. Those files carry uncommitted work from another session, so edit minimally.

- **`src/components/minihouse/MiniHouse3DSimulator.tsx`, "2750 mm clear height":** this figure is invented. R0 gives 2400 mm ([geometría R0](../../../fase1/geometria-R0.md), S-02), and the room-height check shows that even 2.2 m is hard to reach. Write "clear height TBD (R0 assumption 2400 mm)".
- **The intro, "engineered to be lifted by crane … without permanent deformation":** no engineering has been done yet. Write "designed to be lifted by crane … (engineering in progress)".
- **The HTML template (`src/index.html`), `lang="zh-CN"`:** change it to `lang="en"`.

## Done when

- [ ] The live `/` shows the holding page, checked at 360 px and 1280 px.
- [ ] No image, form or contact details, and no sentence outside the claims above.
- [ ] `noindex` is on the holding page and absent from `web/promo`.
- [ ] Antigravity's review has no open critical or serious findings.
- [ ] The engineering app stays offline until the three fixes above are in and Carlos says yes to minihouse-lab.
