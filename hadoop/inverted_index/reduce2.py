#!/usr/bin/env python3
"""Reduce 2."""

# input
## doc_id  word  idf tf  (tf*idf)^2

# output
## word  idf  doc_id  tf  sum(tf*idf)^2

import sys
import itertools
import math

def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    norm_factor = 0
    for line in group:
        _, _, _, _, tmp = line.split("\t")
        norm_factor += float(tmp)
    # norm_factor = math.sqrt(norm_factor)
    for line in group:
        doc_id, word, idf, tf, _ = line.split("\t")
        print(f"{word}\t{idf}\t{doc_id}\t{tf}\t{norm_factor}")



def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]

def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)

if __name__ == "__main__":
    main()
