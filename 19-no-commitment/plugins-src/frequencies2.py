import operator, collections

def top25(word_list):
    counts = collections.Counter(w for w in word_list)
    return counts.most_common(25)

