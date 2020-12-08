###
# This file will change frequently until all the modules have been written, for testing purposes
###
from data.database import create_connection, query_all
from data.file_util import read_kaggle_reviews

db = create_connection()

df = read_kaggle_reviews()
c = query_all(db)
print(c)

