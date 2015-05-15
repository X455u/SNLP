#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ConfigParser
import unicodecsv
import json
import sys
import re

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

# Forming the filename for the cluster files
clusterfile = config.get('clusters', 'clustercounts')

m = re.match( r'(.*)(\..*)', clusterfile)
c_beg =  m.group(1)
c_end = m.group(2)

dataidx = config.get('clusters', 'dataidx')
clusterfile = c_beg + dataidx + c_end

# Reading the SOM cluster data
with open(clusterfile) as f:
    csv_f = unicodecsv.reader(f, encoding='utf-8')

    # Read the file and tokenize
    for idx, row in enumerate(csv_f):
        classes = row

# Transforming the data into numbers
classes = [int(i) for i in classes]

data_file = config.get('clusters', 'descriptions')
text_idx = json.loads(config.get('data', 'textdataidx'))[0]


# Initializing the clusters list
clusters = []
for i in range(max(classes)):
    clusters.append([])

# Reading the text descriptions
with open(data_file) as f:
    csv_f = unicodecsv.reader(f, encoding='utf-8')

    for idx, row in enumerate(csv_f):

        if idx == 0:
            continue

        c = classes[idx-1]
        clusters[c-1].append(str(idx) + ": " + row[0])


### Reading the tdm matrix ###

tdmfile = config.get('data', 'termdocumentmatrix')

# Forming the right filename
m = re.match( r'(.*)(\..*)', tdmfile)
tdmfile = m.group(1) + dataidx + m.group(2)

# Terms of the tdm matrix
termheader = []

# Initializing the term cluster list
termclusters = []

with open(tdmfile) as f:
    csv_f = unicodecsv.reader(f, encoding='utf-8')

    for idx, row in enumerate(csv_f):

        if idx == 0:
            termheader = row

            # initialize term cluster list
            for i in range(max(classes)):
                termclusters.append([0]*len(row))

            continue

        # summing the row to the counts of the righ cluster
        cidx = classes[idx-1] -1
        termclusters[cidx] = [termclusters[cidx][i] + int(row[i]) for i in range(len(row))]


# Writing the large clusters with their texts and some statistics
with open(config.get('clusters', 'clustertexts'),"w") as f:

    for i in range(len(clusters)):
        c = clusters[i]

        # Ignore filler clusters
        if len(c) > 1:

            # Writing cluster info
            f.write("Cluster: " + str(i+1) + "  Texts: " + str(len(c)) + "\n")
            f.write("Avg len: " +  str(avgtextlen(c)) + "  Min len: " + str(mintextlen(c)) + "  Max len: " + str(maxtextlen(c)) + "\n" )

            for j in range(len(termclusters[i])):

                # Do not print terms with low counts
                if termclusters[i][j] > 2:
                    f.write(str(termclusters[i][j]) + " : " + termheader[j].encode('utf-8')+ "\n")

            # Writing the text descriptions
            for s in c:
                f.write(s.encode('utf-8') + "\n")
            f.write("\n----\n\n")