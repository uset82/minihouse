# MiniHouse promo site

Static Astro site for the promotional website. Plain CSS, no React, no Tailwind.

Astro is pinned to 7.4.1. Astro 7.4.2 and later refuse Node 22.22.0, which is the system Node this project uses. Install dependencies with `NODE_ENV` unset so the dev dependencies (`typescript`, `@astrojs/check`) are included.

Commands, from this directory, with the system Node (`C:\Program Files\nodejs`):

| Command | What it does |
| --- | --- |
| `npm run dev` | Dev server on port 4321 |
| `npm run check` | Typecheck and content contract |
| `npm run build` | Development build. Stand-in images are allowed. |
| `npm run build:release` | Fails while copy is `TODO` or any image is not `approved` |
| `npm run preview -- --port 4322` | Preview a build |

`src/content/nb.json` and `en.json` belong to DeepSeek after the content handover. `src/content/images.json` and `src/assets/images/` belong to Antigravity after the image handover. `schema.ts` stays with Cursor.
