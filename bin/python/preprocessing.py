#!/usr/bin/env python

import csv
import sys
import textmining

from nltk import word_tokenize

if len(sys.argv) != 3:
	print("Usage: python preprocessing.py <inputfile> <outputfile>")


# opening the data file
f = open(sys.argv[1])
csv_f = csv.reader(f)

path = sys.argv[2]

# Text data
desc = {}
# Tokens of the text data
desc_tokens = {}

tdm = textmining.TermDocumentMatrix()

idx = -1

# Read the file and tokenize
for row in csv_f:
  idx += 1

  if idx == 0:
    continue

  # Dsecription column
  text = row[13]

  if text != "":
    desc[idx] = text
    print(text)
    desc_tokens[idx] = word_tokenize(text.decode('utf-8').lower())
    tdm.add_doc(text)

# cutoff =1, so all of the words
tdm.write_csv(path, cutoff=1)


# Removing non-alphabetic tokens
for i in desc_tokens.keys():
  tokens = desc_tokens[i]


# TODO: check/print tokens with non-alpthabetic chars


# # TEST!!!!!
# import re
# a = {0:"kissa", 1:"koira", 2:".", 3:"kala", 4:"-"}
# for i in a:
#   print(a[i])

#   m = re.search(r"\W+", a[i])

# ----------------------------

for i in desc.keys():
  print(desc[i])
  print(desc_tokens[i])
  print("---")
