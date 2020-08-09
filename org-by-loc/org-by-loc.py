"""
Orders summary sentences by location.

Attributes:
    TOPIC (str): Topic of the summary.
    SUMMARY_PATH (str): Path for compressed summary.
    DATES_PATH (str): Path for dates of sentences in `SUMMARY_PATH`
    LOC_ORGANIZED_SUMMARY_PATH (str): Path for location-organized summary.

    NLP (NLP object): NLP object.
"""
import pycountry
import spacy

TOPIC = "mask"
SUMMARY_PATH = '../compress/out/summaries/filtered_' + TOPIC + '.txt'
DATES_PATH = '../compress/out/dates/filtered_' + TOPIC + '_dates.txt'
LOC_ORGANIZED_SUMMARY_PATH = 'out/loc_organized_' + TOPIC + '.txt'

NLP = spacy.load('en_core_web_sm')

def get_dates():
    """
    Returns:
        (list of str): List of dates in dates file.
    """
    with open(DATES_PATH, 'r') as f:
        return f.read().splitlines()

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

def has_loc(sentence):
    """
    Args:
        sentence (str): Some string representing a sentence.

    Returns:
        (bool): True if the string contains a location.
    """

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

def output(organized_summary):
    """
    Args:
        (dict from str to list): Keys are countries. Values are a list of lists
            where each inner list contains a sentence and its corresponding date.
            Organizes timestamped_sentences by country.
    """
    with open(LOC_ORGANIZED_SUMMARY_PATH, 'w') as f:
        for country, mini_summary in organized_summary.items():
            f.write(country.upper() + ':' + '\n')
            for date, sentence in mini_summary:
                f.write(f"{date}\t{sentence}\n")
            f.write('\n')

dates = get_dates()
sentences = get_sentences()

timestamped_sentences = get_timestamped_sentences(dates, sentences)
organized_summary = organize(timestamped_sentences)
output(organized_summary)
