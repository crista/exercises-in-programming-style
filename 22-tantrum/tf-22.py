#!/usr/bin/env python

import sys, re, operator, string, traceback

#
# The functions
#
def extract_words(path_to_file):
    assert(type(path_to_file) is str), "I need a string!" 
    assert(path_to_file), "I need a non-empty string!" 

    try:
        with open(path_to_file) as f:
            str_data = f.read()
    except IOError as e:
        print "I/O error({0}) when opening {1}: {2}! I quit!".format(e.errno, path_to_file, e.strerror)
        raise e
    
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    return word_list

def remove_stop_words(word_list):
    assert(type(word_list) is list), "I need a list!"

    try:
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
    except IOError as e:
        print "I/O error({0}) when opening ../stops_words.txt: {1}! I quit!".format(e.errno, e.strerror)
        raise e

    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    assert(type(word_list) is list), "I need a list!"
    assert(word_list <> []), "I need a non-empty list!"

    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freq):
    assert(type(word_freq) is dict), "I need a dictionary!"
    assert(word_freq <> {}), "I need a non-empty dictionary!"

    try:
        return sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)
    except Exception as e:
        print "Sorted threw {0}: {1}".format(e)
        raise e

#
# The main function
#
try:
    assert(len(sys.argv) > 1), "You idiot! I need an input file!"
    word_freqs = sort(frequencies(remove_stop_words(extract_words(sys.argv[1]))))

    assert(type(word_freqs) is list), "OMG! This is not a list!"
    assert(len(word_freqs) > 25), "SRSLY? Less than 25 words!"
    for (w, c) in word_freqs[0:25]:
        print w, ' - ', c
except Exception as e:
    print "Something wrong: {0}".format(e)
    traceback.print_exc()
    
