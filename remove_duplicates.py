import os
import sys
import csv
import string
"""
remove duplicate postings form csv files

how to run:
python remove_duplicates <directory of csv files>

ex: python remove_duplicates.py results/providence



"""
def jaccard_similarity(wordset1, wordset2):
    x = len(wordset1.intersection(wordset2))
    y = len(wordset1.union(wordset2))
    return x / float(y)

def normalize(s):
    for p in string.punctuation:
        s = s.replace(p, '')
    return s.lower().strip()

def remove_dups(csv_file):
	outfilename = 'temp.csv'
	with open(csv_file,'r') as in_file, open(outfilename,'w') as out_file:
		seen = set()
		seen_texts = set()
		csv_writer = csv.writer(out_file)
		csv_reader = csv.reader(in_file)
		dup_count = 0
		for line in csv_reader:
			url = line[0]
			text = line[8]
			if url in seen:
				dup_count += 1
			elif normalize(text) in seen_texts:
				# TODO jaccard or something; still missing some posters re-posting similar messages
				dup_count += 1
			else:
				seen.add(url)
				seen_texts.add(normalize(text))
				csv_writer.writerow(line)

	print csv_file + ': ' + str(dup_count) + ' duplicate rows removed'
	# delete old file
	os.remove(csv_file)
	# rename new file
	os.rename(outfilename, csv_file)

def main():
	if len(sys.argv) < 2:
		print 'Usage: python remove_duplicates.py results/newyork'
		return

	if os.path.isdir(sys.argv[1]):
		for f in os.listdir(sys.argv[1]):
			if f.endswith('.csv'):
				remove_dups(os.path.join(sys.argv[1], f))
	else:
		print sys.argv[1] + ' is not a directory'




if __name__ == '__main__':
	main()
