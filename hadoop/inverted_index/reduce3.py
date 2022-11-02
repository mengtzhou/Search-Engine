#!/usr/bin/env python3
"""Reduce 3."""

# input
## doc_id%3 word  idf  doc_id  tf  sum(tf*idf)^2

# output
## word idf doc_id1 tf1 sum1(tf*idf)^2 doc_id2 tf2 sum2(tf*idf)^2 ...

import sys
import itertools

def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    group.sort(key=sortfunc)
    d = dict()
    words = []
    for line in group:
        _, word, idf, doc_id, tf, norm_factor = line.split()
        if word not in d:
            d[word] = word + ' ' + idf + ' ' + doc_id + ' ' + tf + ' ' + norm_factor
            words.append(word)
        else:
            d[word] += ' ' + doc_id + ' ' + tf + ' ' + norm_factor
    words.sort()
    for w in words:
        print(d[w], end="\n")

def sortfunc(line):
    return line.split("\t")[3]

def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]

def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)

if __name__ == "__main__":
    main()

