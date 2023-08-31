from typing import List
import json


def read_lines(file: str, encoding="utf-8") -> List[str]:
    with open(file, 'r', encoding=encoding) as f:
        return [line.rstrip() for line in f]


def write_text(text: str, file: str):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(f"{text}")


def write_json(json_object: object, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_object, f, indent=4, default=str)


def read_json(path: str) -> object:
    with open(path, "r", encoding="utf-8") as user_file:
        parsed_json = json.load(user_file)
    return parsed_json
