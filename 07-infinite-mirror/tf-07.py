#!/usr/bin/env python
import re, sys, operator

# Mileage may vary. If this crashes, make it lower
RECURSION_LIMIT = 9500
# We add a few more, because, contrary to the name,
# this doesn't just rule recursion: it rules the depth of the call stack
sys.setrecursionlimit(RECURSION_LIMIT+10)

def count(word_list, word_freqs):
    # What to do with an empty list
    if word_list == []:
        return
    # The base case, what to do with 1 word
    if len(word_list) == 1:
        word = word_list[0]
        if word not in stopwords:
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1
    # The inductive case, what to do with a list of words
    else:
        # Process the head word
        count([word_list[0]], word_freqs)
        # Process the tail 
        count(word_list[1:], word_freqs)

def wf_print(word_freq):
    if word_freq == []:
        return
    if len(word_freq) == 1:
        (w, c) = word_freq[0]
        print w, '-', c
    else:
        wf_print([word_freq[0]])
        wf_print(word_freq[1:])

stopwords = set(open('../stop_words.txt').read().split(','))
words = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
word_freqs = {}
# Theoretically, we would just call count(words, word_freqs)
# Try doing that and see what happens.
for i in range(0, len(words), RECURSION_LIMIT):
    count(words[i:i+RECURSION_LIMIT], word_freqs)

wf_print(sorted(word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)[:25])

