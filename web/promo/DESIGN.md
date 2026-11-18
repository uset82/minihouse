# Design System

The MiniHouse promo site's design system, written in the DESIGN.md format for design and code agents (the "/design style" from Carlos's WebDesigner plugin). It summarises [the design guide](../../fase4/promo/DESIGN-GUIDE.md), which holds every rule and wins on any difference. The colour values are copied from [tokens.css](src/styles/tokens.css), and `scripts/check_promo.py` checks that they match. Only Claude Code edits this file.

## Overview

«Patina, made funkier»: modern, funky and natural. Every colour is a material of the house, the colours of Norwegian woods and old fittings:
- lime plaster;
- pine tar;
- heartwood pine;
- oak;
- copper;
- verdigris.

They're laid out with modern calm: big pictures, few words, generous space, and text left-aligned and ragged right.

The funk comes from five moves. Each one comes from a real object of the house and is used once, in its place:
1. the wavy copper mirror frame;
2. the irr band;
3. giant wood-type numerals;
4. the copper follow band;
5. the malmfuru band that carries Carlos's question on the story page.

## Colors

- **Primary: kobber** (#A9481C): copper, the fittings. Only what you can press, on light grounds, plus the one mirror frame.
- **Secondary: malmfuru** (#9D5F30): heartwood pine. Large wood surfaces, numerals and display type of 24 px and up, and the story page's question band.
- **Tertiary: irr** (#2C4F40): verdigris and the petrol-glazed bathroom tile. The interior band.
- **Neutral: kalk** (#ECEAE4): lime plaster. The page ground.
- **Ink: tjære** (#241A13): pine tar. Text and the footer.
- **Eik** (#BA936B): oak. The key-facts band.
- **Kobber-mørk** (#8E3B16): copper on hover.
- **Kobber-lys** (#E08A52): copper on the dark bands (tjære and irr) only.
- **Sølvgrå** (#8C7E71): weathered cladding. Hairlines on kalk only.
- **Malmfuru-mørk** (#6F3F1E): captions and soft text on kalk.

## Typography

- **Headline font:** Besley, 700–800. A Clarendon revival: 19th-century wood type, letters cut in old wood.
- **Body font:** Jost, 400 and 500. A geometric sans for text and UI.
- **Label font:** Jost 500.

**Sizes:**
- Body text is 18 px, with a line height of 1.55 and at most 64 characters a line.
- Leads are 21 px and h3 is 24 px. h2 runs from 28 to 36 px, h1 from 44 to 72 px, and the journey numerals from 80 to 144 px.
- Headings use a line height of 1.08, letter-spacing of -0.01em and balanced wrapping.

**Style:** sentence case everywhere. No all caps, no letter-spaced labels, no monospace, and never one word picked out in italics, colour or bold.

## Elevation

None: no shadows, blur, gradients or glows. Depth comes from full-width bands of material colour, and from the few places where one thing overlaps another:
- the mirror over the living-room film;
- the numerals over their photos;
- the passport tags over their samples.

## Components

- **Buttons:** copper fill, kalk text, Jost 500, a 2 px radius, and at least 48 px high. On dark bands: a kobber-lys fill and tjære text. No icons and no arrows.
- **Links:** copper text with a 1 px underline at a 3 px offset.
- **Bands:** each section is one full-width band in one material colour. Neighbours never share a colour, except kalk next to kalk with a sølvgrå hairline between them.
- **Material passport:** a timber lot tag with a perforated stub and an eyelet, the signature element.
- **Images:** edge to edge of their column, with square corners and no frames. The caption sits below: «Konseptbilde».
- **The film:** silent, with one shared «Pause filmen» button in the caption row.

## Do's and Don'ts

- Do use copper only for what can be pressed.
- Do keep text left-aligned and ragged right, at most 64 characters a line.
- Do take every colour, size and space from tokens.css.
- Don't add colours, font sizes, shadows or radii.
- Don't use cream with terracotta, neon on black, identical shadowed cards, eyebrow labels, "→" on links, or 01 / 02 / 03 outside the journey.
- Don't put text on images or generate pictures. Images come from images.json.
- Don't use a funk move twice, or outside its place.
