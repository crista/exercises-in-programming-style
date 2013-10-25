#!/usr/bin/env python

import sys, re, operator, string

#
# The all-important data stack
#
stack = []

#
# The new "words" of our program
#
def read_file():
    """
    Takes a path to a file and returns the entire
    contents of the file as a string.
    Path to file expected to be on the stack
    """
    path_to_file = stack.pop()
    f = open(path_to_file)
    # Push the result onto the stack
    stack.append([f.read()])
    f.close()

def filter_chars():
    """
    Takes a string and returns a copy with all nonalphanumeric 
    chars replaced by white space. The data is assumed to be on the stack.
    """
    str_data = stack.pop()
    # This is not in style. RE is too high-level, but using it
    # for doing this fast and short. 
    stack.append(re.compile('[\W_]+'))
    pattern = stack.pop()
    # Push the result onto the stack
    stack.append([pattern.sub(' ', str_data[0]).lower()])

def scan():
    """
    Takes a string and scans for words, returning
    a list of words. The data is assumed to be on the stack.
    """
    str_data = stack.pop()
    # Push the result onto the stack
    # Again, split() is too high-level for this style, but using it
    # for doing this fast and short. Left as exercise.
    stack.append(str_data[0].split())

def remove_stop_words():
    """ 
    Takes a list of words and returns a copy with all stop 
    words removed. The data is assumed to be on the stack.
    """
    word_list = stack.pop()
    f = open('../stop_words.txt')
    stack.append([f.read().split(',')])
    f.close()
    # add single-letter words
    stack[0][0].extend(list(string.ascii_lowercase))
    stop_words = stack.pop()[0]
    # Again, this is too high-level for this style, but using it
    # for doing this fast and short. Left as exercise.
    stack.append([w for w in word_list if not w in stop_words])

def frequencies():
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence. The word list is assumed
    to be on the stack.
    """
    word_list = stack.pop()
    word_freqs = {}
    i = len(word_list)
    # A little flavour of the real Forth style here...
    for wi in range(0, len(word_list)):
        stack.append(word_list[wi]) # Push the word, stack[0]
        # ... but the following line is not in style, because the naive implementation 
        # would be too slow, or we'd need to implement faster, hash-based search
        if stack[0] in word_freqs:
            stack.append((word_freqs[stack[0]], word_freqs[stack[0]])) # (w, f) in stack[1]
            stack[1] = (stack[0], stack[1][1] + 1) # Swap the tuple the stack with a new one
            word_freqs[stack[-1][0]] = stack[-1][1]  # Load the updated freq back onto the heap
        else:
            stack.append((stack[0], 1)) # Push the tuple (w, 1)
            word_freqs[stack[-1][0]] = stack[-1][1] # Load it back to the heap
        stack.pop() # Pop (w, f)
        stack.pop() # Pop word

    # Push the result onto the stack
    stack.append(word_freqs)

def sort():
    """
    Takes a dictionary of words and their frequencies
    and returns a list of pairs where the entries are
    sorted by frequency 
    """
    word_freq = stack.pop()
    # Not in style, left as exercise
    return sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)


#
# The main function
#
stack.append(sys.argv[1])
read_file()
filter_chars()
scan()
remove_stop_words()
frequencies()
word_freqs = sort()

for tf in word_freqs[0:25]:
    print tf[0], ' - ', tf[1]

