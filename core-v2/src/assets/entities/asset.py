from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from assets.entities.asset_license import AssetLicenseEntity
from assets.entities.asset_type import AssetTypeEntity
from users.entities.user import UserEntity
from config.database import db


class AssetEntity(db):
    __tablename__ = "asset"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    asset_type_id = Column(
        Integer, ForeignKey(AssetTypeEntity.id), nullable=False, default=0
    )
    owner_id = Column(Integer, ForeignKey(UserEntity.id), nullable=False, default=0)
    description = Column(Text, nullable=True)
    file_location = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    updated_on = Column(DateTime, nullable=False, default=datetime.now)
    size = Column(BigInteger, nullable=False, default=0)
    copyright_level = Column(Integer, nullable=False, default=0)
    asset_type = relationship(AssetTypeEntity, foreign_keys=[asset_type_id])
    asset_license = relationship(AssetLicenseEntity, uselist=False, backref="asset")
    owner = relationship(UserEntity, foreign_keys=[owner_id])
    stages = relationship(
        "ParentStageEntity", lazy="dynamic", back_populates="child_asset"
    )
    tags = relationship("MediaTagEntity", lazy="dynamic", back_populates="asset")
    permissions = relationship(
        "AssetUsageEntity", lazy="dynamic", back_populates="asset"
    )
