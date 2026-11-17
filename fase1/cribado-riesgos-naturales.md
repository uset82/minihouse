# MiniHouse · TEK17 chapter 7 natural-hazard screening

**State:** PROCEDURE — NO SITE, NO HAZARD MAP, NO GEOTECHNICAL ASSESSMENT. This is a screening method and the arithmetic that can be done before a plot is chosen. It is not a siting approval, not a flood assessment and not a geotechnical report.

- Governing route: TEK17 §1-2(2)(a) admits **chapters 1–7 in full** on the mikrohus route.
- Requirements source: S026 (DIBK, TEK17 chapter 7).
- Assigned classes: **F2** for flood and **S2** for landslide.
- Both classes hold for a dwelling *and* for a holiday home, because both appear in the §7-2 and §7-3 lists — so the hazard route does **not** wait on C-01.

## 1. What the safety classes actually mean

The classes are expressed as a largest nominal annual probability of a damaging event. An annual probability is hard to feel; the same number over a service life is not.

| Class | Hazard | Return period | Annual | At least once in 25 y | 50 y | 75 y | MiniHouse |
|---|---|---:|---:|---:|---:|---:|---|
| F1 | flood / storm surge | 1/20 | 5.00% | 72.3% | 92.3% | 97.9% | — |
| F2 | flood / storm surge | 1/200 | 0.50% | 11.8% | 22.2% | 31.3% | **yes** |
| F3 | flood / storm surge | 1/1000 | 0.10% | 2.5% | 4.9% | 7.2% | — |
| S1 | landslide | 1/100 | 1.00% | 22.2% | 39.5% | 52.9% | — |
| S2 | landslide | 1/1000 | 0.10% | 2.5% | 4.9% | 7.2% | **yes** |
| S3 | landslide | 1/5000 | 0.02% | 0.5% | 1.0% | 1.5% | — |

The headline is uncomfortable and worth stating plainly: **F2 at 1/200 is a 22% chance of being exceeded at least once in 50 years.** That is not a defect in the requirement — it is what a 1/200 target means when the building is expected to stand for decades. The requirement is met by *placing* the building where that event does not reach it, which is why chapter 7 is a siting chapter.

Two refinements that soften the numbers for a small building:

- **Outdoor area:** for S2 buildings the associated outdoor area may be assessed at the **S1 level (1/100)**, because exposure time outdoors is shorter. It does not change the class for the building itself.
- **The classes are nominal annual probabilities of a damaging event, not predictions.** They are a design target set by the regulation, not a statement about a particular slope.

## 2. The gate sequence

The order matters, because each gate can stop the plot and each one is cheaper than the next.

| Gate | Question | Evidence | Can stop the plot? |
|---|---|---|---|
| **A** | Where exactly is the plot, and what finished floor level is intended? | coordinates, boundary, access, planned FFL | yes — without these nothing below can be answered |
| **B** | Does the plot intersect a mapped hazard zone? | NVE hazard maps (flood, avalanche, rockfall, debris flow, quick clay), municipal plan hazard zones | yes |
| **C** | Is the plot below the **marine limit**? | NGU loose-material maps, marine-limit line | no, but it forces gate D |
| **D** | Does a special regime apply (quick clay, great depth or strong current)? | NVE quick-clay database, flood-depth/velocity data | yes |
| **E** | Can the hazard be avoided, secured against, or designed for? | §7-2/§7-3 mitigation routes | yes |
| **F** | What does the specialist report say? | geotechnical report, flood assessment, municipal confirmation | yes |

Gate B is a desk exercise and takes an afternoon. Gate F costs money. The whole point of the sequence is to spend the afternoon before spending the money.

## 3. Flood: what the finished floor has to clear

§7-2 can be met by placing the building outside the area, by securing it against flooding, or by designing it to withstand inundation without danger to people or major material damage. Whichever route is taken, the number that matters is the finished floor level.

Three things add to the mapped flood level, and only one of them is in the regulation:

1. **The mapped 1/200 level** for the site.
2. **Sea-level rise over the service life.** §7-2's guidance explicitly requires expected climate change and sea-level rise to be taken into account for storm surge. A cabin near the Bergen shoreline cannot be assessed against today's sea level.
3. **A margin.** No freeboard figure was retrieved from TEK17, so the value below is a **project choice, not a regulatory number**, and it is labelled as such in every row.

Worked sensitivity with a hypothetical mapped level of **1250 mm** above chart datum and a **300 mm** margin. The mapped level is an example, not a Bergen value:

| Sea-level rise | 25 y allowance | 50 y | 75 y | FFL for 25 y | 50 y | 75 y |
|---:|---:|---:|---:|---:|---:|---:|
| 0 mm/yr | 0 | 0 | 0 | 1550 mm | 1550 mm | 1550 mm |
| 2 mm/yr | 50 | 100 | 150 | 1600 mm | 1650 mm | 1700 mm |
| 4 mm/yr | 100 | 200 | 300 | 1650 mm | 1750 mm | 1850 mm |
| 6 mm/yr | 150 | 300 | 450 | 1700 mm | 1850 mm | 2000 mm |
| 8 mm/yr | 200 | 400 | 600 | 1750 mm | 1950 mm | 2150 mm |

Read the table as a rate, not a prediction: **every 1 mm/yr of local sea-level rise adds 50 mm over a 50-year life.** The rate itself has to come from Kartverket for the actual site, and the service life is a project decision that has not been taken.

**A light building is not a protected building.** The §7-2 guidance says that where a flood area would have **great depth or strong current**, the **F3 level (1/1000) should be used** instead of F2. A cabin is light relative to its volume and can float or be pushed before it is submerged, so this escalation is a real consideration for this project, not a technicality.

## 4. Landslide: when a plot is obviously marginal

§7-3 requires the building **and its outdoor area** to be placed, designed or secured so that the class probability is not exceeded. For soil slopes the cheapest first question is whether the slope is anywhere near stable at all.

The infinite-slope model below is the standard textbook screen. It assumes a planar, homogeneous, infinitely long slope with no vegetation, no structure and no anchors — none of which is true of a real Bergen hillside. It is included because it is **conservative enough to reject a plot** and because it makes the dependence on slope angle and friction explicit.

Dry slope, no cohesion, unit weight 18 kN/m³, sliding plane at 2.0 m. FS = tan φ / tan β. Required FS is taken as **1.4** (material factor for field-assessed friction); the Norwegian National Annex is not available (S014), so **that factor is unverified** and is flagged rather than trusted.

| Slope β | φ = 30° | 32° | 34° | 36° |
|---:|---:|---:|---:|---:|
| 20° | 1.59 | 1.72 | 1.85 | 2.00 |
| 25° | 1.24 ! | 1.34 ! | 1.45 | 1.56 |
| 30° | 1.00 ! | 1.08 ! | 1.17 ! | 1.26 ! |
| 35° | 0.82 ✗ | 0.89 ✗ | 0.96 ✗ | 1.04 ! |
| 40° | 0.69 ✗ | 0.74 ✗ | 0.80 ✗ | 0.87 ✗ |

`✗` fails in the model · `!` below the material factor · unmarked is still not a pass.

- **At β = 30° and φ = 32° the factor is about 1.08.** A 30° soil slope is already marginal before any water is added, and pore pressure only makes it worse: the `(1 − ru)` term cuts the resisting side directly.
- **At 35° every friction angle in the table is at or below the material factor, and at 40° every one fails outright.** That is not a reason to reject every steep Bergen plot — much steep terrain there is **rock**, where this model does not apply at all and the hazard is rockfall, assessed differently. It is a reason to know which one the plot is on.
- **Cohesion and suction are what hold real slopes**, and both are lost when a slope saturates. A dry-season factor of safety is not a factor of safety.

## 5. What the ~50 kPa ceiling means

§7-3 allows a building to be **designed to withstand** landslide forces where the loads are not too large, and the guidance puts the practical ceiling at approximately **50 kPa**. In physical terms that is:

- about **5099 kg/m²** — roughly 5.1 tonnes pressing on every square metre;
- equivalent to the weight of about **2.8 m of soil** at 18 kN/m³.

That is a real load, but it is a **small-event** load. A cabin designed for 50 kPa is designed for the edge of the acceptable range, not for a debris flow that carries boulders. Above that ceiling the only routes left are siting and protective works — which is why the ceiling is a siting criterion in disguise.

## 6. Quick clay: the gate that has no arithmetic

Quick clay is not screened by a factor of safety on a slope. §7-3 requires an equivalent safety level for **kvikkleireskred**, and the guidance expands this into *områdeskred* — area landslides in quick clay and other soils with brittle failure — following NVE guide 1/2019.

Three properties make it unlike the rest of chapter 7:

- **The landslide can be far larger than the project.** A hazard zone can extend well beyond the plot, so a stable-looking site can sit inside an unstable area.
- **Below the marine limit the ground must be investigated even outside identified hazard zones.** Bergen has marine-limit terrain, so this is a live requirement for this project, not a formality.
- **The investigation scope is set by a tiltakskategori** (K0–K3) derived from the consequence for the project. The guidance's K0 examples are small interventions with very limited ground works and no influx of people — garages, boat houses, extensions, detached outhouses, tool sheds. **A new dwelling is not on that list**, so a cabin placed as a dwelling cannot be assumed to be K0.

There is no calculation here because there is nothing to calculate: the answer is a geotechnical report by a qualified person, and the only project decision is whether to pay for it on this plot.

## 7. Decision rules

Short forms for the site search. Each one is a stop, not a preference:

| Finding | Consequence |
|---|---|
| Plot intersects a mapped 1/1000 landslide zone | Not buildable as S2 without protective works or a documented equivalent safety level |
| Plot intersects a mapped 1/200 flood zone | Place outside, raise, secure, or design to withstand; otherwise the plot fails |
| Flood area with great depth or strong current | Escalate to **F3 (1/1000)**, not F2 |
| Plot below the marine limit | Geotechnical investigation required **regardless of mapping** |
| Plot in a quick-clay zone or an area-landslide zone | Siting question first; NVE 1/2019 and a tiltakskategori apply |
| Slope steeper than ~35° in soil | Treat as marginal until a geotechnical report says otherwise |
| Slope steeper than ~35° in rock | Different hazard (rockfall); the soil model in §4 does not apply |

## 8. What transportability does and does not change

- **It does not reduce the requirement.** TEK17 assesses the building where it stands. The fact that the cabin *can* be moved does not lower the class at the site it occupies.
- **It does change the paperwork.** The hazard assessment is not a one-time document for the cabin; it is a **per-deployment check** that has to be repeated for every new site over the cabin's life. That is a genuine operational burden of the concept and belongs in the deployment procedure, not only in the design file.
- **It changes the mitigation economics.** Raising a floor or adding a flood-resistant plinth is cheaper on a 18 m² module than on a house, and a cabin that is designed for F3 from the start does not need a new assessment when it moves to a worse plot.

## 9. Limits

- **The screen has no pass state.** It can escalate a plot to "needs a geotechnical report" and it can escalate it to "needs one urgently". It cannot clear a plot, and nothing below should be read as if it could.
- **No hazard map has been consulted.** This document records requirements and a method, not a finding about any plot.
- **No geotechnical, flood or storm-surge assessment has been made** and none can be made by the agent. Those are specialist reports by qualified people.
- The infinite-slope model in §4 ignores cohesion, suction, vegetation, structure, anchors and three-dimensional effects, and does not apply to rock slopes.
- The material factor 1.4 is unverified against the Norwegian National Annex (S014).
- The 300 mm flood margin is a **project choice**, not a TEK17 figure.
- Nothing here is a siting approval, a building permit input or a compliance certificate.

## 10. Source and status

- TEK17 §§7-1…7-4: S026 (DIBK, retrieved 2026-11-17).
- Class assignment F2/S2: S026, §7-2 and §7-3 pre-accepted lists.
- Generated by `scripts/natural_hazard_screen.py`; JSON companion: `knowledge/comparisons/natural-hazard-screen.json`.
- SCREENING ONLY — no plot accepted, no plot rejected, no design released.
