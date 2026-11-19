# Copy deck · Carlos's story «Hvordan ideen oppstod»

Task D-18 ([task-story-page.md](../agents/task-story-page.md)). 2026-11-18. Master: the Norwegian in Appendix A of the task file, pasted by Carlos. The English follows his English. **His sentences are published as he wrote them**; this deck copies them, it does not edit them.

Claims: [claims-register.csv](claims-register.csv), rows K-36 to K-44, with K-06, K-22, K-05, K-19 and K-26 behind them. A paragraph tagged «Carlos's own view» is first person: it is his opinion or intention, published verbatim, and it is not a claim about the built world.

---

## 1 · The five changes to Carlos's text (the complete list)

| # | Change | Where |
|---|---|---|
| 1 | The h1 loses «MiniHouse:», which moves to the page title, because the header already says MiniHouse. | `story.meta.title` = «MiniHouse: Hvordan ideen oppstod»; `story.title` = «Hvordan ideen oppstod» |
| 2 | The English headings go to sentence case. | «From demolition waste to emergency housing», «Giving old materials a new purpose», «The bigger vision» |
| 3 | Two English paragraphs become one, so both languages have arrays of the same length. | `story.intro[1]`: "It was a beautiful old building …" + "The property was being redeveloped …" |
| 4 | His bold lines become typography, not `<strong>`: the question band, the closing and the motto. | `story.question`, `story.questionFollow`, `story.closing`, `story.motto[]` |
| 5 | The bare URL becomes the link text, without `https://`. | `story.reference.link` = «totalbyggoganlegg.no/ovsttunvegen» |

Nothing else changes. Where I would have worded something differently, it is a proposal in my status file, never an edit.

## 2 · The five kept sentences

Carlos answered «Keep my words», so these stay exactly as written and are the **only** place where «bærekraftig» / "sustainable" and the word "experience" are allowed (D-21 checks that):

1. nb «For meg handler prosjektet om å kombinere beredskap, ingeniørfag, bærekraftig bygging og sirkulærøkonomi.»
2. nb «Hvis konseptet fungerer, kan MiniHouse etter hvert bli en praktisk løsning for å gi egnede rivningsmaterialer nytt liv som trygge og bærekraftige beredskapsboliger.»
3. en "That experience made me ask myself a simple question:"
4. en "It's about bringing together emergency preparedness, engineering, sustainable construction and the circular economy."
5. en "If the concept works, MiniHouse could eventually become a practical way to transform suitable demolition materials into safe, sustainable emergency housing."

## 3 · The deck

### meta and header words

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `story.meta.title` | MiniHouse: Hvordan ideen oppstod | MiniHouse: How the idea started | – |
| `story.meta.description` | Hvordan ideen om MiniHouse oppstod: fra rivingen av en gammel lærerbolig i Bergen til et lite hus som er laget for å kunne flyttes. | How MiniHouse began: from the demolition of an old teachers' residence in Bergen to a small house made to be moved. | K-36, K-19 |
| `story.title` | Hvordan ideen oppstod | How the idea started | – |
| `story.byline` | Av Carlos | By Carlos | – |
| `nav.story` | Historien | The story | – |

### The opening

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `story.lead` | Jeg ønsker å se nærmere på noen av tankene bak MiniHouse-prosjektet mitt, og først og fremst fortelle hvordan ideen oppstod. | I want to revisit a few concepts behind my MiniHouse project, starting with how the idea came to life. | Carlos's own view |
| `story.intro[0]` | I 2026 var jeg med på rivingen av den gamle lærerboligen til Midtun skole i Øvsttunvegen 21 i Bergen. | In 2026, I was involved in the demolition of the old Midtun School Teachers' Residence at Øvsttunvegen 21 in Bergen, Norway. | **K-36** |
| `story.intro[1]` | Det var en vakker, gammel bygning med særpreg, historie og mange minner knyttet til seg. Eiendommen skulle utvikles videre, og planen var å oppføre et nytt bygg på samme tomt, med utgangspunkt i den opprinnelige bygningens arkitektoniske uttrykk og form. | It was a beautiful old building with character, history and memories attached to it. The property was being redeveloped, with a new building planned for the site that would preserve the architectural character and form of the original. | **K-38** (his view of the building: Carlos's own view) |
| `story.intro[2]` | Et av målene med prosjektet var å gjenbruke så mye som mulig av de eksisterende byggematerialene. | One of the redevelopment project's objectives was to reuse as much of the existing building material as possible. | **K-39** |
| `story.reference.label` | Prosjektreferanse: | Project reference: | **K-38** |
| `story.reference.link` | totalbyggoganlegg.no/ovsttunvegen | totalbyggoganlegg.no/ovsttunvegen | **K-37** |
| `story.reference.href` | https://totalbyggoganlegg.no/ovsttunvegen/ | the same | **K-37** |

### What he noticed

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `story.noticed[0]` | Arbeidet med rivingen fikk meg til å se på byggavfall på en helt annen måte. | Working on that demolition made me look at construction waste differently. | Carlos's own view |
| `story.noticed[1]` | Etter hvert som vi demonterte bygningen, la jeg stadig merke til kvaliteten på det gamle treverket. Noe av materialet hadde vært en del av bygningen i flere tiår, men var fortsatt i overraskende god stand og så ut til å kunne brukes videre. | As we dismantled the building, I kept noticing the quality of the old timber. Some pieces had been there for decades, yet they still looked remarkably good and potentially useful. | **K-37** (the demolition and the timber) |
| `story.noticed[2]` | Jeg syntes det var synd at materialer som allerede hadde tjent én generasjon, skulle kastes når de kanskje kunne komme til nytte for flere. | It seemed such a waste to throw away materials that had already served one generation and could potentially serve another. | Carlos's own view |
| `story.noticed[3]` | Denne opplevelsen fikk meg til å stille meg selv et enkelt spørsmål: | That experience made me ask myself a simple question: | **K-44** (kept sentence 3) |

### The question band

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `story.question` | Hvorfor skal materialenes levetid ta slutt bare fordi bygningen de kommer fra, blir revet? | Why should the life of a building's materials end when the building itself is demolished? | Carlos's own view |
| `story.questionFollow` | Hva om vi kunne ta vare på disse materialene og bruke dem til å skape noe helt nytt? | What if we could take those materials and create something entirely new? | Carlos's own view |
| `story.origin` | Det var slik ideen om MiniHouse oppstod. | That's where MiniHouse began. | Carlos's own view |

### Section 1 · Fra rivningsmaterialer til beredskapsboliger

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `sections[0].title` | Fra rivningsmaterialer til beredskapsboliger | From demolition waste to emergency housing | **K-40** |
| `sections[0].paragraphs[0]` | Ideen min er å utvikle og bygge små, prefabrikkerte beredskapsboliger på omtrent 3 × 6 meter, der vi bruker ombrukstre og andre byggematerialer som fortsatt er i god stand, så lenge det er praktisk mulig og sikkerhetsmessig forsvarlig. | My idea is to design and build small, prefabricated emergency homes, approximately 3 × 6 metres, using reclaimed timber and other reusable construction materials wherever practical and safe. | **K-40**, **K-01** (≈ 3 × 6 m), **K-06** |
| `sections[0].paragraphs[1]` | Boligene skal bygges rundt en solid og nøye dimensjonert bærekonstruksjon. Den skal være konstruert for å tåle transport og gjøre det mulig å løfte og flytte hele boligen ved hjelp av en kran. | The houses would be built around a properly engineered structural frame, designed to make them strong enough for transportation and suitable for lifting and relocation by crane. | **K-41** |
| `sections[0].paragraphs[2]` | Jeg ønsker at disse boligene skal være praktiske, komfortable og holdbare, samtidig som de skal være enkle å produsere, transportere og sette opp. | I want these homes to be practical, comfortable and durable, but also easy to manufacture, transport and deploy. | Carlos's own view (a design intention) |
| `sections[0].paragraphs[3]` | De skal kunne brukes som midlertidige boliger for mennesker som er rammet av krisesituasjoner, naturkatastrofer eller andre hendelser der det oppstår et akutt behov for et trygt sted å bo. | They could provide temporary accommodation for people affected by emergencies, natural disasters or other situations where safe housing is urgently needed. | **K-40** |

### Section 2 · Å gi gamle materialer et nytt formål

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `sections[1].title` | Å gi gamle materialer et nytt formål | Giving old materials a new purpose | **K-06** |
| `sections[1].paragraphs[0]` | MiniHouse handler ikke bare om å bygge små hus. | MiniHouse is not simply about building tiny homes. | Carlos's own view (his phrase «tiny homes» stays as written) |
| `sections[1].paragraphs[1]` | For meg handler prosjektet om å kombinere beredskap, ingeniørfag, bærekraftig bygging og sirkulærøkonomi. | It's about bringing together emergency preparedness, engineering, sustainable construction and the circular economy. | **K-44** (kept sentence 1 / 4), **K-40**, **K-06**, **K-22** |
| `sections[1].paragraphs[2]` | Jeg ønsker å vise at materialer fra riveprosjekter fortsatt kan ha stor verdi, og at de ikke nødvendigvis trenger å ende opp som avfall. | I want to show that materials recovered from demolition sites can become valuable resources rather than automatically ending up as waste. | **K-39**, Carlos's own view |
| `sections[1].paragraphs[3]` | Tanken er å ta vare på det som fortsatt kan brukes, kombinere det med moderne ingeniørløsninger og skape noe som får en helt ny funksjon. | The idea is to preserve what is still useful, combine it with modern engineering and create something that serves a completely new purpose. | **K-06**, **K-22** |
| `sections[1].paragraphs[4]` | Samtidig er det viktig at alle materialer som skal brukes på nytt, blir kontrollert og vurdert ut fra hva de egner seg til. Konstruksjonssikkerhet, isolasjon, fuktsikring og lang levetid skal være viktige deler av utviklingsarbeidet. | Of course, every reclaimed material would need to be assessed for its suitability. Structural safety, insulation, moisture protection and long-term durability would remain essential parts of the design. | **K-42** |

### Section 3 · Den større visjonen

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `sections[2].title` | Den større visjonen | The bigger vision | – |
| `sections[2].paragraphs[0]` | Det langsiktige målet mitt er å utvikle et standardisert system for produksjon av transportable beredskapsboliger. Første steg blir å bygge en prototype som er grundig planlagt, dimensjonert og testet. | My long-term goal is to develop a repeatable system for manufacturing transportable emergency homes, starting with one properly engineered prototype. | **K-43**, **K-40** |
| `sections[2].paragraphs[1]` | Hvis konseptet fungerer, kan MiniHouse etter hvert bli en praktisk løsning for å gi egnede rivningsmaterialer nytt liv som trygge og bærekraftige beredskapsboliger. | If the concept works, MiniHouse could eventually become a practical way to transform suitable demolition materials into safe, sustainable emergency housing. | **K-44** (kept sentence 2 / 5), **K-40**, **K-06**, **K-22** |
| `sections[2].paragraphs[2]` | Det som startet som en tanke på en riveplass, kan kanskje utvikle seg til noe mye større. | What began as a thought on a demolition site could become something much bigger. | Carlos's own view |

### The ending

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `story.closing` | I stedet for å se på riving som slutten på en bygnings historie, ønsker jeg å se på det som en mulighet til å starte en ny. | Instead of seeing demolition as the end of a building's story, I want to see it as an opportunity to begin another. | Carlos's own view, **K-39** in the background |
| `story.motto[0]` | MiniHouse: | MiniHouse: | – |
| `story.motto[1]` | Gamle materialer. | Old materials. | **K-06** |
| `story.motto[2]` | Nye hjem. | New homes. | **K-19** (a concept, not a built house) |
| `story.motto[3]` | Et nytt liv. | A second life. | **K-06** |
| `story.cta` | Se huset | Explore the house | – (an action, same as `hero.gallery`) |

### The home-page teaser and my own words

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `story.teaser.title` | Hvordan ideen oppstod | How the idea started | – |
| `story.teaser.body` | Historien bak MiniHouse starter på en riveplass i Bergen, med gammelt treverk som fortsatt var i god stand. | The story behind MiniHouse starts on a demolition site in Bergen, with old timber that was still in good condition. | **K-36**, **K-37** |
| `story.teaser.link` | Les historien | Read the story | – |

`story.teaser.body` carries **no emergency words**, as D11 (as amended) requires: the teaser is on the home page, and the emergency purpose belongs to the story page only.

## 4 · What the page never says

- That MiniHouse uses timber from Øvsttunvegen. Carlos's story does not say it, and K-37 forbids implying it.
- That the house is built, tested or approved: the prototype is a plan (K-19, K-43).
- That reclaimed timber is load-bearing (K-06).
- A price, a date, a delivery time, a weight or a U-value (K-16 to K-18, K-15).
- Any picture of the old building, or any generated image (DESIGN-GUIDE §6.16).
- Emergency words anywhere outside `story.*` (D-21 guard).

## 5 · Questions for Carlos (proposals, not edits)

1. **«tiny homes»** in section 2's English first paragraph is his own phrase, and it is kept. On the Norwegian side the same paragraph says «små hus». Nothing to change unless he wants the two languages to match.
2. **His English "experience"** in "That experience made me ask myself a simple question:" is the only other "experience" on the site. It stays because he asked to keep his words; the checker allows it only under `story.*`.
3. **The reference link opens in the same tab** (DESIGN-GUIDE §6.16). If he prefers a new tab, that is a design decision for Grok, not a copy change.

## 6 · R3: the photos, the Midtun film and the home fixes (2026-11-19)

Task D-24 ([task-landing-r3.md](../agents/task-landing-r3.md)), decision D16. Carlos's story text above does not change. The new words come from Appendix A (my JSON keys) and Appendix B (Grok's `images.json` entries).

**Review result: no change to the Norwegian.** All 16 Norwegian strings read as plain, correct Bokmål. All 32 strings (nb and en) pass `check_promo.py`'s word rules, under the story and under the home gallery, so «grønn» and "green" are out. So there is **no "→ Grok: replace … with …"**, and Appendix B goes into `images.json` exactly as written.

### 6.1 · My JSON keys (D-25)

| Key | Norwegian | English | Claims |
|---|---|---|---|
| `gallery.note` | Alle bildene her er konseptbilder. | All the pictures here are concept images. | **K-20** (the home gallery shows only renders) |
| `footer.imagesNote` | Bildene av MiniHouse er konseptbilder. Huset er under utvikling. | The pictures of MiniHouse are concept images. The house is under development. | **K-20**, **K-19** |
| `story.film.alt` | Film fra lærerboligen i Øvsttunvegen: huset og Midtun skole sett fra luften, blyglassvinduet, årstallet 1887 i et bord, den gamle komfyren og rivingen. | Film of the teachers' residence at Øvsttunvegen: the house and Midtun school from the air, the stained-glass window, the year 1887 on a board, the old stove and the demolition. | **K-47**, **K-46**, **K-36** |
| `story.film.caption` | Film: Carlos. Foto i filmen: Joran Ingvaldsen og Carlos. | Film: Carlos. Photos in the film: Joran Ingvaldsen and Carlos. | **K-47** |

The film's caption is a credit, not «Konseptfilm»: this film shows the real house (K-47 vs K-35). `story.film.alt` describes shots I can't see. It stands until Grok's G-16 says the clean film shows something different (Appendix A).

### 6.2 · The six photos: alt texts (Grok enters them in `images.json`)

Copied from Appendix B, both languages, each linked to its claims. The alt text says what the picture shows; the caption below says the same in one line and carries the credit.

| id | Alt nb | Alt en | Claims |
|---|---|---|---|
| `midtun-gable` | Gavlen på den gamle lærerboligen under rivingen. Kledningen er delvis tatt av, og et blyglassvindu sitter fortsatt i veggen. | The gable of the old teachers' residence during the demolition. Part of the cladding is off, and a stained-glass window is still in the wall. | **K-45**, **K-36** (dismantling in progress is visible in the photo) |
| `midtun-1887` | Gamle bord med blyantskrift i løkkeskrift. Årstallet 1887 står skrevet på det midterste bordet. | Old boards with looping pencil writing. The year 1887 is written on the middle board. | **K-45**, **K-46** |
| `midtun-nail` | En rusten, firkantet spiker stikker skrått opp av et gammelt trestykke. | A rusty square nail sticks out at an angle from an old piece of timber. | **K-45** |
| `midtun-glass` | Et blyglassvindu med trær, skyer, en seilbåt, et fyrtårn og en soloppgang rundt en stor rute i ravfarget glass. | A stained-glass window with trees, clouds, a sailing boat, a lighthouse and a sunrise around a large amber pane. | **K-45** |
| `midtun-stove` | En gammel komfyr i støpejern foran en pipe der pussen er slått av og teglsteinen ligger bar. | An old cast-iron cooking stove in front of a chimney with the plaster knocked off and the bricks bare. | **K-45** |
| `midtun-stone` | Stabler med flate steinheller på paller i gresset, med et anleggsgjerde bak. | Stacks of flat stone slabs on pallets in the grass, with a site fence behind. | **K-45**, **K-37** (46 t of stone saved) |

### 6.3 · The six photos: captions (the credit lines)

| id | Caption nb | Caption en | Claims |
|---|---|---|---|
| `midtun-gable` | Lærerboligen under rivingen, april 2026. Foto: Carlos | The teachers' residence during the demolition, April 2026. Photo: Carlos | **K-45**, **K-36** |
| `midtun-1887` | Årstallet 1887, skrevet med blyant på et bord i lærerboligen. Foto: Joran Ingvaldsen | The year 1887, written in pencil on a board in the residence. Photo: Joran Ingvaldsen | **K-45**, **K-46** |
| `midtun-nail` | En gammel spiker i treverket. Foto: Joran Ingvaldsen | An old nail in the timber. Photo: Joran Ingvaldsen | **K-45** |
| `midtun-glass` | Blyglassvinduet i lærerboligen. Foto: Joran Ingvaldsen | The stained-glass window in the residence. Photo: Joran Ingvaldsen | **K-45** |
| `midtun-stove` | Den gamle komfyren under rivingen. Foto: Carlos | The old stove during the demolition. Photo: Carlos | **K-45** |
| `midtun-stone` | Steinheller som ble tatt vare på under rivingen. Foto: Joran Ingvaldsen | Stone slabs saved during the demolition. Photo: Joran Ingvaldsen | **K-45**, **K-37** |

Every caption ends in a credit and none says «Konseptbilde», which `check_promo.py` now enforces for `kind: "photo"` (D-26). The alt texts describe what each photo shows; I can't see the pictures, so they rest on the photographers' and Claude Code's reading, and Grok's G-18 confirms them.

### 6.4 · Checks made for D-24

- **The gable photo's date: the caption stands.** The picture shows the dismantling under way (the cladding partly off, the stained-glass window still in the wall), and the camera records **2026-04-03**. That evidence supports «under rivingen, april 2026», so the caption does not change and there is no «før rivingen» version. The only thing still open is the **exact day the demolition started**; when Carlos gives it, the deck and K-45 record it, and nothing on the page needs to change.
- **K-37's never-claim holds.** No caption, alt text or film line says or suggests that MiniHouse uses the timber, stone, glass or stove from Øvsttunvegen. «Steinheller som ble tatt vare på» says the stone was saved, not where it went.
- **No photographer data.** The credit is the name only, «Foto: Joran Ingvaldsen». No phone number or file data appears in this deck or the register, and `check_promo.py` now fails any JPEG the site serves that carries Exif, XMP or IPTC (D-26b).
- **«1887».** The caption and the alt text say only what the photo shows: the inscription «1887» written in pencil on a board in the residence. They do not date the timber, the house or the boards. The reference page gives «ca. 1887» for the house (K-46). The task quotes the page as «the historic 1887 building», but that phrase isn't on the one page I read, so K-46 cites the line that is.
