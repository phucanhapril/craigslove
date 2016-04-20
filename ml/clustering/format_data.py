import os
import csv

"""
format data for clustering
"""

results_dir = '../../results'
output_file = 'formatted_posts.csv'

def main():
	# process each csv in each subdirectory
	posts_to_write = []

	for d in os.listdir(results_dir):
		d_path = os.path.join(results_dir, d)
		if os.path.isdir(d_path):
			print d_path
			if 'sfbay' in d_path: # ONLY PROVIDENCE REST IS TOO BIG
				for f in os.listdir(d_path):
					if f.endswith('.csv'): 
						csv_file = os.path.join(d_path, f)
						with open(csv_file,'r') as in_file:
							next(in_file)
							csv_reader = csv.reader(in_file)
							for line in csv_reader:
								# extract only the content we want
								# content = []
								# content.append(line[1]) #city
								# content.append(line[8]) #text
								posts_to_write.append([line[8]]) #text

	print ' saving ' + str(len(posts_to_write)) + ' posts'
	with open(output_file, 'w') as out_file:
		csv_writer = csv.writer(out_file)
		for p in posts_to_write:
			csv_writer.writerow(p)
	return posts_to_write

if __name__ == '__main__':
	main()
