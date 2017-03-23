'''Cf-Nade recommender System
'''
from tensorflow import Variable
import tensorflow as tf
from tensorflow import nn
import numpy as np

n_user = 1
n_item = 5
hidden_size = 10

X = np.array([[2, 0, 0, 0, 5]], dtype=tf.int32)
y = np.array([[]])


R = tf.placeholder()
W = Variable(shape=(n_item, hidden_size), name='W', dtype=tf.float32)
c = Variable(shape=(1, hidden_size), name='c', dtype=tf.float32)

V = Variable(shape=(hidden_size, n_item), name='V', dtype=tf.float32)
b = Variable(shape=(1, n_item), name='b', dtype=tf.float32)

embedded_vectors  = nn.embedding_lookup(W, R)
vector_sum = tf.reduce_sum(lookup, axis=0)
h = tf.tanh(c + vector_sum)
p = nn.softmax(b + V * h)

cost = nn.cross_entropy(p, y)
