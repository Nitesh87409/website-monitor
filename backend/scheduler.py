import time
import threading
import requests
import hashlib
from telegram_service import send_telegram
from storage import websites

def check_website(site):
    if not site.enabled:
        return

    try:
        start = time.time()
        response = requests.get(site.url, timeout=10)

        site.last_response_time = round((time.time() - start) * 1000, 2)
        site.last_checked = int(time.time())

        content_hash = hashlib.md5(response.text.encode()).hexdigest()

        if response.status_code == 200:
            site.last_status = "up"
        else:
            site.last_status = f"down ({response.status_code})"

        if not site.first_run and site.last_hash != content_hash:
            send_telegram(
                f"⚠️ Website Updated!\n\n"
                f"Site: {site.name}\n"
                f"URL: {site.url}"
            )

        site.last_hash = content_hash
        site.first_run = False

    except Exception as e:
        site.last_status = "error"
        site.last_checked = int(time.time())

        send_telegram(
            f"🚨 Website Error!\n\n"
            f"Site: {site.name}\n"
            f"Error: {e}"
        )

def scheduler():
    while True:
        for site in websites:
            if time.time() - site.last_checked >= site.interval:
                check_website(site)
        time.sleep(1)

def start_scheduler():
    threading.Thread(target=scheduler, daemon=True).start()
