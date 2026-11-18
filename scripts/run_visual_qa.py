import os
import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path("fase4/promo/qa/screens/qa")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://127.0.0.1:4322"

def run_qa():
    results = {
        "breakpoints": [],
        "keyboard_focus": [],
        "reflow_320": {},
        "reduced_motion": {},
        "metadata": {}
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. Breakpoints testing: Norwegian, English, Personvern, 404
        pages_to_test = [
            ("nb-home", f"{BASE_URL}/"),
            ("en-home", f"{BASE_URL}/en/"),
            ("nb-personvern", f"{BASE_URL}/personvern/"),
            ("en-personvern", f"{BASE_URL}/en/personvern/"),
            ("404", f"{BASE_URL}/nonexistent-test-404")
        ]

        breakpoints = [
            (360, 800, "360px"),
            (768, 1024, "768px"),
            (1280, 900, "1280px"),
            (1920, 1080, "1920px")
        ]

        print("--- Testing Breakpoints ---")
        for page_name, url in pages_to_test:
            # For personvern and 404, we test 360 and 1280
            bps = breakpoints if "home" in page_name else [(360, 800, "360px"), (1280, 900, "1280px")]
            for w, h, bp_name in bps:
                context = browser.new_context(viewport={"width": w, "height": h})
                page = context.new_page()
                resp = page.goto(url, wait_until="networkidle")
                status = resp.status if resp else 0

                # Check horizontal overflow
                overflow = page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
                scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
                inner_w = page.evaluate("() => window.innerWidth")

                shot_path = OUT_DIR / f"{page_name}-{bp_name}.png"
                # For 1280 and 360 full page capture or viewport
                page.screenshot(path=str(shot_path), full_page=False)

                # For home 360 & 1280, also capture full page
                if "home" in page_name and bp_name in ["360px", "1280px"]:
                    full_shot = OUT_DIR / f"{page_name}-{bp_name}-full.png"
                    try:
                        page.screenshot(path=str(full_shot), full_page=True)
                    except Exception as e:
                        print(f"Full page shot error for {page_name}-{bp_name}: {e}")

                results["breakpoints"].append({
                    "page": page_name,
                    "viewport": bp_name,
                    "width": w,
                    "height": h,
                    "status": status,
                    "overflow": overflow,
                    "scrollWidth": scroll_w,
                    "innerWidth": inner_w,
                    "screenshot": str(shot_path)
                })
                print(f"[{page_name}] {bp_name}: status={status}, overflow={overflow} ({scroll_w}/{inner_w})")
                context.close()

        # 2. Reflow / 320 px & 200% zoom check (WCAG 1.4.10)
        print("\n--- Testing 320px Reflow ---")
        context_320 = browser.new_context(viewport={"width": 320, "height": 640})
        page_320 = context_320.new_page()
        page_320.goto(f"{BASE_URL}/", wait_until="networkidle")
        overflow_320 = page_320.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
        scroll_w_320 = page_320.evaluate("() => document.documentElement.scrollWidth")
        page_320.screenshot(path=str(OUT_DIR / "reflow-320px.png"))
        results["reflow_320"] = {
            "overflow": overflow_320,
            "scrollWidth": scroll_w_320,
            "innerWidth": 320,
            "screenshot": str(OUT_DIR / "reflow-320px.png")
        }
        print(f"320px reflow: overflow={overflow_320} (scrollWidth={scroll_w_320}, innerWidth=320)")
        context_320.close()

        # 3. Reduced Motion Test
        print("\n--- Testing Reduced Motion ---")
        context_motion = browser.new_context(
            viewport={"width": 1280, "height": 900},
            reduced_motion="reduce"
        )
        page_motion = context_motion.new_page()
        page_motion.goto(f"{BASE_URL}/", wait_until="networkidle")
        dur_token = page_motion.evaluate("() => getComputedStyle(document.documentElement).getPropertyValue('--dur').trim()")
        results["reduced_motion"] = {
            "dur_token": dur_token,
            "prefers_reduced_motion": True
        }
        print(f"Reduced motion --dur token: '{dur_token}'")
        context_motion.close()

        # 4. Keyboard Navigation & Focus States Walkthrough
        print("\n--- Testing Keyboard Navigation & Focus Rings ---")
        context_kb = browser.new_context(viewport={"width": 1280, "height": 900})
        page_kb = context_kb.new_page()
        page_kb.goto(f"{BASE_URL}/", wait_until="networkidle")

        # Walk interactive elements
        focus_steps = []
        for step in range(25):
            page_kb.keyboard.press("Tab")
            active_info = page_kb.evaluate("""() => {
                const el = document.activeElement;
                if (!el || el === document.body) return null;
                const cs = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return {
                    tagName: el.tagName,
                    id: el.id,
                    className: el.className,
                    text: (el.innerText || el.textContent || '').trim().substring(0, 40),
                    outline: cs.outline,
                    outlineColor: cs.outlineColor,
                    outlineWidth: cs.outlineWidth,
                    outlineStyle: cs.outlineStyle,
                    outlineOffset: cs.outlineOffset,
                    boxShadow: cs.boxShadow,
                    rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
                };
            }""")
            if active_info:
                # Capture screenshot snippet or viewport
                tag = active_info['tagName'].lower()
                cls = active_info['className'].replace(' ', '_')[:20]
                shot_name = f"focus-step-{step:02d}-{tag}-{cls}.png"
                shot_path = OUT_DIR / shot_name
                # take screenshot of focused element or bounding area
                try:
                    # scroll into view if needed
                    page_kb.screenshot(path=str(shot_path), full_page=False)
                    active_info["screenshot"] = str(shot_path)
                except Exception as e:
                    active_info["screenshot_error"] = str(e)
                focus_steps.append(active_info)
                print(f"Step {step:02d}: focused <{active_info['tagName']}> class='{active_info['className']}' text='{active_info['text']}' outline='{active_info['outline']}'")
        results["keyboard_focus"] = focus_steps
        context_kb.close()

        # 5. Mobile Menu Dialog & Lightbox Dialog Keyboard & Focus Test
        print("\n--- Testing Mobile Menu & Lightbox Dialogs ---")
        context_mobile = browser.new_context(viewport={"width": 360, "height": 800})
        page_mobile = context_mobile.new_page()
        page_mobile.goto(f"{BASE_URL}/", wait_until="networkidle")
        
        # Click menu button
        page_mobile.click(".menu-button")
        menu_open = page_mobile.evaluate("() => document.getElementById('meny').hasAttribute('open')")
        page_mobile.screenshot(path=str(OUT_DIR / "dialog-menu-open-360.png"))
        print(f"Mobile menu opened: {menu_open}")
        
        # Press Escape to close
        page_mobile.keyboard.press("Escape")
        menu_closed = page_mobile.evaluate("() => !document.getElementById('meny').hasAttribute('open')")
        focused_after_esc = page_mobile.evaluate("() => document.activeElement ? document.activeElement.className : null")
        print(f"Mobile menu closed by Escape: {menu_closed}, focused element: '{focused_after_esc}'")
        context_mobile.close()

        # Desktop Lightbox Test
        context_dt = browser.new_context(viewport={"width": 1280, "height": 900})
        page_dt = context_dt.new_page()
        page_dt.goto(f"{BASE_URL}/", wait_until="networkidle")
        
        # Click first gallery tile
        gallery_btn = page_dt.query_selector(".gallery-wall button, .gallery-strip button, [data-gallery-open]")
        if gallery_btn:
            gallery_btn.click()
            page_dt.wait_for_timeout(300)
            lightbox_open = page_dt.evaluate("() => { const d = document.querySelector('dialog.lightbox, #lightbox, dialog'); return d ? d.hasAttribute('open') : false; }")
            page_dt.screenshot(path=str(OUT_DIR / "dialog-lightbox-open-1280.png"))
            print(f"Lightbox opened: {lightbox_open}")
            page_dt.keyboard.press("Escape")
            page_dt.wait_for_timeout(200)
            lightbox_closed = page_dt.evaluate("() => { const d = document.querySelector('dialog.lightbox, #lightbox, dialog'); return d ? !d.hasAttribute('open') : true; }")
            print(f"Lightbox closed by Escape: {lightbox_closed}")
        else:
            print("No gallery button selector matched")
        context_dt.close()

        # 6. Sticky Bar scroll test
        print("\n--- Testing Sticky Bar on scroll ---")
        context_sb = browser.new_context(viewport={"width": 360, "height": 800})
        page_sb = context_sb.new_page()
        page_sb.goto(f"{BASE_URL}/", wait_until="networkidle")
        # Scroll past hero
        page_sb.evaluate("() => window.scrollTo(0, 1200)")
        page_sb.wait_for_timeout(300)
        sticky_visible = page_sb.evaluate("() => { const el = document.querySelector('.sticky-bar'); if (!el) return false; const cs = window.getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0'; }")
        page_sb.screenshot(path=str(OUT_DIR / "sticky-bar-scrolled-360.png"))
        print(f"Sticky bar visible on scroll (360px): {sticky_visible}")
        context_sb.close()

        # 7. Metadata extraction
        print("\n--- Checking Metadata & OG Tags ---")
        context_meta = browser.new_context()
        page_meta = context_meta.new_page()
        page_meta.goto(f"{BASE_URL}/", wait_until="networkidle")
        meta = page_meta.evaluate("""() => {
            const getMeta = (prop, isName) => {
                const sel = isName ? `meta[name="${prop}"]` : `meta[property="${prop}"]`;
                const el = document.querySelector(sel);
                return el ? el.getAttribute('content') : null;
            };
            return {
                title: document.title,
                description: getMeta('description', true),
                canonical: document.querySelector('link[rel="canonical"]')?.getAttribute('href'),
                og_title: getMeta('og:title', false),
                og_description: getMeta('og:description', false),
                og_image: getMeta('og:image', false),
                og_image_alt: getMeta('og:image:alt', false),
                twitter_card: getMeta('twitter:card', true),
                hreflang_nb: document.querySelector('link[hreflang="nb"]')?.getAttribute('href'),
                hreflang_en: document.querySelector('link[hreflang="en"]')?.getAttribute('href'),
                json_ld: Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s => s.innerText)
            };
        }""")
        results["metadata"] = meta
        print(f"Title: {meta['title']}")
        print(f"OG Image: {meta['og_image']}")
        print(f"OG Image Alt: {meta['og_image_alt']}")
        context_meta.close()

        browser.close()

    with open(OUT_DIR / "qa-results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nQA completed. Results saved to {OUT_DIR / 'qa-results.json'}")

if __name__ == "__main__":
    run_qa()
