# Messaging · v0

**Landing preview, 2026-11-17.** D13 sets the active brief. Visitors explore the exterior, interior and planned materials. The older research brief below is background for the project. Current interface wording lives in the two copy decks.

Rules this document works under: [DESIGN-GUIDE.md](../../../DESIGN-GUIDE.md) §9 (voice and banned words) and [claims-register.csv](../../../content/claims-register.csv) (every sentence needs a row). If a proof cannot name its rows, it is not a proof.

Basis: the claims register, [kit.md](../01-empathize/kit.md) and PLAN §6. **Excluded on purpose:** Antigravity's market scan (`01-empathize/market-scan.md`) until **CR-16** is closed ([claude-code-review.md](../../../review/claude-code-review.md)); it has no per-entry sources, so it cannot justify a message. Where the structure borrows from the FINN listing, the source is PLAN Appendix A.

---

## 1 · The one sentence

> **Et lite hus i gjenbrukt tre og stål, laget for Bergen og Vestlandet, med et mål om å kunne flyttes i ett stykke — og vi sier ærlig hvor langt vi har kommet.**

**English:** *A small house in reclaimed timber and steel, made for Bergen and Western Norway, with a goal of moving in one piece — and we say honestly how far we have come.*

| Fragment | Claims | Status | What it must never become |
|---|---|---|---|
| a small house | K-01, K-02, K-25 | konsept | "tiny home", "mikrohus" as a legal claim |
| in reclaimed timber and steel | K-03, K-06 | konsept | "bærekraftig", "miljøvennlig" |
| made for Bergen and Western Norway | K-13 | bekreftet (market) | «bygget i Bergen», «designet i Bergen» (not recorded) |
| with a goal of moving in one piece | K-05 | mål | a route, a date, «klar til å flytte», a moving frequency |
| we say honestly how far we have come | K-19, K-26 | bekreftet | "ferdig", a date, a price |

The message is deliberately narrower than a slogan: the location is a market decision, not a workshop address ([K-13](../../../content/claims-register.csv)), and the move is a goal, not a promise ([K-05](../../../content/claims-register.csv)). Moving frequency is unknown, so the message never says "when you want". The copy deck uses these same words.

---

## 2 · Three proofs

Each proof is one section of the page and one row group in the register. Order: material, move, honesty — the house, the crane, the truth.

### Proof 1 · The material is the story (K-03, K-06, K-07, K-08, K-21, K-22, K-23)

Old timber, to be documented per lot, with copper fittings and a steel frame. The material passport shows species, origin, previous use, treatment and status — and where nothing is documented, it says «dokumenteres per parti».

**Say:** «Gjenbrukt tre i kledning og overflater.» · «Vi ser etter gammel malmfuru.» · «Eik er planlagt i terskler og vindusbrett.»
**Never say:** «bærekraftig», «miljøvennlig», «100 år gammelt tre» (no lot is dated), «solid malmfuru» (species unconfirmed).

### Proof 2 · The move is the idea (K-05, K-27)

The house is designed to be moved in one piece: built in the workshop, driven, lifted, set down. The journey section shows the three steps, and the copy keeps the goal a goal.

**Say:** «Målet er at huset skal kunne flyttes i ett stykke.»
**Never say:** a route, a crane, a delivery time, «kan løftes i dag», or the 3.25 m width without the height caveat ([K-27](../../../content/claims-register.csv) note: never without K-05).

### Proof 3 · We say where we are (K-19, K-26, K-14, K-20)

Status first, in the hero and the footer; a permit answer that says «det avhenger av hva huset skal brukes til, og det er kommunen som avgjør» and offers nothing it cannot keep; every image captioned «Konseptbilde».

**Say:** «Huset er under utvikling.» · «Tegninger og beregninger pågår. Prototypen er ikke bygget.» · «Det avhenger av hva huset skal brukes til, og det er kommunen som avgjør.»
**Never say:** «ingen byggesøknad», «TEK17-godkjent», «verifisert», «garantert».

---

## 3 · One call to action

The landing page opens with «Se huset» / “Explore the house”, which leads to the gallery. «Materialer» / “Materials” links directly to the material passports.

«Følg prosjektet» / “Follow the project” is the wording Carlos chose for the future email subscription (D1). The form awaits its provider and destination (D6).

---|---|
| Button, hero and header | «Følg prosjektet» |
| Form heading | «Følg prosjektet» |
| Submit | «Følg prosjektet» |
| Success | «Takk! Du følger nå prosjektet.» |
| Consent checkbox | «Ja, send meg oppdateringer om MiniHouse på e-post.» |
| Secondary action, hero | «Se alle bildene» |

Whatever the button says, it opens the same form. No modal, no second action competing with it. The button keeps its name at the moment of submission too: after the click the *state* changes to «Du følger nå prosjektet», and the button does not become «Send».

The form asks for an e-mail address (required) and a name (optional) and nothing else ([K-32](../../../content/claims-register.csv)).

---

## 4 · Hero message (the shape, not the final words)

| Slot | Constraint | Draft |
|---|---|---|
| Title | one line of thought, sentence case, no word in a different colour; **selected by Carlos (D12)** | «Et lite hus, laget for å flyttes.» — "A small house, made to be moved." The wording states the goal as intent (K-05), not as a capability. |
| Lead | at most 2 sentences, no numbers that need a status | «Vi tegner et hus for Bergen med gamle furubord utenpå, eik i tersklene og kobber rundt speilet på badet.» |
| Primary link | house gallery | «Se huset» |
| Secondary link | material passports | «Materialer» |
| Caption | the status of every image | «Konseptbilde» |
| Facts band | five values, each with a register row | Størrelse, Konstruksjon, Tak, Flytting, Status |

The draft lead uses "tenkt for vestlandsvær": that is the design principle ([K-21](../../../content/claims-register.csv)), not a performance claim. It must stay a principle; the moment copy says "tåler vestlandsvær", it needs a test.

---

## 5 · Message per audience

| Audience | What they need first | Message | Where |
|---|---|---|---|
| Homeowner with a plot | consent to imagine it on their land | the house, its size, the material, and a permit answer | hero, key facts, FAQ |
| Cabin owner | a second small building, no fuss | size, materials, transport | key facts, FAQ |
| Curious follower | what this is, that it is a project, how to follow it | status and the follow form | status, follow |
| Builders, crane firms, municipalities (secondary) | documents, revisions, states | "For fagfolk" to the documentation site | footer, docs site |

The emergency-cabin persona is gone (D11): the house is presented as a minihouse, not as a place to live urgently. The first three audiences are the promo page. The fourth is a link, not a section: the page never turns into a technical report.

---

## 6 · FINN kit: cancelled

PLAN 6.6 proposed an optional FINN ad. **D10 cancels it**: MiniHouse is not for sale, so there is no ad, no title and no sales description to write. The FINN listing stays a model for *presenting* a house (pictures first, key facts), not for selling one. The launch task D-10 therefore shrinks to the live check, the docs and the PROJECT.md lines.

---

## 7 · What we do not say, and why

| We never say | Because | Register |
|---|---|---|
| a price, "fra kr X", «Pris kommer», "bestill" | nothing is for sale | K-16, K-31 |
| "Meld interesse" | D1 replaced it with «Følg prosjektet» | D1 |
| a delivery time | no production plan | K-17 |
| a weight | not measured, the 3000 kg is hypothetical | K-18 |
| a U-value, "TEK17-godkjent" | not calculated | K-15 |
| "ingen byggesøknad" | depends on use class | K-14 |
| "bærekraftig", "miljøvennlig", "grønn" | vague environmental claim, no specific fact | DESIGN-GUIDE §9 |
| "unik", "revolusjonerende", "fremtidens" | hype, and unprovable | DESIGN-GUIDE §9 |
| "verifisert", "garantert", testimonials | nothing is verified or guaranteed | DESIGN-GUIDE §9 |
| a named species or origin for the timber | C-08 open | K-07, K-22 |
| a contact address we do not have | D6, no address recorded | K-24, K-29 |

The strongest sentence on the site is the one that admits what is not known yet. That is the tone: not apologetic, just exact.
