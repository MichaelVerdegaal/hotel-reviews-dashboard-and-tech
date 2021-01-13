import os

# noinspection PyUnresolvedReferences
import comet_ml
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.callbacks import Callback
from tensorflow.python.keras.utils.np_utils import to_categorical

from config import ROOT_DIR
from data.file_util import pickle_object, read_pickled_object
from tensorflow.keras.metrics import Precision, Recall, AUC
from tensorflow_addons.metrics import F1Score, FBetaScore


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


def create_simple_rnn(max_words, output_dim, input_length):
    """
    Create a basic recurrent neural network
    :param max_words: size of the vocabulary
    :param input_length: length of input sequences
    :param output_dim: dimension size of the output
    :return: Keras RNN model
    """
    simple_RNN = Sequential()
    simple_RNN.add(layers.Embedding(max_words, output_dim, input_length=input_length))
    simple_RNN.add(layers.SimpleRNN(output_dim, dropout=0.1))
    simple_RNN.add(layers.Dense(1, activation='sigmoid'))
    simple_RNN.compile(optimizer='rmsprop',
                       loss='binary_crossentropy',
                       metrics=[Precision(), Recall()])
    return simple_RNN


def create_lstm(max_words, output_dim, input_length):
    """
    Create a basic recurrent neural network
    :param max_words: size of the vocabulary
    :param input_length: length of input sequences
    :param output_dim: dimension size of the output
    :return: Keras LSTM model
    """
    LSTM = Sequential()
    LSTM.add(layers.Embedding(max_words, output_dim, input_length=input_length))
    LSTM.add(layers.LSTM(output_dim))
    LSTM.add(layers.Dense(1, activation='sigmoid'))
    LSTM.compile(optimizer='rmsprop',
                 loss='binary_crossentropy',
                 metrics=[Precision(), Recall()])
    return LSTM


def create_gru(max_words, output_dim, input_length):
    """
    Create a basic recurrent neural network
    :param max_words: size of the vocabulary
    :param input_length: length of input sequences
    :param output_dim: dimension size of the output
    :return: Keras GRU model
    """
    GRU = Sequential()
    GRU.add(layers.Embedding(max_words, output_dim, input_length=input_length))
    GRU.add(layers.GRU(output_dim))
    GRU.add(layers.Dense(1, activation='sigmoid'))
    GRU.compile(optimizer='rmsprop',
                loss='binary_crossentropy',
                metrics=[Precision(), Recall()])
    return GRU


class ConfusionMatrixCallback(Callback):
    """
    comet.ml callback for keras, to create a confusion matrix per epoch
    Reference: https://www.comet.ml/site/debugging-classifiers-with-confusion-matrices/
    """

    def __init__(self, experiment, inputs, targets, cutoff=0.5):
        self.experiment = experiment
        self.inputs = inputs
        self.cutoff = cutoff
        self.targets = targets
        self.targets_reshaped = to_categorical(self.targets)

    def on_epoch_end(self, epoch, logs={}):
        predicted = self.model.predict(self.inputs)
        predicted = np.where(predicted < self.cutoff, 0, 1)

        predicted_reshaped = to_categorical(predicted)
        self.experiment.log_confusion_matrix(
            self.targets_reshaped,
            predicted_reshaped,
            title="Confusion Matrix, Epoch #%d" % (epoch + 1),
            file_name="confusion-matrix-%03d.json" % (epoch + 1),
        )
