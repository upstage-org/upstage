from datetime import datetime
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from core.entities.base import BaseEntity
from stages.entities.stage import StageEntity
from sqlalchemy.orm import relationship


class StageLicenseEntity(BaseEntity):
    """
    Stage is yet another asset, but broken out as the 'root' in the hierarchy.
    One can grant a license to everything under a stage, or any other asset,
    to make licensing easier.
    """

    __tablename__ = "stage_license"
    id = Column(BigInteger, primary_key=True)
    stage_id = Column(Integer, ForeignKey(StageEntity.id), nullable=False, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_on = Column(DateTime, nullable=True)
    access_path = Column(String, nullable=False, unique=True)
    grant_recursively = Column(Boolean, nullable=False, default=False)
    stage = relationship("StageEntity", foreign_keys=[stage_id])
