import os

from config import ROOT_DIR
from data.database import *
from data.model_util import create_padded_sequences, split_train_test_np, create_simple_rnn

if __name__ == '__main__':
    # Config
    data_size = 5000
    max_words = 5000
    input_length = 200

    # Prepare dataset
    db = create_connection()
    all_hotels = query_all_limit(db, data_size)[['Review', 'Sentiment']]
    data = list(all_hotels['Review'].values)  # We want a list instead of a series object since it's easier to work with
    labels = list(all_hotels['Sentiment'].values)

    # Text encoding and padding
    padded_sequences = create_padded_sequences(max_words, input_length, data)

    # Split data
    data_train, data_test, label_train, label_test = split_train_test_np(padded_sequences, labels)

    # Create model
    model = create_simple_rnn(max_words, input_length)

    # Train model
    history = model.fit(data_train,
                        label_train,
                        epochs=4,
                        batch_size=2500,
                        validation_data=(data_test, label_test))
    filepath = os.path.join(ROOT_DIR, "static/")
    model.save(filepath, save_format='tf')
    print(model.summary())
