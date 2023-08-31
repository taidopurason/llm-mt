import os
import logging
from typing import List, Optional
from sacrebleu.metrics import BLEU, CHRF, TER

logger = logging.getLogger(__name__)

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
        from comet import download_model, load_from_checkpoint
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

    logger.info(f"{metric} score: {score}")
    return score

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    domains = ["combined","business","communication","crime", "culture", "disaster", "environment","health", "politics", "science", "sport", "travel", "weather"]
    lang_map = {"en":"eng","et":"est","sl":"slv","cs":"ces"}
    languagepairs = []
    for lang1 in lang_map.keys():
        for lang2 in lang_map.keys():
            if lang1 == "en" or lang2 == "en":
                if lang1 != lang2:
                    languagepairs.append([lang1,lang2])

    for dom in domains:
        for lp in languagepairs:

            print(f"{dom}: {lp[0] + '-' + lp[1]}")
            src_file = f"../data/flores200_dataset_filtered/{dom}/{lang_map[lp[0]]}.flores200.txt"
            tgt_file = f"../data/flores200_dataset_filtered/{dom}/{lp[0] + '-' +lp[1]}-gt.flores200.txt"
            ref_file = f"../data/flores200_dataset_filtered/{dom}/{lang_map[lp[1]]}.flores200.txt"

    for metric in ["unbabel-wmt22-comet-da", "chrf", "chrf++", "bleu", "ter"]:
        score = calculate_metrics(src_file, tgt_file, ref_file, metric)