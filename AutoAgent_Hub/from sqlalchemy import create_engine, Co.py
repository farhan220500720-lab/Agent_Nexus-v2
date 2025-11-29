from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Meeting():
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
