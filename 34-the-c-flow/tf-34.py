#!/usr/bin/env python

import sys, re, operator, string, inspect

# Reusing the defensive style program to illustrate this

#
# The functions
#
def extract_words(path_to_file):
    """
    Takes a path to a file and returns the non-stop
    words, after properly removing nonalphanumeric chars
    and normalizing for lower case
    """
    fail = False
    word_list = []
    if type(path_to_file) is str and path_to_file:
        try:
            with open(path_to_file) as f:
                str_data = f.read()
        except IOError as e:
            print "I/O error({0}) when opening {1}: {2}".format(e.errno, path_to_file, e.strerror)
            fail = True
    
        if not fail:
            pattern = re.compile('[\W_]+')
            word_list = pattern.sub(' ', str_data).lower().split()

            try:
                with open('../stop_words.txt') as f:
                    stop_words = f.read().split(',')
            except IOError as e:
                print "I/O error({0}) when opening ../stops_words.txt: {1}".format(e.errno, e.strerror)
                fail = True

            if not fail:
                stop_words.extend(list(string.ascii_lowercase))

    return [w for w in word_list if not w in stop_words] if not fail else []

def frequencies(word_list):
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence
    """
    if type(word_list) is list and word_list <> []:
        word_freqs = {}
        for w in word_list:
            if w in word_freqs:
                word_freqs[w] += 1
            else:
                word_freqs[w] = 1
        return word_freqs
    else:
        return {}

def sort(word_freq):
    """
    Takes a dictionary of words and their frequencies
    and returns a list of pairs where the entries are
    sorted by frequency 
    """
    if type(word_freq) is dict and word_freq <> {}:
        return sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)
    else:
        return []

#
# The main function
#
filename = sys.argv[1] if len(sys.argv) > 1 else "../input.txt"
word_freqs = sort(frequencies(extract_words(filename)))

for tf in word_freqs[0:25]:
    print tf[0], ' - ', tf[1]

