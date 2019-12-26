# -*- coding: utf-8 -*-
'''
# An implementation of deep learning for counting symbols
Input:  [10, 12, 10, 11, 2, 2, 2, 1, 1]
Output: words=[2, 10, 1, 12, 11] counts=[3, 2, 2, 1, 1] (Not necessarily in this order)
'''  
from __future__ import print_function
from keras.models import Sequential
from keras import layers, metrics
from keras import backend as K
from keras.utils import plot_model
from keras.utils import to_categorical
import numpy as np
from six.moves import range
import string, re, collections, os, sys

# Parameters for the model and dataset.
TRAINING_SIZE = 50000
VOCAB_SIZE = 1000
SAMPLE_SIZE = 100
TOP = 2
BATCH_SIZE = 50

data_folder = 'words_data' 
if len(sys.argv) > 1:
    data_folder = data_folder + '_' + sys.argv[1]
train_x = os.path.join(data_folder, 'train_x.txt')
train_y = os.path.join(data_folder, 'train_y.txt')
val_x = os.path.join(data_folder, 'val_x.txt')
val_y = os.path.join(data_folder, 'val_y.txt')


class WordTable(object):
    """Given a text file:
    + Encode the words to a one-hot integer representation
    + Decode the one-hot or integer representation to their character output
    + Decode a vector of probabilities to their character output
    """
    def __init__(self):
        """Initialize words table.

        # Arguments
            filename: The file from which to map the words.
        """
        global TRAINING_SIZE
        global VOCAB_SIZE
        global SAMPLE_SIZE
        global BATCH_SIZE

        self.words = set()
        nlines = 0
        max_words = 0
        with open(train_x) as f:
            for line in f:
                words = line.split()
                self.words.update(words)

                nlines = nlines + 1
                if max_words < len(words):
                    max_words = len(words)

        self.words = list(self.words)
        self.word_indices = dict((w, i) for i, w in enumerate(self.words))
        self.indices_word = dict((i, w) for i, w in enumerate(self.words))

        TRAINING_SIZE = nlines
        VOCAB_SIZE = len(self.words)
        SAMPLE_SIZE = max_words
        BATCH_SIZE = 50

    def words_to_indices(self, words):
        return [self.word_indices[w] for w in words]

    def indices_to_words(self, indices):
        return [self.indices_word[i] for i in indices]

    def encode_one_hot(self, W, forConv=False):
        """One-hot encode given word, or list of indices, W.

        # Arguments
            W: either a word or a list of indices, to be encoded.
        """
        if type(W) is string:
            x = np.zeros(VOCAB_SIZE)
            x[self.word_indices[W]] = 1
            return x
        elif type(W) is list: # Example: [3, 9, 5]
            x = np.zeros((SAMPLE_SIZE, VOCAB_SIZE))  if not forConv else np.zeros((SAMPLE_SIZE, VOCAB_SIZE, 1))
            for i, w in enumerate(W):
                if i >= SAMPLE_SIZE: break
                if not forConv:
                    x[i, w] = 1 
                else:
                    x[i, w, 0] = 1
            return x
        else:
            raise Exception("Bad type to encode")


    def decode(self, x):
        """Decode the given vector or 1D array to their character output.

        # Arguments
            x: A vector or a 2D array of probabilities or one-hot representations;
                or a vector of word indices (used with `calc_argmax=False`).
            calc_argmax: Whether to find the word index with maximum
                probability, defaults to `True`.
        """
        if x.ndim == 1: # either a single word, one-hot encoded, or multiple words
            #one_idxs = [i for i, v in enumerate(x) if v >= 0.5]
            one_idxs = np.argpartition(x, -TOP)[-TOP:]
            print(f'Top 2 indices are {one_idxs} and values are ', np.rint(x[one_idxs]))
            return [self.indices_word[i] for i in one_idxs]
        elif x.ndim == 2: # a list of words, each one-hot encoded
            words = []
            for w in x:
                words.append(self.decode(w))
            return words
        else:
            raise Exception("Bad type to decode")


ctable = WordTable()
print(f'Words table with training size {TRAINING_SIZE}, batch size {BATCH_SIZE}, vocab size {VOCAB_SIZE} and sample size {SAMPLE_SIZE}')


def line_x_to_indices(line):
    words = line.split()
    return ctable.words_to_indices(words)

def line_y_to_indices(line):
    pairs = line.split(',')
    if len(pairs[0]) < 2: # no counts here
        return list(zip(ctable.words_to_indices(pairs), [1 for _ in range(len(pairs))]))
    else:
        words =  [p.split()[0] for p in pairs]
        counts = [int(p.split()[1]) for p in pairs] 
        w_indices = ctable.words_to_indices(words)
        return w_indices, counts 

def input_generator(nsamples, train=True, forConv=False):
    print('Generating input for ', 'training' if train else 'validation')
    f_x, f_y = (train_x, train_y) if train else (val_x, val_y)
    with open(f_x) as fx, open(f_y) as fy:
        j = 0
        x = np.zeros((nsamples, SAMPLE_SIZE, VOCAB_SIZE), dtype=np.int) if not forConv else np.zeros((nsamples, SAMPLE_SIZE, VOCAB_SIZE, 1), dtype=np.int)
        y = np.zeros((nsamples, VOCAB_SIZE), dtype=np.float64)
        for line_x, line_y in zip(fx, fy):
            question = line_x_to_indices(line_x)
            expected_w, expected_c = line_y_to_indices(line_y)
            x[j] = ctable.encode_one_hot(question, forConv)
            y[j][expected_w] = expected_c
            j = j + 1
            if j % nsamples == 0:
                yield x, y
                j = 0
                x = np.zeros((nsamples, SAMPLE_SIZE, VOCAB_SIZE), dtype=np.int) if not forConv else np.zeros((nsamples, SAMPLE_SIZE, VOCAB_SIZE, 1), dtype=np.int)
                y = np.zeros((nsamples, VOCAB_SIZE), dtype=np.float64)
        print("End of ", 'training' if train else 'validation')
        return x, y

def topcats(y_true, y_pred):
    return metrics.top_k_categorical_accuracy(y_true, y_pred, k=TOP)

def model_ff():
    print('Build model...')
    epochs = 50
    model = Sequential()
    model.add(layers.Dense(VOCAB_SIZE,  input_shape=(SAMPLE_SIZE, VOCAB_SIZE)))
#    model.add(layers.Dense(VOCAB_SIZE, activation='relu'))
#    model.add(layers.Dropout(0.5))
#    model.add(layers.Dense(150, activation='relu'))
    model.add(layers.Flatten())
 #   model.add(layers.Dense(VOCAB_SIZE * 2, activation='relu'))
    model.add(layers.Dense(VOCAB_SIZE, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                optimizer='adam',
                metrics=['acc', topcats])
    return model, epochs, "words-ff2-{}b-{}ep".format(BATCH_SIZE, epochs)

def model_convnet1D():
    print('Build model...')
    epochs = 1
    model = Sequential()
    model.add(layers.Conv1D(32, 10, activation='relu', 
                input_shape=(SAMPLE_SIZE, VOCAB_SIZE)))
    model.add(layers.MaxPooling1D(2))
    model.add(layers.Conv1D(64, 10, activation='relu'))
    model.add(layers.MaxPooling1D(2))
    model.add(layers.Conv1D(64, 10, activation='relu'))
    model.add(layers.GlobalMaxPooling1D())
    model.add(layers.Dense(VOCAB_SIZE, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                optimizer='adam',
                metrics=['acc', topcats])
    
    return model, epochs, "words-convnet1D-{}b-{}ep".format(BATCH_SIZE, epochs)

def SumPooling2D(x):
    return K.sum(x, axis=1) 

def model_convnet2D():
    print('Build model...')
    epochs = 150
    model = Sequential()
    model.add(layers.Conv2D(VOCAB_SIZE, (1, VOCAB_SIZE),  
                input_shape=(SAMPLE_SIZE, VOCAB_SIZE, 1)))
    model.add(layers.Lambda(SumPooling2D))
    model.add(layers.Reshape((VOCAB_SIZE,)))
    #    model.add(layers.Flatten())
#    model.add(layers.Dense(VOCAB_SIZE))

    model.compile(loss='mean_squared_error',
                optimizer='adam',
                metrics=['acc', topcats])
    
#    model.compile(loss='binary_crossentropy',
#    optimizer='adam',
#    metrics=['acc', topcategories])

    return model, epochs, "words-convnet2D-{}b-{}ep".format(BATCH_SIZE, epochs)


model, epochs, name = model_convnet2D()
model.summary()
plot_model(model, to_file=name + '.png', show_shapes=True)

# Train the model each generation and show predictions against the validation
# dataset.
val_gen_2 = input_generator(5, train=False, forConv=True)
for iteration in range(1, epochs):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    input_gen = input_generator(BATCH_SIZE, forConv=True)
    val_gen = input_generator(BATCH_SIZE, False, forConv=True)
    model.fit_generator(input_gen,
                epochs = 1,
                steps_per_epoch = 20,
                validation_data = val_gen,
                validation_steps = 10, workers=1)
    # Select 10 samples from the validation set at random so we can visualize
    # errors.
#    print(batch_y)
#    print(preds)
    batch_x, batch_y = next(val_gen_2)
    for i in range(len(batch_x)):
        preds = model.predict(batch_x)
        query = batch_x[i]
        expected = batch_y[i]
        prediction = preds[i]
        #print(preds)
#        preds[preds>=0.5] = 1
#        preds[preds<0.5] = 0

        #q = ctable.decode(query)
        correct = ctable.decode(expected)
        guess = ctable.decode(prediction)
        print('T', correct, '    G', guess)

model.summary()
model.save(name + '.h5')

