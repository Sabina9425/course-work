import json
from typing import List
from .operations import Operation


def parse_operations(json_file_path: str) -> List[Operation]:
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    operations = [Operation.from_json(item) for item in data]
    return operations
