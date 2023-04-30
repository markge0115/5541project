#Translate sentences from ParaMed from english to chinese using ChatGPT
# Morgan Reese 23 April 2023

import csv
from dataset_import import read_into_list, EN_FILENAMES
from os import environ
import openai
import re
openai.api_key = "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"
output_filepath = "output/gpt_translations.csv"

def get_all_sentences(filepaths):
    """Return a list of all sentences from the specified filepaths using read_into_list()."""
    sentences = []
    for filepath in filepaths:
        sentences.extend(read_into_list(filepath))
    return sentences

def get_str_between_quotes(string):
    """Return the portion of the string between two quotation marks (").
    Assumes there are exactly 2 double quote chars in string."""
    first_quote = string.find('"')
    end_string = string[first_quote+1:]
    second_quote = end_string.find('"')
    return end_string[:second_quote]

def chatgpt_translate(sentence):
    gpt = openai.Completion.create(engine = "text-davinci-002",
    prompt = f"Translate the following text into Chinese:\n{sentence}\n---\nEnglish:",
    temperature = 0.7,
    max_tokens = 1000,
    n = 1,
    stop = None,
    timeout=120,)
    translation =gpt.choices[0].text.strip()
    return translation

def writerow(row, filepath, mode='a'):
    """Write a row to the csv at filepath with given mode (default "a" for append).
    Inputs:
        row: (list) a list of values to write as the row
        filepath: (str) filepath of csv
        mode: (str) write mode, e.g. 'a' for append or 'w' for write
    """
    with open(filepath, mode=mode, newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

writerow(['English', 'Chinese'], output_filepath, mode='w')

sentences = get_all_sentences(EN_FILENAMES)

for i,sentence in enumerate(sentences):
    translation = chatgpt_translate(sentence)
    writerow([sentence, translation], output_filepath)
    #if(i%100 == 0):
    print(f"{i/len(sentences)}%")
    print(translation)
