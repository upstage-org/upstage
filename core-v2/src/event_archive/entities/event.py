import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.dialects import postgresql

from core.entities.base import BaseEntity


class EventEntity(BaseEntity):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    topic = Column(String)
    mqtt_timestamp = Column(Float, index=True)
    performance_id = Column(Integer, index=True)
    payload = Column(postgresql.JSON)
    created = Column(DateTime, default=datetime.datetime.now, index=True)
