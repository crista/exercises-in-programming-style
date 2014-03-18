#!/usr/bin/env python

import sys, os, string

# Utility for handling the intermediate 'secondary memory'
def touchopen(filename, *args, **kwargs):
    try:
        os.remove(filename)
    except OSError:
        pass
    open(filename, "a").close() # "touch" file
    return open(filename, *args, **kwargs)

# The constrained memory should have no more than 1024 cells
data = []
# We're lucky:
# The stop words are only 556 characters and the lines are all 
# less than 80 characters, so we can use that knowledge to 
# simplify the problem: we can have the stop words loaded in 
# memory while processing one line of the input at a time.
# If these two assumptions didn't hold, the algorithm would 
# need to be changed considerably.

# Overall strategy: (PART 1) read the input file, count the 
# words, increment/store counts in secondary memory (a file) 
# (PART 2) find the 25 most frequent words in secondary memory

# PART 1: 
# - read the input file one line at a time
# - filter the characters, normalize to lower case
# - identify words, increment corresponding counts in file

# Load the list of stop words
f = open('../stop_words.txt')
data = [f.read(1024).split(',')] # data[0] holds the stop words
f.close()

data.append([])    # data[1] is line (max 80 characters)
data.append(None)  # data[2] is index of the start_char of word
data.append(0)     # data[3] is index on characters, i = 0
data.append(False) # data[4] is flag indicating if word was found
data.append('')    # data[5] is the word
data.append('')    # data[6] is word,NNNN
data.append(0)     # data[7] is frequency

# Open the secondary memory
word_freqs = touchopen('word_freqs', 'rb+')
# Open the input file
f = open(sys.argv[1])
# Loop over input file's lines
while True:
    data[1] = [f.readline()] 
    if data[1] == ['']: # end of input file
        break
    if data[1][0][len(data[1][0])-1] != '\n': # If it does not end with \n
        data[1][0] = data[1][0] + '\n' # Add \n
    data[2] = None
    data[3] = 0 
    # Loop over characters in the line
    for c in data[1][0]: # elimination of symbol c is exercise
        if data[2] == None:
            if c.isalnum():
                # We found the start of a word
                data[2] = data[3]
        else:
            if not c.isalnum():
                # We found the end of a word. Process it
                data[4] = False 
                data[5] = data[1][0][data[2]:data[3]].lower()
                # Ignore words with len < 2, and stop words
                if len(data[5]) >= 2 and data[5] not in data[0]:
                    # Let's see if it already exists
                    while True:
                        data[6] = word_freqs.readline().strip()
                        if data[6] == '':
                            break;
                        data[7] = int(data[6].split(',')[1])
                        # word, no white space
                        data[6] = data[6].split(',')[0].strip() 
                        if data[5] == data[6]:
                            data[7] += 1
                            data[4] = True
                            break
                    if not data[4]:
                        word_freqs.seek(0, 1) # Needed in Windows
                        word_freqs.writelines("%20s,%04d\n" % (data[5], 1))
                    else:
                        word_freqs.seek(-26, 1)
                        word_freqs.writelines("%20s,%04d\n" % (data[5], data[7]))
                    word_freqs.seek(0,0)
                # Let's reset
                data[2] = None
        data[3] += 1
# We're done with the input file
f.close()
word_freqs.flush()

# PART 2
# Now we need to find the 25 most frequently occuring words.
# We don't need anything from the previous values in memory
del data[:]

# Let's use the first 25 entries for the top 25 words
data = data + [[]]*(25 - len(data))
data.append('') # data[25] is word,freq from file
data.append(0)  # data[26] is freq

# Loop over secondary memory file
while True:
    data[25] = word_freqs.readline().strip()
    if data[25] == '': # EOF
        break
    data[26] = int(data[25].split(',')[1]) # Read it as integer
    data[25] = data[25].split(',')[0].strip() # word
    # Check if this word has more counts than the ones in memory
    for i in range(25): # elimination of symbol i is exercise
        if data[i] == [] or data[i][1] < data[26]:
            data.insert(i, [data[25], data[26]]) 
            del data[26] #  delete the last element
            break
            
for tf in data[0:25]: # elimination of symbol tf is exercise
    if len(tf) == 2:
        print tf[0], ' - ', tf[1]
# We're done
word_freqs.close()
