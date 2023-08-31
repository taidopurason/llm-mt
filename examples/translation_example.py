import logging
import os

from llm_mt_eval.translate import translate_file
from llm_mt_eval.utils import write_lines

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

logging.basicConfig(level=logging.INFO)
src_file_path = "../llm_mt_eval/test.et.src"
write_lines(
    [
        "Apple esitas väidetava iPhone’i häkkimise tõttu hagi nuhkvaraettevõtte NSO Group vastu",
        "Ma olen kindel, et see muutub."
    ],
    src_file_path
)

translate_file(
    src_lang="et",
    tgt_lang="en",
    src_path="../llm_mt_eval/test.et.src",
    prompt="Translate from {src_lang} to {tgt_lang}: {sentence}",
    use_last_line=True,
    response_out_path="../llm_mt_eval/test.et-en.response.json",
    hyp_out_path="../llm_mt_eval/test.et-en.hyp.txt",
)
