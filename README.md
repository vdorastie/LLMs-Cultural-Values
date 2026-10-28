# CultureProbe

CultureProbe is a dataset for studying the sociocultural values expressed by large language models (LLMs). It contains **985 debate statements** drawn from [Kialo](https://www.kialo.com/), with **2,007 statement–dimension annotations** across Hofstede's six cultural dimensions. The accompanying [paper](_EMNLP2026__Hofstede_Dimensions.pdf), *Understanding Sociocultural Alignment in Multilingual LLMs via Natural Debate Statements*, describes the method and experiments.

The method starts with naturally occurring debate statements and their Kialo votes. LLMs prompted in English and Chinese first judge whether each statement is relevant to each Hofstede dimension, then score what agreeing with it implies on a scale from −2 to +2. A multilingual, multicultural human annotation study checks the synthetic labels. The authors then ask U.S. and Chinese LLMs whether they agree with the statements and compare their dimension scores with country level human measurements. **The two model groups follow the direction of the human measurements on five of six dimensions** in the paper's group comparison; individual models and prompting languages also show differences.

## How to use the dataset

1. Load [CultureProbe.json](CultureProbe.json). It is a JSON array with one object per debate statement:

   ```python
   import json

   with open("CultureProbe.json", encoding="utf-8") as file:
       records = json.load(file)

   record = records[0]
   print(record["url"], record["dimensions"], record["scores"])
   ```

2. Use the main fields:

   | Field | Meaning |
   | --- | --- |
   | `url` | Kialo debate identifier, stored as a `.csv` filename rather than a full link. |
   | `claim` | Statement text, when present; some records omit this field. |
   | `score`, `number_of_votes` | Kialo voting score and vote count. |
   | `dimensions` | `YES`/`NO` relevance labels for `PDI`, `IDV`, `MAS`, `UAI`, `LTO`, and `IND`. |
   | `count_yes` | Number of relevance votes for each dimension. |
   | `scores` | Agreement polarity for each dimension: −2/−1 for its negative pole, +1/+2 for its positive pole, and 0 when the aggregate score is neutral or no polarity score is assigned. |
   | `llm_responses` | Model agreement (`true`) or disagreement (`false`) in English and Chinese. |
   | `chinese_llm_vote`, `us_llm_vote` | Aggregated responses of the corresponding model groups (`1` agreement, `-1` disagreement, `0` tie). |

   The dimension codes are power distance (`PDI`), individualism (`IDV`), masculinity (`MAS`), uncertainty avoidance (`UAI`), long term orientation (`LTO`), and indulgence (`IND`). See the [paper](_EMNLP2026__Hofstede_Dimensions.pdf) and [prompts](prompts/) for the definitions of each pole and the annotation procedure. For a model's position on a dimension, combine its agreement or disagreement with the statement's polarity score; disagreement reverses the score's sign.

3. To retrieve a statement and its current voting histogram from Kialo, install Python's `selenium` package and make Firefox available to Selenium. The scraper in [scrape/scrape_link.py](scrape/scrape_link.py) accepts a **full Kialo link**, so remove `.csv` from the stored identifier and add the Kialo prefix:

   ```bash
   python3 -m pip install selenium
   python3 - <<'PY'
   import json
   from scrape.scrape_link import scrape_one_link_to_json

   with open("CultureProbe.json", encoding="utf-8") as file:
       record = json.load(file)[0]

   debate_id = record["url"].removesuffix(".csv")
   link = f"https://www.kialo.com/{debate_id}"
   scrape_one_link_to_json(link, out_dir="outputs", out_name=debate_id)
   PY
   ```

   This writes `outputs/<debate_id>.json` with `url`, `statement`, and `votes`. The scraper reads Kialo's live page, so the statement or vote counts may differ from the released data. It depends on Kialo's current page layout.

The [data](data/) directory contains intermediate and evaluation predictions; [prompts](prompts/) contains the English and Chinese prompts used for the two annotation stages and model evaluation.
