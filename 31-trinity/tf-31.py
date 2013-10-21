#!/usr/bin/env python

import sys, re, operator, collections

#
# Model
#
class WordFrequencies:
    """ Models the data. In this case, we're only interested 
    in words and their frequencies as an end result """
    _freqs = {}
    def __init__(self, path_to_file):
        stopwords = set(open('../stop_words.txt').read().split(','))
        words = re.findall('[a-z]{2,}', open(path_to_file).read().lower())
        self._freqs = collections.Counter(w for w in words if w not in stopwords)

    def word_freqs_sorted(self):
        """
        Returns the list of the most frequently-occuring words, sorted
        """
        return sorted(self._freqs.iteritems(), key=operator.itemgetter(1), reverse=True)

#
# View
#
class WordFrequenciesView:
    _freqs = None

    def __init__(self, freqs):
        self._freqs = freqs

    def render(self):
        for (w, c) in self._freqs.word_freqs_sorted()[:25]:
            print w, '-', c

#
# Controller
#
wfmodel = WordFrequencies(sys.argv[1])
wfview = WordFrequenciesView(wfmodel)
wfview.render()
