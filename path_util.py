"""
Utility module for storing txt file paths.

Attributes:
    DATA_PATH (str): Path where all txt files are stored.
    RAW_CORPUS_PATH (str): Path for the raw corpus.
    RAW_DATE_PATH (str): Path for the raw dates corresponding to the raw corpus.
    PREPROCESSED_CORPUS_PATH (str): Path for the preprocessed corpus.
    PREPROCESSED_DATES_PATH (str): Path for the dates corresponding to the preprocessed corpus.
"""
import os

DATA_PATH = os.path.join('/',
                         'Users',
                         'sharonwang',
                         'Desktop',
                         'MyStuff',
                         'UIUC',
                         'Summer20',
                         'Research',
                         'multi_doc_summ_proj',
                         'covid19dataset')

# Paths needed for `preprocess_corpus`.
RAW_CORPUS_PATH = os.path.join(DATA_PATH, 'raw_data', 'raw_corpus.txt')
RAW_DATETIMES_PATH = os.path.join(DATA_PATH, 'raw_data', 'raw_datetimes.txt')
PREPROCESSED_DATA_PATH = os.path.join(DATA_PATH, 'preprocessed_data', 'preprocessed_data.txt')

# Path needed for `extract`.
JOSE_VECTORS_PATH = os.path.join(DATA_PATH, 'jose.txt')

# Paths needed for `compress`.
TEXT_PATH = '../preprocess_corpus/out/articles.txt'
DATETIMES_PATH = '../preprocess_corpus/out/dates.txt'
TOPICS_PATH = 'in/res_items.txt'
VECTORS_PATH = 'in/jose.txt'