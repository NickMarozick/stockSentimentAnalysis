"""Functions for performing sentiment analysis using sklearn.


"""

import os

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

def Train():
    """Trains classifier."""
    training_data = []
    for training_corpus in TRAINING_CORPORA:
        f = open(training_corpus, 'r')
        content = f.read()
        training_data.append(content.split())

    training_tfidf = TransformData(training_data)
    return CLASSIFIER_TYPE.fit(training_data, TRAINING_LABELS)

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


def ParseFile(data_file):
    f = open(data_file, 'r')
    lines = f.readlines()
    for line in lines:
        data = line.split()
        label = data[-1].split(':')[-1]
        for token in data[:-1:]:
            word, count = token.split(':')
            yield (word, count, label)
        break


def ReadTrainingData():
    """Read data from http://www.cs.jhu.edu/~mdredze/datasets/sentiment/"""
    data_dir = '/Users/bcopos/Downloads/processed_acl/books'
    feature_vector = dict()
    for (dirpath, dirnames, filenames) in os.walk(data_dir): 
        print(dirpath, dirnames, filenames)
        for f in filenames:
            for word, count, label in ParseFile(os.path.join(dirpath, f)):
                print(word, count, label)
                pass

ReadTrainingData()
