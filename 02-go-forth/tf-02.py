#!/usr/bin/env python

import sys, re, operator, string

#
# The all-important data stack
#
stack = []

#
# The heap. Let's make it an associative array
# mapping names to data (i.e. variables)
#
heap = {}

#
# The new "words" of our program
#
def read_file():
    """
    Takes a path to a file and returns the entire
    contents of the file as a string.
    Path to file expected to be on the stack
    """
    f = open(stack.pop())
    # Push the result onto the stack
    stack.append([f.read()])
    f.close()

def filter_chars():
    """
    Takes a string and returns a copy with all nonalphanumeric 
    chars replaced by white space. The data is assumed to be 
    on the stack.
    """
    # This is not in style. RE is too high-level, but using it
    # for doing this fast and short. Push the pattern onto stack
    stack.append(re.compile('[\W_]+'))
    # Push the result onto the stack
    stack.append([stack.pop().sub(' ', stack.pop()[0]).lower()])

def scan():
    """
    Takes a string and scans for words, returning
    a list of words. The data is assumed to be on the stack.
    """
    # Push the result onto the stack.
    # Again, split() is too high-level for this style, but using it
    # for doing this fast and short. Left as exercise.
    stack.append(stack.pop()[0].split())

def remove_stop_words():
    """ 
    Takes a list of words and returns a copy with all stop 
    words removed. The data is assumed to be on the stack.
    """
    f = open('../stop_words.txt')
    stack.append(f.read().split(','))
    f.close()
    # add single-letter words
    stack[1].extend(list(string.ascii_lowercase))
    heap['stop_words'] = stack.pop()
    # Again, this is too high-level for this style, but using it
    # for doing this fast and short. Left as exercise.
    stack.append([w for w in stack.pop() if not w in heap['stop_words']])

def frequencies():
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence. The word list is assumed
    to be on the stack.
    """
    heap['word_list'] = stack.pop()
    heap['word_freqs'] = {}
    # A little flavour of the real Forth style here...
    for wi in range(0, len(heap['word_list'])):
        stack.append(heap['word_list'][wi]) # Push the word, stack[0]
        # ... but the following line is not in style, because the naive implementation 
        # would be too slow, or we'd need to implement faster, hash-based search
        if stack[0] in heap['word_freqs']:
            stack.append((heap['word_freqs'][stack[0]], heap['word_freqs'][stack[0]])) # (w, f) in stack[1]
            stack[1] = (stack[0], stack[1][1] + 1) # Swap the tuple the stack with a new one
            heap['word_freqs'][stack[-1][0]] = stack[-1][1]  # Load the updated freq back onto the heap
        else:
            stack.append((stack[0], 1)) # Push the tuple (w, 1)
            heap['word_freqs'][stack[-1][0]] = stack[-1][1] # Load it back to the heap
        stack.pop() # Pop (w, f)
        stack.pop() # Pop word

    # Push the result onto the stack
    stack.append(heap['word_freqs'])

def sort():
    """
    Takes a dictionary of words and their frequencies
    and returns a list of pairs where the entries are
    sorted by frequency 
    """
    # Not in style, left as exercise
    stack.append(sorted(stack.pop().iteritems(), key=operator.itemgetter(1), reverse=True))


#
# The main function
#
stack.append(sys.argv[1])
read_file(); filter_chars(); scan(); remove_stop_words()
frequencies(); sort()

word_freqs = stack.pop()
for i in range(0, 25):
    stack.append(word_freqs[i])
    print stack[0][0], ' - ', stack[0][1]
    stack.pop()

