from config import HOST, PORT
from pymongo import MongoClient


def create_connection():
    """
    Create database connection
    :return: connection object
    """
    try:
        client = MongoClient(HOST, PORT)
        database = client.reviews
        return database
    except Exception as e:
        print(f"Database error: {e}")
