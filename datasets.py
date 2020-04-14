from os import chdir
from os.path import join
import glob
import json

from gensim.models.doc2vec import TaggedDocument
from tqdm import tqdm

from nlp import NLP

from config import ROOT_DIR


# Configure what kind of datasets exist
MIN_DOC_LEN = 20
BIORXIV_DATADIR = join(ROOT_DIR, 'biorxiv_medrxiv', 'biorxiv_medrxiv', 'pdf_json')
COMM_USE_DATADIR1 = join(ROOT_DIR, 'comm_use_subset', 'comm_use_subset', 'pdf_json')
COMM_USE_DATADIR2 = join(ROOT_DIR, 'comm_use_subset', 'comm_use_subset', 'pmc_json')
CUSTOM_LICENSE_DATADIR1 = join(ROOT_DIR, 'custom_license', 'custom_license', 'pdf_json')
CUSTOM_LICENSE_DATADIR2 = join(ROOT_DIR, 'custom_license', 'custom_license', 'pmc_json')
NONCOMM_USE_SUBSET_DATADIR1 = join(ROOT_DIR, 'noncomm_use_subset', 'noncomm_use_subset', 'pdf_json')
NONCOMM_USE_SUBSET_DATADIR2 = join(ROOT_DIR, 'noncomm_use_subset', 'noncomm_use_subset', 'pmc_json')

DATA_DIRS = [BIORXIV_DATADIR, COMM_USE_DATADIR1, COMM_USE_DATADIR2, CUSTOM_LICENSE_DATADIR1, CUSTOM_LICENSE_DATADIR2,
             NONCOMM_USE_SUBSET_DATADIR1, NONCOMM_USE_SUBSET_DATADIR2]

BIORXIV_DATASET_NAME = 'biorxiv'
COMM_USE_DATASET1_NAME = 'comm_use_1'
COMM_USE_DATASET2_NAME = 'comm_use_2'
CUSTOM_LICENSE_DATASET1_NAME = 'custom_license_1'
CUSTOM_LICENSE_DATASET2_NAME = 'custom_license_2'
NONCOMM_USE_SUBSET_DATASET1_NAME = 'noncomm_use_subset_1'
NONCOMM_USE_SUBSET_DATASET2_NAME = 'noncomm_use_subset_2'


DATASETS = [BIORXIV_DATASET_NAME, COMM_USE_DATASET1_NAME, COMM_USE_DATASET2_NAME, CUSTOM_LICENSE_DATASET1_NAME,
            CUSTOM_LICENSE_DATASET2_NAME, NONCOMM_USE_SUBSET_DATASET1_NAME, NONCOMM_USE_SUBSET_DATASET2_NAME]
DATASETS_PATHS = {k: v for (k, v) in zip(DATASETS, DATA_DIRS)}

# TODO: terminology is a bit bad here. In reality datasets can consists of document sets which consists of documents,
# TODO i.e. a document set would be the appropriate abstraction level from which documents are derived with their
# TODO own "recipes", i.e. how to construct a document for machine learning purposes.


class BaseDataset:

    def __init__(self, path, name, **kwargs):
        self.path = path
        self.name = name
        self.extension = kwargs.get('extension', '.json')
        self.data_cols = kwargs.get('data_cols', {'metadata': ['title'], 'abstract': ['text']})  # abstract
        self.tag_cols = kwargs.get('tag_cols', {'root': ['paper_id']})

    @staticmethod
    def __get_entry_from_line(line, key, val):
        if key == 'root':
            return line.get(val, None)
        lines = line.get(key, {})
        if type(lines) == list:
            entries = []
            for l in lines:
                entry = l.get(val, None)
                if entry:
                    entries.append(entry)
            return '\n'.join(entries)
        return lines.get(val, None)

    def get_document_from_line(self, line):
        docs = []
        for key, vals in self.data_cols.items():
            for val in vals:
                entry = self.__get_entry_from_line(line, key, val)
                if entry:
                    docs.append(entry)
        return '\n'.join(docs)

    def get_tags_from_line(self, line):
        tags = []
        for key, vals in self.tag_cols.items():
            for val in vals:
                entry = self.__get_entry_from_line(line, key, val)
                if entry:
                    tags.append(entry)
        return tags

    def get_documents_labels(self):
        chdir(self.path)
        for fname in glob.glob('*' + self.extension):
            with open(fname, 'r') as f:
                data = json.load(f)
                doc = self.get_document_from_line(data)
                tags = self.get_tags_from_line(data)
                if tags and len(doc) >= MIN_DOC_LEN:  # Do not even consider too short documents
                    yield doc, tags


def initialize_dataset(name, **kwargs):
    return BaseDataset(path=DATASETS_PATHS[name], name=name, **kwargs)


class Datasets:

    def __init__(self, lang='en', **kwargs):
        """
        Do not use this object for anything else besides training models because normalization of documents
        takes a while.
        TODO: in an actual solution documents should be normalized and those normalized documents should be stored
        TODO: as corpus for fast loading when initiating a training procedure.
        :param lang: str
        :param kwargs: dict
        """
        self.datasets = kwargs.get('datasets', DATASETS)
        self.nlp = NLP(lang)
        self.tagged_docs = []
        self.__init_tagged_docs()  # The dataset is small enough to be loaded in RAM

    def __init_tagged_docs(self):
        for dataset_name in self.datasets:
            dataset = initialize_dataset(dataset_name)
            for doc, labels in dataset.get_documents_labels():
                self.tagged_docs.append(TaggedDocument(words=self.nlp.normalize_text(doc), tags=labels))

    def __iter__(self):
        for tagged_document in self.tagged_docs:
            yield tagged_document


class DatasetsSearcher:

    def __init__(self, **kwargs):
        """
        A handy searcher object that only has dataset titles and labels present.
        TODO: this object is slow to load. In an ideal solution this would be done in a database.
        :param lang: str
        :param kwargs: dict
        """
        self.datasets = kwargs.get('datasets', DATASETS)
        self.documents = {}
        self.__init_documents()

    def __init_documents(self):
        print("Loading datasets, this may take a couple of minutes...")
        for dataset_name in self.datasets:
            print("loading dataset {}".format(dataset_name))
            dataset = initialize_dataset(dataset_name, **{'data_cols': {'metadata': ['title']}})
            for doc, labels in tqdm(dataset.get_documents_labels()):
                # In this case labels only have one item and it's always unique.
                self.documents[labels[0]] = doc

    def find_title_by_label(self, label):
        return self.documents.get(label, None)
