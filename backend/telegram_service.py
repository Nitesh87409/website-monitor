import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("❌ Telegram env missing")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# =========================
# SEND TEXT MESSAGE
# =========================
def send_telegram(message: str):
    try:
        response = requests.post(
            f"{BASE_URL}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"   # ✅ optional but useful
            },
            timeout=15
        )

        if response.status_code != 200:
            print("❌ Telegram text error:", response.text)
        else:
            print("📨 Telegram text sent")

    except Exception as e:
        print("❌ Telegram text failed:", e)


# =========================
# SEND PHOTO + CAPTION
# =========================
def send_telegram_photo(photo_path: str, caption: str):
    try:
        with open(photo_path, "rb") as photo:
            response = requests.post(
                f"{BASE_URL}/sendPhoto",
                data={
                    "chat_id": CHAT_ID,
                    "caption": caption[:1024],
                    "parse_mode": "Markdown"   # ✅ optional
                },
                files={
                    "photo": photo
                },
                timeout=30
            )

        if response.status_code != 200:
            print("❌ Telegram photo error:", response.text)
        else:
            print("📸 Telegram photo sent")

    except Exception as e:
        print("❌ Telegram photo failed:", e)
