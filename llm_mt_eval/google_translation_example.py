from translate_gt import translate_file
from utils import write_text

src_file_path = "test.et.src"
write_text(
        "Apple esitas väidetava iPhone’i häkkimise tõttu hagi nuhkvaraettevõtte NSO Group vastu\nMa olen kindel, et see muutub.",src_file_path
)

translate_file(
    src_lang="et",
    tgt_lang="en",
    src_file="test.et.src",
    experiment_name="et-en-test-googletrans"
)