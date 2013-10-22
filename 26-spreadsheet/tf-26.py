import sys, re, itertools, operator

#
# The columns. Each column comprises of a data element and a formula.
# The first 2 columns are the input data, so no formulas.
#
all_words = [(), None]
stop_words = [(), None]
non_stop_words = [(), lambda w : w if w not in stop_words[0] else '']
unique_words = [(), lambda word_list: set([w for w in word_list if w != ''])]
counts = [(), lambda w, word_list : word_list.count(w)]
sorted_data = [(), lambda z : sorted(z, key=operator.itemgetter(1), reverse=True)]

#
# The active procedure over the columns of data.
# Call this everytime the input data changes, or periodically.
#
def update():
    global non_stop_words
    global unique_words
    global counts
    global sorted_data
    # Apply the formulas to the 4 last columns
    non_stop_words[0] = map(non_stop_words[1], all_words[0])
    unique_words[0] = unique_words[1](non_stop_words[0])
    counts[0] = map(counts[1], unique_words[0], itertools.repeat(non_stop_words[0], len(unique_words[0])))
    sorted_data[0] = sorted_data[1](zip(list(unique_words[0]), counts[0]))
#
# Load the fixed data into the first 2 columns
#
all_words[0] = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
stop_words[0] = set(open('../stop_words.txt').read().split(','))
# Update the columns with formulas
update()

# Display
for (w, c) in sorted_data[0][:25]:
    print w, '-', c
