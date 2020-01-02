from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import sys, os, string

characters = string.printable
char_indices = dict((c, i) for i, c in enumerate(characters))
indices_char = dict((i, c) for i, c in enumerate(characters))

INPUT_VOCAB_SIZE = len(characters)
WINDOW_SIZE = 3

def encode_one_hot(line):
    line = " " + line + " "
    x = np.zeros((len(line), INPUT_VOCAB_SIZE))
    for i, c in enumerate(line):
        index = char_indices[c] if c in characters else char_indices[' ']
        x[i][index] = 1 
    return x

def decode_one_hot(x):
    s = []
    for onehot in x:
        one_index = np.argmax(onehot) 
        s.append(indices_char[one_index]) 
    return ''.join(s)

def prepare_for_window(x):
    # All slices of size WINDOW_SIZE, sliding through x
    ind = [np.array(np.arange(i, i+WINDOW_SIZE)) for i in range(x.shape[0] - WINDOW_SIZE + 1)]
    ind = np.array(ind, dtype=np.int32)
    x_window = x[ind]
    # Reshape it back to a 2-d tensor
    return x_window.reshape(x_window.shape[0], x_window.shape[1]*x_window.shape[2])
    
def normalization_layer_set_weights(n_layer):
    wb = []
    w = np.zeros((WINDOW_SIZE*INPUT_VOCAB_SIZE, INPUT_VOCAB_SIZE))
    b = np.zeros((INPUT_VOCAB_SIZE))
    # Let lower case letters go through
    for c in string.ascii_lowercase:
        i = char_indices[c]
        w[INPUT_VOCAB_SIZE+i, i] = 1
    # Map capitals to lower case
    for c in string.ascii_uppercase:
        i = char_indices[c]
        il = char_indices[c.lower()]
        w[INPUT_VOCAB_SIZE+i, il] = 1
    # Map all non-letters to space
    sp_idx = char_indices[' ']
    non_letters = [c for c in list(characters) if c not in list(string.ascii_letters)]
    for c in non_letters:
        i = char_indices[c]
        w[INPUT_VOCAB_SIZE+i, sp_idx] = 1
    # Map single letters to space
    for c in non_letters:
        i = char_indices[c]
        w[i, sp_idx] = 0.75
        w[INPUT_VOCAB_SIZE*2+i, sp_idx] = 0.75

    wb.append(w)
    wb.append(b)
    n_layer.set_weights(wb)
    return n_layer

def build_model():
    # Normalize characters using a dense layer
    model = Sequential()
    model.add(Dense(INPUT_VOCAB_SIZE, 
                    input_shape=(WINDOW_SIZE*INPUT_VOCAB_SIZE,),
                    activation='softmax'))
    return model

model = build_model()
model.summary()
normalization_layer_set_weights(model.layers[0])

with open(sys.argv[1]) as f:
    for line in f:
        if line.isspace(): continue
        batch = prepare_for_window(encode_one_hot(line))
        preds = model.predict(batch)
        normal = decode_one_hot(preds)
        print(normal)