from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Text
from core.entities.base import BaseEntity
from performance_config.entities.performance_config import PerformanceConfigEntity
from users.entities.user import UserEntity
from sqlalchemy.orm import relationship


class PerformanceMQTTConfigEntity(BaseEntity):
    # This holds the MQTT server configuration for one performance, to make connecting easier.
    # There may be > 1 MQTT connection in a performance.
    __tablename__ = "live_performance_mqtt_config"
    id = Column(BigInteger, primary_key=True)
    owner_id = Column(Integer, ForeignKey(UserEntity.id), nullable=False, default=0)
    ip_address = Column(Text, nullable=False)
    websocket_port = Column(Integer, nullable=False, default=0)
    webclient_port = Column(Integer, nullable=False, default=0)
    """
    Performance connections will be namespaced by a unique string, so a user can be
    connected to more than one stage at once.
    The topic_name should be modified when this expires, so it can be reused
    in the future. MQTT will send /performance/topic_name as the leading topic.
    """
    topic_name = Column(Text, unique=True, nullable=False)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.now)
    expires_on = Column(DateTime, nullable=False, default=None)
    performance_config_id = Column(
        Integer, ForeignKey(PerformanceConfigEntity.id), nullable=False, default=0
    )

    owner = relationship("UserEntity", foreign_keys=[owner_id])
    performance_config = relationship(
        "PerformanceConfigEntity", foreign_keys=[performance_config_id]
    )
