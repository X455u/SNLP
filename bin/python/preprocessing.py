#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import unicodecsv
import textmining
import nltk
import ConfigParser
import json
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

if len(sys.argv) != 2:
    print('Usage: python preprocessing.py <propertyfile>')

# Opening the configuration file
conf_file = sys.argv[1]
config = ConfigParser.ConfigParser()
config.read(conf_file)

# input and output files
data_file = config.get('data', 'lemmatized')
tdm_file = config.get('data', 'termdocumentmatrix')

# amount of text fields in the document
textcolumns = json.loads(config.get('data', 'textdataidx'))

# initializing term document matrices
tdms = []

for i in range(len(textcolumns)):
    tdms.append(textmining.TermDocumentMatrix(tokenizer=tokenize))
    # tdms.append(textmining.TermDocumentMatrix())


# Text data
desc = {}
# Tokens of the text data
desc_tokens = {}


# creating writers for storing the classes
class_file = config.get('data', 'classes')
classcolumns = json.loads(config.get('data', 'classidx'))

m = re.match( r'(.*)(\..*)', class_file)
class_beg =  m.group(1)
class_end = m.group(2)

writers = []

# Write term document matrices to output files
for i in range(len(textcolumns)):
    path = class_beg + str(i+1) + class_end

    f = open(path, 'w+')
    writers.append(unicodecsv.writer(f, encoding='utf-8'))



# Open the data file for reading
with open(data_file) as f:
    csv_f = unicodecsv.reader(f, encoding='utf-8')

    # Read the file and tokenize
    for idx, row in enumerate(csv_f):

        if idx == 0:

            # Copying the class headers
            for w in writers:
                headers = []

                for i in range(len(classcolumns)):
                    headers.append(row[classcolumns[i]])

                w.writerow(headers)

            continue

        # assuming that the last columns of the data file contain the lemmatized texts
        for i in range(len(textcolumns)):
            text = row[len(row)-len(textcolumns)+i]

            # TODO: separate the classes for the arrays
            if text != '':
                desc[idx] = text
                tdms[i].add_doc(text)

                classes = []

                for c in classcolumns:
                    classes.append(row[c])

                writers[i].writerow(classes)

                # print(text.encode('utf-8'))

                # tokens = word_tokenize(text, language='finnish')
                
                # tokens = tokenize(text)
                # real_tokens = remove_stopwords(tokens)
                # desc_tokens[idx] = tokens
                # tdms[i].add_doc(" ".join(real_tokens))

                # print_utf8_list(tokens)
                # print_utf8_list(real_tokens)
                # print('---')


# Splitting the tdm file path for creating tmd files for all the text columns
m = re.match( r'(.*)(\..*)', tdm_file)
tdm_beg =  m.group(1)
tdm_end = m.group(2)

# Write term document matrices to output files
for i in range(len(textcolumns)):
    path = tdm_beg + str(i+1) + tdm_end

    with open(path, 'w+') as f:
        w = unicodecsv.writer(f, encoding='utf-8')
        # cutoff = 1, also include words that only appear in a single document
        for row in tdms[i].rows(cutoff=1):
            w.writerow(row)

