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
	return num

def main():
	if len(sys.argv) < 2:
		print 'Usage: python count_posts.py results/'
		return
	total = 0
	if os.path.isdir(sys.argv[1]):
		for d in os.listdir(sys.argv[1]):
			city_dir = os.path.join(sys.argv[1], d)
			if os.path.isdir(city_dir):
				city_total = 0
				for f in os.listdir(city_dir):
					if f.endswith('.csv'):
						n = count_posts(os.path.join(city_dir, f))
						city_total += n
						total += n
				print city_dir + ': ' + str(city_total)
		print 'total posts: ' + str(total)
	else:
		print sys.argv[1] + ' is not a directory'




if __name__ == '__main__':
	main()
