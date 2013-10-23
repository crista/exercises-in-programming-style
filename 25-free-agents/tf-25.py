#!/usr/bin/env python

import sys, re, operator, string
from threading import Thread
from Queue import Queue

class ActiveWFObject(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = str(type(self))
        self.queue = Queue()
        self._stop = False
        self.start()

    def run(self):
        while not self._stop:
            message = self.queue.get()
            self.dispatch(message)
            if message[0] == 'die':
                self._stop = True

class DataStorageManager(ActiveWFObject):
    _queue = Queue()
    """ Models the contents of the file """
    _data = ''

    def dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'send_word_freqs':
            self._process_words(message[1:])
        else:
            # forward
            self._stop_word_manager.queue.put(message)
 
    def _init(self, message):
        path_to_file = message[0]
        self._stop_word_manager = message[1]
        f = open(path_to_file)
        self._data = f.read()
        f.close()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def _process_words(self, message):
        recipient = message[0]
        data_str = ''.join(self._data)
        words = data_str.split()
        for w in words:
            self._stop_word_manager.queue.put(['filter', w])
        self._stop_word_manager.queue.put(['top25', recipient])


class StopWordManager(ActiveWFObject):
    """ Models the stop word filter """
    _stop_words = []

    def dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'filter':
            return self._filter(message[1:])
        else:
            # forward
            self._word_freqs_manager.queue.put(message)
 
    def _init(self, message):
        f = open('../stop_words.txt')
        self._stop_words = f.read().split(',')
        f.close()
        self._stop_words.extend(list(string.ascii_lowercase))
        self._word_freqs_manager = message[0]

    def _filter(self, message):
        word = message[0]
        if word not in self._stop_words:
            self._word_freqs_manager.queue.put(['word', word])

class WordFrequencyManager(ActiveWFObject):
    """ Keeps the word frequency data """
    _word_freqs = {}

    def dispatch(self, message):
        if message[0] == 'word':
            self._increment_count(message[1:])
        elif message[0] == 'top25':
            self._top25(message[1:])
 
    def _increment_count(self, message):
        word = message[0]
        if word in self._word_freqs:
            self._word_freqs[word] += 1 
        else: 
            self._word_freqs[word] = 1

    def _top25(self, message):
        recipient = message[0]
        freqs_sorted = sorted(self._word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)
        recipient.queue.put(['top25', freqs_sorted])

class WordFrequencyController(ActiveWFObject):

    def dispatch(self, message):
        if message[0] == 'run':
            self._run(message[1:])
        elif message[0] == 'top25':
            self._display(message[1:])
        else:
            raise Exception("Message not understood " + message[0])
 
    def _run(self, message):
        self._storage_manager = message[0]
        self._storage_manager.queue.put(['send_word_freqs', self])

    def _display(self, message):
        word_freqs = message[0]
        for (w, f) in word_freqs[0:25]:
            print w, ' - ', f
        self._storage_manager.queue.put(['die'])
        self._stop = True


#
# The main function
#
word_freq_manager = WordFrequencyManager()

stop_word_manager = StopWordManager()
stop_word_manager.queue.put(['init', word_freq_manager])

storage_manager = DataStorageManager()
storage_manager.queue.put(['init', sys.argv[1], stop_word_manager])

wfcontroller = WordFrequencyController()
wfcontroller.dispatch(['run', storage_manager])

# Wait for the active objects to finish
[t.join() for t in [word_freq_manager, stop_word_manager, storage_manager, wfcontroller]]
