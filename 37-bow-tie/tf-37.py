from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import sys, os, string

characters = string.printable
char_indices = dict((c, i) for i, c in enumerate(characters))
indices_char = dict((i, c) for i, c in enumerate(characters))

INPUT_VOCAB_SIZE = len(characters)

def encode_one_hot(line):
    x = np.zeros((len(line), INPUT_VOCAB_SIZE))
    for i, c in enumerate(line):
        index = char_indices[c] if c in characters else char_indices[' ']
        x[i][index] = 1 
    return x

def decode_values(x):
    s = []
    for onehot in x:
        # Find the index of the value closest to 1
        one_index = (np.abs(onehot - 1.0)).argmin()
        s.append(indices_char[one_index]) 
    return ''.join(s)
    
def layer0_set_weights(n_layer):
    wb = []
    w = np.zeros((INPUT_VOCAB_SIZE, 1), dtype=np.float32)
    b = np.zeros((1), dtype=np.float32)
    # Let lower case letters go through
    for c in string.ascii_lowercase:
        i = char_indices[c]
        w[i, 0] = 1.0/i
    # Map capitals to lower case
    for c in string.ascii_uppercase:
        i = char_indices[c]
        il = char_indices[c.lower()]
        w[i, 0] = 1.0/il
    # Map all non-letters to space
    sp_idx = char_indices[' ']
    for c in [c for c in list(string.printable) if c not in list(string.ascii_letters)]:
        i = char_indices[c]
        w[i, 0] = 1.0/sp_idx

    wb.append(w)
    wb.append(b)
    n_layer.set_weights(wb)
    return n_layer

def layer1_set_weights(n_layer):
    wb = []
    w = np.zeros((1, INPUT_VOCAB_SIZE), dtype=np.float32)
    b = np.zeros((INPUT_VOCAB_SIZE), dtype=np.float32)
    # Recover the lower case letters 
    for c in string.ascii_lowercase:
        i = char_indices[c]
        w[0, i] = i
    # Recover the space
    sp_idx = char_indices[' ']
    w[0, sp_idx] = sp_idx

    wb.append(w)
    wb.append(b)
    n_layer.set_weights(wb)
    return n_layer

def build_model():
    model = Sequential()
    model.add(Dense(1, input_shape=(INPUT_VOCAB_SIZE,)))
    model.add(Dense(INPUT_VOCAB_SIZE))
    return model

model = build_model()
model.summary()
layer0_set_weights(model.layers[0])
layer1_set_weights(model.layers[1])

with open(sys.argv[1]) as f:
    for line in f:
        if line.isspace(): continue
        batch = encode_one_hot(line)
        preds = model.predict(batch)
        normal = decode_values(preds)
        print(normal)