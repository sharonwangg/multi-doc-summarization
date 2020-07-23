"""
Reduces the redundancy of a summary using Word Mover's Distance.

Attributes:
    TOPIC (str): Topic of the summary.
    SUMMARY_PATH (str): Path for summary.
    DATES_PATH (str): Path for dates of sentences in summary.
    COMPRESSED_SUMMARY_PATH (str): Path for compressed summary.
    COMPRESSED_DATES_PATH (str): Path for dates of sentences in compressed
        summary.
    STOPWORDS (list of str): Stopwords.
    THRESHOLD (float): Threshold for Word Mover's Distance.
    MODEL (gensim model): Model for Word2Vec.
    VECTORIZER (vectorizer): Vectorizer for tfidf.
"""

import gensim.downloader as api
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import download
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

TOPIC = 'symptom'
SUMMARY_PATH = '../initial-extraction/out/summaries/' + TOPIC + '_extracted.txt'
DATES_PATH = '../initial-extraction/out/dates/' + TOPIC + '_extracted_dates.txt'
COMPRESSED_SUMMARY_PATH = 'out/summaries/filtered_' + TOPIC + '.txt'
COMPRESSED_DATES_PATH = 'out/dates/filtered_' + TOPIC + '_dates.txt'

STOPWORDS = stopwords.words('english')
THRESHOLD = 1.51
MODEL = api.load('word2vec-google-news-300')
VECTORIZER = TfidfVectorizer()

def get_sentences():
    """
    Returns:
        (list of str): Summary sentences.
    """
    with open(SUMMARY_PATH, 'r') as f:
        return f.read().splitlines()

def get_split_sentences(sentences):
    """
    Returns:
        (list of list of str): List of list of words where each inner list is
            a sentence.
    """
    return [sentence.lower().split() for sentence in sentences]

def get_tfidf_df(sentences):
    """
    Args:
        sentences (list of str): Summary sentences.

    Returns:
        (pandas DataFrame): DataFrame containing tfidf info on `sentences`.
    """
    vectors = VECTORIZER.fit_transform(sentences)
    feature_names = VECTORIZER.get_feature_names()
    dense = vectors.todense()
    dense_list = dense.tolist()
    df = pd.DataFrame(dense_list, columns=feature_names)
    return df

def get_dates():
    """
    Returns:
        (list of str): Dates.
    """
    with open(DATES_PATH, 'r') as f:
        return f.read().splitlines()

def get_score(s, df):
    """
    Args:
        s (str): Some string.
        df (pandas DataFrame): DataFrame containing tfidf info.

    Returns:
        (float): Summation of tfidf scores of `s`.
    """
    score = 0
    for word in s:
        word = strip_symbols(word)
        score += df[word]
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

def get_compressed_summary(sentences, split_sentences, df, dates):
    """
    Args:
        sentences (list of str): Summary sentences.
        split_sentences (list of list of str): List of list of words where each
            inner list is a sentence.
        df (pandas DataFrame): DataFrame containing tfidf info.
        dates (list of str): Dates.

    Returns:
        (list of str): Compressed summary sentences.
    """
    compressed_summary = []
    compressed_dates = []

    for i, split_sentence in enumerate(split_sentences):
        split_sentences[i] = [word for word in split_sentence if word not in STOPWORDS]
        redundant = False
        for j in reversed(range(i)):
            distance = MODEL.wmdistance(split_sentence, split_sentences[j])
            if distance < THRESHOLD:
                redundant = True
                break
        if redundant:
            sentence1 = ' '.join(split_sentence)
            sentence2 = ' '.join(split_sentences[j])

            sentence1_score = get_score(split_sentence, df)
            sentence2_score = get_score(split_sentences[j], df)
            print(sentence1_score)
            print(sentence2_score)

    return compressed_summary

sentences = get_sentences()
df = get_tfidf_df(sentences)
split_sentences = get_split_sentences(sentences)
dates = get_dates()
compressed_summary = get_compressed_summary(sentences, split_sentences, df, dates)
