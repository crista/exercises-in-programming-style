#!/usr/bin/env python
import sys, re, operator, string

#
# Auxiliary functions that can't be lambdas
#
def extract_words(obj, path_to_file):
    with open(path_to_file) as f:
        obj['data'] = f.read()
    pattern = re.compile('[\W_]+')
    data_str = ''.join(pattern.sub(' ', obj['data']).lower())
    obj['data'] = data_str.split()

def load_stop_words(obj):
    with open('../stop_words.txt') as f:
        obj['stop_words'] = f.read().split(',')
    # add single-letter words
    obj['stop_words'].extend(list(string.ascii_lowercase))

def increment_count(obj, w):
    obj['freqs'][w] = 1 if w not in obj['freqs'] else obj['freqs'][w]+1

data_storage_obj = {
    'data' : [],
    'init' : lambda obj, path_to_file : extract_words(obj, path_to_file),
    'words' : lambda obj : obj['data']
}

stop_words_obj = {
    'stop_words' : [],
    'init' : lambda obj : load_stop_words(obj),
    'is_stop_word' : lambda obj, word : word in obj['stop_words']
}

word_freqs_obj = {
    'freqs' : {},
    'increment_count' : lambda obj, w : increment_count(obj, w),
    'sorted' : lambda obj : sorted(obj['freqs'].iteritems(), key=operator.itemgetter(1), reverse=True)
}

data_storage_obj['init'](data_storage_obj, sys.argv[1])
stop_words_obj['init'](stop_words_obj)

for w in data_storage_obj['words'](data_storage_obj):
    if not stop_words_obj['is_stop_word'](stop_words_obj, w):
        word_freqs_obj['increment_count'](word_freqs_obj, w)

word_freqs = word_freqs_obj['sorted'](word_freqs_obj)
for (w, c) in word_freqs[0:25]:
    print w, ' - ', c
