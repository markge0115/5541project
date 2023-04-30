import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
#import jieba

EN_FILENAMES = ['data/nejm.train.en', 'data/nejm.test.en', 'data/nejm.dev.en']
ZH_FILENAMES = ['data/nejm.train.zh', 'data/nejm.test.zh', 'data/nejm.dev.zh']

def read_into_str(filepath, encoding='utf-8'):
  str = ""
  with open(filepath, encoding=encoding) as f:
    lines = f.readlines()
    str += ' '.join(lines)
  return str

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

# look at sentence pairs
f_en = open('data/nejm.train.en', encoding='utf-8')
lines_en = list(f_en.readlines())
f_zh = open('data/nejm.train.zh', encoding='utf-8')
lines_zh = list(f_zh.readlines())
for i, (en, zh) in enumerate(zip(lines_en, lines_zh)):
  if i % 100 == 0:
    print(f"En: {en}")
    print(f"Zh: {zh}")
    print("\n")

#importing the files as lists of sentences
# trainen_list = read_into_list('nejm.train.en')
# trainzh_list = read_into_list('nejm.train.zh')
# testen_list = read_into_list('nejm.test.en')
# testzh_list = read_into_list('nejm.test.zh')
# deven_list = read_into_list('nejm.dev.en')
# devzh_list = read_into_list('nejm.dev.zh')

# # importing the files as strings
# trainenstr = read_into_str('nejm.train.en')
# trainzhstr = read_into_str('nejm.train.zh')
# testenstr = read_into_str('nejm.test.en')
# testzhstr = read_into_str('nejm.test.zh')
# devenstr = read_into_str('nejm.dev.en')
# devzhstr = read_into_str('nejm.dev.zh')

# #tokenizing in english then chinese
# tokenizedtrainen = nltk.word_tokenize(trainenstr)
# tokenizedtesten = nltk.word_tokenize(testenstr)
# tokenizeddeven = nltk.word_tokenize(devenstr)

# tokenizedtrainzh = jieba.lcut(trainzhstr)
# tokenizedtestzh = jieba.lcut(testzhstr)
# tokenizeddevzh = jieba.lcut(devzhstr)

# #transferring into dataframes
# traindf = pd.DataFrame({'en': pd.Series(tokenizedtrainen), 'zh': pd.Series(tokenizedtrainzh)})
# testdf = pd.DataFrame({'en': pd.Series(tokenizedtesten), 'zh': pd.Series(tokenizedtestzh)})
# devdf = pd.DataFrame({'en': pd.Series(tokenizeddeven), 'zh': pd.Series(tokenizeddevzh)})
