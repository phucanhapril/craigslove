import os
import sys
import csv
import json
import re
from collections import Counter

"""

Usage: python count_word_freq.py <stopwords file> <results dir> <output json file>

"""
IMPORTANT_FREQUENCY_THRESHOLD = 1000
punc = re.compile(ur"[^\w\d'\s]+")
frequency_map = {}
stopwords = set()
# only keep big categories
categories = ["m4m", "m4w", "w4w", "w4m", "stp"]

POST_COUNT = 0

def increment():
    global POST_COUNT
    POST_COUNT = POST_COUNT+1

def clean_text(text):
	text = text.lower()
	text = punc.sub('', text) # remove all punctuation except apostrophe
	words = text.split()
	important_words = []
	for w in words:
		if w not in stopwords:
			fixed = w.replace("'", "") # can remove apostrophes now
			fixed = re.sub(r"\bfriends\b", "friend", fixed)
			fixed = re.sub(r"\bwomen\b", "woman", fixed)
			fixed = re.sub(r"\bmen\b", "man", fixed)
			important_words.append(fixed)
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
			if category not in categories:
				continue
			if not category in frequency_map:
				frequency_map[category] = []
			increment()
			# title text
			frequency_map[category] += clean_text(line[7])# append words form text or something
			# text body
			frequency_map[category] += clean_text(line[8])


def main():
	if len(sys.argv) < 4:
		print 'Usage: python count_word_freq.py <stopwords file> <results dir> <output json file>'
		return
	if not os.path.isfile(sys.argv[1]):
		print sys.argv[1] + ' is not a file'
		return
	if not os.path.isdir(sys.argv[2]):
		print sys.argv[2] + ' is not a directory'
		return

	with open(sys.argv[1], 'r') as f:
		for line in f:
			stopwords.add(line.rstrip('\n'))

	# process each csv in each subdirectory
	for d in os.listdir(sys.argv[2]):
		d_path = os.path.join(sys.argv[2], d)
		if os.path.isdir(d_path):
			for f in os.listdir(d_path):
				if f.endswith('.csv'): 
					process(os.path.join(d_path, f)) # populate frequency_map

	# grab top 10 words and frequencies
	output = []
	words_to_save = set()
	"""

	final format
	[
	{	word: "love"
		values: [{ category: m4w, value: 0.100 }, .. ]
	}, ...
	"""
	for category in frequency_map:
		obj = {}
		obj['name'] = category
		# get top 10 words and add them to words_to_save set
		common = Counter(frequency_map[category]).most_common(10)
		words_to_save.update([x[0] for x in common if x[1] > IMPORTANT_FREQUENCY_THRESHOLD])

	for w in words_to_save:
		obj = {}
		obj['word'] = w
		obj['values'] = []
		# get the value of word for each category
		for category in frequency_map:
			value_object = {}
			value_object['category'] = category
			value_object['value'] = word_value(w, frequency_map[category])
			obj['values'].append(value_object)
		output.append(obj)

	print str(POST_COUNT) + ' posts analyzed'
	with open(sys.argv[3], 'w') as outfile:
	    json.dump(output, outfile)


def word_value(word, wordlist):
	count = wordlist.count(word)
	return (count / (len(wordlist)*1.0))*100.0


if __name__ == '__main__':
	main()
