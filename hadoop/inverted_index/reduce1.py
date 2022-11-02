#!/usr/bin/env python3
"""Reduce 1."""

# input
## word  doc_id  tf

# output
## doc_id  word  idf tf  (tf*idf)^2

import math
import sys
import itertools

def reduce_one_group(key, group):
    """Reduce one group."""
    # number of documents
    N = int(open("total_document_count.txt").readline())
    # number of documents containing key
    group = list(group)
    n = len(group)
    idf = math.log10(N/n)
    for line in group:
        word, doc_id, tf = line.split("\t")
        tf = int(tf)
        print(f"{doc_id}\t{word}\t{idf}\t{tf}\t{tf**2*idf**2}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]

def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)

if __name__ == "__main__":
    main()

