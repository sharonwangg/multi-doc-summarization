"""
Utility module for loading data.

Attributes:
    TOPIC (str): Type of topics of summary.
    TOPICS_PATH (str): Path for topics to extract.
    PREDICTOR_PATH (str): Path for allennlp predictor.
    NLP (spacy.lang.en.English): Spacy object.
"""
import spacy
import os
from covid_summary.path_util import DATA_PATH, PREPROCESSED_CORPUS_PATH, PREPROCESSED_DATES_PATH, JOSE_VECTORS_PATH
from nltk.corpus import stopwords
from allennlp.predictors import Predictor

TOPIC_TYPE = 'items'
TOPICS_PATH = os.path.join(DATA_PATH, 'cate_topics', 'res_' + TOPIC_TYPE + '.txt')
PREDICTOR_PATH = 'https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz'
NLP = spacy.load('en_core_web_sm')

def get_stopwords():
    """
    Returns:
        (list of str): Stopwords.
    """
    return stopwords.words('english')

def get_general_words():
    """
    Returns:
        (frozenset of str): Words that shouldn't be a sub/obj.
    """

    return frozenset(
            ['i', 'you', 'them', 'they', 'he', 'him', 'she', 'her', 'his',
            'we', 'it', 'this', 'these', 'that', 'those', 'who', 'which',
            'as', 'each', 'all', 'everyone', 'either', 'one', 'both',
            'any', 'such', 'somebody', 'what', 'myself', 'herself', 'himself',
            'themselves', 'itself', 'us', 'mine', 'ours', 'yours', 'hers',
            'his', 'theirs', 'their', 'our', 'your', 'my', 'another',
            'any', 'anybody', 'anyone', 'anything', 'both', 'each', 'either',
            'everybody', 'everything', 'few', 'many', 'most', 'neither',
            'nobody', 'none', 'no one', 'nothing', 'other', 'others',
            'several', 'some', 'somebody', 'someone', 'something', 'such',
            'whatever', 'whichever', 'whoever', 'whom', 'whomever',
            'whose'])

def get_topics_lines():
    """
    Returns:
        (list of str): Returns a list of strings, with each string a line of
                       topics_file.
    """
    with open(TOPICS_PATH, 'r') as f:
        return f.read().splitlines()

def get_vectors_lines():
    """
    Returns:
        (list of str): A list of strings, with each string a line of
                       vectors_file.
    """
    with open(JOSE_VECTORS_PATH, 'r') as f:
        return f.read().splitlines()

def get_predictor():
    """
    Returns:
        (allennlp_models.structured_prediction.predictors.srl.SemanticRoleLabelerPredictor):
            A allennlp predictor object.
    """
    return Predictor.from_path(PREDICTOR_PATH)

def get_articles():
    """
    Returns:
        (List of list of sentences): A list of articles, with each article
            being a list of sentences.
    """
    with open(PREPROCESSED_CORPUS_PATH, 'r') as f:
        raw_articles = f.read().splitlines()

    articles = []
    #for i in range(len(raw_articles)):
    for i in range(1000):
        sentences = list(NLP(raw_articles[i]).sents)
        #sentences[0] = sentences[0][1:]
        #sentences[-1] = sentences[-1][:-1]
        articles.append(sentences)
    return articles

def get_datetimes():
    """
    Returns:
        (list of str): Returns a list of strings, each representing a date and
                       time.
    """
    with open(PREPROCESSED_DATES_PATH, 'r') as f:
        return f.read().splitlines()
