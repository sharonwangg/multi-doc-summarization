from covid_summary.path_util import RAW_CORPUS_PATH, RAW_DATES_PATH, PREPROCESSED_CORPUS_PATH, PREPROCESSED_DATES_PATH

def get_raw_corpus():
    """ Reads raw corpus from `RAW_CORPUS_PATH`.
    Returns:
        (list of str): Raw corpus. List of articles.
    """
    with open(RAW_CORPUS_PATH, 'r') as f:
        return f.read().splitlines()

def get_raw_dates():
    """ Reads raw dates from `RAW_DATES_PATH`.
    Returns:
        (list of str): Raw dates. List of publish dates.
    """
    with open(RAW_DATES_PATH, 'r') as f:
        return f.read().splitlines()

def preprocess(raw_corpus, raw_dates):
    """ Removes identical articles in `raw_corpus` and outputs the resulting preprocessed corpus and dates.
    Args:
        raw_corpus (list of str): List of articles.
        raw_dates (list of str): List of publish dates.
    """
    articles = []
    with open(PREPROCESSED_CORPUS_PATH, 'w') as preprocessed_corpus_file:
        with open(PREPROCESSED_DATES_PATH, 'w') as preprocessed_dates_file:
            for i, article in enumerate(raw_corpus):
                if article not in articles:
                    articles.append(article)
                    preprocessed_corpus_file.write(article + '\n')
                    preprocessed_dates_file.write(raw_dates[i] + '\n')

raw_corpus = get_raw_corpus()
raw_dates = get_raw_dates()
preprocess(raw_corpus, raw_dates)
