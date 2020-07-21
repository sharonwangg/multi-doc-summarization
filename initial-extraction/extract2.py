"""
Extracts relevant sentences from corpus related to category names.

Attributes:
    THRESHOLD (float): The threshold for cosine similarity.
    GENERAL_WORDS (frozenset of str): Words that shouldn't be a sub/obj.
    STOPWORDS (list of str): Stopwords.
    STEMMER (SnowballStemmer): Stems words.
    PREDICTOR (SemanticRoleLabelerPredictor): SRL object.
"""

import spacy
import numpy as np
import numpy.linalg as la
from nltk.stem.snowball import SnowballStemmer
from data_util import get_stopwords, get_general_words, get_topics_lines, get_vectors_lines, get_predictor, get_articles, get_datetimes

THRESHOLD = 0.3
GENERAL_WORDS = get_general_words()
STOPWORDS = get_stopwords()
STEMMER = SnowballStemmer('english')
PREDICTOR = get_predictor()

def has_day(s):
    """
    Args:
        s (str): Some string.

    Returns:
        (bool): True if `s` contains a day.
    """
    days = ["monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "weekend",
            "month"]
    return any(day in s.lower() for day in days)

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

def delete_stopwords(string_list):
    """
    Args:
        s (list of str): Some list of strings.

    Returns:
        (str): `s` without stopwords.
    """
    return [s for s in string_list if s not in STOPWORDS]

def normalize(s):
    """
    Args:
        s (str): Some string.

    Returns:
        (str): `s` but stemmized, stripped, and lowercased
    """
    return STEMMER.stem(s.strip().lower())

def get_topics_and_phrases():
    """
    Returns:
        (list of str): List of topics extracted from res_x file.
        (2D list of str): A list of lists of phrases (one list for each topic).
    """
    topics_lines = get_topics_lines()
    phrases = []
    for i in range(0, len(topics_lines), 2):
        curr_phrases = [normalize(topics_lines[i].split()[1][1:][:-2])]
        for phrase in topics_lines[i + 1].split():
            curr_phrases.append(normalize(phrase))
        phrases.append(curr_phrases)
    topics = [i[0] for i in phrases]
    return topics, phrases

def get_processed_phrases():
    """
    Returns:
        (2D list of str): A list of lists of phrases (one list for each topics).
    """
    for i, phrase in enumerate(phrases):
        phrases[i] = delete_stopwords(phrase)
        for j, ngram in enumerate(phrases[i]):
            phrases[i][j] = strip_symbols(ngram)
    return phrases

def get_vectors():
    """
    Returns:
        (dict from str to list of floats): Dictionary for JoSe word embedding.
    """
    word_to_vector = {}
    vectors_lines = get_vectors_lines()
    for line in vectors_lines:
        word = ""
        vector = [float(i) for i in line.split()[-100: ]]
        for i in range(len(line.split()[:-100])):
            word += (' ' + normalize(line.split()[ :-100][i]))
        word = word.strip()
        word_to_vector[word] = vector
    return word_to_vector

def has_x_ngrams(topic, phrase, words, desired_count):
    """
    Args:
        topic (str): Category name.
        phrase (list of str): List of ngrams relating to `topic`.
        words (list of str): List of words in a sentence.
        desired_count (int): Minimum number of ngrams required.
    Returns:
        (bool): True if there are at least `desired_count` ngrams in `words`.
    """
    appearance_counter = 0
    for ngram in phrase:
        if ngram in words and ngram != topic:
            appearance_counter += 1
    return (appearance_counter >= desired_count)

def get_words(s):
    """
    Args:
        s (str): Some string.
    Returns:
        (list of str): List of words in `s` that are stripped of symbols
                       and normalized.
    """
    words = s.split()
    for i, word in enumerate(words):
        words[i] = normalize(strip_symbols(word))
    return words

def sentence_too_general(sentence):
    """
    Args:
        sentence (str): String representing a sentence.
    Returns:
        (bool): True if `sentence` has a vague object and/or subject.
    """
    sentence_components = PREDICTOR.predict(sentence=sentence)['verbs']
    if len(sentence_components) > 0:
        description = sentence_components[0]['description'].split()
        for i in range(len(description)):
            subject = ''
            object = ''
            if description[i] == '[ARG0:':
                subject = description[1].lower()
                if subject[-1] == ']':
                    subject = subject[:-1]
            elif description[i] == '[ARG1:':
                object = description[1].lower()
                if object[-1] == ']':
                    object = object[:-1]
            if subject in general_words or object in general_words:
                return True
    return False

def is_quality_sentence(topic, phrase, words, str_sentence, summary):
    """
    Args:
        topic (str): Category name.
        phrase (list of str): List of ngrams relating to `topic`.
        str_sentence (str): Some string representing a sentence.
        summary (list of str): List of sentences.
    Returns:
        (bool): Returns true if `sentence` should be added to the summary.
    """
    return (((topic in words and has_x_ngrams(topic, phrase, words, 1))
        or has_x_ngrams(topic, phrase, words, 2))
        and not has_day(str_sentence.strip())
        and words[0] != "but"
        and words[0] != "and"
        and str_sentence[-1] != "?"
        and len(words) >= 5)
        and str_sentence not in summary)

def calculate_relevancy_score(topic, words):
    """
    Args:
        topic (str): Category name.
        words (list of str): List of words representing a sentence.
    Returns:
        (float): Relevancy score.
    """
    topic_vector = word_to_vector[topics[k]]
    relevancy_score = 0
    for word in words:
        if word not in word_to_vector:
            continue
        word_vector = word_to_vector[word]
        if la.norm(topic_vector) * la.norm(word_vector) != 0:
            current_cos = np.dot(topic_vector, word_vector) / (la.norm(topic_vector) * la.norm(word_vector))
            relevancy_score += current_cos
    relevancy_score = relevancy_score / len(words)
    return relevancy_score

def initialize_structures():
    """
    Returns:
        summaries (2D list): list of list of sentences
        summary_dates (2D list): list of list of dates
        relevancy_scores (2D list): list of list of relevancy scores
    """
    summaries = []
    summary_dates = []
    relevancy_scores = []
    for i, topic in enumerate(topics):
        summaries.append([])
        summary_dates.append([])
        relevancy_scores.append([])
    return summaries, summary_dates, relevancy_scores

def extract_date(datetime):
    """
    Args:
        datetime (str): Some string representing a date and time.
    Returns:
        date (str): String representing the extracted date.
    """
    return datetime.split()[0]

topics, phrases = get_topics_and_phrases()
phrases = get_processed_phrases()
word_to_vector = get_vectors()

articles = get_articles()
datetimes = get_datetimes()

summaries, summary_dates, relevancy_scores = initialize_structures()


for i, article in enumerate(articles):
    print("summarizing article " + str(i + 1))
    for j, sentence in enumerate(article):
        str_sentence = str(sentences)
        words = get_words(str_sentence)
        for k, phrase in enumerate(phrases):
            if is_quality_sentence(topics[k], phrase, words, str_sentence, summaries[k]):
                summaries[k].append(str_sentence.strip())

                date = extract_date(datetimes[k])
                summary_dates[k].append(date)

                relevancy_score = calculate_relevancy_score(topics[k], words)
                relevancy_scores[k].append(relevancy_score)

for i, summary in enumerate(summaries):
    summary_file = open('out/summaries/' + topics[i] + '_extracted.txt', 'w')
    summary_dates_file = open('out/dates/' + topics[i] + '_extracted_dates.txt', 'w')
    for j, sentence in enumerate(summary):
        summary_file.write(sentence.strip() + '\n')
        summary_dates_file.write(summary_dates[i][j] + '\n')
