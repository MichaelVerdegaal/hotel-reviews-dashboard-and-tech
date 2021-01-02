import os

# noinspection PyUnresolvedReferences
import comet_ml
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from config import ROOT_DIR
from data.file_util import pickle_object, read_pickled_object
from tensorflow.keras.metrics import Precision, Recall, AUC


def save_model(model, filename):
    """
    Saves a keras model as a file
    :param model: keras model
    :param filename: filename to save it at
    """
    filepath = os.path.join(ROOT_DIR, f"static/models/{filename}")
    model.save(filepath, overwrite=True)


def read_model(filename):
    """
    Reads a keras model from fiel
    :param filename: filename to read from
    :return: keras model
    """
    filepath = os.path.join(ROOT_DIR, f"static/{filename}")
    model = load_model(filepath)
    return model


def create_padded_sequences(data, max_words=5000, input_length=200, replace_tokenizer=True):
    """
    Encode a list of strings into number sequences, padded with zeros to always be a consistent length
    :param data: list of strings
    :param max_words: Maximum amount of words that the tokenizer can store
    :param input_length: How long the sequences should be
    :param replace_tokenizer: Whether to construct a new tokenizer or to read an already saved one
    :return: padded sequences
    """
    filepath = os.path.join(ROOT_DIR, f"static/tokenizer.pickle")
    if replace_tokenizer:
        tokenizer = Tokenizer(num_words=max_words)
        tokenizer.fit_on_texts(data)
        pickle_object(tokenizer, filepath)
    else:
        print("Reading tokenizer from file...\n")
        tokenizer = read_pickled_object(filepath)
    sequences = tokenizer.texts_to_sequences(data)
    padded_sequences = pad_sequences(sequences, maxlen=input_length)
    return padded_sequences


def split_train_test_np(padded_sequences, labels):
    """
    Splits data and labels into a train and test set, and converts it into a numpy array. A numpy array was chosen
    as a basic lists caused some issues in the input layer of the model.
    :param padded_sequences: List of padded sequences
    :param labels: Matching labels for the sequences
    :return: train and test sets
    """
    data_train, data_test, label_train, label_test = train_test_split(padded_sequences, labels, random_state=5)
    data_train = np.asarray(data_train)
    data_test = np.asarray(data_test)
    label_train = np.asarray(label_train)
    label_test = np.asarray(label_test)
    return data_train, data_test, label_train, label_test


def create_simple_rnn(max_words, input_length):
    """
    Create a basic recurrent neural network
    :param max_words: size of the vocabulary
    :param input_length: length of input sequences
    :return: Keras RNN
    """
    simple_RNN = Sequential()
    simple_RNN.add(layers.Embedding(max_words, 15, input_length=input_length))
    simple_RNN.add(layers.SimpleRNN(15))
    simple_RNN.add(layers.Dense(1, activation='sigmoid'))
    simple_RNN.compile(optimizer='rmsprop',
                       loss='binary_crossentropy',
                       metrics=['accuracy', Precision(), Recall(), AUC()])
    return simple_RNN
