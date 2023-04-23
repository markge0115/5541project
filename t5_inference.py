# Translate English sentences from ParaMed into Chinese with T5 model (t5-small) as provided by HuggingFace:
# https://huggingface.co/docs/transformers/model_doc/t5#inference
# T5 is pretrained on many text-to-text NLP tasks and has good performance on many tasks as a result.
# Keara Berlin 22 April 2023

from transformers import T5Tokenizer, T5ForConditionalGeneration
from dataset_import import read_into_list, EN_FILENAMES

def get_all_sentences(filepaths):
    """Return a list of all sentences from the specified filepaths using read_into_list()."""
    sentences = []
    for filepath in filepaths:
        sentences.extend(read_into_list(filepath))
    return sentences

def translate(sentence, tokenizer, model, from_lang="English", to_lang="French"):
    """Return a translation of sentence from one language to another using T5.
    Inputs:
        sentence: (str) The sentence to translate
        tokenizer: (Tokenizer) HuggingFace tokenizer object for the given model
        model: (torch.nn.Module) HuggingFace model object to use for translation
        from_lang (str): source language
        to_lang (str): target language
    Output: 
        (str) translated sentence
    """
    prompt = f'translate {from_lang} to {to_lang}: {sentence}'
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length=200)
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

sentences = get_all_sentences(EN_FILENAMES)

for sentence in sentences:
    translation = translate(sentence, tokenizer, model)
    pass

