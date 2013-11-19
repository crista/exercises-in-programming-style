#!/usr/bin/env python

import abc, sys, re, operator, string

#
# The abstract data types
#
class IDataStorage (object):
    """ Models the contents of the file """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def words(self):
        """ Returns the words in storage """
        raise NotImplementedError("Abstract Data Type")

class IStopWordFilter (object):
    """ Models the stop word filter """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_stop_word(self, word):
        """ Checks whether the given word is a stop word """
        raise NotImplementedError("Abstract Data Type")

class IWordFrequencyCounter(object):
    """ Keeps the word frequency data """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def increment_count(self, word):
        """ Increments the count for the given word """
        raise NotImplementedError("Abstract Data Type")

    @abc.abstractmethod
    def sorted(self):
        """ Returns the words and their frequencies, sorted by frequency""" 
        raise NotImplementedError("Abstract Data Type")

#
# The concrete type implementations
#
class DataStorage:
    """ Implements the contents of the file """
    _data = ''
    def __init__(self, path_to_file):
        f = open(path_to_file)
        self._data = f.read()
        f.close()
        self.__filter_chars_normalize()
        self.__scan()

    def __filter_chars_normalize(self):
        """
        Takes a string and returns a copy with all nonalphanumeric chars
        replaced by white space
        """
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def __scan(self):
        self._data = ''.join(self._data).split()

    def words(self):
        """
        Returns the list words in storage
        """
        return self._data

class StopWordFilter:
    """ Implements the stop word filter """
    _stop_words = []
    def __init__(self):
        f = open('../stop_words.txt')
        self._stop_words = f.read().split(',')
        f.close()
        # add single-letter words
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return word in self._stop_words

class WordFrequencyCounter:
    """ Implements the word frequency data """
    _word_freqs = {}

    def increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def sorted(self):
        return sorted(self._word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)


#
# The wiring between ADTs and concrete implementations
#
IDataStorage.register(DataStorage)
IStopWordFilter.register(StopWordFilter)
IWordFrequencyCounter.register(WordFrequencyCounter)

class WordFrequencyApplication:
    def __init__(self, path_to_file):
        self._storage = DataStorage(path_to_file)
        self._stop_word_manager = StopWordFilter()
        self._word_freq_counter = WordFrequencyCounter()

    def run(self):
        for w in self._storage.words():
            if not self._stop_word_manager.is_stop_word(w):
                self._word_freq_counter.increment_count(w)

        word_freqs = self._word_freq_counter.sorted()
        for tf in word_freqs[0:25]:
            print tf[0], ' - ', tf[1]

#
# The main function
#
WordFrequencyApplication(sys.argv[1]).run()
