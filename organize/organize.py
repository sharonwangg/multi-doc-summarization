"""
Orders summary sentences by real time.

Attributes:
    TOPIC (str): Topic of the summary.
    SUMMARY_PATH (str): Path for summary.
    DATES_PATH (str): Path for dates of sentences in summary.
    ORDERED_SUMMARY_PATH (str): Path for time-sorted summary.

    NLP (NLP object): NLP object.
    MONTHS (list of list of int and str):
        Months and their corresponding numbers.
    WEEKDAYS (list of list of int and str):
        Weekdays and their corresponding numbers.
    ORDINAL_INDICATORS (list of str): -st, -nd, -rd, and -th
"""

import datetime
import spacy
import pycountry
from word2number import w2n
from calendar import monthrange, IllegalMonthError
from dateutil.parser import parse

TOPIC = 'mask'
SUMMARY_PATH = '../compress/out/summaries/filtered_' + TOPIC + '.txt'
DATES_PATH = '../compress/out/dates/filtered_' + TOPIC + '_dates.txt'
ORGANIZED_SUMMARY_PATH = 'out/organized_' + TOPIC + '.txt'

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
ORDINAL_INDICATORS = ['st', 'nd', 'rd', 'th']

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
            num = w2n.word_to_num(s_split[0])
            return date + datetime.timedelta(days=-num)
        except ValueError:
            return date
    return date

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

def organize(timestamped_sentences):
    """
    Args:
        timestamped_sentences (list of lists containing datetimes and str):
            List of lists where each inner list contains a sentence and its
            corresponding date.

    Returns:
        (dict from str to list): Keys are countries. Values are a list of lists
            where each inner list contains a sentence and its corresponding date.
            Organizes timestamped_sentences by country.
    """
    loc_stamped_sentences = {}
    for timestamped_sentence in timestamped_sentences:
        sentence = timestamped_sentence[1]
        doc = NLP(sentence)

        for ent in doc.ents:
            if ent.label_ == 'GPE':
                try:
                    possible_country = pycountry.countries.search_fuzzy(str(ent))
                    print(0, str(ent))
                    print(1, possible_country)
                except LookupError:
                    continue

                if len(possible_country) == 1 or str(ent) == possible_country[0].name:
                    country = possible_country[0].name
                else:
                    continue

                if country in loc_stamped_sentences.keys():
                    loc_stamped_sentences[country].append(timestamped_sentence)
                else:
                    loc_stamped_sentences[country] = [timestamped_sentence]

                break

    return loc_stamped_sentences

def order(final_summary):
    """
    Args:
        loc_organized_summary (dict from str to list): Keys are countries.
            Values are a list of lists where each inner list contains a
            sentence and its corresponding date.

    Returns:
        (dict from str to list): Keys are countries. Values are a list of lists
            where each inner list contains a sentence and its CORRECT
            corresponding date.
    """
    for country, mini_summary in final_summary.items():
        for i, timestamped_sentence in enumerate(mini_summary):
            date = timestamped_sentence[0]
            sentence = timestamped_sentence[1]
            doc = NLP(sentence)

            for ent in doc.ents:
                if ent.label_ == 'DATE':
                    timestamped_sentence[0] = handle_relative_time_phrases(ent, date)
                    timestamped_sentence[0] = handle_specific_time_phrases(ent, timestamped_sentence[0])

                    print(0, sentence)
                    print(1, date)
                    print(2, ent)
                    print(3, timestamped_sentence[0])
                    print('\n')

        final_summary[country].sort(key=lambda i: i[0])

    return final_summary

def output(final_summary):
    """
    Args:
        (dict from str to list): Keys are countries. Values are a list of lists
            where each inner list contains a sentence and its corresponding date.
    """
    with open(ORGANIZED_SUMMARY_PATH, 'w') as f:
        for country, mini_summary in final_summary.items():
            f.write(country.upper() + ':' + '\n')
            for datetime, sentence in mini_summary:
                date = str(datetime).split()[0]
                f.write(f"{date}\t{sentence}\n")
            f.write('\n')

dates = get_dates()
sentences = get_sentences()

{dates[i]: sentences[i] for i in range(len(dates))}

timestamped_sentences = get_timestamped_sentences(dates, sentences)
loc_organized_summary = organize(timestamped_sentences)
final_summary = order(loc_organized_summary)
output(final_summary)
