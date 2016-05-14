import os
import numpy as np
import json
from collections import Counter

"""
for each city calculate: which percent of posts fall in 'sex' cluster,
and which percent of posts fall in 'love and friendship' cluster
"""

INPUT_FILE = '../cluster_data/all_city_clusters.json'
OUTPUT_FILE = '../cluster_data/all_city_clusters_w_percentages.json'

def main():
	all_clusters = []

	with open(INPUT_FILE,'r') as json_file:
		data = json.load(json_file)
		seen = set()
		# for every cluster in this file
		for c in data:
			name = c['cluster_name']
			city = c['city']
			num_posts_1 = c['num_posts']
			if city in seen:
				print 'continue'
				continue
			# find other cluster in this city to calculate proportion
			for c2 in data:
				if c2['city'] == city and c2['cluster_name'] != name:
					num_posts_2 = c2['num_posts']
					num_posts_total = float(num_posts_1 + num_posts_2)
					print num_posts_total
					c['percent_posts'] = num_posts_1 / num_posts_total
					c2['percent_posts'] = num_posts_2 / num_posts_total
					seen.add(city)

	with open(OUTPUT_FILE, 'w') as f:
		json.dump(data, f)

if __name__ == '__main__':
	main()