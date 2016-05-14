import numpy as np
import re
import os
import csv
import nltk
import time
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""

***** see cluster.py file for info about the actual clustering *****

this is for calculating inertias in order to use the 'elbow method'

"""

# reference: http://brandonrose.org/clustering


punc = re.compile(ur"[^\w\d'\s]+")
data_file = 'formatted_posts_all.csv' #'small_sample.csv'

# which words are not interesting
stopwords = ['male', 'female', 'guy', 'guys', 'girl', 'girls', 'woman', 'women', 'man', 'men', 'year', 'age', 'good', 'send', 'seek','seeking', 'find', 'thing', 'go' ,'great', 'time', 'email', 'subject', 'reply']

stemmer = SnowballStemmer("english")

def calculate_inertias(data_file, min_clusters, max_clusters):
    # read posts from file
    texts = []
    cities = []
    categories = []
    types = []
    with open(data_file, 'r') as f:
        csv_reader = csv.reader(f)
        for line in csv_reader:
            # line format [text, city, category, posttype]
            texts.append(line[0].decode('utf8'))
            cities.append(line[1])
            categories.append(line[2])
            types.append(line[2] + ' - ' + line[3])
    print 'read ' + str(len(texts)) + ' posts'

    #define vectorizer parameters
    t1 = time.clock()
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                     min_df=0.1, #stop_words=stopwords,
                                     use_idf=True, tokenizer=tokenize, ngram_range=(1,3))

    tfidf_matrix = tfidf_vectorizer.fit_transform(texts) #fit the vectorizer to texts
    t2 = time.clock()
    print("TfidfVectorizer fit_transform: {} seconds.\n".format(t2 - t1))
    print tfidf_matrix.shape

    terms = tfidf_vectorizer.get_feature_names() #a list of the features used in the tf-idf matrix
    
    x_axis = np.arange(min_clusters, max_clusters + 1, 1)
    y_axis = []
    inertias = defaultdict(float)
    
    for num_clusters in range(min_clusters, max_clusters + 1):
        t3 = time.clock()
        km = KMeans(n_clusters=num_clusters)
        km.fit(tfidf_matrix)
        t4 = time.clock()
        print("KMeans fit: {} seconds.\n".format(t4 - t3))

        inertias[num_clusters] = km.inertia_
        y_axis.append(km.inertia_)
    
    print 'inertias'
    print inertias
    
    plt.plot(x_axis, y_axis)

def tokenize(text):
    # first tokenize by sentence, then by word
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (raw punctuation)
    for token in tokens:
        # the only numerical word that we want to keep is 420. The rest are ages, heights, weights, etc
        if re.search('[a-zA-Z]', token) or token == '420':
            if token not in stopwords:
                stem = stemmer.stem(token)
                if stem not in stopwords:
                    if stem == 'pictur':
                        stem = 'pic' # group these together because they both appear a lot and mean the same thing
                    filtered_tokens.append(stem)

    return filtered_tokens

def main():
    if len(sys.argv) < 2:
        print 'Usage: python cluster.py file.csv'
        return

    # add english language stopwords from file
    with open('util/stopwords.txt') as f:
        stopwords.extend(f.read().splitlines())

    calculate_inertias(sys.argv[1], 1, 5)

if __name__ == '__main__':
    main()
