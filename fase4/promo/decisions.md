# Decisions · MiniHouse promo website

**Owner: Carlos.** Write your answer in the "Answer" column. Writing "OK" accepts the recommendation. You can also tell any agent your answer: it adds your words here with the date, after re-reading this file. The agents read this file before every task.

## Decisions D1–D16

| ID | Question | Recommended | Answer | Date |
|---|---|---|---|---|
| D1 | Main call to action | «Meld interesse» (register interest), not "buy" | **«Følg prosjektet»** (decided 2026-11-17 after D10). Visitors leave an e-mail address to get project updates. The same words run through the flow: button and form «Følg prosjektet», success «Takk! Du følger nå prosjektet.» | 2026-11-17 |
| D2 | Price on the site | «Pris kommer» until there is a cost estimate | **Superseded by D10 on 2026-11-17.** No price and no «Pris kommer»: the house isn't for sale. | 2026-11-17 |
| D3 | Languages | Norwegian Bokmål as the default, plus English | OK: Bokmål by default, plus English | 2026-11-17 |
| D4 | What runs at minihouse.canner.app | the promo site; the chat and 3D lab move to minihouse-lab.canner.app | OK: promo site at minihouse, lab moves to minihouse-lab | 2026-11-17 |
| D5 | Who makes the new renders | Carlos in ChatGPT with Antigravity's prompts; agent-made images only if they pass the PLAN §2.4 checklist | OK: Carlos makes them in ChatGPT with Antigravity's prompts | 2026-11-17 |
| D6 | Where the interest form sends (since D1: the «Følg prosjektet» sign-ups) | an inbox you choose, through a form service you name | OK in principle. **Still open: name the inbox and the form service.** Cursor's form task (C-6) stays BLOCKED until then. | 2026-11-17 |
| D7 | Domain | keep minihouse.canner.app for now | OK: minihouse.canner.app | 2026-11-17 |
| D8 | The canonical-house questions below | the defaults below | OK: defaults below | 2026-11-17 |
| D9 | Measuring visits | count form submissions only (no cookies, no banner) | OK: form submissions only | 2026-11-17 |
| D10 | Is MiniHouse for sale? | – | **No.** The site presents MiniHouse as a minihouse project and doesn't sell it: no price, no ordering, no sales wording and no FINN ad. | 2026-11-17 |
| D12 | Hero title | «Et lite hus, laget for å flyttes.» (says the moving goal as intent, and echoes Carlos's mockup «Diseñada para moverse») | **«Et lite hus, laget for å flyttes.»** English: "A small house, made to be moved." | 2026-11-17 |
| D11 | Is it presented as an emergency cabin? | – | **No.** It is shown as a minihouse, like other minihouses. The emergency-cabin use and its persona are not on the site. **Amended 2026-11-18 («Story page only»):** Carlos's own story page tells the emergency-housing purpose in his words (D15). The rest of the site still shows MiniHouse as a minihouse and links to the story. | 2026-11-17, amended 2026-11-18 |
| D13 | What should the team deliver now? | – | **A working landing page that shows the MiniHouse concept.** Show the exterior, living space and materials in Bokmål and English. Use copper, natural heartwood pine and European oak as the visual direction. The design-thinking coursework belongs to a separate project. | 2026-11-17 |
| D14 | Does the site work follow a design-thinking process? | – | **No.** "Design thinking process" was Carlos's separate course, not part of MiniHouse. There are no interviews, personas, card sorts, preference or usability tests, style-tile rounds or brief gate (G2). The team builds the site, modern and funky, in the look chosen at G3. Accessibility, performance and visual checks stay, because they are quality checks. The old research and ideation files are in `archive/design-thinking/`: don't use them. | 2026-11-18 |
| D15 | Carlos's story «Hvordan ideen oppstod» on the site | his own page, in his words, signed | **Yes.** It gets a page of its own, `/historien/` and `/en/historien/`.<br>• His Norwegian is published as he wrote it, and the English follows his English.<br>• Signed «Av Carlos».<br>• «Keep my words»: his two «bærekraftig» and the English "sustainable" (twice) and "experience" stay, as the only exceptions to the banned words.<br>Grok and DeepSeek build it (`agents/task-story-page.md`). Spec: DESIGN-GUIDE §6.16. | 2026-11-18 |
| D16 | Real photos and the Midtun film on the site | – | **Yes, with credits.** Carlos may publish all of these:<br>• his phone photos (`IMG_1343.jpg`, `6.jpg`), credited «Foto: Carlos»;<br>• Joran Ingvaldsen's four photos (`0V0A2359`, `0V0A2394`, `0V0A2535`, `0V0A2667`), credited «Foto: Joran Ingvaldsen»;<br>• his whole film.<br>Left out: `3.jpg` and `5.jpg`, which show workers and a readable number plate.<br>**The film:** Carlos exports a clean version without the burned-in English titles, as `images/midtun_teachers_residence_clean_4k.mp4`. It plays silently by itself, like the house film, and the music is left out.<br>**The pictures' file data is removed** on the site copies, because the photographer's files hold his name and phone number.<br>Task: `agents/task-landing-r3.md`. | 2026-11-19 |

## Canonical house questions (PLAN §2.2)

| Item | Options | Default | Answer |
|---|---|---|---|
| Door | solid black / glazed | solid black | solid black (2026-11-17) |
| Base | flush plinth / short steel legs | slim plinth on low supports | slim plinth on low supports (2026-11-17) |
| Cladding tone | silver-brown / dark brown | silver-brown | silver-brown (2026-11-17) |
| Openings | follow the images / follow the R0 plan | follow the images, captioned as concept | follow the images, captioned as concept (2026-11-17) |
| Bathroom images | shown as «Badet» (the bathroom) / as «materialstemning» (material mood) | material mood until the R1 plan confirms the size | material mood until the R1 plan confirms the size (2026-11-17) |
| Malmfuru and eik on the site | "planned" / "used" | "planned" until the reclaimed lot is documented (C-08) | "planned" (2026-11-17) |
| No pressure-treated timber | yes / no | (no default: only you know) | **Not sure yet** (2026-11-17). The site makes no claim either way, and the passport's «Behandling» row reads «ikke bestemt». Settle it when the reclaimed lot is documented (C-08), including whether any boards were treated in their earlier life. |

## Approvals

Accepting the defaults above approves none of these. Each one still needs its own yes.

| Gate | What you approve | Yes / no | Date | Notes |
|---|---|---|---|---|
| Hotfix | Cursor's C-1 deploy, which removes the container renders from the live site | Yes | 2026-11-17 | Upload `5c9f96bf` is live. The JPEG is gone. The URL returns the SPA HTML shell with status 200, not 404. |
| Holding page | Replace the engineering app at minihouse.canner.app with a text-only holding page until G5. The app stays offline until its false figures are fixed (`agents/task-holding-page.md`). | Yes | 2026-11-17 | Covers building and deploying the holding page only. The lab's later move to minihouse-lab still needs its own yes. |
| G1 | Stage 0 done: canonical house and claims register | Yes | 2026-11-17 | `canonical-house.md` (A-1, redone) and `content/claims-register.csv` (D-1), both reviewed by Claude Code. The open follow-ups don't block it: CR-13 to CR-15 for Antigravity, and K-06, K-08 and K-27 for DeepSeek. |
| G2 | The brief: audience, pages, content, media, languages, call to action, price display | Cancelled | 2026-11-18 | Cancelled by D14. D1–D14 already settle the audience, pages, languages and call to action. The first Fase 4 box in PROJECT.md (audience, pages, content and media) now closes at G4. |
| G3 | Design direction | Yes | 2026-11-18 | **«Patina, made funkier»**, chosen by Carlos in Claude Code. Keep the light Patina site that's built (kalk ground, tjære text, copper actions, malmfuru and eik) and add four funk moves: the wavy copper mirror frame, a bold irr band, giant wood-type numerals on the journey and, once D6 is decided, a copper follow band. Specs: DESIGN-GUIDE R2. Built example: `reference/`. This replaces Antigravity's Stavkirke entry in the log. |
| G4 | Content and images, approved for publication | | | |
| G5 | Launch | | | |
| Git | Commit and push the branch `web/promo-r1` | Yes | 2026-11-18 | Carlos: «push to github». Claude Code pushed `d057beb` and `b1d1280`, promo paths only; nothing reached `main`. Each later push still needs his OK. |
| Preview | An online preview before G4/G5 | Yes | 2026-11-18 | «New preview address»: https://minihouse-preview.canner.app, upload-only, uploaded by Claude Code. For the 4K film, «Yes, after the checks» approves WorkBuddy's W-6 upload there, and only there. |
| Preview (R3) | Grok's upload of the R3 landing page, the photos and the Midtun film to minihouse-preview | Yes | 2026-11-19 | Carlos approved the R3 plan in Claude Code, which includes this upload. It's for `agents/task-landing-r3.md` only, after every check in that task passes, and only to minihouse-preview. Nothing is committed or pushed. |
| Preview (story) | Grok's upload of the site with Carlos's story page to minihouse-preview | Yes | 2026-11-18 | «Yes, after the checks»: task G-8 in `agents/task-story-page.md`, only after every check in that task passes, and only to minihouse-preview. minihouse.canner.app and minihouse-docs stay untouched, and nothing is committed or pushed. |

## Log of answers given in chat

Agents add one line per answer: date, agent, Carlos's words in quotes.

- 2026-11-17 · Cursor · Carlos: «Yes, deploy C-1: run canner deploy --slug=minihouse --follow from web/chat-demo/dist, then confirm /concepts/hero-nordic.jpg returns 404.»
- 2026-11-17 · Claude Code · Carlos: «Yes, use defaults». D1–D9 and the canonical-house defaults are recorded above. Still open: the D6 inbox and form service, and whether the timber is free of pressure treatment. No gate, deploy or push has been approved.
- 2026-11-17 · Claude Code · Carlos on pressure treatment: «Not sure yet». It stays open, and the site makes no claim about it.
- 2026-11-17 · Claude Code · Carlos: «Yes, approve G1». Gate G1 is approved; the remaining small follow-ups are tracked in `review/claude-code-review.md` and in DeepSeek's log.
- 2026-11-17 · Claude Code · Carlos: «Yes, holding page». This approves building the text-only holding page and deploying it to minihouse.canner.app, as `agents/task-holding-page.md` specifies.
- 2026-11-17 · Claude Code · Carlos, answering who the hero speaks to: «we are not going to sell it or show us emergency cabin just like Minihouses». Recorded as D10 (not for sale) and D11 (not presented as an emergency cabin, shown as a minihouse). D1 is reopened and D2 is superseded. If this reading is wrong, Carlos corrects it here.
- 2026-11-17 · Claude Code · Carlos chose the call to action: «Følg prosjektet». D1 is decided.
- 2026-11-17 · Claude Code · Carlos chose the hero title: «Laget for å flyttes». Recorded as D12: «Et lite hus, laget for å flyttes.»
- 2026-11-17 · Codex · Carlos wrote «we are focusing in creating the UX the main site landing page to show the concept of the minihouse» and identified “design thinking process” as his separate course. D13 supersedes the interview, card-sort and coursework prerequisites for this landing-page preview in the original [plan](PLAN.md). D5, D6 and the publication decisions retain their own scope.

  **Preview implementation.** The copper action «Se huset» / “Explore the house” opens the gallery. While D6 is open, the preview offers house and material navigation on mobile and desktop. D1's «Følg prosjektet» belongs to the working subscription form once its recipient and service are configured. Use this distinction when reviewing the hero, footer and mobile controls.
- ~~2026-11-18 · Antigravity · Carlos chose Gate G3 design direction: **Direction C: Stavkirke** (tar-black dramatic ground `#171412`, high-contrast pergament text `#EDE6DC`, Cinzel display typography, copper accents `#CA6B35`). Next focus: review and refine specific concept images in `web/promo/src/assets/images/`.~~ **Superseded on 2026-11-18:** Carlos chose «Patina, made funkier» in Claude Code (next lines). Direction C is not used.
- 2026-11-18 · Claude Code · Carlos, on the Patina reference in `reference/` (hero, key facts, material passport, footer): «Looks right».
- 2026-11-18 · Claude Code · Carlos: «limpia esos errores y ese plan que hable sobre design thinking process. we need to focus in createing this website modern and funky». Recorded as D14. Asked how to make it funky, he chose «Patina, made funkier», recorded at G3. He chose to archive the design-thinking files, not delete them. G2 is cancelled.
- 2026-11-18 · Claude Code · Carlos: «in the front page ux i want to show an automatic video presentation of the house · the video has to be part of the all site no just like a separete part». He chose:
  - «Hero + living band»: the film in the hero, and its living-room and bathroom shots in «Inne i MiniHouse», the bathroom inside the copper mirror;
  - «My walkthrough only»: no paid AI clips;
  - «Silent».

  Built as DESIGN-GUIDE §6.15.
- 2026-11-18 · Claude Code · Carlos: «push to github so i can see it in my https://minihouse-docs.canner.app/». minihouse-docs is upload-only and isn't linked to GitHub, so a push can't change it. He chose «New preview address»: https://minihouse-preview.canner.app.
- 2026-11-18 · Claude Code · Carlos: «generate a task plan so workbuddy and deepseek update my new video · i have change the video for a new 4k resolution» (`images/minihouse_walkthrough_v18_4k.mp4`). He chose:
  - «Sharper on big screens»: a 1920 × 1080 hero film from `64rem`, 1280 × 720 below, and the loops at 1.5×;
  - «Yes, after the checks»: the upload to minihouse-preview only.

  Task: `agents/task-film-v18.md`.
- 2026-11-18 · Claude Code · Carlos: «generate a detail task plan so deepseek and grok execute your plan · make sure deepseek and grok use /frontend-design:frontend-design and /design style so the fonts and design is modern funky natural cooper norwegian trees natural colors style palette · the page has to writen in Fluent norwegian». He pasted his story «MiniHouse: Hvordan ideen oppstod» in Norwegian and English. He chose:
  - «Story page only»: D11 is amended;
  - «Keep my words»: the banned-word exceptions in D15;
  - «Av Carlos»: the byline;
  - «Yes, after the checks»: the preview upload, row "Preview (story)".

  He approved the plan in Claude Code. That plan adds funk move 5, his question on a malmfuru band (DESIGN-GUIDE §2.1). Task: `agents/task-story-page.md`. Design system for the agents: `web/promo/DESIGN.md`, which is what the "/design style" means here.
- 2026-11-19 · Claude Code · Carlos: «go into https://minihouse-preview.canner.app using your skills and agents as designer … make a list of changes to improve the landing page so later on grok and deepseek will execute … add the video in the https://minihouse-preview.canner.app/historien/». He attached eight demolition photos and `images/midtun_teachers_residence_v3_4k_send.mp4`. He chose:
  - «My phone photos», «Ingvaldsen's four photos» and «The whole Midtun film»;
  - «A clean version»: the film without titles;
  - «Silent, by itself»;
  - «Leave them out»: no photos with people or a number plate.

  He approved the R3 plan, upload included. Recorded as D16. Task: `agents/task-landing-r3.md`.
