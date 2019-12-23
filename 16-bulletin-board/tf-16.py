#!/usr/bin/env python
import sys, re, operator, string

#
# The event management substrate
#
class EventManager:
    def __init__(self):
        self._subscriptions = {}

    def subscribe(self, event_type, handler):
        if event_type in self._subscriptions:
            self._subscriptions[event_type].append(handler)
        else:
            self._subscriptions[event_type] = [handler]

    def publish(self, event):
        event_type = event[0]
        if event_type in self._subscriptions:
            for h in self._subscriptions[event_type]:
                h(event)

#
# The application entities
#
class DataStorage:
    """ Models the contents of the file """
    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.subscribe('load', self.load)
        self._event_manager.subscribe('start', self.produce_words)

    def load(self, event):
        path_to_file = event[1]
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def produce_words(self, event):
        data_str = ''.join(self._data)
        for w in data_str.split():
            self._event_manager.publish(('word', w))
        self._event_manager.publish(('eof', None))

class StopWordFilter:
    """ Models the stop word filter """
    def __init__(self, event_manager):
        self._stop_words = []
        self._event_manager = event_manager
        self._event_manager.subscribe('load', self.load)
        self._event_manager.subscribe('word', self.is_stop_word)

    def load(self, event):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, event):
        word = event[1]
        if word not in self._stop_words:
            self._event_manager.publish(('valid_word', word))

class WordFrequencyCounter:
    """ Keeps the word frequency data """
    def __init__(self, event_manager):
        self._word_freqs = {}
        self._event_manager = event_manager
        self._event_manager.subscribe('valid_word', self.increment_count)
        self._event_manager.subscribe('print', self.print_freqs)

    def increment_count(self, event):
        word = event[1]
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def print_freqs(self, event):
        word_freqs = sorted(self._word_freqs.items(), key=operator.itemgetter(1), reverse=True)
        for (w, c) in word_freqs[0:25]:
            print(w, '-', c)

class WordFrequencyApplication:
    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.subscribe('run', self.run)
        self._event_manager.subscribe('eof', self.stop)

    def run(self, event):
        path_to_file = event[1]
        self._event_manager.publish(('load', path_to_file))
        self._event_manager.publish(('start', None))

    def stop(self, event):
        self._event_manager.publish(('print', None))

#
# The main function
#
em = EventManager()
DataStorage(em), StopWordFilter(em), WordFrequencyCounter(em)
WordFrequencyApplication(em)
em.publish(('run', sys.argv[1]))
