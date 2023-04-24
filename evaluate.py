# Perform automatic metric evaluation on translations of ParaMed sentences from English to Chinese 
# with M2M100, Google Translate, and ChatGPT.
# Metrics calculated: dictionary accuracy, BLEU, COMET.
# Keara Berlin 23 April 2023

import pandas as pd
import csv
from dictionary_metric import calculate_dictionary_accuracy

GOOGLE = 'google_cloud_translation_v3'
M2M = 'm2m100_418M'
CHATGPT = 'chat_gpt'

paths = {
    GOOGLE: 'google_translations.csv',
    M2M: 'm2m100_translations_test.csv', # TODO change to final path when ready
    # CHATGPT:'' # TODO
}

def read_dictionary(path='medical_translations_clean.csv'):
    """Read a dictionary csv file with two columns, keys and values, into a Python dictionary object."""
    dictionary = dict()
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) # skip header row

        for row in reader:
            key = row[0]
            value = row[1]
            if key in dictionary.keys():
                dictionary[key].append(value)
            else:
                dictionary[key] = [value]

    dictionary.pop('', None) # remove the key ''

    return dictionary

def BLEU_score(filepath, reference, language):
    ref = reference[language].tolist()
    listoftext = []
    with open(filepath, r) as csvfile:
        text = csv.reader(csvfile, delimiter=',')
        for row in text:
            listoftext.append(row)
    return sentence_bleu(ref, listoftext)

dictionary = read_dictionary()

calc_dict_acc = lambda x: calculate_dictionary_accuracy(x[0], x[1], dictionary, return_terms=True)

for (name, path) in paths.items():
    df = pd.read_csv(path)
    df[['Dictionary Accuracy','Terms','Correct Terms']] = df.apply(calc_dict_acc, axis=1, result_type='expand')
    out_path = f'{name}_dict_acc.csv'
    df.to_csv(out_path)

