from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    interval = Column(Integer, default=300)
    enabled = Column(Boolean, default=True)

    # 🔑 KEYWORD BASED DETECTION (NEW)
    keyword = Column(String, nullable=False)                # e.g. "vacancy", "bharti"
    keyword_found = Column(Boolean, default=False)          # last scan result
    alert_sent = Column(Boolean, default=False)             # prevent spam

    # STATUS / MONITORING
    last_status = Column(String, default="unknown")
    last_response_time = Column(Integer, default=0)
    last_checked = Column(Integer, default=0)
    last_hash = Column(String, nullable=True)
    first_run = Column(Boolean, default=True)

    logs = relationship(
        "WebsiteLog",
        back_populates="website",
        cascade="all, delete"
    )


class WebsiteLog(Base):
    __tablename__ = "website_logs"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("websites.id"))

    event_type = Column(String)   # update / keyword / error / recovery
    message = Column(String)

    old_hash = Column(String, nullable=True)
    new_hash = Column(String, nullable=True)
    timestamp = Column(Integer)

    website = relationship("Website", back_populates="logs")
