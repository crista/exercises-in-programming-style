#!/usr/bin/env python
import sys, re, operator, string, inspect

def read_stop_words():
    """ This function can only be called from a function 
        named extract_words."""
    # Meta-level data: inspect.stack()
    if inspect.stack()[1][3] != 'extract_words':
        return None

    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return stop_words

def extract_words(path_to_file):
    # Meta-level data: locals()
    with open(locals()['path_to_file']) as f:
        str_data = f.read()
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    stop_words = read_stop_words()
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    # Meta-level data: locals()
    word_freqs = {}
    for w in locals()['word_list']:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freq):
    # Meta-level data: locals()
    return sorted(locals()['word_freq'].items(), key=operator.itemgetter(1), reverse=True)

def main():
    word_freqs = sort(frequencies(extract_words(sys.argv[1])))
    for (w, c) in word_freqs[0:25]:
        print(w, '-', c)

if __name__ == "__main__":
    main()

