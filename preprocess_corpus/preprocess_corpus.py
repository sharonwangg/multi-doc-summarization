"""
Removes redundant articles in the raw corpus. Converts articles to NLP sentences and timestamps each article.

Attributes:
    RAW_DATA (list of lists): Corpus. Each inner list is a timestamped article. 0th element is the datetime, 1st element
        is the article.
"""
from data_util import NLP
from path_util import PREPROCESSED_DATA_PATH
from preprocess_corpus.preprocess_function_util import get_raw_data, get_article_str

RAW_DATA = get_raw_data()


def preprocess(raw_data):
    """ Removes identical timestamped articles in `raw_data` and timestamped articles with no assigned date and returns
            the resulting preprocessed data.
    Args:
        raw_data (list of lists): Each inner list is a timestamped article. 0th element is the datetime, 1st element is
            the article.
    Returns:
        (list of lists): `raw_data` with identical articles and articles with invalid dates removed.
    """
    preprocessed_data = []
    all_article_sents = []
    for i, timestamped_article in enumerate(raw_data):
        print('preprocessing article ' + str(i + 1))
        datetime = timestamped_article[0]
        article_str = timestamped_article[1]
        article_sents = list(NLP(article_str).sents)
        if article_sents not in all_article_sents and datetime != 'NA':
            preprocessed_data.append([datetime, article_sents])
            all_article_sents.append(article_sents)
    return preprocessed_data


def output(preprocessed_data):
    """ Outputs `preprocessed_data` for debugging purposes.
    Args:
        preprocessed_data (list of lists): Each inner list is a timestamped article. 0th element is the datetime, 1st
            element is the article.
    """
    with open(PREPROCESSED_DATA_PATH, 'w') as f:
        for timestamped_article in preprocessed_data:
            datetime = timestamped_article[0]
            article_sents = timestamped_article[1]
            article_str = get_article_str(article_sents)
            f.write(f'{str(datetime)}\t{article_str}\n')


preprocessed_data = preprocess(RAW_DATA)
output(preprocessed_data)