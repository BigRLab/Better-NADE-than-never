from __future__ import print_function
from keras.layers import Dense, Activation, Reshape, Conv2D
from keras.models import Sequential
from keras import backend as K
from keras.utils import vis_utils


n_item = 10
hidden_size = 128
encoding_size = 64
n_rating = 5
n_hidden = 1


def cf_nade(n_item, n_rating, n_hidden, hidden_size, encoding_size):
    input_block = (
        Dense(encoding_size, input_shape=(n_item * n_rating,), use_bias=False),
        Dense(hidden_size),
        Activation('tanh')
    )
    hidden_block = n_hidden * (
        Dense(hidden_size, activation='tanh'),
    )
    output_block = (
        Dense(encoding_size, use_bias=False),
        Dense(n_item * n_rating),
        Reshape((n_rating, n_item, 1)),
        Conv2D(1, 1),
        Reshape((n_rating, n_item)),
        Activation('softmax')
    )
    nade = Sequential(input_block + hidden_block + output_block)
    nade.compile(optimizer='adam', loss='categorical_crossentropy')


if __name__ == '__main__':
    print (nade.summary())
    vis_utils.plot_model(nade, to_file='nade_model.png')
