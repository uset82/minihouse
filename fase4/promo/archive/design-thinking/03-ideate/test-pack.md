# Test Pack · Designretninger (Gate G3)

Dato: 2026-11-17.
Ansvarlig: Antigravity (Oppgave A-4, PLAN §3.2–3.3 og Gate G3).
Testskriptforfatter: DeepSeek ([01-empathize/kit.md §5](../01-empathize/kit.md)).
Testmateriell: [style-tiles/index.html](style-tiles/index.html).

---

## 1. Testens formål og oppsett

Gate G3 avgjør hvilken av de tre designretningene (**A · Patina**, **B · Hytte '74**, eller **C · Stavkirke**) som velges for den videre byggingen av MiniHouse-nettsiden:
- Testen gjennomføres med **5 deltakere** (P1–P5) fra målgruppen (tomteeiere, hytteinteresserte, folk som vurderer anneks).
- Testen består av to deler:
  1. **5-sekunders test av Hero (360 px mobilvisning):** Måler umiddelbar forståelse av hva MiniHouse er og at det er et konsept.
  2. **Preferanse- og tillitstest av de tre retningene (360 px og 1280 px):** Måler emosjonell appell, tillit til kvalitet/treverk, og hva brukerne ville valgt eller forkastet.

---

## 2. Testmateriell (Style Tiles)

Hver retning er implementert som en fullverdig, responsiv style tile med identisk innhold (Hero + Materialpass for malmfuru):

| Retning | Karakteristikk | Filplassering |
|---|---|---|
| **A · Patina** (Anbefalt) | Kalkbunn (`#ECEAE4`), tjæresort tekst (`#241A13`), kobber på knapper/lenker (`#A9481C`), Besley 800 + Jost. Arkitektonisk og verdig. | [style-tiles/direction-a-patina.html](style-tiles/direction-a-patina.html) |
| **B · Hytte '74** | Varm furubunn (`#F6EBD9`), rya-oransje aksent (`#D4561D`), dyp nøttebrun tekst, myke Cooper-serifer. Nostalgisk hyttevarme. | [style-tiles/direction-b-hytte74.html](style-tiles/direction-b-hytte74.html) |
| **C · Stavkirke** | Dyp tjæresort bunn (`#171412`), pergamenthvit tekst (`#EDE6DC`), utskårne skarpe serifer, glimt av brent kobber. Mørk og historisk. | [style-tiles/direction-c-stavkirke.html](style-tiles/direction-c-stavkirke.html) |
| **Sammenligningsvisning** | Samlet oversikt med direkte lenker til alle tre retninger. | [style-tiles/index.html](style-tiles/index.html) |

---

## 3. Del 1 · 5-sekunders test av Hero

*Instruksjon:* Vis mobilheroen (360 px) for én retning av gangen på skjerm i nøyaktig 5 sekunder. Skjul deretter bildet helt før spørsmålene stilles. Ikke la deltakeren scrolle eller zoome.

### Manuskript (Ordrett fra kit.md §5.1)
> **NO:** «Du får se et bilde i fem sekunder. Etterpå skjuler jeg det og stiller tre spørsmål. Se så mye du klarer.»  
> **EN:** "You'll see an image for five seconds. Then I'll hide it and ask three questions. Look as much as you can."

### Spørsmål (i denne rekkefølgen)
1. **«Hva var dette?»** *(Registrer deltakerens egne ord).*
2. **«Var det noe du kunne kjøpt i dag?»** *(Ja / Nei / Vet ikke – noter begrunnelsen).*
3. **«Hvem tror du det er for?»** *(Registrer målgruppeoppfatning).*

### Krav for å bestå (Pass criteria)
- Minst **4 av 5 deltakere** må umiddelbart oppfatte at dette er et lite flyttbart trehus.
- Minst **4 av 5 deltakere** må oppfatte at huset er et **konsept under utvikling** (ikke en ferdig vare på lager for umiddelbart kjøp). En hero som skjuler konseptstatusen stryker, uansett hvor godt deltakerne liker bildet.

---

## 4. Del 2 · Preferansetest av de tre retningene

*Instruksjon:* Vis alle tre retningene i samme størrelse (først 1280 px desktop, deretter 360 px mobil). Roter visningsrekkefølgen for hver deltaker (A-B-C, B-C-A, C-A-B, etc.) for å unngå posisjonsbias.

### Manuskript (Ordrett fra kit.md §5.2)
> **NO:** «Her er tre retninger for samme hus. Jeg vil at du ser på dem og sier hvilken som føles mest som et norsk hus laget av gammelt tre. Det finnes ikke noe riktig svar.»  
> **EN:** "Here are three directions for the same house. Look at them and tell me which feels most like a Norwegian house made of old wood. There is no right answer."

### Spørsmål (i denne rekkefølgen)
1. **«Hvilken liker du best? Hvorfor akkurat den?»**
2. **«Hvilken ville du stolt på hvis du skulle kjøpe?»**
3. **«Hvilken ville du gått fra?»**
4. **«Er det noe fra de andre du ville tatt med?»**

### Krav for å bestå (Pass criteria fra kit.md §5.2)
- En retning er godkjent og brukbar når den er **rangert som best av minst 2 av 5 deltakere**, og **forkastet («gått fra») av høyst 1 deltaker**.
- Dersom ingen av retningene oppfyller begge kravene, er dette et formelt avviksfunn for Gate G3 som skal rapporteres ærlig til Carlos i [decisions.md](../../../decisions.md), fremfor å tvinge igjennom den minst dårlige løsningen.

---

## 5. Resultatprotokoll (Skjema for Carlos)

Fylles ut under testgjennomføringen:

| Deltaker | Rekkefølge vist | Liker best (1. valg) | Høyest tillit | Ville gått fra | Begrunnelse (ordrett sitat) | Elementer å låne |
|---|---|---|---|---|---|---|
| **P1** | A – B – C | | | | | |
| **P2** | B – C – A | | | | | |
| **P3** | C – A – B | | | | | |
| **P4** | A – C – B | | | | | |
| **P5** | B – A – C | | | | | |

---

## 6. Neste steg etter testen (Gate G3)

1. Carlos oppsummerer stemmene og notatene i [decisions.md](../../../decisions.md) under Gate G3.
2. Ved valg av **Retning A (Patina)** fortsetter Cursor byggingen i `web/promo/` med eksisterende tokens.
3. Dersom testen peker mot **Retning B** eller **Retning C**, oppdateres kun `tokens.css` og fontvalg i Astro-bygget uten at informasjonsarkitekturen, tekstene eller bildene må bygges om.
