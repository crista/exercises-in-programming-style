import re, sys, operator

# Mileage may vary. If this crashes, make it lower
RECURSION_LIMIT = 9500
# We add a few more, because, contrary to the name,
# this doesn't just rule recursion: it rules the depth of the call stack
sys.setrecursionlimit(RECURSION_LIMIT+10)

def count(word_list, word_freqs):
    if word_list == []:
        return

    if word_list[0] not in stopwords:
        if word_list[0] in word_freqs:
            word_freqs[word_list[0]] += 1
        else:
            word_freqs[word_list[0]] = 1

    count(word_list[1:], word_freqs)

stopwords = set(open('../stop_words.txt').read().split(','))
words = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
word_freqs = {}
# Theoretically, we would just call count(words, word_freqs)
# Try doing that and see what happens.
for i in range(0, len(words), RECURSION_LIMIT):
    count(words[i:i+RECURSION_LIMIT], word_freqs)

for (w, c) in sorted(word_freqs.iteritems(), key=operator.itemgetter(1), reverse=True)[:25]:
    print w, '-', c
