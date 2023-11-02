from functools import reduce
from typing import Any

def get_json_key(json: dict, *keys: str) -> Any:
    o = ''
    def getter(level: dict, key: str) -> Any:
        return o if level is o else level.get(key, o)
    return reduce(getter, keys, json)

def type_check(type: str) -> (str, str):
    title = 'title'
    type = type.rstrip('s')
    if type == 'show':  
        type = 'tv'
        title = 'name'
    return type, title