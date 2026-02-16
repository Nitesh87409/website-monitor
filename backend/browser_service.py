from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
import os
import time

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def scan_website(url: str, keyword: str):
    """
    Scans website for:
    - keyword
    - keyword context (line)
    - pdf links
    - Telegram-safe screenshot

    Returns dict:
    {
        "found": bool,
        "context": str | None,
        "pdf_links": list[str],
        "screenshot": str,
        "final_url": str
    }
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
                "--no-sandbox"
            ]
        )

        page = browser.new_page()

        # ✅ TELEGRAM SAFE VIEWPORT
        page.set_viewport_size({"width": 1280, "height": 720})

        # ⏱️ SHORT TIMEOUT (gov sites safe)
        page.set_default_timeout(30000)

        # ✅ IMPORTANT FIX
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(3)  # small buffer for JS

        # 🔁 Final URL after redirect
        result["final_url"] = page.url

        # 🔑 KEYWORD + CONTEXT
        body_text = page.inner_text("body")
        for line in body_text.splitlines():
            if keyword.lower() in line.lower():
                result["found"] = True
                result["context"] = line.strip()[:300]
                break

        # 📄 PDF LINKS
        seen = set()
        for link in page.query_selector_all("a"):
            href = link.get_attribute("href")
            if not href:
                continue

            full_url = urljoin(result["final_url"], href)
            if full_url.lower().endswith(".pdf") and full_url not in seen:
                seen.add(full_url)
                result["pdf_links"].append(full_url)

        # 📸 TELEGRAM SAFE SCREENSHOT (NOT full page)
        domain = urlparse(result["final_url"]).netloc.replace(".", "_")
        filename = f"{SCREENSHOT_DIR}/{domain}_{int(time.time())}.png"

        page.screenshot(path=filename)
        result["screenshot"] = filename

        browser.close()

    return result
