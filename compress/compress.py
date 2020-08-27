"""
Reduces the redundancy of a summary using Word Mover's Distance.

Attributes:
    WMD_THRESHOLD (float): Threshold for Word Mover's Distance. If 2 sentences have a WMD lower than this, they are too
        similar and 1 of them must be removed from the summary.
    TOPICS (list of str): List of topics that are summarized.
"""
import math
import os
from data_util import WORD2VEC_MODEL
from function_util import delete_stopwords, strip_symbols
from path_util import DATA_PATH
from sentence_details import SentenceDetails
from initial_extract.extract import relevancy_sorted_all_sentence_details

WMD_THRESHOLD = 1.51
TOPICS = relevancy_sorted_all_sentence_details.keys()


def get_tfidf(word, split_sentence, idfs):
    """
    Args:
        word (str): Some string representing a word.
        split_sentence (list of str): Sentence. List of words.
        idfs (dict from str to float): Dict mapping `word` to its idf value.

    Returns:
        (float): tfidf value of `word` in `split_sentence`.
    """
    tf = split_sentence.count(word.lower())
    if word in idfs.keys():
        return tf * idfs[word]
    return 0

def get_tfidf_vector(split_sentence, idfs):
    """
    Args:
        sentence (str): Some string representing a sentence.
        idfs (dict from str to float): Dict mapping words to their idf values.

    Returns:
        (dict from str to float): Dict mapping words to their tfidf values.
    """
    vector = {}

    for i in range(len(split_sentence)):
        word = split_sentence[i]
        vector[word] = get_tfidf(word, split_sentence[i], idfs)
    return vector

def get_idfs(split_sentences):
    """
    Args:
        split_sentences (list of list of str): List of list of words where each
            inner list is a sentence.

    Returns:
        (dict from str to float): Dict mapping words to their idf values.
    """
    document_counts = {}
    for sentence in split_sentences:
        for word in sentence:
            document_counts[word] = document_counts.get(word, 0) + 1

    idfs = {}
    for word, count in document_counts.items():
        idfs[word] = math.log(len(split_sentences) / count)

    return idfs


def get_score(split_sentence, idfs):
    """
    Args:
        sentence (str): Some string representing a sentence.
        idfs (dict from str to float): Dict mapping words to their idf values.

    Returns:
        (float): Summation of tfidf scores of `sentence`.
    """
    score = 0
    for tfidf in get_tfidf_vector(split_sentence, idfs).values():
        score += tfidf
    return score


def compress(sentence_details):
    """
    Args:
        sentence_details (list of SentenceDetails): Represents a summary. Each SentenceDetail contains its text, publish
            date, cosine similarity score, and original article.

    Returns:
        (list of SentenceDetails): Compressed summary.
    """
    compressed_sentence_details = []
    for i, sentence_detail in enumerate(sentence_details):
        split_sentence1 = delete_stopwords(strip_symbols(sentence_detail.text.lower().split()))
        redundant = False
        for j in reversed(range(i)):
            split_sentence2 = delete_stopwords(strip_symbols(sentence_details[j].text.lower().split()))
            distance = WORD2VEC_MODEL.wmdistance(split_sentence1, split_sentence2)
            if distance < WMD_THRESHOLD:
                redundant = True
                break

        sentence1 = sentence_detail.text
        date1 = sentence_detail.date
        relevancy_score1 = sentence_detail.relevancy_score
        article1 = sentence_detail.og_article
        if redundant:
            sentence2 = sentence_details[j].text

            sentence1_score = get_score(split_sentence1, get_idfs(split_sentence1))
            sentence2_score = get_score(split_sentence2, get_idfs(split_sentence2))
            print(0, sentence1 + ' ' + str(sentence1_score))
            print(1, sentence2 + ' ' + str(sentence2_score))

            if sentence1_score > sentence2_score:
                # Add sentence1 and delete sentence2 from `compressed_sentence_details`.
                compressed_sentence_details.append(SentenceDetails(text=sentence1,
                                                                   date=date1,
                                                                   relevancy_score=relevancy_score1,
                                                                   og_article=article1))
                compressed_sentence_details[j] = SentenceDetails(text='NA',
                                                                 date='NA',
                                                                 relevancy_score=0,
                                                                 og_article=[])
                print(2, sentence1)
            else:
                # Add an empty sentence to maintain indexing.
                compressed_sentence_details.append(SentenceDetails(text='NA',
                                                                   date='NA',
                                                                   relevancy_score=0,
                                                                   og_article=[]))
                print(2, sentence2)
        else:
            # Add new sentence as normal as it is not redundant with any previous sentences.
            compressed_sentence_details.append(SentenceDetails(text=sentence1,
                                                               date=date1,
                                                               relevancy_score=relevancy_score1,
                                                               og_article=article1))

    return [sentence_detail for sentence_detail in compressed_sentence_details if sentence_detail.text != 'NA']


def get_compressed_summary_path(topic):
    return os.path.join(DATA_PATH, 'step3_compressed_summary', topic + '_compressed_summary.txt')


def output(topic, compressed_sentence_details):
    """
    Args:
        topic (str): Topic of `compressed_sentence_details`.
        compressed_sentence_details (list of SentenceDetails): Compressed summary.
    """
    with open(get_compressed_summary_path(topic), 'w') as f:
        for sentence_detail in compressed_sentence_details:
            f.write(f'{str(sentence_detail.date)}\t{str(sentence_detail.text.strip())}\n')


compressed_all_sentence_details = {}
for topic, sentence_details in relevancy_sorted_all_sentence_details.items():
    compressed_all_sentence_details[topic] = compress(sentence_details)
    output(topic, compressed_all_sentence_details[topic])
