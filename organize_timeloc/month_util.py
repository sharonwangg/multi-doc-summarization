from organize_timeloc.organize_data_util import MONTHS
from function_util import strip_symbols

def has_month(s):
    """
    Args:
        s (str): Some string representing a date phrase.

    Returns:
        (list): List with the 0th element being a number representing the month,
            (1st element) or an empty string if there is no month in `s`.
    """
    for month in MONTHS:
        if month[1].lower() in s:
            return month
    return ""

def previous_month(s, new_month_num, date):
    """
    Args:
        s (str): Some string representing a month phrase.
        new_month_num (int): Number corresponding to new month.
        date (datetime obj): Publish date.

    Returns:
        (bool): True if `s` is referring to a previous month.
    """
    s_split = [strip_symbols(word).lower() for word in s.split()]
    if s_split[0] == "last" or new_month_num < date.month:
        return True
    return False

def future_month(s, new_month_num, date):
    """
    Args:
        s (str): Some string representing a month phrase.
        new_month_num (int): Number corresponding to new month.
        date (datetime obj): Publish date.

    Returns:
        (bool): True if `s` is referring to a future month.
    """
    s_split = [strip_symbols(word).lower() for word in s.split()]
    if s_split[0] == "next" or new_month_num > date.month:
        return True
    return False

def mid_month(s):
    """
    Args:
        s (str): Some string representing a data phrase.

    Returns:
        (bool): True if `s` is referring to the middle of a month.
    """
    if s[0:3].lower() == "mid":
        return True
    return False

def change_to_previous_month(new_month_num, date):
    """
    Args:
        new_month_num (int): Number corresponding to new month.
        date (datetime obj): Publish date.

    Returns:
        (datetime obj): Real date of event in sentence.
    """
    publish_month_num = date.month
    if new_month_num >= publish_month_num:
        return date.replace(year=date.year - 1, month=new_month_num)
    else:
        return date.replace(month=new_month_num)

def change_to_future_month(new_month_num, date):
    """
    Args:
        new_month_num (int): Number corresponding to new month.
        date (datetime obj): Publish date.

    Returns:
        (datetime obj): Real date of event in sentence.
    """
    publish_month_num = date.month
    if new_month_num <= publish_month_num:
        return date.replace(year=date.year + 1, month=new_month_num)
    else:
        return date.replace(month=new_month_num)

def change_to_mid_month(date):
    """
    Args:
        date (datetime obj): Current date associated with sentence.

    Returns:
        (datetime obj): Same as `date`, but with the day = 15.
    """
    return date.replace(day=15)

def handle_month(ent, date):
    """
    Args:
        ent (spacy date): A spacy entity representing a month.
        date (datetime object): Datetime that may not agree with `ent`.

    Returns:
        (datetime object): Datetime fixed from `ent`.
    """
    new_month = has_month(str(ent))
    if new_month:
        if previous_month(str(ent), new_month[0], date):
            date = change_to_previous_month(new_month[0], date)
        elif future_month(str(ent), new_month[0], date):
            date = change_to_future_month(new_month[0], date)

        if mid_month(str(ent)):
            date = change_to_mid_month(date)

    return date