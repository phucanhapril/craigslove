
import numpy as np
import re
import os
import csv
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.externals import joblib

# reference: http://brandonrose.org/clustering


punc = re.compile(ur"[^\w\d'\s]+")
results_dir = '../../results'
output_file = 'providence_tokenized_posts.csv' #'small_sample.csv'

# which words are not interesting?
personals_stopwords = ['guy', 'guys', 'girl', 'girls', 'woman', 'women', 'man', 'men', 'pics', 'pic', 'send', 'reply', 'good', 'age']



def flatten_results():
	# process each csv in each subdirectory
	posts_to_write = []

	for d in os.listdir(results_dir):
		d_path = os.path.join(results_dir, d)
		if os.path.isdir(d_path):
			print d_path
			for f in os.listdir(d_path):
				if f.endswith('.csv'): 
					csv_file = os.path.join(d_path, f)
					with open(csv_file,'r') as in_file:
						next(in_file)
						csv_reader = csv.reader(in_file)
						for line in csv_reader:
							# extract only the content we want
							content = []
							content.append(line[1]) #city
							content.append(line[8]) #text
							posts_to_write.append(content)

	print ' saving ' + str(len(posts_to_write)) + ' posts'
	with open(output_file, 'w') as out_file:
		csv_writer = csv.writer(out_file)
		for p in posts_to_write:
			csv_writer.writerow(p)
	return posts_to_write

def main():
	# TODO have a 'group by' variable that corresponds to a column -- so we can switch between city and category
	# also a sub-group-by

	#all_posts = flatten_results() # returns posts AND SAVES THEM TO A CSV FILE
	
	all_posts = []
	post_count = 0
	with open(output_file, 'r') as flattened:
		csv_reader = csv.reader(flattened)
		for line in csv_reader:
			all_posts.append(line[1])
			post_count += 1
			#if post_count > 10000:
			#	break #TEMP limit because running out of space


	with open('stopwords.txt') as f:
		stopwords = f.read().splitlines()

	stopwords = stopwords + personals_stopwords
	
	#define vectorizer parameters
	tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
									 min_df=0.1, stop_words=stopwords,
									 use_idf=True, tokenizer=tokenize, ngram_range=(1,3))

	tfidf_matrix = tfidf_vectorizer.fit_transform(all_posts) #fit the vectorizer to synopses

	print tfidf_matrix.shape

	terms = tfidf_vectorizer.get_feature_names() #a list of the features used in the tf-idf matrix
	print terms

	dist = 1 - cosine_similarity(tfidf_matrix)

	num_clusters = 2

	km = KMeans(n_clusters=num_clusters)

	km.fit(tfidf_matrix)
	
	# save the km clusters so we dont recompute every time
	joblib.dump(km, 'doc_cluster.pkl')
	#km = joblib.load('doc_cluster.pkl')

	clusters = km.labels_.tolist()

	order_centroids = km.cluster_centers_.argsort()[:, ::-1]
	for i in range(num_clusters):
		print 'top terms for cluster ' + str(i+1) + ':'
		for ind in order_centroids[i, :8]:
			print terms[ind]
		print ''

def tokenize(text):
	text = text.lower()
	text = punc.sub('', text) # remove all punctuation except apostrophe
	return text.split()

if __name__ == '__main__':
	main()
