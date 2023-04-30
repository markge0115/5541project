# Read bilingual dictionary csv and clean it (split synonyms into new entries)
# Keara Berlin 24 April 2023

import re
import csv
from helpers import lower_except_abbrev, any_in, is_chinese

input_path = 'data/medical_translations.csv'
output_path = 'data/medical_translations_clean.csv'

with open(output_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['English', 'Chinese'])

def split_on_parentheses(strings, mode='synonym'):
    """Split the list of strings further on parentheses.
    Inputs:
        strings (list of strs): list of strings to split further
        mode (str): synonym = split each string into parts by parentheses (assumes parentheses indicate a synonym)
                    exclude = make a copy of the string with the parenthesized sections removed
                                (assumes parentheses indicate a type or category)
    Output: 
        (list of strs) the list of strings, split further
    """
    new_strings = []
    for string in strings:

        if not any_in(['(', '[', '【', '（'], string, split=False):
            new_strings.append(string)
        else:

            if mode == 'synonym':
                split1 = string.split('(')
                for s in split1:
                    new_strings.extend(s.split(')'))

            elif mode == 'exclude':
                # modified from https://stackoverflow.com/questions/14596884/remove-text-between-and
                # new_strings.append(string)
                no_paren = re.sub("[\(\[\【\（].*?[\)\]\】\）]", "", string)
                new_strings.append(no_paren)

    new_strings = [s for s in new_strings if len(s) > 0]
    return new_strings

def remove_lenticular_brackets(strings):
    """Remove any substring between black lenticular brackets 【 】 from each string in strings. Return edited list of strings."""
    new_strings = []
    for string in strings:
        edited = re.sub("[\【].*?[\】]", "", string)
        new_strings.append(edited)
    return new_strings

with open(input_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader) # skip header row

    for i, row in enumerate(reader):
        if len(row) != 2:
            continue 

        english = row[0]
        chinese = row[1]

        if is_chinese(english) and not is_chinese(chinese):
            chinese_temp = chinese
            chinese = english
            english = chinese_temp

        english = re.split(',|，|;|；', english)
        chinese = re.split(',|，|;|；', chinese)

        english = split_on_parentheses(english, mode="synonym")
        chinese = split_on_parentheses(chinese, mode="exclude")

        english = remove_lenticular_brackets(english)

        english = [lower_except_abbrev(term.strip()) for term in english if len(term) > 0]
        chinese = [lower_except_abbrev(term.strip()) for term in chinese]

        with open(output_path, 'a', newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)
            for e in english:
                for c in chinese:
                    writer.writerow([e, c])

