"""
Utility module for loading data.

Attributes:
    TOPIC (str): Type of topics of summary.
    TOPICS_PATH (str): Path for topics to extract.
    PREDICTOR_PATH (str): Path for allennlp predictor.
    NLP (spacy.lang.en.English): Spacy object.
"""
import os
from path_util import DATA_PATH, JOSE_VECTORS_PATH

TOPIC_TYPE = 'topics'
TOPICS_PATH = os.path.join(DATA_PATH, 'cate_topics', 'res_' + TOPIC_TYPE + '.txt')


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


def get_days():
    """

    Returns:
        (frozenset of str): Days. Words that shouldn't be in a summary sentence.
    """
    return frozenset(['monday',
                      'mon',
                      'tuesday',
                      'tues',
                      'wednesday',
                      'wed',
                      'thursday',
                      'thurs',
                      'thur',
                      'friday',
                      'fri',
                      'saturday',
                      'sat',
                      'sunday',
                      'sun',
                      'weekend',
                      'month'])


def get_topics_lines():
    """
    Returns:
        (list of str): Returns a list of strings, with each string a line of
                       the topics file.
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


