###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.database import create_connection, df_to_db
from data.file_util import read_kaggle_reviews

db = create_connection()

df = read_kaggle_reviews()
df_to_db(db, df)

