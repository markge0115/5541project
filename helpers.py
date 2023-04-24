# Helper functions
# Keara Berlin 23 April 2023

def lower_except_abbrev(string):
    """Make all characters in string lowercase, except words (surrounded by whitespace) that are all uppercase.
    This is meant to make case uniform but leave abbreviations like USA as uppercase."""
    words = string.split()
    lowered_words = []
    for word in words:
        if word.isupper():
            lowered_words.append(word)
        else:
            lowered_words.append(word.lower())
    return " ".join(lowered_words)

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
