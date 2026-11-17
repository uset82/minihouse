#!/usr/bin/env python3
"""Automated checks for the MiniHouse promo site (PLAN D-6).

Standard library only. Three modes:

    python scripts/check_promo.py                  # source checks (tokens, content, images)
    python scripts/check_promo.py --dist web/promo/dist
                                                   # + built-site checks (HTML, CSS, links)
    python scripts/check_promo.py --selftest       # run this file's own tests
    python scripts/check_promo.py --release        # a release build: no stand-in/pending images

Exit code 0 when every check passes, 1 when any check fails.

The colour table and the allowed pairs live in fase4/promo/DESIGN-GUIDE.md §3. This
script recomputes every contrast ratio from the hex values instead of trusting the
table: a wrong number in either the guide or tokens.css is reported.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PROMO = ROOT / "web" / "promo"

# --- DESIGN-GUIDE §3 ---------------------------------------------------------

TOKENS = {
    "kalk": "#ECEAE4",
    "tjaere": "#241A13",
    "malmfuru": "#9D5F30",
    "eik": "#BA936B",
    "kobber": "#A9481C",
    "irr": "#2C4F40",
    "kobber-mork": "#8E3B16",
    "kobber-lys": "#E08A52",
    "solvgra": "#8C7E71",
    "malmfuru-mork": "#6F3F1E",
}

# (foreground, background, ratio in the guide, allowed use)
PAIRS = [
    ("tjaere", "kalk", 14.17, "body text, inputs"),
    ("kobber", "kalk", 4.81, "links, buttons, focus ring"),
    ("kalk", "kobber-mork", 6.26, "button hover"),
    ("malmfuru-mork", "kalk", 7.26, "captions, soft text"),
    ("tjaere", "eik", 6.07, "key facts, spec table"),
    ("kalk", "irr", 7.59, "text on the interior band"),
    ("tjaere", "kobber-lys", 6.43, "buttons on dark bands"),
    ("kobber-lys", "tjaere", 6.43, "links in the footer"),
    ("kobber-lys", "irr", 3.45, "button shape and focus ring only, never text"),
    ("malmfuru", "kalk", 4.24, "numerals and display type >= 24 px only"),
    ("solvgra", "kalk", 3.27, "hairlines and borders only"),
]

# Pairs the guide forbids. Keys match the guide's "never use" block.
FORBIDDEN_PAIRS = [
    ("kobber", "eik", 2.06),
    ("kobber-lys", "kalk", 2.20),
    ("solvgra", "eik", 1.40),
]

RATIO_TOLERANCE = 0.01

# --- DESIGN-GUIDE §9 ---------------------------------------------------------

BANNED_WORDS = {
    "nb": [
        "revolusjonerende",
        "unik",
        "drømmehjem",
        "sømløs",
        "innovativ",
        "fremtidens",
        "bærekraftig",
        "miljøvennlig",
        "grønn",
    ],
    "en": [
        "revolutionary",
        "unique",
        "dream home",
        "seamless",
        "elevate",
        "discover",
        "unlock",
        "experience",
        "eco-friendly",
        "sustainable",
        "green",
        "game-changing",
    ],
}

BANNED_PATTERNS = [
    (r"\bingen\s+byggesøknad\b", "claims no building permit is needed"),
    (r"\bsøknadsfri\w*", "claims no building permit is needed"),
    (r"\bTEK\s?17\b", "claims TEK17 compliance"),
    (r"\bU-?\s?verdi\b", "publishes a U-value"),
    (r"\bU-\s?\d", "publishes a U-value"),
    (r"\bgarantert\b", "guarantees something"),
    (r"\bverifisert\b", "claims something is verified"),
    (r"\b\d[\d\s.,]*\s?kr\b", "publishes a price"),
    (r"\bkr\s?\d", "publishes a price"),
    (r"\bNOK\b", "publishes a price"),
    (r"\bleveres\s+innen\b", "promises a delivery time"),
    (r"\bleveringstid\b", "promises a delivery time"),
    (r"\bveier\s+\d", "publishes a weight"),
    (r"\b\d+\s?kg\b", "publishes a weight"),
    (r"\b\d+\s?tonn\b", "publishes a weight"),
    (r"\bkundeomtale\w*", "uses a testimonial"),
    (r"\btestimonials?\b", "uses a testimonial"),
    (r"Meld interesse", "uses the superseded call to action (D1: «Følg prosjektet»)"),
    (r"Pris kommer", "uses the superseded price wording (D10: not for sale)"),
]

MAX_LINK_DEPTH = 4096


# --- contrast ----------------------------------------------------------------


def _channel(value: float) -> float:
    return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4


def relative_luminance(hexcolor: str) -> float:
    value = hexcolor.strip().lstrip("#")
    if len(value) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", value):
        raise ValueError(f"not a six-digit hex colour: {hexcolor!r}")
    r, g, b = (int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast_ratio(first: str, second: str) -> float:
    a, b = relative_luminance(first), relative_luminance(second)
    high, low = max(a, b), min(a, b)
    return (high + 0.05) / (low + 0.05)


# --- source checks -----------------------------------------------------------


def parse_css_variables(text: str) -> dict[str, str]:
    variables: dict[str, str] = {}
    for match in re.finditer(r"(--[a-zA-Z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\b", text):
        variables[match.group(1)[2:]] = match.group(2)
    return variables


def check_tokens(promo: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    path = promo / "src" / "styles" / "tokens.css"
    if not path.is_file():
        return [f"tokens.css not found at {path}"], notes
    declared = parse_css_variables(path.read_text(encoding="utf-8"))

    for name, expected in TOKENS.items():
        actual = declared.get(name)
        if actual is None:
            errors.append(f"tokens.css: --{name} is missing (guide: {expected})")
        elif actual.upper() != expected.upper():
            errors.append(f"tokens.css: --{name} is {actual}, guide says {expected}")

    ratios = 0
    for fg, bg, documented, _use in PAIRS:
        if fg not in declared or bg not in declared:
            continue
        computed = contrast_ratio(declared[fg], declared[bg])
        ratios += 1
        if abs(computed - documented) > RATIO_TOLERANCE:
            errors.append(
                f"contrast: {fg} on {bg} computes {computed:.2f}, "
                f"guide says {documented:.2f}"
            )
    for fg, bg, documented in FORBIDDEN_PAIRS:
        if fg not in declared or bg not in declared:
            continue
        computed = contrast_ratio(declared[fg], declared[bg])
        if abs(computed - documented) > RATIO_TOLERANCE:
            errors.append(
                f"contrast: forbidden pair {fg} on {bg} computes {computed:.2f}, "
                f"guide says {documented:.2f}"
            )

    notes.append(
        f"tokens: {len(declared)} variables, {ratios} pairs recomputed, "
        f"{len(FORBIDDEN_PAIRS)} forbidden pairs"
    )
    return errors, notes


def walk_strings(value, path: str = ""):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from walk_strings(child, f"{path}.{key}" if path else key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_strings(child, f"{path}[{index}]")


def compare_keys(left, right, path: str, errors: list[str]) -> None:
    if isinstance(left, dict) and isinstance(right, dict):
        for key in sorted(set(left) - set(right)):
            errors.append(f"keys: nb has {path}.{key}, en does not")
        for key in sorted(set(right) - set(left)):
            errors.append(f"keys: en has {path}.{key}, nb does not")
        for key in sorted(set(left) & set(right)):
            compare_keys(left[key], right[key], f"{path}.{key}", errors)
        return
    if isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            errors.append(f"keys: {path} has {len(left)} items in nb, {len(right)} in en")
        for index, (a, b) in enumerate(zip(left, right)):
            compare_keys(a, b, f"{path}[{index}]", errors)
        return
    if type(left) is not type(right):
        errors.append(f"keys: {path} is {type(left).__name__} in nb, {type(right).__name__} in en")


def banned_hits(text: str, language: str) -> list[str]:
    hits: list[str] = []
    lowered = text.lower()
    for word in BANNED_WORDS[language]:
        if re.search(r"\b" + re.escape(word) + r"\w*", lowered):
            hits.append(word)
    for pattern, why in BANNED_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append(why)
    return hits


def check_content(promo: Path, release: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    content_dir = promo / "src" / "content"
    loaded: dict[str, dict] = {}
    for language, filename in (("nb", "nb.json"), ("en", "en.json")):
        path = content_dir / filename
        if not path.is_file():
            errors.append(f"content: {filename} not found")
            continue
        try:
            loaded[language] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"content: {filename} is not valid JSON ({error})")

    if "nb" in loaded and "en" in loaded:
        compare_keys(loaded["nb"], loaded["en"], "", errors)

    todo = 0
    empty = 0
    omitted = 0
    words = 0
    for language, data in loaded.items():
        for path, value in walk_strings(data):
            if value == "TODO":
                errors.append(f"content: {language}.{path} is still TODO")
                todo += 1
                continue
            if value.strip() == "":
                # footer.contact is omitted on purpose until Carlos supplies an
                # address (claim K-29); the component renders nothing for it.
                if path == "footer.contact":
                    omitted += 1
                    continue
                errors.append(f"content: {language}.{path} is empty")
                empty += 1
                continue
            words += len(value.split())
            for hit in banned_hits(value, language):
                errors.append(f"content: {language}.{path} contains «{hit}»")

    if release:
        for language, data in loaded.items():
            body = data.get("privacy", {}).get("body", "")
            pending_notices = ("før lansering", "before launch", "har ingen påmelding", "has no sign-up form")
            if any(marker in body for marker in pending_notices):
                errors.append(
                    f"content: {language}.privacy.body describes an incomplete or inactive subscription "
                    "(D6 is open)"
                )

    notes.append(
        f"content: {len(loaded)} languages, {words} words, {todo} TODO, {empty} empty, "
        f"{omitted} omitted"
    )
    return errors, notes


def check_images(promo: Path, release: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    path = promo / "src" / "content" / "images.json"
    if not path.is_file():
        return [f"images: {path} not found"], notes
    try:
        images = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"images: images.json is not valid JSON ({error})"], notes
    if not isinstance(images, list):
        return ["images: images.json must be an array"], notes

    kinds = {"render", "photo", "texture"}
    statuses = {"approved", "pending", "stand-in"}
    for index, image in enumerate(images):
        where = f"images[{index}]"
        if not isinstance(image, dict):
            errors.append(f"{where} is not an object")
            continue
        identifier = image.get("id", where)
        for language in ("nb", "en"):
            for field in ("alt", "caption"):
                value = image.get(field, {})
                text = value.get(language) if isinstance(value, dict) else None
                if not isinstance(text, str) or text.strip() == "" or text == "TODO":
                    errors.append(f"images: {identifier} has no {field}.{language}")
        if image.get("kind") not in kinds:
            errors.append(f"images: {identifier} has an invalid kind")
        status = image.get("status")
        if status not in statuses:
            errors.append(f"images: {identifier} has an invalid status")
        source_file = image.get("file")
        if source_file is not None and not isinstance(source_file, str):
            errors.append(f"images: {identifier} has a non-string file")
        if release:
            if status != "approved":
                errors.append(f"images: {identifier} is {status} in a release build")
            if not isinstance(source_file, str) or source_file.strip() == "":
                errors.append(f"images: {identifier} has no file in a release build")

    approved = sum(1 for image in images if image.get("status") == "approved")
    notes.append(
        f"images: {len(images)} entries, {approved} approved, "
        f"{'release' if release else 'development'} mode"
    )
    return errors, notes


# --- built-site checks -------------------------------------------------------


def srcset_urls(value: str):
    """Read each candidate URL separately from its width or density descriptor."""
    while value:
        tokens = value.lstrip(" ,\t\n\r\f").split(None, 1)
        if not tokens:
            break
        url = tokens[0]
        yield url.rstrip(",")
        value = tokens[1] if len(tokens) > 1 else ""
        if not url.endswith(","):
            # The comma after the descriptor starts the next candidate. A comma
            # inside a URL, including a data URL, is part of the URL token.
            value = value.partition(",")[2]


class PageScan(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.lang_seen = False
        self.h1 = 0
        self.images: list[dict[str, str]] = []
        self.resources: list[tuple[str, str]] = []  # (attribute name, url)
        self.links: list[str] = []
        self.anchors: set[str] = set()
        self.text: list[str] = []
        self.styles: list[str] = []
        self.alt_texts: list[str] = []
        self._in_style = False

    @classmethod
    def from_file(cls, page: Path) -> PageScan:
        scan = cls()
        scan.feed(page.read_text(encoding="utf-8", errors="replace"))
        scan.close()
        return scan

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name: value or "" for name, value in attrs}
        if attributes.get("id"):
            self.anchors.add(attributes["id"])
        if tag == "a" and attributes.get("name"):
            self.anchors.add(attributes["name"])
        if tag == "html":
            self.lang_seen = True
            self.lang = attributes.get("lang")
        elif tag == "h1":
            self.h1 += 1
        elif tag == "img":
            self.images.append(attributes)
            self.alt_texts.append(attributes.get("alt", ""))
            for attribute in ("src", "poster"):
                if attributes.get(attribute):
                    self.resources.append((attribute, attributes[attribute]))
        elif tag in {"script", "iframe", "video", "audio", "source", "object"}:
            for attribute in ("src", "data"):
                if attributes.get(attribute):
                    self.resources.append((attribute, attributes[attribute]))
        elif tag == "link":
            rel = attributes.get("rel", "").lower()
            if attributes.get("href") and rel in {
                "stylesheet",
                "preload",
                "icon",
                "manifest",
                "modulepreload",
            }:
                self.resources.append(("href", attributes["href"]))
        if tag in {"img", "source"}:
            self.resources.extend(("srcset", url) for url in srcset_urls(attributes.get("srcset", "")))
        elif tag == "link" and attributes.get("rel") == "preload":
            self.resources.extend(("imagesrcset", url) for url in srcset_urls(attributes.get("imagesrcset", "")))
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])
        if tag == "style":
            self._in_style = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self.styles.append(data)
        elif data.strip():
            self.text.append(data)


def resource_is_external(url: str) -> bool:
    lowered = url.strip().lower()
    return (
        lowered.startswith("http://")
        or lowered.startswith("https://")
        or lowered.startswith("//")
    )


def css_rules(css: str):
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        yield match.group(1).strip(), match.group(2)


def check_css(css: str, where: str) -> list[str]:
    errors: list[str] = []
    if re.search(r"text-transform\s*:\s*uppercase", css, re.IGNORECASE):
        errors.append(f"{where}: text-transform: uppercase")
    if re.search(r"\bmonospace\b", css, re.IGNORECASE):
        errors.append(f"{where}: monospace font")
    if re.search(r"linear-gradient\s*\(", css, re.IGNORECASE):
        errors.append(f"{where}: linear-gradient")
    for selector, body in css_rules(css):
        if "box-shadow" not in body.lower():
            continue
        if re.search(r"lightbox|dialog", selector, re.IGNORECASE):
            continue
        errors.append(f"{where}: box-shadow outside the lightbox ({selector[:60]})")
    return errors


def resolve_internal(
    dist: Path, page: Path, url: str, anchors: dict[Path, set[str]] | None = None
) -> bool:
    if resource_is_external(url) or url.lower().startswith(("mailto:", "tel:", "data:", "javascript:")):
        return True
    try:
        parsed = urlsplit(url)
        path = unquote(parsed.path)
        if not path:
            target = page.resolve()
        elif path.startswith("/"):
            target = (dist / path.lstrip("/")).resolve()
        else:
            target = (page.parent / path).resolve()
        if not target.is_relative_to(dist.resolve()):
            return False
        if target.is_dir():
            target = target / "index.html"
        elif not target.is_file() and not target.suffix:
            target = target.with_suffix(".html")
        if not target.is_file():
            return False
    except (OSError, ValueError):
        return False
    fragment = unquote(parsed.fragment.partition(":~:")[0])
    if not fragment or fragment.lower() == "top" or target.suffix.lower() not in {".html", ".htm"}:
        return True
    if anchors is not None and target in anchors:
        return fragment in anchors[target]
    return fragment in PageScan.from_file(target).anchors


def check_dist(dist: Path, release: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    if not dist.is_dir():
        return [f"dist: {dist} is not a directory"], notes
    pages = sorted(dist.rglob("*.html"))
    if not pages:
        return [f"dist: no HTML under {dist}"], notes

    scans = {page: PageScan.from_file(page) for page in pages}
    anchors = {page.resolve(): scan.anchors for page, scan in scans.items()}
    for page, scan in scans.items():
        relative = page.relative_to(dist).as_posix()

        if not scan.lang_seen or not (scan.lang or "").strip():
            errors.append(f"{relative}: <html> has no lang")
        elif relative.startswith("en/") or relative == "en":
            if not (scan.lang or "").lower().startswith("en"):
                errors.append(f"{relative}: lang is «{scan.lang}», expected en")
        elif not (scan.lang or "").lower().startswith(("nb", "no")):
            errors.append(f"{relative}: lang is «{scan.lang}», expected nb or no")

        if scan.h1 != 1:
            errors.append(f"{relative}: {scan.h1} h1 elements, expected exactly one")

        for attributes in scan.images:
            if "alt" not in attributes:
                errors.append(f"{relative}: <img> without alt ({attributes.get('src', 'no src')})")
            elif attributes.get("alt", "").strip() == "":
                errors.append(f"{relative}: <img> with empty alt ({attributes.get('src', 'no src')})")
            if attributes.get("alt", "").strip() == "TODO":
                errors.append(f"{relative}: <img> with TODO alt")

        for attribute, url in scan.resources:
            if resource_is_external(url):
                errors.append(f"{relative}: external request in {attribute}: {url[:80]}")
            elif not resolve_internal(dist, page, url, anchors):
                errors.append(f"{relative}: {attribute} does not resolve: {url[:80]}")

        for href in scan.links:
            if resource_is_external(href):
                continue  # an outbound link is allowed; the footer points at the docs site
            if not resolve_internal(dist, page, href, anchors):
                errors.append(f"{relative}: link does not resolve: {href[:80]}")

        for text in scan.text:
            if "TODO" in text:
                errors.append(f"{relative}: TODO text in the built page")
            if "→" in text:
                errors.append(f"{relative}: «→» in text")
        for alt in scan.alt_texts:
            if "→" in alt:
                errors.append(f"{relative}: «→» in alt text")

        for style in scan.styles:
            errors.extend(check_css(style, f"{relative} <style>"))

        notes.append(f"{relative}: lang={scan.lang}, h1={scan.h1}, images={len(scan.images)}")

    for css_file in sorted(dist.rglob("*.css")):
        relative = css_file.relative_to(dist).as_posix()
        errors.extend(check_css(css_file.read_text(encoding="utf-8", errors="replace"), relative))

    notes.insert(0, f"dist: {len(pages)} pages")
    return errors, notes


# --- self-test ---------------------------------------------------------------


def selftest() -> int:
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if condition:
            print(f"PASS {name}")
        else:
            failures.append(f"{name}{': ' + detail if detail else ''}")
            print(f"FAIL {name} {detail}")

    check("contrast black/white is 21", abs(contrast_ratio("#000000", "#FFFFFF") - 21.0) < 0.01)
    check(
        "contrast matches the guide's tjaere/kalk",
        abs(contrast_ratio("#241A13", "#ECEAE4") - 14.17) < RATIO_TOLERANCE,
    )
    check(
        "tokens parse only hex variables",
        parse_css_variables(":root{--a:#FFFFFF;--b:4px;--c:var(--a)}") == {"a": "#FFFFFF"},
    )

    hits = banned_hits("Dette er en unik løsning", "nb")
    check("banned word «unik» is found", "unik" in hits, str(hits))
    check(
        "«petrolgrønn» is not the banned word «grønn»",
        "grønn" not in banned_hits("petrolgrønn flis", "nb"),
    )
    check(
        "a price in kroner is caught",
        any("price" in hit for hit in banned_hits("Fra 485 956 kr", "nb")),
    )
    check(
        "«Pris kommer.» is caught after D10",
        any("price" in hit for hit in banned_hits("Pris kommer.", "nb")),
    )
    check(
        "the new call to action passes",
        banned_hits("Følg prosjektet", "nb") == [],
        str(banned_hits("Følg prosjektet", "nb")),
    )
    check(
        "the superseded call to action is caught",
        any("superseded" in hit for hit in banned_hits("Meld interesse", "nb")),
    )

    errors: list[str] = []
    compare_keys({"a": {"b": "x"}}, {"a": {"c": "x"}}, "", errors)
    check("key parity catches a rename", len(errors) == 2, str(errors))
    errors = []
    compare_keys({"a": ["x", "y"]}, {"a": ["x"]}, "", errors)
    check("key parity catches a length change", len(errors) == 1, str(errors))

    scanner = PageScan()
    scanner.feed('<html lang="nb"><body><h1>En</h1><h1>To</h1><img src="/a.jpg"><a href="/b/">B</a></body></html>')
    check("html: h1 counted", scanner.h1 == 2, str(scanner.h1))
    check("html: lang read", scanner.lang == "nb", str(scanner.lang))
    check("html: img without alt recorded", scanner.images and "alt" not in scanner.images[0])
    check(
        "external resource detected",
        resource_is_external("https://fonts.googleapis.com/css")
        and not resource_is_external("/_astro/x.woff2"),
    )

    scan = PageScan()
    scan.feed('<img src="https://cdn.example.com/x.jpg" alt="a">')
    check(
        "external image is an external request",
        any(resource_is_external(url) for _attr, url in scan.resources),
    )

    scan = PageScan()
    scan.feed('<picture><source srcset="/small.avif 480w, /large.avif 960w">'
              '<img alt="House" srcset="house.jpg, https://example.org/large.jpg 2x"></picture>')
    check(
        "responsive image checking extracts local and external candidates",
        scan.resources == [
            ("srcset", "/small.avif"), ("srcset", "/large.avif"),
            ("srcset", "house.jpg"), ("srcset", "https://example.org/large.jpg"),
        ],
    )
    check(
        "a comma in a data URL stays inside its candidate",
        list(srcset_urls("data:image/png;base64,QUJD 1x,/wide.png 2x"))
        == ["data:image/png;base64,QUJD", "/wide.png"],
    )

    css = "h1{text-transform:uppercase}.card{box-shadow:0 2px 4px #000}.lightbox{box-shadow:0 2px 4px #000}"
    css_errors = check_css(css, "test.css")
    check(
        "css: uppercase and card shadow flagged, lightbox shadow allowed",
        len(css_errors) == 2 and any("uppercase" in error for error in css_errors),
        str(css_errors),
    )
    check("css: gradient flagged", len(check_css(".x{background:linear-gradient(#fff,#000)}", "t")) == 1)
    check("css: monospace flagged", len(check_css("p{font-family:monospace}", "t")) == 1)

    import tempfile

    with tempfile.TemporaryDirectory() as temporary:
        fixture = Path(temporary)
        (fixture / "en").mkdir()
        (fixture / "en" / "index.html").write_text(
            '<html lang="en"><h1 id="house">House</h1><a name="gallery"></a></html>', encoding="utf-8"
        )
        (fixture / "index.html").write_text(
            '<html lang="nb"><h1 id="spørsmål">Spørsmål</h1><a href="#missing">Én</a>'
            '<a href="/en/#missing">To</a><a href="/en/#house">Tre</a></html>', encoding="utf-8"
        )
        (fixture / "asset.png").write_bytes(b"")
        page = fixture / "index.html"
        check("links: / resolves to index.html", resolve_internal(fixture, page, "/"))
        check("links: /en/ resolves to en/index.html", resolve_internal(fixture, page, "/en/"))
        check("links: an asset resolves", resolve_internal(fixture, page, "/asset.png"))
        check("links: a missing target fails", resolve_internal(fixture, page, "/missing.png") is False)
        check("links: a URL-encoded ID resolves", resolve_internal(fixture, page, "#sp%C3%B8rsm%C3%A5l"))
        check("links: queries preserve fragment targets", resolve_internal(fixture, page, "en/?view=room#house"))
        check("links: a named anchor resolves", resolve_internal(fixture, page, "/en/#gallery"))
        check("links: a missing local ID fails", not resolve_internal(fixture, page, "#missing"))
        check("links: an ID on another page is not local", not resolve_internal(fixture, page, "#house"))
        check("links: IDs remain case-sensitive", not resolve_internal(fixture, page, "/en/#House"))
        check("links: an empty fragment still resolves", resolve_internal(fixture, page, "#"))
        check("links: a standard top fragment resolves", resolve_internal(fixture, page, "#top"))
        check("links: browser-handled non-HTML fragments resolve", resolve_internal(fixture, page, "/asset.png#xywh=1,2,3,4"))
        errors, _ = check_dist(fixture, release=False)
        check(
            "built pages report both missing fragment targets",
            errors == ["index.html: link does not resolve: #missing", "index.html: link does not resolve: /en/#missing"],
            str(errors),
        )
    check(
        "links: external urls are allowed",
        resolve_internal(Path("."), Path("x.html"), "https://example.com") is True,
    )

    print()
    if failures:
        print(f"selftest FAILED ({len(failures)})")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("selftest passed")
    return 0


# --- main --------------------------------------------------------------------


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="MiniHouse promo checks")
    parser.add_argument("--selftest", action="store_true", help="run the checks' own tests")
    parser.add_argument("--dist", type=Path, help="path to a built dist directory")
    parser.add_argument("--release", action="store_true", help="a release build")
    parser.add_argument(
        "--promo",
        type=Path,
        default=PROMO,
        help="path to the promo site (default: web/promo)",
    )
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    errors: list[str] = []
    notes: list[str] = []

    for collected_errors, collected_notes in (
        check_tokens(args.promo),
        check_content(args.promo, args.release),
        check_images(args.promo, args.release),
    ):
        errors.extend(collected_errors)
        notes.extend(collected_notes)

    if args.dist is not None:
        collected_errors, collected_notes = check_dist(args.dist, args.release)
        errors.extend(collected_errors)
        notes.extend(collected_notes)

    for note in notes:
        print(note)
    if errors:
        print()
        print(f"{len(errors)} problem(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print()
    print("check_promo: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
