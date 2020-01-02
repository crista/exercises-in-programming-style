from keras.models import Sequential
from keras.layers import Dense
from keras.losses import binary_crossentropy, categorical_crossentropy
from keras.optimizers import SGD
from keras. metrics import top_k_categorical_accuracy
from keras import backend as K
import numpy as np
import sys, os, string, random

characters = string.printable
char_indices = dict((c, i) for i, c in enumerate(characters))
indices_char = dict((i, c) for i, c in enumerate(characters))

INPUT_VOCAB_SIZE = len(characters)
LINE_SIZE = 80
BATCH_SIZE = 200
STEPS_PER_EPOCH = 5000
EPOCHS = 4

def encode_one_hot(line):
    x = np.zeros((1, LINE_SIZE, INPUT_VOCAB_SIZE))
    sp_idx = char_indices[' ']
    for i, c in enumerate(line):
        index = char_indices[c] if c in characters else sp_idx
        x[0][i][index] = 1 
    # Pad with spaces
    for i in range(len(line), LINE_SIZE):
        x[0][i][sp_idx] = 1 
    return x.reshape([1, LINE_SIZE*INPUT_VOCAB_SIZE])

def decode_one_hot(y):
    s = []
    x = y.reshape([1, LINE_SIZE, INPUT_VOCAB_SIZE])
    for onehot in x[0]:
        one_index = np.argmax(onehot) 
        s.append(indices_char[one_index]) 
    return ''.join(s)
    
def input_generator(nsamples):
    def generate_line():
        inline = []; outline = []
        for _ in range(LINE_SIZE):
            c = random.choice(characters) 
            expected = c.lower() if c in string.ascii_letters else ' ' 
            inline.append(c); outline.append(expected)
        for i in range(LINE_SIZE):
            if outline[i] == ' ': continue
            if i > 0 and i < LINE_SIZE - 1:
                outline[i] = ' ' if outline[i-1] == ' ' and outline[i+1] == ' ' else outline[i]
            if (i == 0 and outline[i+1] == ' ') or (i == LINE_SIZE-1 and outline[i-1] == ' '):
                outline[i] = ' '
        return ''.join(inline), ''.join(outline)

    while True:
        data_in = np.zeros((nsamples, LINE_SIZE * INPUT_VOCAB_SIZE))
        data_out = np.zeros((nsamples, LINE_SIZE * INPUT_VOCAB_SIZE))
        for i in range(nsamples):
            input_data, expected = generate_line()
            data_in[i] = encode_one_hot(input_data)[0]
            data_out[i] = encode_one_hot(expected)[0]
        yield data_in, data_out

def train(model):
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    input_gen = input_generator(BATCH_SIZE)
    validation_gen = input_generator(BATCH_SIZE)
    model.fit_generator(input_gen,
                epochs = EPOCHS, workers=1,
                steps_per_epoch = STEPS_PER_EPOCH,
                validation_data = validation_gen,
                validation_steps = 10)

def build_model():
    # Normalize characters using a dense layer
    model = Sequential()
    model.add(Dense(LINE_SIZE*INPUT_VOCAB_SIZE, 
                    input_shape=(LINE_SIZE*INPUT_VOCAB_SIZE,), 
                    activation='sigmoid'))
    return model

def build_deep_model():
    # Normalize characters using a dense layer
    model = Sequential()
    model.add(Dense(80, 
                    input_shape=(LINE_SIZE*INPUT_VOCAB_SIZE,), 
                    activation='sigmoid'))
    model.add(Dense(800, activation='sigmoid'))
    model.add(Dense(LINE_SIZE*INPUT_VOCAB_SIZE, activation='sigmoid'))
    return model

model = build_deep_model()
model.summary()
train(model)

input("Network has been trained. Press <Enter> to run program.")
with open(sys.argv[1]) as f:
    for line in f:
        if line.isspace(): continue
        batch = encode_one_hot(line)
        preds = model.predict(batch)
        normal = decode_one_hot(preds)
        print(normal)