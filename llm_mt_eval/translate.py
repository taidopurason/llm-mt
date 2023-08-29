import logging
from typing import Optional, List

import openai
import tiktoken
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

from tqdm import tqdm

from utils import read_lines, write_json, write_lines

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


def get_n_tokens(prompts: List[str], model="gpt-3.5-turbo") -> int:
    enc = tiktoken.encoding_for_model(model)
    return sum(len(enc.encode(prompt)) for prompt in prompts)


def translate_file(src_lang: str, tgt_lang: str, src_file: str, prompt: str, experiment_name: str,
                   use_last_line: bool = True):
    input_prompts = [
        prompt.format(src_lang=src_lang, tgt_lang=tgt_lang, sentence=line) for line in read_lines(src_file)
    ]

    logger.info(f"translating {get_n_tokens(input_prompts)} lines")

    responses = []
    hyp_sents = []
    try:
        for input_prompt in tqdm(input_prompts):
            response = openai_chat_request(input_prompt)
            response["input_prompt"] = input_prompt
            response["input_prompt_format"] = prompt

            hyp = response["choices"][0]["message"]["content"]
            if "\n" in hyp:
                if use_last_line:
                    logger.info("hyp contains newline(s), using last line as the hypothesis")
                    hyp = hyp.split("\n")[-1]
                else:
                    logger.info("hyp contains newline(s), replacing with space(s)")
                    hyp = hyp.replace("\n", " ")

            responses.append(response)
            hyp_sents.append(hyp)
    finally:
        write_json(responses, f"{experiment_name}.responses.json")
        hyp_file = f"{experiment_name}.hyp.txt"
        write_lines(hyp_sents, hyp_file)

    prompt_tokens = sum([response["usage"]["prompt_tokens"] for response in responses])
    completion_tokens = sum(response["usage"]["completion_tokens"] for response in responses)
    logger.info(f"prompt tokens: {prompt_tokens}, completion tokens: {completion_tokens}")
