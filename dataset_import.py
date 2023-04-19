import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
import jieba

#importing the files as strings
trainenstr = ""
with open ('nejm.train.en') as f:
  lines = f.readlines()
  trainenstr += ' '.join(lines)

trainzhstr = ""
with open ('nejm.train.zh', encoding='utf-8') as f:
  lines = f.readlines()
  trainzhstr += ' '.join(lines)

testenstr = ""
with open ('nejm.test.en') as f:
  lines = f.readlines()
  testenstr += ' '.join(lines)

testzhstr = ""
with open ('nejm.test.zh', encoding='utf-8') as f:
  lines = f.readlines()
  testzhstr += ' '.join(lines)

devenstr = ""
with open ('nejm.dev.en') as f:
  lines = f.readlines()
  devenstr += ' '.join(lines)

devzhstr = ""
with open ('nejm.dev.zh', encoding='utf-8') as f:
  lines = f.readlines()
  devzhstr += ' '.join(lines)
  
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
