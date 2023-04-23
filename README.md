# NLP Final Project

Spring 2023

## Required Packages

pip install:

- transformers
- pandas
- numpy
- nltk 
- jieba
- sentencepiece
- beautifulsoup4
- requests
- google-cloud-translate
- ipython

## Files

### main.py
Run this file to scrape online Chinese-English biomedical term dictionary.

### dataset_import.py 
Load ParaMed parallel corpus for English-Chinese sentence level translation in the biomedical domain.

### dictionary_metric.py 
Provides methods to calculate dictionary accuracy at the sentence or document level.

### google_inference.py
Use Google Cloud Translation v3 API to translate English ParaMed sentences into Chinese.

To set up and use the API yourself, follow instructions at: https://codelabs.developers.google.com/codelabs/cloud-translation-python3#0

You may need to also run in the Google Cloud CLI:

gcloud auth application-default login

And then run:

gcloud auth application-default set-quota-project your-project-id

To set your PROJECT_ID variable permanently, run:

setx /M PROJECT_ID your-project-id

Then close and reopen your terminal or IDE. You should then be able to run scripts like in the example above from an IDE or from the command line using the Google Cloud Translation API.

