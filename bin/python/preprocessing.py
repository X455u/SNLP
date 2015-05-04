#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import unicodecsv
import textmining
import nltk
# from nltk import download, word_tokenize


def tokenize(document):
    """
    A tokenizer for the Python Textmining Package that works for unicode strings
    and doesn't replace non-ASCII characters (such as 'åäö') with spaces.
    """
    document = document.lower()
    document = re.sub(u'[^\w]|[0-9]', u' ', document, flags=re.UNICODE)
    return document.strip().split()


def remove_stopwords(tokens):
    stopwords = nltk.corpus.stopwords.words('finnish')
    tokens = [t for t in tokens if t not in stopwords]

    return tokens

# Workaround to print tokens nicely
def print_utf8_list(s):
    encodedlist=', '.join(map(unicode, s))
    print(u'[{}]'.format(encodedlist).encode('UTF-8'))


### Main starts ###

if len(sys.argv) != 3:
    print('Usage: python preprocessing.py <inputfile> <outputfile>')


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
            # tokens = word_tokenize(text, language='finnish')
            tokens = tokenize(text)
            real_tokens = remove_stopwords(tokens)
            desc_tokens[idx] = tokens
            tdm.add_doc(" ".join(real_tokens))

            # print_utf8_list(tokens)
            # print_utf8_list(real_tokens)
            # print('---')


# TODO: perform lemmatization




# Write term document matrix to output file
with open(output_file, 'w') as f:
    w = unicodecsv.writer(f, encoding='utf-8')
    # cutoff = 1, also include words that only appear in a single document
    for row in tdm.rows(cutoff=1):
        w.writerow(row)

