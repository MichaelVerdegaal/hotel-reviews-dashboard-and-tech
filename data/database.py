from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
import pandas as pd
from config import HOST, USERNAME, PASSWORD, DATABASE


def create_connection():
    """
    Create database connection
    :return: connection object
    """
    try:
        # Take not that you'll HAVE TO set your database charset to utf8mb4, otherwise you'll not be able to call
        # df_to_db(), due to encoding issues
        engine = create_engine(f"mysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}?charset=utf8mb4")
        connection = engine.connect()
        return connection
    except DatabaseError as e:
        print(f"Database error: {e}")


def df_to_db(df, connection=create_connection()):
    """
    Transfers the review dataframe to the connected database
    :param df: dataframe
    :param connection: connection object
    """
    df.to_sql("reviews", connection, if_exists='replace', index=True)


def db_to_df(amount, connection=create_connection()):
    """
    Transfer results of a SQL query to a dataframe
    :param amount: limit amount of entries returned
    :param connection: connection object
    :return: dataframe
    """
    query = pd.read_sql(f"CALL select_reviews(%(amount)s)", connection, params={"amount": amount})
    df = pd.DataFrame(query)
    return df
