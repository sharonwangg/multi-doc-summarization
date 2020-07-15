from nltk.corpus import stopwords
from nltk import download
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import gensim.downloader as api

summary_file    = open('../initial-extraction/out/summaries/symptom_extracted.txt', 'r', encoding='utf8')
dates_file      = open('../initial-extraction/out/datetimes/symptom_extracted_datetimes.txt', 'r', encoding='utf8')
newsummary_file = open('out/summaries/filtered_symptom.txt', 'w', encoding='utf8')
newdates_file   = open('out/datetimes/filtered_symptom_datetimes.txt', 'w', encoding='utf8')

stop_words = stopwords.words('english')
threshold = 1.51
model = api.load('word2vec-google-news-300')

summary = summary_file.read().splitlines()
summarylines = [sentence.lower().split() for sentence in summary]

dates = dates_file.read().splitlines()

summarylines[0] = [word for word in summarylines[0] if word not in stop_words]
newsummary_file.write(summary[0] + '\n')
newdates_file.write(dates[0] + '\n')

for i in range(1, 200):
    summarylines[i] = [word for word in summarylines[i] if word not in stop_words]

    redundant = False
    for j in reversed(range(0, i)):
        curr_distance = model.wmdistance(summarylines[i], summarylines[j])
        if curr_distance < threshold:
            print(0, summary[i])
            print(1, summary[j])
            print(curr_distance)
            redundant = True
            break

    if not redundant:
        newsummary_file.write(summary[i] + '\n')
        newdates_file.write(dates[i] + '\n')


# Obama: 1.586639587909434
# TV host: 1.5671082880477343
