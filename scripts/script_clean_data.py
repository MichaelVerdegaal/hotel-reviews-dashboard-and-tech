from data.dataframes import clean_and_label
from data.file_util import read_kaggle_reviews

if __name__ == '__main__':
    """
    This script runs all the data cleaning functions, including operations to fit everything into a single review 
    column, cleaning the text and labeling the sentiment of it. Results are pickled and can be found in 
    the static folder once generated.
    """
    kaggle_reviews = read_kaggle_reviews()
    cleaned_reviews = clean_and_label(kaggle_reviews)
    print(cleaned_reviews)
