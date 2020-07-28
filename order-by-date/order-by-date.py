"""
Orders summary sentences by time.

Attributes:
    TOPIC (str): Topic of the summary.
    SUMMARY_PATH (str): Path for summary.
    DATES_PATH (str): Path for dates of sentences in summary.
    ORDERED_SUMMARY_PATH (str): Path for time-sorted summary.

    NLP (NLP object): NLP object
    MONTHS (list of list of int and str):
        Months and their corresponding numbers.
    WEEKDAYS (list of list of int and str):
        Weekdays and their corresponding numbers.
"""

import datetime
import spacy

TOPIC = 'symptom'
SUMMARY_PATH = '../compress/out/summaries/filtered_' + TOPIC + '.txt'
DATES_PATH = '../compress/out/dates/filtered_' + TOPIC + '_dates.txt'
ORDERED_SUMMARY_PATH = 'out/ordered_' + TOPIC + '.txt'

NLP = spacy.load('en_core_web_sm')
MONTHS = [[1, 'january'],
          [1, 'jan'],
          [2, 'february'],
          [2, 'feb'],
          [3, 'march'],
          [3, 'mar'],
          [4, 'april'],
          [4, 'apr'],
          [5, 'may'],
          [6, 'june'],
          [6, 'jun'],
          [7, 'july'],
          [7, 'jul'],
          [8, 'august'],
          [8, 'aug'],
          [9, 'september'],
          [9, 'sept'],
          [10, 'october'],
          [10, 'oct'],
          [11, 'november'],
          [11, 'nov'],
          [12, 'december'],
          [12, 'dec']]
WEEKDAYS = [[1, 'monday'],
            [1, 'mon'],
            [2, 'tuesday'],
            [2, 'tues'],
            [3, 'wednesday'],
            [3, 'wed'],
            [4, 'thursday'],
            [4, 'thurs'],
            [5, 'friday'],
            [5, 'fri'],
            [6, 'saturday'],
            [6, 'sat'],
            [7, 'sunday'],
            [7, 'sun']]

def get_dates():
    """
    Returns:
        (list of datetimes): List of dates in dates file.
    """
    with open(DATES_PATH, 'r') as f:
        return [datetime.datetime(int(x[0:4]), int(x[5:7]), int(x[8:10]))
            for x in f.read().splitlines()]

def get_sentences():
    """
    Returns:
        (list of str): Returns list of sentences.
    """
    with open(SUMMARY_PATH, 'r') as f:
        return f.read().splitlines()

def strip_symbols(s):
    """
    Args:
        s (str): Some string.

    Returns:
        (str): `s` without leading or trailing symbols.
    """
    if not s[0].isalnum():
        s = s[1:]
    if len(s) > 1 and not s[-1].isalnum():
        s = s[:-1]
    return s

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

def just_month(s):
    """
    Args:
        s (str): Some string representing a date phrase.

    Returns:
        (bool): True if `s` is just a month.
    """
    s_split = [strip_symbols(word).lower() for word in s.split()]
    if len(s_split) == 1:
        return True
    return False

def previous_time(s):
    """
    Args:
        s (str): Some string representing a date phrase.

    Returns:
        (bool): True if `s` is referring to a previous date.
    """
    s_split = [strip_symbols(word).lower() for word in s.split()]
    if s_split[0] == "last":
        return True
    return False

def future_month(s):
    """
    Args:
        s (str): Some string representing a date phrase.

    Returns:
        (bool): True if `s` is referring to a future month.
    """
    s_split = [strip_symbols(word).lower() for word in s.split()]
    if s_split[0] == "next":
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
        publish_month_num = date.month
        if just_month(str(ent)) or previous_time(str(ent)):
            date = change_to_previous_month(new_month[0], date)
        elif future_month(str(ent)):
            date = change_to_future_month(new_month[0], date)

        if mid_month(str(ent)):
            date = change_to_mid_month(date)

    return date

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

def change_to_previous_weekday(new_weekday_num, date):


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
        publish_weekday_num = date.isoweekday()
        if previous_time(str(ent)):
            date = change_to_previous_weekday(new_weekday[0], date)
    return date

def fix(timestamped_sentences):
    """
    Args:
        timestamped_sentences (list of lists containing datetimes and str):
            List of lists where each inner list contains a sentence and its
            corresponding date.

    Returns:
        (list of lists containing datetimes and str): List of lists where
        each inner list contains a sentence and its correct corresponding date.
    """
    print(timestamped_sentences[0][1])
    for i, timestamped_sentence in enumerate(timestamped_sentences):
        date = timestamped_sentence[0]
        sentence = timestamped_sentence[1].lower()
        doc = NLP(sentence)

        for ent in doc.ents:
            if ent.label_ == "DATE":
                timestamped_sentence[0] = handle_month(ent, date)
                timestamped_sentence[0] = handle_weekday(ent, timestamped_sentence[0])

                print(0, sentence)
                print(1, date)
                print(2, ent)
                print(3, timestamped_sentence[0])

                print('\n')

    return timestamped_sentences

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

    timestamped_sentences = fix(timestamped_sentences)
    return timestamped_sentences

def output(timestamped_sentences):
    with open(ORDERED_SUMMARY_PATH, 'w') as f:
        for date, sentence in timestamped_sentences:
            f.write(f"{date}\t{sentence}\n")

dates = get_dates()
sentences = get_sentences()

{dates[i]: sentences[i] for i in range(len(dates))}

timestamped_sentences = get_timestamped_sentences(dates, sentences)
timestamped_sentences.sort(key=lambda i: i[0])

timestamped_sentences[1][0] = datetime.datetime(2020, 5, 17)

output(timestamped_sentences)
