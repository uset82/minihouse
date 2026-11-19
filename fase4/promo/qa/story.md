# Story page · claims audit and checks

Task D-22 ([task-story-page.md](../agents/task-story-page.md)). 2026-11-18, build from Grok's G-5 (`web/promo/dist`, 7 pages), served on <http://127.0.0.1:4322/>. Tools: axe-core 4.14.1, Lighthouse 13.6.0, curl 8.x, system Node v22.22.0.

**Result: no unsupported claim on either story page.** Every sentence traces to a row in [claims-register.csv](../content/claims-register.csv), every Carlos paragraph is verbatim ([copy-story.md](../content/copy-story.md)), the one external link answers 200, axe finds 0 violations and both Lighthouse runs are clean.

---

## 1 · Claims audit, sentence by sentence

The page renders exactly the strings in `nb.json` / `en.json`; the strings were compared with Carlos's Appendix A (34 of 34 verbatim) in D-18. So this audit maps each rendered block to its claim row.

| Section | Rendered text | Row | Verdict |
|---|---|---|---|
| Header | «Historien» / "The story" (`nav.story`) | – | navigation, not a claim |
| Title | «Hvordan ideen oppstod» | – | Carlos's own title |
| Byline | «Av Carlos» / "By Carlos" | – | his chosen byline |
| Lead | «Jeg ønsker å se nærmere på …» | – | Carlos's own view |
| Intro 1 | «I 2026 var jeg med på rivingen … Øvsttunvegen 21 i Bergen.» | **K-36** | verified: reference page confirms the 2026 demolition |
| Intro 2 | «Det var en vakker, gammel bygning … arkitektoniske uttrykk og form.» | **K-38** | verified: the permit condition on the reference page |
| Intro 3 | «Et av målene med prosjektet var å gjenbruke så mye som mulig …» | **K-39** | verified: 52 % reuse, 43 t materials, 46 t stone on the page |
| Reference | «Prosjektreferanse:» + «totalbyggoganlegg.no/ovsttunvegen» | **K-37** | link answers 200 (§2) |
| Noticed 1 | «Arbeidet med rivingen fikk meg til å se på byggavfall …» | – | Carlos's own view |
| Noticed 2 | «Etter hvert som vi demonterte bygningen … kunne brukes videre.» | **K-37** | the timber he observed during the documented demolition |
| Noticed 3 | «Jeg syntes det var synd …» | – | Carlos's own view |
| Noticed 4 | «Denne opplevelsen fikk meg til å stille meg selv et enkelt spørsmål:» | **K-44** | kept sentence 3 |
| Question | «Hvorfor skal materialenes levetid ta slutt …?» | – | Carlos's own question |
| Follow-up | «Hva om vi kunne ta vare på disse materialene …?» | – | Carlos's own view |
| Origin | «Det var slik ideen om MiniHouse oppstod.» | – | Carlos's own view |
| Section 1 title | «Fra rivningsmaterialer til beredskapsboliger» | **K-40** | intention, story page only |
| 1 · ¶1 | «… beredskapsboliger på omtrent 3 × 6 meter, der vi bruker ombrukstre …» | **K-40**, **K-01**, **K-06** | size, purpose and timber role all registered |
| 1 · ¶2 | «… konstruert for å tåle transport … kran.» | **K-41** | the same goal as K-05, in his words |
| 1 · ¶3 | «Jeg ønsker at disse boligene skal være praktiske …» | – | his design intention |
| 1 · ¶4 | «… midlertidige boliger for mennesker som er rammet av krisesituasjoner …» | **K-40** | intention, no promise to deliver |
| Section 2 title | «Å gi gamle materialer et nytt formål» | **K-06** | reuse in cladding and finishes |
| 2 · ¶1 | «MiniHouse handler ikke bare om å bygge små hus.» | – | his view (his «tiny homes» kept in English) |
| 2 · ¶2 | «… beredskap, ingeniørfag, bærekraftig bygging og sirkulærøkonomi.» | **K-44** | kept sentence 1 / 4 |
| 2 · ¶3 | «Jeg ønsker å vise at materialer fra riveprosjekter fortsatt kan ha stor verdi …» | **K-39** | reuse goal, attributed to the project |
| 2 · ¶4 | «Tanken er å ta vare på det som fortsatt kan brukes …» | **K-06**, **K-22** | reuse plus documentation |
| 2 · ¶5 | «… alle materialer som skal brukes på nytt, blir kontrollert og vurdert …» | **K-42** | planned assessment, not a certification |
| Section 3 title | «Den større visjonen» | – | – |
| 3 · ¶1 | «… Første steg blir å bygge en prototype …» | **K-43**, **K-40** | prototype planned; no date |
| 3 · ¶2 | «Hvis konseptet fungerer, kan MiniHouse etter hvert bli …» | **K-44** | kept sentence 2 / 5 |
| 3 · ¶3 | «Det som startet som en tanke på en riveplass …» | – | his view |
| Picture captions | «Konseptbilde» ×2 (nb), "Concept image" ×2 (en) | **K-20** | every picture of the house is a concept |
| Closing | «I stedet for å se på riving som slutten …» | – | his view |
| Motto | «MiniHouse:», «Gamle materialer.», «Nye hjem.», «Et nytt liv.» | **K-06**, **K-19** | materials and concept status |
| CTA | «Se huset» / "Explore the house" | – | an action, same as the home hero |
| Footer | images note, Personvern, For fagfolk | **K-19**, **K-20**, **K-28** | unchanged site footer |

**The five kept sentences** passed `check_promo.py` through the D-21 exception, and nowhere else: the same words outside those five sentences still fail, and the emergency words are blocked outside `story.*` (never in `story.teaser`).

**What the page does not say:** that MiniHouse uses the Øvsttunvegen timber (K-37 forbids implying it), that the house is built or tested, that the timber is load-bearing, or any price, date, weight or U-value.

## 2 · The external link

```powershell
curl -s -o NUL -w "%{http_code} %{content_type}" https://totalbyggoganlegg.no/ovsttunvegen/
# 200 text/html   (2026-11-18 23:30)
```

The rendered tag is `<a href="https://totalbyggoganlegg.no/ovsttunvegen/">`, same tab, no icon, as §6.16 asks.

## 3 · axe

```powershell
npx @axe-core/cli http://127.0.0.1:4322/historien/ http://127.0.0.1:4322/en/historien/ `
  --save fase4/promo/qa/reports/axe-story.json `
  --chromedriver-path "…/chromedriver-win64/chromedriver.exe"
```

**0 violations on both pages.** Raw output `qa/reports/axe-story.txt` and `.json`.

## 4 · Lighthouse, `/historien/`

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

All four gates in the task (0 axe violations, LCP ≤ 2.5 s, CLS ≤ 0.1) pass.

## 5 · Gaps

None technical. Two things I cannot judge and do not claim: whether the question band reads as the page's one loud moment, and whether the crops show the house well — those are Grok's G-6 and Carlos's G4.

## 6 · D-23 live check · **failed on two of the four routes**

Checked 2026-11-18 23:52 against <https://minihouse-preview.canner.app> with `curl` 8.x:

| Route | Result |
|---|---|
| `/` | **200** `text/html; charset=utf-8` |
| `/en/` | **200** `text/html; charset=utf-8` |
| `/historien/` | **404** `text/html; charset=utf-8` |
| `/en/historien/` | **404** `text/html; charset=utf-8` |

The 404s are not a routing quirk: the uploaded bundle does not contain the pages. `web/promo/.bundle` has no `historien/` and no `en/historien/`, and `check_promo.py --dist web/promo/.bundle` counts **5 pages**, not 7 — it is the pre-story bundle. So whatever was deployed at G-8 is the older build.

**`hreflang`:** the four pages that do answer return the landing-pair tags
`nb → https://minihouse.canner.app/`, `en → …/en/`, `x-default → …/` — production host, not the preview host. The correct story pairs exist **only in the local build**:
`nb → https://minihouse.canner.app/historien/`, `en → …/en/historien/`, `x-default → …/historien/`.
So there are two separate findings:

1. **→ Grok:** rebuild the bundle (`cd web/promo && npm run bundle`) and redeploy to `minihouse-preview`; the current `.bundle` is the 5-page build, so G-8 did not carry the story.
2. **→ Grok / Carlos:** decide whether absolute `hreflang` may point at the production host from the preview. It is harmless while the preview is a staging copy, but it is wrong data on a page served from another origin; either use relative URLs or make the site base configurable per deployment.

**What still passes:** the build itself (`check_promo.py --dist web/promo/dist`, 7 pages), axe (0 violations), Lighthouse (100s, LCP 0.8 s), and the claims audit in §1. The page is ready in `dist`; it is simply not on the preview.

**HANDOVER → Carlos:** the story page is **not** on minihouse-preview yet, so there is nothing for G4 to look at there. Grok needs one more bundle-and-deploy; when the two story routes answer 200, I re-run this section and hand it over again. The page in the local build is as described in §1–§4.

**Correction (2026-11-19):** the run above came one minute before Grok's G-8 upload (23:55, deployment `a658a570`), so it measured the previous deployment. The finding about the bundle was a timing artefact, not a defect. §7 is the valid result.

## 7 · D-23r · live check, re-run · **pass**

2026-11-19 01:12, against <https://minihouse-preview.canner.app> (deployment `a658a570`), `curl` 8.x:

| Route | Result |
|---|---|
| `/` | **200** `text/html; charset=utf-8` |
| `/en/` | **200** `text/html; charset=utf-8` |
| `/historien/` | **200** `text/html; charset=utf-8` |
| `/en/historien/` | **200** `text/html; charset=utf-8` |
| `/film/house-film.mp4`, `-r 0-1` | **206** `video/mp4` |
| `/.env.production` | **404** |

**`hreflang`:** each page names its own twin.

| Page | `nb` | `en` | `x-default` | Language link |
|---|---|---|---|---|
| `/`, `/en/` | `/` | `/en/` | `/` | `/` ↔ `/en/` |
| `/historien/`, `/en/historien/` | `/historien/` | `/en/historien/` | `/historien/` | `/historien/` ↔ `/en/historien/` |

The absolute URLs point at `minihouse.canner.app`, the production host, from the preview. That is the intended canonical address, so it is a note, not a defect.

**`check_promo.py --dist web/promo/.bundle`:** **7 pages, all checks passed**. Both story pages have `lang` right, one `h1` and two images.

**HANDOVER → Carlos:** the story page is live on <https://minihouse-preview.canner.app/historien/> and <https://minihouse-preview.canner.app/en/historien/>, ready for you to look at for G4. The claims audit, axe and Lighthouse are in §1–§4.

## 8 · D-27 · R3 build audited

**Build identified:** `web/promo/dist`, file time **2026-11-19 01:51:12**, 7 pages, served on `http://127.0.0.1:4322`. Routes measured: **`/` and `/historien/`** (the card's two), both languages checked for the claims, both form factors for the tools. Tools: axe-core 4.14.1, Lighthouse 13.6.0, `check_promo.py`.

### 8.1 · The new words, and their rows

| Where | Text rendered | Row | Verdict |
|---|---|---|---|
| Home, gallery | «Alle bildene her er konseptbilder.» / "All the pictures here are concept images." | **K-20** | true: that gallery shows only renders |
| Home, footer | «Bildene av MiniHouse er konseptbilder. Huset er under utvikling.» / "The pictures of MiniHouse are concept images. The house is under development." | **K-20**, **K-19** | narrower than before, and now correct: the story page's photos are real |
| Home, story section | «Lærerboligen under rivingen, april 2026. Foto: Carlos» | **K-45**, **K-36** | the photo shows the dismantling under way; camera 2026-04-03 |
| Home, films | «Konseptfilm» ×3 with «Spill av filmen» | **K-35** | the house film is a render, so the caption is right |
| Home, materials | «Konseptbilde av materialuttrykket» ×4 | **K-20** | textures, not photos |
| Story, trio | «Blyglassvinduet i lærerboligen. Foto: Joran Ingvaldsen» · «Den gamle komfyren under rivingen. Foto: Carlos» · «Steinheller som ble tatt vare på under rivingen. Foto: Joran Ingvaldsen» | **K-45**; the stone also **K-37** | credited, and no claim about where the materials went |
| Story, pair | «Årstallet 1887, skrevet med blyant på et bord i lærerboligen…» · «En gammel spiker i treverket…» | **K-45**, **K-46** | describes the inscription and the nail; dates nothing else |
| Story, pictures | «Konseptbilde» ×2 (`exploded`, `hero-slope`) | **K-20** | renders of MiniHouse |
| Story | **no «Konseptfilm»** | **K-47** | correct: the Midtun film is real, so it must never carry that caption, and it is not on the page (§8.4) |

The six photo captions and their alt texts were verified string by string against Appendix B and `images.json`: **32 strings, 0 differences** (deck §6.2–§6.3).

**What the page still never says:** that MiniHouse uses the timber, stone, glass or stove from Øvsttunvegen (K-37); that the house is built or tested (K-19); any price, date, weight or U-value. No caption carries a photographer's phone number or file data, and `check_promo.py` now refuses a served JPEG that does.

### 8.2 · axe

**0 violations on `/` and on `/historien/`**, axe-core 4.14.1, ChromeDriver 157.0.8103.51. Reports: `qa/reports/axe-r3.txt`, `axe-r3.json`. Details in [a11y.md](a11y.md).

### 8.3 · Lighthouse

Full table in [perf.md](perf.md). Headline: `/` phone **LCP 2.3 s**, CLS 0, perf 0.97; `/` desktop LCP 0.5 s, perf 1; `/historien/` phone **LCP 0.8 s**, CLS 0, perf 1; `/historien/` desktop LCP 0.5 s, perf 1. Accessibility, best practices and SEO are 100 on all four runs.

**Gates:** axe 0 ✓ · LCP ≤ 2.5 s on mobile ✓ (2.3 s on the home page, 0.8 s on the story) · CLS ≤ 0.1 ✓.

### 8.4 · The two gaps that are not failures

1. **The Midtun film is not on the story page**, so the film still is not the largest paint: it is text on the phone and `midtun-stone` on the desktop. Cause: `images/midtun_teachers_residence_clean_4k.mp4` does not exist; only the titled v3 is on disk, which D16 forbids cutting. When Carlos exports the clean master, G-16 makes the cuts, `getFilm('midtun')` starts returning the poster, and I re-run this section.
2. **The home page's LCP is the film poster at 2.3 s**, 0.2 s inside the mobile gate. Recorded in [perf.md](perf.md) as a watch item.

### 8.5 · What I did not judge

Whether the six photos show what their alt texts describe, whether the gable crop works at 4:5, and whether the gallery now reads as a contact sheet. Those are Grok's G-18 screenshots and Carlos's G4.

2026-11-19 01:12, against <https://minihouse-preview.canner.app> (deployment `a658a570`), `curl` 8.x:

| Route | Result |
|---|---|
| `/` | **200** `text/html; charset=utf-8` |
| `/en/` | **200** `text/html; charset=utf-8` |
| `/historien/` | **200** `text/html; charset=utf-8` |
| `/en/historien/` | **200** `text/html; charset=utf-8` |
| `/film/house-film.mp4`, `-r 0-1` | **206** `video/mp4` |
| `/.env.production` | **404** |

**`hreflang`:** each page names its own twin.

| Page | `nb` | `en` | `x-default` | Language link |
|---|---|---|---|---|
| `/`, `/en/` | `/` | `/en/` | `/` | `/` ↔ `/en/` |
| `/historien/`, `/en/historien/` | `/historien/` | `/en/historien/` | `/historien/` | `/historien/` ↔ `/en/historien/` |

The absolute URLs point at `minihouse.canner.app`, the production host, from the preview. That is the intended canonical address, so it is a note, not a defect.

**`check_promo.py --dist web/promo/.bundle`:** **7 pages, all checks passed**. Both story pages have `lang` right, one `h1` and two images.

**HANDOVER → Carlos:** the story page is live on <https://minihouse-preview.canner.app/historien/> and <https://minihouse-preview.canner.app/en/historien/>, ready for you to look at for G4. The claims audit, axe and Lighthouse are in §1–§4.

