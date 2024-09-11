from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from assets.entities.asset import AssetEntity
from core.entities.base import BaseEntity


class AssetAttributeEntity(BaseEntity):
    """
    Attributes are the abilities of the asset: What the asset can do or be.
    For example, flip, rotate, draw, overlay, be opaque, dissolve, loop.
    Breaking out attributes and actions seemed like splitting hairs, and
    seems much easier in one table.
    """

    __tablename__ = "asset_attribute"
    id = Column(BigInteger, primary_key=True)
    asset_id = Column(Integer, ForeignKey(AssetEntity.id), nullable=False, default=0)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    asset = relationship(AssetEntity, foreign_keys=[asset_id])
