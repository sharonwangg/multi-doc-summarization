import datetime
from word2number import w2n

from function_util import strip_symbols


def yesterday(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a day
            phrase.

    Returns:
        (bool): True if `split_phrase` represents yesterday.
    """
    return len(split_phrase) == 1 and split_phrase[0] == 'yesterday'


def tomorrow(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a day
            phrase.

    Returns:
        (bool): True if `split_phrase` represents tomorrow.
    """
    return len(split_phrase) == 1 and split_phrase[0] == 'tomorrow'


def x_days_ago(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a day
            phrase.

    Returns:
        (bool): True if `split_phrase` represents x days ago.
    """
    return len(split_phrase) == 3 and split_phrase[1] == "days" and split_phrase[2] == "ago"


def handle_day(ent, date):
    """
    Args:
        ent (spacy date): A spacy entity representing a day.
        date (datetime object): Datetime that may not agree with `ent`.

    Returns:
        (datetime object): Datetime fixed from `ent`.
    """
    ent_split = [strip_symbols(word).lower() for word in str(ent).split()]
    if yesterday(ent_split):
        return date + datetime.timedelta(days=-1)
    elif tomorrow(ent_split):
        return date + datetime.timedelta(days=1)
    elif x_days_ago(ent_split):
        try:
            num = w2n.word_to_num(ent_split[0])
            return date + datetime.timedelta(days=-num)
        except ValueError:
            return date
    return date