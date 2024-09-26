from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from core.entities.base import BaseEntity


class StageAttributeEntity(BaseEntity):
    __tablename__ = "stage_attribute"
    id = Column(BigInteger, primary_key=True)
    stage_id = Column(Integer, ForeignKey("stage.id"), nullable=False, default=0)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    stage = relationship(
        "StageEntity", foreign_keys=[stage_id], back_populates="attributes"
    )