from nltk.stem.snowball import SnowballStemmer
from data_util import get_stopwords

STEMMER = SnowballStemmer('english')
STOPWORDS = get_stopwords()


def strip_symbols(s):
    """
    Args:
        s (str): Some string.

    Returns:
        (str): `s` without leading or trailing symbols.
    """
    while len(s) > 1 and not s[0].isalnum():
        s = s[1:]

    while len(s) > 1 and not s[-1].isalnum():
        s = s[:-1]

    return s


def normalize(s):
    """
    Args:
        s (str): Some string.

    Returns:
        (str): `s` but stemmized, stripped, and lowercased
    """
    return STEMMER.stem(s.strip().lower())


def delete_stopwords(string_list):
    """
    Args:
        s (list of str): Some list of strings.

    Returns:
        (str): `s` without stopwords.
    """
    return [s for s in string_list if s not in STOPWORDS]

