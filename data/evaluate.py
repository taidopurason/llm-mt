#pip install sacrebleu unbabel-comet

import os
import pandas as pd
import json

from typing import List, Optional
from sacrebleu.metrics import BLEU, CHRF, TER
from comet import download_model, load_from_checkpoint

def write_json(json_object: object, file_path: str):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_object, f, indent=4, default=str)

def calculate_metrics(src_file, tgt_file, ref_file, metric: str):
    metric = metric.lower()
    metric_impl = None

    all_sys = []
    all_refs = []
    comet_data = []

    with open(src_file, 'r', encoding='utf-8') as f_src, \
         open(tgt_file, 'r',  encoding='utf-8') as f_tgt, \
         open(ref_file, 'r',  encoding='utf-8') as f_ref:

        src = f_src.read().strip()
        sys = f_tgt.read().strip()
        ref = f_ref.read().strip()

        all_sys.append(sys)
        all_refs.append([ref])

        if metric == "unbabel-wmt22-comet-da":
            comet_data.append({
                "src": src,
                "mt": sys,
                "ref": ref
            })

    if metric == "unbabel-wmt22-comet-da":
        model_path = download_model("Unbabel/wmt22-comet-da")
        model = load_from_checkpoint(model_path)
        model_output = model.predict(comet_data)
        score = model_output["system_score"]
    else:
        if metric == "chrf":
            metric_impl = CHRF()
        elif metric == "chrf++":
            metric_impl = CHRF(word_order=2)
        elif metric == "bleu":
            metric_impl = BLEU()
        elif metric == "ter":
            metric_impl = TER(case_sensitive=True)
        else:
            raise ValueError(f"Unknown metric {metric}")

        score = round(metric_impl.corpus_score(all_sys, all_refs).score, 2)

    print(f"{metric} score: {score}")
    return score

HOME_DIR = ''
DATA_DIR = HOME_DIR + 'translated/combined'

DATASETS = ['flores200_devtest_by_documents']
SYSTEMS = [ 'DL', 'GT', 'MS', 'OL']
LMS = [ 'palm2', 'vicuna7', 'chatgpt-doc-p2-delim']
CATEGORIES = ['one', 'many']

LANGUAGE_PAIRS = []
LANGUAGE_PAIRS.append(['en','et'])
LANGUAGE_PAIRS.append(['en','cs'])
LANGUAGE_PAIRS.append(['en','sl'])
LANGUAGE_PAIRS.append(['et','en'])
LANGUAGE_PAIRS.append(['cs','en'])
LANGUAGE_PAIRS.append(['sl','en'])
LANGUAGE_PAIRS.append(['sk','cs'])
LANGUAGE_PAIRS.append(['sl','hr'])
LANGUAGE_PAIRS.append(['hr','sl'])

SCORES = {}

for dataset in DATASETS:
    print(f"{dataset}")
    SCORES[dataset] = {}

    for lp in LANGUAGE_PAIRS:
        pair = f"{lp[0] + '-' + lp[1]}" 
        print(pair)
        SCORES[dataset][pair] = {}

        SOURCE = lp[0]   # en, et, cs, sl, sk, hr
        TARGET = lp[1]   # en, et, cs, sl, sk, hr

        for system in SYSTEMS:
            print(f"{system}")
            SCORES[dataset][pair][system] = {}

            if (system == 'DL' and (SOURCE == 'hr' or TARGET == 'hr')) or (system == 'OL' and (SOURCE == 'et' or TARGET == 'et')):
                continue
            
            for category in CATEGORIES:
                print(f"{category}")
                SCORES[dataset][pair][system][category] = {}

                ref_file = f"{DATA_DIR}/{TARGET}_{dataset}_{category}.ref"
                src_file = f"{DATA_DIR}/{SOURCE}_{dataset}_{category}.ref"
                transl_file = f"{DATA_DIR}/{SOURCE}_{TARGET}_{system}_{dataset}_{category}.txt"

                #for metric in ["chrf", "chrf++", "bleu", "unbabel-wmt22-comet-da"]:
                for metric in ["chrf", "chrf++", "bleu"]:
                    score = calculate_metrics(src_file, transl_file, ref_file, metric)

                    SCORES[dataset][pair][system][category][metric] = score

        for lm in LMS:
            print(f"{lm}")
            SCORES[dataset][pair][lm] = {}

            if (lm == 'chatgpt-doc-p2-delim' and (SOURCE == 'hr' or TARGET == 'hr')) or (lm == 'chatgpt-doc-p2-delim' and (SOURCE == 'sk' or TARGET == 'sk')) or (lm == 'palm2' and (SOURCE == 'hr' or TARGET == 'hr')) or (lm == 'vicuna7' and SOURCE == 'sk'):
                continue
            
            for category in CATEGORIES:
                print(f"{category}")
                SCORES[dataset][pair][lm][category] = {}

                ref_file = f"{DATA_DIR}/{TARGET}_{dataset}_{category}.ref"
                src_file = f"{DATA_DIR}/{SOURCE}_{dataset}_{category}.ref"
                transl_file = f"{DATA_DIR}/{SOURCE}_{TARGET}_{lm}_{dataset}_{category}.txt"

                #for metric in ["unbabel-wmt22-comet-da", "chrf", "chrf++", "bleu"]:
                for metric in ["chrf", "chrf++", "bleu"]:
                    score = calculate_metrics(src_file, transl_file, ref_file, metric)

                    SCORES[dataset][pair][lm][category][metric] = score

    write_json(SCORES, HOME_DIR + dataset + '-scores.json')
