import sys, re, operator, string

class DataStorageManager():
    """ Models the contents of the file """
    _data = ''

    def dispatch(self, message):
        if message[0] == 'init':
            return self._init(message[1])
        elif message[0] == 'words':
            return self._words()
        else:
            raise Exception("Message not understood " + message[0])
 
    def _init(self, path_to_file):
        f = open(path_to_file)
        self._data = f.read()
        f.close()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def _words(self):
        """
        Returns the list words in storage
        """
        data_str = ''.join(self._data)
        return data_str.split()


class StopWordManager():
    """ Models the stop word filter """
    _stop_words = []

    def dispatch(self, message):
        if message[0] == 'init':
            return self._init()
        elif message[0] == 'is_stop_word':
            return self._is_stop_word(message[1])
        else:
            raise Exception("Message not understood " + message[0])
 
    def _init(self):
        f = open('../stop_words.txt')
        self._stop_words = f.read().split(',')
        f.close()
        self._stop_words.extend(list(string.ascii_lowercase))

    def _is_stop_word(self, word):
        return word in self._stop_words

class WordFrequencyManager():
    """ Keeps the word frequency data """
    _word_freqs = {}

    def dispatch(self, message):
        if message[0] == 'increment_count':
            return self._increment_count(message[1])
        elif message[0] == 'sorted':
            return self._sorted()
        else:
            raise Exception("Message not understood " + message[0])
 
    def _increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def _sorted(self):
        return sorted(self._word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)

class WordFrequencyController():

    def dispatch(self, message):
        if message[0] == 'init':
            return self._init(message[1])
        elif message[0] == 'run':
            return self._run()
        else:
            raise Exception("Message not understood " + message[0])
 
    def _init(self, path_to_file):
        self._storage_manager = DataStorageManager()
        self._stop_word_manager = StopWordManager()
        self._word_freq_manager = WordFrequencyManager()
        self._storage_manager.dispatch(['init', path_to_file])
        self._stop_word_manager.dispatch(['init'])

    def _run(self):
        for w in self._storage_manager.dispatch(['words']):
            if not self._stop_word_manager.dispatch(['is_stop_word', w]):
                self._word_freq_manager.dispatch(['increment_count', w])

        word_freqs = self._word_freq_manager.dispatch(['sorted'])
        for tf in word_freqs[0:25]:
            print tf[0], ' - ', tf[1]

#
# The main function
#
wfcontroller = WordFrequencyController()
wfcontroller.dispatch(['init', sys.argv[1]])
wfcontroller.dispatch(['run'])

