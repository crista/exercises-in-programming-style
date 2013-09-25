#!/usr/bin/env python

import sys, re, operator, string

#
# Two down-to-earth things that cannot be reflected on
# without serious performance penalties
#
stops = set(open("../stop_words.txt").read().split(",") + list(string.ascii_lowercase))

def frequencies_imp(word_list):
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
    return word_freqs

#
# Let's write our function bodies as strings.
# Because we're looking at them from "above"
#
extract_words_func_body = "lambda name : [x.lower() for x in re.split('[^a-zA-Z]+', open(name).read()) if len(x) > 0 and x.lower() not in stops]"

frequencies_func_body = "lambda word_list : frequencies_imp(word_list)"

sort_func_body = "lambda word_freq: sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)"

#
# So far, this program isn't much about term-frequency. It's about
# a bunch of strings that look like function bodies.
# Let's add our functions to the "base" program, dynamically.
# We're re-writing this program by adding more functions to it
# from "above".
#
exec('extract_words = ' + extract_words_func_body)
exec('frequencies = ' + frequencies_func_body)
exec('sort = ' + sort_func_body)

#
# The main function. This would work just fine:
#  word_freqs = sort(frequencies(extract_words(sys.argv[1])))
# But because we're being introspective, we'll call the 
# functions also from "above"
#
word_freqs = locals()['sort'](locals()['frequencies'](locals()['extract_words'](sys.argv[1])))

for tf in word_freqs[0:25]:
    print tf[0], ' - ', tf[1]

