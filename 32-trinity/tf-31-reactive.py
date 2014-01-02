#!/usr/bin/env python
import sys, re, operator, collections

class WordFrequenciesModel:
    """ Models the data. In this case, we're only interested 
    in words and their frequencies as an end result """
    freqs = {}
    def __init__(self):
        self._observers = []

    def register(self, obs):
        self._observers.append(obs)

    def update(self, path_to_file):
        try:
            stopwords = set(open('../stop_words.txt').read().split(','))
            words = re.findall('[a-z]{2,}', open(path_to_file).read().lower())
            self.freqs = collections.Counter(w for w in words if w not in stopwords)
            for obs in self._observers:
                obs.render()
        except IOError:
            print "File not found"
            self.freqs = {}

class WordFrequenciesView:
    def __init__(self, model):
        self._model = model
        model.register(self)

    def render(self):
        sorted_freqs = sorted(self._model.freqs.iteritems(), key=operator.itemgetter(1), reverse=True)
        for (w, c) in sorted_freqs[:25]:
            print w, '-', c

class WordFrequencyController:
    def __init__(self, model, view):
        self._model, self._view = model, view

    def run(self):
        self._model.update(sys.argv[1])
        while True:
            print "Next file: " 
            sys.stdout.flush() 
            filename = sys.stdin.readline().strip()
            self._model.update(filename)

m = WordFrequenciesModel()
v = WordFrequenciesView(m)
c = WordFrequencyController(m, v)
c.run()
