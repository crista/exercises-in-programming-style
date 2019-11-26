import os, sys
import collections
import numpy as np
import re, string

MAX_LINE_SIZE = 80
MAX_WORDS_IN_LINE = 20

all_chars = ""
with open('pride-and-prejudice.txt') as f:
    all_chars = f.read().replace('\n', ' ')
all_words = re.findall('[a-z]{2,}', all_chars.lower())
words = list(set(all_words))

def generate_pair():
    # Grab a slice of the input file of size MAX_LINE_SIZE
    index = np.random.randint(0, len(all_chars) - MAX_LINE_SIZE)
    cquery = ' ' + all_chars[index:index+MAX_LINE_SIZE - 2] + ' ' 
    # Replace unknown words with known ones
    wquery = set(re.findall('[a-z]{2,}', cquery.lower()))
    for w in wquery:
        if w not in words[:VOCAB_SIZE]:
            # Replace ALL occurrences in query with the same replacement word
            other = words[np.random.randint(0, VOCAB_SIZE/2)]
            exp = '[^a-z]' + w + '[^a-z]'
            indices = [(m.start()+1, m.end()-1) for m in re.finditer(exp, cquery.lower())]
            for b, e in reversed(indices):
                cquery = cquery[0:b] + other + cquery[e:]

    # Make sure the size of all chars is less than MAX_LINE_SIZE
    if len(cquery) >= MAX_LINE_SIZE:
        last_sp = cquery[:MAX_LINE_SIZE].rfind(' ')
        cquery = cquery[:last_sp] + ' ' * (MAX_LINE_SIZE - last_sp)

    # OK, now that we have the sequence of chars, find its sequence of words
    # [TODO] Remember to remove stop words
    list_of_words = re.findall('[a-z]{2,}', cquery.lower())

    return cquery.strip(), list_of_words


def generate_data(ntrain, nval, vocab_size, data_folder, train_x, train_y, val_x, val_y):
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    global VOCAB_SIZE
    VOCAB_SIZE = vocab_size
    with open(train_x, 'w') as fx, open(train_y, 'w') as fy:
        for _ in range(0, ntrain):
            query, ans = generate_pair()
            fx.write(query + '\n')
            fy.write(','.join(ans) + '\n')

    with open(val_x, 'w') as fx, open(val_y, 'w') as fy:
        for _ in range(0, nval):
            query, ans = generate_pair()
            fx.write(query + '\n')
            fy.write(','.join(ans) + '\n')

def main():
    # [1]: number of samples in training set
    # [2]: number of samples in validation set
    # [3]: vocabulary size
    data_folder = 'c2w_data'
    if len(sys.argv) > 3: data_folder = data_folder + "_" + sys.argv[3]
    train_x = os.path.join(data_folder, 'train_x.txt')
    train_y = os.path.join(data_folder, 'train_y.txt')
    val_x = os.path.join(data_folder, 'val_x.txt')
    val_y = os.path.join(data_folder, 'val_y.txt')
    generate_data(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), data_folder, train_x, train_y, val_x, val_y)

if __name__ == "__main__":
    main()

