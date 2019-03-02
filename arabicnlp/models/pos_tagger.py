# -*- coding: utf-8 -*-

from itertools import chain

import keras
import numpy as np
import pandas as pd
from keras import backend as K
from keras.layers import (LSTM, Activation, Bidirectional, Dense, Embedding,
                          InputLayer, TimeDistributed)
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split


class POSTagger:

    def __init__(self):
        pass

    def tags(self, sentence):
        pass

    def retrain(self):
        pass
    
