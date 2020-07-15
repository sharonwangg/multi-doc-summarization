from datetime import datetime

summaryfile          = open('filtered_symptom.txt', 'r', encoding='utf8')
dates_timesfile      = open('filtered_symptom_dates.txt', 'r', encoding='utf8')
organizedsummaryfile = open('organized_symptom.txt', 'w', encoding='utf8')

dates_times = dates_timesfile.read().splitlines()
dates_times = [date_time[1:-1] for date_time in dates_times]

sentences = summaryfile.read().splitlines()

dates_times_to_sentence = {dates_times[i]: sentences[i] for i in range(len(dates_times))}

dates_times.sort(key=lambda date: datetime.strptime(date, '%Y-%m-%d %H:%M'))

for date_time in dates_times:
    sentence = dates_times_to_sentence[date_time]
    organizedsummaryfile.write(sentence + '\n')