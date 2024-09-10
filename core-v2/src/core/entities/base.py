from datetime import datetime
from sqlalchemy import inspect
from config.database import db


class BaseEntity(db):
    __abstract__ = True

    def to_dict(self):
        result = {}
        for c in inspect(self).mapper.column_attrs:
            value = getattr(self, c.key)
            if isinstance(value, datetime):
                result[c.key] = value.isoformat()
            else:
                result[c.key] = value
        return result
