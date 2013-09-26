#!/usr/bin/env python

import sys, re, operator, string, inspect

#
# The functions
#
def extract_words(path_to_file):
    """
    Takes a path to a file and returns the non-stop
    words, after properly removing nonalphanumeric chars
    and normalizing for lower case
    """
    if type(path_to_file) is not str or not path_to_file:
        return []

    try:
        with open(path_to_file) as f:
            str_data = f.read()
    except IOError as e:
        print "I/O error({0}) when opening {1}: {2}".format(e.errno, path_to_file, e.strerror)
        return []
    
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()

    try:
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
    except IOError as e:
        print "I/O error({0}) when opening ../stops_words.txt: {1}".format(e.errno, e.strerror)
        return []

    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence
    """
    if type(word_list) is not list or word_list == []:
        return {}

    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freq):
    """
    Takes a dictionary of words and their frequencies
    and returns a list of pairs where the entries are
    sorted by frequency 
    """
    if type(word_freq) is not dict or word_freq == {}:
        return []

    return sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)

#
# The main function
#
word_freqs = sort(frequencies(extract_words(sys.argv[1])))

for tf in word_freqs[0:25]:
    print tf[0], ' - ', tf[1]

