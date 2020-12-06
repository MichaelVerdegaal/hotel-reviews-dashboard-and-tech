import os
import re

import nltk
import pandas as pd
from langdetect import detect
from textblob import TextBlob
from config import ROOT_DIR
from data.file_util import (read_scraped_reviews, read_kaggle_reviews, read_manual_reviews, file_exists,
                            read_pickled_dataframe, pickle_dataframe)

usable_column_list = ["Hotel_Address", "Average_Score", "Hotel_Name", "Reviewer_Nationality", "Negative_Review",
                      "Positive_Review", "Reviewer_Score"]

print("\nDownloading nltk libraries...")
nltk.download('stopwords')
nltk.download('wordnet')
lst_stopwords = nltk.corpus.stopwords.words("english")


def process_scraped_reviews(reviews=read_scraped_reviews()):
    """
    Processes the scraped reviews so it can be successfully merged
    :param reviews: multi dimensional list of reviews
    :return: dataframe
    """
    df = pd.DataFrame(reviews, columns=usable_column_list)
    df.transpose()
    df['Average_Score'] = df['Average_Score'].astype('float64')
    df['Reviewer_Score'] = df['Reviewer_Score'].astype('float64')
    return df


def merge_dataframes(df1, df2):
    """
    Merges two dataframes together
    :param df1: first dataframe
    :param df2: second dataframe
    :return: merged dataframe
    """
    new_df = pd.merge(df1[usable_column_list],
                      df2[usable_column_list],
                      on=usable_column_list,
                      how='outer')
    return new_df


def get_all_review_sources():
    """
    Master function to get all available dataframes from their respective sources
    :return: 3 dataframes
    """
    kaggle_df = read_kaggle_reviews()[usable_column_list]
    manual_df = read_manual_reviews()
    scraped_df = process_scraped_reviews()
    return kaggle_df, manual_df, scraped_df


def get_combined_review_df():
    """
    Executes all other functions in this file to return 1 dataframe filled with reviews
    :return: dataframe
    """
    kaggle_df, manual_df, scraped_df = get_all_review_sources()
    final_df = merge_dataframes(kaggle_df, manual_df)
    final_df = merge_dataframes(final_df, scraped_df)
    return final_df


def is_en(text):
    """
    If a string is in english or not
    :param text: string
    :return: boolean
    """
    try:
        if text == "" or text is None:
            return False
        langcode = detect(text)
        # Portugal code is included because it incorrectly detects some english text as portuguese
        return langcode in ['en', 'ca', 'pt']
    except:
        return False


def pre_process_text(text):
    """
    Cleans the text of unnecessary features
    :param text: string
    :return: cleaned string
    """
    # Cconvert to lowercase, remove punctuations and unneeded characters, then strip
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())

    # Tokenize
    lst_text = text.split()
    # Remove Stopwords
    lst_text = [word for word in lst_text if word not in lst_stopwords]

    # Lemmatisation (convert the word into root word)
    lem = nltk.stem.wordnet.WordNetLemmatizer()
    lst_text = [lem.lemmatize(word) for word in lst_text]

    # Rejoin tokenized string
    text = " ".join(lst_text)
    return text


def label_sentiment(df):
    """
    Adds a new column to the dataframe, labeling the sentiment of the reviews using TextBlob PatternAnalyzer
    :param df: dataframe
    :return: dataframe
    """
    def return_sentiment(text):
        """
        Judges sentiment of string, 1 being positive, and 0 being negative
        :param text: string
        :return: 1 or 0
        """
        obj = TextBlob(str(text))
        return 1 if obj.polarity >= 0 else 0

    filepath = os.path.join(ROOT_DIR, "static/labeled_df.pickle")
    if file_exists(filepath):
        return read_pickled_dataframe(filepath)
    else:
        df['Sentiment'] = df['Review'].apply(return_sentiment)
        pickle_dataframe(df, filepath)
        print(f"\nWritten reviews to {filepath}!")
        return df


def preliminary_clean(df):
    """
    Perform early cleaning to allow for labeling
    :param df: dataframe
    :return: dataframe
    """
    filepath = os.path.join(ROOT_DIR, "static/preliminary_clean_df.pickle")
    if file_exists(filepath):
        return read_pickled_dataframe(filepath)
    else:
        print("\nMerging columns...")
        df['Review_Original'] = df['Positive_Review'] + ' ' + df['Negative_Review']
        df = df.drop('Positive_Review', 1)
        df = df.drop('Negative_Review', 1)

        print("\nRemoving non-english reviews...")
        df = df[df['Review_Original'].apply(lambda x: is_en(x))]
        pickle_dataframe(df, filepath)
        print(f"\nWritten reviews to {filepath}!")
        return df


def clean_df_text(df):
    """
    clean review column
    :param df: dataframe
    :return: dataframe
    """
    filepath = os.path.join(ROOT_DIR, "static/cleaned_df.pickle")
    if file_exists(filepath):
        return read_pickled_dataframe(filepath)
    else:
        print("\nPre-processing text...")
        df['Review'] = df['Review_Original'].apply(pre_process_text)

        pickle_dataframe(df, filepath)
        print(f"\nWritten reviews to {filepath}!")
        return df


