from keras.models import Model, Sequential
from keras import layers
from keras.layers import Input, Dense
from keras.utils import plot_model

import numpy as np
import sys, os, string, random

characters = sorted(string.printable)
char_indices = dict((c, i) for i, c in enumerate(characters))
indices_char = dict((i, c) for i, c in enumerate(characters))

INPUT_VOCAB_SIZE = len(characters)
BATCH_SIZE = 200

def encode_one_hot(c):
    """One-hot encode the given character.
    """
    x = np.zeros((INPUT_VOCAB_SIZE))
    index = char_indices[c]
    x[index] = 1 
    return x

def decode_one_hot(x):
    """Return a character from a one-hot-encoded vector
    """
    one_index = np.argmax(x)
    c = indices_char[one_index]
    return c
    
def build_model():
    print('Build model...')
    model = Sequential()
    model.add(layers.Dense(INPUT_VOCAB_SIZE, input_shape=(INPUT_VOCAB_SIZE, ), activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
    return model

def input_generator(nsamples):
    def generate_char():
        input_data = random.choice(characters) 
        expected = input_data.lower() if input_data in string.ascii_letters else ' ' 
        return input_data, expected

    while True:
        data_in  = np.zeros((nsamples, INPUT_VOCAB_SIZE))
        data_out = np.zeros((nsamples, INPUT_VOCAB_SIZE))
        for n in range(nsamples):
            input_data, expected = generate_char()
            data_in[n] = encode_one_hot(input_data)
            data_out[n] = encode_one_hot(expected)

        yield data_in, data_out

model = build_model()
model.summary()
plot_model(model, to_file='normalization.png', show_shapes=True)

# Train the model each generation and show predictions against a dataset.
val_gen2 = input_generator(4)
for iteration in range(1, 500):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    input_gen = input_generator(BATCH_SIZE)
    val_gen = input_generator(BATCH_SIZE)
    model.fit_generator(input_gen,
                epochs = 1,
                steps_per_epoch = 20,
                validation_data = val_gen,
                validation_steps = 10, workers=1)
    # Select samples from the a set at random so we can visualize errors.
    batch_x, batch_y = next(val_gen2)
    for i in range(len(batch_y)):
        preds = model.predict(batch_x)
        expected = batch_y[i]
        prediction = preds[i]

        correct = decode_one_hot(expected)
        guess = decode_one_hot(prediction)
        print('T', correct)
        print('G', guess)

#with open(sys.argv[1]) as f:
#    for line in f:
#        if line.isspace(): continue
#        onehots = encode_one_hot(line)

#        data = [[] for _ in range(LINE_SIZE)]
#        for i, c in enumerate(onehots):
#            data[i].append(c)
#        for j in range(len(onehots), LINE_SIZE):
#            data[j].append(np.zeros((INPUT_VOCAB_SIZE)))

#        inputs = [np.array(e) for e in data]

#        preds = model.predict(inputs)
#        normal = decode_one_hot(preds[0])

#        print(decode_one_hot(onehots))
#        print(normal)
