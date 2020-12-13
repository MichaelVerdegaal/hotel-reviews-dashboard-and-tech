from config import HOST, PORT, DATABASE_NAME
from pymongo import MongoClient
import pandas as pd


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
    """
    Inserts a dataframe into the database
    :param db: database object
    :param dataframe: pandas dataframe
    """
    try:
        db.collection.insert_many(dataframe.to_dict('records'))
    except Exception as e:
        print(f"Database error: {e}")


def query_all(db, count=0):
    """
    Queries all records from the database, optionally limiting results count
    Ref: https://stackoverflow.com/a/16255680/7174982
    :param db: database object
    :param count: amount of results to return, if not provided returns all results
    :return: dataframe
    """
    collection = db["collection"]
    query = {}
    if count > 0:
        cursor = collection.find(query, limit=count)
    else:
        cursor = collection.find(query)
    dataframe = pd.DataFrame(list(cursor))
    del dataframe['_id']
    return dataframe
