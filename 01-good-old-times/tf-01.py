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

# The constrained memory, which consists of only 1024 bytes by constraint
data = []

# Overall strategy: 
# - read the input file one line at a time
# - filter the characters, normalize to lower case
# - identify words, incrementing corresponding counts (in secondary memory)


# We're lucky:
# The stop words are only 556 bytes and the lines are all less than
# 80 characters, so we can use that knowledge to simplify the problem:
# we can have the stop words loaded in memory while processing one line
# of the input at a time.
# If these two assumptions didn't hold, the algorithm would need to be
# changed considerably.

# Load the list of stop words
f = open('../stop_words.txt')
data = [f.read(1024).split(',')] # data[0] holds the stop words
f.close()

data.append([])    # data[1] is the line
data.append(None)  # data[2] is the index of the start_char of a word
data.append(0)     # data[3] is an index, i = 0
data.append(False) # data[4] is a flag indicating where a word was found
data.append('')    # data[5] is the word
data.append('')    # data[6] is word,NNNN from the word_freqs file, and then just the word
data.append(0)     # data[7] is frequency

word_freqs = touchopen('word_freqs', 'rb+')
f = open(sys.argv[1])
while True:
    data[1] = [f.readline()] 
    #print data[1]
    if data[1] == ['']: # end of input file
        break
    data[2] = None
    data[3] = 0 
    for c in data[1][0]: # elimination of symbol c left as exercise
        if data[2] == None:
            if c.isalnum():
                # We found the start of a word
                data[2] = data[3]
        else:
            if not c.isalnum():
                # We found the end of a word. Process it
                data[4] = False 
                data[5] = data[1][0][data[2]:data[3]].lower()
                #print "Looking at " + data[5]

                # Ignore words with less than 2 characters and stop words
                if len(data[5]) >= 2 and data[5] not in data[0]:
                    # Let's see if it already exists
                    while True:
                        data[6] = word_freqs.readline().strip()
                        #print "  Comparing to " + data[6]
                        if data[6] == '':
                            break;
                        data[7] = int(data[6].split(',')[1])
                        data[6] = data[6].split(',')[0].strip() # word, no white space
                        if data[5] == data[6]:
                            data[7] += 1
                            data[4] = True
                            break

                    if not data[4]:
                        word_freqs.seek(0, 1) # Not needed in Unix, needed in Windows
                        word_freqs.writelines("%20s,%04d\n" % (data[5], 1))
                    else:
                        word_freqs.seek(-26, 1)
                        word_freqs.writelines("%20s,%04d\n" % (data[5], data[7]))

                    word_freqs.seek(0,0)

                # Let's reset
                data[2] = None
        data[3] += 1

f.close()
word_freqs.flush()

# Now we need to find the 25 most frequently occuring words.
# We don't need anything from the previous values in memory
del data[:]

# Let's use the first 25 entries for the top 25 words
data = data + [[]]*(25 - len(data))
data.append('') # data[25] is word,freq read from word_freqs file, and then word
data.append(0)  # data[26] is freq
#print data

while True:
    data[25] = word_freqs.readline().strip()
    if data[25] == '':
        break;
    data[26] = int(data[25].split(',')[1])
    data[25] = data[25].split(',')[0].strip() # word, no white space

    for i in range(25): # elimination of symbol i left as exercise
        if data[i] == [] or data[i][1] < data[26]:
            #print str(i) + " " + str(data[25]) + " " + str(data[26])
            data.insert(i, [data[25], data[26]]) 
            del data[26] #  pop the last element
            break
            

for tf in data[0:25]: # elimination of symbol tf left as exercise
    if len(tf) == 2:
        print tf[0], ' - ', tf[1]

word_freqs.close()
