# POV and How-might-we · v0

**v0 draft, 2026-11-17.** Task D-3 (PLAN 2.1). Revise to v1 after the five interviews and the synthesis (D-8), before G2.

Basis: [PLAN.md](../PLAN.md) §1 and §6, [claims-register.csv](claims-register.csv), [kit.md](../01-empathize/kit.md) and [DESIGN-GUIDE.md](../DESIGN-GUIDE.md) §9. **Not yet available:** Carlos's questionnaire answers ([kit.md](../01-empathize/kit.md) §1) and the five interviews. **Excluded on purpose:** Antigravity's market scan (`01-empathize/market-scan.md`) stays out of D-3 until **CR-16** is closed ([claude-code-review.md](../review/claude-code-review.md)): it has no per-entry sources and one entry misdescribes the FINN listing, so nothing in it can carry a claim yet. Everything below that depends on research is marked **hypothesis** with the test that would falsify it.

The POV is about the buyer. It is not about the house, and it is not a slogan.

---

## 1 · Point of view

> **A homeowner in Bergen who has a plot and needs a small extra building needs to see that a movable house can be warm, solid and honestly made from old timber, because they have been burned by listings that photograph well and answer nothing: no permit answer, no proof of what the house is actually made of, no honest status.**

One sentence, one buyer, one tension. The buyer is not "everyone who likes small houses"; the site fails if it speaks to everyone. Since D11 the house is presented as a minihouse, so the emergency-cabin persona is off the page.

| Part of the POV | Where it comes from | Status |
|---|---|---|
| Bergen homeowner | market decision, [K-13](claims-register.csv) | bekreftet (market), the persona is not |
| small extra building on their plot | PLAN §1 audience hypothesis 1 | **hypothesis** |
| movable, in one piece | [K-05](claims-register.csv) — a goal, not a fact | mål |
| warm, solid | nothing in the register proves insulation or performance | **not claimable**: no U-value, no energy figure ([K-15](claims-register.csv)) |
| honestly made from old timber | [K-03](claims-register.csv), [K-06](claims-register.csv), [K-19](claims-register.csv) | konsept |
| burned by listings that answer nothing | PLAN §1 ("what we borrow from the FINN listing"), Appendix A | **hypothesis**, test in interview §3.3 |

The phrase "warm, solid" is a *need*, not a claim about the performance of this house. The site answers it with honesty (status, materials, documentation) rather than with a U-value it cannot prove. That distinction is the core of this brief.

---

## 2 · How might we

Five questions, ranked by how much they shape the page. Each names the section it seeds and the register rows it may use.

| # | How might we | Seeds | May use |
|---|---|---|---|
| HMW-1 | …show old timber as a quality rather than a compromise? | materials, material passport | K-03, K-06, K-07, K-08, K-21, K-22, K-23 |
| HMW-2 | …be honest that MiniHouse is still a concept and still make people want it? | hero status line, status and FAQ, footer note | K-19, K-20, K-26 |
| HMW-3 | …make "moved in one piece by crane" easy to picture without promising a route? | journey "Fra verksted til tomt" | K-05, K-27 |
| HMW-4 | …answer "can I put it on my plot?" without making a legal promise? | FAQ, key facts | K-13, K-14 |
| HMW-5 | …let a buyer judge the house without photos of a house that does not exist yet? | gallery, captions, image status | K-20, K-11, K-12 |

HMW-1 and HMW-2 are the two that decide the design direction: one is proof, the other is honesty. HMW-3 to HMW-5 are section-level.

A question we deliberately do **not** ask: "how might we make MiniHouse look bigger than it is?" The footprint is 18 m² gross ([K-02](claims-register.csv)) and the site says so.

---

## 3 · Assumptions to test

Each assumption has a falsifier. If a falsifier lands, this document changes before the copy does.

| ID | Assumption (v0) | Falsified when | Tested in |
|---|---|---|---|
| A-1 | The buyer's first question is "can I put it on my plot, and what is it made of?" | interviews lead with looks or with "is it for sale" | interview §3.2–3.3 |
| A-2 | "Reclaimed timber" reads as charm, not as a quality risk | 3 of 5 call it a risk or ask about rot first | interview §3.4 |
| A-3 | Saying "under development" lowers interest | people leave, or ask for proof of build, not for excuses | interview §3.6, 5-second test |
| A-4 | Visitors need something to do beyond reading | nobody asks how to follow the project, or the follow form gets no use in the test | interview §3.6, usability T5 |
| A-5 | Bergen buyers prefer Norwegian copy and would leave an English-first page | nobody switches to Norwegian, or all test in English | language link use, card sort |
| A-6 | The three personas are distinct enough to write for | all five interviewees fit one persona | synthesis D-8 |

A-7 (market) is not listed because there is no usable market evidence yet: the scan is excluded until CR-16 is closed. The patterns it should establish — what Nordic minihus sites show first, whether they publish a price, how they answer permits and transport — are recorded from PLAN Appendix A only, which is why A-1 and A-4 remain hypotheses.

---

## 4 · What the POV obliges the site to do

1. **Answer the permit question honestly, on the page.** The answer is «det avhenger av hva huset skal brukes til, og det er kommunen som avgjør» ([K-14](claims-register.csv)) — no badge, no promise, no offer of help we cannot staff.
2. **Put a status sentence above the fold.** "Under utvikling" ([K-19](claims-register.csv)) belongs in the hero, not in the footer.
3. **Show the material as evidence.** The passport carries species, origin, previous use and status ([K-22](claims-register.csv)), and says "documented per lot" where nothing is documented yet.
4. **Never fake a number and never sell.** No price and no «Pris kommer» ([K-16](claims-register.csv): nothing is for sale, [K-31](claims-register.csv)), no delivery ([K-17](claims-register.csv)), no weight ([K-18](claims-register.csv)), no U-value ([K-15](claims-register.csv)).
5. **Let the buyer see the house as it is.** Concept images, captioned ([K-20](claims-register.csv)), and a gallery that shows the inside honestly ([K-11](claims-register.csv), [K-12](claims-register.csv)).
6. **Give the visitor one thing to do.** «Følg prosjektet» ([K-30](claims-register.csv)) is the only action: an e-mail address, nothing else ([K-32](claims-register.csv)).

---

## 5 · Open questions for Carlos (blocking v1 and G2)

| # | Question | Why it blocks |
|---|---|---|
| Q-1 | Is the buyer a private person, a municipality, a landlord, or all three? Which one gets the hero? | The POV names one buyer; a split audience weakens the copy |
| Q-2 | Is the one-a-month update ceiling right, and when does the first update go out? | The privacy page has to state the frequency ([K-30](claims-register.csv)) |
| Q-3 | D6: where does the sign-up send, and what is the contact address? | The CTA promise is empty without a destination ([K-24](claims-register.csv), [K-29](claims-register.csv)) |
| Q-4 | Is "Bergen" the buyer's location or the project's? | A Bergen-only site is a different page from a Vestlandet site |

Until Q-1 and Q-3 are answered, the POV is a well-argued hypothesis, not an approved brief.
