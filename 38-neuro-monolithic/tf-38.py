from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import sys, os, string

characters = string.printable
char_indices = dict((c, i) for i, c in enumerate(characters))
indices_char = dict((i, c) for i, c in enumerate(characters))

INPUT_VOCAB_SIZE = len(characters)
LINE_SIZE = 80

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
    
def normalization_layer_set_weights(n_layer):
    wb = []
    w = np.zeros((LINE_SIZE*INPUT_VOCAB_SIZE, LINE_SIZE*INPUT_VOCAB_SIZE))
    b = np.zeros((LINE_SIZE*INPUT_VOCAB_SIZE))
    for r in range(0, LINE_SIZE*INPUT_VOCAB_SIZE, INPUT_VOCAB_SIZE):
        # Let lower case letters go through
        for c in string.ascii_lowercase:
            i = char_indices[c]
            w[r+i, r+i] = 1
        # Map capitals to lower case
        for c in string.ascii_uppercase:
            i = char_indices[c]
            il = char_indices[c.lower()]
            w[r+i, r+il] = 1
        # Map all non-letters to space
        sp_idx = char_indices[' ']
        for c in [c for c in list(string.printable) if c not in list(string.ascii_letters)]:
            i = char_indices[c]
            w[r+i, r+sp_idx] = 1
        # Map single letters to space
        previous_c = r-INPUT_VOCAB_SIZE
        next_c = r+INPUT_VOCAB_SIZE
        for c in [c for c in list(string.printable) if c not in list(string.ascii_letters)]:
            i = char_indices[c]
            if r > 0 and r < (LINE_SIZE-1)*INPUT_VOCAB_SIZE: 
                w[previous_c+i, r+sp_idx] = 0.75
                w[next_c+i, r+sp_idx] = 0.75
            if r == 0:
                w[next_c+i, r+sp_idx] = 1.5
            if r == (LINE_SIZE-1)*INPUT_VOCAB_SIZE:
                w[previous_c+i, r+sp_idx] = 1.5

    wb.append(w)
    wb.append(b)
    n_layer.set_weights(wb)
    return n_layer

def build_model():
    # Normalize characters using a dense layer
    model = Sequential()
    model.add(Dense(LINE_SIZE*INPUT_VOCAB_SIZE, 
                    input_shape=(LINE_SIZE*INPUT_VOCAB_SIZE,),
                    activation='sigmoid'))
    return model

model = build_model()
model.summary()
normalization_layer_set_weights(model.layers[0])

with open(sys.argv[1]) as f:
    for line in f:
        if line.isspace(): continue
        batch = encode_one_hot(line)
        preds = model.predict(batch)
        normal = decode_one_hot(preds)
        print(normal)