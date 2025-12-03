from sqlalchemy import Column, String, Text
# Import the new CommonBase
from .base import CommonBase


class Meeting(CommonBase):
    __tablename__ = "meeting"

    # ID and Timestamps are now inherited!
    title = Column(String(256), index=True, nullable=False)
    transcript = Column(Text, nullable=False)
    