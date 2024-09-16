from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from core.entities.base import BaseEntity
from users.entities.user import UserEntity


class PerformanceConfigEntity(BaseEntity):
    __tablename__ = "performance_config"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey(UserEntity.id), nullable=False, default=0)
    description = Column(Text, nullable=False)
    # This can contain embedded HTML/CSS.
    splash_screen_text = Column(Text, nullable=True, default=None)
    # comma-separated list of animation URLs
    splash_screen_animation_urls = Column(Text, nullable=True, default=None)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    expires_on = Column(DateTime, nullable=False, default=None)

    def get_animation_urls(self):
        return self.splash_screen_animation_urls.split(",")
