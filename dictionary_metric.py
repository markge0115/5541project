# Calculate the referenceless dictionary accuracy metric.
# Keara Berlin
# 18 April 2023

from helpers import lower_except_abbrev

def calculate_dictionary_accuracy(src_sentence, tgt_sentence, dict):
    """Returns the dictionary accuracy of the given target language sentence.
    Inputs:
        src_sentence (str): the untokenized source language sentence
        tgt_sentence (str): the untokenized target language sentence (translated src_sentence)
        dict (dict): dictionary where each key is a source language term and each value is a list of the possible target language translations
        (float) the dictionary accuracy of tgt_sentence
    """
    correct_terms = []
    # TODO we need some form of tokenization for English even if it's just split because lmao "sea" isn't in the sentence
    # just because "disease" is in the sentence
    terms = get_terms(src_sentence, dict)
    if len(terms) > 0:
        pass
    for term in terms:

        translations = dict[term]
        if any_in(translations, tgt_sentence, split=False):
            correct_terms.append(term)

    if len(terms) == 0:
        acc = None
    else:
        acc = len(correct_terms) / len(terms)
    return acc

def corpus_level_dictionary_accuracy(sentences, dict):
    """Weighted average of dictionary accuracies, weighted by # of dictionary terms in sentence.
    Inputs:
        sentences (list of tuples of strs): list of sentence pairs in the corpus of the form:
                                            (src_sentence, tgt_sentence)
                                            where src_sentence is in the source language and tgt_sentence
                                            is in the target language (model translation of src_sentence)
        dict (dict): dictionary where each key is a source language term and each value is a list of the possible target language translations
    Output: 
        (float) the weighted average dictionary accuracy of the corpus
    """
    numerator = 0
    denominator = 0
    for (src_sentence, tgt_sentence) in sentences:

        weight = len(get_terms(src_sentence, dict))
        acc = calculate_dictionary_accuracy(src_sentence, tgt_sentence, dict)

        numerator += acc * weight
        denominator += weight

    return numerator / denominator

def get_terms(sentence, dict, split=True):
    """Return the terms (keys) from dict that are in sentence. Ignore proper subterms.
    Case insensitive except for words (surrounded by whitespace) that are all uppercase, like "USA".
    Inputs:
        sentence (str): the untokenized source language sentence
        dict (dict): dictionary where each key is a source language term and each value is a list of the possible target language translations
        split (bool): default True. If True, split term and sentence by whitespace and check if the term 
                        is a sublist of the sentence.
    Output: 
        (list of strs) the terms from dict that were in sentence
    """
    sentence = lower_except_abbrev(sentence)
    sentence_words = sentence.split()

    sentence_terms = []
    for term in dict.keys():
        term_words = term.split()
        
        if ((split and is_sublist(term_words, sentence_words)) \
                or (not split and term in sentence)) \
            and not is_subterm(term, sentence_terms):

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
