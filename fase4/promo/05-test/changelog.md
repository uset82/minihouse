# Fixes

## 2026-11-17 · VR-02 · sticky bar left unmounted

Finding: `StickyBar.astro` is not in `Base.astro`. Antigravity asked for it to appear after the hero.

Disposition: left unmounted. D6 has no inbox, so there is no follow form. The bar’s only action is «Følg prosjektet», and the privacy page says this preview does not ask for an e-mail. Mounting the bar would add a control with nowhere to go. It goes back in when the form has a destination.

File: `web/promo/src/layouts/Base.astro` (no change). Status: deferred.

## 2026-11-17 · Journey frames · native size

Finding: the workshop picture is a 288×144 detail. A 4:3 frame enlarged it past the master.

Disposition: each journey figure keeps its own aspect ratio and cannot grow past its master width. On the desktop band the three pictures share a 144 px height. On a phone the picture sits beside the step text.

Files: `web/promo/src/components/Figure.astro`, `web/promo/src/components/Journey.astro`. Screenshots: `status/cursor-screens/journey-360.png`, `journey-1280.png`. Status: done, waiting on Antigravity's look at the crop.
