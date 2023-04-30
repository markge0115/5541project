# Translate English sentences from ParaMed into Chinese with Google Translate's cloud API.
# https://cloud.google.com/translate/docs/reference/rpc/google.cloud.translation.v3 
# Keara Berlin 22 April 2023

from dataset_import import read_into_list, EN_FILENAMES
from helpers import get_all_sentences, writerow
import csv
from google.cloud import translate
from os import environ

PROJECT_ID = environ.get("PROJECT_ID", "")
assert PROJECT_ID
PARENT = f"projects/{PROJECT_ID}"

output_filepath = 'output/google_translations.csv'

def get_str_between_quotes(string):
    """Return the portion of the string between two quotation marks ("). 
    Assumes there are exactly 2 double quote chars in string."""
    first_quote = string.find('"')
    end_string = string[first_quote+1:]
    second_quote = end_string.find('"')
    return end_string[:second_quote]

def google_translate(sentence, src_lang="en-US", tgt_lang="zh", project_id="nlp-final-project-384603"):
    """Return a translation of sentence from one language to another using Google Cloud Translation API.
    Inputs:
        sentence: (str) The sentence to translate
        src_lang (str): source language code, e.g. "en-US"
        tgt_lang (str): target language code, e.g. "zh"
        project_id (str): project id from Google account
    Output: 
        (str) translated sentence
    """
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [sentence],
            "mime_type": "text/plain",
            "source_language_code": src_lang,
            "target_language_code": tgt_lang,
        }
    )

    # response = client.translate_text(
    #             parent=PARENT,
    #             contents=[sentence],
    #             target_language_code=tgt_lang,
    #     )

    # for translation in response.translations:
    #     print("Translated text: {}".format(translation.translated_text))

    return response.translations[0].translated_text

writerow(['English', 'Chinese'], output_filepath, mode='w')

sentences = get_all_sentences(EN_FILENAMES)

# Limit to 3385 sentences to stay within free pricing range of # characters submitted.
for sentence in sentences[:3385]:
    translation = google_translate(sentence)
    writerow([sentence, translation], output_filepath)
