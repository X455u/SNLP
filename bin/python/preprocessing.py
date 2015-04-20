#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import unicodecsv
import textmining

from nltk import download, word_tokenize


def tokenize(document):
    """
    A tokenizer for the Python Textmining Package that works for unicode strings
    and doesn't replace non-ASCII characters (such as 'åäö') with spaces.
    """
    document = document.lower()
    document = re.sub(u'[^\w]|[0-9]', u' ', document, flags=re.UNICODE)
    return document.strip().split()


if len(sys.argv) != 3:
    print('Usage: python preprocessing.py <inputfile> <outputfile>')

download('punkt')


input_file = sys.argv[1]

output_file = sys.argv[2]
# Text data
desc = {}
# Tokens of the text data
desc_tokens = {}
# Term document matrix
tdm = textmining.TermDocumentMatrix(tokenizer=tokenize)


# Open the data file for reading
with open(input_file) as f:
    csv_f = unicodecsv.reader(f, encoding='utf-8')

    # Read the file and tokenize
    for idx, row in enumerate(csv_f):

        if idx == 0:
            continue

        # Select the description column
        text = row[13]

        if text != '':
            desc[idx] = text
            desc_tokens[idx] = word_tokenize(text, language='finnish')
            tdm.add_doc(text)


# Write term document matrix to output file
with open(output_file, 'w') as f:
    w = unicodecsv.writer(f, encoding='utf-8')
    # cutoff = 1, also include words that only appear in a single document
    for row in tdm.rows(cutoff=1):
        w.writerow(row)


# Removing non-alphabetic tokens
for i in desc_tokens.keys():
    tokens = desc_tokens[i]


# TODO: check/print tokens with non-alpthabetic chars


# # TEST!!!!!
# a = {0:"kissa", 1:"koira", 2:".", 3:"kala", 4:"-"}
# for i in a:
#     print(a[i])

#     m = re.search(r"\W+", a[i])

# ----------------------------

for i in desc.keys():
    print(desc[i])
    print(desc_tokens[i])
    print("---")
