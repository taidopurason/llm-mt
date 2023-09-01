from translate_gt import translate_file

domains = ["business", "culture", "environment", "health", "weather"]

folders = ["flores200_dev_by_topics","flores200_dataset_filtered"]

lang_map = {
    "en": "eng",
    "et": "est",
    "sl": "slv",
    "cs": "ces",
    "ee": "est",
    "sk": "slk",
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

#lang_map["en-gb"] = "eng"

for folder in folders:
    for lp in languagepairs:
        for dom in domains:
            #if(lp[1] == "en"):
            #    lp[1] = "en-gb"
            print(lp,dom)
            src_file_path = f"../data/{folder}/{dom}/{lang_map[lp[0]]}.flores200.ref"
            tgt_file_path = f"../data/{folder}/{dom}/{lang_map[lp[0]] + '-' +lang_map[lp[1]]}.flores200-gt.txt"

            translate_file(
                src_lang=lp[0],
                tgt_lang=lp[1],
                src_file=src_file_path,
                experiment_name=tgt_file_path
            )