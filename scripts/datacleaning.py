from data.dataframes import get_combined_review_df, preliminary_clean, clean_df_text, label_sentiment

if __name__ == '__main__':
    """
    This script runs all the data cleaning functions, including but not limited to, combining the invididual dataframe,
    removing non-english reviews and processing review text. All dataframes are pickled and can be found in 
    the static folder once generated.
    """
    review_df = get_combined_review_df()
    review_df2 = preliminary_clean(review_df)
    review_df3 = clean_df_text(review_df2)
    review_df4 = label_sentiment(review_df3)
    print(review_df4)
