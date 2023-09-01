import os
from translate_azure import translate_file
import shutil
from tqdm import tqdm

for i in tqdm(range(192)):
    src_file_path = f"../data/wmt-en-cs/{i}_source.txt"
    tgt_file_path = f"../data/translated/en_cs_MS_wmt-en-cs/wmt-en-cs/{i}_source.txt"

    if os.path.exists(tgt_file_path):
        continue
    else:

        tgt_folder_path = os.path.dirname(tgt_file_path)
        os.makedirs(tgt_folder_path, exist_ok=True)

        translate_file(
            src_lang="en",
            tgt_lang="cs",
            src_file=src_file_path,
            experiment_name=tgt_file_path
            )
                
folder_to_zip = f"../data/translated/en_cs_MS_wmt-en-cs/"
shutil.make_archive(folder_to_zip, 'zip', folder_to_zip)
shutil.rmtree(folder_to_zip)