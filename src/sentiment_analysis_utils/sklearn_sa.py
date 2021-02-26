"""Functions for performing sentiment analysis using sklearn.


What's done:
- reads data from files (unzipped directories from the website)
- creates training data and training labels

To do:
- check that TfidfTransformer works (this translates raw training data text
  into feature vectors)
- finish Fit() function (make sure the parameter is correct)
- test

"""


import os

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

# List of files (with path) containing training data
TRAINING_CORPORA = []
TRAINING_LABELS = []
CLASSIFIER_TYPE = MultinomialNB
#CLASSIFIER = Train()
#CLASSIFIER_CLASSES = CLASSIFIER.classes_


def TransformData(text):
    """Converts a list of articles into features vectors."""
    # Option #1: word count
    features = CountVectorizer(analyzer = 'word', lowercase = False
            ).fit_transform(text)
    # Option #2: Normalize counts by converting to frequencies
    text_tfidf = TfidfTransformer(use_idf=False).fit_transform(text_word_count)
    features_nd = features.toarray() # for easy usage
    return text_tfidf


def Fit(article):
    """Takes an article object and classifies it."""
    # TODO: check that article.text is correct
    article_vector = TransformData(article.text)
    predicted_probs = CLASSIFIER.predict_proba(article_vector)
    # the output shoud be an array with two elements, one corresponding to
    # probability it's a positive sentiment and the other corresponding to
    # probability it's a negative sentiment. The order matches the order of
    # CLASSIFIER_CLASSES.
    print('Results: ', zip(CLASSIFIER_CLASSES, predicted_probs))


def ReadTrainingDataFile(data_file):
    f = open(data_file, 'rb')
    data = f.read()
    f.close()
    soup = BeautifulSoup(data)
    reviews = []
    try:
        reviews = soup.find_all('review_text')
        reviews = [review.text.strip() for review in reviews]
    except Exception as e:
        print('Error (%s) while processing training data file %s',
              str(e), data_file)
    return reviews


def ReadTrainingData():
    """Read data from http://www.cs.jhu.edu/~mdredze/datasets/sentiment/"""
    data_directory = '/Users/bcopos/Downloads/sorted_data'
    negative_data = []
    positive_data = []
    for root, dirs, files in os.walk(data_directory):
        if 'negative.review' in files:
            negative_data.extend(ReadTrainingDataFile(
                os.path.join(root, 'negative.review')))
        if 'positive.review' in files:
            positive_data.extend(ReadTrainingDataFile(
                os.path.join(root, 'positive.review')))
    return (positive_data, negative_data)


def Train():
    """Trains classifier."""
    positive_data, negative_data = ReadTrainingData()
    training_data = positive_data
    training_data.extend(negative_data)
    training_labels = [1 for i in positive_data]
    training_labels.extend([-1 for i in negative_data])
    training_tfidf = TransformData(training_data)
    return CLASSIFIER_TYPE.fit(training_data, TRAINING_LABELS)


Train()
