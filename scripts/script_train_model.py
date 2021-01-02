import datetime

from comet_ml import Experiment
from data.database import create_connection, query_all_limit
from data.model_util import *

if __name__ == '__main__':
    # comet.ml config
    experiment = Experiment(
        project_name="Hotel Neural Network",
        auto_metric_logging=True,
        auto_param_logging=True,
        auto_histogram_weight_logging=True,
        auto_histogram_gradient_logging=True,
        auto_histogram_activation_logging=True,
    )
    # Config
    data_size = 0
    max_words = 5000
    input_length = 200
    batch_size = 20000
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
    history = simple_RNN.fit(data_train,
                             label_train,
                             epochs=epochs,
                             batch_size=batch_size,
                             validation_data=(data_test, label_test))
    save_model(simple_RNN, f"simple_RNN_{datetime.datetime.now().strftime('%Y%m%d-%H%M')}.h5")
    print(simple_RNN.summary())
