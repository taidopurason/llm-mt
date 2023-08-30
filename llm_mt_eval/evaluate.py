import logging
from typing import List, Optional

from sacrebleu.metrics import BLEU, CHRF, TER

logger = logging.getLogger(__name__)


def score_results(
        metric: str,
        ref_lines: List[str],
        hyp_lines: List[str],
        src_lines: Optional[List[str]] = None
) -> float:
    metric = metric.lower()
    if metric == "unbabel-wmt22-comet-da":
        if src_lines is None:
            raise ValueError("src_lines must be provided for Unbabel/wmt22-comet-da")

        from comet import download_model, load_from_checkpoint
        model_path = download_model("Unbabel/wmt22-comet-da")
        model = load_from_checkpoint(model_path)
        model_output = model.predict(
            [{"src": src, "mt": mt, "ref": ref} for src, mt, ref in zip(src_lines, hyp_lines, ref_lines)]
        )
        score = round(model_output["system_score"], 4)
        logger.info(f"{metric} score: {score}")
        return score
    elif metric == "chrf":
        metric_impl = CHRF()
    elif metric == "chrf++":
        metric_impl = CHRF(word_order=2)
    elif metric == "spbleu_flores200":
        metric_impl = BLEU(tokenize="flores200")
    elif metric == "bleu":
        metric_impl = BLEU()
    elif metric == "ter":
        metric_impl = TER(case_sensitive=True)
    else:
        raise ValueError(f"Unknown metric {metric}")

    score = round(metric_impl.corpus_score(hyp_lines, [ref_lines]).score, 2)
    logger.info(metric_impl.get_signature())
    logger.info(f"{metric} score: {score}")
    return score
