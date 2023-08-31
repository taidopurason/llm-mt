import os
from translate_deepl import translate_file

def translate_all_files_in_folder(src_folder, tgt_folder, src_lang, tgt_lang, experiment_name):
    if not os.path.exists(tgt_folder):
        os.mkdir(tgt_folder)
    
    for filename in os.listdir(src_folder):
        if filename.endswith(".txt"):
            src_file_path = os.path.join(src_folder, filename)
            tgt_file_name = filename
            tgt_file_path = os.path.join(tgt_folder, tgt_file_name)
            
            translate_file(
                src_lang=src_lang,
                tgt_lang=tgt_lang,
                src_file=src_file_path,
                experiment_name=tgt_file_path
            )

src_folder = "../data/mtee-news/et_src"
tgt_folder = "../data/mtee-news/et-en_tgt_dl"

translate_all_files_in_folder(
    src_folder=src_folder,
    tgt_folder=tgt_folder,
    src_lang="et",
    tgt_lang="en-gb",
    experiment_name=""
)

src_folder = "../data/mtee-news/en_src"
tgt_folder = "../data/mtee-news/en-et_tgt_dl"

translate_all_files_in_folder(
    src_folder=src_folder,
    tgt_folder=tgt_folder,
    src_lang="en",
    tgt_lang="et",
    experiment_name=""
)