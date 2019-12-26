from keras.models import Model
from keras import layers, metrics
from keras.layers import Input, Dense
from keras.utils import plot_model

import numpy as np
import sys, os, string, random

characters = sorted(string.printable)
char_indices = dict((c, i) for i, c in enumerate(characters))
indices_char = dict((i, c) for i, c in enumerate(characters))

INPUT_VOCAB_SIZE = len(characters)
LINE_SIZE = 100
BATCH_SIZE = 200

def encode_one_hot(s):
    """One-hot encode all characters of the given string.
    """
    all = []
    for c in s:
        x = np.zeros((INPUT_VOCAB_SIZE)) 
        index = char_indices[c]
        x[index] = 1 
        all.append(x)
    return all

def encode_one_hot2(s):
    """One-hot encode all characters of the given string.
    """
    x = np.zeros((LINE_SIZE, INPUT_VOCAB_SIZE))
    for n, c in enumerate(s):
        index = char_indices[c]
        x[n, index] = 1 
    return x

def decode_one_hot(x):
    """Return a string from a one-hot-encoded matrix
    """
    s = []
    for onehot in x:
        one_index = np.argmax(onehot)
        c = indices_char[one_index]
        s.append(c) 
    return ''.join(s)

def build_model():
    print('Build model...')
    
    # Normalize every character in the input, using a shared dense model
    n_layer = Dense(INPUT_VOCAB_SIZE, activation = "softmax")
    raw_inputs = []
    normalized_outputs = []
    for _ in range(0, LINE_SIZE):
        input_char = Input(shape=(INPUT_VOCAB_SIZE, ))
        filtered_char = n_layer(input_char)
        raw_inputs.append(input_char)
        normalized_outputs.append(filtered_char)

    merged_output = layers.concatenate(normalized_outputs, axis=-1)

    reshape = layers.Reshape((LINE_SIZE, INPUT_VOCAB_SIZE, ))
    reshaped_output = reshape(merged_output)

    model = Model(inputs=raw_inputs, outputs=reshaped_output)
    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

    return model

def input_generator(nsamples):
    def generate_line():
        input_data = [random.choice(characters) for _ in range(random.randint(1, LINE_SIZE))]
        expected = [c.lower() if c in string.ascii_letters else ' ' for c in input_data]
        return input_data, expected

    while True:
        data_in  = [[] for _ in range(LINE_SIZE)]
        data_out = np.zeros((nsamples, LINE_SIZE, INPUT_VOCAB_SIZE))
        for n in range(nsamples):
            input_data, expected = generate_line()
            input_data = encode_one_hot(input_data)
            for i, c in enumerate(input_data):
                data_in[i].append(c)
            for j in range(len(input_data), LINE_SIZE):
                data_in[j].append(np.zeros((INPUT_VOCAB_SIZE)))

            data_out[n] = encode_one_hot2(expected)

        inputs = [np.array(e) for e in data_in]

        yield inputs, data_out

model = build_model()
#model.summary()
plot_model(model, to_file='normalization.png', show_shapes=True)

# Train the model each generation and show predictions against the validation
# dataset.
val_gen2 = input_generator(1)
for iteration in range(1, 12):
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
        print('T:', correct)
        print('G:', guess)

with open(sys.argv[1]) as f:
    for line in f:
        if line.isspace(): continue
        onehots = encode_one_hot(line)

        data = [[] for _ in range(LINE_SIZE)]
        for i, c in enumerate(onehots):
            data[i].append(c)
        for j in range(len(onehots), LINE_SIZE):
            data[j].append(np.zeros((INPUT_VOCAB_SIZE)))

        inputs = [np.array(e) for e in data]

        preds = model.predict(inputs)
        normal = decode_one_hot(preds[0])

        print(decode_one_hot(onehots))
        print(normal)
