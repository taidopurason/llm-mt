import os
from tqdm import tqdm
import zipfile

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

ind = 0

mt_models = ["GT","OL","MS","DL","chatgpt-doc-p2-delim","mtee","chatgpt-sent-p2","palm2","vicuna7"]
datasets = ["flores200_devtest_by_documents","wmt-en-cs","mtee-news"]
methods = ["many","one"]

for model in tqdm(mt_models):
    for lp in tqdm(languagepairs):
        for dataset in datasets:
            for method in methods:
                zip_file_path = f"../data/translated/{lp[0]}_{lp[1]}_{model}_{dataset}.zip"
                combined_txt_path = f"../data/translated/combined/{lp[0]}_{lp[1]}_{model}_{dataset}_{method}.txt"

                combined_contents = ""

                if os.path.exists(zip_file_path):
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        for file_info in zip_ref.infolist():
                            valid_file = False

                            if dataset == "flores200_devtest_by_documents":
                                valid_file = file_info.filename.startswith(f'{dataset}/') and file_info.filename.endswith('.txt')
                            elif dataset == "wmt-en-cs":
                                valid_file = file_info.filename.startswith(f'wmt-en-cs/') and file_info.filename.endswith('.txt')
                            elif dataset == "mtee-news":
                                valid_file = file_info.filename.startswith(f'mtee-news/{lp[0]}_src/') and file_info.filename.endswith('.txt')

                            if valid_file:
                                with zip_ref.open(file_info.filename) as file:
                                    file_contents = file.read().decode('utf-8').strip()

                                    if method == "one":
                                        file_contents = file_contents.replace("\n", " ").replace("\r", " ").strip()
                                        combined_contents += file_contents + "\n"
                                    elif method == "many":
                                        file_lines = [line.strip() for line in file_contents.split('\n') if line.strip()]
                                        combined_contents += '\n'.join(file_lines)
                                        combined_contents += '\n'

                    with open(combined_txt_path, 'w', encoding='utf-8') as f:
                        f.write(combined_contents)
                else:
                    continue