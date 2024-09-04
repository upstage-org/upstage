import re


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
    else:
        return obj
