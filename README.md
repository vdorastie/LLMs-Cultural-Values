# LLMs-Cultural-Values

## Updated data

The `data/step_1.1` and `data/step_1.2` folders follow the existing `step_1` and `step_2` layout: an aggregate `predictions.json` and one `predictions.json` in each model and language folder. They combine the available `answers`, `answers_09.09.2025`, `answers_combined`, `answers_relaxed_v2`, `answers_threshold_new`, and `answers_v3` datasets from the corresponding `Hofstede_New` step. When the same debate URL occurs in several inputs, the later folder in that order supplies the record. Some models occur in only a subset of those folders, so their record counts differ.

Each record has a `categories` array sourced from `Kialo-Scraper/categories/claim_tags.json` (matched by debate URL without the `.csv` suffix). An empty array means no category was available in that source. Every output JSON has unique debate URLs.

The final step 2.1 file is `data/step_2.1/Hofstede_dimensions_with_llm_opinions_v3_thr3_final.json`. It contains 985 unique debate records and includes responses from eight model and language combinations. Its contents match `Kialo-Scraper/categories/predictions_with_tags_v3_thr3.json`.
