"""
Reduces the redundancy of a summary using Word Mover's Distance.

Attributes:
    TOPIC (str): Topic of the summary.
    INITIAL_SUMMARY_PATH (str): Path for summary.
    INITIAL_DATES_PATH (str): Path for dates of sentences in summary.
    COMPRESSED_SUMMARY_PATH (str): Path for compressed summary.
    COMPRESSED_DATES_PATH (str): Path for dates of sentences in compressed
        summary.

    STOPWORDS (list of str): Stopwords.
    THRESHOLD (float): Threshold for Word Mover's Distance.
    MODEL (model): Word2Vec model.
"""
import gensim.downloader as api
import math
import os
from covid_summary.path_util import DATA_PATH
from covid_summary.extract.extract import extracted_og_articles
from nltk.corpus import stopwords

TOPIC = 'economi'
INITIAL_SUMMARY_PATH = os.path.join(DATA_PATH, TOPIC + '_initial_summary.txt')
INITIAL_DATES_PATH = os.path.join(DATA_PATH, TOPIC + '_initial_summary_dates.txt')
COMPRESSED_SUMMARY_PATH = os.path.join(DATA_PATH, TOPIC + '_filtered_summary.txt')
COMPRESSED_DATES_PATH = os.path.join(DATA_PATH, TOPIC + '_filtered_summary_dates.txt')

STOPWORDS = stopwords.words('english')
THRESHOLD = 1.51
MODEL = api.load('word2vec-google-news-300')

def get_sentences():
    """
    Returns:
        (list of str): Summary sentences.
    """
    with open(INITIAL_SUMMARY_PATH, 'r') as f:
        return f.read().splitlines()

def get_split_sentences(sentences):
    """
    Returns:
        (list of list of str): List of list of words where each inner list is
            a sentence.
    """

    return [strip_symbols(sentence.lower().split()) for sentence in sentences]

def get_tfidf(word, split_sentence, idfs):
    """
    Args:
        word (str): Some string representing a word.
        sentence (str): Some string representing a sentence.
        idfs (dict from str to float): Dict mapping `word` to its idf value.

    Returns:
        (float): tfidf value of `word` in `sentence`.
    """
    tf = split_sentence.count(word.lower())
    return tf * idfs[word]

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

def get_dates():
    """
    Returns:
        (list of str): Dates.
    """
    with open(INITIAL_DATES_PATH, 'r') as f:
        return f.read().splitlines()

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

def get_compressed_results(sentences, split_sentences, idfs, dates, og_articles):
    """
    Args:
        sentences (list of str): Summary sentences.
        split_sentences (list of list of str): List of list of words where each
            inner list is a sentence.
        idfs (dict from str to float): Dict mapping words to their idf values.
        dates (list of str): Dates.
        og_articles (list of list of sentences): Articles that correspond with each sentence
            in summary.

    Returns:
        (list of str): Compressed summary sentences.
        (list of str): Compressed summary's dates.
        (list of str): Compressed original articles.
    """
    compressed_summary = []
    compressed_dates = []
    compressed_og_articles = []

    for i in range(len(split_sentences)):
        split_sentences[i] = [word for word in split_sentences[i] if word not in STOPWORDS]
        redundant = False
        for j in reversed(range(i)):
            distance = MODEL.wmdistance(split_sentences[i], split_sentences[j])
            if distance < THRESHOLD:
                redundant = True
                break
        sentence1 = sentences[i]
        date1 = dates[i]
        article1 = og_articles[i]
        if redundant:
            sentence2 = sentences[j]

            sentence1_score = get_score(split_sentences[i], idfs)
            sentence2_score = get_score(split_sentences[j], idfs)

            print(0, sentence1 + " " + str(sentence1_score))
            print(1, sentence2 + " " + str(sentence2_score))

            if sentence1_score > sentence2_score:
                compressed_summary.append(sentence1)
                compressed_dates.append(date1)
                compressed_og_articles.append(article1)

                compressed_summary[j] = ""
                compressed_dates[j] = ""
                compressed_og_articles[j] = []
                print(2, sentence1)
            else:
                compressed_summary.append("")
                compressed_dates.append("")
                compressed_og_articles.append([])
                print(2, sentence2)
        else:
            compressed_summary.append(sentence1)
            compressed_dates.append(date1)
            compressed_og_articles.append(article1)

    return compressed_summary, compressed_dates, compressed_og_articles

def output(compressed_summary, compressed_dates):
    """
    Args:
        compressed_summary (list of str): List of sentences in compressed
            summary.
        compressed_dates (list of str): List of dates corresponding to
            compressed summary.
    """
    with open(COMPRESSED_SUMMARY_PATH, 'w') as compressed_summary_f:
        with open(COMPRESSED_DATES_PATH, 'w') as compressed_dates_f:
            for i in range(len(compressed_summary)):
                if compressed_summary[i] == "" and compressed_dates[i] == "":
                    continue
                compressed_summary_f.write(compressed_summary[i] + '\n')
                compressed_dates_f.write(compressed_dates[i] + '\n')

sentences = get_sentences()
split_sentences = get_split_sentences(sentences)
idfs = get_idfs(split_sentences)
dates = get_dates()
compressed_summary, compressed_dates, topic_specific_compressed_og_articles = get_compressed_results(sentences, split_sentences, idfs, dates, extracted_og_articles[TOPIC])
output(compressed_summary, compressed_dates)

# delete empty inner lists
topic_specific_compressed_og_articles = [article for article in topic_specific_compressed_og_articles if article]