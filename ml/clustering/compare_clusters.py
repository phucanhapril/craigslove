import os
import numpy as np
import json
from collections import Counter


"""
compare clusters across cities
"""

def main():
	all_words = []
	clusters_dir = 'cluster_data/city_samples_5000_4clusters'
	top_term_sets = {}
	for f in os.listdir(clusters_dir):
		if f.endswith('.json'): 
			city_name = f.split('_')[0]
			f_path = os.path.join(clusters_dir, f)
			with open(f_path,'r') as json_file:
				data = json.load(json_file)

				for c in data.keys():
					all_words.extend(data[c]['terms'])

				# print data['1']['terms']
				# print data['2']['terms']
				# print data['3']['terms']
				# print data['4']['terms']
				# do something

	c = Counter(all_words)
	print c
	print len(c)
	print 15*20

if __name__ == '__main__':
	main()