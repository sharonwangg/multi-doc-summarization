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
                         'covid_summary',
                         'covid19dataset')

'''
Input and output files for `preprocess_corpus`. 
'''
RAW_CORPUS_PATH = os.path.join(DATA_PATH, 'raw_corpus.txt')
RAW_DATES_PATH = os.path.join(DATA_PATH, 'raw_dates.txt')
PREPROCESSED_CORPUS_PATH = os.path.join(DATA_PATH, 'preprocessed_corpus.txt')
PREPROCESSED_DATES_PATH = os.path.join(DATA_PATH, 'preprocessed_dates.txt')

TEXT_PATH = '../preprocess_corpus/out/articles.txt'
DATETIMES_PATH = '../preprocess_corpus/out/dates.txt'
TOPICS_PATH = 'in/res_items.txt'
VECTORS_PATH = 'in/jose.txt'