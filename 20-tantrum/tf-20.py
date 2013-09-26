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
    assert(type(path_to_file) is str), "I need a string! I quit!" 
    assert(path_to_file), "I need a non-empty string! I quit!" 

    try:
        with open(path_to_file) as f:
            str_data = f.read()
    except IOError as e:
        print "I/O error({0}) when opening {1}: {2}! I quit!".format(e.errno, path_to_file, e.strerror)
        raise e
    
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()

    try:
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
    except IOError as e:
        print "I/O error({0}) when opening ../stops_words.txt: {1}! I quit!".format(e.errno, e.strerror)
        raise e

    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence
    """
    assert(type(word_list) is list), "I need a list! I quit!"
    assert(word_list <> []), "I need a non-empty list! I quit!"

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
    assert(type(word_freq) is dict), "I need a dictionary! I quit!"
    assert(word_freq <> {}), "I need a non-empty dictionary! I quit!"

    return sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)

#
# The main function
#
assert(len(sys.argv) > 1), "You idiot! I need an input file! I quit!"
word_freqs = sort(frequencies(extract_words(sys.argv[1])))

assert(len(word_freqs) > 25), "OMG! Less than 25 words! I QUIT!"
for tf in word_freqs[0:25]:
    print tf[0], ' - ', tf[1]

