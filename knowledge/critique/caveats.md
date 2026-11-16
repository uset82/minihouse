# Critique · source errors and validity limits

## C001 · McAvoy precedent cites EN 1993-1-2 for joint design

**Issue:** The Queen's University Belfast / McAvoy paper cited in the research report states its bracket was designed with reference to EN 1993-1-2:2005. The report correctly flags this as inappropriate.

**Verified 2026-11-16 against JRC's official EN 1993 part list (S004):**
- EN 1993-1-2:2005 = "General rules — **Structural fire design**"
- EN 1993-1-8:2005 = "**Design of joints**"

**Conclusion:** The report's correction is right. Do not use EN 1993-1-2 as a dimensioning standard for a lifting ear. Use EN 1993-1-8, supported by Jaspart & Weynand (S006). The mis-citation may be a bibliographic error in the paper; confirm against the original QUB PDF (Stage 3) before treating it as established.

**Status:** confirmed at primary source.

## C002 · steelconstruction.info is UK-only for National Annex values

**Issue:** The SCI page (S003) is useful for Eurocode structure and generation timing but its National Annex guidance applies to the UK, not Norway.

**Rule:** Use S003 for concepts only. Every γ, ψ, α factor for MiniHouse must come from the Norwegian NA (NS-EN …). Log as pending in Stage 6.

**Status:** recorded.

## C003 · The 3,000 kg beam is not the module

**Issue:** The report's illustrative numbers (24.634 mm / 1.490 mm, 1.2 m supports) are a hypothetical ideal beam. D001 reproduces them exactly but they must not be used as module deflections or as an optimal support layout.

**Status:** confirmed by D001 derivation; permanent gate in all calculation work.
