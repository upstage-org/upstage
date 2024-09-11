from datetime import datetime
from sqlalchemy.orm import class_mapper, ColumnProperty, RelationshipProperty
from config.database import db


class BaseEntity(db):
    __abstract__ = True

    def to_dict(self):
        result = {}
        mapper = class_mapper(self.__class__)

        # Include column attributes
        for attr in mapper.attrs:
            if isinstance(attr, ColumnProperty):
                value = getattr(self, attr.key)
                if isinstance(value, datetime):
                    result[attr.key] = value.isoformat()
                else:
                    result[attr.key] = value

        # Include relationship attributes
        for attr in mapper.attrs:
            if isinstance(attr, RelationshipProperty):
                value = getattr(self, attr.key)
                if value is not None:
                    if isinstance(value, list):
                        result[attr.key] = [
                            item.to_dict() if hasattr(item, "to_dict") else item
                            for item in value
                        ]
                    elif hasattr(value, "to_dict"):
                        result[attr.key] = value.to_dict()
                    else:
                        result[attr.key] = value

        return result
