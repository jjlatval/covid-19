from os.path import join
import logging

from gensim.models import Doc2Vec

from datasets import Datasets
from nlp import NLP

from config import MODELS_DIR

# No need to deviate from common good parameters except for:
# epochs - because the dataset is small
# min_count - because the dataset is small

# In some recommender system applications negative ns_exponent values (such as -0.5) may be better; please
# refer to Gensim documentation to find that paper, if you are interested.

DOC2VEC_PARAMS = {
    'dm': 0,
    'hs': 0,
    'negative': 5,
    'ns_exponent': 0.75,
    'sample': 10e-5,
    'dbow_words': 1,
    'workers': 12,
    'vector_size': 300,
    'min_count': 3,
    'window': 5,
    'epochs': 10,
    'alpha': 0.025,
    'min_alpha': 0.0025,
}


class Doc2VecEmbedding:

    def __init__(self, lang='en'):
        self.lang = lang
        self.model = None
        self.nlp = NLP(self.lang)

    def __get_model_fpath(self):
        return join(MODELS_DIR, 'doc2vec_%s.model' % self.lang)

    def load(self):
        self.model = Doc2Vec.load(self.__get_model_fpath())

    def fit(self, **kwargs):
        logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
        logging.root.level = logging.INFO
        datasets = Datasets()
        params = DOC2VEC_PARAMS
        self.model = Doc2Vec(datasets.tagged_docs, **params)
        self.model.save(self.__get_model_fpath())

    def vectorize(self, text):
        tokens = self.nlp.normalize_text(text)
        return self.model.infer_vector(tokens, steps=256)

    def find_most_similar_docs(self, text, topn=10):
        vector = self.vectorize(text)
        return self.model.docvecs.most_similar(positive=[vector], topn=topn)
