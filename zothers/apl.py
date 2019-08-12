import sys, string
import numpy as np
from itertools import count

# Get an array of characters from the file, make sure it starts and ends with a space
characters = np.array([' '] + list(open(sys.argv[1]).read()) + [' '])
# Stop words
stop_words = open('../stop_words.txt').read().split(',')
stop_words.extend(list(string.ascii_lowercase))
stop_words = np.array(list(set(stop_words)))

# Normalize
characters[~np.char.isalpha(characters)] = ' '
characters = np.char.lower(characters)
### Split the words
# indices of the spaces
sp = np.where(characters == ' ')
# A little trick: let's double each index, and then take pairs
sp2 = np.repeat(sp, 2)
# Get the pairs as a 2D matrix
w_ranges = np.reshape(sp2[1:-1], (-1, 2))
# Voila! Words are in between spaces
words = [characters[w_ranges[i][0] : w_ranges[i][1]] for i in range(len(w_ranges)) if w_ranges[i][1]-w_ranges[i][0] > 1]

# But this way too much! Let's reduce rows of characters to strings
swords = np.array([''.join(row).strip() for row in words])

# Next, let's remove stop words
non_stop_words = swords[~np.isin(swords, stop_words)]

### Finally, count the word occurrences
uniq, counts = np.unique(non_stop_words, axis=0, return_counts=True)
wf_sorted = sorted(zip(uniq, counts), key = lambda t: t[1], reverse=True)

for w, c in wf_sorted[:25]:
    print(w, ' - ', c)

