import logging
from typing import List, Dict
import json
import re

logger = logging.getLogger(__name__)


def read_lines(file: str, encoding="utf-8") -> List[str]:
    with open(file, 'r', encoding=encoding) as f:
        return [line.rstrip() for line in f]


def write_lines(lines: List[str], file: str):
    with open(file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(f"{line}\n")


def write_json(json_object: object, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_object, f, indent=4, default=str)


def read_json(path: str) -> object:
    with open(path, "r", encoding="utf-8") as user_file:
        parsed_json = json.load(user_file)
    return parsed_json


def read_file(file: str, encoding="utf-8") -> str:
    with open(file, 'r', encoding=encoding) as f:
        return f.read()


EXTRA_SPACE_PATTERN = re.compile(r' +')


def concat_lines(sentence: str) -> str:
    return EXTRA_SPACE_PATTERN.sub(r' ', sentence.replace('\n', ' '))


def remove_empty_lines(sentence: List[str]) -> List[str]:
    return [line for line in sentence if line.strip() != ""]


def responses_to_hyps(responses: List[Dict], use_last_line: bool = True) -> List[str]:
    hyp_sents = []
    for response in responses:
        hyp = response["choices"][0]["message"]["content"]
        if "\n" in hyp:
            if use_last_line:
                logger.info("hyp contains newline(s), using last line as the hypothesis")
                hyp = remove_empty_lines(hyp.split("\n"))[-1]
            else:
                logger.info("hyp contains multiple lines, concatenating")
                hyp = concat_lines(hyp)
        hyp_sents.append(hyp)
    return hyp_sents


def doc_responses_to_hyps(responses: List[Dict]) -> List[List[str]]:
    hyp_sents = []
    for response in responses:
        hyp = response["choices"][0]["message"]["content"]
        doc_hyps = [sent for sent in map(str.strip, hyp.split("\n")) if sent != ""]
        hyp_sents.append(doc_hyps)

    return hyp_sents

