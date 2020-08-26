"""
Utility module for storing functions needed for preprocess_corpus.py.
"""
import datetime
from path_util import RAW_CORPUS_PATH, RAW_DATETIMES_PATH


def get_raw_corpus():
    """ Reads raw corpus from `RAW_CORPUS_PATH`.
    Returns:
        (list of str): Raw corpus. List of articles.
    """
    with open(RAW_CORPUS_PATH, 'r') as f:
        return f.read().splitlines()


def get_raw_datetimes():
    """ Reads raw datetimes from `RAW_DATETIMES_PATH`.
    Returns:
        (list of str): Raw datetime items. List of publish datetimes.
    """
    raw_datetimes = []
    with open(RAW_DATETIMES_PATH, 'r') as f:
        for x in f.read().splitlines():
            try:
                raw_datetimes.append(datetime.datetime(year=int(x[1:5]), month=int(x[6:8]), day=int(x[9:11])))
            except ValueError:
                raw_datetimes.append('NA')
    return raw_datetimes


def get_raw_data():
    """ Transforms `raw_corpus` and `raw_dates` into a list of lists where each inner list is a timestamped article.
    Args:
        raw_corpus (list of str): List of articles.
        raw_datetimes (list of str): List of publish datetimes.

    Returns:
        (list of lists): Each inner list is a timestamped article. 0th element is the datetime, 1st element is the
            article.
    """
    raw_corpus = get_raw_corpus()
    raw_datetimes = get_raw_datetimes()
    raw_data = []
    for i, raw_datetime in enumerate(raw_datetimes):
        raw_data.append([raw_datetime, raw_corpus[i]])
    return raw_data


def get_article_str(article_sents):
    """ Converts `article_sents` into a single string.
    Args:
        article_sents: List of NLP sentences.
    Returns:
        (str): `article_sents` in a single string format.
    """
    article_str = ""
    for nlp_sent in article_sents:
        article_str += (' ' + nlp_sent.text + ' ')
    return article_str