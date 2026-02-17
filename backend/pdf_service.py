import os
import requests
from urllib.parse import urlparse

PDF_DIR = "pdfs"
os.makedirs(PDF_DIR, exist_ok=True)


def download_pdf(pdf_url: str) -> str | None:
    """
    Downloads PDF and returns local file path
    """
    try:
        filename = os.path.basename(urlparse(pdf_url).path)
        if not filename.lower().endswith(".pdf"):
            filename = "document.pdf"

        file_path = os.path.join(PDF_DIR, filename)

        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        return file_path

    except Exception as e:
        print("❌ PDF download failed:", e)
        return None
