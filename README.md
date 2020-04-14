# Covid-19 Open Research Dataset Challenge (CORD-19) repository

This repository contains the source code for my submission on [CORD-19 challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks?taskId=568) in Kaggle.

# Methodology

This repository contains a content based recommender system for COVID-19 related research questions (i.e. queries). 
This works by comparing a query to the body of research articles with which a vector space model (Doc2Vec-DBOW) has been trained, 
and the query will be compared against statements presented in research articles.

A Doc2Vec-DBOW model is trained with tokenized research articles as document tokens, and their unique paper-id as the 
only training tag. These training examples are fit to a Doc2Vec-DBOW model which then vectorizes the research articles 
(their abstract and body of text). A query is constructed by tokenizing a string input and then vectorizing that list of tokens.
Stopwords and punctuation is preserved because stopwords can influence the semantics of the query. Tokenization is done
using SpaCy. No stemming or lemmatization is used. In case of English tokens are usually good enough but with 
morphologically rich languages that have conjugations and compound words (such as German or Finnish), lemmatization and
compound word splitting may be needed.

The most similar results from all research papers in the Doc2Vec document embedding space are retrived by using cosine similarity
to determine the most similar articles with the query. Cosine similar is a good choice because the length of the vector
does not change it (i.e. short queries can be compared with abstracts and with lengthier bodies of text), and it is nicely
bound between {-1, 1} (although in high dimensional vector spaces the lower threshold will approach 0 in practice).

The most similar (in terms of document vector embedding cosine similarities) results are retrieved from the body of
research papers and listed in descending order of similarity with their titles, similarities and paper IDs.

# How to improve the approach

I opted to use Doc2Vec instead of more modern transfer learning methods (such as BERT) because in my experience working
with a limited and specific domain needs a model that can be trained for that specific domain. Also, BERT does not have
as good document level representation capabilities (yet) as Doc2Vec which has been created for the purpose of representing
lengthier text data in vector space. ELMo could have been another viable approach to address the problem as sentence level
statements rather than as whole abstracts or documents, i.e. it could do a better job at finding the exact statement. Also
Doc2Vec can be further enhanced if additional tags are used. I have experienced significant improvement on Doc2Vec models
with good tagging.

Needless to say, this repository was crafted within 3 hours using the methodology I am familiar with and that's why it does
not have basic functionalities such as:

- tests
- a database for more granular document section vectorization and document handling
- an appropriate approach with proper abstractions to handling dataset - document set - document when composing a document
to be fit to a ML model (and in case the 'recipe' for composing a document may vary)
- proper validation procedures for Doc2Vec (which because it being an unsupervised approach is notoriously difficult to validate), such as intracluster cohesion and document categorization metrics

## Requirements

- Access to [CORD-19 challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks?taskId=568) dataset
- OS: Ubuntu 18.04 LTS or newer
- Python3 with pip and virtualenv
- Disk: 10 GB of disk space
- Memory: 8GB of RAM

## How to setup

1. Clone the repository: `git clone ...`
2. Extract CORD-19 challenge dataset to cloned repository directory.
3. Initiate virtualenv: `virtualenv venv -p python3`
4. Activate created virtualenv: `source venv/bin/activate`
5. Install requirements: `pip install -r requirements.txt`
6. Install SpaCy additions: `bash spacy_install.sh` 

## How to train the ML model

1. Simply run: `python make_model.py`

## How to run research queries

1. Run queries: `python run_queries.py`

Alternatively, you can add / modify queries in `queries.py` and add them to `run_queries.py`

# How to test

- No tests are implemented
