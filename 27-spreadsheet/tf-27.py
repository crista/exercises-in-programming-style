#!/usr/bin/env python
import sys, re, itertools, operator

#
# The columns. Each column is a data element and a formula.
# The first 2 columns are the input data, so no formulas.
#
all_words = [(), None]
stop_words = [(), None]
non_stop_words = [(), lambda : \
                          list(map(lambda w : \
                            w if w not in stop_words[0] else '',\
                              all_words[0]))]
unique_words = [(),lambda : 
                    set([w for w in non_stop_words[0] if w!=''])]
counts = [(), lambda : 
                list(map(lambda w, word_list : word_list.count(w), \
                    unique_words[0], \
                    itertools.repeat(non_stop_words[0], \
                                   len(unique_words[0]))))]
sorted_data = [(), lambda : sorted(zip(list(unique_words[0]), \
                                       list(counts[0])), \
                                   key=operator.itemgetter(1), 
                                   reverse=True)]

# The entire spreadsheet
all_columns = [all_words, stop_words, non_stop_words,\
               unique_words, counts, sorted_data]

#
# The active procedure over the columns of data.
# Call this everytime the input data changes, or periodically.
#
def update():
    global all_columns
    # Apply the formula in each column
    for c in all_columns:
        if c[1] != None:
            c[0] = c[1]() 


# Load the fixed data into the first 2 columns
all_words[0] = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
stop_words[0] = set(open('../stop_words.txt').read().split(','))
# Update the columns with formulas
update()

for (w, c) in sorted_data[0][:25]:
    print(w, '-', c)
