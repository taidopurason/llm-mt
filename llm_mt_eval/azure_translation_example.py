from translate_azure import translate_file
from utils import write_lines

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
    experiment_name="et-en-test-azure"
)