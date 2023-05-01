# Perform automatic metric evaluation on translations of ParaMed sentences from English to Chinese 
# with M2M100, Google Translate, and ChatGPT.
# Metrics calculated: dictionary accuracy, BLEU.
# Keara Berlin, Kim Welch - 23 April 2023

import pandas as pd
import numpy as np
import csv
import jieba
import re
from dictionary_metric import calculate_dictionary_accuracy, calculate_dictionary_recall
from helpers import *
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

paths = {
    GOOGLE: 'output/google_translations.csv',
    M2M: 'output/m2m100_translations.csv',
    CHATGPT: 'output/gpt_translations.csv'
}

def read_dictionary(path='data/medical_translations_clean.csv'):
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
    """Read in source language sentences and reference translations as a two-column pandas dataframe."""
    src_sentences = get_all_sentences(EN_FILENAMES, known_only=False)
    ref_sentences = get_all_sentences(ZH_FILENAMES, known_only=False)
    ref_df = pd.DataFrame([src_sentences, ref_sentences]).transpose()
    ref_df.columns = ["English", "Reference"]
    return ref_df

def tokenize_sentences(sentences):
    """Tokenize the list of Chinese sentences with jieba."""
    tokenized = []
    for sentence in sentences:
        tokenized.append(jieba.lcut(sentence))
    return tokenized

def tokenize(sentence):
    """Tokenize the sentence string with jieba and remove any whitespace tokens."""
    tokenized = jieba.lcut(sentence)
    cleaned = [t for t in tokenized if t.strip() != '']
    return cleaned

def bleu(row):
    """Calculate BLEU score for one row of a pandas dataframe, with columns 
        ['English','Chinese','Reference'] where the English is the source sentence,
        Chinese is the machine translated sentence, and Reference is the reference translation."""
    tokenized_hypothesis = tokenize(row['Chinese'])
    tokenized_reference = tokenize(row['Reference'])
    smooth_fn = SmoothingFunction()
    bleu_score = sentence_bleu([tokenized_reference], 
                               tokenized_hypothesis,
                               smoothing_function=smooth_fn.method7)
    return bleu_score

def clean_translation(row):
    """Clean the Chinese translation output in one row of a pandas dataframe, so that only
    the Chinese translation and not any prepended copy of the source language sentence is included.
        Dataframe columns = ['English','Chinese','Reference'] where English is the source sentence,
        Chinese is the machine translated sentence, and Reference is the reference translation."""

    translation = row['Chinese']
    parts = re.split('中文：|Chinese:', translation)
    return parts[-1].strip()

dictionary = read_dictionary()
references = read_references()

# x will be a row of a pandas df of the form [src_sentence, hypothesis, reference]
# calc_dict_acc = lambda x: calculate_dictionary_accuracy(x[0], x[1], dictionary, return_terms=True)
calc_dict_acc = lambda x: calculate_dictionary_recall(x[0], x[1], dictionary)

for (name, path) in paths.items():
    df = pd.read_csv(path)
    small = df.iloc[:3382,:]

    if name == CHATGPT:
        small['Chinese'] = small.apply(clean_translation, axis=1)

    small = small.merge(references, on=["English"])

    small['BLEU'] = small.apply(bleu, axis=1) 
    # small[['Dictionary Accuracy','Terms','Correct Terms']] = small.apply(calc_dict_acc, axis=1, result_type='expand')
    small['Dictionary Accuracy'] = small.apply(calc_dict_acc, axis=1)

    out_path = f'output/{name}_dict_recall_bleu.csv'
    small.to_csv(out_path)
