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
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = browser.new_page()

        # ✅ Telegram-safe viewport
        page.set_viewport_size({"width": 1280, "height": 720})

        # ⏱️ Govt sites ke liye safe timeout
        page.set_default_timeout(30000)

        try:
            # ⚠️ IMPORTANT: domcontentloaded is fastest + safest
            page.goto(url, wait_until="domcontentloaded")
            time.sleep(3)  # JS buffer

            # 🔁 Final URL after redirect
            result["final_url"] = page.url

            # 🔑 KEYWORD + CONTEXT
            body_text = page.inner_text("body")
            for line in body_text.splitlines():
                if keyword.lower() in line.lower():
                    result["found"] = True
                    result["context"] = line.strip()[:300]
                    break

            # 📄 PDF LINKS (clean + unique)
            seen = set()
            for link in page.query_selector_all("a"):
                href = link.get_attribute("href")
                if not href:
                    continue

                full_url = urljoin(result["final_url"], href)

                if (
                    full_url.lower().endswith(".pdf")
                    and full_url not in seen
                ):
                    seen.add(full_url)
                    result["pdf_links"].append(full_url)

            # 📸 Telegram-safe screenshot (NOT full page)
            domain = urlparse(result["final_url"]).netloc.replace(".", "_")
            filename = f"{SCREENSHOT_DIR}/{domain}_{int(time.time())}.png"

            page.screenshot(path=filename)
            result["screenshot"] = filename

        except Exception as e:
            print("❌ WEBSITE SCAN ERROR:", e)

        finally:
            browser.close()

    return result
