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

from collections import defaultdict, Counter

import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.externals import joblib
from sklearn.decomposition import RandomizedPCA, PCA
from nltk.stem.snowball import SnowballStemmer


reload(sys)
sys.setdefaultencoding("utf-8")
"""
first create data/ using format_data.py

example to run:
python cluster.py -path data/city/sample/providence.csv -c 2 -plot True
or
python cluster.py -path data/city/sample -c 2 -plot True

saves output to cluster_data/
"""


# reference: http://brandonrose.org/clustering

# which words are not interesting?	
stopwords = ['male', 'female', 'guy', 'guys', 'girl', 'girls', 'woman', 'women', 'man', 'men', 'year', 'age', 'good', 'send', 'seek','seeking', 'find', 'thing', 'go' ,'great', 'time', 'email', 'subject', 'reply']#, 'send', 'reply', 'good', 'time', 'age', 'thing', 'seek', 'find']

stemmer = SnowballStemmer("english")

def cluster(data_file, num_clusters, plot_flag):
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
	print 'read {} posts from {}'.format(len(texts), data_file)

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
	tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=200000,
									 min_df=0.05, #stop_words=stopwords,
									 use_idf=True, tokenizer=tokenize)#, ngram_range=(1))

	tfidf_matrix = tfidf_vectorizer.fit_transform(texts) #fit the vectorizer to texts
	t2 = time.clock()
	print("TfidfVectorizer fit_transform: {} seconds.\n".format(t2 - t1))
	print tfidf_matrix.shape

	terms = tfidf_vectorizer.get_feature_names() #a list of the features used in the tf-idf matrix
	
	print terms

	t3 = time.clock()
	
	km = MiniBatchKMeans(n_clusters=num_clusters, init='k-means++', batch_size=1000, verbose=True)
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

	# print top grams
	features_by_gram = defaultdict(list)
	for f, w in zip(tfidf_vectorizer.get_feature_names(), tfidf_vectorizer.idf_):
		features_by_gram[len(f.split(' '))].append((f, w))
	top_n = 5
	for gram, features in features_by_gram.iteritems():
		top_features = sorted(features, key=lambda x: x[1], reverse=True)[:top_n]
		top_features = [f[0] for f in top_features]
		print '{}-gram top:'.format(gram), top_features

	# convert clusters to json objects

	clusters_as_json = {}

	NUM_TOP_TERMS = 40
	NUM_TOP_FIELDS = 20

	# for plotting
	cluster_names = {}


	for i in range(num_clusters):
		cluster_json = {}

		cluster_json['num_posts'] = len(frame.ix[i])

		# top terms
		top_terms = [ terms[j] for j in order_centroids[i, :NUM_TOP_TERMS]]
		cluster_json['terms'] = top_terms
		
		# cluster 'name' for plotting
		cluster_names[i] = '{}, {}, {}, {}'.format(top_terms[0], top_terms[1], top_terms[2], top_terms[3])
		print cluster_names[i]
		
		for p in posts.keys():
			if p == 'cluster' or p == 'text':
				continue
			cluster_json[p] = get_top_normalized_counts(frame.ix[i][p].values.tolist(), totals[p], NUM_TOP_FIELDS)
		clusters_as_json[str(i+1)] = cluster_json


	##### SAVE TO FILE ####

	out_file = get_cluster_filename_from_csv(data_file, num_clusters)
	print 'saving to {}'.format(out_file)
	with open(out_file, 'w') as f:
		json.dump(clusters_as_json, f)

	##### PLOT #####

	if plot_flag:

		# we're plotting the cosine similarities!
		print 'PLOTTING'
		cos = cosine_similarity(tfidf_matrix.astype(np.float64))
		print cos.shape
		dist = 1 - cos

		pca = PCA(n_components=2)
		pos = pca.fit_transform(dist.astype(np.float64))
		xs, ys = pos[:, 0], pos[:, 1]

		cluster_colors = {}
		chosen_colors = [ '#00b159', '#f37735', '#00aedb', '#ffc425', '#d11141']
		r = lambda: random.randint(0,255)
		for n in range(num_clusters):
			if n < len(chosen_colors):
				cluster_colors[n] = chosen_colors[n]
			else:
				cluster_colors[n] = '#%02X%02X%02X' % (r(),r(),r())

		df = pd.DataFrame(dict(x=xs, y=ys, label=clusters))#, type=titles)) 

		#group by cluster
		groups = df.groupby('label')

		# set up plot
		fig, ax = plt.subplots(figsize=(17, 9)) # set size
		ax.margins(0.05)

		for name, group in groups:
			ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
					label=cluster_names[name], color=cluster_colors[name], 
					mec='none')
			ax.set_aspect('auto')
			# turn off x and y axes
			ax.tick_params(\
				axis= 'x',
				which='both',
				bottom='off',
				top='off',
				labelbottom='off')
			ax.tick_params(\
				axis= 'y',
				which='both',
				left='off',
				top='off',
				labelleft='off')
			
		ax.legend(numpoints=1)  #show legend with only 1 point

		#add labels to each point
		# for i in range(len(df)):
		# 	ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['type'], size=8)  
			
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
		# the only numerical word that we want to keep is 420. The rest are ages, heights, weights, etc
		if re.search('[a-zA-Z]', token) or token == '420':
			if token not in stopwords:
				stem = stemmer.stem(token)
				if stem not in stopwords:
					if stem == 'pictur':
						stem = 'pic' # group these together because they both appear a lot and mean the same thing
					filtered_tokens.append(stem)
				#else:
				#	print token + ' ' + stem
	return filtered_tokens

def get_cluster_filename_from_csv(csv_file_name, n):
	return 'cluster_data/cities_2means/{}_{}_clusters.json'.format(csv_file_name.split('/')[-1:][0][:-4], n)

def get_plot_filename_from_csv(csv_file_name, n):
	return 'cluster_plot/cities_2means/{}_{}_clusters.png'.format(csv_file_name.split('/')[-1:][0][:-4], n)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-path', required=True, help='either a csv file OR a directory containing csv files')
	parser.add_argument('-c', required=True, help='number of clusters')
	parser.add_argument('-plot', required=False, help='plot data and save png')
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
				cluster(file_path, num_clusters, opts.plot)


	# process only one csv file
	elif os.path.isfile(opts.path) and opts.path.endswith('.csv'):
		cluster(opts.path, num_clusters, opts.plot)



	else:
		print 'error in ' + opts.path

if __name__ == '__main__':
	main()
