import sys, re, operator, string

#
# The monadic class for this example
#
class TFTheOne:
    def __init__(self, v):
        self._value = v

    def bind(self, func):
        result = func(self._value)
        return TFTheOne(result)

def printm(monad):
    print monad._value,

#
# The functions
#
def read_file(path_to_file):
    """
    Takes a path to a file and returns the entire
    contents of the file as a string
    """
    f = open(path_to_file)
    data = f.read()
    f.close()
    return data

def filter_chars(str_data):
    """
    Takes a string and returns a copy with all nonalphanumeric chars
    replaced by white space
    """
    pattern = re.compile('[\W_]+')
    return pattern.sub(' ', str_data)

def normalize(str_data):
    """
    Takes a string and returns a copy with all characters in lower case """
    return str_data.lower()

def scan(str_data):
    """
    Takes a string and scans for words, returning
    a list of words.
    """
    return str_data.split()

def remove_stop_words(word_list):
    """ Takes a list of words and returns a copy with all stop words removed """
    f = open('../stop_words.txt')
    stop_words = f.read().split(',')
    f.close()
    # add single-letter words
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
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

def sort(word_freq):
    """
    Takes a dictionary of words and their frequencies and returns a list 
    of pairs where the entries are sorted by frequency 
    """
    return sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)

def print_freqs(word_freqs):
    for tf in word_freqs[0:25]:
        print tf[0], ' - ', tf[1]

def top25_freqs(word_freqs):
    top25 = ""
    for tf in word_freqs[0:25]:
        top25 += str(tf[0]) + ' - ' + str(tf[1]) + '\n'
    return top25

#
# The main function
#
printm(TFTheOne(sys.argv[1]).bind(read_file).bind(filter_chars).bind(normalize).bind(scan).bind(remove_stop_words).bind(frequencies).bind(sort).bind(top25_freqs))

