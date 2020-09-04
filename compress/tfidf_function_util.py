import math

def get_tfidf(word, split_sentence, idfs):
    """
    Args:
        word (str): Some string representing a word.
        split_sentence (list of str): Sentence. List of words.
        idfs (dict from str to float): Dict mapping `word` to its idf value.

    Returns:
        (float): tfidf value of `word` in `split_sentence`.
    """
    tf = split_sentence.count(word.lower())
    if word in idfs.keys():
        return tf * idfs[word]
    return 0

def get_tfidf_vector(split_sentence, idfs):
    """
    Args:
        sentence (str): Some string representing a sentence.
        idfs (dict from str to float): Dict mapping words to their idf values.

    Returns:
        (dict from str to float): Dict mapping words to their tfidf values.
    """
    vector = {}

    for i in range(len(split_sentence)):
        word = split_sentence[i]
        vector[word] = get_tfidf(word, split_sentence[i], idfs)
    return vector

def get_idfs(split_sentences):
    """
    Args:
        split_sentences (list of list of str): List of list of words where each
            inner list is a sentence.

    Returns:
        (dict from str to float): Dict mapping words to their idf values.
    """
    document_counts = {}
    for sentence in split_sentences:
        for word in sentence:
            document_counts[word] = document_counts.get(word, 0) + 1

    idfs = {}
    for word, count in document_counts.items():
        idfs[word] = math.log(len(split_sentences) / count)

    return idfs


def get_score(split_sentence, idfs):
    """
    Args:
        sentence (str): Some string representing a sentence.
        idfs (dict from str to float): Dict mapping words to their idf values.

    Returns:
        (float): Summation of tfidf scores of `sentence`.
    """
    score = 0
    for tfidf in get_tfidf_vector(split_sentence, idfs).values():
        score += tfidf
    return score
