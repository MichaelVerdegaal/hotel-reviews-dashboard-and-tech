import pickle

import pandas as pd

from config import *


def pickle_object(object_to_dump, filepath):
    """
    Pickled and writes an object to a file as long as the file doesn't exist
    :param object_to_dump: object that will be written
    :param filepath: where the file is
    """
    if file_exists(filepath):
        pass
    else:
        with open(filepath, 'wb') as f:
            pickle.dump(object_to_dump, f)


def read_pickled_object(filepath):
    """
    Reads from a file and unpickles the stored object
    :param filepath: where the file is
    :return: unpickled object
    """
    with open(filepath, 'rb') as f:
        try:
            unpickled_object = pickle.load(f)
            return unpickled_object
        except pickle.UnpicklingError as e:
            raise e


def pickle_dataframe(dataframe, filepath):
    """
    Pickled and writes an object to a file as long as the file doesn't exist
    :param dataframe: dataframe that will be written
    :param filepath: where the file is
    """
    if file_exists(filepath):
        pass
    else:
        dataframe.to_pickle(filepath)


def read_pickled_dataframe(filepath):
    """
    Unpickles saved dataframe
    :param filepath: where the file is
    :return:
    """
    return pd.read_pickle(filepath)


def file_exists(filepath):
    """
    Check if a file exists
    :param filepath: filepath as string
    :return: boolean
    """
    return os.path.isfile(filepath)


def read_kaggle_reviews():
    """
    Reads the kaggle reviews file
    :return: dataframe
    """
    kaggle_df = pd.read_csv(KAGGLE_CSV)
    return kaggle_df


def read_precleaned_reviews():
    """
    Reads reviews that had some prior cleaning
    :return: dataframe
    """
    filepath = os.path.join(ROOT_DIR, PRELIMINARY_CLEAN_DF)
    return read_pickled_dataframe(filepath)


def read_clean_reviews():
    """
    Reads reviews that were cleaned
    :return: dataframe
    """
    filepath = os.path.join(ROOT_DIR, CLEAN_DF)
    return read_pickled_dataframe(filepath)


def read_labeled_reviews():
    """
    Reads reviews that were labeled
    :return: dataframe
    """
    filepath = os.path.join(ROOT_DIR, LABELED_DF)
    return read_pickled_dataframe(filepath)


def read_your_reviews():
    """
    Reads reviews from the excel file which you can easily edit
    :return: dataframe
    """
    filepath = os.path.join(ROOT_DIR, YOUR_REVIEWS)
    return pd.read_excel(filepath)
