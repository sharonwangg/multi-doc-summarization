from word2number import w2n

from function_util import strip_symbols


def has_year(s):
    """
    Args:
        s (str): Some string representing a spacy date.

    Returns:
        (bool): True if `s` is related to the concept of year.
    """
    if 'year' in s.lower() or 'years' in s.lower():
        return True
    return False

def last_year(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a year
            phrase.

    Returns:
        (bool): True if `split_phrase` represents last year.
    """
    return len(split_phrase) >= 2 and split_phrase[-2] == "last" and split_phrase[-1] == "year"

def next_year(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a year
            phrase.

    Returns:
        (bool): True if `split_phrase` represents last year.
    """
    return len(split_phrase) >= 2 and split_phrase[-2] == "next" and split_phrase[-1] == "year"

def x_years_ago(split_phrase):
    """
    Args:
        split_phrase (list of str): List of words that representing a year
            phrase.

    Returns:
        (bool): True if `split_phrase` represents x years ago.
    """
    return len(split_phrase) == 3 and split_phrase[1] == "years" and split_phrase[2] == "ago"

def change_to_different_year(s, date):
    """
    Args:
        s (str): Some string representing a year phrase.
        date (datetime object): Publish date.

    Returns:
        (datetime object): Adjusted `date` based on `s`.
    """
    s_split = [strip_symbols(word).lower() for word in s.split()]
    if last_year(s_split):
        return date.replace(year=date.year - 1)
    elif next_year(s_split):
        return date.replace(year=date.year + 1)
    elif x_years_ago(s_split):
        try:
            num = w2n.word_to_num(s_split[0])
            return date.replace(year=date.year - num)
        except ValueError:
            return date
    return date

def handle_year(ent, date):
    """
    Args:
        ent (spacy date): A spacy entity representing a year.
        date (datetime object): Datetime that may not agree with `ent`.

    Returns:
        (datetime object): Datetime fixed from `ent`.
    """
    new_year = has_year(str(ent))
    if new_year:
        date = change_to_different_year(str(ent), date)
    return date