'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from typing import Counter
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        """ Implement logic to pre-process & tokenize document text.
            Write the code in such a way that it can be re-used for processing the user's query.
            To be implemented."""
        text = re.sub('[^a-zA-Z0-9 ]', ' ', text)
        text = text.split()
        text = text.strip()
        text = text.lower()
        filter_stop_word = text[:]
        for stopword in text[:]:
            if stopword in self.stop_words:
                filter_stop_word.remove(stopword)
        stem_words = []
        for word in filter_stop_word:
            stem_words.append(self.ps.stem(word))
        c = Counter(stem_words)

        return c
