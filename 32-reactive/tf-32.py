#!/usr/bin/env python

import sys, operator, string, os, threading
from util import getch, cls
from time import sleep

#
# The reactive infrastructure
#
class FreqObserver(threading.Thread):
    def __init__(self, freqs):
        threading.Thread.__init__(self)
        self.daemon = True
        # freqs is the data to be observed and reacted to
        self._freqs = freqs
        self._freqs_0 = sorted(self._freqs.iteritems(), key=operator.itemgetter(1), reverse=True)
        self.start()

    def run(self):
        while True:
            freqs_1 = sorted(self._freqs.iteritems(), key=operator.itemgetter(1), reverse=True)
            if (freqs_1[0:25] != self._freqs_0[0:25]):
                self._update_display(freqs_1[0:25])
            self._freqs_0 = freqs_1
            sleep(0.01)

    def _update_display(self, tuples):
        def refresh_screen(data):
            # clear screen
            cls()
            print data
            sys.stdout.flush()

        data_str = ""
        for tf in tuples:
            data_str += str(tf[0]) + ' - ' + str(tf[1]) + '\n'
        refresh_screen(data_str)

#
# The active part, dataflow-like
#
interactive = True
def get_input():
    global interactive
    if not interactive:
        return True

    while True: 
        key = ord(getch())
        if key == 32: # space bar
            return True
        elif key == 27: # ESC
            interactive = False
            return True
        else: pass

f = open(sys.argv[1])

def characters(filename):
    c = f.read(1)
    if c != "":
        yield c
    else:
        raise StopIteration()

def all_words(filename):
    found_word = False
    start_char = True
    while not found_word:
        try:
            c = characters(filename).next()
        except StopIteration:
            raise StopIteration()

        if start_char == True:
            word = ""
            if c.isalnum():
                # We found the start of a word
                word = c.lower()
                start_char = False
        else:
            if c.isalnum():
                word += c.lower()
            else:
                # We found the end of a word, emit it
                start_char = True
                found_word = True
                yield word

def non_stop_words(filename):
    stopwords = set(open('../stop_words.txt').read().split(',')  + list(string.ascii_lowercase))
    while True:
        w = all_words(filename).next()
        if not w in stopwords:
            yield w

def count_and_sort(filename):
    freqs = {}
    # The declaration for reactive observation of freqs
    FreqObserver(freqs)
    while get_input():
        try:
            w = non_stop_words(filename).next()
            freqs[w] = 1 if w not in freqs else freqs[w]+1
        except StopIteration:
            break

#
# The main function
#
print "Press space bar to fetch words from the file one by one"
print "Press ESC to switch to automatic mode"
count_and_sort(sys.argv[1])


