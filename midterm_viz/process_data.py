import os
import sys
import csv
import re
from collections import Counter

"""
write top 10 most frequent words per category to output file 'frequencies.csv'

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
		return search_type
	return category #stp

def process(file):

	with open(file,'r') as in_file:
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
		print 'Usage: python process_data.py ../results/'
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

	# convert frequency map to lists for csv
	output_rows = []
	for category in frequency_map:
		r = [category]
		# get top 10 words
		common = Counter(frequency_map[category]).most_common(10)
		if len(common) == 10:
			for w in common:
				r.append(w[0]) # word
				r.append(w[1]) # frequency
			output_rows.append(r)

	# write results
	with open('frequencies.csv', 'w') as out_file:
		csv_writer = csv.writer(out_file)
		csv_writer.writerows(output_rows)


if __name__ == '__main__':
	main()
