"""
Orders summary sentences by real time and organizes summary by location.

Attributes:
    ORGANIZED_SUMMARY_PATH (str): Path for location and time-organized summary.

    NLP (NLP object): NLP object.
    MONTHS (list of list of int and str):
        Months and their corresponding numbers.
    WEEKDAYS (list of list of int and str):
        Weekdays and their corresponding numbers.
    ORDINAL_INDICATORS (list of str): -st, -nd, -rd, and -th
"""
import pycountry
from calendar import monthrange, IllegalMonthError
from dateutil.parser import parse
from compress.compress import compressed_topic_specific_sentence_details
from sentence_details import SentenceDetails
from data_util import NLP


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

def is_valid_location(location, possible_countries):
    """
    Args:
        location (str): Location found in sentence.
        possible_countries (list of pycountry Countries): Possible matches for
            `location`.

    Returns:
        (bool): True if `location` matches `possible_countries`.
    """
    return len(possible_countries) == 1 or location == possible_countries[0].name

def add_sentence(loc_stamped_sentences, country, sentence_detail):
    """
    Args:
        loc_stamped_sentences (dict from str to list): Keys are countries.
            Values are a list of lists where each inner list contains a
            sentence and its corresponding date.
        country (str): Country that the sentence is about.
        timestamped_sentence (list containing datetimes and str): List with
            the 0th element being the date and the 1st element being the
            sentence.

    Returns:
        (dict from str to list): `loc_stamped_sentences` with
            `timestamped_sentence` being added as a value for key `country`.
    """
    if country in loc_stamped_sentences.keys():
        loc_stamped_sentences[country].append(sentence_detail)
    else:
        loc_stamped_sentences[country] = [sentence_detail]

    return loc_stamped_sentences

def valid_index(index, list):
    """
    Args:
        index (int): Index.
        list (list of anything): List.

    Returns:
        (bool): True if `index` is valid for `list`.
    """
    return index >= 0 and index < len(list)

def get_country_from_article(str_doc, doc, og_article):
    """
    Args:
        doc (NLP object): Sentence that we are trying to find the associated country of.
        og_article (list of sentences): Article that `doc` is in.

    Returns:
        (str): Country that `doc` is associated with (found in `og_article`).
            Empty string if a country couldn't be found.
    """
    sentence = list(doc.sents)
    if len(sentence) != 1:
        return ""

    str_og_article = ""
    for sent in og_article:
        str_og_article += (' ' + str(sent) + ' ')

    sentence = sentence[0]

    print(sentence)
    if sentence in og_article:
        print('HERE')
        center_idx = og_article.index(sentence)
        print('center_idx: ' + str(center_idx))
        print('center_sentence: ' + str(og_article[center_idx]))
        max_radius = max(center_idx, len(og_article) - center_idx)
        for i in range(1, max_radius):
            previous_idx = center_idx - i
            if valid_index(previous_idx, og_article):
                print('previous_idx: ' + str(previous_idx))
                print('previous sentence: ' + str(og_article[previous_idx]))
                country = get_country_from_sentence(og_article[previous_idx])
                if country:
                    return country
            future_idx = center_idx + i
            if valid_index(future_idx, og_article):
                print('future_idx: ' + str(future_idx))
                print('future sentence: ' + str(og_article[previous_idx]))
                country = get_country_from_sentence(og_article[future_idx])
                if country:
                    return country
    else:
        return ""

def get_country_from_sentence(doc):
    """
    Args:
        doc (NLP object): NLP version of a sentence.

    Returns:
        (str): A country if there is one in `doc`. Else, return empty string.
    """
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            try:
                possible_countries = pycountry.countries.search_fuzzy(str(ent))
            except LookupError:
                continue

            if is_valid_location(str(ent), possible_countries):
                print('GPE: ' + ent.text)
                if possible_countries[0].name == 'VIRGIN ISLANDS, U.S.':
                    return 'UNITED STATES'
                return possible_countries[0].name
            else:
                continue

    return ""

def organize(sentence_details):
    """
    Args:
        timestamped_sentences (list of lists containing datetimes and str): List of lists where each inner list contains
            a sentence and its corresponding date.
        topic_specific_og_articles (list of list of sentences): Contains the original article that each sentence in
            `timestamped_sentences` is from. Each article is a list of sentences.

    Returns:
        (dict from str to list): Keys are countries. Values are a list of lists
            where each inner list contains a sentence and its corresponding date.
            Organizes `timestamped_sentences` by country.
    """
    loc_organized_sentences = {}
    for i, sentence_detail in enumerate(sentence_details):
        str_sentence = sentence_detail.text
        doc = NLP(str_sentence)
        og_article = sentence_detail.og_article

        country_from_sentence = get_country_from_sentence(doc)
        if country_from_sentence:
            print('country from sentence')
            loc_organized_sentences = add_sentence(loc_organized_sentences, country_from_sentence, sentence_detail)
            print(0, str_sentence)
            print(1, country_from_sentence)
        else:
            country_from_article = get_country_from_article(str_sentence, doc, og_article)
            if country_from_article:
                print('country from article')
                loc_organized_sentences = add_sentence(loc_organized_sentences, country_from_article, sentence_detail)
                print(0, str_sentence)
                print(1, country_from_article)

    return loc_organized_sentences


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
        for i, sentence_detail in enumerate(mini_summary):
            sentence = sentence_detail.text
            date = sentence_detail.date
            relevancy_score = sentence_detail.relevancy_score
            article = sentence_detail.og_article
            doc = NLP(sentence)

            for ent in doc.ents:
                if ent.label_ == 'DATE':
                    mini_summary[i] = SentenceDetails(text=sentence,
                                                      date=handle_relative_time_phrases(ent, date),
                                                      relevancy_score=relevancy_score,
                                                      og_article=article)
                    mini_summary[i] = SentenceDetails(text=sentence,
                                                      date=handle_specific_time_phrases(ent, mini_summary[i].date),
                                                      relevancy_score=relevancy_score,
                                                      og_article=article)

                    print(0, sentence)
                    print(1, date)
                    print(2, ent)
                    print(3, mini_summary[i].date)
                    print('\n')

        final_summary[country].sort(key=lambda j: j.date)

    return final_summary


def output(organized_summary):
    """
    Args:
        organized_summary (dict from str to list): Keys are countries. Values are a list of SentenceDetails.
    """
    with open(ORGANIZED_SUMMARY_PATH, 'w') as f:
        for country in sorted(organized_summary, key=lambda country: len(organized_summary[country]), reverse=True):
            mini_summary = organized_summary[country]
            f.write(country.upper() + ':' + '\n')
            for sentence_detail in mini_summary:
                f.write(f'{sentence_detail.date}\t{sentence_detail.text}\n')
            f.write('\n')


loc_organized_summary = organize(compressed_topic_specific_sentence_details)
organized_summary = order(loc_organized_summary)
output(organized_summary)
