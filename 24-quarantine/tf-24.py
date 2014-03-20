#!/usr/bin/env python
import sys, re, operator, string

#
# The Quarantine class for this example
#
class TFQuarantine:
    def __init__(self, func):
        self._funcs = [func]

    def bind(self, func):
        self._funcs.append(func)
        return self

    def execute(self):
        def guard_callable(v):
            return v() if hasattr(v, '__call__') else v

        value = lambda : None
        for func in self._funcs:
            value = func(guard_callable(value))
        print guard_callable(value)

#
# The functions
#
def get_input(arg):
    def _f():
        return sys.argv[1]
    return _f

def extract_words(path_to_file):
    def _f():
        with open(path_to_file) as f:
            data = f.read()
        pattern = re.compile('[\W_]+')
        word_list = pattern.sub(' ', data).lower().split()
        return word_list
    return _f

def remove_stop_words(word_list):
    def _f():
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
        # add single-letter words
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]
    return _f

def frequencies(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freq):
    return sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)

def top25_freqs(word_freqs):
    top25 = ""
    for tf in word_freqs[0:25]:
        top25 += str(tf[0]) + ' - ' + str(tf[1]) + '\n'
    return top25

#
# The main function
#
TFQuarantine(get_input)\
.bind(extract_words)\
.bind(remove_stop_words)\
.bind(frequencies)\
.bind(sort)\
.bind(top25_freqs)\
.execute()

