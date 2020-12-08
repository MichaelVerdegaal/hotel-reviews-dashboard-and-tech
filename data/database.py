from config import HOST, PORT, DATABASE_NAME
from pymongo import MongoClient


def create_connection():
    """
    Create database connection
    :return: connection object
    """
    try:
        client = MongoClient(HOST, PORT)
        database = client[DATABASE_NAME]
        return database
    except Exception as e:
        print(f"Database error: {e}")


def df_to_db(db, dataframe):
    try:
        db.collection.insert_many(dataframe.to_dict('records'))
    except Exception as e:
        print(f"Database error: {e}")