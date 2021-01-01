import datetime

import tensorflow as tf

from data.database import create_connection, query_all_limit
from data.model_util import *

if __name__ == '__main__':
    # Config
    log_dir = os.path.join(ROOT_DIR, "static/logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M"))
    data_size = 0
    max_words = 5000
    input_length = 200
    batch_size = 10000
    epochs = 2

    # Prepare dataset
    db = create_connection()
    all_hotels = query_all_limit(db, data_size)[['Review', 'Sentiment']]
    data = list(all_hotels['Review'].values)  # We want a list instead of a series object since it's easier to work with
    labels = list(all_hotels['Sentiment'].values)

    # Text encoding and padding
    padded_sequences = create_padded_sequences(data, max_words, input_length, replace_tokenizer=True)

    # Split data
    data_train, data_test, label_train, label_test = split_train_test_np(padded_sequences, labels)

    # Create model
    simple_RNN = create_simple_rnn(max_words, input_length)

    # Train model
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, update_freq='batch', histogram_freq=1)
    history = simple_RNN.fit(data_train,
                             label_train,
                             epochs=epochs,
                             batch_size=batch_size,
                             validation_data=(data_test, label_test),
                             callbacks=[tensorboard_callback])
    save_model(simple_RNN, f"simple_RNN_{datetime.datetime.now().strftime('%Y%m%d-%H%M')}.h5")
    print(simple_RNN.summary())
