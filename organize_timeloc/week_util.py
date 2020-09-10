import datetime
from word2number import w2n

from organize_timeloc.organize_data_util import WEEKDAYS
from function_util import strip_symbols


def has_weekday(s):
    """
    Args:
        s (str): Some string representing a spacy date.

    Returns:
        (list): List with the 0th element being a number representing the
            weekday, (1st element) or an empty string if there is no weekday in
            `s`.
    """
    for weekday in WEEKDAYS:
        if weekday[1].lower() in s:
            return weekday
    return ""

def previous_weekday(s, new_weekday_num, date):
    """
    Args:
        s (str): Some string representing a weekday phrase.
        new_weekday_num (int): Number corresponding to new weekday.
        date (datetime obj): Publish date.

    Returns:
        (bool): True if `s` is referring to a previous weekday.
        (int): Number of weeks ago that `s` is referring to.
    """
    s_split = [strip_symbols(word).lower() for word in s.split()]
    if s_split[0] == "last":
        return True, 1
    elif len(s_split) == 3 and s_split[2] == "ago":
        try:
            num = w2n.word_to_num(s_split[0])
            return True, num
        except ValueError:
            return False, 0
    return False, 0

def future_weekday(s, new_weekday_num, date):
    """
    Args:
        s (str): Some string representing a weekday phrase.
        new_weekday_num (int): Number corresponding to new weekday.
        date (datetime obj): Publish date.

    Returns:
        (bool): True if `s` is referring to a future weekday.
    """
    s_split = [strip_symbols(word).lower() for word in s.split()]
    if s_split[0] == "next":
        return True
    return False

def change_to_previous_weekday(new_weekday_num, date, num):
    """
    Args:
        new_weekday_num (int): Number corresponding to new weekday.
        date (datetime obj): Publish date.
        num (int): Number of weeks ago that `new_weekday_num` refers to.

    Returns:
        (datetime obj): Real date of event in sentence.
    """
    publish_weekday_num = date.isoweekday()
    return date - datetime.timedelta(days=publish_weekday_num) + datetime.timedelta(days=new_weekday_num, weeks=-num)

def change_to_future_weekday(new_weekday_num, date):
    """
    Args:
        new_weekday_num (int): Number corresponding to new weekday.
        date (datetime obj): Publish date.

    Returns:
        (datetime obj): Real date of event in sentence.
    """
    publish_weekday_num = date.isoweekday()
    return date - datetime.timedelta(days=publish_weekday_num) + datetime.timedelta(days=new_weekday_num, weeks=1)

def change_weekday(new_weekday_num, date):
    publish_weekday_num = date.isoweekday()
    return date - datetime.timedelta(days=publish_weekday_num) + datetime.timedelta(days=new_weekday_num)

def handle_weekday(ent, date):
    """
    Args:
        ent (spacy date): A spacy entity representing a weekday.
        date (datetime object): Datetime that may not agree with `ent`.

    Returns:
        (datetime object): Datetime fixed from `ent`.
    """
    new_weekday = has_weekday(str(ent))
    if new_weekday:
        if previous_weekday(str(ent), new_weekday[0], date)[0]:
            date = change_to_previous_weekday(new_weekday[0], date, previous_weekday(str(ent), new_weekday[0], date)[1])
        elif future_weekday(str(ent), new_weekday[0], date):
            date = change_to_future_weekday(new_weekday[0], date)
        else:
            date = change_weekday(new_weekday[0], date)
    return date

def has_week(s):
    """
    Args:
        s (str): Some string representing a spacy date.

    Returns:
        (bool): True if `s` is related to the concept of weeks.
    """
    if 'week' in s.lower() or 'weeks' in s.lower():
        return True
    return False

def last_week(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a week
            phrase.

    Returns:
        (bool): True if `split_phrase` represents last week.
    """
    return len(split_phrase) == 2 and split_phrase[0] == "last" and split_phrase[1] == "week"

def early_last_week(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a week
            phrase.

    Returns:
        (bool): True if `split_phrase` represents early last week.
    """
    return len(split_phrase) == 3 and split_phrase[0] == "early" and split_phrase[1] == "last" and split_phrase[2] == "week"

def late_last_week(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a week
            phrase.

    Returns:
        (bool): True if `split_phrase` represents late last week.
    """
    return len(split_phrase) == 3 and split_phrase[0] == "late" and split_phrase[1] == "last" and split_phrase[2] == "week"

def next_week(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a week
            phrase.

    Returns:
        (bool): True if `split_phrase` represents next week.
    """
    return len(split_phrase) == 2 and split_phrase[0] == "next" and split_phrase[1] == "week"

def early_next_week(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a week
            phrase.

    Returns:
        (bool): True if `split_phrase` represents early next week.
    """
    return len(split_phrase) == 3 and split_phrase[0] == "early" and split_phrase[1] == "next" and split_phrase[2] == "week"

def late_next_week(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a week
            phrase.

    Returns:
        (bool): True if `split_phrase` represents late next week.
    """
    return len(split_phrase) == 3 and split_phrase[0] == "late" and split_phrase[1] == "next" and split_phrase[2] == "week"

def x_weeks_ago(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a week
            phrase.

    Returns:
        (bool): True if `split_phrase` represents x weeks ago.
    """
    return len(split_phrase) == 3 and split_phrase[1] == "weeks" and split_phrase[2] == "ago"

def change_to_different_week(s, date):
    """
    Args:
        s (str): Some string representing a week phrase.
        date (datetime object): Publish date.

    Returns:
        (datetime object): Adjusted `date` based on `s`.
    """
    s_split = [strip_symbols(word).lower() for word in s.split()]
    publish_weekday_num = date.isoweekday()
    if last_week(s_split):
        return date + datetime.timedelta(weeks=-1)
    elif early_last_week(s_split):
        return date - datetime.timedelta(days=publish_weekday_num) + datetime.timedelta(days=1, weeks=-1)
    elif late_last_week(s_split):
        return date - datetime.timedelta(days=publish_weekday_num) + datetime.timedelta(days=5, weeks=-1)
    elif next_week(s_split):
        return date + datetime.timedelta(weeks=1)
    elif early_next_week(s_split):
        return date - datetime.timedelta(days=publish_weekday_num) + datetime.timedelta(days=1, weeks=1)
    elif late_next_week(s_split):
        return date - datetime.timedelta(days=publish_weekday_num) + datetime.timedelta(days=5, weeks=1)
    elif x_weeks_ago(s_split):
        try:
            num = w2n.word_to_num(s_split[0])
            return date + datetime.timedelta(weeks=-num)
        except ValueError:
            return date
    return date

def handle_week(ent, date):
    """
    Args:
        ent (spacy date): A spacy entity representing a week.
        date (datetime object): Datetime that may not agree with `ent`.

    Returns:
        (datetime object): Datetime fixed from `ent`.
    """
    new_week = has_week(str(ent))
    if new_week:
        date = change_to_different_week(str(ent), date)
    return date