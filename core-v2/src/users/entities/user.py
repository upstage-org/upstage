from sqlalchemy import TIMESTAMP, BigInteger, Boolean, Column, Integer, String, Text
from datetime import datetime
from core.entities.base import BaseEntity


PLAYER = 1
GUEST = 4
ADMIN = 8
SUPER_ADMIN = 32

ROLES = {
    PLAYER: "Player",  # Player access to on-stage tools
    GUEST: "Guest",  # Can play a stage if granted player permission, cannot create or edit media
    ADMIN: "Admin",  # Admin access to edit media, players, content
    SUPER_ADMIN: "Super Admin",  # Internal Upstage staff access to all
}


class UserEntity(BaseEntity):
    __tablename__ = "upstage_user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False, unique=True, default="")
    password = Column(Text, nullable=False, default="")
    email = Column(Text, nullable=True, default="")
    bin_name = Column(Text, nullable=True, default="")
    role = Column(Integer, nullable=False, default=0)
    first_name = Column(String, default=None)
    last_name = Column(String, default=None)
    display_name = Column(String, default=None)
    active = Column(Boolean, nullable=False, default=False)
    firebase_pushnot_id = Column(String, default=None)
    created_on = Column(TIMESTAMP(timezone=True), default=datetime.now)
    deactivated_on = Column(TIMESTAMP(timezone=True), default=None)
    upload_limit = Column(Integer, default=1024 * 1024)
    intro = Column(Text, default=None)
    can_send_email = Column(Boolean, default=False)
    last_login = Column(TIMESTAMP(timezone=True), default=None)
