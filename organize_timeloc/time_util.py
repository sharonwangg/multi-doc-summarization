from calendar import monthrange, IllegalMonthError
from dateutil.parser import parse

from organize_timeloc.day_util import handle_day
from organize_timeloc.week_util import handle_weekday, handle_week
from organize_timeloc.month_util import handle_month
from organize_timeloc.year_util import handle_year


def handle_relative_time_phrases(ent, date):
    """
    Args:
        ent (spacy date): A spacy entity representing a date.
        date (datetime object): Datetime that may not agree with `ent`.

    Returns:
        (datetime object): Datetime fixed from `ent`.
    """
    date = handle_day(ent, date)
    date = handle_weekday(ent, date)
    date = handle_week(ent, date)
    date = handle_month(ent, date)
    date = handle_year(ent, date)
    return date


def is_date(s, fuzzy=False):
    """
    Args:
        s (str): String to check for date.
        fuzzy (bool): Ignore unknown tokens in string if True

    Returns:
        (bool): True if the string can be interpreted as a date.
    """
    try:
        print(s)
        parse(s, fuzzy=fuzzy)
        return True
    except (IllegalMonthError, ValueError, TypeError):
        return False


def handle_specific_time_phrases(ent, publish_date):
    """
    Args:
        ent (spacy date): A spacy entity representing a possible date.
        publish_date (datetime object): Publish date.

    Returns:
        (datetime object): `publish_date` fixed by `ent`.
    """
    if len(str(ent)) > 3 and is_date(str(ent)):
        return parse(str(ent))
    return publish_date

def get_timestamped_sentences(dates, sentences):
    """
    Args:
        dates (list of datetimes): List of dates.
        sentences (list of str): List of sentences.

    Returns:
        (list of lists containing datetimes and str): List of lists where each
            inner list contains a sentence and its corresponding date.
    """
    timestamped_sentences = []
    for i, date in enumerate(dates):
        timestamped_sentences.append([date, sentences[i]])

    return timestamped_sentences
