from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from core.entities.base import BaseEntity


class AssetLicenseEntity(BaseEntity):
    __tablename__ = "asset_license"
    id = Column(BigInteger, primary_key=True)
    asset_id = Column(Integer, ForeignKey("asset.id"), nullable=False, default=0)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    level = Column(Integer, nullable=False, default=0)
    permissions = Column(String, nullable=True)
