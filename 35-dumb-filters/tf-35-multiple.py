from keras.models import Model
from keras import layers
from keras.layers import Input, Dense
from keras.utils import plot_model
import numpy as np
import sys, os, string

characters = string.printable
char_indices = dict((c, i) for i, c in enumerate(characters))
indices_char = dict((i, c) for i, c in enumerate(characters))

INPUT_VOCAB_SIZE = len(characters)
LINE_SIZE = 100

def encode_one_hot(s):
    all = []
    for c in s:
        if c not in characters:
            continue
        x = np.zeros((INPUT_VOCAB_SIZE)) 
        index = char_indices[c]
        x[index] = 1 
        all.append(x)
    return all

def decode_one_hot(x):
    s = []
    for onehot in x:
        one_index = np.where(onehot == 1) # tuple of two things
        if len(one_index[1]) > 0:
            n = one_index[1][0]
            c = indices_char[n]
            s.append(c) 
    return ''.join(s)
    
def normalization_layer_set_weights(n_layer):
    wb = []
    b = np.zeros((INPUT_VOCAB_SIZE), dtype=np.float32)
    w = np.zeros((INPUT_VOCAB_SIZE, INPUT_VOCAB_SIZE), dtype=np.float32)
    # Let lower case letters go through
    for c in string.ascii_lowercase:
        i = char_indices[c]
        w[i, i] = 1
    # Map capitals to lower case
    for c in string.ascii_uppercase:
        i = char_indices[c]
        il = char_indices[c.lower()]
        w[i, il] = 1
    # Map all non-letters to space
    sp_idx = char_indices[' ']
    for c in [c for c in list(string.printable) if c not in list(string.ascii_letters)]:
        i = char_indices[c]
        w[i, sp_idx] = 1

    wb.append(w)
    wb.append(b)
    n_layer.set_weights(wb)
    return n_layer

def build_model():
    # Normalize characters using a shared dense model
    n_layer = Dense(INPUT_VOCAB_SIZE)
    raw_inputs = []
    normalized_outputs = []
    for _ in range(0, LINE_SIZE):
        input_char = Input(shape=(INPUT_VOCAB_SIZE, ))
        filtered_char = n_layer(input_char)
        raw_inputs.append(input_char)
        normalized_outputs.append(filtered_char)
    normalization_layer_set_weights(n_layer)

    model = Model(inputs=raw_inputs, outputs=normalized_outputs)
    return model

model = build_model()

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
        normal = decode_one_hot(preds)

        print(normal)
