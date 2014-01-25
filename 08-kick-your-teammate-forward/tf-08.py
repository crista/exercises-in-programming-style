#!/usr/bin/env python
import sys, re, operator, string

#
# The functions
#
def read_file(path_to_file, func):
    with  open(path_to_file) as f:
        data = f.read()
    func(data, normalize)

def filter_chars(str_data, func):
    pattern = re.compile('[\W_]+')
    func(pattern.sub(' ', str_data), scan)

def normalize(str_data, func):
    func(str_data.lower(), remove_stop_words)

def scan(str_data, func):
    func(str_data.split(), frequencies)

def remove_stop_words(word_list, func):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    # add single-letter words
    stop_words.extend(list(string.ascii_lowercase))
    func([w for w in word_list if not w in stop_words], sort)

def frequencies(word_list, func):
    wf = {}
    for w in word_list:
        if w in wf:
            wf[w] += 1
        else:
            wf[w] = 1
    func(wf, format)

def sort(wf, func):
    func(sorted(wf.iteritems(), key=operator.itemgetter(1), reverse=True), print_all)

def no_op(func):
    return

def format(word_freqs, func):
    text = ""
    for (w, c) in word_freqs[0:25]:
        text = text + w + ' - ' + str(c) + '\n'
    func(text, no_op)

def print_all(text, func):
    print text
    func(None) 
    
#
# The main function
#
read_file(sys.argv[1], filter_chars)