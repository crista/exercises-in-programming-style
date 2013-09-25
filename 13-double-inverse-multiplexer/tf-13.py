#!/usr/bin/env python

import sys, re, operator, string

#
# Functions for map reduce
#
def partition(data_str, nlines):
    """ 
    Generator function that partitions the input data_str (a big string)
    into chunks of nlines.
    """
    lines = data_str.split('\n')
    for i in xrange(0, len(lines), nlines):
        yield '\n'.join(lines[i:i+nlines])

def split_words(data_str):
    """ 
    Takes a string, filters non alphanumeric characters, normalizes to
    lower case, scans for words, and filters the stop words. 
    It returns a list of pairs (word, 1), one for each word in the input, so
    [(w1, 1), (w2, 1), ..., (wn, 1)]
    """
    def _filter_chars(str_data):
        """
        Takes a string and returns a copy with all nonalphanumeric chars
        replaced by white space
        """
        pattern = re.compile('[\W_]+')
        return pattern.sub(' ', str_data)

    def _normalize(str_data):
        """
        Takes a string and returns a copy with all characters in lower case
        """
        return str_data.lower()

    def _scan(str_data):
        """
        Takes a string and scans for words, returning
        a list of words.
        """
        return str_data.split()

    def _remove_stop_words(word_list):
        f = open('../stop_words.txt')
        stop_words = f.read().split(',')
        f.close()
        # add single-letter words
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]

    # The actual work of the mapper
    result = []
    words = _remove_stop_words(_scan(_normalize(_filter_chars(data_str))))
    for w in words:
        result.append((w, 1))
    return result

def regroup(pairs_list):
    """
    Takes a list of a list of pairs of the form 
    [[(w1, 1), (w2, 1), ..., (wn, 1)],
     [(w1, 1), (w2, 1), ..., (wn, 1)],
     ...]
    and returns a dictionary mapping each unique word to the corresponding 
    list of pairs, so
    { w1 : [(w1, 1), (w1, 1)...], 
      w2 : [(w2, 1), (w2, 1)...], 
      ...}
    """
    mapping = {}
    for pairs in pairs_list:
        for p in pairs:
            if p[0] in mapping:
                mapping[p[0]].append(p)
            else:
                mapping[p[0]] = [p]
    return mapping
    
def count_words(mapping):
    """ 
    Takes a mapping of the form (word, [(word, 1), (word, 1)...)])
    and returns a pair (word, frequency), where frequency is the sum
    of all the reported occurrences
    """
    def add(x, y):
        return x+y

    return (mapping[0], reduce(add, (pair[1] for pair in mapping[1])))


#
# Auxiliary functions
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

def sort(word_freq):
    """
    Takes a collection of words and their frequencies
    and returns a collection of pairs where the entries are
    sorted by frequency 
    """
    return sorted(word_freq, key=operator.itemgetter(1), reverse=True)


#
# The main function
#
splits = map(split_words, partition(read_file(sys.argv[1]), 200))
splits_per_word = regroup(splits)
word_freqs = sort(map(count_words, splits_per_word.items()))

for tf in word_freqs[0:25]:
    print tf[0], ' - ', tf[1]

