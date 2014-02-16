#!/usr/bin/env python
import sys, re, operator, string

#
# The PassiveAggressive class for this example
#
class TFPassiveAggressive:
    def __init__(self):
        self._e = None
        self._offending_func = None
        self._value = None

    def bind(self, func):
        if self._e == None:
            try:
                self._value = func(self._value)
            except Exception as e:
                self._e = e
                self._offending_func = func
        return self

    def printme(self):
        if self._e == None:
            print self._value
        else:
            print self._e, " in ", self._offending_func.__name__

#
# The functions
#
def get_input(ignore):
    assert(len(sys.argv) > 1), "You idiot! I need an input file! I quit!"
    return sys.argv[1]

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

def top25_freqs(word_freqs):
    assert(type(word_freqs) is list), "I need a list! I quit!"
    assert(word_freqs <> {}), "I need a non-empty dictionary! I quit!"

    top25 = ""
    for tf in word_freqs[0:25]:
        top25 += str(tf[0]) + ' - ' + str(tf[1]) + '\n'
    return top25

#
# The main function
#
TFPassiveAggressive().bind(get_input).bind(extract_words).bind(remove_stop_words).bind(frequencies).bind(sort).bind(top25_freqs).printme()