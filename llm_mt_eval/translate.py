import openai
import tiktoken
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

import logging
from typing import List, Tuple, Optional

import os
from pathlib import Path

from .evaluate import score_results
from .utils import read_lines, write_lines, write_json, concat_lines, responses_to_hyps, remove_empty_lines

from dataclasses import dataclass
from tqdm import tqdm

logger = logging.getLogger(__name__)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(20))
def openai_chat_request(
        user_prompt: str,
        system_prompt=None,
        model: str = "gpt-3.5-turbo",
        max_tokens: Optional[int] = None,
        temperature: float = 0,
        top_p: float = 1,
):
    messages = []
    if system_prompt is not None:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        n=1
    )


def get_n_tokens(prompt: str, model="gpt-3.5-turbo") -> int:
    return len(tiktoken.encoding_for_model(model).encode(prompt))


def response_to_lines(response: dict) -> List[str]:
    return remove_empty_lines(response["choices"][0]["message"]["content"].split("\n"))


@dataclass(frozen=True)
class ModelConfig:
    model: str = "gpt-3.5-turbo"
    max_tokens: Optional[int] = None
    temperature: float = 0
    top_p: float = 1


def translate_document(
        src_lang: str,
        tgt_lang: str,
        prompt: str,
        src_sentences: List[str],
        sent_delimiter: str = "\n",
        system_prompt: Optional[str] = None,
        model_cfg: ModelConfig = ModelConfig(),
) -> dict:
    input_prompt = prompt.format(src_lang=src_lang, tgt_lang=tgt_lang, sentence=sent_delimiter.join(src_sentences))
    logger.info(f"translating a request with {get_n_tokens(input_prompt, model_cfg.model)} tokens")

    response = openai_chat_request(
        input_prompt,
        model=model_cfg.model,
        max_tokens=model_cfg.max_tokens,
        temperature=model_cfg.temperature,
        top_p=model_cfg.top_p,
        system_prompt=system_prompt,
    )
    response["input_prompt"] = input_prompt
    response["input_prompt_format"] = repr(prompt)
    return response


def translate_sentence(
        src_lang: str,
        tgt_lang: str,
        prompt: str,
        src_sentence: str,
        system_prompt: Optional[str] = None,
        model_cfg: ModelConfig = ModelConfig(),
) -> dict:
    return translate_document(
        src_lang=src_lang,
        tgt_lang=tgt_lang,
        prompt=prompt,
        src_sentences=[src_sentence],
        sent_delimiter="",
        system_prompt=system_prompt,
        model_cfg=model_cfg,
    )


def translate_document_files(
        src_lang: str,
        tgt_lang: str,
        src_dir: str,
        doc_names: List[str],
        prompt: str,
        response_out_path: str,
        hyp_out_dir: str = None,
        concat_hyp_out_path: str = None,
        sent_delimiter: str = "\n",
        src_file_format: str = "{doc_name}",
        hyp_file_format: str = "{doc_name}",
        ref_file_format: str = "{doc_name}",
        ref_dir: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model_cfg: ModelConfig = ModelConfig(),
        metrics: Tuple[str, ...] = ("bleu",),
):
    responses = []

    try:
        for doc_name in tqdm(doc_names):
            doc_src_path = os.path.join(src_dir, src_file_format.format(doc_name=doc_name))
            logger.info(f"Translating {doc_name} ({doc_src_path})")
            src_lines = read_lines(doc_src_path)
            response = translate_document(
                src_lang=src_lang,
                tgt_lang=tgt_lang,
                prompt=prompt,
                src_sentences=src_lines,
                sent_delimiter=sent_delimiter,
                system_prompt=system_prompt,
                model_cfg=model_cfg,
            )
            responses.append(response)
            if hyp_out_dir is not None:
                hyp_doc_out_path = os.path.join(hyp_out_dir, hyp_file_format.format(doc_name=doc_name))
                Path(os.path.dirname(hyp_doc_out_path)).mkdir(parents=True, exist_ok=True)
                write_lines(response_to_lines(response), hyp_doc_out_path)

    finally:
        prompt_tokens = sum([response["usage"]["prompt_tokens"] for response in responses])
        completion_tokens = sum(response["usage"]["completion_tokens"] for response in responses)
        logger.info(f"prompt tokens: {prompt_tokens}, completion tokens: {completion_tokens}")

        write_json(responses, response_out_path)
        hyp_lines = responses_to_hyps(responses, use_last_line=False)
        if concat_hyp_out_path is not None:
            Path(os.path.dirname(concat_hyp_out_path)).mkdir(parents=True, exist_ok=True)
            write_lines(hyp_lines, concat_hyp_out_path)

    if ref_dir is not None:
        ref_lines = [
            concat_lines(" ".join(read_lines(os.path.join(ref_dir, ref_file_format.format(doc_name=doc_name))))) for
            doc_name in doc_names]
        for metric in metrics:
            logging.info(f"d{metric}: {score_results(metric, ref_lines=ref_lines, hyp_lines=hyp_lines)}")


def translate_file(
        src_lang: str,
        tgt_lang: str,
        src_path: str,
        prompt: str,
        response_out_path: str,
        hyp_out_path: Optional[str] = None,
        system_prompt: Optional[str] = None,
        model_cfg: ModelConfig = ModelConfig(),
        use_last_line=False
):
    responses = []
    try:
        for line in tqdm(read_lines(src_path)):
            response = translate_sentence(src_lang=src_lang, tgt_lang=tgt_lang, prompt=prompt, src_sentence=line,
                                          system_prompt=system_prompt, model_cfg=model_cfg)
            responses.append(response)
    finally:
        prompt_tokens = sum([response["usage"]["prompt_tokens"] for response in responses])
        completion_tokens = sum(response["usage"]["completion_tokens"] for response in responses)
        logger.info(f"prompt tokens: {prompt_tokens}, completion tokens: {completion_tokens}")
        Path(os.path.dirname(response_out_path)).mkdir(parents=True, exist_ok=True)
        write_json(responses, response_out_path)

        if hyp_out_path is not None:
            hyp_lines = responses_to_hyps(responses, use_last_line=use_last_line)
            Path(os.path.dirname(hyp_out_path)).mkdir(parents=True, exist_ok=True)
            write_lines(hyp_lines, hyp_out_path)
