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

ROLL_NO = "22CS72P03"

def extract(file):
    """Extract the data as a python dictionary"""
    data = {}
    with open(file) as f:
        articles = f.read().split('\n.I')
        # print(articles)
    data = {(i+1):process(article) for i,article in enumerate(articles)}
    return data

def process(article):
    article = article.split('\n.T\n')[1]
    T, _, article = article.partition('\n.A\n')
    A, _, article = article.partition('\n.B\n')
    B, _, W = article.partition('\n.W\n')
    return {'T':T, 'A':A, 'B':B, 'W':W}

# Creating the corpus and preprocessing it to generate tokens
def create_corpus(semi_data):
    data = extract(semi_data)
    corpus = []
    for k, v in data.items():
        sent = v['W']
        try:
            nltk.data.find('corpora/stopwords.zip')
            # print("NLTK stopwords dataset is already downloaded.")
        except LookupError:
            print("NLTK stopwords dataset is not downloaded. You can download it using nltk.download('stopwords').")
        words = nltk.word_tokenize(sent)
        words = [word for word in words if word not in string.punctuation]
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]
        filtered_sentence = ' '.join(filtered_words)
        corpus.append(filtered_sentence)
    return corpus

# building the inverted index
def build_inverted_index(file):
    doc = create_corpus(file) # cleaned corpus
    inverted_index = defaultdict(list)
    for doc_id, doc_text in enumerate(doc):
        tokens = doc_text.lower().split()
        for token in tokens:
            inverted_index[token].append(doc_id)
    with open(f"model_queries_{ROLL_NO}.bin", "wb") as fh:
        pickle.dump(inverted_index, fh)
    # print("INVERTED INDEX HAS BEEN CREATED.")
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    cran_file = Path(args.path)
    build_inverted_index(cran_file)
    if os.path.exists(f"model_queries_{ROLL_NO}.bin") == True:
        print("INVERTED INDEX HAVE BEEN CREATED.")
    else:
        print("INVERTED INDEX HAVE NOT BEEN CREATED.")