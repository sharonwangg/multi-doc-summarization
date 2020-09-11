"""
Orders summary sentences by real time and organizes summary by location.

Attributes:
    NLP (NLP object): NLP object.
"""
import os
from data_util import NLP
from path_util import DATA_PATH

from compress.compress import compressed_topic_specific_sentence_details
from compress.compress_data_util import TOPIC
from sentence_details import SentenceDetails
from organize_timeloc.location_util import get_country_from_sentence, add_sentence, get_country_from_article
from organize_timeloc.time_util import handle_relative_time_phrases, handle_specific_time_phrases

ORGANIZED_SUMMARY_PATH = os.path.join(DATA_PATH, 'step4_organized_summary', TOPIC + '_organized_summary.txt')


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
            country_from_article = get_country_from_article(doc, og_article)
            if country_from_article:
                print('country from article')
                loc_organized_sentences = add_sentence(loc_organized_sentences, country_from_article, sentence_detail)
                print(0, str_sentence)
                print(1, country_from_article)
            else:
                loc_organized_sentences = add_sentence(loc_organized_sentences, 'Other', sentence_detail)

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


print('hello?')
loc_organized_summary = organize(compressed_topic_specific_sentence_details)
organized_summary = order(loc_organized_summary)
output(organized_summary)
