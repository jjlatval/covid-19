import re

import spacy


REPLACE_WITH_SPACE = ['\n', '\r', '\t', '\xa0', '/', '|', '\\', '\\n', '\\r', '\\t', '~', '_', '*', '#', '=', ':',
                      '&', '(', ')', '[', ']', '<', '>', '{', '}', '-', '+', '\\xa']
REPLACE_WITH_COMMA = ['、', '､']
REPLACE_WITH_EMPTY_STR = ['"', "'", "`", "´", "^", "¨"]


def clean_str(s):
    """
    A simple string cleaning function for filtering typical noise that the text may have.
    :param s: str
    :return: str
        A cleaned string.
    """
    s = str(s).lower()  # ensure that it is indeed a str + lower

    # CASE 1: Remove Internet noise.
    s = re.sub(r'<.*?>', ' ', s)  # Remove HTML tags.
    s = re.sub(r'http\S+\b', '', s)  # Remove links
    s = re.sub(r'\S*@\S*\s?\b', ' ', s)  # Remove email addresses, even faulty ones and @-mentions such as @mary

    # CASE 2: Normalize spacing and listings given noise present in data and remove difficult characters.
    for char in REPLACE_WITH_SPACE:
        s = s.replace(char, ' ')
    for char in REPLACE_WITH_COMMA:
        s = s.replace(char, ',')
    for char in REPLACE_WITH_EMPTY_STR:
        s = s.replace(char, '')

    s = re.sub(' +', ' ', s, re.UNICODE)  # Replace multiple spaces with one space.
    return s.strip()  # Remove leading and trailing whitespaces.


class NLP:

    def __init__(self, lang):
        self.lang = lang
        self.nlp = spacy.load(self.lang)

    def _tokenize(self, s):
        return [token.text for token in self.nlp(s)]

    def normalize_text(self, text):
        text = clean_str(text)
        return self._tokenize(text)
