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
