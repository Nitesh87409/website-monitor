from pydantic import BaseModel
from typing import Optional

# =========================
# WEBSITE SCHEMAS
# =========================

class WebsiteCreate(BaseModel):
    name: str
    url: str
    interval: int = 300
    keyword: str


class WebsiteResponse(WebsiteCreate):
    id: int
    enabled: bool
    last_status: str
    last_response_time: float
    last_checked: int
    last_hash: Optional[str]
    first_run: bool

    keyword_found: bool
    alert_sent: bool

    class Config:
        from_attributes = True


# =========================
# LOG SCHEMA
# =========================

class WebsiteLogResponse(BaseModel):
    id: int
    website_id: int
    event_type: str
    message: str
    old_hash: Optional[str]
    new_hash: Optional[str]
    timestamp: int

    class Config:
        from_attributes = True
