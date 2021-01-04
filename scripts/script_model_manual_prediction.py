from data.dataframes import clean_manual_review
from data.model_util import *

if __name__ == '__main__':
    """
    This script loads an already built neural network from a file, and uses manually added reviews to predict their 
    respective results. This has been done as metrics can often be a little hard to visualize, and seeing results on 
    your own input is quite fun.
    
    To use, change the filename in read_model to the model to use, and enter your reviews in the review_list variable, 
    then just run the file.
    """
    print("Loading model...\n")
    model = read_model("models/2021-01-04_21-18/Epoch-26_ValLoss-0.186.h5")
    print(model.summary())

    review_list = [
        'No hot water, leaking air conditioning, drip drip all night',
        "Was woken up by a random man persistently knocking on the door at 3am! Check-in took a long time, even though there wasn't a large queue. Long queues for the lifts",
        'Location was great. Size of disabled room great. Staff were great on reception and breakfast staff were very friendly. Tea and coffee was served regularly.',
        'Fantastic location! A very stylish hotel and we found the lifts were very frequent which is not always a given in hotels. The room as comfortable and clean, we had an amazing view of Leeds especially at night time!',
        'The only fault was that after our stay we fancied a little shop around Leeds and at check out we asked to leave our cases for an hour or two, the lady behind the desk decided not to let us keep them there as ‘people will be bringing cases soon before they check in, and it will get too full’. It wasn’t said in a polite way and it felt like as soon as we checked out we were ditched and the staff could be no longer helpful or accommodating. I think when your charging £109 a night then you can hold two small cases for at least an hour. We then dragged our cases round the shops irritating other shoppers as we went around. This is our second stay at the hotel we recommended all our family and friends but now we’re not sure we want to come back.'
    ]

    print("\n\nProcessing input...\n")
    processed_reviews = clean_manual_review(review_list)
    data = list(processed_reviews['Review'].values)
    padded_sequences = create_padded_sequences(data=data, replace_tokenizer=False)

    print("Predicting...\n")
    predictions = (model.predict(padded_sequences) > 0.5).astype("int32")
    predictions = ["Positive" if x == 1 else "Negative" for x in predictions]
    count = 0
    for x, y in zip(review_list, predictions):
        print(f"\nReview {count}: [{x}]\nHas been predicted: {y}")
        count += 1
