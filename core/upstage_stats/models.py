import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ConnectionStat(Base):
    __tablename__ = "connection_stats"
    id = Column(Integer, primary_key=True)
    connected_id = Column(String, index=True)
    mqtt_timestamp = Column(DateTime, index=True)
    topic = Column(String)
    payload = Column(postgresql.JSON)
    created = Column(DateTime, default=datetime.datetime.utcnow, index=True)


class ReceiveStat(Base):
    __tablename__ = "receive_stats"
    id = Column(Integer, primary_key=True)
    received_id = Column(String, index=True)
    mqtt_timestamp = Column(DateTime, index=True)
    topic = Column(String)
    payload = Column(postgresql.JSON)
    created = Column(DateTime, default=datetime.datetime.utcnow, index=True)
