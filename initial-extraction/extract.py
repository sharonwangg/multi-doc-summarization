from __future__ import print_function
from nltk.stem import *
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer
import argparse
import numpy as np
from spacy.pipeline import SentenceSegmenter
from spacy.lang.en import English
import numpy as np
import numpy.linalg as la
import re
from allennlp.predictors import Predictor
from allennlp.models.archival import load_archive

textfile      = open('in/text.txt', 'r', encoding='utf8')
datesfile     = open('in/dates.txt', 'r', encoding='utf8')
topicsfile    = open('in/res_topics.txt', 'r', encoding='utf8')
stopwordsfile = open('in/stopwords.txt', 'r', encoding='utf8')
vectorsfile   = open('in/jose.txt', 'r', encoding='utf8')

threshold = 0.3
stopwords = frozenset(
    [word.strip() for word in stopwordsfile.read().splitlines()])
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz")
stemmer = SnowballStemmer("english")

# initialize the sentencizer
nlp = English()
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)

def noDay(sentence):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "weekend", "Weekend", "month", "Month"]
    return not any(ele in sentence for ele in days)
def deleteSymbols(words):
    for i in range(len(words)):
        words[i] = words[i].strip()
        words[i] = words[i].strip('~')
        words[i] = words[i].strip('`')
        words[i] = words[i].strip('!')
        words[i] = words[i].strip('@')
        words[i] = words[i].strip('#')
        words[i] = words[i].strip('$')
        words[i] = words[i].strip('%')
        words[i] = words[i].strip('^')
        words[i] = words[i].strip('&')
        words[i] = words[i].strip('*')
        words[i] = words[i].strip('(')
        words[i] = words[i].strip(')')
        words[i] = words[i].strip('-')
        words[i] = words[i].strip('_')
        words[i] = words[i].strip('+')
        words[i] = words[i].strip('=')
        words[i] = words[i].strip('{')
        words[i] = words[i].strip('}')
        words[i] = words[i].strip('[')
        words[i] = words[i].strip(']')
        words[i] = words[i].strip('|')
        words[i] = words[i].strip('\\')
        words[i] = words[i].strip(':')
        words[i] = words[i].strip(';')
        words[i] = words[i].strip("'")
        words[i] = words[i].strip('"')
        words[i] = words[i].strip(',')
        words[i] = words[i].strip('<')
        words[i] = words[i].strip('>')
        words[i] = words[i].strip('.')
        words[i] = words[i].strip('?')
        words[i] = words[i].strip('/')
    return words
def deleteStopwords(phrase):
    newphrase = []
    for ngram in phrase:
        if ngram.strip().lower() not in stopwords:
            newphrase.append(ngram.strip().lower())
    return newphrase
def normalize(phrase, stemmer):
    for i, ngram in enumerate(phrase):
        phrase[i] = stemmer.stem(ngram.strip().lower())
def getPhrases():
    topicslines = topicsfile.read().splitlines()
    phrases = []
    for i in range(0, len(topicslines), 2):
        curr_phrases = [stemmer.stem(topicslines[i].split()[1][1:][:-2].strip().lower())]
        for phrase in topicslines[i + 1].split():
            curr_phrases.append(stemmer.stem(phrase).strip().lower())
        phrases.append(curr_phrases)
    return [i[0] for i in phrases], phrases
def getProcessedPhrases():
    print("processing phrases...")

    for i, phrase in enumerate(phrases):
        phrase = deleteSymbols(phrase)
        phrase = deleteStopwords(phrase)
        normalize(phrase, stemmer)
        phrases[i] = list(set(phrase))

    return phrases
def getVectors():
    print("getting vectors...")
    word_to_vector = {}
    for line in vectorsfile.read().splitlines():
        word = ""
        vector = [float(i) for i in line.split()[-100: ]]
        for i in range(len(line.split()[ :-100])):
            word += (' ' + stemmer.stem((line.split()[ :-100][i]).strip().lower()))
        word = word.strip()
        word_to_vector[word] = vector
    return word_to_vector
def hasXNGrams(phrase, words, topic, x):
    appearanceCounter = 0
    for ngram in phrase:
        if ngram in words and ngram != topic:
            appearanceCounter += 1
    return (appearanceCounter >= x)
def getWords(sentence):
    words = sentence.split()
    words = deleteSymbols(words)
    # stemmize the words
    for j in range(len(words)):
        words[j] = stemmer.stem(words[j]).strip().lower()
    return words
def shouldAddSentence(words, topic, phrase, sentence, summary):
    return (((topic in words and hasXNGrams(phrase, words, topic, 1))
        or hasXNGrams(phrase, words, topic, 2))
        and noDay(sentence.strip())
        and words[0] != "but"
        and words[0] != "and"
        and sentence[-1] != "?"
        and len(words) >= 5
        and sentence not in summary)

# set up topics and phrases
topics, phrases = getPhrases()
phrases = getProcessedPhrases()         # delete symbols, stopwords, and repeats. strip, lowercase, and stemmize

word_to_vector = getVectors()           # dict for spherical text embedding

articles = textfile.read().splitlines() # list of articles from dataset
dates = datesfile.read().splitlines()   # list of dates from dataset

print("extracting sentences...")
summaries = []
summary_dates = []
for l in range(len(topics)):
    summaries.append([])
    summary_dates.append([])

def main():
    #print(predictor.predict(sentence="Did Uriah honestly think he could beat the game in under three hours?")
    i = 0
    for article in articles:
        if True:
        #if i < 100:
            print("reading article " + str(i + 1))
            i += 1

            article = nlp(article)
            for sentence in list(article.sents):
                sentence = str(sentence)
                words = getWords(sentence)

                for k in range(len(phrases)):
                    if shouldAddSentence(words, topics[k], phrases[k], sentence, summaries[k]):
                        topic_vector = word_to_vector[topics[k]]
                        relevancy_score = 0
                        for word in words:
                            if word not in word_to_vector:
                                continue
                            word_vector = word_to_vector[word]
                            if la.norm(topic_vector) * la.norm(word_vector) != 0:
                                current_cos = np.dot(topic_vector, word_vector) / (la.norm(topic_vector) * la.norm(word_vector))
                                relevancy_score += current_cos

                        if relevancy_score / len(words) > threshold:
                            summaries[k].append(sentence.strip())
                            summary_dates[k].append(dates[i])
        else:
            break

    for i in range(len(summaries)):
        extractedfile = open('out/summaries/' + topics[i] + '_extracted.txt', 'w', encoding='utf8')
        extracted_datesfile = open('out/datetimes/' + topics[i] + '_extracted_datetimes.txt', 'w', encoding='utf8')
        summary = summaries[i]
        for j in range(len(summary)):
            sentence = summary[j]
            extractedfile.write(sentence.strip() + '\n')
            extracted_datesfile.write(summary_dates[i][j] + '\n')

if __name__ == '__main__':
    main()
