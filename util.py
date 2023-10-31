from functools import reduce
from typing import Any

def get_json_key(json, *keys) -> Any:
    def getter(level, key):
        return None if level is None else level.get(key, None)
    return reduce(getter, keys, json)

def type_check(type):
    title = 'title'
    type = type.rstrip('s')
    if type == 'show':  
        type = 'tv'
    title = 'name'
    return type, title