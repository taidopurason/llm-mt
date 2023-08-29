import logging

from llm_mt_eval.translate import translate_file
from llm_mt_eval.utils import write_lines

import openai

openai.api_key = ""  # your openai api key

logging.basicConfig(level=logging.INFO)
src_file_path = "test.et.src"
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
    src_file="test.et.src",
    prompt="Translate from {src_lang} to {tgt_lang}: {sentence}",
    experiment_name="et-en-test",
    use_last_line=True
)
