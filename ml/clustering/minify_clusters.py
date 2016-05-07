import os
import numpy as np
import json
from collections import Counter

"""
group all clutsres from each city into a single file and save it
then we can go through manually and attach titles
"""

OUTPUT_FILE = 'cluster_data/all_city_clusters_m.json'
INPUT_DIR = 'cluster_data/cities_2means'

def main():
	all_words = []
	all_clusters = []

	for f in os.listdir(INPUT_DIR):

		if f.endswith('.json'): 
			city_name = f.split('_')[0]
			f_path = os.path.join(INPUT_DIR, f)

			with open(f_path,'r') as json_file:
				data = json.load(json_file)
				# for every cluster in thie file
				for c in data.keys():
					all_words.extend(data[c]['terms'])
					minified = {}
					minified['city'] = city_name
					minified['name'] = '' # TO FILL IN MANUALLY
					minified['terms'] = data[c]['terms']
					all_clusters.append(minified)

	with open(OUTPUT_FILE, 'w') as f:
		json.dump(all_clusters, f)


	c = Counter(all_words)
	print c

if __name__ == '__main__':
	main()