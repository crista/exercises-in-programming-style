import sys, string
import numpy as np

# Get an array of characters from the file, make sure it starts and ends with a space
# Example input: "Hello  World! " 
characters = np.array([' '] + list(open(sys.argv[1]).read()) + [' '])
# Result: array([' ', 'H', 'e', 'l', 'l', 'o', ' ', ' ', 
#                'W', 'o', 'r', 'l', 'd', '!', ' ', ' '], dtype='<U1')

# Normalize
characters[~np.char.isalpha(characters)] = ' '
characters = np.char.lower(characters)
# Result: array([' ', 'h', 'e', 'l', 'l', 'o', ' ', ' ', 
#                'w', 'o', 'r', 'l', 'd', ' ', ' '], dtype='<U1')

### Split the words, by finding the indices of spaces
sp = np.where(characters == ' ')
# Result: (array([ 0,  6,  7, 13, 14], dtype=int64),)

# A little trick: let's double each index, and then take pairs
sp2 = np.repeat(sp, 2)
# Result: array([ 0,  0,  6,  6,  7,  7, 13, 13, 14, 14], dtype=int64)

# Get the pairs as a 2D matrix, skip the first and the last
w_ranges = np.reshape(sp2[1:-1], (-1, 2))
# Result: array([[ 0,  6],
#                [ 6,  7],
#                [ 7, 13],
#                [13, 14]], dtype=int64)

# Voila! Words are in between spaces, given as pairs of indices
# But remember to skip contiguous spaces (the conditional at the end)
words = [characters[w_ranges[i][0] : w_ranges[i][1]] for i in range(len(w_ranges)) if w_ranges[i][1]-w_ranges[i][0] > 1]
# Result: [array([' ', 'h', 'e', 'l', 'l', 'o'], dtype='<U1'), 
#          array([' ', 'w', 'o', 'r', 'l', 'd'], dtype='<U1')]

# But this way too much! Let's reduce rows of characters to strings
swords = np.array([''.join(row).strip() for row in words])
# Result: array(['hello', 'world'], dtype='<U5')

# Next, let's remove stop words
stop_words = open('../stop_words.txt').read().split(',')
stop_words.extend(list(string.ascii_lowercase))
stop_words = np.array(list(set(stop_words)))
non_stop_words = swords[~np.isin(swords, stop_words)]

### Finally, count the word occurrences
uniq, counts = np.unique(non_stop_words, axis=0, return_counts=True)
wf_sorted = sorted(zip(uniq, counts), key = lambda t: t[1], reverse=True)

for w, c in wf_sorted[:25]:
    print(w, '-', c)

