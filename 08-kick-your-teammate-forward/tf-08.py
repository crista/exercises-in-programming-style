#!/usr/bin/env python
import sys, re, operator, string

#
# The functions
#
def read_file(path_to_file, func):
    with  open(path_to_file) as f:
        data = f.read()
    return func(data, normalize)

def filter_chars(str_data, func):
    pattern = re.compile('[\W_]+')
    return func(pattern.sub(' ', str_data), scan)

def normalize(str_data, func):
    return func(str_data.lower(), remove_stop_words)

def scan(str_data, func):
    return func(str_data.split(), frequencies)

def remove_stop_words(word_list, func):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    # add single-letter words
    stop_words.extend(list(string.ascii_lowercase))
    return func([w for w in word_list if not w in stop_words], sort)

def frequencies(word_list, func):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return func(word_freqs, no_op)

def sort(word_freq, func):
    return func(sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True), None)

def no_op(a, func):
    return a

#
# The main function
#
word_freqs = read_file(sys.argv[1], filter_chars)

for (w, c) in word_freqs[0:25]:
    print w, ' - ', c

