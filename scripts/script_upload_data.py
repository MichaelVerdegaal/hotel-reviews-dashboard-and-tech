from data.database import create_connection, df_to_db
from data.file_util import read_clean_reviews

if __name__ == '__main__':
    """
    This script reads the cleaned and labeled data, and uploads it to the connected mongodb database.
    """
    reviews = read_clean_reviews()
    db = create_connection()
    df_to_db(db, reviews)
