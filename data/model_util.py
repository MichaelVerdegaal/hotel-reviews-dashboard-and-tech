from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np


def create_padded_sequences(max_words, input_length, data):
    """
    Encode a list of strings into number sequences, padded with zeros to always be a consistent length
    :param max_words: Maximum amount of words that the tokenizer can store
    :param input_length: How long the sequences should be
    :param data: list of strings
    :return: padded sequences
    """
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(data)
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
