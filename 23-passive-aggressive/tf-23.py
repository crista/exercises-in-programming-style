#!/usr/bin/env python
import sys, re, operator, string

#
# The functions
#
def extract_words(path_to_file):
    assert(type(path_to_file) is str), "I need a string! I quit!" 
    assert(path_to_file), "I need a non-empty string! I quit!" 

    with open(path_to_file) as f:
        data = f.read()
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', data).lower().split()
    return word_list

def remove_stop_words(word_list):
    assert(type(word_list) is list), "I need a list! I quit!"

    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    # add single-letter words
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    assert(type(word_list) is list), "I need a list! I quit!"
    assert(word_list <> []), "I need a non-empty list! I quit!"

    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freqs):
    assert(type(word_freqs) is dict), "I need a dictionary! I quit!"
    assert(word_freqs <> {}), "I need a non-empty dictionary! I quit!"

    return sorted(word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)

#
# The main function
#
try:
    assert(len(sys.argv) > 1), "You idiot! I need an input file! I quit!"
    word_freqs = sort(frequencies(remove_stop_words(extract_words(sys.argv[1]))))

    assert(len(word_freqs) > 25), "OMG! Less than 25 words! I QUIT!"
    for tf in word_freqs[0:25]:
        print tf[0], ' - ', tf[1]
except Exception as e:
        print "Something wrong: {0}".format(e)


