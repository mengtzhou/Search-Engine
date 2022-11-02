#!/usr/bin/env python3
"""Map 1."""

# input
## doc_id doc_title doc_body

# output
## word  doc_id  tf

import re
import csv
import sys

csv.field_size_limit(sys.maxsize)

stop_words = set([line.split()[0] for line in open('stopwords.txt')])

lines = csv.reader(sys.stdin, delimiter=",")
for line in lines:
    doc_id = line[0]
    text = line[1] + ' ' + line[2]
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    text = text.casefold()
    words = text.split()
    words_set = set(words) - stop_words
    for word in words_set:
        print(f"{word}\t{doc_id}\t{words.count(word)}")

