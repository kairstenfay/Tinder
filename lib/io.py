import json
from typing import Any


def read_json(file_name: str):
    with open(file_name, 'r') as f:
        return json.loads(f.readlines()[0])

def write_json(data: Any, file_name: str):
    with open(file_name, 'w') as f:
        f.write(json.dumps(data))
