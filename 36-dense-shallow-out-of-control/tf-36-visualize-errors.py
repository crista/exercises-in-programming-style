from keras.models import Sequential
from keras.layers import Dense
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
        if c in characters:
            index = char_indices[c]
        else:
            index = char_indices[' ']
        x[i][index] = 1 
    return x

def decode_one_hot(x):
    s = []
    for onehot in x:
        one_index = np.argmax(onehot) 
        s.append(indices_char[one_index]) 
    return ''.join(s)
    
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
        data_out = encode_one_hot(expected)
        yield data_in, data_out

def build_model():
    # Normalize characters using a dense layer
    model = Sequential()
    dense_layer = Dense(INPUT_VOCAB_SIZE, 
                        input_shape=(INPUT_VOCAB_SIZE,),
                        activation='softmax')
    model.add(dense_layer)
    return model

def train_model(model):
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    # Train the model each generation and show predictions
    val_gen2 = input_generator(20)
    for iteration in range(1, 50):
        print()
        print('Iteration', iteration, '-' * 50)
        input_gen = input_generator(BATCH_SIZE)
        val_gen = input_generator(BATCH_SIZE)
        model.fit_generator(input_gen,
                    epochs = 1, workers=1,
                    steps_per_epoch = 20,
                    validation_data = val_gen,
                    validation_steps = 10)
        # Visualize errors
        batch_x, batch_y = next(val_gen2)
        preds = model.predict(batch_x)
        original = decode_one_hot(batch_x)
        correct = decode_one_hot(batch_y)
        guess = decode_one_hot(preds)
        print('Original   :', original)
        print('True output:', correct)
        print('Prediction :', guess)

model = build_model()
train_model(model)
input("Network has been trained. Press <Enter> to run program.")

with open(sys.argv[1]) as f:
    for line in f:
        if line.isspace(): continue
        batch = encode_one_hot(line)
        preds = model.predict(batch)
        normal = decode_one_hot(preds)
        print(normal)