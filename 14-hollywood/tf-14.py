#!/usr/bin/env python
import sys, re, operator, string

#
# The "I'll call you back" Word Frequency Framework
#
class WordFrequencyFramework:
    _load_event_handlers = []
    _dowork_event_handlers = []
    _end_event_handlers = []

    def register_for_load_event(self, handler):
        self._load_event_handlers.append(handler)

    def register_for_dowork_event(self, handler):
        self._dowork_event_handlers.append(handler)

    def register_for_end_event(self, handler):
        self._end_event_handlers.append(handler)
    
    def run(self, path_to_file):
        for h in self._load_event_handlers:
            h(path_to_file)
        for h in self._dowork_event_handlers:
            h()
        for h in self._end_event_handlers:
            h()

#
# The entities of the application
#
class DataStorage:
    """ Models the contents of the file """
    _data = ''
    _stop_word_filter = None
    _word_event_handlers = []

    def __init__(self, wfapp, stop_word_filter):
        self._stop_word_filter = stop_word_filter
        wfapp.register_for_load_event(self.__load)
        wfapp.register_for_dowork_event(self.__produce_words)

    def __load(self, path_to_file):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def __produce_words(self):
        """ Iterates through the list words in storage 
            calling back handlers for words """
        data_str = ''.join(self._data)
        for w in data_str.split():
            if not self._stop_word_filter.is_stop_word(w):
                for h in self._word_event_handlers:
                    h(w)

    def register_for_word_event(self, handler):
        self._word_event_handlers.append(handler)

class StopWordFilter:
    """ Models the stop word filter """
    _stop_words = []
    def __init__(self, wfapp):
        wfapp.register_for_load_event(self.__load)

    def __load(self, ignore):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        # add single-letter words
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return word in self._stop_words

class WordFrequencyCounter:
    """ Keeps the word frequency data """
    _word_freqs = {}
    def __init__(self, wfapp, data_storage):
        data_storage.register_for_word_event(self.__increment_count)
        wfapp.register_for_end_event(self.__print_freqs)

    def __increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def __print_freqs(self):
        word_freqs = sorted(self._word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)
        for (w, c) in word_freqs[0:25]:
            print w, ' - ', c

#
# The main function
#
wfapp = WordFrequencyFramework()
stop_word_filter = StopWordFilter(wfapp)
data_storage = DataStorage(wfapp, stop_word_filter)
word_freq_counter = WordFrequencyCounter(wfapp, data_storage)
wfapp.run(sys.argv[1])

