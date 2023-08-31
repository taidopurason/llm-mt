import os
import logging
from typing import List, Optional
from sacrebleu.metrics import BLEU, CHRF, TER

logger = logging.getLogger(__name__)

def calculate_metrics(src_folder, tgt_folder, ref_folder, metric: str):
    metric = metric.lower()
    metric_impl = None

    all_sys = []
    all_refs = []
    comet_data = []

    for filename in os.listdir(ref_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(src_folder, filename), 'r', encoding='utf-8') as f_src, \
                 open(os.path.join(tgt_folder, filename), 'r',  encoding='utf-8') as f_tgt, \
                 open(os.path.join(ref_folder, filename), 'r',  encoding='utf-8') as f_ref:

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
    src_folder = "../data/mtee-news/en_src"
    tgt_folder = "../data/mtee-news/en-et_tgt_deepl"
    ref_folder = "../data/mtee-news/en-et_ref"

    for metric in ["unbabel-wmt22-comet-da", "chrf", "chrf++", "bleu", "ter"]:
        score = calculate_metrics(src_folder, tgt_folder, ref_folder, metric)