#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import unicodecsv
import textmining
import nltk
import ConfigParser
import json

def tokenize(document):
    """
    A tokenizer for the Python Textmining Package that works for unicode strings
    and doesn't replace non-ASCII characters (such as 'åäö') with spaces.
    """
    document = document.lower()
    document = re.sub(u'[^\w]|[0-9]', u' ', document, flags=re.UNICODE)
    return document.strip().split()

def remove_stopwords(s, stopwords):
    # Splitting the text into words and joining them again
    tokens = s.split(" ")
    tokens = [t for t in tokens if t not in stopwords]
    return " ".join(tokens)

# Used for testing
def print_utf8_list(s):
    encodedlist=', '.join(map(unicode, s))
    print(u'[{}]'.format(encodedlist).encode('UTF-8'))

###################
### MAIN STARTS ###
###################

if len(sys.argv) != 2:
    print('Usage: python preprocessing.py <propertyfile>')


### CONFIG AND OTHER FILES ###

# Opening the configuration file
conf_file = sys.argv[1]
config = ConfigParser.ConfigParser()
config.read(conf_file)

# stopwords from NLTK
stopwords = []

# Stopwords from a files
if config.getboolean('parameters', 'lemmatize'):
    stopwords.append(nltk.corpus.stopwords.words('finnish'))

    with open(config.get('stopwords', 'stopwordfile')) as f:
        csv_f = unicodecsv.reader(f, encoding='utf-8')

        # Read the file containing stopwords
        for idx, row in enumerate(csv_f):
            # one stopword per line
            if not row[0] in stopwords:
                stopwords.append(row[0])


# input and output files
data_file = config.get('data', 'lemmatized')
tdm_file = config.get('data', 'termdocumentmatrix')

### INITIALIZING DATA STRUCTURES AND WRITERS ###

# amount of text fields in the document
textcolumns = json.loads(config.get('data', 'textdataidx'))

# initializing term document matrices
tdms = []

for i in range(len(textcolumns)):
    tdms.append(textmining.TermDocumentMatrix(tokenizer=tokenize))


# creating writers for storing the classes
class_file = config.get('data', 'classes')
classcolumns = json.loads(config.get('data', 'classidx'))

m = re.match( r'(.*)(\..*)', class_file)
class_beg =  m.group(1)
class_end = m.group(2)

writers = []

# Open writers for storing document classifications
for i in range(len(textcolumns)):
    path = class_beg + str(i+1) + class_end

    f = open(path, 'w+')
    writers.append(unicodecsv.writer(f, encoding='utf-8'))

### READING THE DATA FILE ###s

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

                # there are still some capital letters after lemmatization
                text = text.lower()

                # Removing stopwords
                text = remove_stopwords(text, stopwords)

                # Add to term-document matrix
                tdms[i].add_doc(text)

                # Write classes
                classes = []

                for c in classcolumns:
                    classes.append(row[c])

                writers[i].writerow(classes)


### SAVING THE TERM-DOCUMENT MATRICES ###

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

