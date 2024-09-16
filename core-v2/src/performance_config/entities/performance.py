from datetime import datetime
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from core.entities.base import BaseEntity
from stages.entities.stage import StageEntity
from sqlalchemy.orm import relationship


class PerformanceEntity(BaseEntity):
    __tablename__ = "performance"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    stage_id = Column(Integer, ForeignKey(StageEntity.id), nullable=False, default=0)
    stage = relationship(StageEntity, foreign_keys=[stage_id])
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    saved_on = Column(DateTime, nullable=True)
    recording = Column(Boolean, nullable=False, default=False)
