from datetime import datetime
from sqlalchemy import BigInteger, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from global_config import BaseModel
from users.db_models.user import UserModel


class UserSessionModel(BaseModel):
    __tablename__ = "user_session"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey(UserModel.id, deferrable=True, initially="DEFERRED"),
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
    user = relationship(UserModel, foreign_keys=[user_id])
