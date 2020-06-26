"""Functions for performing sentiment analysis using sklearn.


"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

# List of files (with path) containing training data
TRAINING_CORPORA = []
TRAINING_LABELS = []
CLASSIFIER_TYPE = MultinomialNB
CLASSIFIER = Train()
CLASSIFIER_CLASSES = CLASSIFIER.classes_

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



