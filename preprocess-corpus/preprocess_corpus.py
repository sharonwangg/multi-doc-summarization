RAW_FILE_PATH = '../covid19dataset/articles.txt'
RAW_DATES_FILE_PATH = '../covid19dataset/dates.txt'
TEXT_FILE_PATH = 'out/articles.txt'
DATES_FILE_PATH = 'out/dates.txt'

def get_raw_articles():
    with open(RAW_FILE_PATH, 'r') as f:
        return f.read().splitlines()

def get_raw_dates():
    with open(RAW_DATES_FILE_PATH, 'r') as f:
        return f.read().splitlines()

def preprocess():
    articles = []
    raw_articles = get_raw_articles()
    raw_dates = get_raw_dates()
    with open(TEXT_FILE_PATH, 'w') as articles_file:
        with open(DATES_FILE_PATH, 'w') as dates_file:
            for i, article in enumerate(raw_articles):
                if article not in articles:
                    articles.append(article)
                    articles_file.write(article + '\n')
                    dates_file.write(raw_dates[i] + '\n')

preprocess()
