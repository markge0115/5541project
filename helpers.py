# Helper functions
# Keara Berlin 23 April 2023

import csv
import re

GOOGLE = 'google_cloud_translation_v3'
M2M = 'm2m100_418M'
CHATGPT = 'chat_gpt'

EN_FILENAMES = ['data/nejm.train.en', 'data/nejm.test.en', 'data/nejm.dev.en']
ZH_FILENAMES = ['data/nejm.train.zh', 'data/nejm.test.zh', 'data/nejm.dev.zh']

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

def read_into_list(filepath, encoding='utf-8', known_only=True):
  """Read the given monolingual file into a list of strings (sentences).
  Inputs:
    filepath (str): path to the file to read
    encoding (str): encoding to use to read the file
    known_only (bool): if true, only returns sentences with only known words (no @-@)
  Output: (list of strs) list of sentences
  """
  with open(filepath, encoding=encoding) as f:
    sentences = f.read().splitlines()

  UNK = '@-@'
  if known_only:
    sentences = [s for s in sentences if UNK not in s]

  return sentences

def get_all_sentences(filepaths, known_only=True):
    """Return a list of all sentences from the specified filepaths using read_into_list()."""
    sentences = []
    for filepath in filepaths:
        sentences.extend(read_into_list(filepath, known_only=known_only))
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

def is_chinese(string):
    """Return whether the string contains any Chinese characters.
    Modified from https://stackoverflow.com/questions/2718196/find-all-chinese-text-in-a-string-using-python-and-regex"""
    chinese_substrings = re.findall(r'[\u4e00-\u9fff]+', string)
    return len(chinese_substrings) > 0
