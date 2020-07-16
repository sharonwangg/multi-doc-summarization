from datetime import datetime

summaryfile          = open('../compress/out/summaries/filtered_symptom.txt', 'r', encoding='utf8')
dates_timesfile      = open('../compress/out/datetimes/filtered_symptom_datetimes.txt', 'r', encoding='utf8')
organizedsummaryfile = open('out/ordered_symptom.txt', 'w', encoding='utf8')

dates_times = dates_timesfile.read().splitlines()
dates_times = [date_time[1:-1] for date_time in dates_times]

sentences = summaryfile.read().splitlines()

{dates_times[i]: sentences[i] for i in range(len(dates_times))}

timestamped_sentences = []
for i in range(len(dates_times)):
    timestamped_sentences.append((dates_times[i], sentences[i]))

timestamped_sentences.sort(key=lambda i: datetime.strptime(i[0], '%Y-%m-%d %H:%M'))

for date_time, sentence in timestamped_sentences:
    organizedsummaryfile.write(f"{date_time}\t{sentence}\n")
