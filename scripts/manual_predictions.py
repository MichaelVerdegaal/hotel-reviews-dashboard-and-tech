import os

from config import ROOT_DIR
from data.file_util import read_pickled_object, read_your_reviews
from data.dataframes import pre_process_text

if __name__ == '__main__':
    """
    This script reads review information from an excel file, and then uses pretrained models to evaluate them
    """
    print("Reading reviews from file...\n")
    df = read_your_reviews()
    df['Clean_Review'] = df['Review']
    df['Clean_Review'] = df['Review'].apply(pre_process_text)
    reviews_to_predict = df['Clean_Review'].values

    print("Reading models from file...\n")
    nb = read_pickled_object(os.path.join(ROOT_DIR, f"static/nb.pickle"))
    ada = read_pickled_object(os.path.join(ROOT_DIR, f"static/ada.pickle"))
    rforest = read_pickled_object(os.path.join(ROOT_DIR, f"static/rforest.pickle"))

    print("Predicting model sentiment with reviews...\n")
    nb_pred = nb.predict(reviews_to_predict)
    ada_pred = ada.predict(reviews_to_predict)
    rforest_pred = rforest.predict(reviews_to_predict)

    print("Adding predictions to dataframe...\n")
    df['Naive Bayes predicted'] = nb_pred
    df['AdaBoost predicted'] = ada_pred
    df['Random Forest predicted'] = rforest_pred

    print("Showing review predictions...s\n")
    prediction_value_map = {0: "negative",
                            1: "positive"}
    for r in range(len(reviews_to_predict)):
        print(f"Review {r}:")
        print(f'Naive Bayes predicted "{prediction_value_map[nb_pred[r]]}"')
        print(f'AdaBoost predicted "{prediction_value_map[ada_pred[r]]}"')
        print(f'Random Forest predicted "{prediction_value_map[rforest_pred[r]]}"\n\n')
