import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
import jieba

def read_into_str(filepath, encoding='utf-8'):
  str = ""
  with open(filepath, encoding=encoding) as f:
    lines = f.readlines()
    str += ' '.join(lines)
  return str

#importing the files as strings
trainenstr = read_into_str('nejm.train.en')
trainzhstr = read_into_str('nejm.train.zh')
testenstr = read_into_str('nejm.test.en')
testzhstr = read_into_str('nejm.test.zh')
devenstr = read_into_str('nejm.dev.en')
devzhstr = read_into_str('nejm.dev.zh')
  
#tokenizing in english then chinese
tokenizedtrainen = nltk.word_tokenize(trainenstr)
tokenizedtesten = nltk.word_tokenize(testenstr)
tokenizeddeven = nltk.word_tokenize(devenstr)

tokenizedtrainzh = jieba.lcut(trainzhstr)
tokenizedtestzh = jieba.lcut(testzhstr)
tokenizeddevzh = jieba.lcut(devzhstr)

#transferring into dataframes
traindf = pd.DataFrame({'en': pd.Series(tokenizedtrainen), 'zh': pd.Series(tokenizedtrainzh)})
testdf = pd.DataFrame({'en': pd.Series(tokenizedtesten), 'zh': pd.Series(tokenizedtestzh)})
devdf = pd.DataFrame({'en': pd.Series(tokenizeddeven), 'zh': pd.Series(tokenizeddevzh)})
