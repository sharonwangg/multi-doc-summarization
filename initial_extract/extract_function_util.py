import numpy as np
import numpy.linalg as la
from data_util import PREDICTOR
from function_util import delete_stopwords, strip_symbols, normalize
from initial_extract.extract_data_util import TOPICS_LINES, VECTORS_LINES, DAYS, GENERAL_WORDS


def has_day(s):
    """
    Args:
        s (str): Some string.

    Returns:
        (bool): True if `s` contains a day.
    """
    return any(day in s.lower() for day in DAYS)


def get_processed_phrase(phrase):
    """ Returns `phrase` without stopwords and where each ngram is stripped of symbols.
    Args:
        phrase (list of str): List of ngrams.
    Returns:
        (list of str): `phrase` without stopwords and where each ngram is stripped of symbols.
    """
    phrase = delete_stopwords(phrase)
    for i, ngram in enumerate(phrase):
        phrase[i] = strip_symbols(ngram)
    return phrase


def get_topic_to_phrase():
    """
    Returns:
        (dict from str to list of str): Maps topics to their respective phrases.
    """
    topic_to_phrase = {}
    for i in range(0, len(TOPICS_LINES), 2):
        topic = TOPICS_LINES[i].split()[1][1:][:-2].strip().lower()
        phrase = []
        for ngram in TOPICS_LINES[i + 1].split():
            phrase.append(normalize(ngram))
        topic_to_phrase[topic] = get_processed_phrase(phrase)
    return topic_to_phrase


def get_word_to_vector():
    """
    Returns:
        (dict from str to list of floats): Dictionary for JoSe word embedding.
    """
    word_to_vector = {}
    for line in VECTORS_LINES:
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
    return appearance_counter >= desired_count


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
            if subject in GENERAL_WORDS or object in GENERAL_WORDS:
                return True
    return False


def has_improper_pronoun(sentence):
    for token in sentence:
        if 'PRON' in token.pos_:
            return True
    return False


def contains_theme(topic, words, phrase):
    normalized_topic = normalize(topic)
    return ((normalized_topic in words and has_x_ngrams(normalized_topic, phrase, words, desired_count=1))
            or has_x_ngrams(normalized_topic, phrase, words, desired_count=2))


def is_quality_sentence(topic, phrase, words, sent, summary):
    """
    Args:
        topic (str): Category name.
        phrase (list of str): List of ngrams relating to `topic`.
        str_sentence (str): Some string representing a sentence.
        summary (list of str): List of str_sentences.

    Returns:
        (bool): Returns true if `sentence` should be added to the summary.
    """
    normalized_topic = normalize(topic)
    str_sent = sent.text
    return (((normalized_topic in words and has_x_ngrams(normalized_topic, phrase, words, desired_count=1))
        or has_x_ngrams(normalized_topic, phrase, words, desired_count=2))
        and not has_day(str_sent.strip())
        and words[0] != "but"
        and words[0] != "and"
        and str_sent[-1] != "?"
        and len(words) >= 5
        and str_sent.strip() not in summary
        and not has_improper_pronoun(sent))


def calculate_relevancy_score(topic, words, word_to_vector):
    """
    Args:
        topic (str): Category name.
        words (list of str): List of words representing a sentence.
    Returns:
        (float): Relevancy score of `words` to `topic`.
    """
    topic_vector = word_to_vector[topic]
    relevancy_score = 0
    for word in words:
        if word not in word_to_vector:
            continue
        word_vector = word_to_vector[word]
        if la.norm(topic_vector) * la.norm(word_vector) != 0:
            current_cos = np.dot(topic_vector, word_vector) / (la.norm(topic_vector) * la.norm(word_vector))
            relevancy_score += current_cos
    relevancy_score /= len(words)
    return relevancy_score


def get_str_article(article):
    """
    Args:
        article (list of sentences): List of articles which are lists
            of sentences.

    Returns:
        (str): `article` in str format.
    """
    str_article = ""
    for sentence in article:
        str_article += (' ' + str(sentence))
    return str_article


def sort_by_relevancy_score(all_sentence_details):
    """ Sorts SentenceDetails in `all_sentence_details` by its cosine similarity score (respective to the topic).
    Args:
        all_sentence_details (list of SentenceDetails): A list of sentences with corresponding dates, scores, and
            original articles.
    Returns:
        (list of SentenceDetails): `all_sentence_details` but sorted by relevancy score.
    """
    for topic, sentence_details in all_sentence_details.items():
        sentence_details.sort(key=lambda sentence_detail: sentence_detail.relevancy_score, reverse=True)
    return all_sentence_details