import os
from translate_deepl import translate_file

def is_leaf_folder(folder_path):
    for _, _, filenames in os.walk(folder_path):
        if filenames:
            return True
    return False

root_folder = '../data/flores200_devtest_by_documents'

lang_map = {
    "en": "eng",
    "et": "est",
    "sl": "slv",
    "cs": "ces",
    "sk": "slk",
    "cz": "ces",
    "hr": "hrv"
}

languagepairs = [
    ["en", "et"],
    ["en", "cs"],
    ["en", "sl"],
    ["et", "en"],
    ["cs", "en"],
    ["sl", "en"],
    ["sk", "cs"],
    ["hr", "sl"],
    ["sl", "hr"]
]

lang_map["en-gb"] = "eng"

for dirpath, dirnames, filenames in os.walk(root_folder):
    if is_leaf_folder(dirpath):
        for lp in languagepairs:
            if(lp[1] == "en"):
                lp[1] = "en-gb"
            src_file_path = os.path.join(dirpath, f"{lang_map[lp[0]]}.flores200.txt")
            tgt_file_path = os.path.join(dirpath, f"{lang_map[lp[0]] + '-' + lang_map[lp[1]]}.flores200-dl.txt")

            if os.path.exists(src_file_path):
                if os.path.exists(tgt_file_path):
                    continue
                else:    
                    translate_file(
                        src_lang=lp[0],
                        tgt_lang=lp[1],
                        src_file=src_file_path,
                        experiment_name=tgt_file_path
                    )
            else:
                print(f"Source file {src_file_path} does not exist. Skipping.")