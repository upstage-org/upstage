from sqlalchemy import BigInteger, Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from config.database import db


class BaseEntity(db):
    __abstract__ = True

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    created_at = Column(
        DateTime(True),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        index=True,
    )
    updated_at = Column(DateTime(True), nullable=False, onupdate=func.now())
