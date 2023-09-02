# Results

### Prompts


| Prompt ID | prompt_example                                               | chrF++ ↑  | BLEU ↑    | unbabel-wmt22-comet-da ↑ | chrF ↑    | spbleu_flores200 ↑ | TER ↓     | prompt_tokens ↓ | completion_tokens ↓ | cost (USD) ↓ |
|-----------| ------------------------------------------------------------ |----------|----------|-------------------------|----------|-------------------|----------|----------------|--------------------|-------------|
| P1        | Provide the English translation for the sentence:\\n{sent}   | 62.1     | 36.5     | 0.8903                  | 64.2     | 41                | 52       | **66065**      | 27634              | **0.154**   |
| P2        | Translate the following Estonian text into English:\\n{sent} | **62.6** | **36.7** | **0.8946**              | **64.7** | **41.3**          | **51.5** | 67077          | 27514              | 0.156       |
| P3        | Translate this sentence from Estonian to English:\\n{sent}   | 62.4     | 36.5     | 0.8944                  | 64.5     | 41                | 51.6     | 67077          | **27451**          | 0.156       |

FLORES-200 results. P1 is from [https://arxiv.org/pdf/2304.02210.pdf](https://arxiv.org/pdf/2304.02210.pdf). P2 is proposed by GPT-4 by asking "Provide five concise prompts or templates that can make you translate from Estonian to English." (idea adapted from [https://arxiv.org/abs/2301.08745](https://arxiv.org/abs/2301.08745)).


### Regular MT baselines

| MT | lang | dataset                                          | chrF++   | BLEU       | unbabel-wmt22-comet-da  | chrF     | TER      |
|----| -----| -------------------------------------------------|----------|------------|-------------------------|----------|----------|
| Google Translate        | et-en   | mtee-news | **66.6**     | 36.5     | 0.8458                               | 69.7     | 109.3    |
|                         | en-et   | mtee-news | 61.7         | 23.9     | 0.8998                               | 68.0     | 121.37   |
| DeepL                   | et-en   | mtee-news | 65.9         | **39.6** | 0.8441                               | 68.6     | 114.74   |
|                         | en-et   | mtee-news | 66.0         | 31.0     | **0.9129**                           | **71.7** | **108.5**|

## BLEU for flores200 ##
| MT | en-et | en-cs | en-sl | et-en | cs-en | sl-en | sk-cs | sl-hr | hr-sl |
| ---------------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| DeepL | 33.47 | 38.58 | 39.96 | 45.91 | 50.17 | 45.09 | 33.41 | / | / |
| Google Translate| 27.22 | 32.58 | 32.17 | 35.72 | 37.79 | 33.93 | 27.9 | 25.65 | 26.72 |
| Microsoft Azure | 34.65 | 40.9 | 37.89 | 42.55 | 47.84 | 39.85 | 34.13 | 29.42 | 31.69 |
| OnlineL | / | 37.02 | 29.99 | / | 45.19 | 34.94 | 31.61 | 25.09 | 27.72 |
