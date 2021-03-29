#!/usr/bin/env python
import sys
import operator
import string


def characters(filename):
    for line in open(filename):
        for c in line:
            yield c


def all_words(filename):
    start_char = True
    for c in characters(filename):
        if start_char == True:
            word = ""
            if c.isalnum():
                # We found the start of a word
                word = c.lower()
                start_char = False
            else:
                pass
        else:
            if c.isalnum():
                word += c.lower()
            else:
                # We found end of word, emit it
                start_char = True
                yield word


def non_stop_words(filename):
    stopwords = set(open(
        '../stop_words.txt').read().strip('\n').split(',') + list(string.ascii_lowercase))
    for w in all_words(filename):
        if not w in stopwords:
            yield w


def count_and_sort(filename):
    freqs, i = {}, 1
    for w in non_stop_words(filename):
        freqs[w] = 1 if w not in freqs else freqs[w]+1
        if i % 5000 == 0:
            yield sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
        i = i+1
    yield sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)


#
# The main function
#
for word_freqs in count_and_sort(sys.argv[1]):
    print("-----------------------------")
    for (w, c) in word_freqs[0:25]:
        print(w, '-', c)
