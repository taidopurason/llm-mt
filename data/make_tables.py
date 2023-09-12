import pandas as pd
import numpy as np
import json

from pandas import json_normalize

HOME_DIR = ''

DATASETS = ['flores200_devtest_by_documents']
dataset = DATASETS[0]

data = HOME_DIR + dataset + '-scores.json'

category = 'one'
#METRICS = ['bleu', 'chrf', 'chrf++', 'unbabel-wmt22-comet-da']
METRICS = ['bleu', 'chrf', 'chrf++']

# Opening JSON file
with open(data) as json_file:
    SCORES = json.load(json_file)

    df = pd.DataFrame(index = SCORES[dataset]['en-et'].keys())

    for metric in METRICS:

        for lp in SCORES[dataset]:
            values = []

            for system in SCORES[dataset][lp]:
                if len(SCORES[dataset][lp][system]) > 0:
                    values.append(SCORES[dataset][lp][system][category][metric])
                else:
                    values.append(np.nan)

            df[lp] = values

        print(df.to_markdown())
