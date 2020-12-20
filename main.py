###
# This file will change frequently until all the modules have been written, for testing purposes
###
from config import MBTOKEN
from data.database import *
from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound
from data.dataframes import df_to_geojson, read_geojson

# Data
db = create_connection()
all_hotels = query_hotels(db)
df_to_geojson(all_hotels)
geojson = read_geojson()

# Flask
app = Flask(__name__, template_folder='templates', static_folder='static')


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


if __name__ == "__main__":
    app.run(debug=True, port=1205)
