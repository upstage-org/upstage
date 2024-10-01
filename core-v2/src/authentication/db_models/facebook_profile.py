from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Text
from global_config import BaseModel
from users.db_models.user import UserModel


class FacebookProfileModel(BaseModel):
    __tablename__ = "facebook_profile"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=True, default=None)
    facebook_id = Column(Text, nullable=True, default=None)
    facebook_phone = Column(Text, nullable=True, default=None)
    facebook_email = Column(Text, nullable=True, default=None)
    facebook_first_name = Column(Text, nullable=True, default=None)
    facebook_last_name = Column(Text, nullable=True, default=None)
    facebook_username = Column(Text, nullable=True, default=None)
    other_profile_json = Column(Text, nullable=True, default=None)
    received_datetime = Column(DateTime, nullable=True, default=datetime.utcnow)
