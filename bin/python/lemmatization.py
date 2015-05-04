#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
import ConfigParser
import unicodecsv
import subprocess
import csv
from os import walk
import json
import time
import re

# NOTE: Loading the lemmatization script takes some 15s.
# Additionally, the script removes new line characters,
# so concatenating the texts into a single file would not
# have been trivial either.
# For these reasons, the text descriptions are saved as separate
# files, which are given to the script for lemmatization.

if len(sys.argv) != 2:
    print('Usage: python lemmatization.py <configfile>')

print(time.strftime("%H:%M:%S") + ' Started at')

# Opening the configuration file
conf_file = sys.argv[1]
config = ConfigParser.ConfigParser()
config.read(conf_file)



# Path of the texts for lemmatizing
dirpath = config.get('lemmatization', 'lemmatizationdir')

# Copy of the data file
# Lemmatized texts will
data = []

# Indexes of columns containing data for lemmatization
idxs = json.loads(config.get("data","textdataidx"))

print(time.strftime("%H:%M:%S") + ' Starting to read the data file')

### READING THE TEXT DESCRIPTIONS ###

# Open the data file for reading
with open(config.get('data', 'original')) as f:
    csv_f = unicodecsv.reader(f, encoding='utf-8')

    # Read the file and tokenize
    for idx, row in enumerate(csv_f):
        
        # Save row data with emty columns for the lemmas
        # The columns will be later used for storing the lemmas
        rownew = row + len(idxs) * ['']
        data.append(rownew)

        # No need to lemmatize the column headers
        if idx == 0:
            continue

        # Going through all the text columns
        for i in idxs:
            text = row[i]

            if text != '':
                # Write the text to a file
                ft = open(dirpath +"/" + 'text-' + str(idx) + '-' + str(i) + ".txt", "w+")
                ft.write(text.encode('utf-8'))
                ft.close()


print(time.strftime("%H:%M:%S") + ' Lemmatization started')

### LEMMATIZING TEXTS ###
if config.getboolean('parameters', 'lemmatize'):
    command = config.get('lemmatization', 'lemmascriptpath')
    command +=" lemmatize --locale fi " + config.get('lemmatization','lemmatizationdir') +"/*.txt" 
    subprocess.call(command, shell=True)

print(time.strftime("%H:%M:%S") + ' Lemmatization finished')
### 

# Files in the lemmatization dir
path = config.get('lemmatization', 'lemmatizationdir')
files = []
for (dirpath, dirnames, filenames) in walk(path):
    files.extend(filenames)
    break

rowlen = len(data[0])
lemmacolamount = len(idxs)

for fpath in files:
    mo = re.match(r'text-(\d+)-(\d+).txt.lemmatized', fpath)
    if mo:
        # print(fpath)
        rowidx = int(mo.group(1))
        # print(rowidx)
        colidx = int(mo.group(2))
        # print(colidx)

        text = ''

        with open(path + "/" + fpath) as f:
            # print(f)

            for row in f:
                text += row

        # print(idxs)
        # print(idxs[1])
        # print(idxs.index(colidx))
        lemmacolidx = rowlen - lemmacolamount + idxs.index(colidx)
        # print(lemmacolidx)
        data[rowidx][lemmacolidx] = text
        # print('-------')

print(time.strftime("%H:%M:%S")  + ' Reading lemmas finished')

### ADDING THE LEMMAS TO THE CSV FILE ###

# Adding headers to the lemmatized columns
data[0][15] = 'perusmuotoistettu muuttoteksti'
data[0][16] = 'perusmuotoistettu työttömyyden kuvaus'

# Saving the original data with extra columns for lemmas
f = open(config.get('data', 'lemmatized'), 'w+')
w = unicodecsv.writer(f, encoding='utf-8')
w.writerows(data)


print(time.strftime("%H:%M:%S")  + ' Finished')