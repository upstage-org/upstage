from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from core.entities.base import BaseEntity


class MediaTagEntity(BaseEntity):
    __tablename__ = "media_tag"
    id = Column(BigInteger, primary_key=True)
    asset_id = Column(Integer, ForeignKey("asset.id"), nullable=False, default=0)
    tag_id = Column(Integer, ForeignKey("tag.id"), nullable=False, default=0)
    asset = relationship("AssetEntity", foreign_keys=[asset_id], back_populates="tags")
    tag = relationship("TagEntity", foreign_keys=[tag_id])
