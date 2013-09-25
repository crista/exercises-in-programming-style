#!/usr/bin/env python

import sys, re, operator, string

#
# The functions
#
def read_file(path_to_file, func):
    """
    Takes a path to a file and returns the entire
    contents of the file as a string
    """
    f = open(path_to_file)
    data = f.read()
    f.close()
    return func(data, normalize)

def filter_chars(str_data, func):
    """
    Takes a string and returns a copy with all nonalphanumeric chars
    replaced by white space
    """
    pattern = re.compile('[\W_]+')
    return func(pattern.sub(' ', str_data), scan)

def normalize(str_data, func):
    """
    Takes a string and returns a copy with all characters in lower case
    """
    return func(str_data.lower(), remove_stop_words)

def scan(str_data, func):
    """
    Takes a string and scans for words, returning
    a list of words.
    """
    return func(str_data.split(), frequencies)

def remove_stop_words(word_list, func):
    """ Takes a list of words and returns a copy with all stop words removed """
    f = open('../stop_words.txt')
    stop_words = f.read().split(',')
    f.close()
    # add single-letter words
    stop_words.extend(list(string.ascii_lowercase))
    return func([w for w in word_list if not w in stop_words], sort)

def frequencies(word_list, func):
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence
    """
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return func(word_freqs, no_op)

def sort(word_freq, func):
    """
    Takes a dictionary of words and their frequencies
    and returns a list of pairs where the entries are
    sorted by frequency 
    """
    return func(sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True), None)

def no_op(a, func):
    return a

#
# The main function
#
word_freqs = read_file(sys.argv[1], filter_chars)

for tf in word_freqs[0:25]:
    print tf[0], ' - ', tf[1]

