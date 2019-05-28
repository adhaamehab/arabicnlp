# -*- coding: utf-8 -*-

import pickle
import re
from itertools import chain
from os import path
from pickle import loads
import pkg_resources

import keras
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences


def _ignore_class_accuracy(to_ignore=0):
    def ignore_accuracy(y_true, y_pred):
        y_true_class = K.argmax(y_true, axis=-1)
        y_pred_class = K.argmax(y_pred, axis=-1)

        ignore_mask = K.cast(K.not_equal(y_pred_class, to_ignore), 'int32')
        matches = K.cast(K.equal(y_true_class, y_pred_class), 'int32') * ignore_mask
        accuracy = K.sum(matches) / K.maximum(K.sum(ignore_mask), 1)
        return accuracy
    return ignore_accuracy

def _logits_to_tokens(sequences, index):
    token_sequences = []
    for categorical_sequence in sequences:
            token_sequence = []
            for categorical in categorical_sequence:
                    token_sequence.append(index[np.argmax(categorical)])

            token_sequences.append(token_sequence)

    return token_sequences

    ## One-Hot Encoded tags
def to_categorical(sequences, categories):
    cat_sequences = []
    for s in sequences:
        cats = []
        for item in s:
            cats.append(np.zeros(categories))
            cats[-1][item] = 1.0
        cat_sequences.append(cats)
    return np.array(cat_sequences)

def _string_to_sequence(string):
    s_int = []
    for w in _tokens(string):
        try:
            s_int.append(word2index[w.lower()])
        except KeyError:
            s_int.append(word2index['-OOV-'])
    return pad_sequences([s_int], maxlen=_MAX_LENGTH, padding='post')

def _tokens(text):
    r = re.compile(r'\w+|[^\w\s]+', re.UNICODE | re.MULTILINE | re.DOTALL)
    return r.findall(text)

this_dir, this_filename = path.split(__file__)
MODEL_PATH = path.join(this_dir, "data", "post_lstm_march_2019_.h5")
WORDINDEX_PATH = path.join(this_dir, "data", "word2index.bin")
TAGINDEX_PATH = path.join(this_dir, "data", "tag2index.bin")


model = load_model(MODEL_PATH, custom_objects={'ignore_accuracy': _ignore_class_accuracy()})
global graph
graph = tf.get_default_graph() 

with open(WORDINDEX_PATH, 'rb') as f:
    word2index = pickle.load(f)

with open(TAGINDEX_PATH, 'rb') as f:
    tag2index = pickle.load(f)



_MAX_LENGTH = 398 # check the training article


def tags( sentence):
    predictions = model.predict(_string_to_sequence(sentence))
    pre_result = _logits_to_tokens(predictions, {i: t for t, i in tag2index.items()})[0]
    result = {}
    for idx, value in enumerate(_tokens(sentence)):
        if pre_result[idx] == '-PAD-':
            break
        result[value] = pre_result[idx]
    return result
