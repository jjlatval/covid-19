from doc2vec import Doc2VecEmbedding


def main():
    d = Doc2VecEmbedding(lang='en')
    d.fit()


if __name__ == '__main__':
    main()
