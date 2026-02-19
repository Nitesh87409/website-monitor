from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
import os
import time
import hashlib

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def scan_website(
    url: str,
    keyword: str,
    take_screenshot: bool = False   # ✅ default FALSE
):
    """
    Fast website scan:
    - keyword detection (optional)
    - page hash (for full-page change detection)
    - pdf links
    - screenshot ONLY when explicitly asked
    """

    result = {
        "found": False,
        "context": None,
        "pdf_links": [],
        "screenshot": None,
        "final_url": None,
        "page_hash": None,          # ✅ IMPORTANT
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
            # ⚡ Fast load
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(2)

            result["final_url"] = page.url

            body_text = page.inner_text("body")
            body_lower = body_text.lower()

            # =========================
            # 🔐 PAGE HASH (ALWAYS)
            # =========================
            clean_text = " ".join(body_text.split())
            result["page_hash"] = compute_hash(clean_text)

            # =========================
            # ⛔ IGNORE ERROR PAGES
            # =========================
            error_phrases = [
                "default error",
                "aspxerrorpath",
                "page not found",
                "404",
                "error occurred"
            ]

            for phrase in error_phrases:
                if phrase in body_lower:
                    print("⛔ ERROR PAGE DETECTED — SKIPPED CONTENT")
                    return result   # hash already set ✔

            # =========================
            # 🔑 KEYWORD DETECTION (ONLY if keyword provided)
            # =========================
            if keyword:
                for line in body_text.splitlines():
                    if keyword.lower() in line.lower():
                        result["found"] = True
                        result["context"] = line.strip()[:300]
                        break

            # =========================
            # 📄 PDF LINKS
            # =========================
            seen = set()
            for link in page.query_selector_all("a"):
                href = link.get_attribute("href")
                if not href:
                    continue

                full_url = urljoin(result["final_url"], href)
                if full_url.lower().endswith(".pdf") and full_url not in seen:
                    seen.add(full_url)
                    result["pdf_links"].append(full_url)

            # =========================
            # 📸 SCREENSHOT (ONLY when requested)
            # =========================
            if take_screenshot:
                domain = urlparse(result["final_url"]).netloc.replace(".", "_")
                filename = f"{SCREENSHOT_DIR}/{domain}_{int(time.time())}.png"
                page.screenshot(path=filename)
                result["screenshot"] = filename

        except Exception as e:
            print("❌ WEBSITE SCAN ERROR:", repr(e))

        finally:
            browser.close()

    return result
