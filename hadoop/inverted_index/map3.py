#!/usr/bin/env python3
"""Map 3."""

# input
## word  idf  doc_id  tf  sum(tf*idf)^2

# output
## doc_id%3 word  idf  doc_id  tf  sum(tf*idf)^2

import sys

for line in sys.stdin:
    doc_id = int(line.split("\t")[2])
    print(f"{str(doc_id%3)}\t{line}", end="")
