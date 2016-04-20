
import numpy as np
import re
import os
import csv
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib

"""
first run 'python format_data.py' to create formatted_posts.csv
"""


# reference: http://brandonrose.org/clustering


punc = re.compile(ur"[^\w\d'\s]+")
data_file = 'formatted_posts.csv' #'small_sample.csv'

# which words are not interesting?
stopwords = ['guy', 'guys', 'girl', 'girls', 'woman', 'women', 'man', 'men', 'pics', 'pic', 'send', 'reply', 'good', 'age']


def main():

	# read posts from file
	all_posts = []
	with open(data_file, 'r') as flattened:
		csv_reader = csv.reader(flattened)
		for line in csv_reader:
			all_posts.append(line[0])

	print 'read ' + str(len(all_posts)) + ' posts'

	# add english language stopwords from file
	with open('stopwords.txt') as f:
		stopwords.extend(f.read().splitlines())
	
	#define vectorizer parameters
	tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
									 min_df=0.1, stop_words=stopwords,
									 use_idf=True, tokenizer=tokenize, ngram_range=(1,3))

	tfidf_matrix = tfidf_vectorizer.fit_transform(all_posts) #fit the vectorizer to synopses

	print tfidf_matrix.shape

	terms = tfidf_vectorizer.get_feature_names() #a list of the features used in the tf-idf matrix
	
	print terms

	#dist = 1 - cosine_similarity(tfidf_matrix)

	num_clusters = 2

	km = KMeans(n_clusters=num_clusters)

	km.fit(tfidf_matrix)
	
	# save the km clusters so we dont recompute every time
	joblib.dump(km, 'doc_cluster.pkl')
	#km = joblib.load('doc_cluster.pkl')

	clusters = km.labels_.tolist()

	order_centroids = km.cluster_centers_.argsort()[:, ::-1]
	for i in range(num_clusters):
		print ''
		print 'top terms for cluster ' + str(i+1) + ':'
		for j in order_centroids[i, :8]:
			print terms[j]

def tokenize(text):
	text = text.lower()
	text = punc.sub('', text) # remove all punctuation except apostrophe
	return text.split()

if __name__ == '__main__':
	main()
