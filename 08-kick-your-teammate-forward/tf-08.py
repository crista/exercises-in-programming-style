#!/usr/bin/env python
import sys, re, operator, string

#
# The functions
#
def read_file(path_to_file, word_freqs, func):
    with  open(path_to_file) as f:
        data = f.read()
    func(data, word_freqs, normalize)

def filter_chars(str_data, word_freqs, func):
    pattern = re.compile('[\W_]+')
    func(pattern.sub(' ', str_data), word_freqs, scan)

def normalize(str_data, word_freqs, func):
    func(str_data.lower(), word_freqs, remove_stop_words)

def scan(str_data, word_freqs, func):
    func(str_data.split(), word_freqs, frequencies)

def remove_stop_words(word_list, word_freqs, func):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    # add single-letter words
    stop_words.extend(list(string.ascii_lowercase))
    func([w for w in word_list if not w in stop_words], word_freqs, sort)

def frequencies(word_list, word_freqs, func):
    wf = {}
    for w in word_list:
        if w in wf:
            wf[w] += 1
        else:
            wf[w] = 1
    func(wf, word_freqs, no_op)

def sort(wf, word_freqs, func):
    word_freqs.extend(func(sorted(wf.iteritems(), key=operator.itemgetter(1), reverse=True), None))

def no_op(a, func):
    return a

#
# The main function
#
word_freqs = []
read_file(sys.argv[1], word_freqs, filter_chars)

for (w, c) in word_freqs[0:25]:
    print w, ' - ', c

