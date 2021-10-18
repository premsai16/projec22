'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, next=None, tf=None, tfidf=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.tf = tf
        self.tfidf = tfidf
        self.skip_pointer = None


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""

    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            x = self.start_node
            while x is not None:
                traversal.append(x.value)
                x = x.next
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            print("No Element in the list")
            return
        else:
            x = self.start_node   
            while x is not None:
                if self.length > 2:
                    traversal.append(x.value)
                x = x.skip_pointer
            return traversal

    def add_skip_connections(self, key=None):
        if self.length > 2:
            n_skips = math.floor(math.sqrt(self.length))
            if n_skips * n_skips == self.length:
                n_skips = n_skips - 1
            self.dist = round(math.sqrt(self.length))
            n, s = self.start_node, self.start_node
            u = 0
            while u < int(n_skips):
                for i in range(self.dist):
                    n = n.next
                s.skip_pointer = n
                u += 1
                s = n
            print("----", key)

    def insert_at_end(self, value, tf, tfidf=None):
        """ Write logic to add new elements to the linked list.
            Insert the element at an appropriate position, such that elements to the left are lower than the inserted
            element, and elements to the right are greater than the inserted element.
            To be implemented. """
        new_node = Node(value=value, tf=tf, tfidf=tfidf)
        n = self.start_node
        self.length = self.length + 1

        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return

        elif self.start_node.value >= value:
            self.start_node = new_node
            self.start_node.next = n
            return

        elif self.end_node.value <= value:
            self.end_node.next = new_node
            self.end_node = new_node
            return

        else:
            while n.value < value < self.end_node.value and n.next is not None:
                n = n.next

            p = self.start_node
            while p.next != n and p.next is not None:
                p = p.next
            p.next = new_node
            new_node.next = n
            return

    def calculate_tf_idf(self, idf):
        if self.start_node is None:
            return
        else:
            n = self.start_node
            while n is not None:
                n.tfidf = n.tf * idf
                n = n.next
