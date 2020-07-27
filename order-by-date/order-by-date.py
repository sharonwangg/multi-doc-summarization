"""
Orders summary sentences by time.

Attributes:
    TOPIC (str): Topic of the summary.
    SUMMARY_PATH (str): Path for summary.
    DATES_PATH (str): Path for dates of sentences in summary.
    ORDERED_SUMMARY_PATH (str): Path for time-sorted summary.

    NLP (NLP object): NLP object
    MONTHS (list of str): Months.
"""

import datetime
import spacy

TOPIC = 'symptom'
SUMMARY_PATH = '../compress/out/summaries/filtered_' + TOPIC + '.txt'
DATES_PATH = '../compress/out/dates/filtered_' + TOPIC + '_dates.txt'
ORDERED_SUMMARY_PATH = 'out/ordered_' + TOPIC + '.txt'

NLP = spacy.load('en_core_web_sm')
MONTHS = [[1, "January"],
          [2, "February"],
          [3, "March"],
          [4, "April"],
          [5, "May"],
          [6, "June"],
          [7, "July"],
          [8, "August"],
          [9, "September"],
          [10, "October"],
          [11, "November"],
          [12, "December"]]

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
        s (str): Some string representing a spacy date.

    Returns:
        (list): List with the 0th element being a number representing the month,
            (1st element).
    """
    for month in MONTHS:
        if month[1].lower() in s:
            return month
    return ""

def handle_month(ent, date):
    month = has_month(str(ent))
    if month:
        publish_month = date.month
        change_date = False
        if month[0] != publish_month:
            change_date = True
        if change_date:
            return date.replace(month=month[0])
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
    for i, timestamped_sentence in enumerate(timestamped_sentences):
        date = timestamped_sentence[0]
        sentence = timestamped_sentence[1].lower()
        doc = NLP(sentence)
        for ent in doc.ents:
            if ent.label_ == "DATE":
                timestamped_sentence[0] = handle_month(ent, date)
                


                #print(0, sentence)
                #print(1, date)
                #print(2, ent)
                #print('\n')

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
