# Claims audit · v1

Task D-9 (PLAN 5.7). 2026-11-17, 23:35 for the source and 23:55 against the 23:29 build. Audited: `web/promo/src/content/nb.json` and `en.json`, and the rendered landing at `web/promo/dist/index.html` and `/en/index.html`.

Method: every sentence on the page read against [claims-register.csv](../02-define/claims-register.csv). A sentence passes when its row exists, the row's status admits the wording, and the wording adds no detail the row does not carry.

**Verdict: the rendered landing page carries no unsupported claim.** One latent contradiction and one colour wording need a decision from the copy owner, and the name check is half done.

---

## 1 · Correction to the first pass: the privacy contradiction is latent, not live

My first pass said the privacy page contradicted the follow form. Against the **rendered** page that is wrong, and I am correcting it:

- The 23:29 landing build has **no form, no input fields and no «Følg prosjektet» button** in either language. `interest.*` and `nav.cta` exist in the content files but the D13 landing layout does not mount them.
- So the sentence «Denne siden har ingen påmelding og ber ikke om navn eller e-postadresse» is **true of the page as it stands today**.
- It becomes **false the moment the follow form or the header CTA is mounted** (D1, C-6). The privacy text also carries none of the D-5 content: what is collected, why, who receives it, how long it is kept, how to have it deleted, the frequency and the unsubscribe promise (K-30, K-24).

**Decision needed, not a silent copy fix:** either the landing keeps no form — then the privacy page is fine and `interest.*` and `nav.cta` are dead content that should be removed or parked — or the follow form ships and the privacy page must be replaced by the D-5 text before G4. Owner: Carlos, with Cursor for the build. My proposed text is in the copy deck, `privacy.body`, and stays blocked until D6 names the recipient.

## 2 · The copy batch from the first pass

| # | Item | State |
|---|---|---|
| 1 | Bathroom «mørke fliser» → petrol-green | **fixed** (nb «petrolgrønne fliser»; en "deep teal tiles" — a rendering of the same colour, accepted, but it should say petrol-green if the team wants parity with K-23/K-34) |
| 2 | Bench cushion | **fixed** — «En innebygd benk under vinduet» / "A built-in bench under the window" |
| 3 | Drawer depth | **fixed** — «Skuffer under benken» / "Drawers under the bench" |
| 4 | Kitchen worktop and «dempede fronter» | **fixed** — «Et lite kjøkken langs veggen» / "A small kitchen along the wall" |
| 5 | Timber floor under the steel frame | **fixed** — «stålrammen under huset» / "the steel frame sits beneath the house" |
| 6 | `meta.title` middle dot | **fixed by the team** — «MiniHouse for Vestlandet» / "MiniHouse for Western Norway" (no separator at all) |
| 7 | `meta.description` «Utforsk»/«Explore» | **fixed by the team** — both now open with «Et huskonsept for Bergen …» / "A house concept for Bergen …" |

Some of this was fixed by the team in parallel with me; the two of us edited the same rows within minutes. The file is consistent now, and `check_promo.py` and `check-content.mjs` both pass on the source.

## 3 · What the rendered page says, and its rows

| Section | Sentence | Rows |
|---|---|---|
| Hero | headline; «Vi tegner et hus for Bergen med gamle furubord utenpå, eik i tersklene og kobber rundt speilet på badet.» | K-01, K-03, K-05, K-06, K-07, K-08, K-13, K-23 |
| Facts | size, construction, roof, moving goal, status | K-01, K-03, K-04, K-05, K-19 |
| Gallery | «Huset i bilder», «Konseptbilde» captions | K-20 |
| Materials lead | old boards as cladding; passport records origin and previous use | K-06, K-22 |
| Malmfuru | reddish-brown heartwood used in Norwegian cladding; looking for old boards | **K-33** (team row, Treteknisk and Riksantikvaren sources) |
| Eik | oak where the hand rests and the foot crosses | K-08 |
| Kobber | copper edge around the mirror in the sketch | K-23, K-34 |
| Stål | steel frame beneath the house, tying the base | K-03 |
| Living | kitchen and window seat share one room; bathroom at one end | K-10, K-12 |
| Journey | built indoors, moved in one piece, lifted onto supports | K-05 |
| Status | «MiniHouse finnes foreløpig på tegnebordet», three phases | K-19, K-26 |
| FAQ | permit, not for sale, no prototype date, moving, concept images, timber | K-14, K-31, K-17, K-05, K-27, K-20, K-06, K-07, K-22 |
| Footer | images note; «For fagfolk» to the docs site | K-19, K-20, K-28 |

Every one of those rows was read in the register, not assumed. The only unverified source is the team's K-33 pair of external references (Treteknisk «Fokus på tre» nr. 34 and Riksantikvaren 2023), which I have not fetched; that check belongs at G4.

## 4 · Environmental claims

None. `bærekraftig`, `miljøvennlig`, `grønn`, `sustainable`, `eco-friendly` and `green` do not occur in either content file; `check_promo.py` enforces that and passes. «Gjenbrukt tre» and «gamle furubord» are material descriptions whose sourcing is stated as open (K-07, K-22), which is the specific-and-documented route the guidance asks for.

Forbrukertilsynet's guidance on environmental claims: <https://www.forbrukertilsynet.no/lov-og-rett/veiledninger-og-retningslinjer/>, read 2026-11-17. **Limitation:** every URL on that host, including the root, returned their 404 page to this environment's fetcher, so the current wording could not be read; the check is against the guide's §9 rule set and will be re-read before G5.

## 5 · Name risk

- **Brønnøysundregistrene**, 2026-11-17, open API `https://data.brreg.no/enhetsregisteret/api/enheter?navn=MiniHouse` → **0 hits**. No company named MiniHouse is registered there today. Company-name check only.
- **Patentstyret: not checked.** No browser route from this environment. Owner: Carlos or Cursor before G5; record the result here.
- The name is descriptive, which makes it harder to protect and easier for others to use. Not legal advice; a flag for G5.

## 6 · Fix list

| # | Owner | Item | Status |
|---|---|---|---|
| 1 | Carlos + Cursor | Decide whether the landing ships the follow form; if yes, replace the privacy text with the D-5 version | **open, decision** |
| 2 | DeepSeek | Five softeners and two metadata fixes | **done** |
| 3 | Cursor | Rebuild after the copy changes; the 23:29 build predates the kitchen, bench and storage edits | open |
| 4 | Carlos or Cursor | Patentstyret search | open, before G5 |
| 5 | DeepSeek | Re-run the built-page audit after the rebuild | open |

The built-page re-run is the only step left in D-9's own done-when. Everything else is a decision or a Cursor build.
