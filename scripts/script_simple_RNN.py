import os

import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

from config import ROOT_DIR
from data.database import *

if __name__ == '__main__':
    max_words = 5000
    input_length = 200

    # Prepare dataset
    db = create_connection()
    all_hotels = query_all_limit(db)
    all_hotels_filtered = all_hotels[['Review', 'Sentiment']]
    data = list(all_hotels_filtered['Review'].values)
    labels = list(all_hotels_filtered['Sentiment'].values)

    # Text encoding and padding
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(data)
    sequences = tokenizer.texts_to_sequences(data)
    padded_sequences = pad_sequences(sequences, maxlen=input_length)

    # Split data
    data_train, data_test, label_train, label_test = train_test_split(padded_sequences, labels, random_state=5)
    data_train = np.asarray(data_train)
    data_test = np.asarray(data_test)
    label_train = np.asarray(label_train)
    label_test = np.asarray(label_test)

    # Create model
    model = Sequential()
    model.add(layers.Embedding(max_words, 15, input_length=input_length))
    model.add(layers.SimpleRNN(15))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Train model
    history = model.fit(data_train,
                        label_train,
                        epochs=4,
                        batch_size=2500,
                        validation_data=(data_test, label_test))
    filepath = os.path.join(ROOT_DIR, "static/")
    model.save(filepath, save_format='tf')
    print(model.summary())
