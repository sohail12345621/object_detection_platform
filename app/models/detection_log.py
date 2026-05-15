from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database.session import Base

class DetectionLog(Base):
    __tablename__ = "detection_logs"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    type = Column(String) # image or video
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
