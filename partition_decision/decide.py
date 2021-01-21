"""
Performs k-means clustering on extended summary.
"""
import os
import numpy as np
from nltk.corpus import stopwords

#from extend.extend import extended_summary
from sentence_details import SentenceDetails
from path_util import DATA_PATH

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score


def cluster(summary):
    """
    Args:
        summary: (list of strings, each a sentence)

    Returns:
        (dict from int to list of SentenceDetails): Clustered summary. Cluster ID maps to sub-summary.
    """
    #documents = [sentence.text for sentence in summary]
    documents = summary
    vectorizer = TfidfVectorizer(stop_words='english')
    print(documents)
    X = vectorizer.fit_transform(documents, documents)

    true_k = 5
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    clusters = {i: np.where(model.labels_ == i)[0] for i in range(model.n_clusters)}
    return clusters
    # for cluster_id, sentence_indices in clusters.items():
    #     print("cluster id", cluster_id)
    #     for sentence_index in sentence_indices:
    #         print(documents[sentence_index])
    #
    # print('Top terms per cluster:')
    # order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    # terms = vectorizer.get_feature_names()
    # for i in range(true_k):
    #     print('Cluster %d:' % i),
    #     for ind in order_centroids[i, :10]:
    #         print(' %s' % terms[ind]),
    #     print
    #
    # print('\n')
    # print('Prediction')
    #
    # Y = vectorizer.transform(['chrome browser to open.'])
    # prediction = model.predict(Y)
    # print(prediction)
    #
    # Y = vectorizer.transform(['My cat is hungry.'])
    # prediction = model.predict(Y)
    # print(prediction)


STOPWORDS = stopwords.words('english')


def delete_stopwords(string_list):
    """
    Args:
        s (list of str): Some list of strings.

    Returns:
        (str): `s` without stopwords.
    """
    return [s for s in string_list if s not in STOPWORDS]


def getExtendedSummary(extended_path):
    extended_summary = []
    simplified_extended_summary = []
    with open(extended_path, 'r') as f:
        for sentence in f.read().splitlines():
            extended_summary.append(sentence)
            simplified_sentence = " ".join(delete_stopwords(sentence.split()))
            simplified_extended_summary.append(simplified_sentence)
    return extended_summary[:25], simplified_extended_summary[:25]


def outputClusteredSummary(clustered_summary, documents, clustered_path):
    with open(clustered_path, 'w') as f:
        for cluster_id, sentence_indices in clustered_summary.items():
            f.write(f'{str("cluster id")}\t{str(cluster_id)}\n')
            for sentence_index in sentence_indices:
                f.write(f'{str(documents[sentence_index])}\n')


#extended_summary = ["Business activity has stalled across much of the globe as the containment measures hammer the world economy, cementing economists' views of a deep global recession.",
                    #"Many states, including Georgia, Oklahoma, South Carolina and Ohio, have already moved to restart parts of their economies following weeks of mandatory lockdowns that have thrown nearly one in six American workers out of their jobs.",
                    #"The council rejects the \"two quarters\" rule and instead defines a recession as a \"pronounced, persistent and pervasive decline in aggregate economic activity\" based largely on GDP and the job market. There are no hard and fast rules for declaring a recession, although one rule of thumb used by economists is that an economy is probably in one if it has shrunk for two three-month periods in a row. The council, which monitors recessions and recoveries in Canada, said the economy peaked in February, just before drastic measures to slow the spread of the coronavirus were implemented across the country."]

EXTENDED_PATH = os.path.join(DATA_PATH, 'step5_extended_summary', 'economy_extended_summary.txt')
extended_summary, simplified_extended_summary = getExtendedSummary(EXTENDED_PATH)
clustered_summary = cluster(simplified_extended_summary)
CLUSTERED_PATH = os.path.join(DATA_PATH, 'economy_clustered_summary.txt')
outputClusteredSummary(clustered_summary, extended_summary, CLUSTERED_PATH)