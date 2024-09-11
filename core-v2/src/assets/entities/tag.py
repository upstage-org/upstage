from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, String
from core.entities.base import BaseEntity


class TagEntity(BaseEntity):
    __tablename__ = "tag"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=True)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
