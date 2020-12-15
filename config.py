import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
KAGGLE_CSV = os.path.join(ROOT_DIR, "static/kaggle_reviews.csv")

CLEAN_DF = "static/cleaned_df.pickle"
YOUR_REVIEWS = "static/enter_your_reviews.xlsx"

# Unless you also use localhost, don't fill in your database credentials here.
# Create a separate config file with your credentials in that case.
HOST = "localhost"
DATABASE_NAME = "reviews"
PORT = 27017

# Mapbox access token
MBTOKEN = os.environ.get('MBTOKEN')