import operator, collections

def top25(word_list):
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence
    """
    counts = collections.Counter(w for w in word_list)
    return counts.most_common(25)

