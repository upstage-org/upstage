from sqlalchemy import Column, DateTime, String, BigInteger, Text
from datetime import datetime
from global_config import BaseModel


class ConfigModel(BaseModel):
    """
    System configuration, such as the Terms of Service's URL, theme, global settings,...
    """

    __tablename__ = "config"
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(Text, nullable=True)
    created_on = Column(DateTime, nullable=False, default=datetime.now())
