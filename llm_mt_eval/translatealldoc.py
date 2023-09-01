import os
from translate_deepl import translate_file
import shutil
from tqdm import tqdm

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
    ["sk", "cs"]
]

##Uncomment for Deepl
#lang_map["en-gb"] = "eng"

for root, dirs, files in os.walk(root_folder):
    for dir in tqdm(dirs):
        for lp in languagepairs:
            src_file_path = os.path.join(root, f"{dir}/{lang_map[lp[0]]}.flores200.txt")
            tgt_file_path = f"../data/translated/{lp[0]}_{lp[1]}_DL_flores200_devtest_by_documents/flores200_devtest_by_documents/{dir}/{lang_map[lp[0]]}.flores200.txt"

            if os.path.exists(tgt_file_path):
                continue
            else:

                tgt_folder_path = os.path.dirname(tgt_file_path)
                os.makedirs(tgt_folder_path, exist_ok=True)

                #Uncomment for Deepl
                #if(lp[1] == "en"):
                #    lp[1] = "en-gb"
                translate_file(
                    src_lang=lp[0],
                    tgt_lang=lp[1],
                    src_file=src_file_path,
                    experiment_name=tgt_file_path
                    )
                #Uncomment for Deepl
                #if(lp[1] == "en-gb"):
                #    lp[1] = "en"
            

for lp in languagepairs:
    folder_to_zip = f"../data/translated/{lp[0]}_{lp[1]}_DL_flores200_devtest_by_documents/"
    shutil.make_archive(folder_to_zip, 'zip', folder_to_zip)
    shutil.rmtree(folder_to_zip)