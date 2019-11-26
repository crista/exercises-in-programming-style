import os, sys
import collections
import numpy as np
import re

SAMPLE_SIZE = 80
VOCAB_SIZE = 10
TOP = 5

stopwords = set(open('../stop_words.txt').read().split(','))
all_words = re.findall('[a-z]{2,}', open('../pride-and-prejudice.txt').read().lower())
words = list(set([w for w in all_words if w not in stopwords]))

def generate_pair(with_counts):
    # Grab a slice of the input file of size SAMPLE_SIZE
    index = np.random.randint(0, len(all_words) - SAMPLE_SIZE)
    querytmp = all_words[index:index+SAMPLE_SIZE]
    # Replace unknown words with known ones
    query = querytmp
    for i, w in enumerate(querytmp):
        if w not in words[:VOCAB_SIZE] and query[i] == w:
            # Replace ALL occurrences in query with the same replacement word
            other = words[np.random.randint(0, VOCAB_SIZE/2)]
            query = [other if v == w else v for v in query]

    counts = collections.Counter(query)
    top = counts.most_common()
    if not with_counts:
        ans = list(list(zip(*top))[0])
    else:
        ans = [t[0] + " " + str(t[1]) for t in top]
    return query, ans


def generate_data(data_folder, ntrain, nval, vocab_size, with_counts):
    train_x = os.path.join(data_folder, 'train_x.txt')
    train_y = os.path.join(data_folder, 'train_y.txt')
    val_x = os.path.join(data_folder, 'val_x.txt')
    val_y = os.path.join(data_folder, 'val_y.txt')

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    global VOCAB_SIZE
    VOCAB_SIZE = vocab_size
    with open(train_x, 'w') as fx, open(train_y, 'w') as fy:
        for _ in range(0, ntrain):
            query, ans = generate_pair(with_counts)
            fx.write(' '.join(query) + '\n')
            fy.write(','.join(ans) + '\n')

    with open(val_x, 'w') as fx, open(val_y, 'w') as fy:
        for _ in range(0, nval):
            query, ans = generate_pair(with_counts)
            fx.write(' '.join(query) + '\n')
            fy.write(','.join(ans) + '\n')

def main():
    # [1]: number of samples in training set
    # [2]: number of samples in validation set
    # [3]: vocabulary size
    # [4]: output with (1) or without (0) counts
    data_folder = 'words_data'
    if len(sys.argv) > 3: data_folder = data_folder + "_" + sys.argv[3]
    generate_data(data_folder, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), bool(int(sys.argv[4])))

if __name__ == "__main__":
    main()

