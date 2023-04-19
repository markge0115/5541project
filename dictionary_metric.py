# Calculate the referenceless dictionary accuracy metric.
# Keara Berlin
# 18 April 2023

def calculate_dictionary_accuracy(sentence, dict):
    """Returns the dictionary accuracy of the given sentence.
    Inputs:
        sentence (str): the untokenized sentence
        dict (dict): dictionary with keys being source language terms and values being target language translations
    Output:
        (float) the dictionary accuracy of the sentence
    """
    pass 

def corpus_level_dictionary_accuracy(infos, dict):
    """Weighted average of dictionary accuracies by # of dictionary terms in sentence
    Inputs:
        infos (list): a list of dictionaries of the form {'sentence':str, 'n_terms':int, 'acc':float}
                        where n_terms is the number of dictionary terms in that sentence.
                        sentence is optional if both n_terms and acc are given.
                        acc and n_terms are optional if sentence is given.
        dict (dict): dictionary with keys being source language terms and values being target language translations
    Output:
        (float) the weighted average dictionary accuracy of the dataset
    """
    SENTENCE_KEY = 'sentence'
    N_TERMS_KEY = 'n_terms'
    ACC_KEY = 'acc'

    numerator = 0
    denominator = 0

    for info in infos:
        ks = info.keys()

        if N_TERMS_KEY in ks and ACC_KEY in ks:
            weight = info[N_TERMS_KEY]
            acc = info[ACC_KEY]
        
        elif SENTENCE_KEY in ks:
            sentence = info[SENTENCE_KEY]
            weight = count_n_terms(sentence, dict)
            acc = calculate_dictionary_accuracy(sentence, dict)

        else:
            acc = 0
            weight = 1

        numerator += acc * weight
        denominator += weight

    return numerator / denominator

def count_n_terms(sentence, dict):
    """Return the number of terms (keys) from dict that are in sentence. Ignore proper subterms.
    Inputs:
        sentence (str): the untokenized sentence
        dict (dict): dictionary with keys being source language terms and values being target language translations
    Output: 
        (int) the number of terms from dict in sentence
    """
    pass
