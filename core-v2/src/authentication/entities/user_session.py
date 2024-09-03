from datetime import datetime
from sqlalchemy import BigInteger, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import db
from users.entities.user import UserEntity


class UserSessionEntity(db):
    __tablename__ = "user_session"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey(UserEntity.id, deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    access_token = Column(Text, default=None)
    refresh_token = Column(Text, default=None)
    recorded_time = Column(
        DateTime, nullable=False, index=True, default=datetime.utcnow
    )
    app_version = Column(Text, default=None)
    app_os_type = Column(Text, default=None)
    app_os_version = Column(Text, default=None)
    app_device = Column(Text, default=None)
    user = relationship(UserEntity, foreign_keys=[user_id])
