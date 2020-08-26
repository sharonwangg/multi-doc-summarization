import gensim.downloader as api
import spacy
from nltk.corpus import stopwords
from allennlp.predictors import Predictor

NLP = spacy.load('en_core_web_sm')
PREDICTOR_PATH = 'https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz'
WORD2VEC_MODEL = api.load('word2vec-google-news-300')


def get_stopwords():
    """
    Returns:
        (list of str): Stopwords.
    """
    return stopwords.words('english')


def get_predictor():
    """
    Returns:
        (allennlp_models.structured_prediction.predictors.srl.SemanticRoleLabelerPredictor):
            A allennlp predictor object.
    """
    return Predictor.from_path(PREDICTOR_PATH)


STOPWORDS = get_stopwords()
PREDICTOR = get_predictor()

