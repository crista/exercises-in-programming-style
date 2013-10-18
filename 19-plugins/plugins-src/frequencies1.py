import operator

def top25(word_list):
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence
    """
    if type(word_list) is not list or word_list == []:
        return {}

    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return sorted(word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)[:25]

