import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
KAGGLE_CSV = os.path.join(ROOT_DIR, "static/kaggle_reviews.csv")

PRELIMINARY_CLEAN_DF = "static/preliminary_clean_df.pickle"
CLEAN_DF = "static/cleaned_df.pickle"
LABELED_DF = "static/labeled_df.pickle"
YOUR_REVIEWS = "static/enter_your_reviews.xlsx"

# Unless you also use localhost, don't fill in your database credentials here.
# Create a separate config file with your credentials in that case.
HOST = "localhost"
PORT = 27017
