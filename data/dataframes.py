import json
import os
import re

import geojson
import nltk
import pandas as pd

from config import ROOT_DIR
from data.file_util import file_exists, read_pickled_dataframe, pickle_dataframe


def pre_process_text(text):
    """
    Cleans the text of unnecessary features
    :param text: string
    :return: cleaned string
    """
    print("\nDownloading nltk libraries...")
    nltk.download('stopwords')
    nltk.download('wordnet')
    lst_stopwords = nltk.corpus.stopwords.words("english")

    # Convert to lowercase, remove punctuations and unneeded characters, then strip
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


def clean_and_label(df):
    """
    Explodes negative and positive review columns into 2 rows and labels the sentiment at the same time, then cleans
    the text.
    :param df: dataframe
    :return: dataframe
    """
    filepath = os.path.join(ROOT_DIR, "static/cleaned_df.pickle")
    if file_exists(filepath):
        return read_pickled_dataframe(filepath)
    else:
        print("\nSplitting columns...")
        df_size = len(df)
        columns = ['Hotel_Address', 'Review_Date', 'Average_Score', 'Hotel_Name', 'Reviewer_Nationality',
                   'Reviewer_Score', 'lat', 'lng', 'Review', 'Sentiment']
        row_list = []

        for index, row in df.iterrows():
            print(f"Splitting row {index}//{df_size}")
            row1 = {'Hotel_Address': row['Hotel_Address'],
                    'Review_Date': row['Review_Date'],
                    'Average_Score': row['Average_Score'],
                    'Hotel_Name': row['Hotel_Name'],
                    'Reviewer_Nationality': row['Reviewer_Nationality'],
                    'Reviewer_Score': row['Reviewer_Score'],
                    'lat': row['lat'],
                    'lng': row['lng'],
                    'Review': row['Positive_Review'],
                    'Sentiment': 1}

            row2 = {'Hotel_Address': row['Hotel_Address'],
                    'Review_Date': row['Review_Date'],
                    'Average_Score': row['Average_Score'],
                    'Hotel_Name': row['Hotel_Name'],
                    'Reviewer_Nationality': row['Reviewer_Nationality'],
                    'Reviewer_Score': row['Reviewer_Score'],
                    'lat': row['lat'],
                    'lng': row['lng'],
                    'Review': row['Negative_Review'],
                    'Sentiment': 0}
            row_list.append(row1)
            row_list.append(row2)
        new_df = pd.DataFrame(row_list, columns=columns)

        print("\nPre-processing text...")
        new_df['Review'] = new_df['Review'].apply(pre_process_text)

        print("\nDropping reviews with custom stop-words...")
        # Custom stop-words based on manual observation of the data
        custom_stop_words = ['negative', 'nothing', 'positive', 'n']
        new_df = new_df[~new_df['Review'].isin(custom_stop_words)]

        print(f"\nWritten reviews to {filepath}!")
        pickle_dataframe(new_df, filepath)
        return new_df


def df_to_geojson(df):
    """
    Writes a dataframe to geojson.
    :param df: dataframe of distinct hotels
    """
    filepath = os.path.join(ROOT_DIR, "static/all_hotels.geojson")
    if file_exists(filepath):
        pass
    else:
        def append_feature(x):
            feature = geojson.Feature(geometry=geojson.Point((x["lng"],
                                                              x["lat"])),
                                      properties={'count': x["count"],
                                                  '_id': str(x["_id"]),
                                                  'Hotel_Address': x['Hotel_Address'],
                                                  'Average_Score': x['Average_Score'],
                                                  'Hotel_Name': x['Hotel_Name']})
            features.append(feature)

        features = []
        df.apply(append_feature, axis=1)
        feature_collection = geojson.FeatureCollection(features)

        with open(filepath, 'w', encoding='utf8') as f:
            geojson.dump(feature_collection, f, sort_keys=True, ensure_ascii=False)


def read_geojson():
    """
    Reads geojson hotel data from file
    :return: geojson as json
    """
    filepath = os.path.join(ROOT_DIR, "static/all_hotels.geojson")
    if file_exists(filepath):
        with open(filepath) as f:
            return json.load(f)
