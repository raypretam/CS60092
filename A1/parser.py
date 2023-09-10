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

def extract_qry(file):
    """Extract the data as a python dictionary"""
    data = {}
    with open(file) as f:
        articles = f.read().split('\n.I')
        # print(articles)
    data = {(i+1):process(article) for i,article in enumerate(articles)}
    return data

def process(article):
    id = article.split('\n.W\n')[0].strip()
    article = article.split('\n.W\n')[1]
    # T, _, article = article.partition('\n.A\n')
    # A, _, article = article.partition('\n.B\n')
    W, _, _ = article.partition('\n.W\n')
    return {'id':id, 'W':W}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    cran_qry_file = Path(args.path)
    qry = extract_qry(cran_qry_file)
    with open(f"queries_{ROLL_NO}.txt", "w") as f:
        for _, v in qry.items():
            id = v['id']
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
            f.write(id)
            f.write("\t")
            f.write(filtered_sentence)
            f.write("\n")
    if os.path.exists(f"queries_{ROLL_NO}.txt") == True:
        print("QUERIES HAVE BEEN PARSED.")
    else:
        print("QUERIES HAVE NOT BEEN PARSED.")
    

