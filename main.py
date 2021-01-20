###
# This file will change frequently until all the modules have been written, for testing purposes
###
from config import MBTOKEN
from data.database import *
from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound
from data.dataframes import df_to_geojson, read_geojson, clean_manual_review
from data.model_util import *
import json

# Data
db = create_connection()
all_hotels = query_hotels(db)
df_to_geojson(all_hotels)
geojson = read_geojson()

# Flask
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load neural networks
simple_RNN = read_model("/models/2021_01_11-09_36 simple_RNN/Epoch-12_ValLoss-0.1656.h5")
LSTM = read_model("/models/2021_01_12-00_44 LSTM/Epoch-07_ValLoss-0.1581.h5")
GRU = read_model("/models/2021_01_12-10_20 GRU/Epoch-08_ValLoss-0.1585.h5")


@app.route('/')
def homepage():
    try:
        return render_template('homepage.html', token=MBTOKEN, hotels=geojson)
    except TemplateNotFound:
        abort(404)


@app.route('/hotel/<string:hotel_name>')
def ajax_hotel(hotel_name):
    reviews = query_where_hotel(db, hotel_name)
    reviews['Sentiment'] = reviews['Sentiment'].apply(lambda x: "Positive" if x == 1 else "Negative")
    review_json = reviews.to_json(orient='records', default_handler=str)
    return review_json


@app.route('/judge/<string:raw_review>')
def ajax_judge_sentiment(raw_review):
    processed_reviews = clean_manual_review([raw_review])
    data = list(processed_reviews['Review'].values)
    padded_sequences = create_padded_sequences(data=data, replace_tokenizer=False)

    RNN_confidence = round(simple_RNN.predict(padded_sequences).item(0), 5)
    RNN_labeled = "Positive" if (simple_RNN.predict(padded_sequences) > 0.5).astype("int32") == 1 else "Negative"

    LSTM_confidence = round(LSTM.predict(padded_sequences).item(0), 5)
    LSTM_labeled = "Positive" if (LSTM.predict(padded_sequences) > 0.5).astype("int32") == 1 else "Negative"

    GRU_confidence = round(GRU.predict(padded_sequences).item(0), 5)
    GRU_labeled = "Positive" if (GRU.predict(padded_sequences) > 0.5).astype("int32") == 1 else "Negative"

    scores = {'RNN': [RNN_confidence, RNN_labeled],
              'LSTM': [LSTM_confidence, LSTM_labeled],
              'GRU': [GRU_confidence, GRU_labeled]}
    return json.dumps(scores)


if __name__ == "__main__":
    app.run(debug=False, port=1205, use_reloader=False)
