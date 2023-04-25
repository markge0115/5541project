# Helper functions
# Keara Berlin 23 April 2023

from dataset_import import read_into_list
import csv

GOOGLE = 'google_cloud_translation_v3'
M2M = 'm2m100_418M'
CHATGPT = 'chat_gpt'

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

def get_all_sentences(filepaths):
    """Return a list of all sentences from the specified filepaths using read_into_list()."""
    sentences = []
    for filepath in filepaths:
        sentences.extend(read_into_list(filepath))
    return sentences


def lower_except_abbrev(string):
    """Make all characters in string lowercase, except words (surrounded by whitespace) that are all uppercase.
    This is meant to make case uniform but leave abbreviations like USA as uppercase."""
    words = string.split()
    lowered_words = []
    for word in words:
        if word.isupper():
            lowered_words.append(word)
        else:
            lowered_words.append(word.lower())
    return " ".join(lowered_words)

def is_sublist(sublist, superlist):
    for idx in range(len(superlist) - len(sublist) + 1):
        if superlist[idx: idx + len(sublist)] == sublist:
            return True
    return False

def any_in(terms, sentence, split=True):
    """Returns whether at least one term in terms can be found in sentence.
    Inputs:
        terms (list of strs): list of terms to check
        sentence (str): sentence to be checked for terms
        split (bool): default True. If True, split term and sentence by whitespace and check if the term 
                        is a sublist of the sentence.
    Output: (bool)
    """
    if split:
        sentence_words = sentence.split()
        for term in terms:
            term_words = term.split()
            if is_sublist(term_words, sentence_words):
                return True 
        return False
    
    else:
        for term in terms:
            if term in sentence:
                return True
        return False
