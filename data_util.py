from nltk.corpus import stopwords
from allennlp.predictors import Predictor

PREDICTOR_PATH = 'https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz'


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

