#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ConfigParser
import unicodecsv
import json
import sys

### FUNCTIONS FOR COUNTING CLUSTER STATISTICS ### 

def avgtextlen(texts):
    count = 0
    for t in texts:
        count += len(t.split())

    return count / float(len(texts))

def maxtextlen(texts):
    maxlen = 0

    for t in texts:
        l = len(t.split())
        if l > maxlen:
            maxlen = l

    return maxlen


def mintextlen(texts):
    minlen = sys.maxint

    for t in texts:
        l = len(t.split())
        if l < minlen:
            minlen = l

    return minlen

###################
### MAIN STARTS ###
###################

if len(sys.argv) != 2:
    print('Usage: python sortclusters.py <propertyfile>')

# opening the config file
conf_file = sys.argv[1]
config = ConfigParser.ConfigParser()
config.read(conf_file)

classes = []

# Reading the SOM cluster data
with open(config.get('clusters', 'clustercounts')) as f:
    csv_f = unicodecsv.reader(f, encoding='utf-8')

    # Read the file and tokenize
    for idx, row in enumerate(csv_f):
        classes = row

# Transforming the data into numbers
classes = [int(i) for i in classes]

data_file = config.get('clusters', 'descriptions')
text_idx = json.loads(config.get('data', 'textdataidx'))[0]


# Reading the text descriptions
clusters = []
for i in range(max(classes)):
    clusters.append([])


with open(data_file) as f:
    csv_f = unicodecsv.reader(f, encoding='utf-8')

    # Read the file and tokenize
    for idx, row in enumerate(csv_f):

        if idx == 0:
            continue

        c = classes[idx-1]
        clusters[c-1].append(str(idx) + ": " + row[0])


# Writing the large clusters with their texts and some statistics
with open(config.get('clusters', 'clustertexts'),"w") as f:

    for i in range(len(clusters)):
        c = clusters[i]

        # Ignore filler clusters
        if len(c) > 1:

            # Writing cluster info
            f.write("Cluster: " + str(i+1) + "  Texts: " + str(len(c)) + "\n")
            f.write("Avg len: " +  str(avgtextlen(c)) + "  Min len: " + str(mintextlen(c)) + "  Max len: " + str(maxtextlen(c)) + "\n" )

            # Writing the text descriptions
            for s in c:
                f.write(s.encode('utf-8') + "\n")
            f.write("\n----\n\n")