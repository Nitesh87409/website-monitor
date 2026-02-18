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
                "parse_mode": "Markdown"
            },
            timeout=60
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
        if not os.path.exists(photo_path):
            print("❌ Screenshot not found:", photo_path)
            return

        with open(photo_path, "rb") as photo:
            response = requests.post(
                f"{BASE_URL}/sendPhoto",
                data={
                    "chat_id": CHAT_ID,
                    "caption": caption[:1024],
                    "parse_mode": "Markdown"
                },
                files={
                    "photo": photo
                },
                timeout=60
            )

        if response.status_code != 200:
            print("❌ Telegram photo error:", response.text)
        else:
            print("📸 Telegram photo sent")

    except Exception as e:
        print("❌ Telegram photo failed:", e)


# =========================
# SEND PDF / DOCUMENT (NEW)
# =========================
def send_telegram_document(file_path: str, caption: str = ""):
    """
    PDF / Document attach karke Telegram par bhejta hai
    """
    try:
        if not os.path.exists(file_path):
            print("❌ PDF not found:", file_path)
            return

        with open(file_path, "rb") as doc:
            response = requests.post(
                f"{BASE_URL}/sendDocument",
                data={
                    "chat_id": CHAT_ID,
                    "caption": caption[:1024],
                    "parse_mode": "Markdown"
                },
                files={
                    "document": doc
                },
                timeout=300
            )

        if response.status_code != 200:
            print("❌ Telegram document error:", response.text)
        else:
            print("📎 Telegram PDF sent")

    except Exception as e:
        print("❌ Telegram document failed:", e)
