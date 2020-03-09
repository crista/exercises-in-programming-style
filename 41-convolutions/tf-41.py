from keras.models import Sequential, Model
from keras.layers import Conv2D, ReLU, Lambda, Reshape
from keras import backend as K
import numpy as np
import string, re, collections, os, sys, operator, math

stopwords = set(open('../stop_words.txt').read().split(','))
all_words = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
words = [w for w in all_words if w not in stopwords]

uniqs = [''] + list(set(words))
uniqs_indices = dict((w, i) for i, w in enumerate(uniqs))
indices_uniqs = dict((i, w) for i, w in enumerate(uniqs))

indices = [uniqs_indices[w] for w in words]

WORDS_SIZE = len(words)
VOCAB_SIZE = len(uniqs)
BIN_SIZE = math.ceil(math.log(VOCAB_SIZE, 2))
print(f'Words size {WORDS_SIZE}, vocab size {VOCAB_SIZE}, bin size {BIN_SIZE}')

def encode_binary(W):
    x = np.zeros((1, WORDS_SIZE, BIN_SIZE, 1))
    for i, w in enumerate(W):
        for n in range(BIN_SIZE): 
            n2 = pow(2, n)
            x[0, i, n, 0] = 1 if (w & n2) == n2 else 0
    return x

def conv_layer_set_weights(clayer):
    wb = []
    b = np.zeros((VOCAB_SIZE), dtype=np.float32)
    w = np.zeros((1, BIN_SIZE, 1, VOCAB_SIZE), dtype=np.float32)
    for i in range(VOCAB_SIZE):
        for n in range(BIN_SIZE):
            n2 = pow(2, n)
            w[0][n][0][i] = 1 if (i & n2) == n2 else -1 #-(BIN_SIZE-1)
    for i in range(VOCAB_SIZE):
        slice_1 = w[0, :, 0, i]
        n_ones = len(slice_1[ slice_1 == 1 ])
        if n_ones > 0: slice_1[ slice_1 == 1 ] = 1./n_ones 
        n_ones = len(slice_1[ slice_1 == -1 ])
        if n_ones > 0: slice_1[ slice_1 == -1 ] = -1./n_ones 
    wb.append(w)
    wb.append(b)
    clayer.set_weights(wb)

def SumPooling2D(x):
    return K.sum(x, axis = 1) 

def build_model():
    model = Sequential()
    model.add(Conv2D(VOCAB_SIZE, (1, BIN_SIZE),  input_shape=(WORDS_SIZE, BIN_SIZE, 1)))
    model.add(ReLU(threshold=1-1/BIN_SIZE))
    model.add(Lambda(SumPooling2D))
    model.add(Reshape((VOCAB_SIZE,)))

    return model

model = build_model()
model.summary()
conv_layer_set_weights(model.layers[0])

batch_x = encode_binary(indices)
preds = model.predict(batch_x)
prediction = preds[0] 
 
for w, c in sorted(list(zip(uniqs, prediction)), key = operator.itemgetter(1), reverse=True)[:25]:
    print(w, "-", c)

