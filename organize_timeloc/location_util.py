import pycountry

from function_util import get_list_str_article


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


def get_country_from_article(doc, og_article):
    """
    Args:
        doc (NLP object): Sentence that we are trying to find the associated country of.
        og_article (list of sentences): Article that `doc` is in.

    Returns:
        (str): Country that `doc` is associated with (found in `og_article`).
            Empty string if a country couldn't be found.
    """
    return ""
    sentence = list(doc.sents)[0]
    str_og_article = get_list_str_article(og_article)
    print(sentence)
    if str(sentence) in str_og_article:
        center_idx = str_og_article.index(str(sentence))
        for i in range(center_idx + 1, len(str_og_article) - 1):
            country = get_country_from_sentence(og_article[i])
            if country:
                return country

        for i in range(center_idx - 1, 0, -1):
            country = get_country_from_sentence(og_article[i])
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