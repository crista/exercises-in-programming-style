import operator

def top25(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return sorted(word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)[:25]

