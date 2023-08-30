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
| Google Translate        | et-en   | mtee-news | **66.6**     | 36.5     | 0.8458                               | **69.7** | **109.3**|
|                         | en-et   | mtee-news | 61.7         | 23.9     | **0.8998**                           | 68.0     | 121.37   |
| DeepL                   | et-en   | mtee-news | 65.9         | **39.6** | 0.8441                               | 68.6     | 114.74   |
|                         | en-et   | mtee-news | 66.0         | 31.0     | 0.9129                               | 71.7     | 108.5    |

mtee-news results. FLORES-200 coming soon...
