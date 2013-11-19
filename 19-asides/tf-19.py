#!/usr/bin/env python

import sys, re, operator, string, time

#
# The functions
#
def extract_words(path_to_file):
    """
    Takes a path to a file and returns the non-stop
    words, after properly removing nonalphanumeric chars
    and normalizing for lower case
    """
    with open(path_to_file) as f:
        str_data = f.read()
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
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
    Takes a dictionary of words and their frequencies
    and returns a list of pairs where the entries are
    sorted by frequency 
    """
    return sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)

# The side functionality
def profile(f):
    def profilewrapper(*arg, **kw):
        start_time = time.time()
        ret_value = f(*arg, **kw)
        elapsed = time.time() - start_time
        print "%s(...) took %s secs" % (f.__name__, elapsed)
        return ret_value
    return profilewrapper

# join points
tracked_functions = [extract_words, frequencies, sort]
# weaver
for func in tracked_functions:
    globals()[func.func_name]=profile(func)

#
# The main function
#
word_freqs = sort(frequencies(extract_words(sys.argv[1])))

for tf in word_freqs[0:25]:
    print tf[0], ' - ', tf[1]

