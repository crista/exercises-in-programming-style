#!/usr/bin/env python
import sys, operator, string, os, threading, re
from util import getch, cls, get_input
from time import sleep

lock = threading.Lock()

#
# The active view
#
class FreqObserver(threading.Thread):
    def __init__(self, freqs):
        threading.Thread.__init__(self)
        self.daemon,self._end = True, False
        # freqs is the part of the model to be observed
        self._freqs = freqs
        self._freqs_0 = sorted(self._freqs.iteritems(), key=operator.itemgetter(1), reverse=True)[:25]
        self.start()

    def run(self):
        while not self._end:
            self._update_view()
            sleep(0.1)
        self._update_view()

    def stop(self):
        self._end = True

    def _update_view(self):
        lock.acquire()
        freqs_1 = sorted(self._freqs.iteritems(), key=operator.itemgetter(1), reverse=True)[:25]
        lock.release()
        if (freqs_1 != self._freqs_0):
            self._update_display(freqs_1)
            self._freqs_0 = freqs_1

    def _update_display(self, tuples):
        def refresh_screen(data):
            # clear screen
            cls()
            print data
            sys.stdout.flush()

        data_str = ""
        for (w, c) in tuples:
            data_str += str(w) + ' - ' + str(c) + '\n'
        refresh_screen(data_str)

#
# The model
#
class WordsCounter:
    freqs = {}
    def count(self):
        def non_stop_words():
            stopwords = set(open('../stop_words.txt').read().split(',')  + list(string.ascii_lowercase))
            for line in f:
                yield [w for w in re.findall('[a-z]{2,}', line.lower()) if w not in stopwords]

        words = non_stop_words().next()
        lock.acquire()
        for w in words:
            self.freqs[w] = 1 if w not in self.freqs else self.freqs[w]+1
        lock.release()

#
# The controller
#
print "Press space bar to fetch words from the file one by one"
print "Press ESC to switch to automatic mode"
model = WordsCounter()
view = FreqObserver(model.freqs)
with open(sys.argv[1]) as f:
    while get_input():
        try:
            model.count()
        except StopIteration:
            # Let's wait for the view thread to die gracefully
            view.stop()
            sleep(1)
            break


