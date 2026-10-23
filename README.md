# LLMs-Cultural-Values

## Updated data

The `data/step_1.1`, `data/step_1.2`, and `data/step_2.1` folders contain the newer aggregate outputs from the corresponding analysis steps. Each record has a `categories` array sourced from `Kialo-Scraper/categories/claim_tags.json` (matched by debate URL without the `.csv` suffix). An empty array means no category was available in that source.

The final step 2.1 file is `data/step_2.1/Hofstede_dimensions_with_llm_opinions_v3_thr3_final.json`. It contains 985 unique debate records and includes responses from eight model and language combinations. Its contents match `Kialo-Scraper/categories/predictions_with_tags_v3_thr3.json`.
