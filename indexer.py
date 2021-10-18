'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from linkedlist import LinkedList
from collections import OrderedDict


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        totalCount = 0
        for key, value in tokenized_document.items():
            totalCount = totalCount + value
        for key, value in tokenized_document.items():
            self.add_to_index(key, doc_id, value / totalCount)

    def add_to_index(self, term_, doc_id_, tfidf):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        if term_ not in self.inverted_index.keys():
            self.inverted_index[term_] = LinkedList()
            self.inverted_index[term_].insert_at_end(doc_id_, tfidf)
        else:
            self.inverted_index[term_].insert_at_end(doc_id_, tfidf)

    def display_function(self):
        for k, v in self.inverted_index.items():
            print(k, v.traverse_list())


    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
       
        for key,data in self.inverted_index.items():
            data.add_skip_connections(key)


    def calculate_tf_idf(self, no_of_doc):
        for data in list(self.inverted_index.values()):
            idf = no_of_doc / data.length
            data.calculate_tf_idf(idf)
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
