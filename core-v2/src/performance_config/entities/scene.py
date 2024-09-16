from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, Text
from core.entities.base import BaseEntity
from sqlalchemy.orm import relationship

from stages.entities.stage import StageEntity
from users.entities.user import UserEntity


class SceneEntity(BaseEntity):
    __tablename__ = "scene"
    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    scene_order = Column(Integer, index=True, nullable=True, default=0)
    scene_preview = Column(Text, nullable=True)
    payload = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    active = Column(Boolean, nullable=False, default=True)
    owner_id = Column(Integer, ForeignKey(UserEntity.id), nullable=False, default=0)
    stage_id = Column(Integer, ForeignKey(StageEntity.id), nullable=False, default=0)
    owner = relationship("UserEntity", foreign_keys=[owner_id])
    stage = relationship("StageEntity", foreign_keys=[stage_id])
