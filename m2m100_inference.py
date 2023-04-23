# Translate English sentences from ParaMed into Chinese with M2M100 418M model as provided by HuggingFace:
# https://huggingface.co/facebook/m2m100_418M
# This model is trained on translation between 100 languages, including English and Chinese.
# Keara Berlin 22 April 2023

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from dataset_import import read_into_list, EN_FILENAMES

def get_all_sentences(filepaths):
    """Return a list of all sentences from the specified filepaths using read_into_list()."""
    sentences = []
    for filepath in filepaths:
        sentences.extend(read_into_list(filepath))
    return sentences

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

model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")

sentences = get_all_sentences(EN_FILENAMES)

for sentence in sentences:
    translation = translate(sentence, tokenizer, model)
    pass

