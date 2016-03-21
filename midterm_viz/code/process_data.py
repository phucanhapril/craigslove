import os
import sys
import csv
import json
import re
from collections import Counter

"""
write top 10 most frequent words per category to output file 'frequencies.json'

Usage: python process_data.py ../results/

"""

punc = re.compile(ur"[^\w\d'\s]+")
stopword_file = 'stopwords.txt'
frequency_map = {}
stopwords = set()

def clean_text(text):
	text = text.lower()
	text = punc.sub('', text) # remove all punctuation except apostrophe
	words = text.split()
	important_words = []
	for w in words:
		if w not in stopwords:
			important_words.append(w.replace("'", "")) # can remove apostrophes now
	return important_words

def get_category(category, search_type):
	if category == 'msr' and not search_type:
		return category
	if category == 'msr' and search_type:
		return search_type.lower()
	return category #stp

def process(f):
	print 'processing ' + f
	with open(f,'r') as in_file:
		next(in_file)
		seen = set()
		csv_reader = csv.reader(in_file)
		for line in csv_reader:
			if line[0] in seen:
				continue # skip duplicate URLs
			seen.add(line[0])

			category = get_category(line[5], line[6])
			
			if not category in frequency_map:
				frequency_map[category] = []

			# title text
			frequency_map[category] += clean_text(line[7])# append words form text or something
			# text body
			frequency_map[category] += clean_text(line[8])


def main():
	if len(sys.argv) < 2:
		print 'Usage: python process_data.py ../../results/'
		return

	with open(stopword_file, 'r') as f:
		for line in f:
			stopwords.add(line.rstrip('\n'))

	# process each csv in each subdirectory
	for d in os.listdir(sys.argv[1]):
		d_path = os.path.join(sys.argv[1], d)
		if os.path.isdir(d_path):
			for f in os.listdir(d_path):
				if f.endswith('.csv'): 
					process(os.path.join(d_path, f)) # populate frequency_map



	# grab top 10 words and frequencies
	output = []
	#TODO calculate TF-IDF http://www.tfidf.com/
	for category in frequency_map:
		obj = {}
		obj['name'] = category
		# get top 10 words
		common = Counter(frequency_map[category]).most_common(10)
		if len(common) == 10:
			obj['frequencies'] = []
			
			for w in common:
				item = {}
				item['word'] = w[0]
				item['count'] = w[1]
				obj['frequencies'].append(item)

			output.append(obj)

	with open('../data/frequencies.json', 'w') as outfile:
	    json.dump(output, outfile)


if __name__ == '__main__':
	main()
