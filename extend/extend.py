import os

from data_util import NLP
from sentence_details import SentenceDetails

from organize_timeloc.organize import organized_summary
from initial_extract.extract import topic_to_phrase
from compress.compress import TOPIC
from initial_extract.extract_function_util import contains_theme, get_str_article, get_words
from path_util import DATA_PATH
from function_util import get_list_str_article


FINAL_SUMMARY_PATH = os.path.join(DATA_PATH, 'step5_final_summary', TOPIC + '_final_summary.txt')


def extend(organized_summary, phrases):
    """
    Args:
        organized_summary (dict from str to list): Keys are countries. Values are a list of SentenceDetails.
        phrases (dict from str to list of str): Maps topics to their respective phrases.

    Returns:
    """
    extended_summary = dict.fromkeys(organized_summary)
    for country in extended_summary.keys():
        extended_summary[country] = []
    for country, sentence_details in organized_summary.items():
        for j, sentence_detail in enumerate(sentence_details):
            sentence = list(NLP(sentence_detail.text).sents)[0]
            str_og_article = get_list_str_article(sentence_detail.og_article)

            if str(sentence) in str_og_article:
                center_idx = str_og_article.index(str(sentence))
                indices_to_add = [center_idx]
                for i in range(center_idx - 1, 0, -1):
                    if contains_theme(TOPIC, get_words(str_og_article[i]), topic_to_phrase[TOPIC]):
                        indices_to_add.append(i)
                        
                for i in range(center_idx + 1, len(str_og_article) - 1):
                    if contains_theme(TOPIC, get_words(str_og_article[i]), topic_to_phrase[TOPIC]):
                        indices_to_add.append(i)

                new_chunk = [str_og_article[i] for i in indices_to_add]
                print(country)
                extended_summary[country].append(SentenceDetails(get_str_article(new_chunk),
                                                               sentence_detail.date,
                                                               sentence_detail.relevancy_score,
                                                               sentence_detail.og_article))
                print(new_chunk)

    return extended_summary


def output(summary):
    with open(FINAL_SUMMARY_PATH, 'w') as f:
        for country in sorted(summary, key=lambda country: len(summary[country]), reverse=True):
            mini_summary = summary[country]
            f.write(country.upper() + ':' + '\n')
            for sentence_detail in mini_summary:
                f.write(f'{sentence_detail.date}\t{sentence_detail.text}\n')
            f.write('\n')


final_summary = extend(organized_summary, topic_to_phrase[TOPIC])
output(final_summary)