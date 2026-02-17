"""
Website Monitor Backend – FINAL SQLITE STABLE
FastAPI + Scheduler + Telegram Alerts + Logs + Screenshot + PDF
"""

import os
import time
import threading
import requests

from fastapi import FastAPI, HTTPException

from database import SessionLocal, engine
from models import Website, WebsiteLog
from schemas import WebsiteCreate, WebsiteResponse, WebsiteLogResponse

from browser_service import scan_website

from telegram_service import (
    send_telegram,
    send_telegram_photo,
    send_telegram_document
)


app = FastAPI(title="Website Monitor Backend")

# =========================
# GLOBAL FLAGS
# =========================
RUN_SCHEDULER = True
MONITORING_ENABLED = True


# =========================
# LOG HELPER
# =========================
def save_log(db, site_id, event_type, message, old_hash=None, new_hash=None):
    log = WebsiteLog(
        website_id=site_id,
        event_type=event_type,
        message=message,
        old_hash=old_hash,
        new_hash=new_hash,
        timestamp=int(time.time())
    )
    db.add(log)
    db.commit()

    logs = (
        db.query(WebsiteLog)
        .filter(WebsiteLog.website_id == site_id)
        .order_by(WebsiteLog.timestamp.desc())
        .all()
    )

    for extra in logs[20:]:
        db.delete(extra)
    db.commit()


# =========================
# STARTUP / SHUTDOWN
# =========================
@app.on_event("startup")
def startup():
    Website.metadata.create_all(bind=engine)
    threading.Thread(target=scheduler, daemon=True).start()
    print("▶️ Scheduler + DB started")


@app.on_event("shutdown")
def shutdown():
    global RUN_SCHEDULER
    RUN_SCHEDULER = False
    print("🛑 Scheduler stopped")

# =========================
# WEBSITE CHECK (KEYWORD + SCREENSHOT + PDF DOWNLOAD + ATTACH)
# =========================
def check_website(db, site: Website):
    if not site.enabled or not MONITORING_ENABLED:
        return

    try:
        site.last_checked = int(time.time())

        # 🔍 Playwright deep scan
        scan = scan_website(site.url, site.keyword)

        site.last_status = "up"

        # 🚨 FIRST TIME KEYWORD FOUND
        if scan["found"] and not site.alert_sent:

            message = (
                f"🚨 *NEW SARKARI UPDATE FOUND!*\n\n"
                f"🏢 *Site:* {site.name}\n"
                f"🔑 *Keyword:* {site.keyword}\n"
                f"🌐 *Page:* {scan.get('final_url') or site.url}\n"
            )

            # 🧠 CONTEXT (where keyword found)
            if scan.get("context"):
                message += f"\n🧾 *Context:*\n{scan['context']}\n"

            # 📄 PDF LINKS (text info)
            if scan["pdf_links"]:
                message += "\n📄 *PDF Links:*\n"
                message += "\n".join(scan["pdf_links"][:3])

            # 📸 Screenshot (Telegram-safe)
            if scan.get("screenshot"):
                send_telegram_photo(
                    scan["screenshot"],
                    message
                )
            else:
                send_telegram(message)

            # =========================
            # 📥 PDF DOWNLOAD + ATTACH
            # =========================
            if scan["pdf_links"]:
                os.makedirs("downloads", exist_ok=True)

                for pdf_url in scan["pdf_links"][:2]:  # max 2 PDFs (safe)
                    try:
                        filename = pdf_url.split("/")[-1]
                        local_path = os.path.join("downloads", filename)

                        # Download PDF
                        r = requests.get(pdf_url, timeout=30)
                        if r.status_code == 200:
                            with open(local_path, "wb") as f:
                                f.write(r.content)

                            # Send PDF to Telegram
                            send_telegram_document(
                                local_path,
                                caption=f"📎 {filename}\n{site.name}"
                            )

                    except Exception as pdf_err:
                        print("❌ PDF download/send error:", pdf_err)

            # 📝 LOG
            save_log(
                db,
                site.id,
                "keyword",
                f"Keyword '{site.keyword}' found with screenshot & PDF"
            )

            site.keyword_found = True
            site.alert_sent = True

        # 🔄 KEYWORD REMOVED → RESET ALERT
        if not scan["found"]:
            site.keyword_found = False
            site.alert_sent = False

        site.first_run = False
        db.commit()

    except Exception as e:
        site.last_checked = int(time.time())

        error_text = repr(e) if not str(e).strip() else str(e)
        print("❌ WEBSITE SCAN ERROR:", error_text)

        # ⚠️ Ignore first run glitches
        if site.first_run:
            site.first_run = False
            db.commit()
            return

        # 🚫 Prevent repeat spam
        if site.last_status != "error":
            save_log(db, site.id, "error", error_text)

            send_telegram(
                f"🚨 *Website Error!*\n\n"
                f"Site: {site.name}\n"
                f"Error: {error_text}"
            )

        site.last_status = "error"
        db.commit()



# =========================
# SCHEDULER
# =========================
def scheduler():
    while RUN_SCHEDULER:
        if not MONITORING_ENABLED:
            time.sleep(1)
            continue

        db = SessionLocal()
        sites = db.query(Website).filter(Website.enabled == True).all()

        for site in sites:
            if time.time() - site.last_checked >= site.interval:
                check_website(db, site)

        db.close()
        time.sleep(1)


# =========================
# API ROUTES
# =========================
@app.get("/")
def root():
    return {"status": "Backend running (SQLite + Screenshot + PDF)"}


@app.get("/api/websites", response_model=list[WebsiteResponse])
def get_websites():
    db = SessionLocal()
    sites = db.query(Website).all()
    db.close()
    return sites


@app.post("/api/websites", response_model=WebsiteResponse)
def add_website(site: WebsiteCreate):
    db = SessionLocal()

    new_site = Website(
        name=site.name,
        url=site.url,
        interval=site.interval,
        keyword=site.keyword,
        keyword_found=False,
        alert_sent=False
    )

    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    db.close()

    return new_site


@app.post("/api/websites/{site_id}/toggle")
def toggle_website(site_id: int):
    db = SessionLocal()
    site = db.query(Website).filter(Website.id == site_id).first()

    if not site:
        db.close()
        raise HTTPException(status_code=404, detail="Website not found")

    site.enabled = not site.enabled
    db.commit()
    db.close()
    return {"enabled": site.enabled}


@app.delete("/api/websites/{site_id}")
def delete_website(site_id: int):
    db = SessionLocal()
    site = db.query(Website).filter(Website.id == site_id).first()

    if not site:
        db.close()
        raise HTTPException(status_code=404, detail="Website not found")

    db.delete(site)
    db.commit()
    db.close()
    return {"message": "deleted"}


# =========================
# LOGS
# =========================
@app.get("/api/logs/{website_id}", response_model=list[WebsiteLogResponse])
def get_logs(website_id: int):
    db = SessionLocal()
    logs = (
        db.query(WebsiteLog)
        .filter(WebsiteLog.website_id == website_id)
        .order_by(WebsiteLog.timestamp.desc())
        .limit(20)
        .all()
    )
    db.close()
    return logs


# =========================
# MONITORING CONTROL
# =========================
@app.post("/api/monitoring/stop")
def stop_monitoring():
    global MONITORING_ENABLED
    MONITORING_ENABLED = False
    return {"enabled": False}


@app.post("/api/monitoring/start")
def start_monitoring():
    global MONITORING_ENABLED
    MONITORING_ENABLED = True
    return {"enabled": True}


@app.get("/api/monitoring/status")
def monitoring_status():
    return {"enabled": MONITORING_ENABLED}


@app.post("/api/telegram/test")
def telegram_test():
    send_telegram("✅ Telegram Test Successful! Screenshot system ready.")
    return {"status": "sent"}
