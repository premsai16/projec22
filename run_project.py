'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def _merge(self, list1_tfidf, list2_tfidf):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        if list1_tfidf > list2_tfidf:
            return 1
        else:
            return 2

    def _daat_and(self, all_query_posting_list):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        all_query_posting_list = sorted(
            all_query_posting_list,
            key=lambda x: x.length)
        list1 = all_query_posting_list[0].start_node
        temp = 0
        i = 1
        while(i < len(all_query_posting_list)):
            lil = LinkedList()
            list2 = all_query_posting_list[i].start_node
            while list1 is not None and list2 is not None:
                temp = temp + 1
                if list1.value == list2.value:
                    max_tf_list = self._merge(list1.tfidf, list2.tfidf)
                    if max_tf_list == 1:
                        lil.insert_at_end(list1.value, list1.tf, list1.tfidf)
                    else:
                        lil.insert_at_end(list2.value, list2.tf, list2.tfidf)
                    list1 = list1.next
                    list2 = list2.next
                elif list2.value > list1.value:
                    list1 = list1.next
                else:
                    list2 = list2.next
            list1 = lil
            i = i + 1
        return lil, temp

    def _daat_and_skip(self, all_query_posting_list):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        all_query_posting_list = sorted(
            all_query_posting_list,
            key=lambda x: x.length)
        list1 = all_query_posting_list[0].start_node
        temp = 0
        i = 1
        while(i < len(all_query_posting_list)):
            lil = LinkedList()
            list2 = all_query_posting_list[i].start_node
            while list1 is not None and list2 is not None:
                temp = temp + 1
                if list1.value == list2.value:
                    max_tf_list = self._merge(list1.tfidf, list2.tfidf)
                    if max_tf_list == 1:
                        lil.insert_at_end(list1.value, list1.tf, list1.tfidf)
                    else:
                        lil.insert_at_end(list2.value, list2.tf, list2.tfidf)
                    list1 = list1.next
                    list2 = list2.next
                elif list2.value > list1.value:
                    if list1.skip_pointer is not None and list1.skip_pointer.value <= list2.value:
                        while list1.skip_pointer is not None and list1.skip_pointer.value <= list2.value:
                            list1 = list1.skip_pointer
                            
                    else:
                        list1 = list1.next
                else:
                    if list2.skip_pointer is not None and list2.skip_pointer.value <= list1.value:
                        while list2.skip_pointer is not None and list2.skip_pointer.value <= list1.value:
                            list2 = list2.skip_pointer
                            # count = count + 1
                    else:
                        list2 = list2.next
            lil.add_skip_connections()
            list1 = lil
            i = i + 1
        return lil, temp

    def _get_postings(self):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        self.indexer.add_skip_connections(self, key=None)
        raise NotImplementedError

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r') as fp:
            doc = fp.readlines()
            for line in tqdm(doc):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                self.indexer.generate_inverted_index(
                    doc_id, tokenized_document)
        self.indexer.sort_terms()
        self.indexer.display_function()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf(len(doc))

    def sort_according_TFIDIF(self, list):
        node = list.start_node
        tfidf = []
        while node is not None:
            tfidf.append((node.tfidf, node.value))
            node = node.next
        tfidf = sorted(tfidf, key=lambda x: x[0])
        tfidf.reverse()
        doclist = []
        for doc in tfidf:
            doclist.append(doc[1])
        return doclist

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""

            # Tokenized query. To be implemented.
            input_term_arr = self.preprocessor.tokenizer(query)
            posting_list_query = []
            for term in input_term_arr:
                postings, skip_postings = self.indexer.inverted_index[term].traverse_list(
                ), self.indexer.inverted_index[term].traverse_skips(
                )
                posting_list_query.append(self.indexer.inverted_index[term])

                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""

                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings
            merge_list, no_of_compare = self._daat_and(posting_list_query)
            merge_list_skip, no_of_compare_skip = self._daat_and_skip(
                posting_list_query)
            print(no_of_compare)
            merge_list_sorted = self.sort_according_TFIDIF(merge_list)
            merge_list_skip_sorted = self.sort_according_TFIDIF(
                merge_list_skip)

            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = merge_list.traverse_list(), merge_list_skip.traverse_list(), merge_list_sorted, merge_list_skip_sorted
            and_comparisons_no_skip, and_comparisons_skip, \
                and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = no_of_compare, no_of_compare_skip, no_of_compare, no_of_compare_skip
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            

            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(
                and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(
                and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(
                and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(
                and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip(
            )]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip(
            )]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip(
            )]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip(
            )]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip(
            )]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip(
            )]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip(
            )]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip(
            )]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip(
            )]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip(
            )]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip(
            )]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip(
            )]['num_comparisons'] = and_comparisons_skip_sorted
        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str,
                        help="Corpus File name, with path.")
    parser.add_argument("--output_location", type=str,
                        help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")

    argv = parser.parse_args()

    # corpus = argv.corpus
    # output_location = argv.output_location
    # username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    corpus = "data/input.txt"
    output_location = argv.output_location
    username_hash = "chitrava"

    """ Initialize the project runner"""
    runner = ProjectRunner()

    runner.run_indexer(corpus)
    runner.run_queries(["hello world", "hello swimming", "random swimming", "swimming going"], "")
    # app.run(host="0.0.0.0", port=9999)
