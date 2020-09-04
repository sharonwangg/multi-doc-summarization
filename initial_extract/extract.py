"""
Extracts relevant sentences from corpus related to category names.
"""
from preprocess_corpus.preprocess_corpus import preprocessed_data
from function_util import normalize
from sentence_details import SentenceDetails
from initial_extract.extract_path_util import get_summary_path
from initial_extract.extract_data_util import DEFAULT_SUMMARY_LENGTH
from initial_extract.extract_function_util import get_words, is_quality_sentence, calculate_relevancy_score, get_topic_to_phrase, get_word_to_vector, sort_by_relevancy_score


def extract(topic_to_phrase, timestamped_articles):
    """
    Args:
        topic_to_phrase (dict from str to list of str): Maps topics to their respective phrases.
        timestamped_articles (list of lists): Each inner list is a timestamped article. 0th element is the datetime, 1st
            element is the article.

    Returns:
        (dict from str to list of SentenceDetails): Maps topics to a list of SentenceDetails that each represent a
            summary. Each SentenceDetail contains its text, date, cosine similarity score, and original article.
    """
    all_sentence_details = {}
    topic_to_summary = {}
    for topic in topic_to_phrase.keys():
        all_sentence_details[topic] = []
        topic_to_summary[topic] = set()

    for i, timestamped_article in enumerate(timestamped_articles):
        print('extracting from article ' + str(i + 1))
        datetime = timestamped_article[0]
        article_sents = timestamped_article[1]

        for j, sent in enumerate(article_sents):
            words = get_words(sent.text)

            for topic, phrase in topic_to_phrase.items():
                if is_quality_sentence(normalize(topic), phrase, words, sent, topic_to_summary[topic]):
                    sentence_to_add = SentenceDetails(
                        sent.text.strip(),
                        datetime,
                        calculate_relevancy_score(normalize(topic), words, word_to_vector),
                        article_sents)
                    all_sentence_details[topic].append(sentence_to_add)
                    topic_to_summary[topic].add(sent.text.strip())

    return all_sentence_details


def output(sorted_all_sentence_details):
    """
    Args:
        sorted_all_sentence_details (list of SentenceDetails): A list of sentences with corresponding dates, scores, and
            original articles.
    """
    for topic, sentence_details in sorted_all_sentence_details.items():
        with open(get_summary_path(topic), 'w') as f:
            for sentence_detail in sentence_details:
                f.write(f'{str(sentence_detail.date)}\t{str(sentence_detail.text.strip())}\n')


topic_to_phrase = get_topic_to_phrase()
word_to_vector = get_word_to_vector()
all_sentence_details = extract(topic_to_phrase, preprocessed_data)
relevancy_sorted_all_sentence_details = sort_by_relevancy_score(all_sentence_details)

for topic, sentence_details in relevancy_sorted_all_sentence_details.items():
    summary_length = DEFAULT_SUMMARY_LENGTH
    if len(sentence_details) < summary_length:
        summary_length = len(sentence_details)
        continue
    relevancy_sorted_all_sentence_details[topic] = sentence_details[:summary_length]

output(relevancy_sorted_all_sentence_details)