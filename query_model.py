from datasets import DatasetsSearcher
from doc2vec import Doc2VecEmbedding


class QueryModel:

    def __init__(self, lang='en'):
        self.doc2vec = Doc2VecEmbedding(lang)
        self.doc2vec.load()
        self.searcher = DatasetsSearcher()

    def query(self, query):
        """
        Vectorizes a query through Doc2Vec and uses DatasetSearcher to find the research paper with the title
        :param query: str
        :return: list[list, list, list...]
            A list of results with format: [label, similarity, title]
        """
        res = []
        sims = self.doc2vec.find_most_similar_docs(query)
        for sim in sims:
            label = sim[0]
            res.append([label, sim[1], self.searcher.find_title_by_label(label)])
        return res
