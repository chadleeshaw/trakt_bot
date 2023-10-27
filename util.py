from functools import reduce
from typing import Any

def get_json_key(json, *keys) -> Any:
    o = ""
    def getter(level, key):
        return o if level is o else level.get(key, o)
    return reduce(getter, keys, json)