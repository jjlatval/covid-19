from datasets import DatasetsSearcher
from doc2vec import Doc2VecEmbedding
from queries import QUERIES


def main():
    doc2vec = Doc2VecEmbedding('en')
    doc2vec.load()
    searcher = DatasetsSearcher()
    for query in QUERIES:
        similar_docs = doc2vec.find_most_similar_docs(query)
        print_out = "Query: {}".format(query) + '\n\n'
        for similar_doc in similar_docs:
            label = similar_doc[0]
            print_out += '{}; {:3f}'.format(searcher.find_title_by_label(label), similar_doc[1]) + '\n'
        print(print_out)


if __name__ == '__main__':
    main()
