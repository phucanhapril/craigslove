import numpy as np
import re
import os
import csv
import nltk
# import pandas as pd
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
first create data using format_data.py
"""


# reference: http://brandonrose.org/clustering


punc = re.compile(ur"[^\w\d'\s]+")
data_file = 'formatted_posts_all.csv' #'small_sample.csv'

# which words are not interesting?
stopwords = ['guy', 'guys', 'girl', 'girls', 'woman', 'women', 'man', 'men', 'pics', 'pic', 'send', 'reply', 'good', 'age']

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
    
    print terms

    dist = 1 - cosine_similarity(tfidf_matrix) #TODO look at this
    print dist
    
    x_axis = np.arange(min_clusters, max_clusters + 1, 1)
    y_axis = []
    inertias = defaultdict(float)
    
    for num_clusters in range(min_clusters, max_clusters + 1):
        t3 = time.clock()
        km = KMeans(n_clusters=num_clusters)
        km.fit(tfidf_matrix)
        t4 = time.clock()
        print("KMeans fit: {} seconds.\n".format(t4 - t3))

        joblib.dump(km, 'doc_cluster.pkl')
        
        # save the km clusters so we dont recompute every time
        """
        km = joblib.load('doc_cluster.pkl')
        """
        clusters = km.labels_.tolist()

        posts = {'category': categories, 'type': types, 'city': cities, 'text': texts, 'cluster': clusters }

        # frame = pd.DataFrame(posts, index = [clusters] , columns = ['cluster', 'category', 'type', 'city', 'text'])
        # print frame['cluster'].value_counts()

        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        for i in range(num_clusters):
            print ''
            print ' CLUSTER ' + str(i+1)

            # TOP TERMS
            print ''
            print '~ terms ~'
            for j in order_centroids[i, :10]:
                print terms[j]
            
            # TOP TYPES
            print ''
            print '~ types ~'
            # types = frame.ix[i]['type'].values.tolist()
            # print pd.value_counts(types)[:4]

            # TOP CATEGORIES
            print ''
            print '~ categories ~'
            # categories = frame.ix[i]['category'].values.tolist()
            # print pd.value_counts(categories)[:4]

            # TOP CITIES
            print ''
            print '~ cities ~'
            # cities = frame.ix[i]['city'].values.tolist()
            # print pd.value_counts(cities)[:4]
            #TODO write results to file! so can visualize/compare
        
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
        if re.search('[a-zA-Z0-9]', token):
            if token not in stopwords:
                filtered_tokens.append(stemmer.stem(token))
    return filtered_tokens

def main():
    if len(sys.argv) < 2:
        print 'Usage: python cluster.py file.csv'
        return

    # add english language stopwords from file
    with open('stopwords.txt') as f:
        stopwords.extend(f.read().splitlines())

    calculate_inertias(sys.argv[1], 1, 5) # TODO return results and write to file

if __name__ == '__main__':
    main()
