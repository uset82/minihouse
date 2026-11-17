# Metrics · v0

**v0 draft, 2026-11-17.** Task D-3 (PLAN 2.4). One page: what success means, how it is measured, and what we refuse to measure.

Decision D9: **count form submissions only** — no cookies, no banner, no third-party analytics. That decision limits what is measurable, and this document must not pretend otherwise.
Basis: the claims register, [kit.md](../01-empathize/kit.md) and PLAN §10. Antigravity's market scan is **excluded** until CR-16 is closed ([claude-code-review.md](../review/claude-code-review.md)): none of its figures has a source, so it can justify no target or benchmark here.

---

## 1 · The one number

**Sign-ups to follow the project** — the count of valid e-mail addresses that complete the «Følg prosjektet» form, per week, from launch onwards.

- **Primary metric:** sign-ups, counted as one number. No personal data in the measurement, no cookie, no visitor identity.
- **What it cannot tell us:** a *rate*. "Sign-ups per 100 visitors" needs a visitor count, which D9 rules out. If Canner's own server dashboard reports request counts without cookies, the rate can be computed for information only; it is **not** a target and never goes on the page.
- **Test sign-ups** are excluded and marked as tests (the usability round uses an obvious test name and address).

Owner: Carlos reads the inbox and the list; DeepSeek records the count in the launch documentation. No automated counter is added to the site.

---

## 2 · What else we would like to know (and cannot, without instrumentation)

| Question | Why it matters | Status at v1 |
|---|---|---|
| Did people open the gallery? | the FINN pattern says pictures first | **not measured** — needs an event, and D9 forbids a tracker. Ask in the usability test instead (§4) |
| Did they read the materials section? | it is the differentiator | **not measured** — same reason |
| Did the language switch get used? | confirms Norwegian-first | **not measured** — ask in the usability test |
| Which image gets the most attention? | informs the second render round | **not measured** |

Say so, plainly, in the launch documentation. A metric that is not measured is not a metric, and inventing a proxy is how "we have analytics" becomes a lie.

---

## 3 · Quality gates with numbers (measurable, already planned)

These are the numbers the project can prove with tooling, and they are the ones that block launch.

| Gate | Target | How | Where |
|---|---|---|---|
| Accessibility | 0 axe violations on `/` and `/en/`, mobile and desktop | `npx @axe-core/cli` | `05-test/a11y.md` (D-7) |
| Performance | LCP ≤ 2.5 s, CLS ≤ 0.1, INP ≤ 200 ms | Lighthouse, mobile, simulated 4G | `05-test/perf.md` (D-7) |
| JavaScript budget | ≤ 50 KB gzipped | build output | `05-test/perf.md` |
| First load | ≤ 1.5 MB | network panel, cold cache | `05-test/perf.md` |
| Contrast | every text pair ≥ 4.5:1 (3:1 for large and UI) | `scripts/check_promo.py`, recomputed | D-6, D-9 |
| Claims | 0 unsupported sentences | audit against the register | `05-test/claims-audit.md` (D-9) |
| Images | no `stand-in` or `pending` in a release build | `check_promo.py --release` | D-6 |

If a gate fails, the finding goes to its owner (Cursor for code, Antigravity for the image cause, DeepSeek for the words) — the launch does not move.

---

## 4 · Human tests (the metrics that actually teach us)

These come from PLAN §10 and the kit, and they are pass/fail, not percentages of a sample of five.

| Test | Pass | Source |
|---|---|---|
| 5-second hero test | ≥ 4 of 5 say "a small movable house" **and** notice it is a concept | [kit](../01-empathize/kit.md) §5.1 |
| Preference test | one direction ranked first by ≥ 2 of 5, walked away from by ≤ 1 | [kit](../01-empathize/kit.md) §5.2 |
| Usability, five tasks | ≥ 4 of 5 complete each task | [kit](../01-empathize/kit.md) §6 |
| Permit answer | nobody concludes "no permit needed" after reading the FAQ | usability T4 |
| Status answer | nobody says "you can buy it today" after the hero | usability T2 |

Five people is a design test, not a survey. Report it as "4 of 5", never as a percentage of buyers.

---

## 5 · What we will not do

- No cookie banner, because there are no cookies (D9).
- No heatmap, no session recorder, no A/B test on a site with this little traffic: the sample would be noise, and the tooling would contradict D9.
- No "engagement" number (time on page, scroll depth) reported as success.
- No conversion rate invented from a server log and presented as a marketing fact.

---

## 6 · Success at G5

The launch is a success when, **on the live site and with evidence**:

1. the five gates in §3 pass;
2. the five human tests in §4 pass or the failures are accepted in writing by Carlos;
3. the claims audit finds no unsupported sentence;
4. the form delivers a marked test sign-up to the destination Carlos chose (D6) and the confirmation reads «Takk! Du følger nå prosjektet.»;
5. the first week's sign-up count is recorded in `docs/despliegue-web.md` with the date it was read.

Nothing here measures whether the house is good. It measures whether the site tells the truth about it, and whether someone can follow the project from that truth.
