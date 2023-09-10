import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
from collections import defaultdict
import pickle
import argparse
from pathlib import Path
import os

def merge_posting_lists(posting_list1, posting_list2):
    merged_list = []
    i = 0  # Pointer for posting_list1
    j = 0  # Pointer for posting_list2

    while i < len(posting_list1) and j < len(posting_list2):
        if posting_list1[i] == posting_list2[j]:
            merged_list.append(posting_list1[i])
            i += 1
            j += 1
        elif posting_list1[i] < posting_list2[j]:
            merged_list.append(posting_list1[i])
            i += 1
        else:
            merged_list.append(posting_list2[j])
            j += 1

    # Append remaining elements if any
    while i < len(posting_list1):
        merged_list.append(posting_list1[i])
        i += 1

    while j < len(posting_list2):
        merged_list.append(posting_list2[j])
        j += 1

    return merged_list


inverted_index = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path")
    parser.add_argument("query_path")
    args = parser.parse_args()
    model_queries = Path(args.model_path)
    queries = Path(args.query_path)
    with open(model_queries, "rb") as f:
        inverted_index = pickle.load(f)

    # Initialize a result set with all document IDs
    # Merge routine for "AND" operation
    with open(queries, "r") as q:
        query = q.readlines()
        for line in query:
            id  = line.split("\t")[0]
            sent = line.split("\t")[1]
            result_set = inverted_index[sent.split(" ")[0]]
            for term in sent.split(" ")[1:]:
                if term in inverted_index:
                    merged_list = merge_posting_lists(result_set, inverted_index[term])
            # print(merged_list)

            # Convert the result set back to a sorted list of document IDs
            result_list = sorted(merged_list)
            with open("results.txt", "a+") as r:
                r.write(id)
                r.write("\t")
                for item in result_list:
                    r.write(str(item)+ ' ')
                r.write("\n")

        