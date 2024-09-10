import re
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime


def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_keys_to_camel_case(obj):
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            new_key = snake_to_camel(k)
            new_obj[new_key] = convert_keys_to_camel_case(v)
        return new_obj
    elif isinstance(obj, list):
        return [convert_keys_to_camel_case(i) for i in obj]
    elif isinstance(obj.__class__, DeclarativeMeta):
        # Convert SQLAlchemy object to dict
        new_obj = {}
        for c in obj.__table__.columns:
            value = getattr(obj, c.name)
            if isinstance(value, datetime):
                new_obj[snake_to_camel(c.name)] = value.isoformat()
            else:
                new_obj[snake_to_camel(c.name)] = convert_keys_to_camel_case(value)
        # Handle relationships
        for rel in obj.__mapper__.relationships:
            value = getattr(obj, rel.key)
            if value is not None:
                if rel.uselist:
                    new_obj[snake_to_camel(rel.key)] = [
                        convert_keys_to_camel_case(i) for i in value
                    ]
                else:
                    new_obj[snake_to_camel(rel.key)] = convert_keys_to_camel_case(value)
        return new_obj
    else:
        return obj
