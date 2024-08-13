# MF-GPT
A Mutual Fund GPT based on GPT-2

## Models

1. **Text Classifier:** A text classification model to classify whether the query is mutual funds related or not.

2. **GPT2 Model:** A GPT2-Medium base model fine-tuned on the factsheets of ICICI Prudential Mutual Fund and HDFC Mutual Fund.

## Helpers

1. **Web Scraper:** A web scraper to scrape mutual funds related articles from various websites.

2. **PDF Parser:** A PDF parser to parse the information from ICICI and HDFC MF factsheets and create a dataset for finetuning the GPT2-Medium model.

3. **MF NAVs:** A MF NAV function to download historical Mutual Funds NAV from [Free Mutual Fund API](https://www.mfapi.in/).

## TO-DO

1. Parse other AMCs factsheets and train the model
2. Train the model on various finance and mf related articles and regulatory guidelines
3. Train the model with returns of mutual funds

## Limitations

- **GPU and RAM:** Training a GPT2 model requires higher GPU and a huge RAM even for a smaller dataset.
