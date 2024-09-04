from sqlalchemy import inspect

from config.database import db


class BaseEntity(db):
    __abstract__ = True

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
