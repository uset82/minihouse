from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Test 1: Desktop gallery lightbox
        page = browser.new_page(viewport={'width': 1280, 'height': 900})
        page.goto('http://127.0.0.1:4322/', wait_until='networkidle')
        btn = page.query_selector('.gallery-tile')
        print(f"Gallery tile found: {bool(btn)}")
        if btn:
            btn.click()
            page.wait_for_timeout(400)
            dialogs = page.query_selector_all('dialog')
            for i, d in enumerate(dialogs):
                open_val = d.get_attribute('open')
                cls = d.get_attribute('class')
                print(f"Dialog #{i} class='{cls}', open={open_val}")
            page.screenshot(path='fase4/promo/qa/screens/qa/dialog-lightbox-open-1280.png')
            
            # Press Escape
            page.keyboard.press("Escape")
            page.wait_for_timeout(200)
            closed_check = page.evaluate("() => Array.from(document.querySelectorAll('dialog')).every(d => !d.open)")
            print(f"All dialogs closed after Escape: {closed_check}")
            
        # Test 2: Sticky bar on 360px mobile
        page_m = browser.new_page(viewport={'width': 360, 'height': 800})
        page_m.goto('http://127.0.0.1:4322/', wait_until='networkidle')
        bar = page_m.query_selector('.sticky-cta')
        print(f"Sticky CTA element found: {bool(bar)}")
        if bar:
            init_hidden = bar.get_attribute('hidden')
            print(f"Initial hidden attribute: {init_hidden}")
            # Scroll past hero
            page_m.evaluate("() => window.scrollTo(0, 1500)")
            page_m.wait_for_timeout(600)
            scrolled_hidden = bar.get_attribute('hidden')
            print(f"Scrolled hidden attribute: {scrolled_hidden}")
            page_m.screenshot(path='fase4/promo/qa/screens/qa/sticky-cta-scrolled-360.png')
            
        browser.close()

if __name__ == '__main__':
    test()
