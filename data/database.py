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


def query_where_hotel(db, hotel_name):
    """
    Queries all records from the database from a specific hotel
    :param db: database object
    :param hotel_name: name of hotel to select from
    :return: dataframe
    """
    collection = db["collection"]
    pipeline = [
        {
            u"$match": {
                u"Hotel_Name": hotel_name
            }
        }
    ]
    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=True
    )
    # Ref: https://stackoverflow.com/a/16255680/7174982
    dataframe = pd.DataFrame(list(cursor))
    return dataframe


def query_hotels(db):
    """
    Queries all hotels from the database
    Ref: https://stackoverflow.com/a/16255680/7174982
    :param db: database object
    :return: dataframe
    """
    collection = db["collection"]
    pipeline = [
        {
            u"$group": {
                u"_id": u"$Hotel_Name",
                u"user": {
                    u"$first": u"$$ROOT"
                },
                u"count": {
                    u"$sum": 1.0
                }
            }
        },
        {
            u"$replaceRoot": {
                u"newRoot": {
                    u"$mergeObjects": [
                        {
                            u"count": u"$count"
                        },
                        u"$user"
                    ]
                }
            }
        }
    ]
    cursor = collection.aggregate(
        pipeline,
        allowDiskUse=True
    )
    dataframe = pd.DataFrame(list(cursor))
    return dataframe
