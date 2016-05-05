import os
import sys
import csv
"""
count the total number of posts in the results/ firectory

python count_posts.py results/

"""

def count_posts(csv_file):
	num = 0
	with open(csv_file,'r') as in_file:
		csv_reader = csv.reader(in_file)
		for line in csv_reader:
			num += 1
	return num - 1 # exclude column headers

def count_by_field(results_dir):
	count_by_type = {}

	if os.path.isdir(results_dir):
		for d in os.listdir(results_dir):
			city_dir = os.path.join(results_dir, d)
			if os.path.isdir(city_dir):
				city_total = 0
				for f in os.listdir(city_dir):
					if f.endswith('.csv'):
						with open(os.path.join(city_dir, f),'r') as in_file:
							csv_reader = csv.reader(in_file)
							for line in csv_reader:
								t = line[6].lower()
								if not t:
									t = 'none'
								if t not in count_by_type:
									count_by_type[t] = 0
								count_by_type[t] += 1
	with open('post_count_by_type.csv', 'w') as out_file:
		file_writer = csv.writer(out_file)
		for t in count_by_type:
			file_writer.writerow([t, count_by_type[t]])

def count_by_city(results_dir):
	total = 0
	cities = {}
	for d in os.listdir(results_dir):
		city_dir = os.path.join(results_dir, d)
		if os.path.isdir(city_dir):
			for f in os.listdir(city_dir):
				if f.endswith('.csv'):
					n = count_posts(os.path.join(city_dir, f))
					if d not in cities:
						cities[d] = 0
					cities[d] += n
					total += n
	print ''
	print 'TOTAL: ' + str(total)
	with open('post_count_by_city.csv', 'w') as out_file:
		file_writer = csv.writer(out_file)
		for c in cities:
			file_writer.writerow([c, cities[c]])

def main():
	if len(sys.argv) < 2:
		print 'Usage: python count_posts.py results/'
		return

	if os.path.isdir(sys.argv[1]):
		#count_by_field(sys.argv[1])
		count_by_city(sys.argv[1])
		pass
	else:
		print sys.argv[1] + ' is not a directory'





if __name__ == '__main__':
	main()
