# Calculate the referenceless dictionary accuracy metric.
# Keara Berlin
# 18 April 2023

import time
from helpers import lower_except_abbrev, any_in, is_sublist

# def delete_element(ls, element):
#     """Return a version of a list ls without the first instance of element. 
#     Returns ls if element is not in ls."""
#     if element in ls:
#         ls.remove(element)
#     return ls

def term_recall(tgt_terms, tgt_sentence, use_chars):
    """Calculate recall between the words / characters in the term and the words/characters
    in the target language sentence. If use_chars is true, evaluate on characters, not words.
    tgt_terms is a list because there can be more than one possible translation of one source
    language term. Return only the max recall out of all tgt_terms."""
    if use_chars:
        sentence_substrs = list(tgt_sentence)
    else:
        sentence_substrs = tgt_sentence.split()
    
    max_recall = 0
    for term in tgt_terms:
        
        if use_chars:
            term_substrs = list(term)
        else:
            term_substrs = term.split()

        sum = 0
        for substr in term_substrs:
            if substr in sentence_substrs:
                sum += 1
        recall = sum / len(term_substrs)

        if recall > max_recall:
            max_recall = recall
        if max_recall >= 1:
            break

    return max_recall

def calculate_dictionary_recall(src_sentence, tgt_sentence, dict, use_chars=True):
    """Calculate dictionary recall of the given target language sentence, i.e.
    the average recall of words/characters in the target language term compared to 
    words/characters in the translated target language sentence.
    If there is more than one possible translated term, use only the max recall."""
    terms = get_terms(src_sentence, dict)
    if len(terms) == 0:
        return None
    sum_recall = 0
    for term in terms:
        translations = dict[term]
        sum_recall += term_recall(translations, tgt_sentence, use_chars=use_chars)
    return sum_recall / len(terms)

def calculate_dictionary_accuracy(src_sentence, tgt_sentence, dict, return_terms=False):
    """Returns the dictionary accuracy of the given target language sentence.
    Inputs:
        src_sentence (str): the untokenized source language sentence
        tgt_sentence (str): the untokenized target language sentence (translated src_sentence)
        dict (dict): dictionary where each key is a source language term and each value is a list of the possible target language translations
        return_terms (bool): default False. If True, returns (acc, terms, correct_terms) instead of just acc
                            where terms are the terms in the src_sentence and 
                            correct_terms are the corresponding target language terms from the dictionary which
                            are in tgt_sentence.
        (float) the dictionary accuracy of tgt_sentence
    """
    correct_terms = []
    terms = get_terms(src_sentence, dict)
    for term in terms:

        translations = dict[term]
        if any_in(translations, tgt_sentence, split=False):
            correct_terms.append(term)
    # toc = time.perf_counter()
    # print(f'get correct terms: {toc-tic:0.4f}s')

    if len(terms) == 0:
        acc = None
    else:
        acc = len(correct_terms) / len(terms)

    if return_terms:
        return (acc, terms, correct_terms)
    else:
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
    # tic = time.perf_counter()
    sentence = lower_except_abbrev(sentence)
    # toc = time.perf_counter()
    # print(f"lower: {toc-tic:0.4}s")

    # tic = time.perf_counter()
    sentence_words = sentence.split()
    # toc = time.perf_counter()
    # print(f"sentence split: {toc-tic:0.4}s")

    sentence_terms = []
    # times = 0
    for term in dict.keys():
        if not (term in sentence):
            continue 

        # tic = time.perf_counter()
        if (not split) or (split and is_sublist(term.split(), sentence_words)):
            sentence_terms.append(term)
    #     toc = time.perf_counter()
    #     times += toc-tic

    # print(f"avg is sub: {times/len(dict.keys()):0.4}s")

    final_sentence_terms = []
    for i, term in enumerate(sentence_terms):
        other_terms = sentence_terms[:i] + sentence_terms[i+1:]
        if not is_subterm(term, other_terms):
            final_sentence_terms.append(term)
        
    return final_sentence_terms

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
