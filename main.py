###
# This file will change frequently until all the modules have been written, for testing purposes
###
from config import MBTOKEN
from data.database import *
from data.dataframes import create_marker_label_data
from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound

# Data
db = create_connection()
all_hotels = query_hotels(db)

# Map data
customdata = create_marker_label_data(all_hotels)

# Flask
app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def homepage():
    try:
        return render_template('homepage.html', token=MBTOKEN)
    except TemplateNotFound:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True, port=656565)
