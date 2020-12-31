from data.database import create_connection, query_all_limit
from data.model_util import *

if __name__ == '__main__':
    # Config
    data_size = 20000
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
    simple_RNN = create_simple_rnn(max_words, input_length)

    # Train model
    history = simple_RNN.fit(data_train,
                             label_train,
                             epochs=4,
                             batch_size=2500,
                             validation_data=(data_test, label_test))
    save_model(simple_RNN, "simple_RNN.h5")
    print(simple_RNN.summary())
