# Translate English sentences from ParaMed into Chinese with M2M100 418M model as provided by HuggingFace:
# https://huggingface.co/facebook/m2m100_418M
# This model is trained on translation between 100 languages, including English and Chinese.
# Keara Berlin 22 April 2023

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from dataset_import import read_into_list, EN_FILENAMES
import csv

output_filepath = 'output/m2m100_translations_test.csv'

def get_all_sentences(filepaths):
    """Return a list of all sentences from the specified filepaths using read_into_list()."""
    sentences = []
    for filepath in filepaths:
        sentences.extend(read_into_list(filepath))
    return sentences[:100]

def translate(sentence, tokenizer, model, src_lang="en", tgt_lang="zh"):
    """Return a translation of sentence from one language to another using M2M100.
    Inputs:
        sentence: (str) The sentence to translate
        tokenizer: (Tokenizer) HuggingFace tokenizer object for the given model
        model: (torch.nn.Module) HuggingFace model object to use for translation
        src_lang (str): source language code, e.g. "en"
        tgt_lang (str): target language code, e.g. "zh"
    Output: 
        (str) translated sentence
    """
    tokenizer.src_lang = src_lang
    input_tokens = tokenizer(sentence, return_tensors="pt")
    generated_tokens = model.generate(**input_tokens, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

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

model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

writerow(['English', 'Chinese'], output_filepath, mode='w')

sentences = get_all_sentences(EN_FILENAMES)

for sentence in sentences:
    translation = translate(sentence, tokenizer, model)
    writerow([sentence, translation], output_filepath)
