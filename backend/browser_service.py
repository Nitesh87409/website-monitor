from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
import os
import time

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def scan_website(
    url: str,
    keyword: str,
    take_screenshot: bool = False   # ✅ DEFAULT FALSE
):
    """
    Fast website scan:
    - keyword detection
    - keyword context
    - pdf links
    - OPTIONAL screenshot (ONLY when change detected)
    """

    result = {
        "found": False,
        "context": None,
        "pdf_links": [],
        "screenshot": None,
        "final_url": None
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 720})
        page.set_default_timeout(30000)

        try:
            # ⚡ Fast + stable load
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(2)

            result["final_url"] = page.url

            body_text = page.inner_text("body")
            body_lower = body_text.lower()

            # ⛔ IGNORE ERROR / DEFAULT PAGES
            error_phrases = [
                "default error",
                "please review the following url",
                "aspxerrorpath",
                "page not found",
                "404",
                "error occurred"
            ]

            for phrase in error_phrases:
                if phrase in body_lower:
                    print("⛔ ERROR PAGE DETECTED — SKIPPED")
                    return result

            # 🔑 Keyword + context
            for line in body_text.splitlines():
                if keyword.lower() in line.lower():
                    result["found"] = True
                    result["context"] = line.strip()[:300]
                    break

            # 📄 PDF links (unique)
            seen = set()
            for link in page.query_selector_all("a"):
                href = link.get_attribute("href")
                if not href:
                    continue

                full_url = urljoin(result["final_url"], href)
                if full_url.lower().endswith(".pdf") and full_url not in seen:
                    seen.add(full_url)
                    result["pdf_links"].append(full_url)

            # 📸 Screenshot ONLY if keyword FOUND
            if take_screenshot and result["found"]:
                domain = urlparse(result["final_url"]).netloc.replace(".", "_")
                filename = f"{SCREENSHOT_DIR}/{domain}_{int(time.time())}.png"
                page.screenshot(path=filename)
                result["screenshot"] = filename

        except Exception as e:
            print("❌ WEBSITE SCAN ERROR:", repr(e))

        finally:
            browser.close()

    return result
