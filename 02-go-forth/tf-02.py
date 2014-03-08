#!/usr/bin/env python
import sys, re, operator, string

#
# The all-important data stack
#
stack = []

#
# The heap. Maps names to data (i.e. variables)
#
heap = {}

#
# The new "words" (procedures) of our program
#
def read_file():
    """
    Takes a path to a file on the stack and places the entire
    contents of the file back on the stack.
    """
    f = open(stack.pop())
    # Push the result onto the stack
    stack.append([f.read()])
    f.close()

def filter_chars():
    """
    Takes data on the stack and places back a copy with all 
    nonalphanumeric chars replaced by white space. 
    """
    # This is not in style. RE is too high-level, but using it
    # for doing this fast and short. Push the pattern onto stack
    stack.append(re.compile('[\W_]+'))
    # Push the result onto the stack
    stack.append([stack.pop().sub(' ', stack.pop()[0]).lower()])

def scan():
    """
    Takes a string on the stack and scans for words, placing
    the list of words back on the stack
    """
    # Again, split() is too high-level for this style, but using
    # it for doing this fast and short. Left as exercise.
    stack.extend(stack.pop()[0].split())

def remove_stop_words():
    """ 
    Takes a list of words on the stack and removes stop words.
    """
    f = open('../stop_words.txt')
    stack.append(f.read().split(','))
    f.close()
    # add single-letter words
    stack[-1].extend(list(string.ascii_lowercase))
    heap['stop_words'] = stack.pop()
    # Again, this is too high-level for this style, but using it
    # for doing this fast and short. Left as exercise.
    heap['words'] = []
    while len(stack) > 0:
        if stack[-1] in heap['stop_words']:
            stack.pop() # pop it and drop it
        else:
            heap['words'].append(stack.pop()) # pop it, store it
    stack.extend(heap['words']) # Load the words onto the stack
    del heap['stop_words']; del heap['words'] # Not needed 
    
def frequencies():
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence.
    """
    heap['word_freqs'] = {}
    # A little flavour of the real Forth style here...
    while len(stack) > 0:
        # ... but the following line is not in style, because the 
        # naive implementation would be too slow
        if stack[-1] in heap['word_freqs']:
            # Increment the frequency, postfix style: f 1 +
            stack.append(heap['word_freqs'][stack[-1]]) # push f
            stack.append(1) # push 1
            stack.append(stack.pop() + stack.pop()) # add
        else:
            stack.append(1) # Push 1 in stack[2]
        # Load the updated freq back onto the heap
        heap['word_freqs'][stack.pop()] = stack.pop()  

    # Push the result onto the stack
    stack.append(heap['word_freqs'])
    del heap['word_freqs'] # We don't need this variable anymore

def sort():
    # Not in style, left as exercise
    stack.extend(sorted(stack.pop().iteritems(), key=operator.itemgetter(1)))

# The main function
#
stack.append(sys.argv[1])
read_file(); filter_chars(); scan(); remove_stop_words()
frequencies(); sort()

stack.append(0)
# Check stack length against 1, because after we process
# the last word there will be one item left
while stack[-1] < 25 and len(stack) > 1:
    heap['i'] = stack.pop()
    (w, f) = stack.pop(); print w, ' - ', f
    stack.append(heap['i']); stack.append(1)
    stack.append(stack.pop() + stack.pop())

