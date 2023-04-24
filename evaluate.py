# Perform automatic metric evaluation on translations of ParaMed sentences from English to Chinese 
# with M2M100, Google Translate, and ChatGPT.
# Metrics calculated: dictionary accuracy, BLEU, COMET.
# Keara Berlin 23 April 2023

import pandas as pd
import csv
import time
from dictionary_metric import calculate_dictionary_accuracy
from helpers import get_all_sentences
from nltk.translate.bleu_score import sentence_bleu
from dataset_import import EN_FILENAMES, ZH_FILENAMES

GOOGLE = 'google_cloud_translation_v3'
M2M = 'm2m100_418M'
CHATGPT = 'chat_gpt'

paths = {
    # GOOGLE: 'google_translations.csv',
    M2M: 'm2m100_translations.csv',
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

#Parameters:
#   filepath: filename of a csv file, ie "output.csv"
#   reference: sentences from paramed
def BLEU_score(dataframe, reference):
    listofresults = []
    listoftext = dataframe.tolist()
    for sentence in references:
        listofresults.append(sentence_bleu(sentence, listoftext))
    return listofresults

def read_references():
    src_sentences = get_all_sentences(EN_FILENAMES)
    ref_sentences = get_all_sentences(ZH_FILENAMES)
    references = {}
    for src, ref in zip(src_sentences, ref_sentences):
        references[src] = ref
    return references

dictionary = read_dictionary()
references = read_references()

calc_dict_acc = lambda x: calculate_dictionary_accuracy(x[0], x[1], dictionary, return_terms=True)
bleu = lambda x: sentence_bleu([references[x[0]]], x[1])

for (name, path) in paths.items():
    df = pd.read_csv(path)
    df['BLEU'] = df.apply(bleu, axis=1) 
    df[['Dictionary Accuracy','Terms','Correct Terms']] = df.apply(calc_dict_acc, axis=1, result_type='expand')
    out_path = f'{name}_dict_acc.csv'
    df.to_csv(out_path)

