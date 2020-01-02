from keras.models import Sequential
from keras.layers import Dense, Activation, Multiply, ReLU, Lambda
import keras.backend as K
import numpy as np
import sys, os, string, random

characters = string.printable
char_indices = dict((c, i) for i, c in enumerate(characters))
indices_char = dict((i, c) for i, c in enumerate(characters))

INPUT_VOCAB_SIZE = len(characters)
BATCH_SIZE = 200

def encode_one_hot(line):
    x = np.zeros((len(line), INPUT_VOCAB_SIZE))
    for i, c in enumerate(line):
        index = char_indices[c] if c in characters else char_indices[' ']
        x[i][index] = 1 
    return x

def encode_values(line):
    x = np.zeros((len(line), INPUT_VOCAB_SIZE))
    for i, c in enumerate(line):
        index = char_indices[c] if c in characters else char_indices[' ']
        for a_c in characters:
            if a_c == c:
                x[i][index] = 1 
            else:
                idx = char_indices[a_c]
                x[i][idx] = idx/index 
    return x

def decode_values(x):
    s = []
    for onehot in x:
        # Find the index of the value closest to 1
        one_index = (np.abs(onehot - 1.0)).argmin()
        s.append(indices_char[one_index]) 
    return ''.join(s)
    
def build_model():
    model = Sequential()
    model.add(Dense(1, input_shape=(INPUT_VOCAB_SIZE,)))
    model.add(Dense(INPUT_VOCAB_SIZE))
    return model

def input_generator(nsamples):
    def generate_line():
        inline = []; outline = []
        for _ in range(nsamples):
            c = random.choice(characters) 
            expected = c.lower() if c in string.ascii_letters else ' ' 
            inline.append(c); outline.append(expected)
        return ''.join(inline), ''.join(outline)

    while True:
        input_data, expected = generate_line()
        data_in = encode_one_hot(input_data)
        data_out = encode_values(expected)
        yield data_in, data_out

def train(model):
    model.compile(loss='mse',
                  optimizer='adam',
                  metrics=['accuracy', 'mse'])
    input_gen = input_generator(BATCH_SIZE)
    validation_gen = input_generator(BATCH_SIZE)
    model.fit_generator(input_gen,
                epochs = 10, workers=1,
                steps_per_epoch = 1000,
                validation_data = validation_gen,
                validation_steps = 10)

model = build_model()
model.summary()
train(model)

input("Network has been trained. Press <Enter> to run program.")
with open(sys.argv[1]) as f:
    for line in f:
        if line.isspace(): continue
        batch = encode_one_hot(line)
        preds = model.predict(batch)
        normal = decode_values(preds)
        print(normal)