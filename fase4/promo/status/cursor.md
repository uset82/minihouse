# Status · Cursor

Only Cursor writes this file; the other agents and Carlos read it. Put the newest entry at the top of the log. Brief: [agents/cursor.md](../agents/cursor.md). Protocol: [agents/README.md §5](../agents/README.md).

## Requests to other agents

Open requests go here, one line each, for example "→ DeepSeek: …". Mark them done when they're answered.

- → Carlos: C-1 deploy is live (`5c9f96bf`). The concept JPEG is gone, but Canner's static-spa fallback answers `/concepts/hero-nordic.jpg` with status 200 and the HTML shell, not 404. Done as far as the upload can go.
- → Carlos: DESIGN-GUIDE §5 asks for 20 px side margins at 360 px. There is no token for 20 px, and `tokens.css` has to stay verbatim, so the page uses `--gutter` (24 px). Say if that should change. **Answered 2026-11-17:** R1.1 sets side margins to `--gutter` at every width. Done.
- → DeepSeek: D1 is now «Følg prosjektet». Removed keys were `interest.price` and `interest.fields.municipality`, `use`, `useOptions`, `timeline`, `timelineOptions`, `message`. **Done:** both JSON files already match.
- → DeepSeek: HANDOVER content. `web/promo/src/content/nb.json` and `en.json` are yours. Every string is `TODO`. Stable ids, not copy: materials `malmfuru`, `eik`, `kobber`, `stal`; rooms `kitchen`, `bench`, `storage`, `bath`. Array lengths are placeholders (5 facts, 4 materials, 4 rooms, 3 journey steps, 5 phases, 1 FAQ, 1 option in each radio list). You can change those lengths. Missing keys fail `npm run check`.
- → Antigravity: HANDOVER images. `web/promo/src/content/images.json` and `web/promo/src/assets/images/` are yours. All 19 ids are present, `file` is null, `status` is `stand-in`, alt text is `TODO`. Do not put container renders in the site.
- → Antigravity: holding page live, please review. https://minihouse.canner.app (deployment `f3dece04`). A first pass is in `review/visual-review.md`. Screenshots are in `status/cursor-screens/`.
- → Antigravity: VR-01 is done. VR-02 stays unmounted until D6. «Følg prosjektet» has no form yet, and the privacy page says this preview does not collect an e-mail. The component is still in `src/components/StickyBar.astro`.
- → DeepSeek: `npm run check` passed (0 diagnostics) and `python scripts/check_promo.py` passed on the source and on `web/promo/dist` (5 pages, 18 images on each home page).
- → DeepSeek: D-7 items: irr captions are `--kalk`; `/favicon.ico` returns 200; `/personvern/` and `/en/personvern/` return 200; `hreflang` is absolute (`https://minihouse.canner.app/` and `/en/`). A Lighthouse run against the preview still cannot confirm the return tag on the live host, because that host is the holding page. New keys for you to revise: `notFound.title`, `notFound.body`, `notFound.home`.
- → Carlos: a missing path on the current Canner upload returns the home HTML with status 200. The promo build now includes `404.html`, but that host has not been shown to serve it as a real 404. The follow form is still waiting on D6.
- → Antigravity: the workshop step uses the 288×144 master at its own width. On the 1280 layout it is 288×144; the truck and hillside share that 144 px height and are not cropped. At 360 px each picture sits beside the step text at 106 px wide. Screenshots: `status/cursor-screens/journey-360.png` (360×1100) and `journey-1280.png` (1280×860). No sideways overflow.
- → DeepSeek: rebuilt after the kitchen, bench and storage copy. `npm run check` is 0 diagnostics. `check_promo.py` passed on the source and on `web/promo/dist` (5 pages, 18 images, 1485 words, 0 TODO).
- → DeepSeek: the usability preview is on the LAN. On this Wi-Fi the address is http://10.0.0.24:4322/ (also http://localhost:4322/). Task T5 has no form while D6 is open.
- → DeepSeek: Patentstyret search is in `05-test/claims-audit.md` §5. Exact `MiniHouse` is 0 varemerker, 0 patenter, 0 design. The two-word search is a different query and its listed marks are other names.

## Log

### 2026-11-18 00:28 · Name check and LAN preview · done
Files: `fase4/promo/05-test/claims-audit.md` §5 and the fix list. No page change.
Plan (DESIGN-GUIDE §1, step 2): no layout. The name check was the open G5 item assigned here, and the usability script asks for a preview the phone can open.
Evidence: Patentstyret simple search `MiniHouse` on 2026-11-18 returned varemerke 0, patent 0, design 0 (`https://search.patentstyret.no/advanced/#/?cs=MiniHouse`). `mini house` returned 44 varemerker whose mark texts are other names. The built pages already contain the current kitchen, workshop and status sentences, so fix-list item 3 is closed. Preview: `npm run preview -- --port 4322 --host`. http://10.0.0.24:4322/en/ returned 200 from this PC.
BLOCKED: the follow form, and usability task T5, until D6. Launch until G5. No deploy.
Next: DeepSeek re-runs the built-page audit. Carlos can open the Wi-Fi address on a phone on this network.

### 2026-11-17 23:44 · Journey picture sizing · done
Files: `web/promo/src/components/Journey.astro`, `web/promo/src/components/Figure.astro`.
Plan (DESIGN-GUIDE §1, step 2): the workshop master is 288×144. Each journey figure keeps its own aspect ratio and stops at its master width (`max-inline-size: min(100%, {width}px)`). From 48rem the three steps share one band and a common picture height of `--space-7 + 2 * --space-4` (144 px) without cropping. Below that, the picture sits beside the numeral and the sentence. VR-02 stays unmounted; the disposition is in `05-test/changelog.md`.
Evidence: `npm run build` 5 pages. Measured pictures at 1280: workshop 288×144, truck 192×144, plot 256×144. At 360 each picture is 106 px wide. `scrollWidth` matched the viewport at both widths. `npm run check` 0 diagnostics. `check_promo.py` source and `--dist` passed. Screenshots `status/cursor-screens/journey-360.png` (360×1100) and `journey-1280.png` (1280×860).
Definition of done (DESIGN-GUIDE §11): [x] tokens and §3 literals [x] copper not used on this band [x] copy from the content files [x] pictures from `images.json` [x] no new controls [x] no new motion [x] 360 and 1280 screenshots [x] garbage list clear [x] one accessory removed: the 4:3 crop that enlarged the workshop panel [ ] Antigravity's look at the new crop is open
BLOCKED: C-6 form until D6. C-11 launch until G5. `build:release` still fails while images are stand-in or pending.
Next: Antigravity reviews the journey frames. No deploy.

### 2026-11-17 23:27 · C-8 SEO, 404, sticky bar, images on the page · done
Files: `web/promo/src/layouts/Base.astro`, `src/components/StickyBar.astro`, `src/pages/404.astro`, `src/styles/base.css`, `astro.config.mjs`, `public/robots.txt`, `public/favicon.ico`, `src/content/schema.ts`, `scripts/content-contract.mjs`, `nb.json`, `en.json` (only the new `notFound` keys).
Plan (DESIGN-GUIDE §1, step 2): sticky bar is kalk, 1 px sølvgrå top border, full-width copper button, hidden while the hero or `#folg` is on screen, and hidden from 64rem. It uses `env(safe-area-inset-bottom)`. Open Graph, Twitter and Organization JSON-LD use the content files and `og-image.jpg`, with no price. `hreflang` is absolute. Irr captions stay `--kalk`.
Evidence: `npm run build` → 5 pages, sitemap-index.xml, AVIF and WebP, `fetchpriority` on the hero. Preview: favicon 200 `image/x-icon`, `/personvern/` 200. Screenshots `c8-360.png` is 360×800 and `c8-1280.png` is 1280×900; the hero picture is the house, and the sticky bar is not covering the hero. Canner's earlier upload of the holding page answered missing paths with status 200. `404.html` is in this build and has not been uploaded.
Definition of done (DESIGN-GUIDE §11): [x] tokens and §3 literals, plus the safe-area inset the guide names [x] copper only on the button and links [x] new 404 sentences are in the content files [x] pictures come from `images.json` through `<Picture>` [x] sticky bar is a link [x] no new motion [x] 360 and 1280 screenshots [x] garbage list clear [x] one accessory removed: no second button in the sticky bar [ ] Antigravity's review of the pictures is open
BLOCKED: the follow form still waits on D6. Launch still waits on G5.
Next: C-10 when a review names a fix. C-9's widths and formats are in this build; `build:release` still fails while any image is `stand-in` or `pending`.

### 2026-11-17 · Concept landing page · Codex supervision

The first screen pairs the approved D12 headline in Besley with the fjord-side house image. The copper action opens the pictures. A second action leads to the reclaimed wood and its material passports. The page uses the existing chalk, oak, tar and verdigris colours, with image-led spreads at wide widths and a single reading column at 360 px. D13 makes the cabin, living space and materials the subject of the landing page. Sign-up controls stay hidden while D6 is open.

Cursor Agent edited the hero, header, footer and base layout in its local CLI. Codex integrated those changes with the final DeepSeek copy and Antigravity masters, fixed language links, tested the mobile dialog and removed the unavailable sticky follow action from the layout. The pictures use Astro's responsive AVIF, WebP and JPEG exports. Each homepage contains 18 captioned figures. The gallery has three views and a keyboard-controlled lightbox. Material passport details open using Enter or Space. The mobile and desktop gallery now share one set of tiles.

Verified on the 23:29:47 local build with `npm run check` (zero diagnostics), `npm run build` (five pages) and `python scripts/check_promo.py --dist web/promo/dist` (all checks passed). Bokmål and English titles, descriptions, bathroom and steel copy in the HTTP response match the two final content files. Both menus open and close with Escape, focus returns to the opener, and the lightbox advances from view one to view two with the arrow key. Both widths had zero horizontal overflow and zero placeholder figures. The preview returns a 404 status for a missing page and its language links work.

Opening views in [Bokmål at 360 px](cursor-screens/concept-nb-360.png), [Bokmål at 1280 px](cursor-screens/concept-nb-1280.png), [English at 360 px](cursor-screens/concept-en-360.png) and [English at 1280 px](cursor-screens/concept-en-1280.png). [Material passport on mobile](cursor-screens/concept-material-nb-360.png) and [desktop](cursor-screens/concept-material-en-1280.png). Antigravity independently confirmed that the sticky control is gone from both phone layouts and that the material images remain visible. See the [visual review](../review/visual-review.md). The image approval register and form destination remain open for publication. The local preview is available at http://127.0.0.1:4322/.

### 2026-11-17 23:12 · C-6 status, FAQ and privacy · form blocked
Files: `web/promo/src/components/StatusFaq.astro`, `src/pages/personvern.astro`, `src/pages/en/personvern.astro`.
Plan (DESIGN-GUIDE §1, step 2): status is a short paragraph plus phase name and state, with spacing instead of a ruled table. FAQ summaries are Jost 500 at `--size-lead` with a copper + / − on the summary, which is the control. Privacy is one measured paragraph on kalk. The follow form is not on the page.
Evidence: both privacy routes built. FAQ questions are buttons. D6 still has no inbox or form service, so the form is not posted and no success state is faked.
Definition of done (DESIGN-GUIDE §11): [x] tokens only [x] copper only on the FAQ marker [x] copy from the content files [x] no new images [x] summaries are buttons [x] no motion [x] included in the 360 and 1280 screenshots [x] garbage list clear [x] one accessory removed: no rules between the phase rows [ ] Antigravity's review is open
BLOCKED: the interest form stays blocked until D6 names the inbox and the form service.
Next: C-7 is partly in place (both languages, hreflang, the language link keeps the hash). Image alt texts are still `TODO`.

### 2026-11-17 23:12 · Gallery, build tabs, living, journey · ready for review
Files: `Gallery.astro`, `BuildTabs.astro`, `Living.astro`, `Journey.astro`, `Figure.astro`, `src/styles/base.css`, both home pages. `hreflang` links added in `Base.astro`.
Plan (DESIGN-GUIDE §1, step 2): gallery is a mobile scroll-snap strip with «{current} av {total}», and from 48rem a wall of 4:5 tiles with `--space-2` gaps plus wide 3:2 rows. Lightbox is a dialog on `color-mix(in srgb, var(--tjaere) 92%, transparent)`, image contained, controls in `--kobber-lys`, Esc, arrows and swipe. Tabs use a 3 px copper underline. Living is an irr band, text in kalk. Journey numerals are Besley 800 at `--size-h1` in `--malmfuru`.
Evidence: `npm run build` → 4 pages. Lightbox opens from a tile and Lukk returns focus to that tile. The Konstruksjon tab becomes selected. Screenshots: `status/cursor-screens/c5-360.png` is 360×6400, `c5-1280.png` is 1280×4200. Preview http://127.0.0.1:4322/ .
Definition of done (DESIGN-GUIDE §11): [x] tokens and §3 literals only [x] copper only on controls [x] copy from the content files; «Bilde kommer» / "Image coming" is the missing-image label [x] every figure reads `images.json` [x] lightbox and tabs are keyboard controls [x] reduced motion clears transitions [x] 360 and 1280 screenshots [x] garbage list clear [x] one accessory removed: the image count is only on the mobile strip [ ] Antigravity's review is open
ready for review: gallery, tabs, living, journey, with the earlier header, hero, facts, footer and passport.
Next: C-6 form, blocked on D6.

### 2026-11-17 22:36 · C-5 material passport · ready for review
Files: `web/promo/src/components/Materials.astro`, `Figure.astro`, `src/styles/base.css`.
Plan (DESIGN-GUIDE §1, step 2): same structure as `reference/tile-a.css`. Sample 4:5 at 60% width on mobile, then the name in Besley 800 at `--size-h3`, one lead, then the tag. The tag is a `--space-5` stub, 1 px dashed perforation, 10 px eyelet with a 2 px ring, «Materialpass» in Jost 500 at `--size-small`, and a `<dl>` with the six rows. Labels `--malmfuru-mork`, values `--tjaere`, no row hairlines. From 48rem the sample is about a third of the row (`4fr` / `7fr`); eik and stål swap sides. All four materials come from `nb.json` / `en.json`.
Evidence: built with C-4. Passport rows match the content files. Missing textures show the eik «Bilde kommer» block.
Definition of done (DESIGN-GUIDE §11): [x] tokens and the §3 literals only [x] allowed pairs; copper is not used on the tag [x] copy from the content files; «Bilde kommer» is the missing-image label from the image contract [x] figure reads `images.json` [x] no extra controls [x] no motion [x] 360 and 1280 screenshots [x] garbage list clear [x] one accessory removed: the hairline under each passport row, as in the reference [ ] Antigravity's review is open
ready for review: material passport, with header, hero, facts and footer.
Next: C-6 is blocked on D6.

### 2026-11-17 22:36 · C-4 header, hero, key facts, footer · ready for review
Files: `web/promo/src/components/SiteHeader.astro`, `Hero.astro`, `KeyFacts.astro`, `SiteFooter.astro`, `layouts/Base.astro`, `pages/index.astro`, `pages/en/index.astro`, `src/styles/base.css`.
Plan (DESIGN-GUIDE §1, step 2): copied the reference structure. Header: wordmark Besley 800 at `--size-h3`, nav hidden until 64rem, «Meny» opens a full-screen kalk sheet, «Lukk» and Esc return focus to the button. Hero splits at 64rem and the figure bleeds to the right edge. Facts are an eik band, rows on mobile and 5 columns with 1 px tjære hairlines from 48rem. Footer is the tjære band with the image note, Personvern, For fagfolk (docs site) and the language link. The 3D lab is not linked; it is not live (K-28).
Evidence: `npm run check` 0 errors, content check passed. `npm run build` 2 pages. Screenshots from device emulation, confirmed by pixel size: `status/cursor-screens/c4-360.png` is 360×4200, `c4-1280.png` is 1280×2400. At 360 the interactive tree shows Meny and not the desktop nav. Opening Meny focuses Lukk; Escape closes it and returns focus to Meny. Preview: http://127.0.0.1:4322/ . «Se alle bildene» points at `#bilder`, which is not built yet.
Definition of done (DESIGN-GUIDE §11): [x] tokens and the §3 literals only (48/64/80rem, 1–3 px lines, 10 px eyelet, 48 px targets, -0.01em, aspect ratios, fr) [x] copper only on links, the button and the focus ring [x] copy from `nb.json` and `en.json` [x] images from `images.json`; missing files are the eik block [x] keyboard: menu opens, Esc closes, focus returns [x] reduced motion removes transitions [x] 360 and 1280 screenshots looked at; no sideways overflow [x] garbage list clear [x] one accessory removed: no visible heading on the facts band [ ] Antigravity's review is open
ready for review: header, hero, facts, footer.
Next: C-5

### 2026-11-17 21:58 · Content schema · follow form · done
Files: `web/promo/src/content/schema.ts`, `web/promo/scripts/content-contract.mjs`. Did not edit `nb.json` or `en.json`.
Plan (DESIGN-GUIDE §1, step 2): no layout. D1 is «Følg prosjektet». The form collects e-post (required) and navn (optional). Consent is one string, shown later as an unticked checkbox.
Evidence: `npm run check` → astro check 0 errors, content check passed. The JSON files still contain the removed keys; the checker only requires the keys that remain.
HANDOVER / ready for review / BLOCKED: → DeepSeek: remove the keys listed under Requests and rewrite the follow-form strings.
Next: C-4

### 2026-11-17 21:55 · C-1b holding page · done
Files: `web/promo-holding/index.html`, `holding.css`, `fonts/besley-latin-800-normal.woff2`, `fonts/jost-latin-400-normal.woff2`. Source-only fixes, not deployed: `web/chat-demo/src/components/minihouse/MiniHouse3DSimulator.tsx` (clear height TBD, R0 assumption 2400 mm), `MiniHouseFrontPage.tsx` ("designed to be lifted… (engineering in progress)"), `src/index.html` (`lang="en"`). Review note: `fase4/promo/review/visual-review.md`.
Plan (DESIGN-GUIDE §1, step 2): one quiet page. `--kalk` ground, `--tjaere` text, Besley 800 at `--size-h1`, Norwegian lead at `--size-lead`, English at `--size-body`, 1 px `--solvgra` hairline with `--space-5` above it, footer `--tjaere` with `--space-6` padding and `--kobber-lys` links. Top padding `--space-6`, `--space-7` from `80rem`. Side margins `--gutter`. Tokens in `holding.css` match DESIGN-GUIDE §3 (byte check). Removed a skip link: the diagram has no navigation, and the footer links are the only controls.
Evidence: `scripts/check_promo.py` does not exist, so the check was by hand: no `<script>`, no `<img>`, one `<h1>`, `lang="nb"`, an English block with `lang="en"`, `noindex` present, and the only external URL is the docs link. Local screenshots at real widths: `status/cursor-screens/holding-360.png` (360×1400) and `holding-1280.png` (1280×900). At 360 px, `innerWidth` and the footer were both 360, `scrollWidth` was 360, the h1 was 44 px Besley, and the first sentence breaks before "stålramme", not inside the word. `canner deploy --slug=minihouse --follow` from `web/promo-holding/` → deployment `f3dece04`, health check OK. Live `/` is the holding page (200, the development sentence, `noindex`, no engineering bundle). `/diario.html` and `/static/js/main.167ace0f.js` return that same HTML with status 200, not the app. https://minihouse-docs.canner.app returns 200. Live screenshots: `holding-live-360.png` (360×1400), `holding-live-768.png` (768×1100), `holding-live-1280.png` (1280×900), `holding-live-1920.png` (1920×1080). The engineering app was not redeployed. `noindex` is absent from `web/promo`.
Definition of done (DESIGN-GUIDE §11, for anything visual): [x] tokens only, plus the allowed literals in §3 (80rem, 1 px line, 3 px underline offset, 48 px touch target, percentages) [x] allowed pairs; copper only on the footer links [x] copy is the task's claim sentences [x] no images [x] the links are the only controls; focus ring is `--focus-ring-dark` [x] no motion [x] 360 and 1280 screenshots, plus 768 and 1920 of the live page [x] garbage list clear [x] one accessory removed: the skip link [ ] Antigravity's own confirmation is still open
HANDOVER / ready for review / BLOCKED: → Antigravity: holding page live, please review.
Next: C-4 after that review, unless you say to start it now.

### 2026-11-17 21:11 · C-1 deployed · done
Files: uploaded `web/chat-demo/dist` only. No source edits in this step.
Plan (DESIGN-GUIDE §1, step 2): not a promo section. Remove the container pictures from the live site.
Evidence: `canner deploy --slug=minihouse --follow` from `web/chat-demo/dist` → deployment `5c9f96bf`, health check OK, live at https://minihouse.canner.app. `dist/concepts` was absent and the bundle has no `concepts/` path. Live `main.167ace0f.js`: `hero-nordic` false, `concepts/` false, `U-0.15` false, "Concept pictures withdrawn" true. `GET /concepts/hero-nordic.jpg` (and the other two JPEGs) returns **200** `text/html` (458 bytes, `<!doctype html>`), not 404. `Cache-Control: no-cache`. Same with a cache-busting query. Canner's build log called the bundle `static-spa`, so an unknown path falls back to `index.html`. `framework_override` is already `static`. Did not run `canner redeploy`.
Definition of done (DESIGN-GUIDE §11, for anything visual): the container picture is not served. The status-code check in the brief is not met, because the platform answers missing files with the app shell.
HANDOVER / ready for review / BLOCKED: deployed. The 404 itself is blocked on Canner's SPA fallback.
Next: C-4

### 2026-11-17 20:57 · C-3 tokens, fonts, base layout · done
Files: `web/promo/src/styles/tokens.css` (verbatim from DESIGN-GUIDE §3; compared equal to the guide's code block), `fonts.css`, `base.css`, `src/layouts/Base.astro`, `src/pages/index.astro`, `src/pages/en/index.astro`. Fonts: `@fontsource/besley` and `@fontsource/jost`, Latin WOFF2 only in the build.
Plan (DESIGN-GUIDE §1, step 2): page ground `--kalk`, text `--tjaere`, footer `--tjaere` with `--kalk` text, skip link `--kobber` on `--kalk`. Display Besley 800 at `--size-h1` / `--size-h3` for the wordmark. Body Jost 400 at `--size-body`, lead at `--size-lead`, measure `--measure`. Bands use `--space-6` padding, `--space-7` from 80 rem (1280 px). No header rule. This is the shell, not the hero (C-4).
Evidence: `npm run check` → 0 errors, content check passed. `npm run build` → `/` and `/en/`. Besley 800 preload URL matches the `@font-face` file (`occurrences: 2`). No Google Fonts request. fontTools: Besley 800 and Jost 400 contain æøå, «», × and ²; Jost has `tnum`, so Albert Sans is not needed. At 360 px: viewport and footer both 360, no horizontal overflow, h1 44 px Besley left-aligned, wordmark 24 px tjære, body 18 px Jost. At 1280 px: footer 1280, band padding 96 px, h1 72 px. `/en/` has `lang="en"` and the wordmark points at `/en/`. Screenshots: `c:\Users\carlos\AppData\Local\Temp\cursor\screenshots\promo-foundation-360.png` and `promo-foundation-1280.png`. The preview document never took window focus (`document.hasFocus()` stayed false), so the `:focus` reveal of the skip link could not be seen; the built rule is `.skip-link:focus{transform:none}`. Preview on 4322 was stopped. Not a section review.
Definition of done (DESIGN-GUIDE §11, for anything visual): [x] tokens only, except `80rem` (the desktop breakpoint; no token exists), `letter-spacing: -0.01em` (§4), and `translateY(-200%)` on the skip link [x] allowed pairs; copper only on the skip link and the focus ring [x] visible sentences come from the content files; the wordmark is the literal "MiniHouse" from §6.2 [x] no images on the page [x] skip link then wordmark; focus ring is `--focus-ring` [x] no motion besides the token `--dur: 0ms` under reduced motion [x] 360 and 1280 screenshots looked at; no overflow [x] garbage list clear [x] one accessory removed: a hairline under the header [ ] Antigravity review — not requested; this is not "ready for review"
HANDOVER / ready for review / BLOCKED: not ready for review. Copy is still `TODO`.
Next: C-4, after you say so. The hotfix deploy is still waiting on your yes.

### 2026-11-17 20:48 · C-2 scaffold web/promo · done
Files: `web/promo/**` (scaffold, `src/content/schema.ts`, `nb.json`, `en.json`, `images.ts`, `images.json`, `assert-content.ts`, `assert-images.ts`, `scripts/check-content.mjs`, `scripts/release-check.mjs`, `scripts/content-contract.mjs`). Did not edit `pnpm-workspace.yaml` or the root `package.json`.
Plan (DESIGN-GUIDE §1, step 2): no visual section yet. Stack is Astro, TypeScript strict, plain CSS. Content and image files are data only.
Evidence: WebDesigner `wd_intake_project` (task-956869) selected Next.js, which this brief forbids, so the scaffolder was not run. `npm create astro@latest web/promo -- --template minimal --install --no-git --no-ai --yes` on system Node v22.22.0. Astro 7.4.12 refuses that Node (`>=22.23.4`), so Astro is pinned to 7.4.1, the newest 7.x whose CLI accepts `>=22.22.0`. `npm run check` → astro check 0 errors, content check passed. `npm run build` → `/` and `/en/` in 494ms. `npm run build:release` exits 1 on stand-in images and missing files, as the contract requires. Removed the Astro logo favicons from `public/`.
Definition of done (DESIGN-GUIDE §11, for anything visual): not a designed section. [x] copy placeholders only in the JSON files [x] images.json has every id and no picture file
HANDOVER content: DeepSeek owns `nb.json` and `en.json` from now on. HANDOVER images: Antigravity owns `images.json` and `src/assets/images/` from now on. Cursor keeps `schema.ts` and `images.ts`.
Next: C-3

### 2026-11-17 20:35 · C-1 hotfix prepared, not deployed · done
Files: `web/chat-demo/src/components/minihouse/MiniHouseFrontPage.tsx` (removed the three `concepts/*.jpg` fields and the `<img>`; left the existing card copy), `fase4/promo/archive/rejected-renders/` (`hero-nordic.jpg`, `3d-lifting-sim.jpg`, `exploded-materials.jpg`, `README.md`). Empty `web/chat-demo/public/concepts/` removed.
Plan (DESIGN-GUIDE §1, step 2): not a promo section. Neutral text panel in place of the pictures. No substitute render.
Evidence: system Node v22.22.0. `node node_modules\@rspack\cli\bin\rspack.js build -c rspack.config.ts` with `NODE_ENV=production` → compiled in 3.43s. `dist/concepts` absent. No `hero-nordic`, `3d-lifting-sim`, `exploded-materials`, or `concepts/` in `dist` JS. `npx vitest run` → 2 files, 8 tests passed. `npx tsc -p tsconfig.json` → exit 0. Deploy was not run.
Definition of done (DESIGN-GUIDE §11, for anything visual): not the promo site. The live URL still returns the old images until Carlos approves the deploy.
HANDOVER / ready for review / BLOCKED: prepared only. Blocked on Carlos's yes before `canner deploy --slug=minihouse --follow`.
Next: C-2

```text
### YYYY-MM-DD HH:MM · C-3 tokens and fonts · done | in progress | BLOCKED
Files: …
Plan (DESIGN-GUIDE §1, step 2): tokens, sizes and layout used …
Evidence: commands run and results, screenshot paths …
Definition of done (DESIGN-GUIDE §11, for anything visual): [ ] tokens only  [ ] allowed pairs  [ ] copy from content files  [ ] images from images.json  [ ] keyboard  [ ] reduced motion  [ ] 360/1280 screenshots  [ ] garbage list clear  [ ] one accessory removed: …
HANDOVER / ready for review / BLOCKED: …
Next: C-…
```
