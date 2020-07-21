"""
Utility module for loading data.

Attributes:
    TEXT_PATH (str): Path for corpus of articles.
    DATETIMES_PATH (str): Path for dates and times of articles.
    TOPICS_PATH (str): Path for topics to extract.
    VECTORS_PATH (str): Path for Jose word embedding vectors.
    PREDICTOR_PATH (str): Path for allennlp predictor.
    NLP (spacy.lang.en.English): Spacy object.
    SENTENCIZER (spacy.pipeline.pipes.Sentencizer): Sentencizer object.
"""

from nltk.corpus import stopwords
from allennlp.predictors import Predictor
from spacy.pipeline import SentenceSegmenter
from spacy.lang.en import English

TEXT_PATH = '../covid19dataset/articles.txt'
DATETIMES_PATH = '../covid19dataset/dates.txt'
TOPICS_PATH = 'in/res_topics.txt'
VECTORS_PATH = 'in/jose.txt'
PREDICTOR_PATH = 'https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz'

NLP = English()
SENTENCIZER = NLP.create_pipe("sentencizer")
NLP.add_pipe(SENTENCIZER)

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
    topics_file = open(TOPICS_PATH, 'r')
    return topics_file.read().splitlines()

def get_vectors_lines():
    """
    Returns:
        (list of str): A list of strings, with each string a line of
                       vectors_file.
    """
    vectors_file = open(VECTORS_PATH, 'r')
    return vectors_file.read().splitlines()

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
        (list of str): Returns a list of articles.
    """
    articles_file = open(TEXT_PATH, 'r')
    raw_articles = articles_file.read().splitlines()
    articles = []
    for i in range(len(raw_articles)):
        article = NLP(raw_articles[i])
        article = list(article.sents)
        article[0] = article[0][1:]
        article[-1] = article[-1][:-1]
        articles.append(article)
    return articles

def get_datetimes():
    """
    Returns:
        (list of str): Returns a list of strings, each representing a date and
                       time.
    """
    datetimes_file = open(DATETIMES_PATH, 'r')
    return datetimes_file.read().splitlines()