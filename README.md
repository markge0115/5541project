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

## Files

### main.py
Run this file to scrape online Chinese-English biomedical term dictionary.

### dataset_import.py 
Load ParaMed parallel corpus for English-Chinese sentence level translation in the biomedical domain.

### dictionary_metric.py 
Provides methods to calculate dictionary accuracy at the sentence or document level.

### t5_inference.py
Uses T5 to translate ParaMed English sentences into Chinese.