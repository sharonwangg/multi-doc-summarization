from datetime import datetime

TOPIC = 'symptom'
SUMMARY_PATH = '../compress/out/summaries/filtered_' + TOPIC + '.txt'
DATES_PATH = '../compress/out/dates/filtered_' + TOPIC + '_dates.txt'
ORDERED_SUMMARY_PATH = 'out/ordered_' + TOPIC + '.txt'

def get_dates():
    with open(DATES_PATH, 'r') as f:
        return [date_time for date_time in f.read().splitlines()]

def get_sentences():
    with open(SUMMARY_PATH, 'r') as f:
        return f.read().splitlines()

def get_timestamped_sentences(dates, sentences):
    timestamped_sentences = []
    for i, date in enumerate(dates):
        timestamped_sentences.append((date, sentences[i]))
    return timestamped_sentences

def output(timestamped_sentences):
    with open(ORDERED_SUMMARY_PATH, 'w') as f:
        for date, sentence in timestamped_sentences:
            f.write(f"{date}\t{sentence}\n")

dates = get_dates()
sentences = get_sentences()

{dates[i]: sentences[i] for i in range(len(dates))}

timestamped_sentences = get_timestamped_sentences(dates, sentences)
timestamped_sentences.sort(key=lambda i: datetime.strptime(i[0], '%Y-%m-%d'))

output(timestamped_sentences)
