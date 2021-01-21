"""
Includes previous and subsequent sentences that contain the theme.
"""
import os

from data_util import NLP
from sentence_details import SentenceDetails

from compress.compress import compressed_topic_specific_sentence_details
from compress.compress import TOPIC
from initial_extract.extract import topic_to_phrase
from initial_extract.extract_function_util import contains_theme, get_str_article, get_words
from path_util import DATA_PATH
from function_util import get_list_str_article


EXTENDED_SUMMARY_PATH = os.path.join(DATA_PATH, 'step5_extended_summary', TOPIC + '_extended_summary.txt')


def extend(compressed_summary, phrases):
    """
    Args:
        compressed_summary (list of SentenceDetails): Compressed summary.
        phrases (list of str): Phrases associated with TOPIC.

    Returns:
        (list of SentenceDetails): Extended summary.
    """
    extended_summary = []
    for sentence_detail in compressed_summary:
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
            extended_summary.append(SentenceDetails(get_str_article(new_chunk),
                                                    sentence_detail.date,
                                                    sentence_detail.relevancy_score,
                                                    sentence_detail.og_article))

    return extended_summary


def output(summary):
    with open(EXTENDED_SUMMARY_PATH, 'w') as f:
        for sentence_detail in summary:
            f.write(f'{sentence_detail.date}\t{sentence_detail.text}\n')


extended_summary = extend(compressed_topic_specific_sentence_details, topic_to_phrase[TOPIC])
output(extended_summary)