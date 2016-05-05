import os
import sys
import csv
import json
import re
import nltk
import time
import argparse
import pandas as pd
import numpy as np

import random
from sklearn.decomposition import PCA
from collections import defaultdict,Counter

import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.manifold import MDS

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.externals import joblib
from nltk.stem.snowball import SnowballStemmer
from sklearn.decomposition import RandomizedPCA


reload(sys)
sys.setdefaultencoding("utf-8")
"""
first create data using format_data.py

cluster.py will output clusters in json format to the cluster_data/ directory
"""


# reference: http://brandonrose.org/clustering

# which words are not interesting?
stopwords = ['guy', 'guys', 'girl', 'girls', 'woman', 'women', 'man', 'men', 'pics', 'pic', 'send', 'reply', 'good', 'age']

stemmer = SnowballStemmer("english")

def cluster(data_file, num_clusters):
	# read posts from file
	texts = []
	cities = []
	categories = []
	category_types = []
	types = []
	ages = []
	bodies = []
	statuses = []

	with open(data_file, 'r') as f:
		csv_reader = csv.reader(f)
		for city, title, text, category, post_type, age, body, status, zodiac in csv_reader:
			if not post_type:
				post_type = 'none'
			#save additional features TODO
			texts.append(text.decode('utf8'))
			cities.append(city)
			categories.append(category.lower())
			types.append(post_type.lower())
			category_types.append(category.lower() + ' - ' + post_type.lower())
			ages.append(age)
			bodies.append(body)
			statuses.append(status)
	print 'read ' + str(len(texts)) + ' posts'

	# for normalizing later
	totals = {}
	totals['city'] = Counter(cities)
	totals['category'] = Counter(categories)
	totals['category_type'] = Counter(category_types)
	totals['type'] = Counter(types)
	totals['age'] = Counter(ages)
	totals['body'] = Counter(bodies)
	totals['status'] = Counter(statuses)

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

	dist = 1 - cosine_similarity(tfidf_matrix)
	#print dist
	
	t3 = time.clock()
	km = MiniBatchKMeans(n_clusters=num_clusters, init='k-means++', n_init=1, init_size=1000, batch_size=1000, verbose=True)

	# km = KMeans(n_clusters=num_clusters, init='k-means++', max_iter=100, n_init=1,
	#            verbose=True))
	km.fit(tfidf_matrix)
	t4 = time.clock()
	print("KMeans fit: {} seconds.\n".format(t4 - t3))

	joblib.dump(km, 'doc_cluster.pkl')
	
	# save the km clusters so we dont recompute every time
	
	#km = joblib.load('doc_cluster.pkl')
	
	clusters = km.labels_.tolist()


	posts = {'cluster': clusters, 'category': categories, 'type': types, 'category_type' : category_types, \
		'city': cities, 'text': texts, 'age': ages, 'body': bodies, 'status': statuses }

	frame = pd.DataFrame(posts, index = [clusters] , columns = posts.keys())

	order_centroids = km.cluster_centers_.argsort()[:, ::-1]


	features_by_gram = defaultdict(list)
	for f, w in zip(tfidf_vectorizer.get_feature_names(), tfidf_vectorizer.idf_):
		features_by_gram[len(f.split(' '))].append((f, w))
	top_n = 3
	for gram, features in features_by_gram.iteritems():
		top_features = sorted(features, key=lambda x: x[1], reverse=True)[:top_n]
		top_features = [f[0] for f in top_features]
		print '{}-gram top:'.format(gram), top_features

	print order_centroids

	# convert clusters to json objects

	clusters_as_json = {}

	NUM_TOP_TERMS = 20
	NUM_TOP_FIELDS = 8

	# for plotting
	cluster_names = {}


	for i in range(num_clusters):
		cluster_json = {}

		#print order_centroids
		cluster_json['num_posts'] = len(frame.ix[i])

		# top terms
		top_terms = [ terms[j] for j in order_centroids[i, :NUM_TOP_TERMS]]
		cluster_json['terms'] = top_terms
		
		# cluster 'name' for plotting
		cluster_names[i] = top_terms[0] + " " + top_terms[1] + " " + top_terms[2]
		print cluster_names[i]
		
		for p in posts.keys():
			if p == 'cluster' or p == 'text':
				continue
			cluster_json[p] = get_top_normalized_counts(frame.ix[i][p].values.tolist(), totals[p], NUM_TOP_FIELDS)
		clusters_as_json[str(i+1)] = cluster_json


	##### SAVE TO FILE ####

	with open(get_cluster_filename_from_csv(data_file, num_clusters), 'w') as outfile:
		json.dump(clusters_as_json, outfile)

	##### PLOT #####
	plotting = True
	if plotting:
		MDS()

		# convert two components as we're plotting points in a two-dimensional plane
		# "precomputed" because we provide a distance matrix
		# we will also specify `random_state` so the plot is reproducible.
		mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

		pos = mds.fit_transform(dist)

		xs, ys = pos[:, 0], pos[:, 1]

		cluster_colors = {}
		r = lambda: random.randint(0,255)
		for n in range(num_clusters):
			cluster_colors[n] = '#%02X%02X%02X' % (r(),r(),r())

		#create data frame that has the result of the MDS plus the cluster numbers and titles
		df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, type=category_types)) 

		#group by cluster
		groups = df.groupby('label')

		# set up plot
		fig, ax = plt.subplots(figsize=(17, 9)) # set size
		ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

		#iterate through groups to layer the plot
		#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
		for name, group in groups:
			ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
					label=cluster_names[name], color=cluster_colors[name], 
					mec='none')
			ax.set_aspect('auto')
			ax.tick_params(\
				axis= 'x',          # changes apply to the x-axis
				which='both',      # both major and minor ticks are affected
				bottom='off',      # ticks along the bottom edge are off
				top='off',         # ticks along the top edge are off
				labelbottom='off')
			ax.tick_params(\
				axis= 'y',         # changes apply to the y-axis
				which='both',      # both major and minor ticks are affected
				left='off',      # ticks along the bottom edge are off
				top='off',         # ticks along the top edge are off
				labelleft='off')
			
		ax.legend(numpoints=1)  #show legend with only 1 point

		#add label in x,y position with the label as the film title
		for i in range(len(df)):
			ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['type'], size=8)  
			
		#plt.show()
		plt.savefig(get_plot_filename_from_csv(data_file, num_clusters), dpi=200)

def get_top_normalized_counts(values, total_counts, num):
	normalized = []
	for t,count in pd.value_counts(values).iteritems():
		normalized.append((t, count/float(total_counts[t])))
	return sorted(normalized, key=lambda tup: tup[1], reverse=True)[:num]

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

def get_cluster_filename_from_csv(csv_file_name, n):
	return 'cluster_data/' + csv_file_name.split('/')[-1:][0][:-4] + '_' + str(n) + '_clusters.json'

def get_plot_filename_from_csv(csv_file_name, n):
	return 'cluster_plot/' + csv_file_name.split('/')[-1:][0][:-4] + '_' + str(n) + '_clusters.png'


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-path', required=True, help='either a csv file OR a directory containing csv files')
	parser.add_argument('-c', required=True, help='number of clusters')
	opts = parser.parse_args()

	num_clusters = int(opts.c)

	# add english language stopwords from file
	with open('stopwords.txt') as f:
		stopwords.extend(f.read().splitlines())

	# process entire directory of csv files
	if os.path.isdir(opts.path):
		for f in os.listdir(opts.path):
			if f.endswith('.csv'): 
				file_path = os.path.join(opts.path, f)
				cluster(file_path, num_clusters)


	# process only one csv file
	elif os.path.isfile(opts.path) and opts.path.endswith('.csv'):
		cluster(opts.path, num_clusters)



	else:
		print 'error in ' + opts.path

if __name__ == '__main__':
	main()
