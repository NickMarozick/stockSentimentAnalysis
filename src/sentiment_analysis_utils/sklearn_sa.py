"""Functions for performing sentiment analysis using sklearn.


"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

TRAINING_CORPORA = []
TRAINING_LABELS = []
CLASSIFIER_TYPE = MultinomialNB
CLASSIFIER = Train()
CLASSIFIER_CLASSES = CLASSIFIER.classes_

def TransformData(text):
    """Converts a list of articles into features vectors."""
    text_word_count = count_vect.fit_transform(text)
    # Normalize counts by converting to frequencies
    text_tfidf = TfidfTransformer(use_idf=False).fit_transform(text_word_count)
    return text_tfidf

def Train():
    """Trains classifier."""
    # TODO: figure out how to provide multiple training corpora
    training_data = []
    for training_corpus in TRAINING_CORPORA:
        training_tfidf = TransformData(TRAINING_CORPUS)
        training_data.append(training_tfidf)
    return CLASSIFIER_TYPE.fit(training_data, TRAINING_LABELS)

def Fit(article):
    """Takes an article object and classifies it."""
    count_vect = CountVectorizer()
    # TODO: check that article.text is correct
    article_tfidf = TransformData(article.text)
    predicted_probs = CLASSIFIER.predict_proba(article_tfdf)
    # the output shoud be an array with two elements, one corresponding to
    # probability it's a positive sentiment and the other corresponding to
    # probability it's a negative sentiment. The order matches the order of
    # CLASSIFIER_CLASSES.
    print('Results: ', zip(CLASSIFIER_CLASSES, predicted_probs))



