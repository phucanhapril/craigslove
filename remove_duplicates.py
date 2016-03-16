import os
import sys
import csv
"""
remove duplicate postings form csv files

how to run:
python remove_duplicates <directory of csv files>

ex: python remove_duplicates.py results/providence



"""
def remove_dups(csv_file):
	outfilename = 'temp.csv'
	with open(csv_file,'r') as in_file, open(outfilename,'w') as out_file:
		seen = set() # set for fast O(1) amortized lookup
		csv_writer = csv.writer(out_file)
		csv_reader = csv.reader(in_file)
		dup_count = 0
		for line in csv_reader:
			# first item is the unique url
			if line[0] in seen:
				dup_count += 1
				continue # skip duplicate

			seen.add(line[0])
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


	for f in os.listdir(sys.argv[1]):
		if f.endswith('.csv'): 
			remove_dups(sys.argv[1] + '/' + f)
		else:
			continue



if __name__ == '__main__':
	main()
