# Calculate the referenceless dictionary accuracy metric.
# Keara Berlin
# 18 April 2023

def calculate_dictionary_accuracy(sentence, dict):
    """Returns the dictionary accuracy of the given sentence.
    Inputs:
        sentence (str): the untokenized sentence
        dict (dict): dictionary where each key is a source language term and each value is a list of the possible target language translations
        (float) the dictionary accuracy of the sentence
    """
    correct_terms = []
    terms = get_terms(sentence, dict)
    for term in terms:

        translations = dict[term]
        if any_in(translations, sentence):
            correct_terms.append(term)

    acc = len(correct_terms) / len(terms)
    return acc

def corpus_level_dictionary_accuracy(sentences, dict):
    """Weighted average of dictionary accuracies, weighted by # of dictionary terms in sentence.
    Inputs:
        sentences (list of strs): list of untokenized source language sentences in the corpus
        dict (dict): dictionary where each key is a source language term and each value is a list of the possible target language translations
    Output: 
        (float) the weighted average dictionary accuracy of the corpus
    """
    numerator = 0
    denominator = 0
    for sentence in sentences:

        weight = len(get_terms(sentence, dict))
        acc = calculate_dictionary_accuracy(sentence, dict)

        numerator += acc * weight
        denominator += weight

    return numerator / denominator

def get_terms(sentence, dict):
    """Return the terms (keys) from dict that are in sentence. Ignore proper subterms.
    Inputs:
        sentence (str): the untokenized source language sentence
        dict (dict): dictionary where each key is a source language term and each value is a list of the possible target language translations
    Output: 
        (list of strs) the terms from dict that were in sentence
    """
    sentence_terms = []
    for term in dict.keys():
        if term in sentence and not is_subterm(term, sentence_terms):
            sentence_terms.append(term)
    return sentence_terms

def is_subterm(term, terms):
    """Returns whether term is a subterm of (can be found verbatim within) any term in terms.
    For example, 'ovarian cancer' is a proper subterm of 'epithelial ovarian cancer', 
    but not of 'ovarian carcinoma'.
    is_subterm('ovarian cancer', ['teratoma', 'epithelial ovarian cancer', 'ovarian carcinoma']): True
    is_subterm('ovarian cancer', ['teratoma', 'ovarian carcinoma']): False
    """ 
    for t in terms:
        if term in t:
            return True
    return False

def any_in(terms, sentence):
    """Returns whether at least one term in terms can be found in sentence."""
    for term in terms:
        if term in sentence:
            return True 
    return False
