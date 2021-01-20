import datetime

from comet_ml import Experiment
from data.database import create_connection, query_all_limit
from data.model_util import *
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import f1_score

if __name__ == '__main__':
    """
    This is the general script used to train our Recurrent Neural Networks. To use, make sure you've set your comet.ml
    API key as an environment variable. Lastly, tweak the config variables to your liking, and run the file.
    """

    # Enable this line if you cant run the code on your gpu.
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

    # comet.ml config
    experiment = Experiment(
        project_name="Hotel Neural Network",
        auto_histogram_weight_logging=True,
        auto_histogram_gradient_logging=True,
        auto_histogram_activation_logging=True,
    )

    # General config
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M')
    checkpoint_filepath = os.path.join(ROOT_DIR, (f'static/models/{timestamp}/' +
                                                  'Epoch-{epoch:02d}_ValLoss-{val_loss:.4f}.h5'))

    # Model config
    data_size = 0
    max_words = 5000
    out_put_dim = 150
    input_length = 200
    batch_size = 1028
    epochs = 50
    patience_level = 5

    # Prepare dataset
    db = create_connection()
    all_hotels = query_all_limit(db, data_size)[['Review', 'Sentiment']]
    print(f"Sentiment class distribution is: \n{all_hotels['Sentiment'].value_counts()}\n")
    data = list(all_hotels['Review'].values)  # We want a list instead of a series object since it's easier to work with
    labels = list(all_hotels['Sentiment'].values)

    # Text encoding and padding
    padded_sequences = create_padded_sequences(data, max_words, input_length, replace_tokenizer=True)

    # Split data
    data_train, data_test, label_train, label_test = split_train_test_np(padded_sequences, labels)

    # Create model
    # model = create_simple_rnn(max_words, out_put_dim, input_length)
    model = create_lstm(max_words, out_put_dim, input_length)
    # model = create_gru(max_words, out_put_dim, input_length)


    # Callbacks
    callbacks = []
    callbacks.append(EarlyStopping(monitor='val_loss', mode='min', patience=patience_level, verbose=1))
    callbacks.append(ModelCheckpoint(filepath=checkpoint_filepath,
                                     monitor='val_loss',
                                     save_best_only=True,
                                     mode='min',
                                     save_freq='epoch',
                                     verbose=1))
    # disable confusion matrix callback if not needed, as it slows down performance a lot
    # callbacks.append(ConfusionMatrixCallback(experiment, data_test, label_test))

    # Train model
    training_results = model.fit(data_train,
                                 label_train,
                                 epochs=epochs,
                                 batch_size=batch_size,
                                 validation_data=(data_test, label_test),
                                 callbacks=callbacks,
                                 use_multiprocessing=True)

    # Upload custom metrics
    test_pred = (model.predict(data_test) > 0.5).astype("int32")
    f1_score = f1_score(label_test, test_pred)
    experiment.log_metrics({'val_f1_score': f1_score})
