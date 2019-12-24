#!/usr/bin/env python
import sys, re, operator, string
from functools import reduce
#
# Functions for map reduce
#
def partition(data_str, nlines):
    """
    Partitions the input data_str (a big string)
    into chunks of nlines.
    """
    lines = data_str.split('\n')
    for i in range(0, len(lines), nlines):
        yield '\n'.join(lines[i:i+nlines])

def split_words(data_str):
    """
    Takes a string,  returns a list of pairs (word, 1),
    one for each word in the input, so
    [(w1, 1), (w2, 1), ..., (wn, 1)]
    """
    def _scan(str_data):
        pattern = re.compile('[\W_]+')
        return pattern.sub(' ', str_data).lower().split()

    def _remove_stop_words(word_list):
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]

    # The actual work of splitting the input into words
    result = []
    words = _remove_stop_words(_scan(data_str))
    for w in words:
        result.append((w, 1))
    return result

def count_words(pairs_list_1, pairs_list_2):
    """
    Takes two lists of pairs of the form
    [(w1, 1), ...]
    and returns a list of pairs [(w1, frequency), ...],
    where frequency is the sum of all the reported occurrences
    """
    mapping = {}
    for pl in [pairs_list_1, pairs_list_2]:
        for p in pl:
            if p[0] in mapping:
                mapping[p[0]] += p[1]
            else:
                mapping[p[0]] = p[1]
    return mapping.items()

#
# Auxiliary functions
#
def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data

def sort(word_freq):
    return sorted(word_freq, key=operator.itemgetter(1), reverse=True)

#
# The main function
#
splits = map(split_words, partition(read_file(sys.argv[1]), 200))
word_freqs = sort(reduce(count_words, splits))

for (w, c) in word_freqs[0:25]:
    print(w, '-', c)
